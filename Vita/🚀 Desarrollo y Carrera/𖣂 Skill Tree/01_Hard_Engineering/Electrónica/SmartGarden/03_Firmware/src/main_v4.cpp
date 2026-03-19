#include <Arduino.h>
#include <WiFi.h>
#include <SPIFFS.h>
#include <ArduinoJson.h>
#include "driver/adc.h"
#include "esp_sleep.h"
#include "DHTesp.h"

#include "TensorFlowLite_ESP32.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "model_data.h"   // brain_v4_tflite

// ==========================================
// 🔌 MAPA DE CONEXIONES
// ==========================================
#define PIN_DHT    4
#define PIN_SUELO  34
#define PIN_BATERIA 32
#define PIN_LUZ    18
#define PIN_FAN    19
#define PIN_BOMBA  21

// ==========================================
// ⚙️  CALIBRACIÓN — sensores
// ==========================================
const int SUELO_SECO   = 3500;
const int SUELO_MOJADO = 1500;

// ==========================================
// ⚙️  CULTIVO ACTIVO
// Se carga desde SPIFFS/Perfiles_Cultivo.json.
// Si el archivo no existe, usa estos fallbacks.
// ==========================================
float TARGET_TEMP = 24.0;
float TARGET_HUM  = 60.0;

// ==========================================
// ⚙️  UMBRALES DE DECISIÓN
// ==========================================
const float TH_LUZ   = 0.60;
const float TH_FAN   = 0.55;
const float TH_RIEGO = 0.65;
const float TH_SLEEP = 0.50;

#define TIEMPO_DORMIR_US (30ULL * 60ULL * 1000000ULL)

// ==========================================
// ⚙️  TFLite
// ==========================================
const int kTensorArenaSize = 12 * 1024;  // ajusta según el notebook
uint8_t tensor_arena[kTensorArenaSize];

// ==========================================
// OBJETOS GLOBALES
// ==========================================
DHTesp dht;
bool sistema_listo = false;

tflite::MicroErrorReporter* error_reporter = nullptr;
const tflite::Model*        model          = nullptr;
tflite::MicroInterpreter*   interpreter    = nullptr;
TfLiteTensor* input  = nullptr;
TfLiteTensor* output = nullptr;
static tflite::MicroMutableOpResolver<6> micro_op_resolver;

// ==========================================
// FUNCIONES AUXILIARES
// ==========================================
float leerBateria() {
    int raw = analogRead(PIN_BATERIA);
    float voltaje = (raw / 4095.0) * 3.3 * 2.0;
    float pct;
    if      (voltaje >= 4.2) pct = 100.0;
    else if (voltaje <= 3.3) pct = 0.0;
    else                     pct = (voltaje - 3.3) / (4.2 - 3.3) * 100.0;
    return constrain(pct, 0.0, 100.0);
}

float leerSuelo() {
    long suma = 0;
    for (int i = 0; i < 10; i++) { suma += analogRead(PIN_SUELO); delay(5); }
    int pct = map(suma / 10, SUELO_SECO, SUELO_MOJADO, 0, 100);
    return constrain(pct, 0.0, 100.0);
}

// Hora simulada con millis() hasta tener RTC
// Arranca en 8am y avanza en tiempo real
float horaActual() {
    float hora = 8.0 + (millis() / 3600000.0);
    return fmod(hora, 24.0);
}

// ---------------------------------------------------------
// CARGAR CULTIVO DESDE JSON EN SPIFFS
//
// Uso:
//   Sube Perfiles_Cultivo.json a SPIFFS con:
//     Arduino IDE → Tools → ESP32 Sketch Data Upload
//   o con PlatformIO:
//     pio run --target uploadfs
//
// El archivo debe estar en /data/Perfiles_Cultivo.json
// El nombre del cultivo se define en CULTIVO_ACTIVO abajo.
// ---------------------------------------------------------
#define CULTIVO_ACTIVO "Tomato"   // ← cambia aquí para cambiar de cultivo

bool cargarCultivo(const char* nombre) {
    if (!SPIFFS.begin(true)) {
        Serial.println("⚠️  SPIFFS no disponible — usando fallback");
        return false;
    }

    File f = SPIFFS.open("/Perfiles_Cultivo.json", "r");
    if (!f) {
        Serial.println("⚠️  Perfiles_Cultivo.json no encontrado — usando fallback");
        return false;
    }

    // ArduinoJson — añade a platformio.ini: lib_deps = bblanchon/ArduinoJson
    StaticJsonDocument<2048> doc;
    DeserializationError err = deserializeJson(doc, f);
    f.close();

    if (err) {
        Serial.printf("⚠️  JSON inválido: %s — usando fallback\n", err.c_str());
        return false;
    }

    JsonArray cultivos = doc["cultivos"];
    for (JsonObject c : cultivos) {
        if (strcmp(c["id_cultivo"], nombre) == 0) {
            TARGET_TEMP = c["parametros_optimos"]["temperatura_ideal"].as<float>();
            TARGET_HUM  = c["parametros_optimos"]["humedad_suelo_ideal"].as<float>();
            Serial.printf("✅ Cultivo cargado: %s — %.1f°C / %.0f%%\n",
                          nombre, TARGET_TEMP, TARGET_HUM);
            return true;
        }
    }

    Serial.printf("⚠️  '%s' no encontrado en JSON — usando fallback\n", nombre);
    return false;
}

