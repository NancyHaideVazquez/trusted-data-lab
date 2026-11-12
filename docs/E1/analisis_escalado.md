# T07 — Normalización y estandarización de datos

## 1. Objetivo

Aplicar técnicas de normalización y estandarización a las series históricas de INEGI y Banxico, conservando los valores originales, los registros faltantes y los parámetros necesarios para reproducir las transformaciones.

## 2. Metodología

Se utilizaron dos técnicas de escalamiento:

### Normalización Min-Max

Transforma los valores utilizando el mínimo y máximo de la serie:

**X_normalizado = (X − mínimo) / (máximo − mínimo)**

Cuando se ajusta con toda la serie, los valores válidos quedan en el intervalo de 0 a 1.

### Estandarización Z-score

Transforma los valores utilizando la media y desviación estándar:

**Z = (X − media) / desviación estándar**

Se utilizó `StandardScaler` de scikit-learn, que calcula la desviación estándar poblacional.

Las transformaciones se aplicaron independientemente a cada serie.

Se conservaron los datos originales y se agregaron las columnas:

- `valor_minmax`
- `valor_zscore`

## 3. Resultados

| Parámetro | Banxico SF43783 | INEGI 910402 |
|---|---:|---:|
| Registros | 7,958 | 183 |
| Mínimo | 3.2741 | -0.24 |
| Máximo | 90.5 | 0.82 |
| Media | 9.9380542537 | 0.2914754098 |
| Desviación estándar | 7.8554478922 | 0.1742697745 |
| Valores faltantes conservados | 200 | 0 |

Los 200 registros no publicados de Banxico permanecieron sin valor tanto en la columna original como en las columnas transformadas.

No se eliminaron registros ni se sustituyeron valores faltantes.

## 4. Reproducibilidad

Los parámetros utilizados se almacenaron en:

`data/reportes/parametros_escalado.json`

Este archivo contiene los valores mínimo, máximo, media y desviación estándar de cada serie.

Las transformaciones pueden reproducirse utilizando los parámetros guardados.

## 5. Prevención de fuga de datos

La función `escalar_datos()` permite ajustar los parámetros con un conjunto de entrenamiento y reutilizarlos posteriormente para transformar otros conjuntos de datos.

Cuando se proporcionan parámetros existentes, la función no vuelve a calcular la media, desviación estándar, mínimo ni máximo.

Esto permite evitar que los datos de prueba influyan en el ajuste del escalamiento.

Los archivos generados en esta tarea utilizan la serie histórica completa para fines descriptivos. No representan una partición de entrenamiento y prueba.

Si posteriormente se desarrolla un modelo predictivo, deberá realizarse una partición temporal y ajustar los parámetros únicamente con los datos de entrenamiento.

## 6. Validación

Se ejecutó el comando:

`python -m pytest tests/test_transformaciones.py -v`

**Resultado: 10 pruebas aprobadas y 0 fallidas.**

Se verificaron:

- Normalización Min-Max.
- Estandarización Z-score.
- Conservación del DataFrame original.
- Conservación de valores faltantes.
- Cálculo de parámetros.
- Validación de columnas.
- Reutilización de parámetros.
- Prevención de fuga de datos mediante parámetros de entrenamiento.

También se ejecutaron las transformaciones sobre los archivos reales de Banxico e INEGI.

## 7. Evidencias

**Código:**

- `src/transformaciones.py`
- `src/ejecutar_escalado.py`

**Pruebas:**

- `tests/test_transformaciones.py`

**Archivos generados:**

- `data/reportes/escalado_banxico.csv`
- `data/reportes/escalado_inegi.csv`
- `data/reportes/parametros_escalado.json`

**Archivos de entrada:**

- `data/reportes/limpieza_preliminar_banxico.csv`
- `data/reportes/limpieza_preliminar_inegi.csv`

## 8. Conclusión

Se implementaron satisfactoriamente las técnicas Min-Max y Z-score para las series históricas de INEGI y Banxico.

Se conservaron los registros originales y los valores faltantes, se almacenaron los parámetros para reproducir los resultados y se incorporó la posibilidad de transformar nuevos datos sin recalcular los parámetros.

La implementación fue validada mediante diez pruebas automatizadas aprobadas.