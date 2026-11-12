# Análisis de datos faltantes — T04

**Proyecto:** Trusted Data Lab  
**Etapa:** E1 — Diagnóstico y preparación de datos  
**Fecha:** 12 de noviembre de 2026  
**Fuentes analizadas:** INEGI (indicador 910402) y Banco de México (serie SF43783)

## 1. Objetivo

Analizar los valores faltantes de las capturas históricas de INEGI y Banco de México, identificar patrones de ausencia y formular hipótesis sobre los mecanismos MCAR, MAR y MNAR.

También se propone un método de tratamiento para cada columna afectada, justificando la decisión y sus limitaciones.

El análisis no modifica los archivos originales de la capa Bronce.

## 2. Datos analizados

### 2.1 INEGI

Se analizó la captura histórica del indicador 910402, correspondiente al 12 de noviembre de 2026.

- **Total de registros:** 183
- **Periodo:** agosto de 2011 a octubre de 2026
- **Valores faltantes en `OBS_VALUE`:** 0
- **Completitud de `OBS_VALUE`:** 100%

El diagnóstico por columna identificó tres campos completamente vacíos:

| Columna | Registros | Faltantes | Porcentaje faltante |
|---|---:|---:|---:|
| OBS_EXCEPTION | 183 | 183 | 100% |
| OBS_SOURCE | 183 | 183 | 100% |
| OBS_NOTE | 183 | 183 | 100% |

Las columnas `TIME_PERIOD`, `OBS_VALUE`, `OBS_STATUS` y `COBER_GEO` no presentan valores faltantes.

Los campos auxiliares vacíos no implican necesariamente un error de captura. Es necesario revisar su significado antes de decidir si requieren tratamiento.

### 2.2 Banco de México

Se analizó la captura histórica de la serie SF43783, correspondiente a la TIIE a 28 días.

- **Total de registros:** 7,958
- **Valores faltantes:** 200
- **Registros con valor disponible:** 7,758
- **Porcentaje global de faltantes:** 2.51%
- **Marcador identificado:** `N/E`

Los 200 valores faltantes se encuentran en la columna `dato`.

## 3. Distribución temporal de los faltantes

### 3.1 INEGI

Los campos `OBS_EXCEPTION`, `OBS_SOURCE` y `OBS_NOTE` están vacíos en todas las observaciones del periodo analizado.

Por lo tanto, su ausencia no se limita a un año específico: se presenta en el 100% de los registros.

No existe variación en el indicador de ausencia de estas columnas que permita evaluar asociaciones temporales dentro de esta captura.

### 3.2 Banco de México

| Año | Registros | Faltantes | Disponibles | Porcentaje faltante |
|---|---:|---:|---:|---:|
| 1995 | 193 | 152 | 41 | 78.76% |
| 1996 | 252 | 48 | 204 | 19.05% |
| 1997–2026 | 7,513 | 0 | 7,513 | 0% |
| **Total** | **7,958** | **200** | **7,758** | **2.51%** |

Los valores faltantes se concentran exclusivamente en 1995 y 1996.

Aunque la ausencia global representa el 2.51%, durante 1995 alcanza el 78.76% y durante 1996 el 19.05%.

Este patrón muestra una asociación entre el periodo temporal y la presencia de valores faltantes, pero no demuestra por sí solo su mecanismo estadístico.

## 4. Análisis de mecanismos de ausencia

### 4.1 MCAR — Missing Completely At Random

MCAR significa que la probabilidad de que falte un valor no depende de las variables observadas ni de los valores no observados.

En Banxico, la concentración temporal de los faltantes es evidencia contraria a la hipótesis de una ausencia completamente aleatoria respecto al año.

En INEGI, las tres columnas auxiliares están completamente vacías, por lo que no existe información suficiente para comprobar este mecanismo.

### 4.2 MAR — Missing At Random

MAR significa que la probabilidad de ausencia puede explicarse por variables observadas, sin depender de los valores faltantes después de considerar dichas variables.

En Banxico, el año podría estar relacionado con la ausencia. Por ello, MAR es una hipótesis posible, pero no está demostrada.

En INEGI, no se dispone de evidencia suficiente para afirmar que los campos auxiliares estén ausentes debido a otras variables observadas.

### 4.3 MNAR — Missing Not At Random

MNAR significa que la probabilidad de ausencia depende de los valores no observados, incluso después de considerar las variables disponibles.

No existe evidencia suficiente para establecer que los faltantes de INEGI o Banxico correspondan a este mecanismo.

### 4.4 Resultado de la clasificación

Con la información disponible, los mecanismos de ausencia se clasifican como **indeterminados**.

Esta clasificación reconoce que existen patrones observables, pero no se cuenta con evidencia suficiente para identificar definitivamente MCAR, MAR o MNAR.

