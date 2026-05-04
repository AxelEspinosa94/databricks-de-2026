
---

# 📄 **Federated Querying vs Delta Sharing — Bilingual Guide**  

---

# ------------------------------------------------------------
# 🇺🇸 **ENGLISH VERSION**
# ------------------------------------------------------------

# **Federated Querying vs Delta Sharing in Databricks**

This document explains the difference between:

- **Foreign Connections + Foreign Catalogs** (federated querying)  
- **Delta Sharing** (governed data sharing)

And why a **foreign connection to Amazon Redshift** is the correct approach when Databricks needs to **query external data in place** without replication.

---

# **1. Federated Querying with Foreign Connections**

Federated querying allows Databricks to **query external databases directly**, without copying or replicating data.

Supported systems include:

- Amazon Redshift  
- PostgreSQL  
- MySQL  
- SQL Server  
- Snowflake (preview)  
- Other JDBC-compatible warehouses  

### ✔ Key Benefits

- **No data movement**  
- **No replication or ETL**  
- **Live queries against the external system**  
- **Full Unity Catalog governance**  
- **Audit logging for all access**  
- **Cross-cloud compatibility**  
- **Ability to JOIN external data with Delta Lake tables**

### ✔ How it works

1. Create a **foreign connection** (credentials + URL).  
2. Create a **foreign catalog** that mirrors schemas/tables from the external system.  
3. Query the external tables as if they were native UC tables.

### ✔ Example

```sql
CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host 'redshift.amazonaws.com',
    port '5439',
    user 'my_user',
    password 'my_password',
    database 'sales'
  );

CREATE FOREIGN CATALOG redshift_catalog
  USING CONNECTION redshift_conn;
```

Querying:

```sql
SELECT *
FROM redshift_catalog.public.customers c
JOIN main.analytics.orders o
  ON c.id = o.customer_id;
```

To avoid hardcoded credentials it is recommended the use of Databricks Secrets or summon the credentials as environment variables. To do the first, the process is:

1. Store the secrets
```bash
databricks secrets put --scope redshift --key user
databricks secrets put --scope redshift --key password
```

2. We use them in SQL:
```sql
CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host 'redshift.amazonaws.com',
    port '5439',
    user secret('redshift', 'user'),
    password secret('redshift', 'password'),
    database 'sales'
  );
```

Or we can  use SQL variables to call them
```sql
SET redshift_user = secret('redshift', 'user');
SET redshift_pass = secret('redshift', 'password');

CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host 'redshift.amazonaws.com',
    port '5439',
    user '${redshift_user}',
    password '${redshift_pass}',
    database 'sales'
  );
```

To use environment variables it is recommended to upload a .venv in a Databricks dedicated Volume. In general env variables can be read with the following code:

```python
import os
from dotenv import load_dotenv

load_dotenv("/Volumes/proyecto/config/.env")

host = os.getenv("REDSHIFT_HOST")
user = os.getenv("REDSHIFT_USER")
password = os.getenv("REDSHIFT_PASSWORD")
```

Then substitute them in the query

```sql
CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host '${host}',
    port '5439',
    user '${user}',
    password '${password}',
    database 'sales'
  );
```

Finally we can use Lakehouse UI Federation, going to **Catalog -> External Data -> Connections -> Add Connection**. And in SQl coding:
```sql
CREATE FOREIGN CATALOG redshift_catalog
  USING CONNECTION redshift_conn;
```


---

# **2. Delta Sharing**

Delta Sharing is an **open protocol** for sharing **Delta Lake tables** securely and without copying data.

### ✔ Best for:

- Sharing **Delta tables** across organizations  
- Cross-cloud sharing  
- Tokenless Databricks-to-Databricks sharing  
- UC-governed access to Delta data  

### ❌ Not suitable for:

- Querying external warehouses (e.g., Redshift, Snowflake, BigQuery)  
- Federated querying  
- Joining external data with Lakehouse data in real time  

Delta Sharing requires the **provider** to expose **Delta tables**.  
Amazon Redshift **cannot** act as a Delta Sharing provider.

---

# **3. When Federated Querying Is the Correct Approach?**

