
---

## 🇬🇧 **Job Notifications in Databricks**  
### How to Trigger Alerts When a Job Fails or Runs Successfully

Databricks provides **four main mechanisms** to generate notifications when a Job runs, succeeds, or fails. Each mechanism serves different use cases, from simple UI‑based alerts to fully automated webhook integrations.

---

## 1. **Job Email Notifications (UI & API)**  
The simplest and most common method.

### What you can notify:
- On **success**
- On **failure**
- On **start**
- On **cancellation**

### How to configure (UI):
1. Go to **Workflows → Jobs**  
2. Select your job  
3. Open the **Notifications** section  
4. Add emails under:
   - *On success*
   - *On failure*
   - *On start*
   - *On cancellation*

### How to configure (API):
```json
{
  "name": "example-job",
  "email_notifications": {
    "on_start": ["ops-team@example.com"],
    "on_success": ["data-team@example.com"],
    "on_failure": ["alerts@example.com"]
  },
  "tasks": [
    {
      "task_key": "main",
      "notebook_task": { "notebook_path": "/Repos/example" }
    }
  ]
}
```

---

## 2. **Webhook Notifications (Slack, Teams, Discord, Custom APIs)**  
Webhooks allow Databricks to send JSON payloads to external systems.

### How to configure (UI):
1. Go to **Workflows → Jobs**  
2. Open **Notifications**  
3. Add a **Webhook**  
4. Paste your Slack/Teams/custom endpoint URL  

### Example payload Databricks sends:
```json
{
  "job_id": 12345,
  "run_id": 67890,
  "state": {
    "life_cycle_state": "TERMINATED",
    "result_state": "FAILED"
  },
  "timestamp": 1714500000
}
```

### Example Slack webhook receiver (Python):
```python
import requests

def send_slack_alert(message):
    url = "<YOUR_SLACK_WEBHOOK>"
    payload = {"text": message}
    requests.post(url, json=payload)
```

---

## 3. **Task-Level Alerts Using `dbutils.notebook.exit()`**  
You can force a job to fail or return a custom message.

### Example:
```python
# inside a notebook task
if error_condition:
    dbutils.notebook.exit("ERROR: Invalid data detected")
```

Databricks will:
- Mark the task as **FAILED**
- Trigger **failure notifications**
- Include the exit message in the Job Run output

---

## 4. **Custom Notification Logic Inside the Job (Python / SQL)**  
Useful when you want **conditional alerts**, not just success/failure.

### Example: Send email only if a metric exceeds a threshold
```python
import smtplib

if metric > 0.9:
    send_email("Alert: Drift detected")
```

### Example: Send Teams/Slack message manually
```python
import requests

webhook = "<TEAMS_WEBHOOK>"
requests.post(webhook, json={"text": "Pipeline completed successfully"})
```

---

## 5. **Monitoring via Databricks REST API + External Alerting**  
You can poll job status externally and trigger alerts.

### Example: Check last run status
```bash
curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  https://<workspace-url>/api/2.1/jobs/runs/get?run_id=123
```

You can integrate this with:
- Airflow
- Azure Monitor
- AWS CloudWatch
- Prometheus/Grafana

---

## 6. **Notifications via Databricks Workflows Webhooks (Advanced)**  
Databricks supports **workflow-level webhooks** that trigger on:
- Job start
- Job success
- Job failure
- Task-level events

### Example (API):
```json
{
  "webhook_notifications": {
    "on_failure": [
      {
        "id": "slack-webhook-123"
      }
    ]
  }
}
```

---

# 🇪🇸 **Notificaciones de Jobs en Databricks**  
### Cómo generar alertas cuando un Job falla o se ejecuta correctamente

Databricks ofrece **cuatro mecanismos principales** para crear notificaciones cuando un Job se ejecuta, falla o termina con éxito.

---

## 1. **Notificaciones por correo (UI y API)**  
El método más simple y directo.

### Puedes notificar:
- Al **iniciar**
- Al **terminar con éxito**
- Al **fallar**
- Al **cancelarse**

### Configuración (UI):
1. Ve a **Workflows → Jobs**  
2. Selecciona tu job  
3. Abre la sección **Notifications**  
4. Agrega correos en:
   - *On success*
   - *On failure*
   - *On start*
   - *On cancellation*

### Configuración (API):
```json
{
  "name": "example-job",
  "email_notifications": {
    "on_start": ["ops-team@example.com"],
    "on_success": ["data-team@example.com"],
    "on_failure": ["alerts@example.com"]
  },
  "tasks": [
    {
      "task_key": "main",
      "notebook_task": { "notebook_path": "/Repos/example" }
    }
  ]
}
```

---

## 2. **Notificaciones vía Webhooks (Slack, Teams, Discord, APIs)**  
Permiten enviar mensajes JSON a sistemas externos.

### Configuración (UI):
1. Ve a **Workflows → Jobs**  
2. Abre **Notifications**  
3. Agrega un **Webhook**  
4. Pega la URL de Slack/Teams/API  

### Ejemplo de payload enviado por Databricks:
```json
{
  "job_id": 12345,
  "run_id": 67890,
  "state": {
    "life_cycle_state": "TERMINATED",
    "result_state": "FAILED"
  },
  "timestamp": 1714500000
}
```

### Ejemplo de receptor Slack (Python):
```python
import requests

def send_slack_alert(message):
    url = "<YOUR_SLACK_WEBHOOK>"
    payload = {"text": message}
    requests.post(url, json=payload)
```

---

## 3. **Alertas a nivel de tarea con `dbutils.notebook.exit()`**  
Puedes forzar que un job falle o devuelva un mensaje personalizado.

### Ejemplo:
```python
if error_condition:
    dbutils.notebook.exit("ERROR: Datos inválidos detectados")
```

Databricks:
- Marca la tarea como **FAILED**
- Dispara notificaciones de **fallo**
- Incluye el mensaje en el output del Job

---

## 4. **Lógica personalizada dentro del Job (Python / SQL)**  
Útil cuando quieres alertas **condicionales**, no solo éxito/fallo.

### Ejemplo: Enviar correo si un métrico supera un umbral
```python
if metric > 0.9:
    send_email("Alerta: Drift detectado")
```

### Ejemplo: Enviar mensaje a Teams/Slack manualmente
```python
import requests

webhook = "<TEAMS_WEBHOOK>"
requests.post(webhook, json={"text": "Pipeline completado con éxito"})
```

---

## 5. **Monitoreo vía REST API + Alertas externas**  
Puedes consultar el estado del job desde fuera.

### Ejemplo:
```bash
curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  https://<workspace-url>/api/2.1/jobs/runs/get?run_id=123
```

Integrable con:
- Airflow  
- Azure Monitor  
- AWS CloudWatch  
- Prometheus/Grafana  

---

## 6. **Webhooks de Workflows (Avanzado)**  
Permiten notificaciones a nivel de workflow.

### Ejemplo (API):
```json
{
  "webhook_notifications": {
    "on_failure": [
      {
        "id": "slack-webhook-123"
      }
    ]
  }
}
```

---
