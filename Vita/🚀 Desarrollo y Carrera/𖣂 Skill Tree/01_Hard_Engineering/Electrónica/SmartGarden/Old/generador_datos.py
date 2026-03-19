import csv
import random
import os
from sim_env import Greenhouse

# ---------------------------------------------------------
# CONFIGURACIÓN CRÍTICA
# ---------------------------------------------------------
random.seed(42)  # 🔑 Reproducibilidad total

DIAS_A_SIMULAR = 365       
PASOS_POR_DIA = 24
TOTAL_PASOS = DIAS_A_SIMULAR * PASOS_POR_DIA
ARCHIVO_SALIDA = "dataset_entrenamiento.csv"


# ---------------------------------------------------------
# AGENTE EPSILON-GREEDY v2
# ---------------------------------------------------------
def agente_explorador(obs, target_temp):
    """Agente explorador con lógica estable y errores controlados"""

    # 10% Exploración (ruido para aprendizaje)
    if random.random() < 0.1:
        return {
            'luz': random.choice([0, 1]),
            'ventilador': random.choice([0, 1]),
            'riego': random.choice([0, 1]),
            'deep_sleep': random.choice([0, 1])
        }

    # 90% Explotación
    accion = {'luz': 0, 'ventilador': 0, 'riego': 0, 'deep_sleep': 0}

    # Emergencia energética
    if obs["bateria_pct"] < 20:
        accion['deep_sleep'] = 1
        return accion

    # Control térmico
    if obs["temp_int"] < target_temp - 2:
        accion['luz'] = 1
    elif obs["temp_int"] > target_temp + 2:
        accion['ventilador'] = 1

    # Control hídrico
    if obs["hum_suelo"] < 40:
        accion['riego'] = 1

    # Sueño inteligente
    es_noche = obs["hora_dia"] < 6 or obs["hora_dia"] > 19
    temp_ok = abs(obs["temp_int"] - target_temp) < 3
    if es_noche and temp_ok:
        accion['deep_sleep'] = 1

    return accion


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
if __name__ == "__main__":
    print("💾 Generador de Dataset v3.2 (Robusto y Reproducible)")
    print(f"   - Días: {DIAS_A_SIMULAR}")
    print(f"   - Total pasos: {TOTAL_PASOS}")
    print(f"   - Seed: 42\n")

    env = Greenhouse(cultivo_objetivo="Chile Habanero")
    target = env.perfil["parametros_optimos"]["temperatura_ideal"]

    # --- SANITY CHECK DEL ENTORNO ---
    required = ["temp_int", "hum_suelo", "bateria_pct", "modo_cpu", "hora_dia"]
    for key in required:
        if key not in env.state:
            raise RuntimeError(f"❌ ERROR: Falta '{key}' en sim_env.py")
    print("✅ Entorno validado correctamente")
    print(f"🎯 Objetivo térmico: {target}°C\n")

    registro_datos = []
    muertes = 0

    for paso in range(TOTAL_PASOS):
        estado_actual = env.state.copy()

        # 1️⃣ Decisión del agente
        accion = agente_explorador(estado_actual, target)

        # 2️⃣ Simulación
        obs_siguiente, sol, consumo = env.step(accion)

        # 3️⃣ CLAMP DE SEGURIDAD (MEJORA 1️⃣)
        obs_siguiente["hum_suelo"] = max(0, min(100, obs_siguiente["hum_suelo"]))

        # 4️⃣ Recompensa
        error_temp = abs(obs_siguiente["temp_int"] - target)
        recompensa = -error_temp - (consumo * 0.05)

        if obs_siguiente["modo_cpu"] == "DEAD":
            recompensa -= 100
            if estado_actual["modo_cpu"] != "DEAD":
                muertes += 1

        # 5️⃣ Registro (MEJORA 2️⃣: energía solar incluida)
        fila = {
            "hora": round(estado_actual["hora_dia"], 2),
            "target_temp": round(target, 1),
            "temp_input": round(estado_actual["temp_int"], 2),
            "hum_input": round(estado_actual["hum_suelo"], 2),
            "bat_input": round(estado_actual["bateria_pct"], 2),

            "accion_luz": accion['luz'],
            "accion_fan": accion['ventilador'],
            "accion_riego": accion['riego'],
            "accion_sleep": accion['deep_sleep'],

            "solar_w": round(sol, 2),
            "consumo_w": round(consumo, 2),

            "temp_output": round(obs_siguiente["temp_int"], 2),
            "bat_output": round(obs_siguiente["bateria_pct"], 2),
            "recompensa": round(recompensa, 4),
            "estado_cpu": obs_siguiente["modo_cpu"]
        }

        registro_datos.append(fila)

        if paso % 100 == 0:
            print(f"   ⏳ Paso {paso}/{TOTAL_PASOS}")

    # ---------------------------------------------------------
    # EXPORTACIÓN CSV NATIVA
    # ---------------------------------------------------------
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_final = os.path.join(ruta_script, ARCHIVO_SALIDA)

    try:
        with open(ruta_final, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=registro_datos[0].keys())
            writer.writeheader()
            writer.writerows(registro_datos)

        print("\n" + "=" * 45)
        print(f"✅ DATASET GENERADO CORRECTAMENTE")
        print(f"📄 Archivo: {ruta_final}")
        print(f"📊 Filas: {len(registro_datos)}")
        print(f"💀 Muertes del sistema: {muertes}")
        print("=" * 45)

    except IOError as e:
        print(f"❌ Error al guardar CSV: {e}")
