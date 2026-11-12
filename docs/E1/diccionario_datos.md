# Diccionario de datos — E1

**Proyecto:** Trusted Data Lab  
**Etapa:** E1 — Diagnóstico y preparación de datos  
**Fuentes:** INEGI y Banco de México

## 1. Objetivo

Documentar los campos de las fuentes de datos utilizadas en el proyecto, identificando sus nombres originales, nombres canónicos propuestos, tipos de datos, unidades, frecuencias y observaciones relevantes para su posterior procesamiento.

## 2. Fuente INEGI

- **Identificador:** 910402
- **Origen:** API de indicadores INEGI BIE-BISE
- **Formato:** JSON
- **Registros históricos:** 182
- **Periodo:** agosto de 2011 a septiembre de 2026
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

**Observaciones:** Los valores de `OBS_VALUE` se reciben como cadenas numéricas. `OBS_EXCEPTION` contiene valores nulos. Los campos canónicos son propuestas para la etapa de estandarización y no implican modificar los archivos originales.

## 3. Fuente Banco de México

- **Identificador:** SF43783
- **Indicador:** TIIE a 28 días
- **Origen:** API SIE de Banco de México
- **Formato:** JSON
- **Registros históricos:** 7,955
- **Periodo:** marzo de 1995 a noviembre de 2026
- **Frecuencia observada:** fechas diarias
- **Unidad:** porcentaje anual
- **Cobertura:** México

### Diccionario de campos

| Campo original | Campo canónico propuesto | Descripción | Tipo esperado | Unidad |
|---|---|---|---|---|
| fecha | fecha | Fecha correspondiente a la observación | Fecha | No aplica |
| dato | valor | Tasa TIIE a 28 días | Decimal / valor no disponible | Porcentaje anual |

**Observaciones:** El campo `dato` contiene valores numéricos representados como texto y marcadores `N/E`. Estos marcadores deberán identificarse durante el diagnóstico de calidad de datos.

## 4. Consideraciones de calidad

Los archivos originales de la capa Bronce permanecerán sin modificaciones.

Los tipos documentados corresponden a los tipos esperados después de la conversión; en los archivos originales varios campos están representados como texto.

Los valores faltantes, duplicados y formatos inválidos serán evaluados en la actividad T03 antes de definir cualquier tratamiento.

## 5. Evidencias

- `data/reportes/inventario_bronce.csv`
- `data/bronce/inegi/2026-11-08/910402_historico.json`
- `data/bronce/banxico/2026-11-08/SF43783_historico.json`

## 6. Pendientes

- Confirmar el nombre oficial del indicador INEGI 910402.
- Confirmar la descripción de la unidad 302.
- Verificar los códigos de estado y excepción de INEGI.
- Validar los nombres canónicos antes de utilizarlos en la capa Plata.