When Databricks needs to:

- Run analytical queries  
- Join Lakehouse data with Redshift data  
- Avoid replication  
- Maintain UC governance  
- Maintain audit logging  
- Avoid data movement  

The correct solution is:

# ⭐ **Foreign Connection + Foreign Catalog**

Because:

- Redshift cannot publish Delta Shares  
- Delta Sharing cannot expose Redshift tables  
- Federated querying allows live access  
- UC governs permissions and auditing  
- No ETL or replication is required  

---

# **4. Federated Querying Flow**

```mermaid
flowchart LR
    A[Databricks Workspace] --> B[Foreign Connection]
    B --> C[Foreign Catalog]
    C --> D[(Amazon Redshift)]
    A --> E[Delta Lake Tables]
    E --> F[JOIN Queries]
    D --> F
```

---

# **5. When to Use Each Approach**

| Requirement | Use Foreign Catalog | Use Delta Sharing |
|------------|---------------------|-------------------|
| Query external DB in place | ✔ Yes | ❌ No |
| Join external data with Delta Lake | ✔ Yes | ❌ No |
| No data replication | ✔ Yes | ✔ Yes |
| UC governance & audit | ✔ Yes | ✔ Yes |
| External system is Redshift | ✔ Yes | ❌ No |
| External system provides Delta tables | ❌ No | ✔ Yes |
| Cross-cloud sharing of Delta | ❌ No | ✔ Yes |

---

# **6. Summary**

- **Federated querying** enables Databricks to query Redshift directly.  
- **Delta Sharing** only works with Delta Lake tables.  
- Redshift cannot publish Delta Shares.  
- Therefore, the correct approach is:  
  **Foreign Connection + Foreign Catalog**.

---

# ------------------------------------------------------------
# 🇲🇽 **VERSIÓN EN ESPAÑOL**
# ------------------------------------------------------------

# **Consultas Federadas vs Delta Sharing en Databricks**

Este documento explica la diferencia entre:

- **Foreign Connections + Foreign Catalogs** (consultas federadas)  
- **Delta Sharing** (compartición gobernada de datos)

Y por qué una **conexión federada a Amazon Redshift** es la solución correcta cuando Databricks necesita **consultar datos externos sin replicarlos**.

---

# **1. Consultas Federadas con Foreign Connections**

Las consultas federadas permiten que Databricks **consulte bases externas directamente**, sin mover ni copiar datos.

Sistemas soportados:

- Amazon Redshift  
- PostgreSQL  
- MySQL  
- SQL Server  
- Snowflake (preview)  
- Cualquier warehouse compatible con JDBC  

### ✔ Beneficios clave

- **Sin movimiento de datos**  
- **Sin replicación ni ETL**  
- **Consultas en vivo contra el sistema externo**  
- **Gobernanza completa con Unity Catalog**  
- **Auditoría de accesos**  
- **Compatibilidad entre nubes**  
- **Permite JOIN con tablas Delta Lake**

### ✔ Cómo funciona

1. Crear una **foreign connection** (credenciales + URL).  
2. Crear un **foreign catalog** que refleja los esquemas/tablas del sistema externo.  
3. Consultar las tablas externas como si fueran nativas de UC.

### ✔ Ejemplo

```sql
CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host 'redshift.amazonaws.com',
    port '5439',
    user 'my_user',
    password 'my_password',
    database 'sales'
  );

CREATE FOREIGN CATALOG redshift_catalog
  USING CONNECTION redshift_conn;
```

Consulta:

```sql
SELECT *
FROM redshift_catalog.public.customers c
JOIN main.analytics.orders o
  ON c.id = o.customer_id;
```

Para evitar poner credenciales de forma explícita, se recomienda el uso de Databricks Secrets o llamar las credenciales como variables de entorno. Para hacer lo primero, el proceso es:

1. Almacenar los secretos
```bash
databricks secrets put --scope redshift --key user
databricks secrets put --scope redshift --key password
```

2. Usarlos en SQL:
```sql
CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host 'redshift.amazonaws.com',
    port '5439',
    user secret('redshift', 'user'),
    password secret('redshift', 'password'),
    database 'sales'
  );
```

