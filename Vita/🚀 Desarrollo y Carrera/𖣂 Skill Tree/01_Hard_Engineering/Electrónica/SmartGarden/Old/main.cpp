#include <Arduino.h>
#include <WiFi.h>
#include "driver/adc.h"
#include "esp_sleep.h"

// ===== Sensores =====
#include "DHTesp.h"

// ===== IA =====
#include "TensorFlowLite_ESP32.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "model_data.h"

// ==========================================
// 🔌 MAPA DE CONEXIONES
// ==========================================
#define PIN_DHT       4
#define PIN_SUELO     34
#define PIN_BATERIA   32

#define PIN_LUZ       18
#define PIN_FAN       19
#define PIN_BOMBA     21

// ==========================================
// ⚙️ CALIBRACIÓN
// ==========================================
const int SUELO_SECO   = 3500;
const int SUELO_MOJADO = 1500;

const float TARGET_TEMP = 21.1;

// IA
const int kTensorArenaSize = 8 * 1024;
uint8_t tensor_arena[kTensorArenaSize];

const float TH_LUZ   = 0.60;
const float TH_FAN   = 0.55;
const float TH_RIEGO = 0.65;
const float TH_SLEEP = 0.50;

#define TIEMPO_DORMIR_US  (30ULL * 60ULL * 1000000ULL)

// ==========================================
// OBJETOS GLOBALES
// ==========================================
DHTesp dht;

tflite::MicroErrorReporter* error_reporter = nullptr;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
static tflite::MicroMutableOpResolver<6> micro_op_resolver;

// ==========================================
// FUNCIONES AUXILIARES
// ==========================================

// 🔋 Batería real (LiPo)
float leerBateria() {
  int raw = analogRead(PIN_BATERIA);
  float voltaje = (raw / 4095.0) * 3.3 * 2.0;

  float porcentaje;
  if (voltaje >= 4.2) porcentaje = 100;
  else if (voltaje <= 3.3) porcentaje = 0;
  else porcentaje = (voltaje - 3.3) / (4.2 - 3.3) * 100;

  return constrain(porcentaje, 0, 100);
}

// 🌱 Suelo con filtrado
float leerSuelo() {
  long suma = 0;
  for (int i = 0; i < 10; i++) {
    suma += analogRead(PIN_SUELO);
    delay(5);
  }
  int raw = suma / 10;
  int pct = map(raw, SUELO_SECO, SUELO_MOJADO, 0, 100);
  return constrain(pct, 0, 100);
}

// ==========================================
// SETUP
// ==========================================
void setup() {
  Serial.begin(115200);

  // ADC CONFIG (clave)
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  pinMode(PIN_LUZ, OUTPUT);
  pinMode(PIN_FAN, OUTPUT);
  pinMode(PIN_BOMBA, OUTPUT);

  digitalWrite(PIN_LUZ, LOW);
  digitalWrite(PIN_FAN, LOW);
  digitalWrite(PIN_BOMBA, LOW);

  dht.setup(PIN_DHT, DHTesp::DHT22);

  // ===== TFLite =====
  static tflite::MicroErrorReporter micro_error_reporter;
  error_reporter = &micro_error_reporter;

  model = tflite::GetModel(brain_v2_tflite);
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
    Serial.println("❌ Arena insuficiente");
    return;
  }

  input = interpreter->input(0);
  output = interpreter->output(0);

  Serial.println("✅ SmartGarden ONLINE");
}

// ==========================================
// LOOP
// ==========================================
void loop() {
  float temperatura = dht.getTemperature();
  float hum_suelo   = leerSuelo();
  float bateria     = leerBateria();
  float hora_actual = 14.0; // placeholder sin RTC

  // Validaciones
  if (isnan(temperatura) || temperatura < -10 || temperatura > 60) {
    temperatura = TARGET_TEMP;
  }

  Serial.printf(
    "\n🌱 Temp: %.1f°C | Suelo: %.0f%% | Bat: %.0f%%\n",
    temperatura, hum_suelo, bateria
  );

  // ===== IA INPUT =====
  input->data.f[0] = hora_actual;
  input->data.f[1] = TARGET_TEMP;
  input->data.f[2] = temperatura;
  input->data.f[3] = hum_suelo;
  input->data.f[4] = bateria;

  if (interpreter->Invoke() != kTfLiteOk) {
    Serial.println("❌ Error IA");
    return;
  }

  float p_luz   = output->data.f[0];
  float p_fan   = output->data.f[1];
  float p_riego = output->data.f[2];
  float p_sleep = output->data.f[3];

  bool cmd_luz   = p_luz > TH_LUZ;
  bool cmd_fan   = p_fan > TH_FAN;
  bool cmd_riego = p_riego > TH_RIEGO;
  bool cmd_sleep = p_sleep > TH_SLEEP;

  // 🛑 Seguridad de riego
  if (bateria < 20 || hum_suelo > 80) {
    cmd_riego = false;
  }

  digitalWrite(PIN_LUZ,   cmd_luz   ? HIGH : LOW);
  digitalWrite(PIN_FAN,   cmd_fan   ? HIGH : LOW);
  digitalWrite(PIN_BOMBA, cmd_riego ? HIGH : LOW);

  Serial.println("🤖 ACCIONES:");
  Serial.printf(" 💡 LUZ   : %s (%.2f)\n", cmd_luz ? "ON" : "OFF", p_luz);
  Serial.printf(" 💨 FAN   : %s (%.2f)\n", cmd_fan ? "ON" : "OFF", p_fan);
  Serial.printf(" 💧 RIEGO : %s (%.2f)\n", cmd_riego ? "ON" : "OFF", p_riego);

  // ===== DEEP SLEEP =====
  if (cmd_sleep) {
    Serial.println("🌙 Deep Sleep activado");

    digitalWrite(PIN_LUZ, LOW);
    digitalWrite(PIN_FAN, LOW);
    digitalWrite(PIN_BOMBA, LOW);

    WiFi.mode(WIFI_OFF);
    btStop();
    adc_power_release();

    Serial.flush();
    esp_sleep_enable_timer_wakeup(TIEMPO_DORMIR_US);
    esp_deep_sleep_start();
  }

  delay(5000);
}
