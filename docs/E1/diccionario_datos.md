# Diccionario de datos — E1

**Proyecto:** Trusted Data Lab  
**Etapa:** E1 — Diagnóstico y preparación de datos  
**Fuentes:** INEGI y Banco de México  
**Última actualización:** 12 de noviembre de 2026

## 1. Objetivo

Documentar los campos de las fuentes de datos utilizadas en el proyecto, identificando sus nombres originales, nombres canónicos propuestos, tipos de datos, unidades, frecuencias y observaciones relevantes para su posterior procesamiento.

También se registra la información de las capturas históricas y oportunas, con el propósito de mantener la trazabilidad de los datos obtenidos mediante las API de INEGI y Banco de México.

## 2. Fuente INEGI

- **Identificador:** 910402
- **Origen:** API de indicadores INEGI BIE-BISE
- **Formato:** JSON
- **Registros históricos:** 183
- **Periodo:** agosto de 2011 a octubre de 2026
- **Última observación:** 2026-10-01
- **Registros en captura oportuna:** 1
- **Fecha de captura actualizada:** 2026-11-12
- **Frecuencia observada:** mensual
- **Cobertura:** nacional (código 00)
- **Código de unidad:** 302
- **Nombre oficial y unidad:** pendientes de verificación

### Diccionario de campos

| Campo original | Campo canónico propuesto | Descripción | Tipo esperado | Unidad |
|---|---|---|---|---|
| TIME_PERIOD | fecha | Periodo de la observación | Fecha/periodo mensual | No aplica |
| OBS_VALUE | valor | Valor del indicador | Decimal | Pendiente |
| OBS_EXCEPTION | excepcion | Código o información de excepción | Texto / nulo | No aplica |
| OBS_STATUS | estado | Código de estado de la observación | Texto | No aplica |
| OBS_SOURCE | fuente_observacion | Información de procedencia de la observación | Texto | No aplica |
| OBS_NOTE | nota | Nota asociada a la observación | Texto | No aplica |
| COBER_GEO | cobertura_geografica | Código de cobertura geográfica | Texto | No aplica |

### Observaciones

Los valores de `OBS_VALUE` se reciben como cadenas numéricas. El campo `OBS_EXCEPTION` puede contener valores nulos.

Los campos canónicos son propuestas para la etapa de estandarización y no implican modificar los archivos originales.

La captura histórica del 8 de noviembre de 2026 contenía 182 observaciones, mientras que la captura del 12 de noviembre contiene 183, incorporando el periodo de octubre de 2026.

La captura oportuna del 12 de noviembre devolvió una observación correspondiente al periodo 2026-10-01.

## 3. Fuente Banco de México

- **Identificador:** SF43783
- **Indicador:** TIIE a 28 días
- **Origen:** API SIE de Banco de México
- **Formato:** JSON
- **Registros históricos:** 7,958
- **Periodo:** marzo de 1995 a noviembre de 2026
- **Última observación:** 2026-11-12
- **Registros en captura oportuna:** 1
- **Fecha de captura actualizada:** 2026-11-12
- **Frecuencia observada:** fechas diarias
- **Unidad:** porcentaje anual
- **Cobertura:** México

### Diccionario de campos

| Campo original | Campo canónico propuesto | Descripción | Tipo esperado | Unidad |
|---|---|---|---|---|
| fecha | fecha | Fecha correspondiente a la observación | Fecha | No aplica |
| dato | valor | Tasa TIIE a 28 días | Decimal / valor no disponible | Porcentaje anual |

### Observaciones

El campo `dato` contiene valores numéricos representados como texto y marcadores `N/E`, que indican observaciones sin valor numérico disponible.

Durante el diagnóstico T03 de la captura histórica del 8 de noviembre de 2026 se identificaron 200 registros con `N/E`, equivalentes aproximadamente al 2.51% de los 7,955 registros analizados.

Los valores faltantes se distribuyeron de la siguiente manera:

| Año | Registros con N/E |
|---|---:|
| 1995 | 152 |
| 1996 | 48 |
| **Total** | **200** |

Los valores faltantes identificados se concentraron en los primeros dos años de la serie histórica.

Esta concentración temporal requiere investigación adicional y no permite determinar por sí sola si el mecanismo de ausencia corresponde a MCAR, MAR o MNAR.

La captura histórica del 12 de noviembre de 2026 contiene 7,958 registros. El diagnóstico de calidad deberá ejecutarse nuevamente sobre esta versión para verificar los resultados actualizados.

La captura oportuna del 12 de noviembre devolvió una observación correspondiente al 2026-11-12.

## 4. Consideraciones de calidad

Los archivos originales de la capa Bronce permanecerán sin modificaciones.

Los tipos documentados corresponden a los tipos esperados después de la conversión; en los archivos originales varios campos están representados como texto.

Durante el diagnóstico inicial T03 se evaluaron los archivos históricos del 8 de noviembre de 2026.

Los resultados fueron los siguientes:

| Métrica | INEGI | Banxico |
|---|---:|---:|
| Registros analizados | 182 | 7,955 |
| Valores faltantes | 0 | 200 |
| Fechas duplicadas | 0 | 0 |
| Fechas inválidas | 0 | 0 |
| Valores numéricos inválidos adicionales | 0 | 0 |

Estos resultados corresponden exclusivamente a las capturas históricas del 8 de noviembre.

Será necesario actualizar el diagnóstico para incluir las capturas del 12 de noviembre de 2026.

No se reemplazarán los valores `N/E` por cero ni se eliminarán registros de los archivos originales.

## 5. Evidencias

### Inventario de archivos

- `data/reportes/inventario_bronce.csv`

### Capturas históricas anteriores — 8 de noviembre de 2026

