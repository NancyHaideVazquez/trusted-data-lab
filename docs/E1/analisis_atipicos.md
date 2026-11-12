# T06 — Detección y tratamiento de valores atípicos

## 1. Objetivo

Identificar valores atípicos en las series históricas de INEGI y Banco de México (Banxico), utilizando el método del rango intercuartílico (IQR), sin modificar ni eliminar los registros originales.

El propósito es detectar observaciones que requieren revisión y conservar la trazabilidad de los datos.

## 2. Metodología

Se utilizó el método de Tukey, basado en el rango intercuartílico (IQR).

Las fórmulas utilizadas fueron:

- **Q1:** Primer cuartil (25 %).
- **Q3:** Tercer cuartil (75 %).
- **IQR:** Q3 − Q1.
- **Límite inferior:** Q1 − 1.5 × IQR.
- **Límite superior:** Q3 + 1.5 × IQR.

Una observación se marca como atípica cuando su valor está fuera de los límites establecidos.

El análisis se realizó de forma independiente para cada serie, evitando mezclar indicadores con diferentes escalas y comportamientos.

## 3. Resultados obtenidos

### 3.1. Banxico — Serie SF43783

| Estadística | Resultado |
|---|---:|
| Registros totales | 7,958 |
| Valores numéricos válidos | 7,758 |
| Primer cuartil (Q1) | 4.915 |
| Tercer cuartil (Q3) | 10.328525 |
| Rango intercuartílico (IQR) | 5.413525 |
| Límite inferior | -3.2052875 |
| Límite superior | 18.4488125 |
| Valores atípicos detectados | 1,044 |
| Registros eliminados | 0 |
| Registros imputados | 0 |

Se identificaron 1,044 observaciones fuera de los límites calculados.

La serie contiene información histórica de tasas de interés, por lo que pueden existir variaciones importantes entre distintos periodos económicos.

Los valores extremos se conservaron y marcaron como pendientes de revisión, ya que el método IQR identifica diferencias estadísticas, pero no demuestra por sí solo que los datos sean incorrectos.

También se conservaron los 200 registros no publicados, sin sustituirlos por cero ni aplicar imputaciones.

### 3.2. INEGI — Serie 910402

| Estadística | Resultado |
|---|---:|
| Registros totales | 183 |
| Valores numéricos válidos | 183 |
| Primer cuartil (Q1) | 0.185 |
| Tercer cuartil (Q3) | 0.390 |
| Rango intercuartílico (IQR) | 0.205 |
| Límite inferior | -0.1225 |
| Límite superior | 0.6975 |
| Valores atípicos detectados | 4 |
| Registros eliminados | 0 |
| Registros imputados | 0 |

Se identificaron cuatro observaciones fuera de los límites del método IQR.

Los valores fueron conservados porque no existe evidencia suficiente para clasificarlos como errores de captura o medición.

## 4. Tratamiento de los valores atípicos

Se aplicaron las siguientes decisiones:

1. Conservar todos los registros originales.
2. Marcar los valores extremos mediante la columna `es_atipico`.
3. Utilizar `clasificacion_atipico` para indicar las observaciones que requieren revisión.
4. Mantener la clasificación `por_revisar` para los valores extremos detectados.
5. No sustituir, eliminar ni corregir automáticamente los valores atípicos.
6. Realizar los cálculos de forma independiente por serie.

Esta estrategia permite mantener la integridad de los datos y facilita futuras revisiones estadísticas.

## 5. Justificación de las decisiones

Se decidió utilizar IQR porque permite identificar observaciones extremas mediante cuartiles, sin depender directamente de la media o desviación estándar.

No se eliminaron valores atípicos porque una observación extrema puede representar un fenómeno económico real.

En particular, las series económicas pueden presentar cambios importantes a lo largo del tiempo. Por esta razón, los resultados del método IQR se consideran alertas estadísticas y no pruebas definitivas de errores.

Una limitación del análisis es que el cálculo global de cuartiles puede marcar numerosos valores de periodos históricos con comportamientos diferentes. Esto es especialmente relevante para la serie de Banxico.

Como mejora futura, se recomienda contrastar los valores señalados con la fuente oficial y analizar los cambios históricos antes de modificar cualquier observación.

## 6. Validación y pruebas

Se ejecutaron las pruebas automatizadas del módulo de limpieza mediante el comando:

`python -m pytest tests/test_limpieza.py -v`

**Resultado obtenido: 21 pruebas aprobadas, 0 fallidas.**

Las pruebas verificaron, entre otros aspectos:

- Detección de valores extremos mediante IQR.
- Análisis independiente por serie.
- Conservación de los datos originales.
- Tratamiento de grupos con pocos registros.
- Protección de identificadores y fechas.
- Conservación de valores no publicados.
- Ausencia de eliminación automática de registros.

## 7. Evidencias

**Código fuente:**

- `src/limpieza.py`

**Pruebas automatizadas:**

- `tests/test_limpieza.py`

**Reportes de valores atípicos:**

- `data/reportes/atipicos_iqr_banxico.csv`
- `data/reportes/atipicos_iqr_inegi.csv`

**Reportes de limpieza:**

- `data/reportes/resumen_limpieza_banxico.csv`
- `data/reportes/resumen_limpieza_inegi.csv`

**Datos originales:**

- `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`
- `data/bronce/inegi/2026-11-12/910402_historico_130114_649094_60dc15f7.json`

## 8. Conclusión

La tarea T06 permitió detectar 1,044 valores atípicos en Banxico y cuatro en INEGI mediante el método IQR.

Se conservaron todos los registros y se marcaron los valores extremos para su posterior revisión, sin alterar las observaciones originales.

La implementación cuenta con pruebas automatizadas aprobadas y reportes que permiten verificar los cálculos realizados.

Por lo tanto, se cumple el objetivo técnico de detectar y señalar valores atípicos sin comprometer la integridad de las series históricas.