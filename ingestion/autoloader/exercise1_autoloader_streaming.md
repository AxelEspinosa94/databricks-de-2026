# 🚀 Ejercicio 1 — Ingestión con Auto Loader, Volumes y Delta Lake

Este ejercicio demuestra cómo implementar un pipeline de ingestión usando **Databricks Auto Loader**, **Volumes**, **Delta Lake** y **Structured Streaming** dentro de un entorno **Databricks Free Edition**.

Aprenderás:

- Cómo leer archivos de manera incremental con Auto Loader  
- Cómo manejar `schemaLocation` y `checkpointLocation`  
- Cómo escribir datos en una tabla Delta  
- Cómo usar triggers compatibles con Free Edition  
- Cómo validar que la tabla se actualiza correctamente  

---

## 📁 Estructura del ejercicio

```
ingestion/
└── autoloader/
    ├── exercise1_autoloader_streaming.py
    └── README.md   ← este archivo
```

---

## 🎯 Objetivo

Construir un pipeline de ingestión que:

1. Lea archivos JSON desde un Volume usando Auto Loader  
2. Procese los archivos nuevos de forma incremental  
3. Escriba los datos en una tabla Delta  
4. Permita re‑ejecutar el stream cada vez que se agreguen archivos nuevos  

---

## ⚙️ Configuración del stream

### **1. Lectura con Auto Loader**

```python
df_stream = (
    spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/Volumes/workspace/default/streaming_demo/schema")
        .load("/Volumes/workspace/default/streaming_demo/input")
)
```

### **2. Escritura en Delta Lake**

> En Free Edition, solo se permiten triggers finitos (`availableNow` o `once`).

```python
(df_stream.writeStream
    .format("delta")
    .option("checkpointLocation", "/Volumes/workspace/default/streaming_demo/chk")
    .trigger(availableNow=True)
    .outputMode("append")
    .table("workspace.default.streaming_demo"))
```

---

## ⚡ Triggers disponibles en Databricks

| Trigger | Descripción | Free Edition | Pro/Enterprise |
|--------|-------------|--------------|----------------|
| `processingTime="10 seconds"` | Streaming continuo real | ❌ No soportado | ✔ Sí |
| `once=True` | Procesa un solo batch | ✔ Sí | ✔ Sí |
| `availableNow=True` | Procesa todos los micro‑batches pendientes y termina | ✔ Sí | ✔ Sí |

En este ejercicio usamos:

```python
.trigger(availableNow=True)
```

porque es el más cercano a streaming continuo en Free Edition.

---

## 📥 Cómo agregar nuevos archivos al stream

Ejemplo para insertar 4 archivos JSON:

```python
dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file2.json",
               """{"id": 2, "value": "nuevo archivo 2"}""", True)

dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file3.json",
               """{"id": 3, "value": "nuevo archivo 3"}""", True)

dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file4.json",
               """{"id": 4, "value": "nuevo archivo 4"}""", True)

dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file5.json",
               """{"id": 5, "value": "nuevo archivo 5"}""", True)
```

---

## 🔄 Flujo correcto en Free Edition

1. **Sube archivos nuevos** al folder de entrada  
2. **Ejecuta solo el writeStream**  
3. El stream procesa los archivos y termina  
4. **Valida la tabla Delta**

---

## 🔍 Validación de la tabla

```python
spark.table("workspace.default.streaming_demo").show()
```

O para contar filas:

```python
spark.table("workspace.default.streaming_demo").count()
```

O su equivalente en SQL:

```sql
SELECT * FROM workspace.default.streaming_demo;
```

O para contar filas:

```sql
SELECT COUNT(1) FROM workspace.default.streaming_demo;
```


---

## 🧠 Notas importantes

- Auto Loader **no re‑procesa archivos con el mismo nombre**  
- Si modificas un archivo existente, **no se vuelve a cargar**  
- Para re‑procesar un archivo, cambia su nombre o borra el checkpoint  
- `df_stream.show()` **no** muestra la tabla Delta, solo la fuente  
- En Free Edition **no existe streaming continuo**  

---

## 🏁 Resultado final

Al completar este ejercicio, tendrás un pipeline de ingestión funcional que:

