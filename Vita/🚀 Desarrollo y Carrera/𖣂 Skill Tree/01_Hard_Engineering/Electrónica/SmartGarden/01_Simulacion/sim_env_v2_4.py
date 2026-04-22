import json
import math
import random
import os

# ---------------------------------------------------------
# CLASE: ENTORNO DE SIMULACIÓN (PHYSICS ENGINE v2.4)
# Fixes vs v2.3:
#   - Carga config_agronomo.json para resolver alias de cultivos
#   - Usa humedad_suelo_ideal del perfil si está disponible
#   - Falla ruidosamente si el cultivo no existe (no silencioso)
# ---------------------------------------------------------
class Greenhouse:
    def __init__(self, cultivo_objetivo="Habanero Pepper"):
        ruta_script   = os.path.dirname(os.path.abspath(__file__))
        self._ruta_docs = os.path.join(ruta_script, "..", "00_Docs")

        # 1. Cargar config de alias ANTES de buscar el perfil
        self._alias = self._cargar_alias()

        # 2. Resolver alias (ej. "Tomate Cherry" → "Tomato")
        cultivo_resuelto = self._alias.get(cultivo_objetivo, cultivo_objetivo)
        if cultivo_resuelto != cultivo_objetivo:
            print(f"🔀 Alias resuelto: '{cultivo_objetivo}' → '{cultivo_resuelto}'")

        print(f"🌱 Inicializando Invernadero Virtual v2.4 para: {cultivo_resuelto}")

        # 3. Cargar perfil — falla ruidosamente si no existe
        self.perfil = self._cargar_perfil(cultivo_resuelto)
        if not self.perfil:
            cultivos_disponibles = self._listar_cultivos()
            raise ValueError(
                f"❌ Cultivo '{cultivo_resuelto}' no encontrado en Perfiles_Cultivo.json.\n"
                f"   Disponibles: {cultivos_disponibles}\n"
                f"   Agrega el cultivo con agente_agronomo.py o revisa el alias."
            )

        params = self.perfil["parametros_optimos"]
        self.TARGET_TEMP     = params["temperatura_ideal"]
        self.MARGEN_TEMP     = params.get("margen_tolerancia", 3.0)
        # FIX: usa humedad_suelo_ideal si el JSON la tiene; si no, fallback razonable
        self.TARGET_HUM      = params.get("humedad_suelo_ideal", 55.0)

        print(f"   Temp objetivo:    {self.TARGET_TEMP}°C ± {self.MARGEN_TEMP}°C")
        print(f"   Humedad objetivo: {self.TARGET_HUM}%")

        # --- HARDWARE ---
        self.HARDWARE = {
            "bateria_capacidad_wh":   50.0,
            "panel_solar_max_w":      30.0,   # 20W → 30W: sostiene ventilador + ESP32 activo
            "consumo_led_w":          10.0,
            "consumo_pump_w":          5.0,
            "consumo_fan_w":           2.0,
            "consumo_esp32_active_w":  0.6,
            "consumo_esp32_sleep_w":   0.01
        }

        self.state = {
            "temp_int":         20.0,
            "hum_suelo":        50.0,
            "bateria_actual_wh": 40.0,
            "hora_dia":          8.0,
            "dia_simulacion":    1,
            "modo_cpu":        "ACTIVE"
        }

        max_bat = self.HARDWARE["bateria_capacidad_wh"]
        self.state["bateria_pct"] = (self.state["bateria_actual_wh"] / max_bat) * 100

        self.PHYSICS = {
            "calor_led_gain":     0.8,
            "frio_fan_loss":      1.2,
            "aislamiento_factor": 0.15
        }

    # ------------------------------------------------------------------
    # UTILIDADES PRIVADAS
    # ------------------------------------------------------------------
    def _cargar_alias(self):
        """Carga alias_cultivos de config_agronomo.json."""
        ruta = os.path.join(self._ruta_docs, "..", "01_Simulacion", "config_agronomo.json")
        # Busca también en el mismo directorio del script
        rutas_candidatas = [
            ruta,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_agronomo.json")
        ]
        for r in rutas_candidatas:
            if os.path.exists(r):
                try:
                    with open(r, encoding="utf-8") as f:
                        cfg = json.load(f)
                        alias = cfg.get("alias_cultivos", {})
                        print(f"📋 Config cargado: {len(alias)} alias disponibles")
                        return alias
                except Exception as e:
                    print(f"⚠️  config_agronomo.json inválido: {e}")
        print("⚠️  config_agronomo.json no encontrado — sin resolución de alias")
        return {}

    def _cargar_perfil(self, nombre):
        ruta_json = os.path.join(self._ruta_docs, "Perfiles_Cultivo.json")
        if not os.path.exists(ruta_json):
            return None
        try:
            with open(ruta_json, encoding="utf-8") as f:
                data = json.load(f)
            for c in data["cultivos"]:
                if c.get("id_cultivo") == nombre:
                    return c
            return None
        except Exception as e:
            print(f"❌ Error leyendo Perfiles_Cultivo.json: {e}")
            return None

    def _listar_cultivos(self):
        ruta_json = os.path.join(self._ruta_docs, "Perfiles_Cultivo.json")
        try:
            with open(ruta_json, encoding="utf-8") as f:
                data = json.load(f)
            return [c["id_cultivo"] for c in data["cultivos"]]
        except:
            return ["(no se pudo leer el JSON)"]

    def _simular_sol(self, hora):
        if 7 <= hora <= 17:
            intensidad = math.sin(((hora - 7) / 10) * math.pi)
            return max(0, intensidad * self.HARDWARE["panel_solar_max_w"])
        return 0

    # ------------------------------------------------------------------
    # RECOMPENSA — usa los objetivos reales del cultivo
    # ------------------------------------------------------------------
    def _calcular_recompensa(self, obs, accion, generacion, consumo):
        """
        Penaliza por alejarse de los objetivos del cultivo activo.
        """
        error_temp = abs(obs["temp_int"] - self.TARGET_TEMP) / self.MARGEN_TEMP
        error_hum  = abs(obs["hum_suelo"] - self.TARGET_HUM) / 20.0
        penalizacion_energia = max(0, consumo - generacion) * 0.1
        bonus_sleep = 0.5 if accion.get("deep_sleep") and obs["bateria_pct"] < 30 else 0

        return -(error_temp + error_hum + penalizacion_energia) + bonus_sleep

    # ------------------------------------------------------------------
    # STEP
    # ------------------------------------------------------------------
    def step(self, accion):
        dt = 1.0

        # 1. Check batería muerta
        if self.state["bateria_actual_wh"] <= 0.1:
            accion = {"luz": 0, "ventilador": 0, "riego": 0, "deep_sleep": 1}
            self.state["modo_cpu"] = "DEAD"
        elif accion.get("deep_sleep", False):
            accion["luz"] = 0
            accion["ventilador"] = 0
            accion["riego"] = 0
            self.state["modo_cpu"] = "SLEEP"
        else:
            self.state["modo_cpu"] = "ACTIVE"

        # 2. Física térmica
        # Temperatura exterior fija y realista — clima tropical/subtropical.
        # Independiente del cultivo: el ambiente no cambia según lo que siembres.
        # Esto genera presión térmica real en cultivos fríos (lechuga, fresa),
        # forzando al ventilador a activarse y produciendo datos representativos
        # de lo que el hardware va a vivir en la realidad.
        TEMP_EXT_DIA   = 32.0   # pico diurno (clima tropical, verano)
        TEMP_EXT_NOCHE = 22.0   # mínimo nocturno
        temp_ext = TEMP_EXT_DIA if (9 < self.state["hora_dia"] < 16) else TEMP_EXT_NOCHE
        delta_temp = 0
        if accion["luz"]:        delta_temp += self.PHYSICS["calor_led_gain"] * dt
        if accion["ventilador"]: delta_temp -= self.PHYSICS["frio_fan_loss"] * dt
        diferencia = temp_ext - self.state["temp_int"]
        delta_temp += (diferencia * self.PHYSICS["aislamiento_factor"]) * dt
        self.state["temp_int"] += delta_temp

        # 3. Hidrología
        evap = (0.4 + (self.state["temp_int"] * 0.03)) * dt
        if accion["luz"]: evap += 0.2 * dt
        self.state["hum_suelo"] = max(0, self.state["hum_suelo"] - evap)
        if accion["riego"]:
            self.state["hum_suelo"] = min(100, self.state["hum_suelo"] + 15.0)

        # 4. Energía
        generacion_solar = self._simular_sol(self.state["hora_dia"]) * dt
        consumo_total = 0
        if self.state["modo_cpu"] in ["SLEEP", "DEAD"]:
            consumo_total += self.HARDWARE["consumo_esp32_sleep_w"] * dt
        else:
            consumo_total += self.HARDWARE["consumo_esp32_active_w"] * dt
            if accion["luz"]:        consumo_total += self.HARDWARE["consumo_led_w"] * dt
            if accion["ventilador"]: consumo_total += self.HARDWARE["consumo_fan_w"] * dt
            if accion["riego"]:      consumo_total += self.HARDWARE["consumo_pump_w"] * dt

        self.state["bateria_actual_wh"] = max(
            0,
            min(
                self.HARDWARE["bateria_capacidad_wh"],
                self.state["bateria_actual_wh"] + generacion_solar - consumo_total
            )
        )
        max_bat = self.HARDWARE["bateria_capacidad_wh"]
        self.state["bateria_pct"] = (self.state["bateria_actual_wh"] / max_bat) * 100

        # 5. Tiempo
        self.state["hora_dia"] += dt
        if self.state["hora_dia"] >= 24.0:
            self.state["hora_dia"] = 0.0
            self.state["dia_simulacion"] += 1

        obs = self.state.copy()
        obs["temp_int"] += random.uniform(-0.1, 0.1)

        recompensa = self._calcular_recompensa(obs, accion, generacion_solar, consumo_total)

        return obs, generacion_solar, consumo_total, recompensa


# ------------------------------------------------------------------
if __name__ == "__main__":
    # Test: cultivo por nombre exacto
    env1 = Greenhouse("Habanero Pepper")
    print(f"Test 1 OK — Target temp: {env1.TARGET_TEMP}°C")

    # Test: alias
    env2 = Greenhouse("Chile Habanero")   # alias definido en config_agronomo.json
    print(f"Test 2 OK — Alias resuelto, target: {env2.TARGET_TEMP}°C")

    # Test: cultivo inexistente → debe lanzar ValueError, no silencio
    try:
        env3 = Greenhouse("Cilantro")
    except ValueError as e:
        print(f"Test 3 OK — Fallo ruidoso:\n{e}")
