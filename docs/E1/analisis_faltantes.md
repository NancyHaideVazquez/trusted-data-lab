# Análisis de datos faltantes — T04

**Proyecto:** Trusted Data Lab  
**Etapa:** E1 — Diagnóstico y preparación de datos  
**Fecha:** 12 de noviembre de 2026  
**Fuente analizada:** Banco de México, serie SF43783 (TIIE a 28 días)

## 1. Objetivo

Analizar la distribución temporal de los valores faltantes en la serie histórica de Banco de México, identificar posibles patrones de ausencia y discutir los mecanismos MCAR, MAR y MNAR.

## 2. Datos analizados

Se utilizó la captura histórica del 12 de noviembre de 2026, correspondiente a la serie SF43783.

- **Total de registros:** 7,958
- **Valores faltantes:** 200
- **Registros disponibles:** 7,758
- **Porcentaje global de faltantes:** 2.51%
- **Marcador identificado:** `N/E`

Los archivos originales de la capa Bronce no fueron modificados.

## 3. Distribución temporal de los faltantes

| Año | Registros | Faltantes | Disponibles | Porcentaje faltante |
|---|---:|---:|---:|---:|
| 1995 | 193 | 152 | 41 | 78.76% |
| 1996 | 252 | 48 | 204 | 19.05% |
| 1997–2026 | 7,513 | 0 | 7,513 | 0% |
| **Total** | **7,958** | **200** | **7,758** | **2.51%** |

Se identificó una concentración de valores faltantes durante los primeros dos años de la serie histórica.

En 1995, aproximadamente el 78.76% de las observaciones registradas no tiene un valor numérico disponible. En 1996, esta proporción disminuye al 19.05%.

Desde 1997 hasta noviembre de 2026 no se identificaron observaciones con el marcador `N/E`.

## 4. Análisis de mecanismos de ausencia

### MCAR — Missing Completely At Random

Los datos se consideran MCAR cuando la probabilidad de ausencia no depende de las variables observadas ni de los valores faltantes.

La concentración de los faltantes en 1995 y 1996 muestra una asociación temporal que requiere investigación. No se puede afirmar que los datos sean MCAR.

### MAR — Missing At Random

Los datos se consideran MAR cuando, una vez consideradas las variables observadas, la ausencia no depende de los valores que faltan.

Dado que los faltantes están concentrados en determinados años, MAR constituye una hipótesis posible. Sin embargo, el patrón observado no demuestra por sí solo este mecanismo.

### MNAR — Missing Not At Random

Los datos se consideran MNAR cuando la probabilidad de ausencia depende de los propios valores no observados, incluso después de considerar las variables disponibles.

No se cuenta con evidencia suficiente para establecer que los valores faltantes de Banxico correspondan a este mecanismo.

## 5. Interpretación

El análisis identificó un patrón temporal de valores faltantes en la serie histórica SF43783.

Aunque el porcentaje global de ausencia es relativamente pequeño (2.51%), su distribución no es uniforme. Los faltantes representan una proporción elevada de las observaciones de 1995 y una proporción importante de las de 1996.

Por esta razón, el porcentaje global no debe utilizarse como único criterio para evaluar la calidad de la serie.

La información disponible permite describir el patrón, pero no establecer de manera definitiva su causa o mecanismo estadístico.

## 6. Consideraciones para el tratamiento

- Conservar los archivos originales de la capa Bronce sin modificaciones.
- Mantener identificados los valores `N/E` como datos faltantes.
- No reemplazar los valores faltantes por cero.
- Evitar imputaciones automáticas sin una justificación estadística.
- Documentar cualquier decisión de filtrado o tratamiento en etapas posteriores.
- Investigar la documentación de la fuente para determinar si existen razones de publicación o disponibilidad que expliquen los registros faltantes.

## 7. Evidencias

- `src/analisis_faltantes.py`
- `data/reportes/faltantes_banxico_por_anio.csv`
- `src/diagnostico.py`
- `data/reportes/diagnostico_calidad.csv`
- `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`

## 8. Conclusión

Se identificaron 200 valores faltantes en la serie histórica de Banxico, concentrados exclusivamente en 1995 y 1996.

El análisis demuestra que la ausencia presenta una concentración temporal, pero no permite determinar de manera concluyente si el mecanismo corresponde a MCAR, MAR o MNAR.

Se recomienda conservar los registros originales y documentar las decisiones de tratamiento antes de continuar con la preparación de los datos para la capa Plata.