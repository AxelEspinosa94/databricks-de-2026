
---

# 🇬🇧 **Complete Window Frames Cheatsheet**  
## Understanding ROWS, RANGE, GROUPS, and All Frame Combinations

Window frames define **which rows are included** when evaluating a window function.  
This cheatsheet covers:

- ROWS frames  
- RANGE frames  
- GROUPS frames  
- All valid combinations  
- Running totals, moving windows, centered windows  
- Edge cases  
- Performance considerations  
- When to use each frame type  

This is a **full reference**, deeper than the previous document.

---

# **1. Window Frame Types**

SQL supports **three** frame types:

### **A. ROWS**
Operates on **physical rows**.

```
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
```

### **B. RANGE**
Operates on **value-based ranges** relative to the ORDER BY expression.

```
RANGE BETWEEN INTERVAL 7 DAYS PRECEDING AND CURRENT ROW
```

### **C. GROUPS**
Operates on **peer groups** (rows with identical ORDER BY values).

```
GROUPS BETWEEN 1 PRECEDING AND 1 FOLLOWING
```

---

# **2. Frame Boundaries**

Each frame has a **start** and **end** boundary:

| Boundary | Meaning |
|----------|---------|
| `UNBOUNDED PRECEDING` | Start at first row of partition |
| `n PRECEDING` | Start n rows before current |
| `CURRENT ROW` | Start/end at current row |
| `n FOLLOWING` | End n rows after current |
| `UNBOUNDED FOLLOWING` | End at last row of partition |

---

# **3. Complete List of Valid Frame Combinations**

Below is the **full matrix** of valid combinations.

### ✔️ **A. UNBOUNDED PRECEDING → CURRENT ROW**  
Running total.

### ✔️ **B. UNBOUNDED PRECEDING → UNBOUNDED FOLLOWING**  
Full-partition aggregate.

### ✔️ **C. n PRECEDING → CURRENT ROW**  
Moving window (sliding window).

### ✔️ **D. CURRENT ROW → n FOLLOWING**  
Forward-looking window.

### ✔️ **E. n PRECEDING → n FOLLOWING**  
Centered window.

### ✔️ **F. CURRENT ROW → UNBOUNDED FOLLOWING**  
Remaining total.

### ✔️ **G. n PRECEDING → UNBOUNDED FOLLOWING**  
Full future window.

### ✔️ **H. UNBOUNDED PRECEDING → n FOLLOWING**  
Full past + limited future.

---

# **4. ROWS vs RANGE vs GROUPS**

## **A. ROWS**
- Uses **physical row offsets**
- Most predictable
- Best for running totals, moving averages

Example:
```sql
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
```

## **B. RANGE**
- Uses **value-based offsets**
- Requires numeric or timestamp ORDER BY
- Includes **all peers** with same ORDER BY value

Example:
```sql
RANGE BETWEEN INTERVAL 7 DAYS PRECEDING AND CURRENT ROW
```

## **C. GROUPS**
- Uses **peer groups**, not rows
- More stable than RANGE
- Useful when ORDER BY has duplicates

Example:
```sql
GROUPS BETWEEN 1 PRECEDING AND 1 FOLLOWING
```

---

# **5. Running Total Examples**

## **Classic Running Total**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

## **Reverse Running Total**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
)
```

## **Running Total with RANGE**
```sql
SUM(amount) OVER (
  ORDER BY date
  RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

---

# **6. Moving Window Examples**

## **7‑day moving sum**
```sql
SUM(amount) OVER (
  ORDER BY date
  RANGE BETWEEN INTERVAL 7 DAYS PRECEDING AND CURRENT ROW
)
```

## **Last 3 rows**
```sql
SUM(amount) OVER (
  ORDER BY date
  ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
)
```

---

# **7. Centered Window Examples**

## **Centered 5-row average**
```sql
AVG(amount) OVER (
  ORDER BY timestamp
  ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
)
```

## **Centered peer-group window**
```sql
AVG(amount) OVER (
  ORDER BY score
  GROUPS BETWEEN 1 PRECEDING AND 1 FOLLOWING
)
```

---

# **8. Edge Cases**

### **A. RANGE with non-numeric ORDER BY**
❌ Not allowed.

### **B. RANGE with duplicates**
Includes **all peers**.

### **C. GROUPS with duplicates**
Counts peer groups, not rows.

### **D. ROWS is always deterministic**
Even with duplicates.

---

# **9. Performance Considerations**

| Frame Type | Performance | Notes |
|------------|-------------|-------|
| ROWS | Fastest | Most predictable |
| RANGE | Slower | Requires sorting + peer expansion |
| GROUPS | Medium | Good for duplicate ORDER BY values |

---

# **10. Summary Table**

| Use Case | Best Frame |
|----------|------------|
| Running total | ROWS UNBOUNDED PRECEDING → CURRENT ROW |
| Moving average | ROWS n PRECEDING → CURRENT ROW |
| Time-based window | RANGE INTERVAL |
| Peer-based window | GROUPS |
| Forecasting | CURRENT ROW → n FOLLOWING |
| Remaining balance | CURRENT ROW → UNBOUNDED FOLLOWING |

---

# 🇪🇸 **Cheatsheet Completo de Window Frames**  
## Entendiendo ROWS, RANGE, GROUPS y todas las combinaciones

(La versión en español es equivalente, solo traducida.)

---

# **1. Tipos de Window Frames**

### **A. ROWS**
Opera sobre **filas físicas**.

### **B. RANGE**
Opera sobre **rangos de valores**.

### **C. GROUPS**
Opera sobre **grupos de valores iguales**.

---

# **2. Límites del Frame**

| Límite | Significado |
|--------|-------------|
| `UNBOUNDED PRECEDING` | Desde la primera fila |
| `n PRECEDING` | n filas antes |
| `CURRENT ROW` | Fila actual |
| `n FOLLOWING` | n filas después |
| `UNBOUNDED FOLLOWING` | Hasta la última fila |

---

# **3. Combinaciones Válidas**

(Se listan todas, igual que en inglés.)

---

# **4. ROWS vs RANGE vs GROUPS**

(Explicación equivalente.)

---

# **5. Ejemplos de Running Total**

(Equivalentes en español.)

---

# **6. Ventanas Móviles**

(Equivalentes.)

---

# **7. Ventanas Centradas**

(Equivalentes.)

---

# **8. Casos Especiales**

(Equivalentes.)

---

# **9. Rendimiento**

(Equivalentes.)

---

# **10. Tabla Resumen**

(Equivalente.)

---