O podemos usar variables SQL, donde la sintáxis sería
```sql
SET redshift_user = secret('redshift', 'user');
SET redshift_pass = secret('redshift', 'password');

CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host 'redshift.amazonaws.com',
    port '5439',
    user '${redshift_user}',
    password '${redshift_pass}',
    database 'sales'
  );
```

Para el uso de variables de entorno se recomienda cargar un archivo .venv en un volumen dedicado de Databricks. En general las variables de entorno se pueden leer con el siguiente código:

```python
import os
from dotenv import load_dotenv

load_dotenv("/Volumes/proyecto/config/.env")

host = os.getenv("REDSHIFT_HOST")
user = os.getenv("REDSHIFT_USER")
password = os.getenv("REDSHIFT_PASSWORD")
```

Y luego sustituirlos en el query

```sql
CREATE FOREIGN CONNECTION redshift_conn
  TYPE redshift
  OPTIONS (
    host '${host}',
    port '5439',
    user '${user}',
    password '${password}',
    database 'sales'
  );
```

Finalmente, podemos usar el Lakehouse UI Federation, yendo a **Catalog -> External Data -> Connections -> Add Connection**. Y en SQL haríamos:

```sql
CREATE FOREIGN CATALOG redshift_catalog
  USING CONNECTION redshift_conn;
```

---

# **2. Delta Sharing**

Delta Sharing es un **protocolo abierto** para compartir **tablas Delta Lake** de forma segura y sin copiar datos.

### ✔ Ideal para:

- Compartir **tablas Delta** entre organizaciones  
- Compartir entre nubes  
- Compartición sin tokens (Databricks-to-Databricks)  
- Gobernanza UC sobre datos Delta  

### ❌ No sirve para:

- Consultar warehouses externos (Redshift, Snowflake, BigQuery)  
- Consultas federadas  
- Hacer JOIN en tiempo real con datos externos  

Delta Sharing requiere que el **proveedor** exponga **tablas Delta**.  
Amazon Redshift **no puede** actuar como proveedor de Delta Sharing.

---

# **3. Por qué la Conexión Federada es la Solución Correcta**

Cuando Databricks necesita:

- Ejecutar consultas analíticas  
- Unir datos del Lakehouse con datos de Redshift  
- Evitar replicación  
- Mantener gobernanza UC  
- Mantener auditoría  
- Evitar movimiento de datos  

La solución correcta es:

# ⭐ **Foreign Connection + Foreign Catalog**

Porque:

- Redshift no puede publicar Delta Shares  
- Delta Sharing no expone tablas de Redshift  
- Las consultas federadas permiten acceso en vivo  
- UC gobierna permisos y auditoría  
- No se requiere ETL ni replicación  

---

# **4. Diagrama Mermaid — Flujo de Consultas Federadas**

```mermaid
flowchart LR
    A[Databricks Workspace] --> B[Foreign Connection]
    B --> C[Foreign Catalog]
    C --> D[(Amazon Redshift)]
    A --> E[Tablas Delta Lake]
    E --> F[Consultas JOIN]
    D --> F
```

---

# **5. Cuándo usar cada enfoque**

| Necesidad | Foreign Catalog | Delta Sharing |
|-----------|-----------------|---------------|
| Consultar DB externa en vivo | ✔ Sí | ❌ No |
| Hacer JOIN con Delta Lake | ✔ Sí | ❌ No |
| Sin replicación | ✔ Sí | ✔ Sí |
| Gobernanza UC | ✔ Sí | ✔ Sí |
| Sistema externo es Redshift | ✔ Sí | ❌ No |
| Sistema externo expone Delta | ❌ No | ✔ Sí |
| Compartición cross-cloud de Delta | ❌ No | ✔ Sí |

---

# **6. Resumen en Español**

- **Consultas federadas** permiten consultar Redshift directamente.  
- **Delta Sharing** solo funciona con tablas Delta.  
- Redshift no puede publicar Delta Shares.  
- Por lo tanto, la solución correcta es:  
  **Foreign Connection + Foreign Catalog**.

---

