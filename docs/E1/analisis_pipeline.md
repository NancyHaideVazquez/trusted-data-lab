# Análisis del pipeline de datos Bronce → Plata → Oro

## 1. Objetivo

Automatizar el procesamiento de los datos históricos de INEGI y Banxico, desde los archivos JSON almacenados en la capa Bronce hasta la generación de datos integrados y validados en las capas Plata y Oro.

El proceso incorpora diagnóstico de calidad, limpieza conservadora, detección de valores atípicos, transformaciones, reducción, integración, validación automática, separación de registros inválidos y publicación protegida.

Además, incluye una bitácora de ejecución y pruebas de idempotencia para comprobar que el procesamiento repetido con las mismas entradas produce resultados consistentes y sin duplicados.

## 2. Arquitectura del pipeline

El proyecto utiliza una arquitectura por capas:

- **Bronce:** conserva los archivos originales de las fuentes oficiales.
- **Plata:** almacena los registros mensuales integrados que superaron las reglas de calidad.
- **Oro:** contiene los indicadores preparados para consulta y análisis.
- **Cuarentena:** conserva los registros rechazados y sus motivos.
- **Reportes:** almacena información de diagnóstico y resultados del procesamiento.
- **Logs:** registra las ejecuciones del pipeline.

La lógica se organiza en dos carpetas principales:

- `src/`: funciones de procesamiento, limpieza, transformación y validación.
- `pipeline/`: coordinación de las etapas y publicación de resultados.

Esta separación permite reutilizar las funciones y mantener organizado el código del proyecto.

## 3. Flujo de procesamiento

El pipeline realiza las siguientes operaciones:

1. **Selección de archivos:** identifica los archivos JSON históricos más recientes de INEGI y Banxico.
2. **Diagnóstico:** analiza valores faltantes, completitud, fechas inválidas, duplicados y estadísticas descriptivas.
3. **Lectura:** carga los archivos originales sin modificarlos.
4. **Limpieza conservadora:** normaliza fechas y valores, identifica faltantes y detecta atípicos mediante el método IQR.
5. **Reducción:** convierte las observaciones diarias de Banxico en observaciones mensuales.
6. **Transformaciones:** aplica escalado Min-Max, estandarización Z-score y discretización como análisis auxiliares.
7. **Integración:** combina las series mensuales de INEGI y Banxico en una estructura común.
8. **Validación de calidad:** comprueba las reglas definidas mediante Pandera.
9. **Cuarentena:** separa los registros que no cumplen las reglas y conserva sus motivos de rechazo.
10. **Preparación de Plata:** utiliza únicamente los registros aprobados.
11. **Preparación de Oro:** genera una tabla curada para consulta.
12. **Publicación protegida:** guarda las salidas mediante archivos temporales y respaldos.
13. **Registro de ejecución:** guarda la fecha UTC, los archivos utilizados, los conteos y las rutas de salida.

Actualmente, la integración ocurre antes de la validación de la tabla mensual conjunta. Esta decisión permite verificar la estructura integrada antes de publicar, aunque no equivale a validar individualmente cada fuente antes de la integración.

## 4. Archivos del proyecto

| Archivo | Función |
|---|---|
| `src/main.py` | Punto de entrada para ejecutar el pipeline |
| `pipeline/ejecutar_pipeline.py` | Coordina el procesamiento completo |
| `pipeline/publicacion.py` | Gestiona la publicación protegida |
| `src/diagnostico.py` | Diagnóstico y selección de archivos históricos |
| `src/lectura.py` | Lectura de los archivos originales |
| `src/limpieza.py` | Normalización, tratamiento conservador y detección de atípicos |
| `src/transformaciones.py` | Escalado Min-Max y Z-score |
| `src/discretizacion.py` | Clasificación de valores numéricos |
| `src/reduccion.py` | Agregación mensual de Banxico |
| `src/integracion.py` | Integración de ambas fuentes |
| `src/calidad.py` | Validación automática mediante Pandera |
| `src/cuarentena.py` | Separación de registros inválidos |
| `src/oro.py` | Preparación de los indicadores de Oro |
| `tests/test_pipeline.py` | Pruebas automatizadas del procesamiento |
| `tests/test_publicacion.py` | Pruebas de publicación y recuperación |

## 5. Ejecución

Desde la raíz del repositorio, el pipeline se ejecuta con:

`python -m src.main`

También puede ejecutarse directamente mediante:

`python -m pipeline.ejecutar_pipeline`

El proceso utiliza los archivos históricos previamente capturados en Bronce. No realiza nuevas descargas desde las API oficiales.

## 6. Diagnóstico de las fuentes

Se utilizaron las siguientes series históricas:

| Característica | INEGI | Banxico |
|---|---|---|
| Identificador | 910402 | SF43783 |
| Frecuencia de entrada | Mensual | Diaria |
| Registros originales | 183 | 7,958 |
| Valores faltantes | 0 | 200 |
| Atípicos detectados mediante IQR | 4 | 1,044 |

