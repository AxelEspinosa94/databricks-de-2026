
---

# 🇺🇸 **README — Local Fixtures Extractor (API‑Football) → Databricks Pipeline**

This repository contains the **local extractor for national team fixtures** using **API‑Football (API‑Sports)**, optimized for:

- Free plan (100 requests/day)  
- Incremental extraction by groups  
- Daily resume capability  
- Real‑time dashboard  
- Silent rate‑limit handling  
- Incremental saving  
- Integration with Databricks (Bronze → Silver → Gold)

The goal is to obtain **raw JSON fixtures** locally and upload them to a **Databricks Volume** to continue the pipeline.

---

## 📁 Repository Structure

```
/
└── etude-de-cas/                 # Main project folder
    │
    ├── bronze/                   # Bronze tables (Databricks)
    │
    ├── silver/                   # Silver tables (Databricks)
    │
    ├── gold/                     # Gold tables (Databricks)
    │
    ├── checkpoints/              # Auto Loader / streaming checkpoints
    │
    ├── docs/                     # Documentation, diagrams, notes
    │
    ├── input/                    # JSON raw files (landing zone)
    │   ├── fixtures_group_0_20260422_085418.json
    │   ├── fixtures_group_1_20260422_090501.json
    │   ├── fixtures_group_2_20260422_092233.json
    │   ├── fixtures_group_3_20260422_094812.json
    │   ├── fixtures_group_4_20260422_101055.json
    │   ├── fixtures_group_5_20260422_103344.json
    │   ├── fixtures_group_6_20260422_105812.json
    │   ├── fixtures_group_7_20260422_112501.json
    │   ├── fixtures_group_8_20260422_115922.json
    │   ├── fixtures_group_9_20260422_122355.json
    │   ├── fixtures_group_10_20260422_124955.json
    │   ├── fixtures_group_11_20260422_130555.json
    │   └── fixtures_group_12_20260422_130555.json
    │
    ├── libs/                     # Pipeline source code
    │   ├── __pycache__/
    │   └── api_client.py
    │
    ├── .gitignore
    ├── README.md
    └── API-Football-source-to-landing-LOCAL-Ext_API-LIMIT.ipynb
```

---

## 🔑 Requirements

### 1. Python 3.9+
### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. `.env` file (DO NOT commit)

```
API_FOOTBALL_KEY=your_api_key_here
```

---

## 🧠 Extractor Overview

The script `extract_fixtures_final.py`:

- Splits 48 national teams into **12 groups of 4**  
- Extracts fixtures by year (configurable)  
- Respects the **100 requests/day** limit  
- Automatically stops if:
  - The limit is reached  
  - A team ID cannot be retrieved (silent rate limit)  
- Saves progress per group  
- Shows a **real‑time dashboard**  
- Allows resuming the next day without losing progress  

---

## 🗂️ Team Groups (Fixed Order)

```
Mexico, South Korea, South Africa, Czech Republic
Canada, Bosnia and Herzegovina, Qatar, Switzerland
Brazil, Morocco, Haiti, Scotland
USA, Australia, Paraguay, Turkey
Germany, Ecuador, Ivory Coast, Curacao
Netherlands, Japan, Sweden, Tunisia
Belgium, Iran, Egypt, New Zealand
Spain, Uruguay, Saudi Arabia, Cape Verde
France, Senegal, Iraq, Norway
Argentina, Algeria, Austria, Jordan
Portugal, Colombia, Uzbekistan, Congo DR
England, Croatia, Ghana, Panama
```

Names are **normalized** for API‑Football.

---

## 🚀 How to Run the Extractor

From the `extractor/` folder:

```bash
python extract_fixtures_final.py
```

The script:

1. Starts at **Group 1**  
2. Extracts fixtures year by year  
3. Saves one JSON file per group  
4. Stops if:
   - The daily limit is reached  
   - A team ID cannot be retrieved  
5. Prints exactly where to resume the next day  

---

## 📊 Real‑Time Dashboard

Example output:

```
📊 Progress
   Group: 3/12
   Team in group: 2/4 — Paraguay
   Year: 2023
   Requests used: 47/100
   Requests remaining: 53
```

