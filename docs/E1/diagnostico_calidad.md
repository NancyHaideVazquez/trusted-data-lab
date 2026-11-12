# Diagnóstico de calidad de datos — T03

**Proyecto:** Trusted Data Lab  
**Etapa:** E1 — Diagnóstico y preparación de datos  
**Fecha de actualización:** 12 de noviembre de 2026

## 1. Objetivo

Evaluar la calidad de los datos históricos de INEGI y Banco de México mediante el análisis de valores faltantes, completitud, tipos de datos, valores únicos, columnas constantes, duplicados y estadísticas descriptivas.

El análisis se realiza sin modificar los archivos originales de la capa Bronce.

## 2. Archivos analizados

### INEGI

- **Indicador:** 910402
- **Registros:** 183
- **Periodo:** agosto de 2011 a octubre de 2026
- **Última observación:** 2026-10-01
- **Archivo:** `data/bronce/inegi/2026-11-12/910402_historico_130114_649094_60dc15f7.json`

### Banco de México

- **Serie:** SF43783
- **Indicador:** TIIE a 28 días
- **Registros:** 7,958
- **Periodo:** marzo de 1995 a noviembre de 2026
- **Última observación:** 2026-11-12
- **Archivo:** `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`

## 3. Resultados generales

Las estadísticas numéricas corresponden a `OBS_VALUE` en INEGI y `dato` en Banxico.

| Métrica | INEGI | Banxico |
|---|---:|---:|
| Registros analizados | 183 | 7,958 |
| Valores faltantes del indicador | 0 | 200 |
| Completitud del indicador | 100% | 97.49% |
| Duplicados exactos | 0 | 0 |
| Duplicados por llave temporal | 0 | 0 |
| Fechas inválidas | 0 | 0 |
| Valores numéricos inválidos adicionales | 0 | 0 |
| Mínimo | -0.2400 | 3.2741 |
| Máximo | 0.8200 | 90.5000 |
| Media | 0.291475 | 9.938054 |
| Mediana | 0.3000 | 7.7050 |
| Primer cuartil (Q1) | 0.1850 | 4.9150 |
| Tercer cuartil (Q3) | 0.3900 | 10.328525 |
| Desviación estándar | 0.174748 | 7.855954 |

Los duplicados por llave se comprobaron utilizando la fecha dentro de cada archivo, dado que cada captura analizada corresponde a una sola serie.

## 4. Diagnóstico por columna

### 4.1 INEGI

| Columna | Tipo | Nulos | Completitud | Valores únicos | Constante |
|---|---|---:|---:|---:|---|
| TIME_PERIOD | str | 0 | 100% | 183 | No |
| OBS_VALUE | str | 0 | 100% | 86 | No |
| OBS_EXCEPTION | object | 183 | 0% | 0 | Sí* |
| OBS_STATUS | str | 0 | 100% | 1 | Sí |
| OBS_SOURCE | str | 183 | 0% | 0 | Sí* |
| OBS_NOTE | str | 183 | 0% | 0 | Sí* |
| COBER_GEO | str | 0 | 100% | 1 | Sí |

*Las columnas marcadas con asterisco están completamente vacías. El programa las identifica como constantes porque tienen cero valores distintos disponibles, aunque técnicamente no contienen un valor constante observado.*

Las columnas `TIME_PERIOD` y `OBS_VALUE` tienen una completitud del 100%. Sin embargo, `OBS_EXCEPTION`, `OBS_SOURCE` y `OBS_NOTE` están completamente vacías.

Esto significa que la serie principal de INEGI está completa, pero no todos los campos auxiliares contienen información.

### 4.2 Banco de México

| Columna | Tipo | Nulos | Completitud | Valores únicos | Constante |
|---|---|---:|---:|---:|---|
| fecha | str | 0 | 100% | 7,958 | No |
| dato | str | 200 | 97.49% | 4,209 | No |

La columna `fecha` está completa y no presenta valores duplicados.

La columna `dato` contiene 200 valores faltantes, identificados mediante el marcador `N/E`.

Los tipos mostrados corresponden a los datos cargados originalmente. Para calcular las estadísticas, los valores numéricos se convierten temporalmente sin modificar Bronce.

## 5. Análisis de valores faltantes

### 5.1 INEGI

La columna principal `OBS_VALUE` no contiene valores faltantes.