El diagnóstico comprueba la estructura de los datos, identifica problemas potenciales y calcula estadísticas descriptivas.

La detección de atípicos se realiza mediante el rango intercuartílico con factor 1.5.

Los valores atípicos quedan marcados para revisión, sin eliminarlos ni modificarlos automáticamente.

## 7. Tratamiento de valores faltantes

En los datos históricos de Banxico se detectaron 200 observaciones sin valor numérico publicado.

Los marcadores como `N/E` se interpretan como datos faltantes durante el procesamiento numérico.

Se decidió no aplicar imputación automática porque estos registros corresponden a valores no publicados por la fuente oficial.

Sustituirlos mediante medias, medianas o interpolaciones podría introducir valores que no fueron observados.

Por esta razón, el procesamiento mantiene una política conservadora:

- No se sustituyen valores faltantes por cero.
- No se imputan automáticamente los valores no publicados.
- Se conserva el valor original y el motivo de revisión durante la preparación.
- Los promedios mensuales se calculan utilizando los valores numéricos disponibles.

Esta decisión evita introducir observaciones artificiales, aunque requiere considerar la cobertura de cada periodo al interpretar los resultados.

## 8. Detección de valores atípicos

Se utilizó el método del rango intercuartílico para detectar observaciones extremas.

Los resultados fueron:

| Fuente | Atípicos identificados |
|---|---:|
| INEGI | 4 |
| Banxico | 1,044 |

Los valores marcados no necesariamente representan errores.

En indicadores económicos, las variaciones extremas pueden corresponder a acontecimientos reales y resultar relevantes para el análisis.

Por ello, los atípicos se conservan y se clasifican como observaciones que requieren revisión.

## 9. Escalado y discretización

Las transformaciones se aplican por separado a cada indicador, sin mezclar las distribuciones de INEGI y Banxico.

### Escalado

Se utilizan dos métodos:

- **Min-Max:** transforma los valores numéricos a una escala relativa.
- **Z-score:** expresa la distancia de cada valor respecto a la media en unidades de desviación estándar.

Ambos procedimientos conservan la columna original y generan resultados adicionales.

### Discretización

Se utiliza el método `cut`, que divide el rango de valores en tres intervalos de igual amplitud:

- Bajo.
- Medio.
- Alto.

Los resultados obtenidos fueron:

| Categoría | INEGI | Banxico |
|---|---:|---:|
| Bajo | 29 | 359 |
| Medio | 122 | 20 |
| Alto | 32 | 2 |
| Total | 183 | 381 |

Las categorías describen la distribución de cada indicador y no deben interpretarse como una clasificación de errores.

Cuando existen menos de tres valores numéricos distintos, la discretización se omite y el pipeline registra esta condición.

Las transformaciones se calculan como resultados auxiliares en memoria. Los valores originales permanecen sin modificaciones en las tablas publicadas.

## 10. Reducción e integración

Para integrar las dos fuentes se utiliza una frecuencia mensual común.

Los registros diarios de Banxico se agrupan por fuente, serie y periodo, calculando el promedio mensual de las observaciones numéricas disponibles.

El resultado de la reducción fue:

**7,958 registros diarios → 381 registros mensuales.**

Posteriormente, los 381 registros mensuales de Banxico se integraron con los 183 registros de INEGI.

| Concepto | Registros |
|---|---:|
| INEGI original | 183 |
| Banxico original | 7,958 |
| Total de registros de entrada | 8,141 |
| INEGI mensual | 183 |
| Banxico mensual | 381 |
| Registros integrados | 564 |

La diferencia entre el número de observaciones originales y la tabla integrada se debe al cambio de granularidad de los datos diarios de Banxico.

Los indicadores se conservan como series independientes. No se suman ni se promedian valores entre ambas fuentes porque representan conceptos económicos diferentes.

## 11. Validación de calidad y Cuarentena

Los registros integrados se validan mediante las reglas definidas en Pandera.

Las comprobaciones incluyen estructura, tipos de datos, columnas obligatorias, periodos válidos, frecuencia mensual, valores requeridos y unicidad por fuente, serie y periodo.

Los registros inválidos identificables se separan en Cuarentena con el motivo correspondiente.

Los errores estructurales que impiden procesar los datos de forma segura detienen la ejecución.

La conciliación obtenida fue:

| Concepto | Resultado |
|---|---:|
| Registros integrados | 564 |
| Registros válidos | 564 |
| Registros rechazados | 0 |
| Estado | SIN_RECHAZOS |

Se verificó la igualdad:

**564 registros integrados = 564 válidos + 0 rechazados.**

Antes de publicar se valida nuevamente la tabla de registros aprobados.

## 12. Resultados de Plata y Oro

Los archivos generados son:

| Capa | Archivo | Registros |
|---|---|---:|
| Plata | `data/plata/integracion_mensual.csv` | 564 |
| Oro | `data/oro/indicadores_mensuales.csv` | 564 |
| Cuarentena | `data/cuarentena/registros/integracion_mensual_rechazados.csv` | 0 |
| Reporte | `data/cuarentena/reportes/reporte_cuarentena.csv` | 1 fila de resumen |

