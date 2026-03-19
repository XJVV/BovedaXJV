import json
import os
import re
import math
import statistics
import time
from ddgs import DDGS

# ---------------------------------------------------------
# FUENTES
# ---------------------------------------------------------
SOURCES = [
    {"name": "Cornell Extension", "domain": "cornell.edu",     "peso": 1.0},
    {"name": "Purdue Extension",  "domain": "purdue.edu",      "peso": 0.9},
    {"name": "UF IFAS",           "domain": "ufl.edu",         "peso": 0.9},
    {"name": "Texas A&M AgriLife","domain": "tamu.edu",        "peso": 0.9},
    {"name": "WikiFarmer",        "domain": "wikifarmer.com",  "peso": 0.6}
]

FALLBACK_DATA = {
    "Tomato":          {"temp": (18, 27), "hum": (60, 80)},
    "Lettuce":         {"temp": (10, 20), "hum": (50, 70)},
    "Habanero Pepper": {"temp": (22, 32), "hum": (50, 70)}
}

# ---------------------------------------------------------
class CropResearcher:
    def __init__(self, config_path=None):
        print("🤖 Agente Agrónomo v5.2 (JSON plano para ESP32)")
        self.ddgs = DDGS()
        self.config = self._cargar_config(config_path)

    # ------------------------------------------------------------------
    # CONFIG
    # ------------------------------------------------------------------
    def _cargar_config(self, ruta=None):
        """FIX: ahora sí carga y usa config_agronomo.json."""
        candidatos = [
            ruta,
            os.path.join(os.path.dirname(__file__), "config_agronomo.json"),
            os.path.join(os.path.dirname(__file__), "..", "01_Simulacion", "config_agronomo.json"),
        ]
        for r in candidatos:
            if r and os.path.exists(r):
                try:
                    with open(r, encoding="utf-8") as f:
                        cfg = json.load(f)
                    print(f"📋 Config cargado desde: {r}")
                    return cfg
                except Exception as e:
                    print(f"⚠️  Error leyendo config: {e}")
        print("⚠️  config_agronomo.json no encontrado — usando defaults")
        return {
            "ajustes_sistema": {"max_tolerancia_temp": 5.0},
            "alias_cultivos": {}
        }

    def _resolver_alias(self, nombre):
        alias = self.config.get("alias_cultivos", {})
        resuelto = alias.get(nombre, nombre)
        if resuelto != nombre:
            print(f"   🔀 Alias: '{nombre}' → '{resuelto}'")
        return resuelto

    # ------------------------------------------------------------------
    # EXTRACCIÓN DE VALORES
    # ------------------------------------------------------------------
    def _f_to_c(self, f):
        return (f - 32) * 5 / 9

    def _extraer_temperaturas(self, texto):
        resultados = []
        for a, b in re.findall(r'(\d{2})\s?[–\-]\s?(\d{2})\s?°?C', texto):
            resultados.append((float(a) + float(b)) / 2)
        for a, b in re.findall(r'(\d{2})\s?[–\-]\s?(\d{2})\s?°?F', texto):
            resultados.append(self._f_to_c((float(a) + float(b)) / 2))
        for v in re.findall(r'(\d{2})\s?°?C', texto):
            val = float(v)
            if 8 <= val <= 40:
                resultados.append(val)
        for v in re.findall(r'(\d{2})\s?°?F', texto):
            val = self._f_to_c(float(v))
            if 8 <= val <= 40:
                resultados.append(val)
        return resultados

    def _extraer_humedad(self, texto):
        """
        Busca rangos de humedad de suelo en texto.
        Ej: "60-80% soil moisture" / "field capacity 70%"
        """
        resultados = []
        # Rangos explícitos de humedad de suelo
        for a, b in re.findall(
            r'(\d{2})\s?[–\-]\s?(\d{2})\s?%\s*(?:soil\s*moisture|field\s*capacity|volumetric)',
            texto, re.IGNORECASE
        ):
            resultados.append((float(a) + float(b)) / 2)
        # Porcentaje solo cerca de palabras clave
        for v in re.findall(
            r'(\d{2})\s?%\s*(?:soil|moisture|humidity|field)',
            texto, re.IGNORECASE
        ):
            val = float(v)
            if 20 <= val <= 100:
                resultados.append(val)
        return resultados

    # ------------------------------------------------------------------
    # SCRAPER
    # ------------------------------------------------------------------
    def _buscar_fuente(self, cultivo, fuente, buscar_humedad=False):
        tema = "soil moisture requirements" if buscar_humedad else "optimal growing temperature"
        query = f"{cultivo} {tema} site:{fuente['domain']}"
        hallazgos_temp = []
        hallazgos_hum  = []

        print(f"      📡 {fuente['name']} {'(humedad)' if buscar_humedad else '(temp)'}")

        try:
            resultados = self.ddgs.text(query, max_results=3)
            for r in resultados:
                texto = r["body"]
                for t in self._extraer_temperaturas(texto):
                    hallazgos_temp.append({"valor": t, "peso": fuente["peso"],
                                           "fuente": fuente["name"], "url": r["href"]})
                for h in self._extraer_humedad(texto):
                    hallazgos_hum.append({"valor": h, "peso": fuente["peso"],
                                          "fuente": fuente["name"], "url": r["href"]})
        except Exception as e:
            print(f"         ❌ Error: {e}")

        time.sleep(1)
        return hallazgos_temp, hallazgos_hum

    # ------------------------------------------------------------------
    # CONSENSO
    # ------------------------------------------------------------------
    def _consenso(self, hallazgos, fallback_valor, fallback_margen=3.0):
        if not hallazgos:
            return fallback_valor, fallback_margen

        valores = [h["valor"] for h in hallazgos]
        pesos   = [h["peso"]  for h in hallazgos]
        media   = sum(v * p for v, p in zip(valores, pesos)) / sum(pesos)
        margen  = min(statistics.stdev(valores) * 1.5, 5.0) if len(valores) > 1 else fallback_margen
        return round(media, 1), round(margen, 1)

    # ------------------------------------------------------------------
    # API PRINCIPAL
    # ------------------------------------------------------------------
    def investigar_cultivo(self, cultivo_raw):
        cultivo = self._resolver_alias(cultivo_raw)
        print(f"\n🔎 INVESTIGANDO: {cultivo}")

        hallazgos_temp = []
        hallazgos_hum  = []

        for fuente in SOURCES:
            t, h = self._buscar_fuente(cultivo, fuente, buscar_humedad=False)
            hallazgos_temp.extend(t)
            # Segunda búsqueda por humedad solo si no hay datos aún
            if not hallazgos_hum:
                _, h2 = self._buscar_fuente(cultivo, fuente, buscar_humedad=True)
                hallazgos_hum.extend(h2)

        # Fallback por cultivo
        fb = FALLBACK_DATA.get(cultivo, {"temp": (20, 25), "hum": (50, 70)})
        fb_temp = (fb["temp"][0] + fb["temp"][1]) / 2
        fb_hum  = (fb["hum"][0]  + fb["hum"][1])  / 2

        if not hallazgos_temp:
            print("   ⚠️  Sin datos de temperatura — usando fallback.")
        if not hallazgos_hum:
            print("   ⚠️  Sin datos de humedad — usando fallback.")

        temp_final, margen_temp = self._consenso(hallazgos_temp, fb_temp)
        hum_final,  margen_hum  = self._consenso(hallazgos_hum,  fb_hum, fallback_margen=10.0)

        print(f"   ✅ Temp: {temp_final}°C | Hum suelo: {hum_final}%")

        # JSON plano — el ESP32 lo parsea directo sin anidar
        fuentes_unicas = list(set(h["fuente"] for h in hallazgos_temp + hallazgos_hum))
        return {
            "id_cultivo":          cultivo,
            "temperatura_ideal":   temp_final,
            "humedad_suelo_ideal": hum_final,
            "origen":              " + ".join(fuentes_unicas) if fuentes_unicas else "Fallback científico",
            "confianza":           "alta" if fuentes_unicas else "media"
        }

    def generar_archivo_maestro(self, lista):
        data = {"version": "5.2", "cultivos": []}
        for c in lista:
            data["cultivos"].append(self.investigar_cultivo(c))

        ruta = os.path.join(os.path.dirname(__file__), "..", "00_Docs")
        os.makedirs(ruta, exist_ok=True)
        destino = os.path.join(ruta, "Perfiles_Cultivo.json")

        with open(destino, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"\n💾 Archivo generado: {destino}")
        print(f"   {len(data['cultivos'])} cultivos con temp + humedad de suelo")

# ---------------------------------------------------------
if __name__ == "__main__":
    agente = CropResearcher()
    agente.generar_archivo_maestro([
        "Tomato",
        "Lettuce",
        "Habanero Pepper"
    ])
