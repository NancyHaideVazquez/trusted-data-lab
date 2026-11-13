# Matriz de requerimientos verificables — E1

**Proyecto:** Trusted Data Lab
**Observatorio:** Vivienda y Costos de Colima
**Etapa:** E1 — Datos de confianza y pronóstico
**Equipo:** Nancy y David
**Fecha de revisión:** 13 de noviembre de 2026

## 1. Objetivo

Establecer requisitos funcionales y no funcionales verificables para el pipeline de datos del observatorio, especificando para cada uno un criterio de aceptación y la evidencia que permite evaluar su cumplimiento.

La matriz vincula los requisitos con las pruebas automatizadas, los resultados documentados y las verificaciones pendientes. Se diferencia entre tener una prueba implementada y contar con evidencia suficiente de cumplimiento.

## 2. Requerimientos funcionales

| ID | Requerimiento verificable | Criterio de aceptación | Evidencia | Estado |
|---|---|---|---|---|
| RF-01 | Preservar la capa Bronce durante el procesamiento | El contenido y los hashes SHA-256 permanecen idénticos antes y después de ejecutar el pipeline | [test_pipeline_no_modifica_bronce](../../tests/test_pipeline.py) | Verificado |
| RF-02 | Validar automáticamente los datos de entrada | Se detectan valores faltantes, fuentes desconocidas, periodos inválidos, frecuencia incorrecta y duplicados | [Pruebas de calidad](../../tests/test_calidad.py) | Verificado |
| RF-03 | Enviar registros inválidos a Cuarentena | Los registros rechazados se conservan con un motivo específico y no desaparecen silenciosamente | [Pruebas de Cuarentena](../../tests/test_cuarentena.py) | Verificado |
| RF-04 | Detener el procesamiento ante errores estructurales inseguros | Una estructura inválida impide publicar resultados incorrectos | [test_pipeline_detiene_error_estructural](../../tests/test_pipeline.py) | Verificado |
| RF-05 | Identificar observaciones atípicas sin eliminarlas automáticamente | Los valores extremos se marcan, conservando los registros y sus valores originales | [test_iqr_marca_extremo_sin_eliminar_ni_modificar_original](../../tests/test_limpieza.py) | Verificado |
| RF-06 | Aplicar tratamientos controlados de valores faltantes | La imputación respeta grupos, orden temporal y reglas que evitan inventar ceros | [Pruebas de limpieza](../../tests/test_limpieza.py) | Verificado en funciones |
| RF-07 | Normalizar y estandarizar indicadores sin alterar valores originales | Min-Max y Z-score generan valores transformados sin modificar las entradas | [Pruebas de transformaciones](../../tests/test_transformaciones.py) | Verificado |
| RF-08 | Discretizar indicadores numéricos | Los valores válidos se clasifican según el método elegido y sus límites son consistentes | [Pruebas de discretización](../../tests/test_discretizacion.py) | Verificado |
| RF-09 | Reducir observaciones diarias a frecuencia mensual | La agregación conserva identificadores y calcula promedios mensuales sin modificar originales | [Pruebas de reducción](../../tests/test_reduccion.py) | Verificado |
| RF-10 | Integrar fuentes con metadatos identificables | Cada registro conserva fuente, serie, periodo, valor y metadatos correspondientes | [Pruebas de integración](../../tests/test_integracion.py) | Verificado |
| RF-11 | Publicar automáticamente las capas Plata y Oro | La ejecución con datos válidos genera las salidas esperadas y conserva sus series | [Pruebas del pipeline](../../tests/test_pipeline.py) | Verificado |
| RF-12 | Garantizar idempotencia | Dos ejecuciones con las mismas entradas producen salidas equivalentes sin duplicar registros | [test_pipeline_es_idempotente](../../tests/test_pipeline.py) | Verificado |
| RF-13 | Proteger los resultados durante la publicación | Una excepción simulada durante la publicación permite recuperar las salidas anteriores | [test_recuperacion_si_falla_publicacion](../../tests/test_publicacion.py) | Verificado ante fallo simulado |
| RF-14 | Generar análisis y pronósticos para las series mensuales | Se obtienen resultados ADF, ACF/PACF, cuatro modelos, métricas y pronósticos | [Análisis estadístico](estadistica/analisis_series_temporales.md) · [Comparación de modelos](estadistica/comparacion_general_modelos.csv) | Evidencia de ejecución; faltan pruebas automatizadas específicas |