---

## 🛑 Daily Resume

If the extractor stops due to limit or ID failure:

```
🛑 Global stop: could not obtain ID for Turkey.
   Last position: group 4, team 3 (Turkey).
```

Next day:

- You may adjust `START_GROUP` and `START_TEAM`  
- Or simply let the script continue with the next group  

*(If you want, I can add a `progress.json` for automatic resume.)*

---

## 📤 Upload JSONs to Databricks

In Databricks:

1. Go to **Data → Volumes**
2. Open your Volume:

```
/Volumes/workspace/default/api_football_pipeline/input
```

3. Upload the JSON files from `raw_fixtures/`

---

## 🪣 Continue the Pipeline (Bronze → Silver → Gold)

### 1. Notebook 2 — COPY INTO → Bronze  
- Creates Bronze table  
- Incremental ingestion  
- History tracking  

### 2. Notebook 3 — Silver  
- Flatten  
- Normalization  
- Correct data types  

### 3. Notebook 4 — Gold  
- Metrics  
- Aggregations  
- ML‑ready tables  

---

## 🛡️ Best Practices

✔ Do upload:  
- notebooks  
- scripts  
- requirements  
- README  
- api_client.py  

❌ Do NOT upload:  
- `.env`  
- `raw_fixtures/`  

---

## 🧩 Pipeline Diagram

```
[Local Extractor]
      ↓ JSON
[raw_fixtures/]
      ↓ Upload
[Databricks Volume /input]
      ↓ COPY INTO
[Bronze]
      ↓ Transform
[Silver]
      ↓ Aggregate
[Gold]
```

---

## 🏁 Conclusion

This repository implements a hybrid pipeline:

- **Local extraction** (due to API‑Football free plan limits)  
- **Databricks processing** (Bronze → Silver → Gold)  

Robust, reproducible, and scalable.

---

---

# 🇲🇽 **README — Extractor Local de Fixtures (API‑Football) → Pipeline en Databricks**

Este repositorio contiene el **extractor local de fixtures de selecciones nacionales** usando **API‑Football (API‑Sports)**, optimizado para:

- Plan gratuito (100 requests/día)  
- Extracción incremental por grupos  
- Reanudación diaria  
- Dashboard en tiempo real  
- Manejo de rate limits silenciosos  
- Guardado incremental  
- Integración con Databricks (Bronze → Silver → Gold)

El objetivo es obtener los **JSON crudos** localmente y subirlos a un **Volume de Databricks** para continuar el pipeline.

---

## 📁 Estructura del repositorio
```
/
└── etude-de-cas/                 # Main project folder
    │
    ├── bronze/                   # Bronze tables (Databricks)
    │
    ├── silver/                   # Silver tables (Databricks)
    │
    ├── gold/                     # Gold tables (Databricks)
    │
    ├── checkpoints/              # Auto Loader / streaming checkpoints
    │
    ├── docs/                     # Documentation, diagrams, notes
    │
    ├── input/                    # JSON raw files (landing zone)
    │   ├── fixtures_group_0_20260422_085418.json
    │   ├── fixtures_group_1_20260422_090501.json
    │   ├── fixtures_group_2_20260422_092233.json
    │   ├── fixtures_group_3_20260422_094812.json
    │   ├── fixtures_group_4_20260422_101055.json
    │   ├── fixtures_group_5_20260422_103344.json
    │   ├── fixtures_group_6_20260422_105812.json
    │   ├── fixtures_group_7_20260422_112501.json
    │   ├── fixtures_group_8_20260422_115922.json
    │   ├── fixtures_group_9_20260422_122355.json
    │   ├── fixtures_group_10_20260422_124955.json
    │   ├── fixtures_group_11_20260422_130555.json
    │   └── fixtures_group_12_20260422_130555.json
    │
    ├── libs/                     # Pipeline source code
    │   ├── __pycache__/
    │   └── api_client.py
    │
    ├── .gitignore
    ├── README.md
    └── API-Football-source-to-landing-LOCAL-Ext_API-LIMIT.ipynb
```

---

## 🔑 Requisitos