// ==========================================
// SETUP
// ==========================================
void setup() {
    Serial.begin(115200);
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db);

    pinMode(PIN_LUZ,   OUTPUT); digitalWrite(PIN_LUZ,   LOW);
    pinMode(PIN_FAN,   OUTPUT); digitalWrite(PIN_FAN,   LOW);
    pinMode(PIN_BOMBA, OUTPUT); digitalWrite(PIN_BOMBA, LOW);

    dht.setup(PIN_DHT, DHTesp::DHT22);

    // Cargar parámetros del cultivo activo
    cargarCultivo(CULTIVO_ACTIVO);
    // Si falla → TARGET_TEMP y TARGET_HUM mantienen sus valores por defecto

    // ── TFLite ──────────────────────────────────────────
    static tflite::MicroErrorReporter micro_error_reporter;
    error_reporter = &micro_error_reporter;

    model = tflite::GetModel(brain_v4_tflite);
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        Serial.println("❌ Modelo incompatible");
        return;
    }

    micro_op_resolver.AddFullyConnected();
    micro_op_resolver.AddRelu();
    micro_op_resolver.AddLogistic();
    micro_op_resolver.AddAdd();
    micro_op_resolver.AddQuantize();
    micro_op_resolver.AddDequantize();

    static tflite::MicroInterpreter static_interpreter(
        model, micro_op_resolver, tensor_arena, kTensorArenaSize, error_reporter
    );
    interpreter = &static_interpreter;

    if (interpreter->AllocateTensors() != kTfLiteOk) {
        Serial.println("❌ Arena insuficiente — sube kTensorArenaSize");
        return;
    }

    input  = interpreter->input(0);
    output = interpreter->output(0);

    if (input->dims->data[1] != 6) {
        Serial.printf("❌ Modelo espera %d inputs, código usa 6\n",
                      input->dims->data[1]);
        return;
    }

    sistema_listo = true;
    Serial.printf("✅ SmartGarden ONLINE — %s (%.1f°C / %.0f%% hum objetivo)\n",
                  CULTIVO_ACTIVO, TARGET_TEMP, TARGET_HUM);
}

// ==========================================
// LOOP
// ==========================================
void loop() {
    if (!sistema_listo) {
        Serial.println("⛔ Sistema no inicializado.");
        delay(5000);
        return;
    }

    float temperatura = dht.getTemperature();
    float hum_suelo   = leerSuelo();
    float bateria     = leerBateria();
    float hora        = horaActual();

    if (isnan(temperatura) || temperatura < -10 || temperatura > 60) {
        temperatura = TARGET_TEMP;
        Serial.println("⚠️  DHT22 error — usando TARGET_TEMP");
    }

    Serial.printf("\n🌱 [%s] %.1fh | Temp: %.1f°C (obj %.1f) | "
                  "Suelo: %.0f%% (obj %.0f) | Bat: %.0f%%\n",
                  CULTIVO_ACTIVO, hora,
                  temperatura, TARGET_TEMP,
                  hum_suelo, TARGET_HUM,
                  bateria);

    // ── IA INPUT — 6 features, mismo orden que features_orden en model_input_ranges.json ──
    input->data.f[0] = hora;          // hora        [0-23]
    input->data.f[1] = TARGET_TEMP;   // target_temp — del cultivo activo
    input->data.f[2] = TARGET_HUM;    // target_hum  — del cultivo activo
    input->data.f[3] = temperatura;   // temp_input  — sensor
    input->data.f[4] = hum_suelo;     // hum_input   — sensor
    input->data.f[5] = bateria;       // bat_input   — sensor

    if (interpreter->Invoke() != kTfLiteOk) {
        Serial.println("❌ Error IA");
        return;
    }

    float p_luz   = output->data.f[0];
    float p_fan   = output->data.f[1];
    float p_riego = output->data.f[2];
    float p_sleep = output->data.f[3];

    bool cmd_luz   = p_luz   > TH_LUZ;
    bool cmd_fan   = p_fan   > TH_FAN;
    bool cmd_riego = p_riego > TH_RIEGO;
    bool cmd_sleep = p_sleep > TH_SLEEP;

    // Seguridad de riego — dinámico según el cultivo
    if (bateria < 20 || hum_suelo > (TARGET_HUM + 15)) {
        cmd_riego = false;
    }

    digitalWrite(PIN_LUZ,   cmd_luz   ? HIGH : LOW);
    digitalWrite(PIN_FAN,   cmd_fan   ? HIGH : LOW);
    digitalWrite(PIN_BOMBA, cmd_riego ? HIGH : LOW);

    Serial.println("🤖 ACCIONES:");
    Serial.printf(" 💡 LUZ   : %s (%.2f)\n", cmd_luz   ? "ON":"OFF", p_luz);
    Serial.printf(" 💨 FAN   : %s (%.2f)\n", cmd_fan   ? "ON":"OFF", p_fan);
    Serial.printf(" 💧 RIEGO : %s (%.2f)\n", cmd_riego ? "ON":"OFF", p_riego);

    if (cmd_sleep) {
        Serial.println("🌙 Deep Sleep");
        digitalWrite(PIN_LUZ,  LOW);
        digitalWrite(PIN_FAN,  LOW);
        digitalWrite(PIN_BOMBA,LOW);
        WiFi.mode(WIFI_OFF);
        btStop();
        adc_power_release();
        Serial.flush();
        esp_sleep_enable_timer_wakeup(TIEMPO_DORMIR_US);
        esp_deep_sleep_start();
    }

    delay(5000);
}
