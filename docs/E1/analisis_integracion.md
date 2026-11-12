# T10 — Integración de datos

## 1. Objetivo

Integrar los datos procesados provenientes del Instituto Nacional de Estadística y Geografía (INEGI) y del Banco de México (Banxico), conservando su identificación, periodicidad y metadatos, para disponer de una estructura común de consulta y análisis.

## 2. Fuentes utilizadas

| Fuente | Serie | Indicador | Frecuencia |
|---|---|---|---|
| INEGI | 910402 | Inflación mensual | Mensual |
| Banxico | SF43783 | TIIE a 28 días | Diaria, reducida a mensual |

Archivos de entrada:

- `data/reportes/limpieza_preliminar_inegi.csv`
- `data/reportes/reduccion_banxico.csv`

## 3. Método de integración

Se utilizó una integración vertical mediante la función `pd.concat()` de pandas.

Primero se normalizó la fecha de INEGI al formato `AAAA-MM`. Los datos de Banxico ya se encontraban reducidos a frecuencia mensual mediante T09.

Posteriormente se seleccionaron nueve columnas comunes y se concatenaron los registros, conservando la fuente y el identificador de cada serie.

No se realizó una unión horizontal ni se sumaron valores de indicadores diferentes.

## 4. Metadatos conservados

El archivo integrado contiene:

- `fuente`: institución de origen.
- `serie_id`: identificador de la serie.
- `indicador`: descripción del indicador.
- `periodo`: periodo mensual.
- `valor`: valor observado o agregado.
- `unidad`: unidad económica.
- `frecuencia`: periodicidad de los datos integrados.
- `metodo`: tratamiento aplicado.
- `cobertura`: ámbito geográfico.

## 5. Resultados

| Concepto | Cantidad |
|---|---:|
| Registros de INEGI | 183 |
| Registros de Banxico | 381 |
| Registros integrados | 564 |
| Columnas finales | 9 |
| Registros duplicados | 0 |
| Valores faltantes | 0 |
| Metadatos faltantes en las columnas verificadas | 0 |

Periodo global del archivo: marzo de 1995 a noviembre de 2026.

El periodo global representa el mínimo y máximo de las series integradas; no implica que ambas tengan observaciones durante todos esos meses.

Archivo de salida:

`data/plata/integracion_mensual.csv`

## 6. Validación y pruebas

Se ejecutaron ocho pruebas automatizadas para T10, verificando:

- Cantidad de registros.
- Conservación de fuentes.
- Conservación de identificadores.
- Normalización de periodos.
- No modificación de los datos originales.
- Conservación de valores.
- Presencia de metadatos.
- Correspondencia de metadatos por fuente.

El conjunto completo del proyecto obtuvo **54 pruebas aprobadas**, sin fallos.

También se comprobó que el archivo generado no contiene duplicados por fuente, serie y periodo, ni valores o metadatos faltantes en los campos revisados.

## 7. Compatibilidad semántica y limitaciones

La integración es válida como catálogo común de observaciones mensuales, porque cada registro conserva su fuente, identificador, indicador y unidad.

La inflación mensual y la TIIE a 28 días representan conceptos económicos diferentes. Por ello, sus valores no deben sumarse ni interpretarse como magnitudes directamente equivalentes.

La frecuencia mensual de Banxico corresponde a promedios de observaciones diarias de una tasa anualizada.

La reducción de Banxico identificó meses con baja cobertura de observaciones, por lo que sus promedios deben interpretarse con precaución.

La integración no constituye una serie de precios de vivienda ni demuestra relaciones causales entre inflación y tasas de interés.

## 8. Conclusión

Se generó correctamente una tabla integrada de 564 registros y nueve columnas, conservando la identificación y el significado de ambas series.

La implementación superó las pruebas automatizadas y las comprobaciones estructurales realizadas.

La integración queda técnicamente preparada para revisión y uso posterior, respetando las limitaciones semánticas y de cobertura documentadas.