# 🧠 Centro de Investigación (Tesis de Inversión)

> [!QUOTE] Filosofía
> "No compras una acción, compras una parte de un negocio. Haz la tarea."

## 📚 Biblioteca de Tesis Activas

```dataview
TABLE without id
	file.link as "Empresa / Tesis",
	ticker as "Ticker",
	sector as "Sector",
	conviction as "Convicción (1-5)"
FROM "Vita/💰 Finanzas/Tesis"
WHERE file.name != this.file.name
SORT file.mtime DESC
```


[[💰 Finanzas]]