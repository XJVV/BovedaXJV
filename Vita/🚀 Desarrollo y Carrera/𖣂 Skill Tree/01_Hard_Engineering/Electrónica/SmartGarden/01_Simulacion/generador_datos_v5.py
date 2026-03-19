import csv
import random
import os
from sim_env_v2_4 import Greenhouse

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------
random.seed(42)

DIAS_A_SIMULAR = 365
PASOS_POR_DIA  = 24
TOTAL_PASOS    = DIAS_A_SIMULAR * PASOS_POR_DIA
ARCHIVO_SALIDA = "dataset_entrenamiento.csv"

# ---------------------------------------------------------
# ESCENARIOS — cubre el espacio físico posible de cultivos
#
# En vez de simular cultivos por nombre, simulamos combinaciones
# de (target_temp, target_hum) que abarcan desde un cactus hasta
# un tropical. El modelo aprende a controlar hacia CUALQUIER punto
# dentro de este espacio.
#
# Lógica de cobertura:
#   Temp:  10°C (fresas) → 32°C (tropicales)
#   Hum:   20% (suculentas) → 85% (arroz, taro)
#
# Añade o quita escenarios según los cultivos que te interesen.
# No necesitas que sean cultivos reales — solo que cubran el rango.
# ---------------------------------------------------------
ESCENARIOS = [
    # ── Fríos y secos ─────────────────────────────────────
    {"target_temp": 10.0, "target_hum": 40.0},  # fresa, espinaca
    {"target_temp": 13.0, "target_hum": 50.0},  # lechuga de invierno
    {"target_temp": 15.0, "target_hum": 35.0},  # suculentas en clima frío

    # ── Templados ─────────────────────────────────────────
    {"target_temp": 17.0, "target_hum": 60.0},  # lechuga, cilantro
    {"target_temp": 19.0, "target_hum": 55.0},  # perejil, albahaca fría
    {"target_temp": 21.0, "target_hum": 65.0},  # habanero, menta

    # ── Cálidos — los más comunes en huerto ───────────────
    {"target_temp": 23.0, "target_hum": 70.0},  # tomate cherry
    {"target_temp": 25.0, "target_hum": 65.0},  # tomate, pimiento
    {"target_temp": 25.0, "target_hum": 45.0},  # romero, orégano
    {"target_temp": 27.0, "target_hum": 75.0},  # pepino, berenjena

    # ── Calientes ─────────────────────────────────────────
    {"target_temp": 29.0, "target_hum": 80.0},  # albahaca tropical
    {"target_temp": 30.0, "target_hum": 30.0},  # cactus, aloe

    # ── Extremos (asegura que los bordes del espacio estén cubiertos)
    {"target_temp": 12.0, "target_hum": 75.0},  # berro, menta acuática
    {"target_temp": 32.0, "target_hum": 70.0},  # jengibre, cúrcuma
]