Se identificaron tres columnas auxiliares completamente vacías:

- `OBS_EXCEPTION`
- `OBS_SOURCE`
- `OBS_NOTE`

No se deben imputar automáticamente estos campos, ya que primero debe confirmarse su significado y si su ausencia es esperada según la fuente.

### 5.2 Banco de México

Se identificaron 200 valores faltantes de 7,958 registros, equivalentes al 2.51%.

La distribución temporal confirmada es:

| Año | Registros | Faltantes | Porcentaje |
|---|---:|---:|---:|
| 1995 | 193 | 152 | 78.76% |
| 1996 | 252 | 48 | 19.05% |
| 1997–2026 | 7,513 | 0 | 0% |
| **Total** | **7,958** | **200** | **2.51%** |

Todos los valores faltantes de la serie se concentran en 1995 y 1996.

Este patrón temporal no permite demostrar por sí solo si el mecanismo de ausencia es MCAR, MAR o MNAR.

La clasificación y las decisiones de tratamiento se documentan en `docs/E1/analisis_faltantes.md`.

## 6. Tres hallazgos principales

**Hallazgo 1. La serie principal de INEGI está completa.**

Las 183 observaciones cuentan con fecha y valor numérico válido. Sin embargo, existen tres columnas auxiliares completamente vacías, por lo que la completitud debe evaluarse por columna y no únicamente por indicador.

**Hallazgo 2. Los faltantes de Banxico se concentran en los primeros años.**

Aunque el porcentaje global de faltantes es de 2.51%, durante 1995 alcanza el 78.76% y durante 1996 el 19.05%. Desde 1997 no se identificaron faltantes en la captura analizada.

**Hallazgo 3. La serie de Banxico presenta mayor dispersión numérica.**

Banxico tiene una desviación estándar de 7.855954 y un rango entre 3.2741 y 90.50. INEGI tiene una desviación estándar de 0.174748 y un rango entre -0.24 y 0.82.

Estas estadísticas describen cada serie individualmente. No deben interpretarse como una comparación directa de volatilidad porque los indicadores tienen significados y escalas diferentes.

## 7. Validaciones realizadas

El programa `src/diagnostico.py` realiza las siguientes operaciones:

1. Selecciona la captura histórica más reciente de cada fuente.
2. Lee los archivos JSON sin modificar Bronce.
3. Identifica valores faltantes y marcadores como `N/E`, `N/D` y `-`.
4. Calcula la completitud de cada columna.
5. Identifica tipos de datos, valores únicos y columnas constantes.
6. Detecta fechas inválidas y valores numéricos inválidos.
7. Comprueba duplicados exactos y duplicados por fecha dentro de cada serie.
8. Calcula mínimo, máximo, media, mediana, Q1, Q3 y desviación estándar.
9. Genera un reporte general y un reporte detallado por fuente.

## 8. Conclusiones

El diagnóstico permitió identificar las principales características de calidad de ambas fuentes.

INEGI presenta 183 valores válidos en su indicador principal, pero tres campos auxiliares completamente vacíos.

Banxico contiene 7,958 registros, con 200 valores faltantes concentrados en 1995 y 1996.

No se identificaron fechas inválidas, duplicados ni valores numéricos inválidos adicionales en las capturas analizadas.

Los resultados proporcionan información para tomar decisiones sobre tratamiento de faltantes, detección de atípicos y transformaciones posteriores.

Los archivos originales de Bronce no fueron modificados por el programa de diagnóstico.

## 9. Evidencias

- `src/diagnostico.py`
- `data/reportes/diagnostico_calidad.csv`
- `data/reportes/diagnostico_inegi.csv`
- `data/reportes/diagnostico_banxico.csv`
- `data/reportes/faltantes_banxico_por_anio.csv`
- `docs/E1/diccionario_datos.md`
- `docs/E1/analisis_faltantes.md`
- `data/bronce/inegi/2026-11-12/910402_historico_130114_649094_60dc15f7.json`
- `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`

## 10. Ejecución

Desde la raíz del proyecto:

```powershell
python -m src.diagnostico
```

El programa genera los siguientes reportes:

```text
data/reportes/diagnostico_calidad.csv
data/reportes/diagnostico_inegi.csv
data/reportes/diagnostico_banxico.csv
```

Estos reportes permiten consultar los resultados generales y las estadísticas de cada columna de manera independiente.