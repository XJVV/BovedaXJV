import json
import math
import random
import os

# ---------------------------------------------------------
# CLASE: ENTORNO DE SIMULACIÓN (PHYSICS ENGINE v2.3 - Init Fixed)
# ---------------------------------------------------------
class Greenhouse:
    def __init__(self, cultivo_objetivo="Tomate Cherry"):
        print(f"🌱 Inicializando Invernadero Virtual v2.3 para: {cultivo_objetivo}")
        
        self.perfil = self._cargar_perfil(cultivo_objetivo)
        if not self.perfil:
            self.perfil = {"parametros_optimos": {"temperatura_ideal": 24.0}}

        # --- HARDWARE ---
        self.HARDWARE = {
            "bateria_capacidad_wh": 50.0, 
            "panel_solar_max_w": 20.0,    
            "consumo_led_w": 10.0,        
            "consumo_pump_w": 5.0,        
            "consumo_fan_w": 2.0,         
            "consumo_esp32_active_w": 0.6,
            "consumo_esp32_sleep_w": 0.01 
        }

        self.state = {
            "temp_int": 20.0,      # °C
            "hum_suelo": 50.0,     # %
            "bateria_actual_wh": 40.0, 
            "hora_dia": 8.0,
            "dia_simulacion": 1,
            "modo_cpu": "ACTIVE"
        }
        
        # 🔥 BUGFIX CRÍTICO: Calcular el % inicial AQUÍ para que el agente lo vea
        max_bat = self.HARDWARE["bateria_capacidad_wh"]
        self.state["bateria_pct"] = (self.state["bateria_actual_wh"] / max_bat) * 100
        
        self.PHYSICS = {
            "calor_led_gain": 0.8,     
            "frio_fan_loss": 1.2,      
            "aislamiento_factor": 0.15 
        }

    def _cargar_perfil(self, nombre):
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_json = os.path.join(ruta_script, "..", "00_Docs", "Perfiles_Cultivo.json")
        if not os.path.exists(ruta_json): return None
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for c in data["cultivos"]:
                    if c.get("id_cultivo") == nombre or c.get("categoria_base") == nombre:
                        return c
            return None
        except: return None

    def _simular_sol(self, hora):
        if 7 <= hora <= 17: 
            intensidad = math.sin(((hora - 7) / 10) * math.pi)
            return max(0, intensidad * self.HARDWARE["panel_solar_max_w"])
        return 0

    def step(self, accion):
        dt = 1.0 
        
        # 1. CHECK DE MUERTE SÚBITA
        if self.state["bateria_actual_wh"] <= 0.1:
            accion = {'luz': 0, 'ventilador': 0, 'riego': 0, 'deep_sleep': 1}
            self.state["modo_cpu"] = "DEAD"
        
        # 2. EXCLUSIÓN MUTUA
        elif accion.get('deep_sleep', False):
            accion['luz'] = 0
            accion['ventilador'] = 0
            accion['riego'] = 0
            self.state["modo_cpu"] = "SLEEP"
        else:
            self.state["modo_cpu"] = "ACTIVE"

        # 3. FÍSICA TÉRMICA
        temp_ext = 28.0 if (9 < self.state["hora_dia"] < 16) else 18.0
        
        delta_temp = 0
        if accion['luz']: delta_temp += self.PHYSICS["calor_led_gain"] * dt
        if accion['ventilador']: delta_temp -= self.PHYSICS["frio_fan_loss"] * dt
        
        diferencia = temp_ext - self.state["temp_int"]
        delta_temp += (diferencia * self.PHYSICS["aislamiento_factor"]) * dt
        
        self.state["temp_int"] += delta_temp

        # 4. HIDROLOGÍA
        evap = (0.4 + (self.state["temp_int"] * 0.03)) * dt
        if accion['luz']: evap += 0.2 * dt
        
        self.state["hum_suelo"] -= evap
        if accion['riego']:
            self.state["hum_suelo"] = min(100, self.state["hum_suelo"] + 15.0)

        # 5. BALANCE ENERGÉTICO (Wh)
        generacion_solar = self._simular_sol(self.state["hora_dia"]) * dt
        
        consumo_total = 0
        if self.state["modo_cpu"] in ["SLEEP", "DEAD"]:
             consumo_total += self.HARDWARE["consumo_esp32_sleep_w"] * dt
        else:
             consumo_total += self.HARDWARE["consumo_esp32_active_w"] * dt
             if accion['luz']: consumo_total += self.HARDWARE["consumo_led_w"] * dt
             if accion['ventilador']: consumo_total += self.HARDWARE["consumo_fan_w"] * dt
             if accion['riego']: consumo_total += self.HARDWARE["consumo_pump_w"] * dt
        
        balance = generacion_solar - consumo_total
        self.state["bateria_actual_wh"] += balance
        
        # Clamping
        max_bat = self.HARDWARE["bateria_capacidad_wh"]
        self.state["bateria_actual_wh"] = max(0, min(max_bat, self.state["bateria_actual_wh"]))
        
        # Cálculo del porcentaje (Actualizado)
        self.state["bateria_pct"] = (self.state["bateria_actual_wh"] / max_bat) * 100

        # 6. TIEMPO
        self.state["hora_dia"] += dt
        if self.state["hora_dia"] >= 24.0:
            self.state["hora_dia"] = 0.0
            self.state["dia_simulacion"] += 1
            
        obs = self.state.copy()
        obs["temp_int"] += random.uniform(-0.1, 0.1)
        
        return obs, generacion_solar, consumo_total

if __name__ == "__main__":
    # Test rápido de init
    env = Greenhouse()
    print(f"Test Init: Bateria PCT = {env.state['bateria_pct']}%") 
    # Debería imprimir 80.0%