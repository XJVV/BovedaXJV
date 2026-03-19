// ==========================================
// ⚙️  CALIBRACIÓN — Cultivo activo
// ==========================================
// Cambia este valor para cambiar el cultivo.
// Debe coincidir con el id_cultivo del dataset:
//   0 = Tomato  |  1 = Lettuce  |  2 = Habanero Pepper
const int    CULTIVO_ID    = 2;
const float  TARGET_TEMP   = 21.1;   // parametros_optimos.temperatura_ideal
const float  TARGET_HUM    = 60.0;   // parametros_optimos.humedad_suelo_ideal  ← NUEVO
// Idealmente estos valores se leerían de SPIFFS/LittleFS desde el JSON,
// pero hardcodearlos aquí es correcto mientras no tengas sistema de archivos.

// ==========================================
// ⚙️  CALIBRACIÓN — TFLite
// ==========================================
// Ajusta según lo que imprima el notebook de entrenamiento:
//   "Arena mínima recomendada: X KB"
const int kTensorArenaSize = 12 * 1024;   // sube de 8 si el notebook lo indica


// ==========================================
// SETUP — flag para evitar loop() sin modelo
// ==========================================
bool sistema_listo = false;   // FIX: loop() no corre si setup() falló

void setup() {
    Serial.begin(115200);
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db);

    pinMode(PIN_LUZ,  OUTPUT);  digitalWrite(PIN_LUZ,  LOW);
    pinMode(PIN_FAN,  OUTPUT);  digitalWrite(PIN_FAN,  LOW);
    pinMode(PIN_BOMBA,OUTPUT);  digitalWrite(PIN_BOMBA,LOW);

    dht.setup(PIN_DHT, DHTesp::DHT22);

    // ── TFLite ──────────────────────────────────────────
    static tflite::MicroErrorReporter micro_error_reporter;
    error_reporter = &micro_error_reporter;

    model = tflite::GetModel(brain_v3_tflite);   // actualiza el nombre del array
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        Serial.println("❌ Modelo incompatible");
        return;   // sistema_listo queda false
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
        return;   // sistema_listo queda false
    }

    input  = interpreter->input(0);
    output = interpreter->output(0);

    // Verificar dimensiones — el modelo v3 espera 7 inputs
    if (input->dims->data[1] != 7) {
        Serial.printf("❌ Modelo espera %d inputs, código configura 7\n",
                      input->dims->data[1]);
        return;
    }

    sistema_listo = true;
    Serial.println("✅ SmartGarden ONLINE — brain_v3 (7 features, multi-cultivo)");
}


// ==========================================
// LOOP — solo corre si setup() terminó bien
// ==========================================
void loop() {
    // FIX: guarda contra setup() fallido
    if (!sistema_listo) {
        Serial.println("⛔ Sistema no inicializado. Revisa el Serial de setup().");
        delay(5000);
        return;
    }

    float temperatura = dht.getTemperature();
    float hum_suelo   = leerSuelo();
    float bateria     = leerBateria();

    // FIX: hora simulada con millis() hasta que tengas RTC
    // Cada ciclo de 5s avanza ~0.0014h → 24h virtuales en ~86400s reales
    float hora_actual = fmod((millis() / 3600000.0), 24.0);

    if (isnan(temperatura) || temperatura < -10 || temperatura > 60) {
        temperatura = TARGET_TEMP;
        Serial.println("⚠️  DHT22 error — usando TARGET_TEMP como fallback");
    }

    Serial.printf("\n🌱 Temp: %.1f°C | Suelo: %.0f%% | Bat: %.0f%% | Hora: %.1fh\n",
                  temperatura, hum_suelo, bateria, hora_actual);

    // ── IA INPUT — 7 features, mismo orden que features_orden en model_input_ranges.json ──
    input->data.f[0] = (float)CULTIVO_ID;   // id_cultivo  [0, 1, 2]
    input->data.f[1] = hora_actual;          // hora        [0-23]
    input->data.f[2] = TARGET_TEMP;          // target_temp [19.1-25.5]
    input->data.f[3] = TARGET_HUM;           // target_hum  [50-75]   ← NUEVO
    input->data.f[4] = temperatura;          // temp_input
    input->data.f[5] = hum_suelo;            // hum_input
    input->data.f[6] = bateria;              // bat_input

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

    // Seguridad de riego — ahora usa TARGET_HUM como referencia
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