## 5. Tabla de clasificación y tratamiento propuesto

| Fuente | Columna | Nulos | % | Mecanismo | Confianza | Evidencia | Método propuesto | Limitación |
|---|---|---:|---:|---|---|---|---|---|
| INEGI | OBS_EXCEPTION | 183 | 100% | Indeterminado | Alta en la detección; mecanismo no determinado | Campo vacío en todos los registros | Conservar nulos | No se ha confirmado si el campo es opcional |
| INEGI | OBS_SOURCE | 183 | 100% | Indeterminado | Alta en la detección; mecanismo no determinado | Campo vacío en todos los registros | Conservar nulos | No se ha confirmado si la fuente proporciona este metadato |
| INEGI | OBS_NOTE | 183 | 100% | Indeterminado | Alta en la detección; mecanismo no determinado | Campo vacío en todos los registros | Conservar nulos | No se ha confirmado si existen notas asociadas |
| Banxico | dato | 200 | 2.51% | Indeterminado | Alta en la detección; mecanismo no determinado | Faltantes concentrados en 1995 y 1996 | Conservar nulos | Falta verificar el significado de `N/E` y la causa de ausencia |

La confianza alta corresponde a los conteos y patrones observados, no a la identificación del mecanismo MCAR, MAR o MNAR.

No se recomienda imputar automáticamente ninguna de estas columnas durante esta etapa.

## 6. Justificación del tratamiento

### 6.1 INEGI

Los campos `OBS_EXCEPTION`, `OBS_SOURCE` y `OBS_NOTE` son auxiliares.

Al encontrarse completamente vacíos, no existe información observada en esas mismas columnas que permita estimar valores mediante media, mediana o interpolación.

La decisión propuesta es conservar los valores nulos y documentar su ausencia.

No se deben inventar excepciones, fuentes ni notas.

### 6.2 Banco de México

La columna `dato` representa el valor de la serie TIIE a 28 días.

Los 200 valores `N/E` deben conservarse como faltantes mientras no se confirme su significado y la razón por la cual aparecen en los primeros años.

No se recomienda:

- Reemplazar los faltantes por cero, porque podría introducir valores artificiales.
- Aplicar automáticamente la media o mediana, porque podría distorsionar la serie histórica.
- Interpolar sin comprobar primero que los periodos faltantes sean adecuados para ese procedimiento.
- Eliminar registros silenciosamente, porque se perdería información temporal y trazabilidad.

Si posteriormente se justifica alguna imputación, deberá realizarse sobre una copia de los datos, identificando las observaciones imputadas y conservando los valores originales.

## 7. Limitaciones del análisis

El análisis se basa en las capturas históricas disponibles y en la distribución de los valores faltantes.

No se realizó una prueba estadística concluyente para identificar el mecanismo de ausencia.

Tampoco se verificó todavía mediante documentación oficial si los marcadores `N/E` corresponden a datos no publicados, no disponibles u otra condición específica.

Por estas razones, no se puede afirmar definitivamente que los datos sean MCAR, MAR o MNAR.

La decisión de conservar los faltantes es provisional y deberá revisarse si se obtiene evidencia adicional de las fuentes.

## 8. Relación con T05

Los resultados de T04 proporcionan criterios para la etapa de imputación controlada.

Por el momento, la configuración recomendada es conservar los nulos de las columnas identificadas.

Cualquier tratamiento posterior deberá:

1. Trabajar sobre una copia y mantener Bronce intacto.
2. Justificar el método seleccionado.
3. Registrar qué valores fueron modificados o imputados.
4. Conservar evidencia del número de registros antes y después.
5. Evitar la imputación de fechas, identificadores y valores cuya ausencia represente información no publicada.

## 9. Evidencias

- `src/analisis_faltantes.py`
- `src/diagnostico.py`
- `data/reportes/faltantes_banxico_por_anio.csv`
- `data/reportes/diagnostico_calidad.csv`
- `data/reportes/diagnostico_inegi.csv`
- `data/reportes/diagnostico_banxico.csv`
- `docs/E1/diagnostico_calidad.md`
- `data/bronce/inegi/2026-11-12/910402_historico_130114_649094_60dc15f7.json`
- `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`

## 10. Conclusión

El análisis permitió identificar dos situaciones diferentes de ausencia.

En INEGI, el indicador principal está completo, pero tres columnas auxiliares presentan un 100% de valores faltantes.

En Banxico, se identificaron 200 valores faltantes en la columna `dato`, concentrados exclusivamente en 1995 y 1996.

Los patrones observados permiten describir la distribución de los faltantes, pero no determinar de manera definitiva su mecanismo estadístico.

Se propone conservar los nulos, evitar imputaciones sin justificación y mantener intactos los archivos originales de la capa Bronce.