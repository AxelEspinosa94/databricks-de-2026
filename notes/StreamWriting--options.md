# 📝 Opciones de escritura del stream  
## (outputMode en Structured Streaming)

# 🇪🇸 Español

## 🟦 ¿Qué variantes tiene `outputMode`?

Spark Structured Streaming tiene **3 modos principales**:

---

## 1) `append` (el más común)

✔ Solo escribe **nuevas filas**  
✔ No modifica lo que ya existe  
✔ Ideal para ingestión de archivos, Kafka, logs, IoT  
✔ Es el modo más eficiente  

**Ejemplos típicos:**
- Auto Loader  
- Kafka → Bronze  
- Archivos JSON → Delta  

---

## 2) `complete`

✔ Reescribe **toda la tabla** en cada micro‑batch  
✔ Solo funciona con **agregaciones** (ej. `groupBy`)  
✔ No funciona con sinks como Delta (solo con memory/table console)

**Ejemplo:**

```python
df.groupBy("country").count()
```

Cada batch produce toda la tabla agregada completa.

---

## 3) `update`

✔ Escribe solo las filas que cambiaron
✔ Requiere operaciones con estado (stateful)
✔ Funciona con agregaciones y joins con watermark

**Ejemplos:**

- Ventanas de tiempo
- Contadores por clave
- Joins de streams

---

## 🧩 Tabla resumen

| Modo `outputMode` | Qué escribe | Cuándo usarlo |
|-------------------|-------------|----------------|
| **append** | Solo nuevas filas | Ingestión de archivos, Auto Loader, Kafka, logs, IoT |
| **complete** | Reescribe toda la tabla | Agregaciones globales (`groupBy`) |
| **update** | Solo filas que cambiaron | Ventanas, joins, operaciones con estado |


-----------------------------------------------------------------------------------


# 🇺🇸 English

## 🟦 3. What variants does outputMode have?

Spark Structured Streaming has 3 main modes:

---

## 1) `append (the most common)`

✔ Writes only new rows
✔ Does not modify existing data
✔ Ideal for file ingestion, Kafka, logs, IoT
✔ Most efficient mode

**Typical examples:**

- Auto Loader
- Kafka → Bronze
- JSON files → Delta

---

## 2) `complete`
✔ Rewrites the entire table on every micro‑batch
✔ Works only with aggregations (e.g., groupBy)
✔ Does not work with sinks like Delta (only memory/table console)

**Example:**
```python
df.groupBy("country").count()
```

Each batch produces the full aggregated table.

---

## 3) `update`

✔ Writes only the rows that changed
✔ Requires stateful operations
✔ Works with aggregations and joins with watermark

**Examples:**

- Time windows
- Per‑key counters
- Stream‑stream joins

---

## 🧩 Summary Table


| `outputMode` | What it writes | When to use it |
|--------------|----------------|----------------|
| **append** | Only new rows | File ingestion, Auto Loader, Kafka, logs, IoT |
| **complete** | Full table rewrite | Global aggregations (`groupBy`) |
| **update** | Only updated rows | Windows, joins, stateful operations |


---

