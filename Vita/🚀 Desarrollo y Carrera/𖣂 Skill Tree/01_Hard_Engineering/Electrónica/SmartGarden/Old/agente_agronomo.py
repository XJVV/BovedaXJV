import json
import os
import re
import math
import statistics
import time
from ddgs import DDGS

# ---------------------------------------------------------
# FUENTES REALMENTE SCRAPEABLES
# ---------------------------------------------------------
SOURCES = [
    {"name": "Cornell Extension", "domain": "cornell.edu", "peso": 1.0},
    {"name": "Purdue Extension", "domain": "purdue.edu", "peso": 0.9},
    {"name": "UF IFAS", "domain": "ufl.edu", "peso": 0.9},
    {"name": "Texas A&M AgriLife", "domain": "tamu.edu", "peso": 0.9},
    {"name": "WikiFarmer", "domain": "wikifarmer.com", "peso": 0.6}
]

# ---------------------------------------------------------
# FALLBACK CIENTÍFICO (GROUND TRUTH)
# ---------------------------------------------------------
FALLBACK_DATA = {
    "Tomato": (18, 27),
    "Lettuce": (10, 20),
    "Habanero Pepper": (22, 32)
}

class CropResearcher:
    def __init__(self):
        print("🤖 Agente Agrónomo v5.0 (Robust Web Intelligence)")
        self.ddgs = DDGS()

    # -----------------------------------------------------
    # UTILIDADES
    # -----------------------------------------------------
    def _f_to_c(self, f):
        return (f - 32) * 5 / 9

    def _extraer_temperaturas(self, texto):
        """
        Detecta:
        - Rangos: 20-25 °C / 68–77°F
        - Valores sueltos
        """
        resultados = []

        # Rangos °C
        for a, b in re.findall(r'(\d{2})\s?[–\-]\s?(\d{2})\s?°?C', texto):
            resultados.append((float(a) + float(b)) / 2)

        # Rangos °F
        for a, b in re.findall(r'(\d{2})\s?[–\-]\s?(\d{2})\s?°?F', texto):
            resultados.append(self._f_to_c((float(a) + float(b)) / 2))

        # Valores individuales °C
        for v in re.findall(r'(\d{2})\s?°?C', texto):
            val = float(v)
            if 8 <= val <= 40:
                resultados.append(val)

        # Valores individuales °F
        for v in re.findall(r'(\d{2})\s?°?F', texto):
            val = self._f_to_c(float(v))
            if 8 <= val <= 40:
                resultados.append(val)

        return resultados

    # -----------------------------------------------------
    # SCRAPER REAL
    # -----------------------------------------------------
    def _buscar_fuente(self, cultivo, fuente):
        query = f"{cultivo} optimal growing temperature site:{fuente['domain']}"
        hallazgos = []

        print(f"      📡 {fuente['name']}")

        try:
            resultados = self.ddgs.text(query, max_results=3)
            for r in resultados:
                texto = r["body"]
                temps = self._extraer_temperaturas(texto)
                for t in temps:
                    hallazgos.append({
                        "valor": t,
                        "peso": fuente["peso"],
                        "fuente": fuente["name"],
                        "url": r["href"]
                    })
        except Exception as e:
            print(f"         ❌ Error: {e}")

        time.sleep(1)
        return hallazgos

    # -----------------------------------------------------
    # API PRINCIPAL
    # -----------------------------------------------------
    def investigar_cultivo(self, cultivo):
        print(f"\n🔎 INVESTIGANDO: {cultivo}")
        hallazgos = []

        for fuente in SOURCES:
            hallazgos.extend(self._buscar_fuente(cultivo, fuente))

        # ---------------- FALLBACK ----------------
        if not hallazgos:
            print("   ⚠️ Sin datos web. Usando fallback científico.")
            tmin, tmax = FALLBACK_DATA.get(cultivo, (20, 25))
            return self._formato_final(
                cultivo,
                [(tmin + tmax) / 2],
                "Fallback Científico"
            )

        # ---------------- CONSENSO ----------------
        valores = []
        pesos = []

        for h in hallazgos:
            valores.append(h["valor"])
            pesos.append(h["peso"])

        temp_final = sum(v * p for v, p in zip(valores, pesos)) / sum(pesos)
        margen = min(statistics.stdev(valores) * 1.5, 5.0) if len(valores) > 1 else 3.0

        print(f"   ✅ Consenso: {temp_final:.1f}°C")

        return {
            "id_cultivo": cultivo,
            "origen_datos": "Web Scraping (Extensión Universitaria)",
            "fuentes": list(set(h["fuente"] for h in hallazgos)),
            "parametros_optimos": {
                "temperatura_ideal": round(temp_final, 1),
                "margen_tolerancia": round(margen, 1)
            }
        }

    def _formato_final(self, cultivo, valores, origen):
        return {
            "id_cultivo": cultivo,
            "origen_datos": origen,
            "parametros_optimos": {
                "temperatura_ideal": round(statistics.mean(valores), 1),
                "margen_tolerancia": 3.0
            }
        }

    def generar_archivo_maestro(self, lista):
        data = {"version": "5.0", "cultivos": []}
        for c in lista:
            data["cultivos"].append(self.investigar_cultivo(c))

        ruta = os.path.join(os.path.dirname(__file__), "..", "00_Docs")
        os.makedirs(ruta, exist_ok=True)

        with open(os.path.join(ruta, "Perfiles_Cultivo.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("\n💾 Archivo generado correctamente.")

# ---------------------------------------------------------
if __name__ == "__main__":
    agente = CropResearcher()
    agente.generar_archivo_maestro([
        "Tomato",
        "Lettuce",
        "Habanero Pepper"
    ])
