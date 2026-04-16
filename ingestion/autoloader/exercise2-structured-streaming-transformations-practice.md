---

# 🚀 Exercise 2 — Structured Streaming + Transformations

This exercise demonstrates how to apply **DataFrame API transformations** within a **Structured Streaming** pipeline using **Databricks Auto Loader**, **Volumes**, and **Delta Lake**.

You will learn:

- How to enrich a streaming DataFrame with `withColumn`
- How to filter records in a stream using `filter`
- How to select or transform fields before writing
- How to write the transformed stream into a new Delta table
- How to manage independent checkpoints for multiple pipelines

---

## 📁 Exercise Structure

```
ingestion/
└── autoloader/
    ├── exercise2_streaming_transformations.py
    └── README.md   ← this file
```

---

## 🎯 Objective

Build a streaming pipeline that:

1. Reads JSON files from a Volume using Auto Loader  
2. Applies transformations to the streaming DataFrame  
3. Writes the transformed data into a **new Delta table**  
4. Uses a **separate checkpoint** to avoid conflicts with Exercise 1  

---

## ⚙️ Stream Configuration

### **1. Read stream with Auto Loader + transformations**

```python
from pyspark.sql.functions import col, current_timestamp

df_stream2 = (
    spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/Volumes/workspace/default/streaming_demo/schema2")
        .load("/Volumes/workspace/default/streaming_demo/input")
        .withColumn("processed_at", current_timestamp())
        .filter(col("id") > 0)
)
```

### 🔍 Notes

- `schema2` is used to keep schema inference separate from Exercise 1.  
- The input folder is the same as Exercise 1.  
- A new column `processed_at` is added.  
- Records with `id <= 0` are filtered out.  

---

## 📝 2. Write the transformed stream to Delta Lake

> Free Edition supports only finite triggers (`availableNow` or `once`).

```python
(df_stream2.writeStream
    .format("delta")
    .option("checkpointLocation", "/Volumes/workspace/default/streaming_demo/chk2")
    .trigger(availableNow=True)
    .outputMode("append")
    .table("workspace.default.streaming_demo_transformed"))
```

### 🔍 Notes

- `chk2` is required to avoid interfering with Exercise 1’s checkpoint.  
- The output table is **streaming_demo_transformed**.  

---

## 📥 Adding new files to test the stream

```python
dbutils.fs.put(
    "/Volumes/workspace/default/streaming_demo/input/file10.json",
    """{"id": 10, "value": "exercise 2 file"}""",
    True
)
```

---

## 🔍 Validating the transformed table

### Python

```python
spark.table("workspace.default.streaming_demo_transformed").show()
```

### SQL

```sql
SELECT * FROM workspace.default.streaming_demo_transformed;
```

Count rows:

```sql
SELECT COUNT(1) FROM workspace.default.streaming_demo_transformed;
```

---

## 🧠 Important Notes

- Auto Loader **does not reprocess files with the same name**.  
- If you modify an existing file, it **will not be re‑ingested**.  
- To reprocess a file, rename it or delete the checkpoint.  
- Each streaming pipeline must have its **own checkpoint**.  
- Free Edition **does not support continuous streaming**.  

---

## 🏁 Final Result

By completing this exercise, you will have a streaming pipeline that:

- Reads data incrementally with Auto Loader  
- Applies transformations in real time  
- Writes enriched data into a new Delta table  
- Uses independent checkpoints for multiple pipelines  
- Works fully within Databricks Free Edition  

This exercise builds on Exercise 1 and prepares you for more advanced streaming topics such as joins, aggregations, and multi-hop pipelines.

---

---

# 🇲🇽 Versión en Español — Ejercicio 2

Este ejercicio demuestra cómo aplicar **transformaciones del DataFrame API** dentro de un pipeline de **Structured Streaming** usando **Databricks Auto Loader**, **Volumes** y **Delta Lake**.

Aprenderás:

- Cómo enriquecer un DataFrame en streaming con `withColumn`
- Cómo filtrar registros en un stream usando `filter`
- Cómo seleccionar o transformar campos antes de escribir
- Cómo escribir el stream transformado en una nueva tabla Delta
- Cómo manejar checkpoints independientes para múltiples pipelines

---

## 📁 Estructura del ejercicio

```
ingestion/
└── autoloader/
    ├── exercise2_streaming_transformations.py
    └── README.md   ← este archivo
```

---

## 🎯 Objetivo

Construir un pipeline de streaming que:

1. Lea archivos JSON desde un Volume usando Auto Loader  
2. Aplique transformaciones al DataFrame en streaming  
3. Escriba los datos transformados en una **nueva tabla Delta**  
4. Use un **checkpoint independiente** para evitar conflictos con el Ejercicio 1  

---

## ⚙️ Configuración del stream

### **1. Lectura con Auto Loader + transformaciones**

```python
from pyspark.sql.functions import col, current_timestamp

df_stream2 = (
    spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/Volumes/workspace/default/streaming_demo/schema2")
        .load("/Volumes/workspace/default/streaming_demo/input")
        .withColumn("processed_at", current_timestamp())
        .filter(col("id") > 0)
)
```

### 🔍 Notas

- Se usa `schema2` para mantener separado el esquema del Ejercicio 1.  
- El folder de entrada es el mismo del Ejercicio 1.  
- Se agrega la columna `processed_at`.  
- Se filtran registros donde `id <= 0`.  

---

## 📝 2. Escritura del stream transformado a Delta Lake

> Free Edition solo soporta triggers finitos (`availableNow` o `once`).

```python
(df_stream2.writeStream
    .format("delta")
    .option("checkpointLocation", "/Volumes/workspace/default/streaming_demo/chk2")
    .trigger(availableNow=True)
    .outputMode("append")
    .table("workspace.default.streaming_demo_transformed"))
```

### 🔍 Notas

- `chk2` evita interferir con el checkpoint del Ejercicio 1.  
- La tabla destino es **streaming_demo_transformed**.  

---

## 📥 Cómo agregar archivos nuevos para probar el stream

```python
dbutils.fs.put(
    "/Volumes/workspace/default/streaming_demo/input/file10.json",
    """{"id": 10, "value": "archivo ejercicio 2"}""",
    True
)
```

---

## 🔍 Validación de la tabla transformada

### Python

```python
spark.table("workspace.default.streaming_demo_transformed").show()
```

### SQL

```sql
SELECT * FROM workspace.default.streaming_demo_transformed;
```

Contar filas:

```sql
SELECT COUNT(1) FROM workspace.default.streaming_demo_transformed;
```

---

## 🧠 Notas importantes

- Auto Loader **no re‑procesa archivos con el mismo nombre**.  
- Si modificas un archivo existente, **no se vuelve a cargar**.  
- Para re‑procesar un archivo, cámbiale el nombre o borra el checkpoint.  
- Cada pipeline de streaming debe tener su **propio checkpoint**.  
- Free Edition **no soporta streaming continuo**.  

---

## 🏁 Resultado final

Al completar este ejercicio tendrás un pipeline de streaming que:

- Lee datos incrementalmente con Auto Loader  
- Aplica transformaciones en tiempo real  
- Escribe datos enriquecidos en una nueva tabla Delta  
- Usa checkpoints independientes para múltiples pipelines  
- Funciona completamente en Databricks Free Edition  

Este ejercicio construye sobre el Ejercicio 1 y te prepara para temas más avanzados como joins, agregaciones y pipelines multi-hop.

---
