# T09 — Reducción de datos

## 1. Objetivo

Reducir la cantidad de registros de la serie de Banxico mediante agregación mensual, conservando la información necesaria para el análisis estadístico.

## 2. Datos utilizados

- **Fuente:** Banco de México (Banxico).
- **Serie:** SF43783.
- **Archivo de entrada:** `data/reportes/limpieza_preliminar_banxico.csv`.
- **Archivo de salida:** `data/reportes/reduccion_banxico.csv`.
- **Frecuencia original:** diaria.
- **Frecuencia resultante:** mensual.

## 3. Método de reducción

Se utilizó la agregación temporal mensual mediante el cálculo de la media aritmética de los valores numéricos disponibles en cada mes.

Los valores faltantes no se sustituyeron por cero. Se conservaron los conteos de registros originales y válidos para identificar cuántas observaciones participaron en cada promedio.

La elección del promedio mensual requiere confirmar que la serie corresponde a una tasa de interés y que su unidad es porcentual.

## 4. Resultados

| Característica | Antes | Después |
|---|---:|---:|
| Filas | 7,958 | 381 |
| Columnas | 14 | 8 |

**Reducción de filas:** 95.21 %.

La reducción permitió representar las observaciones diarias mediante registros mensuales.

## 5. Información conservada

El archivo resultante contiene:

- `fuente`
- `serie_id`
- `periodo`
- `valor`
- `registros_originales`
- `registros_validos`
- `unidad_original`
- `metodo_reduccion`

## 6. Pruebas realizadas

Se ejecutaron cuatro pruebas automatizadas mediante pytest:

1. Cálculo correcto del promedio mensual.
2. Conservación de identificadores.
3. Protección de los datos originales.
4. Tratamiento de valores faltantes.

**Resultado:** 4 pruebas aprobadas y 0 errores.

## 7. Consideraciones pendientes

- Verificar en el diccionario de datos la descripción y unidad de la serie SF43783.
- Confirmar la aprobación semántica del método.
- Revisar que los meses sin observaciones válidas permanezcan identificables.
- Verificar si existe un `source_id` que deba conservarse para trazabilidad.

## 8. Conclusión

Se implementó y probó una reducción de datos mediante agregación mensual, disminuyendo los registros de 7,958 a 381 sin modificar el archivo original.

La implementación técnica funciona correctamente. El cierre definitivo de T09 queda sujeto a la validación de metadatos y revisión semántica.


## 9. Verificación de metadatos y validación semántica

### 9.1. Metadatos de la serie

Se identificó la serie SF43783 del Banco de México como la Tasa de Interés Interbancaria de Equilibrio (TIIE) a 28 días.

La serie presenta observaciones diarias de una tasa expresada económicamente en porcentaje anual.

Se distingue entre la unidad económica indicada en el título de la serie y el campo técnico de unidad de las consultas históricas del SIE.

### 9.2. Justificación del método

Se seleccionó la agregación temporal mediante media aritmética mensual porque la variable corresponde a una tasa de interés y no a un flujo acumulable.

La operación permite resumir las tasas observadas durante cada mes sin sumar porcentajes ni modificar su escala.

El resultado representa el promedio mensual de una tasa anualizada, no una tasa de interés mensual efectiva.

### 9.3. Resultados de validación

- Serie identificada: SF43783.
- Método: promedio mensual.
- Registros antes: 7,958.
- Registros después: 381.
- Reducción: 95.21 %.
- Pruebas automatizadas del proyecto: 46 aprobadas.
- Archivos originales: conservados por el procedimiento de reducción.

### 9.4. Limitaciones y revisión

La implementación ignora valores faltantes al calcular los promedios y registra cuántas observaciones válidas existen por mes.

Está pendiente comprobar la cobertura mínima de observaciones de cada mes y documentar cualquier periodo sin datos válidos.

La validación técnica del método es favorable. La aprobación formal del revisor no se ha registrado.

### 9.5. Referencias

- Banco de México, Sistema de Información Económica: https://www.banxico.org.mx/SieInternet/
- Catálogo de series económicas, identificación de SF43783: https://bookdown.org/dcr_infosel/catalogo_datos/


## Validación semántica y análisis de cobertura

Se realizó una revisión de la reducción mensual aplicada a la serie SF43783 de Banxico, identificada como la TIIE a 28 días.

El promedio mensual se considera adecuado para resumir las observaciones de una tasa de interés, siempre que se interprete como el promedio de tasas anualizadas y no como una tasa mensual efectiva.

### Resultados de cobertura

Se analizaron los registros correspondientes al periodo de marzo de 1995 a marzo de 1996, obteniendo:

- Registros originales: 255.
- Registros válidos: 55.
- Registros faltantes o no numéricos: 200.
- Porcentaje de registros válidos: 21.57 %.

También se identificaron 14 meses con menos de 10 observaciones válidas: 13 entre marzo de 1995 y marzo de 1996, y noviembre de 2026.

En noviembre de 2026 se encontraron 8 registros originales y 8 válidos, lo que es compatible con un periodo mensual todavía incompleto.

### Interpretación

La reducción se realizó sin reemplazar ni inventar valores faltantes.

Los promedios calculados para los meses de baja cobertura se conservaron, pero deben utilizarse con precaución debido a su limitada representatividad.

No se establece un umbral mínimo de cobertura como criterio de exclusión, ya que dicho umbral requiere una decisión metodológica explícita.

### Conclusión

La estrategia de reducción mensual mediante promedio aritmético es semánticamente adecuada para una serie de tasas de interés.

La revisión detectó limitaciones de cobertura que quedaron identificadas y documentadas.

La validación técnica del procedimiento es favorable, con advertencias para los periodos de baja cobertura. No se ha registrado una aprobación formal independiente.
