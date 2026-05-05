
---

# **Row Filter Functions in Databricks (Unity Catalog)**
A complete reference with basic and advanced examples using identity metadata, comparisons, boolean logic, string/date functions, CASE expressions, arithmetic, and null-handling functions.

---

# 1. Overview

A **Row Filter Function** is a SQL function that returns a boolean expression.  
Databricks automatically applies it to every query on a table or view where the filter is attached.

Example attachment:

```sql
ALTER TABLE sales
SET ROW FILTER security.filter_sales_region ON (region);
```

---

# 2. Basic Row Filter Functions

## 2.1 Filter by user identity

```sql
CREATE FUNCTION security.filter_by_user(owner STRING)
RETURN owner = current_user();
```

Attach:

```sql
ALTER TABLE documents
SET ROW FILTER security.filter_by_user ON (owner);
```

---

## 2.2 Filter by user department (identity metadata)

```sql
CREATE FUNCTION security.filter_by_department(dept STRING)
RETURN dept = current_user_metadata().department;
```

---

## 2.3 Filter by simple comparison

```sql
CREATE FUNCTION security.filter_positive(amount DOUBLE)
RETURN amount > 0;
```

---

## 2.4 Filter by boolean logic

```sql
CREATE FUNCTION security.filter_active_and_paid(status STRING, paid BOOLEAN)
RETURN status = 'ACTIVE' AND paid = TRUE;
```

---

# 3. Intermediate Row Filter Functions

## 3.1 Using string functions

```sql
CREATE FUNCTION security.filter_email_domain(email STRING)
RETURN lower(split(email, '@')[1]) = 'company.com';
```

---

## 3.2 Using date functions

```sql
CREATE FUNCTION security.filter_last_30_days(order_date DATE)
RETURN order_date >= current_date() - INTERVAL 30 DAYS;
```

---

## 3.3 Using arithmetic expressions

```sql
CREATE FUNCTION security.filter_high_value(amount DOUBLE)
RETURN amount * 1.16 > 1000;
```

---

## 3.4 Using COALESCE / NULLIF

```sql
CREATE FUNCTION security.filter_non_empty_region(region STRING)
RETURN coalesce(nullif(region, ''), 'UNKNOWN') != 'UNKNOWN';
```

---

## 3.5 Using CASE expressions

```sql
CREATE FUNCTION security.filter_case_status(status STRING)
RETURN CASE
         WHEN status IN ('ACTIVE', 'PENDING') THEN TRUE
         ELSE FALSE
       END;
```

---

# 4. Advanced Row Filter Functions

## 4.1 Combining identity metadata + business logic

```sql
CREATE FUNCTION security.filter_sales(region STRING, amount DOUBLE)
RETURN region = current_user_metadata().region
       AND amount > 0;
```

---

## 4.2 Multi-column + date + string logic

```sql
CREATE FUNCTION security.filter_complex(
    region STRING,
    order_date DATE,
    category STRING
)
RETURN
    region = current_user_metadata().region
    AND order_date >= current_date() - INTERVAL 90 DAYS
    AND lower(category) NOT LIKE '%restricted%';
```

---

## 4.3 Using OR logic for multi-role access

```sql
CREATE FUNCTION security.filter_role_based(dept STRING)
RETURN
    dept = current_user_metadata().department
    OR is_account_group_member('executives');
```

---

## 4.4 Using nested expressions + arithmetic + null handling

```sql
CREATE FUNCTION security.filter_profit(
    revenue DOUBLE,
    cost DOUBLE,
    region STRING
)
RETURN
    (coalesce(revenue, 0) - coalesce(cost, 0)) > 500
    AND region = current_user_metadata().region;
```

---

## 4.5 Using CASE + identity metadata + date logic

```sql
CREATE FUNCTION security.filter_dynamic(
    region STRING,
    order_date DATE,
    priority STRING
)
RETURN
    CASE
        WHEN priority = 'HIGH'
            THEN region = current_user_metadata().region
        WHEN priority = 'MEDIUM'
            THEN order_date >= current_date() - INTERVAL 60 DAYS
        ELSE FALSE
    END;
```

---

# 5. Attaching Row Filters to Tables

```sql
ALTER TABLE silver_orders
SET ROW FILTER security.filter_complex
ON (region, order_date, category);
```

---

# 6. What You Can Do After a Row Filter Is Applied

Once a row filter is active, **all column-level operations are allowed**, but only on the filtered rows:

- SELECT  
- Expressions  
- Aggregations  
- Window functions  
- Joins  
- Updates / deletes (if permitted)  
- Inserts into other tables  

Example:

```sql
SELECT
  customer_id,
  upper(name) AS name_upper,
  sha2(email, 256) AS email_hash,
  amount * 1.16 AS amount_taxed,
  coalesce(phone, 'N/A') AS phone_clean
FROM silver_orders;
```

All valid — but only on rows allowed by the row filter.

---

# 7. Best Practices

- Keep row filter functions **deterministic**  
- Use **identity metadata** for dynamic security  
- Avoid heavy logic inside filters  
- Combine with **column masking** for full data protection  
- Test with multiple users  

---

# End of Document
```

---