## 3. Requerimientos no funcionales

| ID | Requerimiento verificable | Criterio de aceptación | Evidencia | Estado |
|---|---|---|---|---|
| RNF-01 | Mantener una suite automatizada de pruebas | Todas las pruebas pasan sin fallos | [Evidencia pytest](evidencia_pruebas_cobertura.txt) | Verificado: 85 pruebas aprobadas |
| RNF-02 | Medir cobertura de código | Se genera un reporte de cobertura reproducible | [Reporte de cobertura](evidencia_pruebas_cobertura.txt) | Verificado: 54%; sin umbral aprobado documentado |
| RNF-03 | Revisar las dependencias para detectar vulnerabilidades conocidas | La auditoría de dependencias no informa vulnerabilidades conocidas abiertas | [Evidencia de seguridad](evidencia_seguridad.md) | Verificado en la ejecución documentada |
| RNF-04 | Revisar el repositorio para detectar secretos | El historial Git y los archivos del proyecto se analizan mediante Gitleaks | [Evidencia de seguridad](evidencia_seguridad.md) | Verificado con las exclusiones documentadas |
| RNF-05 | Medir fiabilidad y disponibilidad | Se calculan MTBF, MTTR y disponibilidad utilizando siete días de bitácoras | [Análisis de fiabilidad](analisis_fiabilidad.md) | Pendiente: evidencia temporal insuficiente |
| RNF-06 | Ejecutar controles de calidad en cada push | GitHub Actions ejecuta pruebas, linter y puerta de datos en cada push | [Workflows de GitHub](../../.github/workflows/) | Pendiente de implementar y verificar |
| RNF-07 | Mantener un plan de aseguramiento de calidad | Existe un plan SQA adaptado al proyecto, con estructura basada en IEEE 730 | [COMPLETAR cuando exista el plan] | Pendiente |
| RNF-08 | Documentar tiempos y defectos PSP | Cada integrante conserva registros de esfuerzo y defectos | [Tiempos Nancy](../../calidad/tiempo-nancy.csv) · [Tiempos David](../../calidad/tiempo-david.csv) · [Defectos Nancy](../../calidad/defectos-nancy.csv) · [Defectos David](../../calidad/defectos-david.csv) | Archivos existentes; contenido pendiente de revisión |
| RNF-09 | Demostrar recuperación ante fallos de publicación | Una prueba de fallo controlado conserva o recupera la versión anterior | [Pruebas de publicación](../../tests/test_publicacion.py) | Verificado con una excepción simulada; falta validar recuperación operativa si se exige |

## 4. Relación con los criterios de la rúbrica E1

| Materia | Criterio | Requisitos asociados |
|---|---|---|
| Ingeniería de Datos | Valores faltantes | RF-02, RF-03, RF-06 |
| Ingeniería de Datos | Atípicos y ruido | RF-05 |
| Ingeniería de Datos | Normalización, discretización y reducción | RF-07, RF-08, RF-09 |
| Ingeniería de Datos | Integración de fuentes | RF-10 |
| Ingeniería de Datos | Puerta de calidad | RF-02, RF-03, RF-04, RF-11 |
| Análisis Estadístico | Caracterización y descomposición | RF-14 |
| Análisis Estadístico | Estacionariedad y autocorrelación | RF-14 |
| Análisis Estadístico | Cuatro modelos | RF-14 |
| Análisis Estadístico | Selección por error | RF-14 |
| Análisis Estadístico | Residuos y comunicación | RF-14 |
| Calidad | Fiabilidad y disponibilidad | RNF-05 |
| Calidad | Seguridad | RNF-03, RNF-04, RNF-09 |
| Calidad | Requerimientos | RF-01 a RF-14 y RNF-01 a RNF-09 |
| Calidad | Plan SQA | RNF-07 |
| Calidad | Integración continua | RNF-06 |


## 5. Resultado de la revisión

**Pruebas identificadas:** 85.
**Última ejecución documentada:** 85 aprobadas.
**Cobertura global documentada:** 54%.

La matriz proporciona trazabilidad entre requisitos, criterios de aceptación y evidencias existentes. Los requisitos pendientes permanecen expresamente identificados para evitar declarar cumplimiento sin pruebas suficientes.