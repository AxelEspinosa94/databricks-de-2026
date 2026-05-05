
---

# 🇬🇧 **Running Totals with Window Frames in SQL**  
## Understanding `UNBOUNDED PRECEDING`, `CURRENT ROW`, and All Frame Combinations

Window frames define **which rows are included** when a window function (like `SUM`, `AVG`, `COUNT`, etc.) is evaluated.  
Running totals are one of the most common use cases.

This guide explains:

- What a running total is  
- How `UNBOUNDED PRECEDING` + `CURRENT ROW` works  
- All valid frame combinations  
- What each combination computes  
- Practical examples  

---

# **1. Running Total with UNBOUNDED PRECEDING and CURRENT ROW**

### Query
```sql
SUM(amount) OVER (
  PARTITION BY region
  ORDER BY month
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_total
```

### Meaning
- **UNBOUNDED PRECEDING** → start at the first row in the partition  
- **CURRENT ROW** → end at the current row  
- **ROWS** → count physical rows, not value-based ranges  

### Result
A **running total** (cumulative sum):

| Row | amount | running_total |
|-----|--------|----------------|
| 1   | 100    | 100            |
| 2   | 200    | 300            |
| 3   | 50     | 350            |

---

# **2. All Window Frame Combinations**

Window frames follow this structure:

```
ROWS BETWEEN <start> AND <end>
```

Where `<start>` and `<end>` can be:

- `UNBOUNDED PRECEDING`
- `n PRECEDING`
- `CURRENT ROW`
- `n FOLLOWING`
- `UNBOUNDED FOLLOWING`

Below is a complete guide.

---

## **A. UNBOUNDED PRECEDING → CURRENT ROW**  
### Running total (cumulative sum)

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

Includes: all rows from the start → current row.

---

## **B. UNBOUNDED PRECEDING → UNBOUNDED FOLLOWING**  
### Full-partition aggregation (same as GROUP BY)

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

Example:

```sql
SUM(amount) OVER (PARTITION BY region)
```

Same value repeated for all rows.

---

## **C. n PRECEDING → CURRENT ROW**  
### Sliding window (moving window)

```sql
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
```

Includes: current row + previous 3 rows.

Use cases:
- Moving averages  
- Rolling sums  
- Trend detection  

---

## **D. CURRENT ROW → n FOLLOWING**  
### Forward-looking window

```sql
ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING
```

Includes: current row + next 2 rows.

Use cases:
- Forecasting  
- Lead-based calculations  

---

## **E. n PRECEDING → n FOLLOWING**  
### Centered window

```sql
ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
```

Includes: 2 rows before + current + 2 rows after.

Use cases:
- Smoothing  
- Weighted averages  

---

## **F. CURRENT ROW → UNBOUNDED FOLLOWING**  
### Remaining-partition window

```sql
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
```

Includes: current row → last row.

Use cases:
- Reverse running totals  
- Remaining balance calculations  

---

# **3. Practical Examples**

## **Running Total**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

## **Moving 7‑day Sum**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

## **Centered 5‑row Average**
```sql
AVG(amount) OVER (
  ORDER BY timestamp
  ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
)
```

## **Remaining Total**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
)
```

---

# 🇪🇸 **Running Totals con Window Frames en SQL**  
## Entendiendo `UNBOUNDED PRECEDING`, `CURRENT ROW` y todas las combinaciones

Los window frames definen **qué filas se incluyen** cuando una función de ventana se evalúa.  
Los running totals son uno de los casos más comunes.

---

# **1. Running Total con UNBOUNDED PRECEDING y CURRENT ROW**

### Query
```sql
SUM(amount) OVER (
  PARTITION BY region
  ORDER BY month
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_total
```

### Significado
- **UNBOUNDED PRECEDING** → desde la primera fila  
- **CURRENT ROW** → hasta la fila actual  
- **ROWS** → filas físicas  

### Resultado
Un **acumulado progresivo**:

| Fila | amount | running_total |
|------|--------|----------------|
| 1    | 100    | 100            |
| 2    | 200    | 300            |
| 3    | 50     | 350            |

---

# **2. Todas las combinaciones de Window Frames**

Los frames siguen esta estructura:

```
ROWS BETWEEN <inicio> AND <fin>
```

Donde `<inicio>` y `<fin>` pueden ser:

- `UNBOUNDED PRECEDING`
- `n PRECEDING`
- `CURRENT ROW`
- `n FOLLOWING`
- `UNBOUNDED FOLLOWING`

---

## **A. UNBOUNDED PRECEDING → CURRENT ROW**  
### Acumulado (running total)

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

---

## **B. UNBOUNDED PRECEDING → UNBOUNDED FOLLOWING**  
### Agregación completa (como GROUP BY)

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

---

## **C. n PRECEDING → CURRENT ROW**  
### Ventana móvil (sliding window)

```sql
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
```

---

## **D. CURRENT ROW → n FOLLOWING**  
### Ventana hacia adelante

```sql
ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING
```

---

## **E. n PRECEDING → n FOLLOWING**  
### Ventana centrada

```sql
ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
```

---

## **F. CURRENT ROW → UNBOUNDED FOLLOWING**  
### Ventana hasta el final

```sql
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
```

---

# **3. Ejemplos prácticos**

## **Acumulado**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

## **Suma móvil de 7 días**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

## **Promedio centrado de 5 filas**
```sql
AVG(amount) OVER (
  ORDER BY timestamp
  ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
)
```

## **Total restante**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
)
```

---

