import csv
import random
import os
from sim_env_v2_4 import Greenhouse   # actualiza el import si renombraste el archivo

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------
random.seed(42)

DIAS_A_SIMULAR   = 365
PASOS_POR_DIA    = 24
TOTAL_PASOS      = DIAS_A_SIMULAR * PASOS_POR_DIA
ARCHIVO_SALIDA   = "dataset_entrenamiento.csv"

# Los 3 cultivos que tiene el JSON.
# El id numérico es la feature que entra al modelo (0, 1, 2).
CULTIVOS = [
    {"nombre": "Tomato",          "id": 0},
    {"nombre": "Lettuce",         "id": 1},
    {"nombre": "Habanero Pepper", "id": 2},
]


# ---------------------------------------------------------
# AGENTE EPSILON-GREEDY v3
# Ahora recibe target_hum además de target_temp.
# ---------------------------------------------------------
def agente_explorador(obs, target_temp, target_hum):
    """
    Agente heurístico que genera datos de entrenamiento variados.
    10% exploración aleatoria, 90% heurística basada en los objetivos
    reales del cultivo activo.
    """
    if random.random() < 0.10:
        return {
            'luz':        random.choice([0, 1]),
            'ventilador': random.choice([0, 1]),
            'riego':      random.choice([0, 1]),
            'deep_sleep': random.choice([0, 1])
        }

    accion = {'luz': 0, 'ventilador': 0, 'riego': 0, 'deep_sleep': 0}

    # Emergencia energética — prioridad máxima
    if obs["bateria_pct"] < 20:
        accion['deep_sleep'] = 1
        return accion

    # Control térmico
    if obs["temp_int"] < target_temp - 2:
        accion['luz'] = 1
    elif obs["temp_int"] > target_temp + 2:
        accion['ventilador'] = 1

    # Control hídrico — FIX: usa target_hum del cultivo, no 40 hardcodeado
    umbral_riego_bajo = target_hum - 15   # regar si cae más de 15pp bajo el objetivo
    umbral_riego_alto = target_hum + 10   # no regar si ya está suficientemente húmedo
    if obs["hum_suelo"] < umbral_riego_bajo:
        accion['riego'] = 1
    elif obs["hum_suelo"] > umbral_riego_alto:
        accion['riego'] = 0   # explícito para claridad

    # Sueño inteligente (solo noche + condiciones estables)
    es_noche   = obs["hora_dia"] < 6 or obs["hora_dia"] > 19
    temp_ok    = abs(obs["temp_int"]  - target_temp) < 3
    hum_ok     = abs(obs["hum_suelo"] - target_hum)  < 20
    if es_noche and temp_ok and hum_ok:
        accion['deep_sleep'] = 1

    return accion


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
if __name__ == "__main__":
    print("💾 Generador de Dataset v4.0 (Multi-Cultivo)")
    print(f"   Cultivos : {[c['nombre'] for c in CULTIVOS]}")
    print(f"   Días/cultivo: {DIAS_A_SIMULAR} ({TOTAL_PASOS} pasos)")
    print(f"   Seed: 42\n")

    registro_datos = []
    muertes_total  = 0

    for cultivo_cfg in CULTIVOS:
        nombre    = cultivo_cfg["nombre"]
        id_cultivo = cultivo_cfg["id"]

        print(f"🌱 Simulando: {nombre} (id={id_cultivo})")

        # Cada cultivo arranca con su propio entorno limpio
        env = Greenhouse(cultivo_objetivo=nombre)

        # Validación de campos requeridos
        required = ["temp_int", "hum_suelo", "bateria_pct", "modo_cpu", "hora_dia"]
        for key in required:
            if key not in env.state:
                raise RuntimeError(f"❌ Falta '{key}' en sim_env. Revisa la versión.")

        target_temp = env.TARGET_TEMP
        target_hum  = env.TARGET_HUM
        print(f"   Temp objetivo: {target_temp}°C | Hum objetivo: {target_hum}%")

        muertes = 0

        for paso in range(TOTAL_PASOS):
            estado_actual = env.state.copy()

            # 1. Decisión
            accion = agente_explorador(estado_actual, target_temp, target_hum)

            # 2. Simulación — FIX: desempaqueta 4 valores (v2.4 devuelve recompensa)
            obs_sig, sol, consumo, recompensa = env.step(accion)

            # 3. Clamp de seguridad (por si acaso)
            obs_sig["hum_suelo"] = max(0.0, min(100.0, obs_sig["hum_suelo"]))

            # 4. Penalización por muerte (recompensa ya viene calculada del env,
            #    solo añadimos la penalización catastrófica aquí)
            if obs_sig["modo_cpu"] == "DEAD":
                recompensa -= 100.0
                if estado_actual["modo_cpu"] != "DEAD":
                    muertes += 1

            # 5. Registro — incluye id_cultivo como feature
            fila = {
                # ── Inputs al modelo ──────────────────────────
                "id_cultivo":  id_cultivo,              # 0=Tomato, 1=Lettuce, 2=Habanero
                "hora":        round(estado_actual["hora_dia"],  2),
                "target_temp": round(target_temp, 1),
                "target_hum":  round(target_hum,  1),   # NUEVO
                "temp_input":  round(estado_actual["temp_int"],  2),
                "hum_input":   round(estado_actual["hum_suelo"], 2),
                "bat_input":   round(estado_actual["bateria_pct"], 2),

                # ── Acciones (targets de entrenamiento) ───────
                "accion_luz":   accion['luz'],
                "accion_fan":   accion['ventilador'],
                "accion_riego": accion['riego'],
                "accion_sleep": accion['deep_sleep'],

                # ── Contexto / debug ──────────────────────────
                "solar_w":    round(sol,       2),
                "consumo_w":  round(consumo,   2),
                "temp_output":round(obs_sig["temp_int"],  2),
                "bat_output": round(obs_sig["bateria_pct"], 2),
                "recompensa": round(recompensa, 4),
                "estado_cpu": obs_sig["modo_cpu"]
            }

            registro_datos.append(fila)

            if paso % 500 == 0:
                print(f"   ⏳ {nombre} — paso {paso}/{TOTAL_PASOS}")

        muertes_total += muertes
        print(f"   ✅ {nombre} — {TOTAL_PASOS} pasos | Muertes: {muertes}\n")

    # ---------------------------------------------------------
    # EXPORTACIÓN
    # ---------------------------------------------------------
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_final  = os.path.join(ruta_script, ARCHIVO_SALIDA)

    try:
        with open(ruta_final, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=registro_datos[0].keys())
            writer.writeheader()
            writer.writerows(registro_datos)

        filas_por_cultivo = TOTAL_PASOS
        print("=" * 50)
        print(f"✅ DATASET MULTI-CULTIVO GENERADO")
        print(f"📄 {ruta_final}")
        print(f"📊 Total filas : {len(registro_datos):,}  ({filas_por_cultivo:,} × {len(CULTIVOS)} cultivos)")
        print(f"💀 Muertes totales: {muertes_total}")
        print(f"📋 Features   : id_cultivo, hora, target_temp, target_hum, temp_input, hum_input, bat_input")
        print(f"🎯 Targets    : accion_luz, accion_fan, accion_riego, accion_sleep")
        print("=" * 50)

    except IOError as e:
        print(f"❌ Error al guardar CSV: {e}")
