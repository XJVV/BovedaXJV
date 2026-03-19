**Estado:** En Progreso
**Tags:** TinyML
**Fecha de Inicio:** 2026-01-10
**Ubicación Física:** `.../Electrónica/SmartGarden/`

---

## 📂 Estructura del Proyecto
Para mantener el orden entre el código, los datos y la documentación, este proyecto se divide en:

* **[[00_Docs]]**: La "Fuente de la Verdad" (Perfiles de cultivo JSON, Datasheets, Papers).
* **[[01_Simulacion]]**: El "Gemelo Digital" (Scripts Python, Entorno virtual, Datasets sintéticos).
* **[[02_Modelos]]**: Los "Cerebros" (Archivos `.tflite`, `.h5`, Logs de entrenamiento).
* **[[03_Diagramas]]**: Los "Planos" (Circuitos, Máquinas de Estados en Canvas, Flujos).

---

## 📅 Roadmap Técnico

### Fase 1: Módulo de Investigación Autónoma (Data Mining)
*Objetivo: Que el sistema obtenga sus propios parámetros de fuentes confiables.*
- [x] **Script de Investigación (`agente_agronomo.py`)**:
    - Desarrollar script en Python que busque en APIs (OpenFarm, USDA) o scraping web.
    - Implementar algoritmo de "Consenso": Si 3 fuentes dicen 24°C y una dice 30°C, descartar outlier y promediar.
- [x] **Generación Dinámica de JSON**:
    - El script debe "escupir" el archivo `Perfiles_Cultivo.json` automáticamente.
- [x] **Validación Humana**:
    - Interfaz simple (print en consola) para que tú apruebes los datos encontrados antes de enviarlos al huerto.

### Fase 2: El Gemelo Digital (Python Simulation)
*Objetivo: Generar datos sintéticos antes de tener hardware.*
- [x] Configurar entorno virtual (`venv`) en la carpeta `01_Simulacion`.
- [x] Programar `sim_env.py` (Clase `Greenhouse` con física básica).
- [x] Generar **Dataset Sintético** (30 días virtuales) y exportar a CSV.

### Fase 3: TinyML & Entrenamiento
*Objetivo: Crear la IA aprovechando tus conocimientos de Data Science.*
> 💡 **Recurso:** Si necesitas refrescar conceptos de pre-procesamiento o redes neuronales, consulta tu nota maestra: [[Vita/🚀 Desarrollo y Carrera/𖣂 Skill Tree/01_Hard_Engineering/Data Science/Data Science|Data Science Knowledge Base]].

- [x] **Feature Engineering**: Crear variables de tendencia (deltas de temperatura).
- [x] **Modelo 1 (Regresión)**: Predicción de disponibilidad energética futura.
- [x] **Modelo 2 (Autoencoder)**: Detección de anomalías en sensores.

### Fase 4: Lógica de Control (The Manager)
*Objetivo: El árbitro entre lo que la planta quiere y lo que la batería permite.*
- [ ] Diseñar Máquina de Estados Finitos (FSM) en `03_Diagramas`.
- [ ] Implementar algoritmo de optimización de costes ($J = w_1 \cdot Error + w_2 \cdot Energia$).

### Fase 5: Hardware & Presupuesto
*Objetivo: Llevar el código al mundo físico.*
- [ ] Selección de Microcontrolador (ESP32-S3 / Portenta H7).
- [ ] **Gestión de Compras (BOM)**: Registrar costos y proveedores en tu sistema financiero.
    > 💰 **Link:** [[Vita/💰 Finanzas/Registro de Gastos/Registro de Gastos|Presupuesto del Proyecto SmartGarden]]
- [ ] Validación "Hardware-in-the-Loop".

---























## 📝 Bitácora Rápida
*Espacio para notas sueltas del día a día antes de procesarlas.*

* [Fecha]: Idea...
[[Electrónica]]