
---

# **PySpark Lakeflow Declarative Pipeline Decorators — Complete Cheatsheet**

This cheatsheet covers **all decorators used in Databricks Lakeflow Spark Declarative Pipelines**, including:

- Table & model declaration  
- Expectations (drop, fail, quarantine, warn)  
- Schema & column constraints  
- Dependencies  
- Incremental processing  
- Materialization options  

Each section includes **syntax + examples**.

---

# **1. Table & Model Declaration Decorators**

## **`@dp.table`**
Declares a table in a declarative pipeline.

```python
@dp.table
def customers():
    return spark.read.table("bronze_customers")
```

---

## **`@dp.model`**
Declares a model (logical transformation) that may or may not materialize.

```python
@dp.model
def enriched_customers(customers):
    return customers.withColumn("age_bucket", ...)
```

---

# **2. Expectation Decorators (Data Quality Rules)**

These are the MOST important for the exam.

Databricks supports **four expectation behaviors**:

| Decorator | Behavior |
|----------|----------|
| `@dp.expect` | Check rule, but do NOT drop or fail |
| `@dp.expect_or_drop` | Drop rows that fail the rule |
| `@dp.expect_or_fail` | Fail the pipeline if rule fails |
| `@dp.expect_or_quarantine` | Move failing rows to a quarantine table |
| `@dp.expect_or_warn` | Log a warning but continue |

---

## **2.1 `@dp.expect`**
Evaluates a rule but **does nothing** (no drop, no fail).  
Useful for monitoring.

```python
@dp.expect("valid_age", "age BETWEEN 0 AND 120")
```

---

## **2.2 `@dp.expect_or_drop`**
Rows failing the rule are **silently dropped**.

```python
@dp.expect_or_drop("valid_age", "customer_age BETWEEN 0 AND 150")
```

---

## **2.3 `@dp.expect_or_fail`**
If ANY row fails the rule → **pipeline fails immediately**.

```python
@dp.expect_or_fail("valid_id", "customer_id IS NOT NULL")
```

This is the correct decorator for your exam question.

---

## **2.4 `@dp.expect_or_quarantine`**
Moves failing rows to a **quarantine table**.

```python
@dp.expect_or_quarantine("valid_email", "email LIKE '%@%'")
```

Quarantine table name is auto‑generated unless specified.

---

## **2.5 `@dp.expect_or_warn`**
Logs a warning but continues.

```python
@dp.expect_or_warn("valid_zip", "zip_code RLIKE '^[0-9]{5}$'")
```

---

# **3. Schema & Column Decorators**

## **`@dp.schema`**
Defines the schema of the output table.

```python
from pyspark.sql.types import *

@dp.schema(
    StructType([
        StructField("id", IntegerType()),
        StructField("name", StringType()),
        StructField("age", IntegerType())
    ])
)
@dp.table
def customers():
    return spark.read.csv("/path")
```

---

## **`@dp.column`**
Define column-level metadata or constraints.

```python
@dp.column("customer_id", nullable=False)
@dp.column("email", comment="Customer email address")
```

---

# **4. Dependency Decorators**

## **`@dp.dependency`**
Declare that a table depends on another.

```python
@dp.dependency(customers)
@dp.table
def gold_customers():
    return customers.filter("status = 'active'")
```

---

# **5. Incremental Processing Decorators**

## **`@dp.incremental`**
Marks a table as incrementally processed.

```python
@dp.incremental("event_time")
@dp.table
def events():
    return spark.read.table("bronze_events")
```

---

## **`@dp.append_only`**
Indicates the table only receives new rows.

```python
@dp.append_only
@dp.table
def logs():
    return spark.read.table("raw_logs")
```

---

# **6. Materialization Decorators**

## **`@dp.materialize`**
Controls how the table is written.

```python
@dp.materialize("delta")
@dp.table
def sales():
    return spark.read.table("bronze_sales")
```

---

## **`@dp.refresh`**
Controls refresh behavior.

```python
@dp.refresh(mode="full")
```

---

# **7. Full Example Combining Decorators**

This example mirrors your exam question:

```python
from pyspark import pipelines as dp

@dp.table
@dp.expect_or_drop("valid_age", "customer_age BETWEEN 0 AND 150")
@dp.expect_or_fail("valid_id", "customer_id IS NOT NULL")
def cleaned_customers():
    return spark.read.table("bronze_customers")
```

### Behavior:
- Invalid age → **dropped silently**  
- NULL customer_id → **pipeline fails immediately**  

This matches the exam’s correct answer (**Option B**).

---

# **8. Quick Reference Table**

| Decorator | Purpose |
|----------|---------|
| `@dp.table` | Declares a table |
| `@dp.model` | Declares a logical model |
| `@dp.expect` | Check only |
| `@dp.expect_or_drop` | Drop failing rows |
| `@dp.expect_or_fail` | Fail pipeline |
| `@dp.expect_or_quarantine` | Move failing rows to quarantine |
| `@dp.expect_or_warn` | Log warning |
| `@dp.schema` | Define schema |
| `@dp.column` | Column metadata |
| `@dp.dependency` | Declare dependency |
| `@dp.incremental` | Incremental processing |
| `@dp.append_only` | Append-only table |
| `@dp.materialize` | Control materialization |
| `@dp.refresh` | Refresh behavior |

---

