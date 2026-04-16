# ⚡ Opciones del atributo `trigger` en Structured Streaming  
## (Databricks: Free Edition vs Pro/Enterprise)

# 🇪🇸 Español

El atributo `trigger` define **cuándo** y **con qué frecuencia** Spark procesa los micro‑batches de un stream.

---

# 🟦 1. Tipos de `trigger` disponibles

## ✔ 1) `trigger(processingTime="10 seconds")`

Ejecuta un micro‑batch **cada intervalo fijo**.

**Ejemplo:**

```python
.trigger(processingTime="10 seconds")
```

**Características:**

- Streaming continuo real  
- Procesa datos cada N segundos  
- Mantiene el stream vivo indefinidamente  

**Disponibilidad:**

- ❌ **NO disponible en Databricks Free Edition**  
- ✔ **Disponible en Databricks Pro/Enterprise**

---

## ✔ 2) `trigger(once=True)`

Procesa **un solo micro‑batch** y termina.

**Ejemplo:**

```python
.trigger(once=True)
```

**Características:**

- Procesa todo lo disponible en un batch  
- Se detiene al terminar  
- Ideal para cargas incrementales tipo batch  

**Disponibilidad:**

- ✔ Disponible en **todas** las ediciones de Databricks  
  (incluyendo Free Edition)

---

## ✔ 3) `trigger(availableNow=True)`

Procesa **todos los micro‑batches necesarios** hasta vaciar la cola de datos, y luego termina.

**Ejemplo:**

```python
.trigger(availableNow=True)
```

**Características:**

- Simula streaming continuo  
- Procesa en múltiples micro‑batches  
- Se detiene cuando ya no hay más datos  
- Es el modo recomendado en Free Edition  

**Disponibilidad:**

- ✔ Disponible en **todas** las ediciones  
- Es el **reemplazo oficial** de streaming continuo en Free Edition

---

# 🟥 2. Comparación por edición de Databricks

| Trigger | Free Edition | Pro / Enterprise |
|---------|--------------|------------------|
| `processingTime` | ❌ No soportado | ✔ Sí |
| `once` | ✔ Sí | ✔ Sí |
| `availableNow` | ✔ Sí | ✔ Sí |

---

# 🧠 3. ¿Por qué Free Edition no soporta `processingTime`?

Porque Free Edition usa un **cluster serverless limitado**, sin soporte para:

- jobs de larga duración  
- streams infinitos  
- triggers continuos  

Por eso aparece el error:

```
INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED
```

---

# 🟩 4. Reglas prácticas

- Si estás en **Free Edition** → usa **`availableNow`**  
- Si necesitas streaming continuo real → necesitas **Pro/Enterprise**  
- Si quieres un pipeline incremental tipo batch → usa **`once`**

---

# 🇺🇸 English Version

# ⚡ `trigger` Options in Structured Streaming  
## (Databricks: Free Edition vs Pro/Enterprise)

The `trigger` attribute defines **when** and **how often** Spark processes micro‑batches in a stream.

---

# 🟦 1. Available `trigger` types

## ✔ 1) `trigger(processingTime="10 seconds")`

Runs a micro‑batch **at a fixed interval**.

**Example:**

```python
.trigger(processingTime="10 seconds")
```

**Characteristics:**

- True continuous streaming  
- Executes every N seconds  
- Keeps the stream alive indefinitely  

**Availability:**

- ❌ **NOT supported in Databricks Free Edition**  
- ✔ Supported in **Databricks Pro/Enterprise**

---

## ✔ 2) `trigger(once=True)`

Runs **one single micro‑batch** and stops.

**Example:**

```python
.trigger(once=True)
```

**Characteristics:**

- Processes all available data once  
- Stops immediately  
- Ideal for incremental batch‑style pipelines  

**Availability:**

- ✔ Supported in **all** Databricks editions  
  (including Free Edition)

---

## ✔ 3) `trigger(availableNow=True)`

Runs **as many micro‑batches as needed** until all data is consumed, then stops.

**Example:**

```python
.trigger(availableNow=True)
```

**Characteristics:**

- Simulates continuous streaming  
- Processes multiple micro‑batches  
- Stops when no more data is available  
- Recommended for Free Edition  

**Availability:**

- ✔ Supported in **all** editions  
- Official replacement for continuous streaming in Free Edition

---

# 🟥 2. Edition Comparison

| Trigger | Free Edition | Pro / Enterprise |
|---------|--------------|------------------|
| `processingTime` | ❌ Not supported | ✔ Supported |
| `once` | ✔ Supported | ✔ Supported |
| `availableNow` | ✔ Supported | ✔ Supported |

---

# 🧠 3. Why Free Edition does not support `processingTime`

Free Edition uses a **limited serverless cluster** that does not support:

- long‑running jobs  
- infinite streaming  
- continuous triggers  

Hence the error:

```
INFINITE_STREAMING_TRIGGER_NOT_SUPPORTED
```

---

# 🟩 4. Practical rules

- If you're on **Free Edition** → use **`availableNow`**  
- If you need true continuous streaming → use **Pro/Enterprise**  
- For incremental batch pipelines → use **`once`**

---

