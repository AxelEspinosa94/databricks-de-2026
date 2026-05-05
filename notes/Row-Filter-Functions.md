
---

# row-filter-functions-databricks.md

# 🇬🇧 Row Filter Functions in Databricks  

---

# 1. What Are Row Filter Functions?

Row filters in Databricks (Unity Catalog) allow you to **restrict which rows a user can see** based on a SQL function that returns a boolean expression.

They are attached to:

- Tables  
- Views  
- Materialized views  

A row filter acts like a **transparent WHERE clause** that Databricks automatically applies for every query, depending on the user’s identity.

---

# 2. Creating a Row Filter Function

A row filter is a **SQL function** that returns `TRUE` for rows the user is allowed to see.

Example:

```sql
CREATE FUNCTION security.filter_sales_region(region STRING)
RETURN region = current_user();
```

Or using identity metadata:

```sql
CREATE FUNCTION security.filter_by_department(dept STRING)
RETURN dept = current_user_metadata().department;
```

---

# 3. Attaching a Row Filter to a Table

```sql
ALTER TABLE sales
SET ROW FILTER security.filter_sales_region ON (region);
```

Meaning:

- The function receives the column `region`
- Only rows where the function returns TRUE are visible

---

# 4. Removing a Row Filter

```sql
ALTER TABLE sales
DROP ROW FILTER;
```

---

# 5. How Row Filters Work Internally

Databricks rewrites queries automatically:

```sql
SELECT * FROM sales;
```

Becomes:

```sql
SELECT * FROM sales
WHERE security.filter_sales_region(region);
```

Users **cannot bypass** this filter unless they have `BYPASS ROW FILTER` privilege.

---

# 6. Column‑Level Operations Allowed After a Row Filter

Once a row filter is applied, **all column operations are allowed**, but only on the **filtered subset** of rows.

You *can*:

### ✔️ Select columns
```sql
SELECT customer_id, amount FROM sales;
```

### ✔️ Apply expressions
```sql
SELECT amount * 1.16 AS amount_taxed FROM sales;
```

### ✔️ Aggregations
```sql
SELECT SUM(amount) FROM sales;
```

### ✔️ Window functions
```sql
SELECT
  customer_id,
  SUM(amount) OVER (PARTITION BY customer_id)
FROM sales;
```

### ✔️ Joins
```sql
SELECT *
FROM sales s
JOIN customers c ON s.customer_id = c.id;
```

### ✔️ Updates / Deletes (if user has privileges)
```sql
UPDATE sales SET amount = amount * 1.1;
```

### ✔️ Insert into other tables
```sql
INSERT INTO gold_sales SELECT * FROM sales;
```

---

# 7. Column‑Level Operations That Are *Not* Allowed to Break the Filter

Users **cannot**:

### ❌ Access filtered-out rows  
Row filters are enforced at query time.

### ❌ Disable or bypass the filter  
Unless they have:

```sql
GRANT BYPASS ROW FILTER ON TABLE sales TO user axel;
```

### ❌ Use functions that reveal filtered values  
Example: `approx_count_distinct()` still respects the filter.

### ❌ Use `DESCRIBE HISTORY` to infer hidden rows  
Row filters apply to history queries too.

---

# 8. Example: Full Row Filter Workflow

## Step 1 — Create the function

```sql
CREATE FUNCTION security.filter_by_country(country STRING)
RETURN country = current_user_metadata().country;
```

## Step 2 — Attach it to a table

```sql
ALTER TABLE silver_customers
SET ROW FILTER security.filter_by_country ON (country);
```

## Step 3 — Query the table

```sql
SELECT customer_id, email FROM silver_customers;
```

User sees only rows where:

```
country = current_user_metadata().country
```

## Step 4 — Apply column operations

```sql
SELECT
  sha2(email, 256) AS email_hash,
  upper(name) AS name_upper,
  age + 1 AS age_next_year
FROM silver_customers;
```

All valid — but only on filtered rows.

---

# 9. Best Practices

### ✔️ Keep row filter functions simple  
Avoid heavy logic.

### ✔️ Use identity metadata  
Examples:

- `current_user()`
- `current_user_metadata().department`
- `current_user_metadata().country`

### ✔️ Combine with column masking  
Row filters hide rows; masking hides values.

### ✔️ Test with multiple users  
Row filters behave differently per identity.

---

# 🇪🇸 Row Filter Functions en Databricks  
*Guía bilingüe con ejemplos SQL y comportamiento a nivel columna*

---

# 1. ¿Qué son las Row Filter Functions?

Son funciones SQL que determinan **qué filas puede ver un usuario**.  
Actúan como un `WHERE` automático aplicado por Unity Catalog.

---

# 2. Crear una Row Filter Function

```sql
CREATE FUNCTION seguridad.filtro_region(region STRING)
RETURN region = current_user();
```

---

# 3. Asociar un Row Filter a una tabla

```sql
ALTER TABLE ventas
SET ROW FILTER seguridad.filtro_region ON (region);
```

---

# 4. Eliminar el filtro

```sql
ALTER TABLE ventas
DROP ROW FILTER;
```

---

# 5. Cómo funcionan internamente

Databricks reescribe:

```sql
SELECT * FROM ventas;
```

Como:

```sql
SELECT * FROM ventas
WHERE seguridad.filtro_region(region);
```

---

# 6. Operaciones permitidas a nivel columna

Después de aplicar un row filter, puedes:

- Seleccionar columnas  
- Aplicar expresiones  
- Agregar  
- Usar window functions  
- Hacer joins  
- Actualizar o borrar (si tienes permisos)  
- Insertar en otras tablas  

Ejemplo:

```sql
SELECT
  sha2(email, 256) AS email_hash,
  upper(nombre),
  edad + 1
FROM ventas;
```

---

# 7. Operaciones NO permitidas

- Ver filas filtradas  
- Bypassear el filtro  
- Usar funciones para inferir datos ocultos  
- Acceder a historial sin restricciones  

---

# 8. Ejemplo completo

(Equivalente al inglés.)

---

# 9. Mejores prácticas

(Equivalentes al inglés.)

---
