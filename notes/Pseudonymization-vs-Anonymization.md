
---

# 🇬🇧 Pseudonymization vs Anonymization in Databricks & Spark
*A practical guide with Spark cryptographic functions*

---

## 1. Core concepts

### 1.1 Pseudonymization

**Definition:**  
Replacing direct identifiers (email, phone, customer_id) with **consistent tokens or hashes**, where:

- Same input → same output (deterministic)  
- Re-identification is **possible in principle** (e.g., via keys, lookup tables, or brute force)  

**Examples:**

- `sha2(email, 256)`  
- `aes_encrypt(ssn, key)`  
- Tokenization with a mapping table  

**Use cases:**

- Analytics where you still need to **join** on identifiers  
- Data minimization while keeping **linkability** across tables  
- Regulatory contexts where re-identification is allowed under strict controls  

---

### 1.2 Anonymization

**Definition:**  
Transforming data so that **re-identification is not reasonably possible**.

- No keys to reverse  
- No lookup tables  
- Often includes **generalization**, **aggregation**, or **noise**  

**Examples:**

- Dropping identifiers entirely  
- Aggregating to region/month instead of individual  
- Hashing with strong salt that is **not stored**  
- Differential privacy techniques  

**Use cases:**

- Public datasets  
- Sharing with external parties  
- Long-term analytics where identity is irrelevant  

---

## 2. Spark cryptographic functions

All are available in **Spark SQL** and **PySpark** (`pyspark.sql.functions`).

### 2.1 `sha2(expr, bitLength)`

- Deterministic  
- Not reversible  
- Good for **pseudonymization** of identifiers  

**SQL:**

```sql
SELECT
  email,
  sha2(email, 256) AS email_hash
FROM silver_customers;
```

**PySpark:**

```python
from pyspark.sql.functions import sha2, col

df = (
    spark.read.table("silver_customers")
         .withColumn("email_hash", sha2(col("email"), 256))
)
```

---

### 2.2 `md5(expr)`

- Deterministic  
- Not reversible, but **cryptographically weak**  
- Generally **not recommended** for sensitive PII  

**SQL:**

```sql
SELECT md5(email) AS email_md5 FROM silver_customers;
```

---

### 2.3 `aes_encrypt(expr, key)` / `aes_decrypt(expr, key)`

- **Reversible encryption**  
- Requires a **secret key**  
- This is **NOT anonymization**, it’s **pseudonymization** (or just encryption)

**SQL:**

```sql
SELECT
  aes_encrypt(ssn, 'my_secret_key') AS ssn_encrypted
FROM bronze_customers;
```

```sql
SELECT
  cast(aes_decrypt(ssn_encrypted, 'my_secret_key') AS STRING) AS ssn_original
FROM bronze_customers_secure;
```

**PySpark:**

```python
from pyspark.sql.functions import aes_encrypt, aes_decrypt, col

key = "my_secret_key"

df_enc = df.withColumn("ssn_encrypted", aes_encrypt(col("ssn"), key))
df_dec = df_enc.withColumn("ssn_original", aes_decrypt(col("ssn_encrypted"), key).cast("string"))
```

---

### 2.4 Adding a salt (stronger pseudonymization)

**Important:**  
- If you **store** the salt → still pseudonymization  
- If you **don’t store** the salt → closer to anonymization (but then you lose joinability)

**PySpark example:**

```python
from pyspark.sql.functions import sha2, concat_ws, lit, col

SALT = "static_salt_value"  # if stored, still pseudonymization

df = (
    spark.read.table("silver_customers")
         .withColumn(
             "email_hash_salted",
             sha2(concat_ws(":", col("email"), lit(SALT)), 256)
         )
)
```

---

## 3. Pseudonymization patterns in Databricks

### 3.1 Deterministic pseudonymization for joins

```sql
CREATE OR REPLACE TABLE silver_customers_pseudo AS
SELECT
  sha2(email, 256) AS email_hash,
  customer_id,
  country,
  signup_date
FROM silver_customers;
```

You can now join on `email_hash` instead of `email`.

---

### 3.2 Pseudonymization with encryption (reversible under strict control)

```sql
CREATE OR REPLACE TABLE gold_customers_secure AS
SELECT
  aes_encrypt(ssn, 'prod_key_123') AS ssn_encrypted,
  customer_id,
  country
FROM silver_customers;
```

Access to the key controls who can re-identify.

---

## 4. Anonymization patterns in Databricks

### 4.1 Drop identifiers completely

```sql
CREATE OR REPLACE TABLE analytics_customers_anon AS
SELECT
  country,
  age_bucket,
  COUNT(*) AS customers
FROM silver_customers
GROUP BY country, age_bucket;
```

No direct or indirect identifiers remain.

---

### 4.2 Strong hashing with non-recoverable salt

If the salt is **not stored anywhere**, and is random per batch, re-identification becomes practically impossible—but you also lose deterministic joins.

```python
import uuid
from pyspark.sql.functions import sha2, concat_ws, lit, col

batch_salt = str(uuid.uuid4())  # not stored → closer to anonymization

df_anon = (
    spark.read.table("silver_customers")
         .withColumn(
             "email_hash",
             sha2(concat_ws(":", col("email"), lit(batch_salt)), 256)
         )
         .drop("email")  # drop original identifier
)
```

---

## 5. Exam-style summary

**Pseudonymization:**

- Deterministic  
- May be reversible (encryption) or vulnerable to re-identification (hashing of low-entropy values)  
- Examples: `sha2(email, 256)`, `aes_encrypt(ssn, key)`  

**Anonymization:**

- Not reasonably reversible  
- Often removes or aggregates identifiers  
- Examples: dropping identifiers, aggregating, strong salted hashing without storing salt  

**Typical exam correct answer:**

> “Use `sha2(email, 256)` to pseudonymize email addresses in a silver table. It is deterministic and not reversible in practice.”

---

# 🇪🇸 Pseudonimización vs Anonimización en Databricks & Spark
*Guía práctica con funciones criptográficas de Spark*

---

## 1. Conceptos clave

### 1.1 Pseudonimización

Reemplazar identificadores directos por **tokens o hashes determinísticos**.

- Mismo input → mismo output  
- Re-identificación posible en principio (claves, tablas de mapeo, fuerza bruta)  

Ejemplos:

- `sha2(email, 256)`  
- `aes_encrypt(ssn, key)`  

---

### 1.2 Anonimización

Transformar datos de forma que **no sea razonablemente posible** re-identificar a la persona.

- Sin claves  
- Sin tablas de mapeo  
- Generalización, agregación, ruido  

---

## 2. Funciones criptográficas en Spark

(Equivalentes a la sección en inglés: `sha2`, `md5`, `aes_encrypt`, `aes_decrypt`, salting, con los mismos ejemplos SQL y PySpark.)

---

## 3. Patrones de pseudonimización en Databricks

(Equivalentes: hashing determinístico, cifrado reversible bajo control.)

---

## 4. Patrones de anonimización en Databricks

(Equivalentes: eliminación de identificadores, agregación, hashing con salt no recuperable.)

---

## 5. Resumen estilo examen

- **Pseudonimización:** se puede, en teoría, revertir o vincular.  
- **Anonimización:** no se puede revertir razonablemente.  
- `sha2(email, 256)` → típico para pseudonimizar emails en capa silver.  

---
