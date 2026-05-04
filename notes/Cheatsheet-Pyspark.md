
---

# **PySpark Commands Cheatsheet**
A compact but comprehensive reference for the most commonly used PySpark operations in Data Engineering workflows.

---

## **1. SparkSession**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("example") \
    .getOrCreate()
```

---

## **2. Creating DataFrames**
### From Python objects
```python
df = spark.createDataFrame(
    [(1, "Alice"), (2, "Bob")],
    ["id", "name"]
)
```

### From CSV / JSON / Parquet
```python
df = spark.read.csv("/path/file.csv", header=True, inferSchema=True)
df = spark.read.json("/path/file.json")
df = spark.read.parquet("/path/file.parquet")
```

---

## **3. DataFrame Actions**
```python
df.show()          # Display rows
df.head(5)         # First N rows
df.collect()       # Bring all rows to driver
df.count()         # Count rows
df.describe().show()
```

---

## **4. DataFrame Transformations**
### Selecting & Renaming
```python
df.select("col1", "col2")
df.selectExpr("col1 as new_name", "col2 * 2 as doubled")
```

### Filtering
```python
df.filter(df.age > 30)
df.filter("age > 30 AND country = 'MX'")
```

### Adding Columns
```python
from pyspark.sql.functions import col, lit

df.withColumn("age_plus_1", col("age") + 1)
df.withColumn("country", lit("MX"))
```

### Dropping Columns
```python
df.drop("col1", "col2")
```

---

## **5. Aggregations**
```python
from pyspark.sql.functions import avg, sum, count

df.groupBy("country").agg(
    count("*").alias("total"),
    avg("age").alias("avg_age")
)
```

---

## **6. Joins**
```python
df.join(df2, on="id", how="inner")
df.join(df2, df.id == df2.user_id, "left")
df.join(df2, ["id", "date"], "outer")
```

Join types:
- `inner`
- `left`
- `right`
- `outer`
- `left_semi`
- `left_anti`
- `cross`

---

## **7. Window Functions**
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank

w = Window.partitionBy("country").orderBy("age")

df.withColumn("rn", row_number().over(w))
df.withColumn("rk", rank().over(w))
```

---

## **8. Handling Nulls**
```python
df.na.fill({"age": 0, "name": "unknown"})
df.na.drop(subset=["age"])
df.na.replace([""], ["unknown"])
```

---

## **9. Working with Dates & Timestamps**
```python
from pyspark.sql.functions import to_date, current_timestamp, datediff

df.withColumn("date", to_date("string_date", "yyyy-MM-dd"))
df.withColumn("ts", current_timestamp())
df.withColumn("days_diff", datediff("end_date", "start_date"))
```

---

## **10. Reading & Writing Data**
### Parquet
```python
df.write.mode("overwrite").parquet("/path/output")
df = spark.read.parquet("/path/output")
```

### Delta Lake
```python
df.write.format("delta").save("/path/delta")
df = spark.read.format("delta").load("/path/delta")
```

### CSV
```python
df.write.csv("/path/csv", header=True)
```

---

## **11. Schema Handling**
### Print schema
```python
df.printSchema()
```

### Define schema manually
```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True)
])

df = spark.read.schema(schema).json("/path/file.json")
```

---

## **12. Explode & Array Operations**
```python
from pyspark.sql.functions import explode, split

df.withColumn("word", explode(split(col("text"), " ")))
```

---

## **13. UDFs**
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

def add_one(x):
    return x + 1

add_one_udf = udf(add_one, IntegerType())

df.withColumn("new_col", add_one_udf("old_col"))
```

---

## **14. Using `applyInPandas`**
```python
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf(df.schema)
def transform(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf["value"] = pdf["value"] * 2
    return pdf

df_transformed = df.groupby("id").applyInPandas(transform, schema=df.schema)
```

---

## **15. Caching & Persistence**
```python
df.cache()
df.persist()
df.unpersist()
```

---

## **16. Repartitioning**
```python
df.repartition(10)
df.repartition("country")
df.coalesce(1)
```

---

## **17. Ordering**
```python
df.orderBy("age")
df.orderBy(col("age").desc())
```

---

## **18. Writing SQL with Spark**
```python
df.createOrReplaceTempView("people")

spark.sql("""
SELECT country, COUNT(*) AS total
FROM people
GROUP BY country
""")
```

---

## **19. Broadcast Joins**
```python
from pyspark.sql.functions import broadcast

df.join(broadcast(df_small), "id")
```

---

## **20. Handling Corrupt Records**
```python
df = spark.read \
    .option("badRecordsPath", "/tmp/bad") \
    .json("/path/data")
```

---

