# T11 — Puerta de Calidad con Pandera

## 1. Objetivo

Implementar una Puerta de Calidad para validar la estructura y consistencia de los datos integrados de INEGI y Banxico antes de autorizar su uso en las siguientes etapas del proyecto Trusted Data Lab.

## 2. Herramientas utilizadas

- Python 3.14.3.
- Pandera 0.35.0.
- pandas.
- pytest.

## 3. Datos de entrada

Archivo: `data/plata/integracion_mensual.csv`

El conjunto contiene 564 registros y 9 columnas:

- `fuente`
- `serie_id`
- `indicador`
- `periodo`
- `valor`
- `unidad`
- `frecuencia`
- `metodo`
- `cobertura`

Los registros provienen de la integración realizada en T10: 183 observaciones de INEGI y 381 observaciones mensuales de Banxico.

## 4. Reglas de calidad implementadas

Se definió un esquema de validación con Pandera en `src/calidad.py` que comprueba:

1. Presencia de las nueve columnas requeridas.
2. Ausencia de columnas adicionales no contempladas.
3. Fuente perteneciente a INEGI o Banxico.
4. Identificadores y metadatos obligatorios no vacíos.
5. Periodos mensuales con formato `AAAA-MM` y meses entre 01 y 12.
6. Valores numéricos finitos y no nulos.
7. Frecuencia mensual.
8. Ausencia de duplicados en la combinación `fuente`, `serie_id` y `periodo`.

La validación utiliza `lazy=True` para recopilar distintos incumplimientos.

## 5. Implementación

Se desarrollaron los siguientes archivos:

- `src/calidad.py`: definición del esquema y función de validación.
- `src/ejecutar_calidad.py`: ejecución de la Puerta de Calidad y generación del reporte.
- `tests/test_calidad.py`: pruebas automatizadas.

La función de validación trabaja sobre una copia del DataFrame, sin alterar los datos originales.

## 6. Resultados

La ejecución de la Puerta de Calidad produjo los siguientes resultados:

| Métrica | Resultado |
|---|---:|
| Registros evaluados | 564 |
| Registros aprobados | 564 |
| Casos de fallo reportados | 0 |
| Estado | APROBADO |

Reporte generado:

`data/reportes/validacion_calidad.csv`

## 7. Pruebas automatizadas

Se ejecutaron nueve pruebas específicas de T11 para comprobar la aceptación de registros válidos y la detección de fuentes desconocidas, periodos inválidos, valores faltantes, metadatos vacíos, frecuencias incorrectas, duplicados y columnas faltantes.

También se verificó que la validación no modifica los datos originales.

**Resultado de T11: 9 pruebas aprobadas.**

Se ejecutó igualmente la suite completa del proyecto:

**Resultado general: 63 pruebas aprobadas, sin fallos.**

## 8. Limitaciones y siguientes pasos

La validación comprueba el formato mensual, pero aún no verifica exhaustivamente el calendario ni la correspondencia entre cada fuente, serie, indicador y unidad.

Los valores atípicos no se eliminan automáticamente, puesto que pueden representar observaciones económicas reales.

El archivo de entrada ya se encuentra físicamente en `data/plata`; por tanto, en esta etapa se valida su contenido, pero todavía no se implementa una publicación condicionada que impida escribir datos inválidos en Plata.

En T12 se implementará la Cuarentena para conservar registros inválidos junto con los motivos de rechazo.

En T13 se integrará la Puerta de Calidad al pipeline automatizado para controlar la publicación de los datos.

## 9. Conclusión

Se implementó una primera Puerta de Calidad funcional con Pandera, capaz de validar la estructura de la tabla integrada e identificar errores mediante pruebas automatizadas.

Los 564 registros evaluados cumplieron las reglas configuradas y la suite completa del proyecto obtuvo 63 pruebas aprobadas.