# ---------------------------------------------------------
# AGENTE EXPLORADOR v4 — agnóstico al cultivo
#
# Recibe los objetivos como parámetros numéricos.
# La lógica es física pura — funciona para cualquier cultivo.
# ---------------------------------------------------------
def agente_explorador(obs, target_temp, target_hum):
    # 12% exploración aleatoria — genera variedad en el dataset
    if random.random() < 0.12:
        return {
            'luz':        random.choice([0, 1]),
            'ventilador': random.choice([0, 1]),
            'riego':      random.choice([0, 1]),
            'deep_sleep': random.choice([0, 1])
        }

    accion = {'luz': 0, 'ventilador': 0, 'riego': 0, 'deep_sleep': 0}

    # Prioridad 1 — emergencia energética
    if obs["bateria_pct"] < 20:
        accion['deep_sleep'] = 1
        return accion

    # Prioridad 2 — control térmico
    error_temp = obs["temp_int"] - target_temp
    if error_temp < -2.0:
        accion['luz'] = 1          # muy frío → calentar con LED
    elif error_temp > 2.0:
        accion['ventilador'] = 1   # muy caliente → ventilar

    # Prioridad 3 — control hídrico
    error_hum = obs["hum_suelo"] - target_hum
    if error_hum < -15.0:
        accion['riego'] = 1        # muy seco → regar
    # (no hacemos nada si está húmedo — la evaporación lo regula)

    # Prioridad 4 — sueño inteligente
    es_noche = obs["hora_dia"] < 6 or obs["hora_dia"] > 19
    temp_ok  = abs(error_temp) < 3.0
    hum_ok   = abs(error_hum)  < 20.0
    if es_noche and temp_ok and hum_ok:
        accion['deep_sleep'] = 1

    return accion


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
if __name__ == "__main__":
    print("💾 Generador de Dataset v5.0 (Universal — espacio continuo)")
    print(f"   Escenarios : {len(ESCENARIOS)}")
    print(f"   Días/escenario: {DIAS_A_SIMULAR} ({TOTAL_PASOS} pasos)")
    print(f"   Total filas estimadas: {len(ESCENARIOS) * TOTAL_PASOS:,}\n")

    registro_datos = []
    muertes_total  = 0

    for i, escenario in enumerate(ESCENARIOS):
        target_temp = escenario["target_temp"]
        target_hum  = escenario["target_hum"]

        print(f"🌡  Escenario {i+1}/{len(ESCENARIOS)} — "
              f"target_temp={target_temp}°C, target_hum={target_hum}%")

        # Greenhouse en modo "genérico" — le pasamos los targets directamente
        # en lugar de cargarlos del JSON para este generador
        env = Greenhouse.__new__(Greenhouse)
        env._ruta_docs   = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "00_Docs")
        env.TARGET_TEMP  = target_temp
        env.TARGET_HUM   = target_hum
        env.MARGEN_TEMP  = 3.0
        env.perfil       = {"parametros_optimos": {
                                "temperatura_ideal":   target_temp,
                                "humedad_suelo_ideal": target_hum,
                                "margen_tolerancia":   3.0
                            }}
        env.HARDWARE = {
            "bateria_capacidad_wh":   50.0,
            "panel_solar_max_w":      20.0,
            "consumo_led_w":          10.0,
            "consumo_pump_w":          5.0,
            "consumo_fan_w":           2.0,
            "consumo_esp32_active_w":  0.6,
            "consumo_esp32_sleep_w":   0.01
        }
        env.state = {
            "temp_int":          target_temp - 2.0,  # arranca ligeramente bajo el objetivo
            "hum_suelo":         target_hum  - 5.0,
            "bateria_actual_wh": 40.0,
            "hora_dia":          8.0,
            "dia_simulacion":    1,
            "modo_cpu":         "ACTIVE"
        }
        env.state["bateria_pct"] = (env.state["bateria_actual_wh"] /
                                    env.HARDWARE["bateria_capacidad_wh"]) * 100
        env.PHYSICS = {
            "calor_led_gain":     0.8,
            "frio_fan_loss":      1.2,
            "aislamiento_factor": 0.15
        }
        import random as _r
        env._rng = _r  # sim_env usa random directamente

        muertes = 0

        for paso in range(TOTAL_PASOS):
            estado_actual = env.state.copy()
            accion = agente_explorador(estado_actual, target_temp, target_hum)

            obs_sig, sol, consumo, recompensa = env.step(accion)
            obs_sig["hum_suelo"] = max(0.0, min(100.0, obs_sig["hum_suelo"]))

            if obs_sig["modo_cpu"] == "DEAD":
                recompensa -= 100.0
                if estado_actual["modo_cpu"] != "DEAD":
                    muertes += 1

            fila = {
                # ── Features del modelo (6) ───────────────────
                "hora":        round(estado_actual["hora_dia"],    2),
                "target_temp": round(target_temp,                  1),
                "target_hum":  round(target_hum,                   1),
                "temp_input":  round(estado_actual["temp_int"],    2),
                "hum_input":   round(estado_actual["hum_suelo"],   2),
                "bat_input":   round(estado_actual["bateria_pct"], 2),

                # ── Targets (4) ───────────────────────────────
                "accion_luz":   accion['luz'],
                "accion_fan":   accion['ventilador'],
                "accion_riego": accion['riego'],
                "accion_sleep": accion['deep_sleep'],

                # ── Contexto / debug ──────────────────────────
                "solar_w":     round(sol,                          2),
                "consumo_w":   round(consumo,                      2),
                "temp_output": round(obs_sig["temp_int"],          2),
                "bat_output":  round(obs_sig["bateria_pct"],       2),
                "recompensa":  round(recompensa,                   4),
                "estado_cpu":  obs_sig["modo_cpu"]
            }
            registro_datos.append(fila)

            if paso % 1000 == 0:
                print(f"   ⏳ paso {paso}/{TOTAL_PASOS}")

        muertes_total += muertes
        print(f"   ✅ muertes: {muertes}\n")

    # ---------------------------------------------------------
    # EXPORTACIÓN
    # ---------------------------------------------------------
    ruta_final = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              ARCHIVO_SALIDA)
    with open(ruta_final, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=registro_datos[0].keys())
        writer.writeheader()
        writer.writerows(registro_datos)

    print("=" * 52)
    print(f"✅ DATASET UNIVERSAL GENERADO")
    print(f"📄 {ruta_final}")
    print(f"📊 Total filas   : {len(registro_datos):,}")
    print(f"🌡  Rango temp   : {min(e['target_temp'] for e in ESCENARIOS)}°C"
          f" – {max(e['target_temp'] for e in ESCENARIOS)}°C")
    print(f"💧 Rango humedad : {min(e['target_hum'] for e in ESCENARIOS)}%"
          f" – {max(e['target_hum'] for e in ESCENARIOS)}%")
    print(f"💀 Muertes totales: {muertes_total}")
    print("=" * 52)