- `data/bronce/inegi/2026-11-08/910402_historico.json`
- `data/bronce/banxico/2026-11-08/SF43783_historico.json`

### Capturas históricas actuales — 12 de noviembre de 2026

- `data/bronce/inegi/2026-11-12/910402_historico_130114_649094_60dc15f7.json`
- `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`

### Capturas oportunas actuales — 12 de noviembre de 2026

- `data/bronce/inegi/2026-11-12/910402_oportuno_130303_362253_b16037c9.json`
- `data/bronce/banxico/2026-11-12/SF43783_oportuno_130304_955934_ab308d96.json`

### Diagnóstico de calidad

- `src/diagnostico.py`
- `data/reportes/diagnostico_calidad.csv`

El reporte de diagnóstico disponible corresponde inicialmente a las capturas históricas del 8 de noviembre de 2026.

## 6. Pendientes

- Confirmar el nombre oficial del indicador INEGI 910402.
- Confirmar la descripción de la unidad 302.
- Verificar los códigos de estado y excepción de INEGI.
- Validar los nombres canónicos antes de utilizarlos en la capa Plata.
- Actualizar el diagnóstico T03 utilizando las capturas históricas del 12 de noviembre de 2026.
- Verificar si los valores faltantes de Banxico permanecen concentrados en 1995 y 1996.
- Investigar el mecanismo de ausencia de los valores faltantes durante T04.

## 7. Actualización de capturas

El 12 de noviembre de 2026 se realizaron nuevas capturas históricas y oportunas de INEGI y Banco de México mediante el orquestador del proyecto.

Los comandos utilizados fueron:

**Captura histórica:**

```powershell
python -m extractores.main --historico
```

**Captura oportuna:**

```powershell
python -m extractores.main
```

Ambas ejecuciones finalizaron correctamente y las consultas a las API devolvieron respuestas HTTP 200.

### Comparación de capturas históricas

| Fuente | 8 de noviembre | 12 de noviembre | Diferencia |
|---|---:|---:|---:|
| INEGI | 182 | 183 | +1 |
| Banxico | 7,955 | 7,958 | +3 |

### Resultados de capturas oportunas

| Fuente | Registros | Última observación |
|---|---:|---|
| INEGI | 1 | 2026-10-01 |
| Banxico | 1 | 2026-11-12 |

Las capturas se almacenaron en carpetas organizadas por fuente y fecha. Los nombres de archivo incluyen identificadores únicos para evitar sobrescribir ejecuciones anteriores.

Los archivos originales se conservan para mantener la trazabilidad, reproducibilidad y evidencia de las consultas realizadas.

La actualización de las capturas no modifica automáticamente los resultados del diagnóstico T03, por lo que este deberá ejecutarse nuevamente sobre los archivos actuales.

## 8. Diccionario de datos de la capa Oro

La capa Oro contiene los indicadores mensuales de INEGI y Banco de México preparados para consulta y análisis.

El archivo generado es:

`data/oro/indicadores_mensuales.csv`

La tabla conserva 564 observaciones: 183 de INEGI y 381 de Banxico.

### Estructura de la tabla

| Campo | Tipo esperado | Descripción |
|---|---|---|
| `periodo` | Fecha | Mes al que corresponde la observación |
| `fuente` | Texto | Organismo de procedencia: INEGI o Banxico |
| `serie_id` | Texto | Identificador oficial de la serie |
| `indicador` | Texto | Nombre del indicador económico |
| `valor` | Decimal | Valor mensual de la observación |
| `unidad` | Texto | Unidad de medida correspondiente al indicador |
| `metodo` | Texto | Método utilizado para obtener el valor mensual |
| `cobertura` | Texto | Ámbito geográfico del indicador |

### Granularidad

Cada fila representa una observación mensual de una serie económica.

La combinación de `fuente`, `serie_id` y `periodo` identifica una observación.

Los datos de Banxico se obtienen mediante agregación mensual de sus registros diarios. Los datos de INEGI conservan su frecuencia mensual original.

### Reglas de calidad

Antes de publicar los registros, el pipeline aplica una validación mediante Pandera.

Se comprueban los campos requeridos, los tipos de datos, los periodos válidos, los valores numéricos y la ausencia de duplicados por serie y mes.

Los registros que no cumplen las reglas se envían a Cuarentena cuando sus errores pueden identificarse de manera individual.

### Conservación de las unidades

Los valores de INEGI y Banxico representan indicadores distintos.

Por esta razón, el pipeline conserva cada serie por separado y no suma ni promedia valores entre fuentes.

La unidad y el nombre oficial del indicador INEGI deben verificarse contra la documentación de la fuente, tal como se indica en los apartados anteriores de este diccionario.

## 9. Conclusión

Se documentaron los campos originales de INEGI y Banco de México, junto con sus tipos de datos esperados, frecuencias, unidades y nombres canónicos utilizados durante el procesamiento.

Las capturas históricas del 12 de noviembre de 2026 permitieron actualizar la cobertura temporal de ambas fuentes y ejecutar nuevamente el diagnóstico de calidad.

El procesamiento identificó 200 valores faltantes en Banxico y ninguno en INEGI. Se adoptó una política conservadora que evita imputar automáticamente los valores no publicados y mantiene intactos los archivos originales de Bronce.

Mediante la reducción mensual y la integración de las fuentes se obtuvieron 564 observaciones válidas, publicadas en Plata y Oro.

También se documentaron las ocho columnas de la capa Oro, su granularidad mensual y las reglas generales de calidad utilizadas para validar los registros.

Queda pendiente verificar el nombre oficial y la unidad del indicador INEGI, así como completar las investigaciones adicionales sobre los mecanismos de ausencia.