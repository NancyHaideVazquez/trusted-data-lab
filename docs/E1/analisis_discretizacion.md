# T08 — Discretización de variables

## 1. Objetivo

Aplicar técnicas de discretización a las series históricas de INEGI y Banxico para convertir valores numéricos continuos en categorías estadísticas, conservando los datos originales y documentando los límites de los intervalos utilizados.

## 2. Metodología

Se implementaron dos métodos utilizando la biblioteca pandas:

### CUT — Intervalos de igual amplitud

Se utilizó `pd.cut()` para dividir el rango de valores en tres intervalos de igual amplitud.

Este método permite identificar en qué parte del rango total se encuentra cada observación.

### QCUT — Intervalos por cuantiles

Se utilizó `pd.qcut()` para dividir las observaciones en tres grupos mediante cuantiles.

Este método busca obtener categorías con cantidades similares de registros, aunque los intervalos pueden tener amplitudes diferentes.

En ambos casos se utilizaron las etiquetas:

- Bajo
- Medio
- Alto

Estas etiquetas representan posiciones relativas dentro de cada serie y no implican una evaluación económica o social.

## 3. Conservación de datos

Se mantuvo la columna numérica original `valor`.

Se agregaron dos columnas:

- `valor_cut`: clasificación por intervalos de igual amplitud.
- `valor_qcut`: clasificación por cuantiles.

No se eliminaron registros ni se imputaron valores faltantes durante la discretización.

## 4. Resultados de Banxico

Serie: SF43783.

Total de registros: 7,958.

Valores válidos: 7,758.

Valores faltantes conservados: 200.

| Categoría | CUT | QCUT |
|---|---:|---:|
| Bajo | 7,538 | 2,586 |
| Medio | 211 | 2,586 |
| Alto | 9 | 2,586 |
| Sin dato | 200 | 200 |
| **Total** | **7,958** | **7,958** |

### Interpretación

El método CUT concentró la mayoría de las observaciones en la categoría Bajo debido a la amplitud del rango y la presencia de valores extremos.

El método QCUT generó tres grupos con el mismo número de observaciones válidas.

Para análisis comparativos que requieran grupos equilibrados, QCUT es una alternativa más adecuada en esta serie.

## 5. Resultados de INEGI

Serie: 910402.

Total de registros: 183.

Valores faltantes: 0.

| Categoría | CUT | QCUT |
|---|---:|---:|
| Bajo | 29 | 61 |
| Medio | 122 | 63 |
| Alto | 32 | 59 |
| **Total** | **183** | **183** |

### Interpretación

El método CUT concentró la mayoría de las observaciones en la categoría Medio.

El método QCUT produjo una distribución más equilibrada entre las tres categorías.

Ambos métodos se conservaron para permitir diferentes análisis estadísticos.

## 6. Límites y cobertura de los intervalos

Los límites de cada método se almacenaron en:

`data/reportes/parametros_discretizacion.json`

Se utilizaron tres intervalos ordenados por serie y método.

La clasificación se realizó con las funciones `pd.cut()` y `pd.qcut()` de pandas, que asignan cada valor válido a una sola categoría.

La opción `include_lowest=True` permitió incluir el valor mínimo en CUT.

Se comprobó que todos los valores válidos de las dos series recibieron una categoría y que los valores faltantes permanecieron sin clasificar.

## 7. Validación

Se ejecutó el comando:

`python -m pytest tests/test_discretizacion.py -v`

**Resultado: 11 pruebas aprobadas y 0 fallidas.**

Se validaron:

- Discretización mediante CUT.
- Discretización mediante QCUT.
- Conservación de los datos originales.
- Conservación de los valores faltantes.
- Clasificación de todos los valores válidos.
- Orden de los límites.
- Validación de columnas inexistentes.
- Validación de datos no numéricos.
- Validación de métodos incorrectos.
- Manejo de series sin valores válidos.
- Manejo de valores distintos insuficientes.

## 8. Evidencias

### Código fuente

- `src/discretizacion.py`
- `src/ejecutar_discretizacion.py`

### Pruebas automatizadas

- `tests/test_discretizacion.py`

### Archivos generados

- `data/reportes/discretizacion_banxico.csv`
- `data/reportes/discretizacion_inegi.csv`
- `data/reportes/parametros_discretizacion.json`

### Archivos de entrada

- `data/reportes/limpieza_preliminar_banxico.csv`
- `data/reportes/limpieza_preliminar_inegi.csv`

## 9. Conclusión

Se implementaron satisfactoriamente dos técnicas de discretización para las series históricas de INEGI y Banxico.

Los resultados demostraron que CUT y QCUT producen distribuciones diferentes según las características de los datos.

Se conservaron todos los registros y los valores originales, se documentaron los parámetros utilizados y se validó la implementación mediante once pruebas automatizadas aprobadas.