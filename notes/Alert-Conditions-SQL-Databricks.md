
---

# 🇬🇧 **Databricks Query Alert Conditions**  
## How to Configure Alerts for SQL Queries in Databricks

Databricks allows you to create **SQL Alerts** that automatically notify you when a query result meets a specific condition. These alerts are commonly used for:

- Data quality monitoring  
- SLA/SLO enforcement  
- Pipeline anomaly detection  
- Threshold-based business rules  
- Detecting missing or late data  

Alerts can be triggered from **SQL Warehouses**, **Dashboards**, or **Saved Queries**.

---

## **1. Where Alerts Can Be Created**
You can create alerts from:

### **A. SQL Editor (Saved Query)**
1. Write a SQL query  
2. Click **Save**  
3. Click **Create Alert**  
4. Define the condition and notification channel  

### **B. Dashboards**
1. Add a visualization  
2. Click the three‑dot menu  
3. Select **Create Alert**  

### **C. Lakehouse Monitoring (Advanced)**
Monitors automatically generate alerts based on:
- Freshness  
- Volume  
- Schema changes  
- Data quality rules  

---

## **2. How Alert Conditions Work**
Alert conditions evaluate the **first row** of the query result.

Your SQL query **must return a numeric or boolean value**, for example:

```sql
SELECT COUNT(*) AS total_errors
FROM logs
WHERE status = 'ERROR'
```

Then you define a condition such as:

- `total_errors > 0`
- `total_errors >= 100`
- `total_errors = 0`
- `total_errors IS NULL`

---

## **3. Supported Condition Types**
Databricks supports:

| Condition Type | Example |
|----------------|---------|
| Greater than | `value > 10` |
| Less than | `value < 5` |
| Equal to | `value = 0` |
| Not equal | `value != 1` |
| Is null | `value IS NULL` |
| Is not null | `value IS NOT NULL` |

---

## **4. Notification Channels**
Alerts can notify via:

- **Email**
- **Webhook** (Slack, Teams, Discord, custom API)
- **Job trigger** (run a workflow)
- **Dashboard alert tiles**
- **Lakehouse Monitoring notifications**

### Example webhook payload:
```json
{
  "alert_id": 123,
  "alert_name": "High Error Count",
  "query_result": 57,
  "condition": "value > 10",
  "triggered_at": "2026-04-30T13:00:00Z"
}
```

---

## **5. Example: Creating an Alert from a Query**
### SQL Query
```sql
SELECT
  COUNT(*) AS failed_records
FROM bronze_events
WHERE status = 'FAILED'
```

### Alert Condition
```
failed_records > 0
```

### Notification
- Email: `data-team@example.com`  
- Webhook: Slack channel  

---

## **6. Example: Data Freshness Alert**
### SQL Query
```sql
SELECT
  MAX(event_time) AS last_event
FROM bronze_events
```

### Condition
```
last_event < now() - INTERVAL 1 HOUR
```

This triggers when data is **older than 1 hour**.

---

## **7. Example: Missing Data Alert**
```sql
SELECT
  CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END AS missing_data
FROM silver_sales
WHERE sale_date = current_date()
```

Condition:
```
missing_data = 1
```

---

## **8. Scheduling Alerts**
Alerts can run:

- Every 1 minute  
- Every 5 minutes  
- Every 1 hour  
- Daily  
- Custom intervals  

They run using a **SQL Warehouse**, so the warehouse must be running or set to auto‑start.

---

## **9. Best Practices**
- Always return **one row, one column**  
- Use **aliases** for clarity  
- Avoid expensive queries for frequent alerts  
- Use **Delta optimizations** (Z‑Order, stats) for performance  
- Store alert queries in a **shared folder** for team visibility  

---

# 🇪🇸 **Condiciones de Alerta en Consultas SQL de Databricks**  
## Cómo Configurar Alertas al Ejecutar Queries en Databricks

Databricks permite crear **Alertas SQL** que se disparan automáticamente cuando el resultado de una consulta cumple una condición específica. Se usan para:

- Monitoreo de calidad de datos  
- Cumplimiento de SLAs  
- Detección de anomalías  
- Reglas de negocio basadas en umbrales  
- Detección de datos faltantes o retrasados  

---

## **1. Dónde se Pueden Crear Alertas**
Puedes crear alertas desde:

### **A. SQL Editor (Saved Query)**
1. Escribe tu query  
2. Guarda la consulta  
3. Selecciona **Create Alert**  
4. Define la condición y el canal de notificación  

### **B. Dashboards**
1. Agrega una visualización  
2. Abre el menú de tres puntos  
3. Selecciona **Create Alert**  

### **C. Lakehouse Monitoring (Avanzado)**
Los monitores generan alertas basadas en:
- Frescura  
- Volumen  
- Cambios de esquema  
- Reglas de calidad de datos  

---

## **2. Cómo Funcionan las Condiciones**
Las condiciones evalúan **la primera fila** del resultado.

Tu query debe regresar un valor **numérico o booleano**, por ejemplo:

```sql
SELECT COUNT(*) AS total_errors
FROM logs
WHERE status = 'ERROR'
```

Luego defines una condición como:

- `total_errors > 0`
- `total_errors >= 100`
- `total_errors = 0`
- `total_errors IS NULL`

---

## **3. Tipos de Condiciones Soportadas**
| Tipo | Ejemplo |
|------|---------|
| Mayor que | `value > 10` |
| Menor que | `value < 5` |
| Igual | `value = 0` |
| Diferente | `value != 1` |
| Es nulo | `value IS NULL` |
| No es nulo | `value IS NOT NULL` |

---

## **4. Canales de Notificación**
Las alertas pueden notificar vía:

- **Correo**
- **Webhook** (Slack, Teams, Discord, API)
- **Ejecución de un Job**
- **Alert tiles en dashboards**
- **Lakehouse Monitoring**

### Ejemplo de payload:
```json
{
  "alert_id": 123,
  "alert_name": "High Error Count",
  "query_result": 57,
  "condition": "value > 10",
  "triggered_at": "2026-04-30T13:00:00Z"
}
```

---

## **5. Ejemplo: Crear una Alerta desde un Query**
### Query SQL
```sql
SELECT
  COUNT(*) AS failed_records
FROM bronze_events
WHERE status = 'FAILED'
```

### Condición
```
failed_records > 0
```

### Notificación
- Email: `data-team@example.com`  
- Webhook: Slack  

---

## **6. Ejemplo: Alerta de Frescura**
```sql
SELECT
  MAX(event_time) AS last_event
FROM bronze_events
```

Condición:
```
last_event < now() - INTERVAL 1 HOUR
```

---

## **7. Ejemplo: Alerta de Datos Faltantes**
```sql
SELECT
  CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END AS missing_data
FROM silver_sales
WHERE sale_date = current_date()
```

Condición:
```
missing_data = 1
```

---

## **8. Programación de Alertas**
Las alertas pueden ejecutarse:

- Cada 1 minuto  
- Cada 5 minutos  
- Cada hora  
- Diario  
- Intervalos personalizados  

Requieren un **SQL Warehouse** activo.

---

## **9. Mejores Prácticas**
- Regresa **una fila, una columna**  
- Usa **aliases** descriptivos  
- Evita queries costosos si la alerta corre frecuentemente  
- Optimiza tablas Delta  
- Guarda las alertas en carpetas compartidas  

---
