
---

# 🟩 **Ejercicio 8 — COPY INTO (Bilingüe, Adaptado a Free Edition)**

# 🧩 Exercise 8 — COPY INTO with Volumes  
## Bilingual (English + Spanish)  
## Fully compatible with Databricks Free Edition

---

# 🇺🇸 ENGLISH VERSION

# 1. Objective

Practice batch ingestion using **COPY INTO**, including:

- Loading files from Volumes  
- Incremental ingestion  
- Using patterns (`*.json`)  
- Creating managed and external Delta tables  
- Validating ingestion with `DESCRIBE HISTORY`  

---

# 2. Create a Volume and Input Folder

```sql
CREATE VOLUME IF NOT EXISTS workspace.default.copy_demo;
```

```python
dbutils.fs.mkdirs("/Volumes/workspace/default/copy_demo/input")
```

---

# 3. Create Sample JSON Files

```python
dbutils.fs.put(
    "/Volumes/workspace/default/copy_demo/input/batch1.json",
    """{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob"}"""
)
```

---

# 4. Create the Target Delta Table (Managed)

```sql
CREATE TABLE IF NOT EXISTS workspace.default.copy_into_demo (
  id BIGINT,
  name STRING
);
```

---

# 5. COPY INTO (Basic)

```sql
COPY INTO workspace.default.copy_into_demo
FROM '/Volumes/workspace/default/copy_demo/input'
FILEFORMAT = JSON;
```

---

# 6. Validate

```sql
SELECT * FROM workspace.default.copy_into_demo;
```

---

# 7. COPY INTO is Incremental

Add more data:

```python
dbutils.fs.put(
    "/Volumes/workspace/default/copy_demo/input/batch2.json",
    """{"id": 3, "name": "Charlie"}"""
)
```

Run COPY INTO again:

```sql
COPY INTO workspace.default.copy_into_demo
FROM '/Volumes/workspace/default/copy_demo/input'
FILEFORMAT = JSON;
```

Check results:

```sql
SELECT * FROM workspace.default.copy_into_demo;
```

---

# 8. View Ingestion History

```sql
DESCRIBE HISTORY workspace.default.copy_into_demo;
```

---

# 🇲🇽 VERSIÓN EN ESPAÑOL

# 1. Objetivo

Practicar ingesta batch usando **COPY INTO**, incluyendo:

- Cargar archivos desde Volumes  
- Ingesta incremental  
- Uso de patrones (`*.json`)  
- Crear tablas Delta administradas y externas  
- Validar ingesta con `DESCRIBE HISTORY`  

---

# 2. Crear Volume y Carpeta de Entrada

```sql
CREATE VOLUME IF NOT EXISTS workspace.default.copy_demo;
```

```python
dbutils.fs.mkdirs("/Volumes/workspace/default/copy_demo/input")
```

---

# 3. Crear Archivos JSON de Ejemplo

```python
dbutils.fs.put(
    "/Volumes/workspace/default/copy_demo/input/batch1.json",
    """{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob"}"""
)
```

---

# 4. Crear la Tabla Delta (Managed)

```sql
CREATE TABLE IF NOT EXISTS workspace.default.copy_into_demo (
  id BIGINT,
  name STRING
);
```

---

# 5. COPY INTO (Básico)

```sql
COPY INTO workspace.default.copy_into_demo
FROM '/Volumes/workspace/default/copy_demo/input'
FILEFORMAT = JSON;
```

---

# 6. Validar

```sql
SELECT * FROM workspace.default.copy_into_demo;
```

---

# 7. COPY INTO es Incremental

Agregar más datos:

```python
dbutils.fs.put(
    "/Volumes/workspace/default/copy_demo/input/batch2.json",
    """{"id": 3, "name": "Charlie"}"""
)
```

Ejecutar COPY INTO otra vez:

```sql
COPY INTO workspace.default.copy_into_demo
FROM '/Volumes/workspace/default/copy_demo/input'
FILEFORMAT = JSON;
```

Validar:

```sql
SELECT * FROM workspace.default.copy_into_demo;
```

---

# 8. Ver Historial de Ingesta

```sql
DESCRIBE HISTORY workspace.default.copy_into_demo;
```

---

# 🧊 Iceberg Table Creation — Reference Notebook  
## (Not executable in Free Edition)

---

# 1. Create Catalog with External Location

```sql
CREATE CATALOG IF NOT EXISTS analytics
MANAGED LOCATION 's3://my-bucket/analytics/';
```

---

# 2. Create Schema

```sql
CREATE SCHEMA IF NOT EXISTS analytics.raw;
```

---

# 3. Create Iceberg Table

```sql
CREATE TABLE analytics.raw.events (
  event_id STRING,
  ts TIMESTAMP,
  payload STRING
)
USING ICEBERG;
```

---

# 4. Insert Data

```sql
INSERT INTO analytics.raw.events VALUES
("e1", now(), "hello"),
("e2", now(), "world");
```

---

# 5. Read Iceberg Table

```sql
SELECT * FROM analytics.raw.events;
```

---

# 6. Time Travel (Iceberg)

```sql
SELECT * FROM analytics.raw.events VERSION AS OF 0;
```

---

# 7. COPY INTO → Iceberg

```sql
COPY INTO analytics.raw.events
FROM 's3://my-bucket/events/'
FILEFORMAT = JSON;
```

---

# 8. Table Metadata

```sql
DESCRIBE DETAIL analytics.raw.events;
```

---

---

# 🧊 **Spark DataFrame → Iceberg Table (Notebook Ready)**  

```python
# ============================================================
# 1. Create a Spark DataFrame
# ============================================================

from pyspark.sql import Row
from pyspark.sql import functions as F

data = [
    Row(event_id="e100", ts="2024-01-01T10:00:00Z", value=10),
    Row(event_id="e101", ts="2024-01-01T11:00:00Z", value=20),
    Row(event_id="e102", ts="2024-01-01T12:00:00Z", value=30)
]

df = spark.createDataFrame(data).withColumn("ts", F.to_timestamp("ts"))

df.show()
```

---

```sql
-- ============================================================
-- 2. Create an Iceberg table (Unity Catalog required)
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics.raw.iceberg_events (
  event_id STRING,
  ts TIMESTAMP,
  value INT
)
USING ICEBERG;
```

---

```python
# ============================================================
# 3. Write DataFrame into Iceberg table
# ============================================================

(
    df.write
      .format("iceberg")     # Required for Iceberg tables
      .mode("append")        # append / overwrite / overwriteDynamic
      .saveAsTable("analytics.raw.iceberg_events")
)
```

---

```sql
-- ============================================================
-- 4. Validate the data
-- ============================================================

SELECT * FROM analytics.raw.iceberg_events;
```

---

```sql
-- ============================================================
-- 5. Time Travel (Iceberg)
-- ============================================================

SELECT * FROM analytics.raw.iceberg_events VERSION AS OF 0;
```

---

```sql
-- ============================================================
-- 6. Table metadata
-- ============================================================

DESCRIBE DETAIL analytics.raw.iceberg_events;
```

---

# 🇲🇽 **Versión en Español (explicación rápida)**

### ✔ 1. Creas un DataFrame  
Con datos de ejemplo o reales.

### ✔ 2. Creas la tabla Iceberg  
Debe ser en un catálogo UC que soporte Iceberg.

### ✔ 3. Insertas datos con:  
```python
df.write.format("iceberg").mode("append").saveAsTable("catalog.schema.table")
```

### ✔ 4. Validación  
`SELECT * FROM tabla`

### ✔ 5. Time Travel  
Iceberg soporta versiones igual que Delta.

---