- Detecta archivos nuevos automáticamente  
- Escribe datos en Delta Lake  
- Mantiene historial mediante checkpoints  
- Funciona correctamente en Databricks Free Edition  

Este es el primer paso hacia un pipeline completo estilo **Bronze → Silver → Gold**.


-------------------------------------------------------------------------------------------------------

# 🚀 Exercise 1 — Ingestion with Auto Loader, Volumes, and Delta Lake

This exercise demonstrates how to implement an ingestion pipeline using **Databricks Auto Loader**, **Volumes**, **Delta Lake**, and **Structured Streaming** within a **Databricks Free Edition** environment.

You will learn:

- How to read files incrementally with Auto Loader  
- How to manage `schemaLocation` and `checkpointLocation`  
- How to write data into a Delta table  
- How to use triggers supported in Free Edition  
- How to validate that the Delta table updates correctly  

---

## 📁 Exercise Structure

```
ingestion/
└── autoloader/
    ├── exercise1_autoloader_streaming.py
    └── README.md   ← this file
```

---

## 🎯 Objective

Build an ingestion pipeline that:

1. Reads JSON files from a Volume using Auto Loader  
2. Processes new files incrementally  
3. Writes the data into a Delta table  
4. Allows re‑running the stream whenever new files are added  

---

## ⚙️ Stream Configuration

### **1. Reading with Auto Loader**

```python
df_stream = (
    spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/Volumes/workspace/default/streaming_demo/schema")
        .load("/Volumes/workspace/default/streaming_demo/input")
)
```

### **2. Writing to Delta Lake**

> In Free Edition, only finite triggers (`availableNow` or `once`) are supported.

```python
(df_stream.writeStream
    .format("delta")
    .option("checkpointLocation", "/Volumes/workspace/default/streaming_demo/chk")
    .trigger(availableNow=True)
    .outputMode("append")
    .table("workspace.default.streaming_demo"))
```

---

## ⚡ Available Triggers in Databricks

| Trigger | Description | Free Edition | Pro/Enterprise |
|--------|-------------|--------------|----------------|
| `processingTime="10 seconds"` | True continuous streaming | ❌ Not supported | ✔ Supported |
| `once=True` | Processes a single batch | ✔ Supported | ✔ Supported |
| `availableNow=True` | Processes all pending micro‑batches and stops | ✔ Supported | ✔ Supported |

In this exercise we use:

```python
.trigger(availableNow=True)
```

because it is the closest alternative to continuous streaming in Free Edition.

---

## 📥 How to Add New Files to the Stream

Example for inserting 4 JSON files:

```python
dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file2.json",
               """{"id": 2, "value": "new file 2"}""", True)

dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file3.json",
               """{"id": 3, "value": "new file 3"}""", True)

dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file4.json",
               """{"id": 4, "value": "new file 4"}""", True)

dbutils.fs.put("/Volumes/workspace/default/streaming_demo/input/file5.json",
               """{"id": 5, "value": "new file 5"}""", True)
```

---

## 🔄 Correct Workflow in Free Edition

1. **Upload new files** to the input folder  
2. **Run only the writeStream**  
3. The stream processes the new files and stops  
4. **Validate the Delta table**  

---

## 🔍 Table Validation

```python
spark.table("workspace.default.streaming_demo").show()
```

Or to count rows:

```python
spark.table("workspace.default.streaming_demo").count()
```

SQL equivalents:

```sql
SELECT * FROM workspace.default.streaming_demo;
```

```sql
SELECT COUNT(1) FROM workspace.default.streaming_demo;
```

---

## 🧠 Important Notes

- Auto Loader **does not re‑process files with the same name**  
- If you modify an existing file, **it will not be re‑ingested**  
- To re‑process a file, rename it or delete the checkpoint  
- `df_stream.show()` **does not** show the Delta table, only the source stream  
- Free Edition **does not support continuous streaming**  

---

## 🏁 Final Result

By completing this exercise, you will have a functional ingestion pipeline that:

- Automatically detects new files  
- Writes data into Delta Lake  
- Maintains state using checkpoints  
- Works correctly in Databricks Free Edition  

This is the first step toward a full **Bronze → Silver → Gold** pipeline.

---
