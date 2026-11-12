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
