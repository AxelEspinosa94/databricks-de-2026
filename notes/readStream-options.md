# 🔥 Streaming Sources en `readStream`  

Cuando usas:

```python
spark.readStream.format("algo")
```

El valor `"algo"` define **la fuente de streaming**: de dónde vienen los datos y cómo Spark los interpreta.

---

# 🟩 1. Fuentes nativas de Spark (open source)

Estas funcionan en cualquier distribución de Spark, no solo en Databricks.

## ✔ `rate`

Genera datos sintéticos para pruebas.

```python
spark.readStream.format("rate").load()
```

Produce:
- `timestamp`
- `value` (contador incremental)

---

## ✔ `rate-micro-batch`

Similar a `rate`, pero con control más preciso de micro‑batches.

---

## ✔ `socket`

Lee texto desde un socket TCP.

```python
spark.readStream.format("socket")
  .option("host", "localhost")
  .option("port", 9999)
  .load()
```

---

## ✔ `kafka`

Lee mensajes desde Kafka.

```python
spark.readStream.format("kafka")
  .option("kafka.bootstrap.servers", "host:9092")
  .option("subscribe", "topic")
  .load()
```

Columnas generadas:
- `key`
- `value`
- `topic`
- `partition`
- `offset`
- `timestamp`

---

## ✔ `json`, `csv`, `text`, `parquet`

Lectura directa de archivos en modo streaming.

```python
spark.readStream.format("json").load("/path")
```

Requiere un filesystem real (por eso usamos **Volumes** en Free Edition).

---

# 🟦 2. Fuentes extendidas por Databricks

Estas **solo existen en Databricks** y son las más usadas en producción.

## ⭐ `cloudFiles` (Auto Loader)

Fuente recomendada para ingestión continua desde almacenamiento en la nube.

```python
spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .load("/Volumes/<catalog>/<schema>/<volume>/input")
```

Ventajas:
- Detecta nuevos archivos automáticamente  
- Maneja schema evolution  
- Escala mejor que `json`/`csv` nativo  
- Tolerante a fallos  
- Ideal para pipelines reales  

Por eso se usa en el **Ejercicio 1**.

---

## ⭐ `delta`
Permite leer una tabla Delta como stream.

```python
spark.readStream.format("delta").table("mi_tabla")
```

Útil para:
- CDC (Change Data Capture)  
- Pipelines incrementales  
- Propagar cambios entre tablas  

---

# 🟥 3. Formatos que NO son streaming

Estos funcionan solo con `read`, no con `readStream`:

- `jdbc`
- `orc`
- `avro`
- `binaryFile`
- `image`

---

# 🎯 Resumen práctico

| Caso | Formato recomendado |
|------|---------------------|
| Ingestión continua de archivos | `cloudFiles` |
| Pruebas rápidas | `rate` |
| Kafka | `kafka` |
| CDC desde Delta | `delta` |
| Lectura de archivos sin Auto Loader | `json`, `csv`, `parquet` |

---

# 🚀 ¿Qué estás haciendo en el Ejercicio 1?

Estás usando:

```python
spark.readStream.format("cloudFiles")
```

Porque:
- Estás leyendo archivos nuevos que llegan a un folder  
- Quieres ingestión continua  
- Estás en Databricks (Auto Loader es nativo)  
- Estás usando Volumes (soportan streaming)  

Es la forma **correcta y profesional** de hacer ingestión en Databricks.

------------------------------------------------------------------------------

# 🔥 Streaming Sources in `readStream`

When you use:

```python
spark.readStream.format("something")
```

The value `"something"` defines **the streaming source**: where the data comes from and how Spark interprets it.

---

# 🟩 1. Native Spark Sources (open source)

These work in any Spark distribution, not just Databricks.

## ✔ `rate`

Generates synthetic data for testing.

```python
spark.readStream.format("rate").load()
```

Produces:
- `timestamp`
- `value` (incremental counter)

---

## ✔ `rate-micro-batch`

Similar to `rate`, but with more precise micro‑batch control.

---

## ✔ `socket`

Reads text from a TCP socket.

```python
spark.readStream.format("socket")
  .option("host", "localhost")
  .option("port", 9999)
  .load()
```

---

## ✔ `kafka`

Reads messages from Kafka.

```python
spark.readStream.format("kafka")
  .option("kafka.bootstrap.servers", "host:9092")
  .option("subscribe", "topic")
  .load()
```

Generated columns:
- `key`
- `value`
- `topic`
- `partition`
- `offset`
- `timestamp`

---

## ✔ `json`, `csv`, `text`, `parquet`

Direct file streaming.

```python
spark.readStream.format("json").load("/path")
```

Requires a real filesystem (which is why we use **Volumes** in Free Edition).

---

# 🟦 2. Databricks‑Extended Sources

These **exist only in Databricks** and are the most commonly used in production.

## ⭐ `cloudFiles` (Auto Loader)

Recommended source for continuous ingestion from cloud storage.

```python
spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .load("/Volumes/<catalog>/<schema>/<volume>/input")
```

Advantages:
- Automatically detects new files  
- Handles schema evolution  
- Scales better than native `json`/`csv`  
- Fault‑tolerant  
- Ideal for real production pipelines  

This is why it is used in **Exercise 1**.

---

## ⭐ `delta`

Allows reading a Delta table as a stream.

```python
spark.readStream.format("delta").table("my_table")
```

Useful for:
- CDC (Change Data Capture)  
- Incremental pipelines  
- Propagating changes across tables  

---

# 🟥 3. Formats that are NOT streaming

These work only with `read`, not with `readStream`:

- `jdbc`
- `orc`
- `avro`
- `binaryFile`
- `image`

---

# 🎯 Practical Summary

| Use Case | Recommended Format |
|----------|---------------------|
| Continuous file ingestion | `cloudFiles` |
| Quick testing | `rate` |
| Kafka | `kafka` |
| CDC from Delta | `delta` |
| File streaming without Auto Loader | `json`, `csv`, `parquet` |

---

# 🚀 What are you doing in Exercise 1?

You are using:

```python
spark.readStream.format("cloudFiles")
```

Because:
- You are reading new files arriving in a folder  
- You want continuous ingestion  
- You are in Databricks (Auto Loader is native)  
- You are using Volumes (they support streaming)  

This is the **correct and professional** way to build ingestion pipelines in Databricks.
