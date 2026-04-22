# 🚀 Pipeline de MLOps v4.0 (IA Universal + SPIFFS)

Arquitectura Definitiva: El modelo ahora es **Agnóstico al Cultivo**. Aprende termodinámica (control de la distancia hacia `target_temp` y `target_hum`) usando 14 escenarios físicos, logrando Zero-Shot Generalization para cualquier planta nueva.

## 🌐 1. Extracción de Datos (agente_agronomo_v5_1.py)
- **Acción:** Ejecutar `python3 agente_agronomo_v5_1.py`
- **Por qué:** Mantiene actualizado `Perfiles_Cultivo.json` con los datos científicos de Temp y Humedad. (Este archivo luego se subirá al chip físico).

## 🎲 2. Motor de Experiencia Universal (generador_datos_v5.py)
- **Acción:** Ejecutar `python3 generador_datos_v5.py`
- **Detalle Técnico:** Ya no simula cultivos por nombre. Simula 14 escenarios físicos (fríos, templados, cálidos, calientes y extremos) generando ~122,000 pasos de experiencia.
- **Salida:** `dataset_entrenamiento.csv` (con 6 features, sin `id_cultivo`).

## 🧠 3. Entrenamiento Agnóstico (train_cerebro_v4.py)
- **Acción:** Ejecutar en Google Colab con el nuevo CSV.
- **Validación:** El notebook corre una prueba final con cultivos "nunca vistos" (Orquídea, Cactus) para confirmar que la IA generalizó las reglas de la física correctamente.
- **Salida:** Descargar como `brain_v4.tflite` (Convertir con `xxd` a `brain_v4_tflite[]`).
[[🌿 SmartGarden]] 
## ⚙️ 4. Configuración del Entorno C++ (platformio.ini)
- **Acción:** Añadir la librería de JSON a las dependencias.
- **Código requerido:**
- ```ini
  lib_deps =
      tanakamasayuki/TensorFlowLite_ESP32 @ ^1.0.0
      beegee-tokyo/DHT sensor library for ESPx @ ^1.19
      bblanchon/ArduinoJson @ ^6.21.3 ```
      