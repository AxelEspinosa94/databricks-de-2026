# 📦 DBFS vs Unity Catalog + Volumes

Diferencias prácticas, arquitectura y cuándo usar cada uno

## 🟥 ¿Qué es DBFS?

DBFS (Databricks File System) era un filesystem virtual que Databricks montaba sobre el almacenamiento del cloud.

<b>Características</b>

- Accesible como /dbfs, /mnt, /FileStore.
- Permitía guardar archivos, checkpoints, datasets, etc.
- No tenía gobernanza fina (ACLs, permisos por tabla, lineage).
- No era multi‑workspace ni multi‑tenant.
- No era compatible con Unity Catalog.
- Está depreciado y en Free Edition está deshabilitado.

<b>Uso típico (antes)</b>

- Demos rápidas.
- Notebooks.
- Checkpoints de streaming.
- Archivos temporales.
Hoy ya no es el camino recomendado.

## 🟩 ¿Qué es Unity Catalog + Volumes?

Unity Catalog es el sistema de gobernanza, seguridad y lineage de Databricks.
Los Volumes son el reemplazo moderno de DBFS para almacenar archivos.

<b>Características de Volumes</b>

- Se acceden vía rutas como:
/Volumes/<catalog>/<schema>/<volume>/
- Soportan:
- archivos
- checkpoints
- Auto Loader
- Structured Streaming
- ingestion pipelines
- Tienen permisos granulares (GRANT SELECT, WRITE, etc.).
- Funcionan en todos los clouds y workspaces con UC habilitado.
- Son multi‑workspace y multi‑tenant.
Uso típico
- Pipelines de producción.
- Ingestión con Auto Loader.
- Structured Streaming.
- Almacenamiento de datos crudos.
- Feature stores, modelos, artefactos.
- Cualquier cosa que antes hacías en /mnt o /FileStore.

## 🥊 Comparación directa

| Tema | DBFS | Unity Catalog + Volumes |
|------|------|--------------------------|
| Gobernanza | ❌ No | ✔ Sí (ACLs, lineage, audit) |
| Seguridad | Básica | Enterprise-grade |
| Multi-workspace | ❌ No | ✔ Sí |
| Multi-cloud | ✔ Sí | ✔ Sí |
| Checkpoints de streaming | ✔ Sí | ✔ Sí |
| Auto Loader | ✔ Sí | ✔ Sí |
| Soporte en Free Edition | ❌ No | ✔ Sí |
| Futuro | Deprecado | Estándar recomendado |


## 🎯 ¿Cuál conviene usar hoy?

✔ En Free Edition
- Solo Unity Catalog + Volumes.
- DBFS está completamente deshabilitado.

✔ En producción
- Unity Catalog + Volumes siempre.
- DBFS ya no cumple requisitos de seguridad ni gobernanza.

✔ En clusters legacy (sin UC)
- DBFS todavía funciona, pero Databricks recomienda migrar.

## 🧠 Regla práctica para no equivocarte

Si tu workspace tiene Unity Catalog habilitado (como Free Edition), nunca uses /dbfs, /mnt o /FileStore. Siempre usa /Volumes/<catalog>/<schema>/<volume>/...


## 🚀 Conclusión

Unity Catalog + Volumes es el reemplazo moderno, seguro y soportado de DBFS.
Para Structured Streaming, ingestion y Delta Lake, Volumes es el camino correcto.

# 📦 DBFS vs Unity Catalog + Volumes

Practical differences, architecture, and when to use each one

## 🟥 What is DBFS?

DBFS (Databricks File System) was a virtual filesystem that Databricks mounted on top of cloud storage.

**Characteristics**

- Accessible as /dbfs, /mnt, /FileStore.
- Allowed storing files, checkpoints, datasets, etc.
- Lacked fine‑grained governance (ACLs, table‑level permissions, lineage).
- Not multi‑workspace or multi‑tenant.
- Not compatible with Unity Catalog.
- It is deprecated and disabled in Free Edition.

**Typical usage (before)**

- Quick demos.  
- Notebooks.  
- Streaming checkpoints.  
- Temporary files.  

Today it is no longer the recommended approach.

---

## 🟩 What is Unity Catalog + Volumes?

Unity Catalog is Databricks’ governance, security, and lineage system.  
Volumes are the modern replacement for DBFS when storing files.

**Characteristics of Volumes**

- Accessed through paths like:  
  `/Volumes/<catalog>/<schema>/<volume>/`
- Support:
  - files  
  - checkpoints  
  - Auto Loader  
  - Structured Streaming  
  - ingestion pipelines  
- Provide granular permissions (GRANT SELECT, WRITE, etc.).
- Work across all clouds and UC‑enabled workspaces.
- Are multi‑workspace and multi‑tenant.

**Typical usage**

- Production pipelines.  
- Ingestion with Auto Loader.  
- Structured Streaming.  
- Raw data storage.  
- Feature stores, models, artifacts.  
- Anything you previously stored in /mnt or /FileStore.

---

## 🥊 Direct Comparison

| Topic | DBFS | Unity Catalog + Volumes |
|------|------|--------------------------|
| Governance | ❌ No | ✔ Yes (ACLs, lineage, audit) |
| Security | Basic | Enterprise‑grade |
| Multi‑workspace | ❌ No | ✔ Yes |
| Multi‑cloud | ✔ Yes | ✔ Yes |
| Streaming checkpoints | ✔ Yes | ✔ Yes |
| Auto Loader | ✔ Yes | ✔ Yes |
| Free Edition support | ❌ No | ✔ Yes |
| Future | Deprecated | Recommended standard |

---

## 🎯 Which one should you use today?

✔ **In Free Edition**  
- Only Unity Catalog + Volumes.  
- DBFS is completely disabled.

✔ **In production**  
- Always Unity Catalog + Volumes.  
- DBFS no longer meets governance or security requirements.

✔ **In legacy clusters (without UC)**  
- DBFS still works, but Databricks recommends migrating.

---

## 🧠 Practical rule to avoid mistakes

If your workspace has Unity Catalog enabled (like Free Edition), **never use /dbfs, /mnt, or /FileStore. Always use /Volumes/<catalog>/<schema>/<volume>/...**

---

## 🚀 Conclusion

Unity Catalog + Volumes is the modern, secure, and fully supported replacement for DBFS.  
For Structured Streaming, ingestion, and Delta Lake, **Volumes is the correct path forward**.