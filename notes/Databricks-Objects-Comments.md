
---

# 🇬🇧 COMMENT ON in Databricks SQL  

---

## 1. Overview

Databricks SQL supports the `COMMENT ON` command to document objects in Unity Catalog.  
You can add, update, or remove comments on:

- Catalogs  
- Schemas  
- Tables  
- Columns  
- Providers  
- Shares  
- Recipients  
- Volumes  

---

## 2. COMMENT ON TABLE

### Add or modify a table comment

```sql
COMMENT ON TABLE sales_data IS 'Historical sales data table';
```

### Remove a table comment

```sql
COMMENT ON TABLE sales_data IS NULL;
```


---

## 3. COMMENT ON COLUMN

Column comments **do not** use `COMMENT ON COLUMN`.  
Databricks requires:

```sql
ALTER TABLE table_name
  ALTER COLUMN column_name
  COMMENT 'New comment';
```

### Remove a column comment

```sql
ALTER TABLE table_name
  ALTER COLUMN column_name
  COMMENT NULL;
```

---

## 4. COMMENT ON SCHEMA

```sql
COMMENT ON SCHEMA analytics IS 'Schema for BI and reporting';
```

Remove:

```sql
COMMENT ON SCHEMA analytics IS NULL;
```

---

## 5. COMMENT ON CATALOG

```sql
COMMENT ON CATALOG main IS 'Primary production catalog';
```

Remove:

```sql
COMMENT ON CATALOG main IS NULL;
```

---

## 6. COMMENT ON PROVIDER / SHARE / RECIPIENT / VOLUME

Supported in Unity Catalog

### Provider

```sql
COMMENT ON PROVIDER my_provider IS 'External data provider';
```

### Share

```sql
COMMENT ON SHARE finance_share IS 'Share for finance department';
```

### Recipient

```sql
COMMENT ON RECIPIENT partner_x IS 'External partner recipient';
```

### Volume

```sql
COMMENT ON VOLUME bronze_vol IS 'Raw ingestion volume';
```

---

## 7. Permissions Required

To modify comments in Unity Catalog, you need:

- `MODIFY` privilege on the object  
- Or be the **OWNER**  

---

## 8. Compatibility Notes

- Works in **Databricks SQL** and **Databricks Runtime** (recent versions)  
- Materialized views require **DBR 16.3+**  

---

# 🇪🇸 COMMENT ON en Databricks SQL  

---

## 1. Descripción general

El comando `COMMENT ON` permite documentar objetos en Unity Catalog:

- Catálogos  
- Esquemas  
- Tablas  
- Columnas  
- Proveedores  
- Recursos compartidos (shares)  
- Destinatarios (recipients)  
- Volúmenes  


---

## 2. COMMENT ON TABLE

### Agregar o modificar comentario

```sql
COMMENT ON TABLE sales_data IS 'Tabla con datos de ventas históricas';
```

### Eliminar comentario

```sql
COMMENT ON TABLE sales_data IS NULL;
```

---

## 3. COMMENT ON COLUMN

Databricks **no** usa `COMMENT ON COLUMN`.  
Debe hacerse con `ALTER TABLE`:

```sql
ALTER TABLE tabla
  ALTER COLUMN columna
  COMMENT 'Nuevo comentario';
```

Eliminar:

```sql
ALTER TABLE tabla
  ALTER COLUMN columna
  COMMENT NULL;
```

---

## 4. COMMENT ON SCHEMA

```sql
COMMENT ON SCHEMA analytics IS 'Esquema para BI y reportes';
```

Eliminar:

```sql
COMMENT ON SCHEMA analytics IS NULL;
```

---

## 5. COMMENT ON CATALOG

```sql
COMMENT ON CATALOG main IS 'Catálogo principal de producción';
```

Eliminar:

```sql
COMMENT ON CATALOG main IS NULL;
```

---

## 6. COMMENT ON PROVIDER / SHARE / RECIPIENT / VOLUME

### Provider

```sql
COMMENT ON PROVIDER mi_proveedor IS 'Proveedor externo de datos';
```

### Share

```sql
COMMENT ON SHARE finanzas_share IS 'Recurso compartido para finanzas';
```

### Recipient

```sql
COMMENT ON RECIPIENT socio_x IS 'Destinatario externo';
```

### Volume

```sql
COMMENT ON VOLUME bronze_vol IS 'Volumen de ingesta raw';
```

---

## 7. Permisos requeridos

- Privilegio `MODIFY`  
- O ser el **OWNER** del objeto  

---

## 8. Notas de compatibilidad

- Disponible en Databricks SQL y Databricks Runtime  
- Para vistas materializadas se requiere DBR 16.3+  

---