### 1. Python 3.9+
### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Archivo `.env` (NO subir)

```
API_FOOTBALL_KEY=tu_api_key_aqui
```

---

## 🧠 Descripción del extractor

El script `extract_fixtures_final.py`:

- Divide 48 selecciones en **12 grupos de 4**  
- Extrae fixtures por año (configurable)  
- Respeta el límite de **100 requests/día**  
- Se detiene automáticamente si:
  - Se alcanza el límite  
  - No se puede obtener un ID (rate limit silencioso)  
- Guarda progreso por grupo  
- Muestra un **dashboard en tiempo real**  
- Permite reanudar al día siguiente sin perder nada  

---

## 🗂️ Grupos de selecciones (orden fijo)

```
México, Corea del Sur, Sudáfrica, República Checa
Canadá, Bosnia y Herzegovina, Qatar, Suiza
Brasil, Marruecos, Haití, Escocia
Estados Unidos, Australia, Paraguay, Turquía
Alemania, Ecuador, Costa de Marfil, Curazao
Países Bajos, Japón, Suecia, Túnez
Bélgica, Irán, Egipto, Nueva Zelanda
España, Uruguay, Arabia Saudita, Cabo Verde
Francia, Senegal, Irak, Noruega
Argentina, Argelia, Austria, Jordania
Portugal, Colombia, Uzbekistán, República Democrática del Congo
Inglaterra, Croacia, Ghana, Panamá
```

Los nombres ya están **normalizados** para API‑Football.

---

## 🚀 Cómo ejecutar el extractor

Desde la carpeta `extractor/`:

```bash
python extract_fixtures_final.py
```

El script:

1. Inicia en el **Grupo 1**  
2. Extrae fixtures año por año  
3. Guarda un archivo JSON por grupo  
4. Se detiene si:
   - Se alcanza el límite diario  
   - No se puede obtener un ID  
5. Te indica exactamente dónde reanudar mañana  

---

## 📊 Dashboard en tiempo real

Ejemplo:

```
📊 Progreso
   Grupo: 3/12
   Equipo en grupo: 2/4 — Paraguay
   Año: 2023
   Requests usados: 47/100
   Requests restantes: 53
```

---

## 🛑 Reanudación diaria

Si el extractor se detiene:

```
🛑 Stop general: no se pudo obtener ID para Turkey.
   Última posición: grupo 4, equipo 3 (Turkey).
```

Al día siguiente:

- Puedes ajustar `START_GROUP` y `START_TEAM`  
- O dejar que el script continúe con el siguiente grupo  

*(Si quieres, puedo agregar `progress.json` para reanudación automática.)*

---

## 📤 Subir JSONs a Databricks

En Databricks:

1. Ve a **Data → Volumes**
2. Entra a tu Volume:

```
/Volumes/workspace/default/api_football_pipeline/input
```

3. Sube los JSON generados en `raw_fixtures/`

---

## 🪣 Continuar el pipeline (Bronze → Silver → Gold)

### 1. Notebook 2 — COPY INTO → Bronze  
- Crea tabla Bronze  
- Ingesta incremental  
- Historial  

### 2. Notebook 3 — Silver  
- Flatten  
- Normalización  
- Tipos correctos  

### 3. Notebook 4 — Gold  
- Métricas  
- Agregaciones  
- Tablas para ML  

---

## 🛡️ Buenas prácticas

✔ Sube:  
- notebooks  
- scripts  
- requirements  
- README  
- api_client.py  

❌ No subas:  
- `.env`  
- `raw_fixtures/`  

---

## 🧩 Diagrama del flujo

```
[Extractor Local]
      ↓ JSON
[raw_fixtures/]
      ↓ Upload
[Databricks Volume /input]
      ↓ COPY INTO
[Bronze]
      ↓ Transform
[Silver]
      ↓ Aggregate
[Gold]
```

---

## 🏁 Conclusión

Este repositorio implementa un pipeline híbrido:

- **Extracción local** (por límites del plan gratuito)  
- **Procesamiento en Databricks** (Bronze → Silver → Gold)  

Robusto, reproducible y escalable.

---
