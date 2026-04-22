# 🔭 Radar de Oportunidades (Watchlist)

> [!TIP] Estrategia
> "Esperar el pitch correcto. La paciencia paga más que la actividad."

## 📡 Activos en Vigilancia

```dataview
TABLE without id
	file.link as "Empresa",
	ticker as "Ticker",
	precio_entrada as "Precio Objetivo",
	moat as "Ventaja Competitiva"
FROM "Vita/💰 Finanzas/🔭 Watchlist"
WHERE file.name != this.file.name AND file.name != "Plantilla Watchlist"
SORT file.mtime DESC
```


[[💰 Finanzas]]