La tabla Oro contiene ocho columnas y conserva las observaciones mensuales de ambas fuentes por separado.

La revisión de Plata confirmó:

- Cero duplicados por fuente, serie y periodo.
- Cero valores faltantes en la columna `valor`.
- Conservación de los identificadores de las fuentes.

## 13. Protección de los archivos originales

Los archivos JSON de Bronce se utilizan como entradas de lectura.

El pipeline no realiza operaciones destinadas a modificar, reemplazar o eliminar estos archivos.

Una prueba automatizada utiliza archivos JSON temporales y compara sus contenidos antes y después de ejecutar el procesamiento.

Los resultados confirmaron que los archivos permanecen idénticos.

Esta comprobación respalda la política de inmutabilidad de Bronce, aunque no reemplaza una auditoría completa de integridad de todos los históricos reales.

## 14. Publicación protegida

El módulo de publicación prepara archivos temporales y conserva respaldos de las versiones anteriores.

Si ocurre un error controlado durante el reemplazo de archivos, intenta restaurar los resultados previamente publicados.

Las pruebas automatizadas comprobaron la recuperación ante un fallo simulado.

El mecanismo reduce el riesgo de publicaciones parciales, pero no garantiza atomicidad completa entre varios archivos ni recuperación ante interrupciones abruptas del sistema.

## 15. Bitácora de ejecución

Cada ejecución exitosa se registra en:

`logs/pipeline_ejecuciones.csv`

La bitácora contiene:

- Fecha y hora en UTC.
- Archivos históricos utilizados.
- Cantidad de registros de cada fuente.
- Registros mensuales de Banxico.
- Registros integrados.
- Registros válidos e inválidos.
- Rutas de las salidas publicadas.
- Estado de ejecución.

Este registro es independiente de `logs/capturas.csv`, que pertenece a los extractores.

La bitácora actual documenta las ejecuciones exitosas; los fallos que ocurran antes de la publicación no quedan registrados de forma completa.

## 16. Idempotencia

Se realizaron dos ejecuciones consecutivas del pipeline utilizando los mismos archivos históricos.

Después de cada ejecución se calcularon hashes SHA-256 de las salidas de Plata y Oro.

| Comprobación | Resultado |
|---|---|
| Plata idéntica entre ejecuciones | True |
| Oro idéntico entre ejecuciones | True |
| Registros Plata | 564 |
| Registros Oro | 564 |
| Duplicados Plata | 0 |
| Duplicados Oro | 0 |

Adicionalmente, una prueba automatizada ejecuta dos veces el pipeline con entradas temporales y compara los contenidos de las cuatro salidas.

Los resultados permiten comprobar la idempotencia bajo las mismas condiciones de entrada.

La bitácora registra cada ejecución como un evento independiente, aunque las tablas publicadas sean idénticas.

## 17. Pruebas automatizadas

Se ejecutó el conjunto completo de pruebas mediante:

`python -m pytest tests/ -q`

El resultado fue:

**83 pruebas aprobadas y 0 fallos.**

Nueve pruebas verifican directamente el procesamiento automatizado, incluyendo:

- Publicación de registros válidos.
- Separación de registros inválidos.
- Rechazo de errores estructurales.
- Generación de Oro.
- Conservación de las series.
- Protección ante fallos de preparación.
- Inmutabilidad de Bronce.
- Idempotencia.
- Omisión controlada de discretización con pocos valores distintos.

Otras tres pruebas verifican la publicación protegida, la recuperación ante errores simulados y el rechazo de rutas duplicadas.

## 18. Alcance y limitaciones

El pipeline procesa archivos históricos existentes en Bronce, pero no realiza nuevas extracciones desde las API oficiales.

No imputa automáticamente los valores faltantes no publicados.

Los resultados de escalado y discretización se generan como análisis auxiliares y no se incorporan actualmente a los archivos publicados.

La selección de archivos históricos depende de la fecha de carpeta y del nombre de los archivos disponibles.

El mecanismo de publicación no garantiza atomicidad completa ante interrupciones abruptas.

La bitácora registra las ejecuciones exitosas, pero no representa todavía un sistema completo de monitoreo y recuperación de fallos.

Estas limitaciones deben considerarse durante las mejoras posteriores del sistema.

## 19. Conclusión

Se implementó un pipeline automatizado que comienza con los archivos históricos de Bronce y genera datos integrados y validados en Plata y Oro, junto con los archivos y reportes de Cuarentena.

El procesamiento incorpora diagnóstico, limpieza conservadora, detección de atípicos, transformaciones auxiliares, reducción, integración y controles automáticos de calidad.

La ejecución real produjo 564 registros mensuales válidos, sin duplicados ni valores faltantes en Plata.

También se verificaron la inmutabilidad de Bronce, la publicación protegida, el registro de ejecuciones y la idempotencia.

**La última ejecución de pruebas obtuvo 83 pruebas aprobadas y cero fallos.**