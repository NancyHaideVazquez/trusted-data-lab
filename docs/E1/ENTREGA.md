# Entrega E1 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima
**Equipo:** Nancy y David
**Etapa:** E1 — Datos de confianza y pronóstico
**Fecha de preparación:** 13 de noviembre de 2026
**Rama de trabajo para las pruebas ampliadas:** `e1parte1d` (integración a `main` pendiente de verificar)
**Commit de integración continua previamente verificado:** `02dc26e`
**Commit de ampliación de pruebas (David):** `85d6cae`
**Etiqueta `e1`:** pendiente de confirmación al cerrar la entrega
**Tablero público:** [agregar URL verificada, si aplica]

## 1. Resumen ejecutivo

En E1 se trabajó con datos de INEGI y Banxico para construir un flujo trazable **Bronce → Plata → Oro**, con diagnósticos, transformaciones, integración, validaciones de calidad y separación de registros rechazados en Cuarentena. Se preservó la evidencia de la capa Bronce mediante hashes SHA-256.

Se analizaron las series temporales de inflación de INEGI y TIIE de Banxico, incluyendo descomposición, ADF, ACF, PACF, comparación de cuatro familias de pronóstico y diagnóstico de residuos.

En Calidad se incorporaron pruebas automatizadas, linting, documentación de seguridad, análisis de fiabilidad, matriz de requerimientos, plan SQA y un workflow de GitHub Actions. Se registran también limitaciones que no deben presentarse como criterios cumplidos.

## 2. Ingeniería de Datos

| Criterio E1 | Evidencias del repositorio | Estado y resultado |
|---|---|---|
| Valores faltantes | [Análisis de faltantes](analisis_faltantes.md) | Diagnóstico y decisiones de tratamiento documentadas. |
| Atípicos y ruido | [Análisis de atípicos](analisis_atipicos.md) | Detección, clasificación y decisiones documentadas. |
| Normalización, discretización y reducción | [Escalado](analisis_escalado.md) · [Discretización](analisis_discretizacion.md) · [Reducción](analisis_reduccion.md) | Evidencia separada de las tres técnicas y sus análisis. |
| Integración de fuentes | [Integración](analisis_integracion.md) · [Diccionario de datos](diccionario_datos.md) | Armonización de estructuras y valores; revisión de duplicados. |
| Puerta de calidad y Cuarentena | [Validación](validacion_calidad.md) · [Cuarentena](analisis_cuarentena.md) · [Diagnóstico](diagnostico_calidad.md) | Validaciones automáticas y motivos para registros rechazados. |

**Trazabilidad complementaria:** [Pipeline](analisis_pipeline.md), [huellas SHA-256 de Bronce](hashes_bronce_inicial.csv) y [análisis de integración](analisis_integracion.md).

En la ejecución válida revisada, Cuarentena quedó vacía. Esto no impide probar sus reglas con registros inválidos y duplicados en pruebas automatizadas; no debe interpretarse que necesariamente existieron rechazos reales en esa ejecución.

## 3. Estadística

| Criterio E1 | Evidencias del repositorio | Resultado |
|---|---|---|
| Caracterización y descomposición | [Análisis de series temporales](estadistica/analisis_series_temporales.md) · [Gráfico TIIE](estadistica/banxico_tiie_descomposicion.png) · [Gráfico INEGI](estadistica/inegi_inflacion_descomposicion.png) | Series y descomposiciones estudiadas. |
| Estacionariedad y autocorrelación | [ADF Banxico](estadistica/banxico_tiie_adf.txt) · [ADF INEGI](estadistica/inegi_inflacion_adf.txt) · [ACF TIIE](estadistica/banxico_tiie_acf_original.png) · [PACF INEGI](estadistica/inegi_inflacion_pacf_original.png) | Pruebas e interpretación documentadas. |
| Cuatro modelos | [Análisis estadístico](estadistica/analisis_series_temporales.md) | Suavizamiento exponencial simple, Holt, Holt-Winters y ARIMA. |
| Selección por error | [Comparación general](estadistica/comparacion_general_modelos.csv) · [Métricas Banxico](estadistica/banxico_tiie_metricas.csv) · [Métricas INEGI](estadistica/inegi_inflacion_metricas.csv) | Comparación fuera de muestra usando MAE, RMSE y MAPE. |
| Residuos e intervalos | [Análisis estadístico](estadistica/analisis_series_temporales.md) · [Pronósticos consolidados](estadistica/pronosticos_finales_e1.csv) | Diagnóstico Ljung-Box y pronósticos con incertidumbre; limitación en Banxico. |

### Resultados representativos

- **Banxico, TIIE:** ARIMA(3,0,0) obtuvo el menor RMSE de prueba, **1.7604** aproximadamente. No obstante, los residuos **no superaron Ljung-Box** en los rezagos evaluados; el pronóstico debe interpretarse con esa advertencia. [Pronóstico CSV](estadistica/banxico_tiie_pronostico_final.csv) · [Gráfico](estadistica/banxico_tiie_pronostico_final.png) · [Evaluación SARIMA adicional](estadistica/banxico_evaluacion_sarima.csv).
- **INEGI, inflación:** Holt-Winters aditivo obtuvo el menor RMSE, **0.0986** aproximadamente; el diagnóstico Ljung-Box no mostró autocorrelación residual significativa en los rezagos revisados. [Pronóstico CSV](estadistica/inegi_inflacion_pronostico_final.csv) · [Gráfico](estadistica/inegi_inflacion_pronostico_final.png).

Los intervalos expresan incertidumbre del método empleado y no son garantías sobre el futuro.

## 4. Calidad de Software

| Criterio E1 | Evidencias del repositorio | Estado |
|---|---|---|
| Fiabilidad y disponibilidad | [Análisis de fiabilidad](analisis_fiabilidad.md) · [Capturas](../../logs/capturas.csv) | **Parcial:** registros observados de cinco días distintos, no siete días completos; sin fallas observadas para estimar MTBF y MTTR de modo informativo. |
| Seguridad | [Evidencia de seguridad](evidencia_seguridad.md) | Revisiones documentadas de Gitleaks y pip-audit; consultar el documento para alcance y resultados. |
| Requerimientos verificables | [Matriz de requerimientos](matriz_requerimientos.md) | Vínculos entre requisitos y evidencias/pruebas. |
| Plan SQA | [Plan SQA](plan_sqa.md) | Plan adaptado con referencia a IEEE 730. |
| Integración continua | [Workflow](../../.github/workflows/calidad-e1.yml) · [Pruebas y cobertura](evidencia_pruebas_cobertura.txt) | **Ejecución exitosa observada** en GitHub Actions del workflow *Calidad E1 - Trusted Data Lab* asociado al commit `02dc26e`. |

En la verificación local más reciente (13 de noviembre de 2026) se observaron **131 pruebas aprobadas y 65 % de cobertura de `src`** (1140 sentencias, 400 no cubiertas), superando la meta de 60 %. La evidencia está en `evidencia_pruebas_cobertura.txt`, registrada en el commit `85d6cae` de la rama `e1parte1d`. Las comprobaciones de Ruff y `git diff --check` sin errores corresponden a la verificación anterior; no se afirma que el nuevo commit haya superado CI hasta verificar su ejecución. El workflow contiene pasos para Ruff, pytest y pruebas de la puerta de calidad con Pandera/Cuarentena. La comprobación automatizada de casos de prueba **no equivale a validar todo el histórico real de Bronce en cada push**.

### Evidencia de proceso personal (PSP)

- [Tiempo de Nancy](../../calidad/tiempo-nancy.csv) · [Defectos de Nancy](../../calidad/defectos-nancy.csv).
- [Tiempo de David](../../calidad/tiempo-david.csv) · [Defectos de David](../../calidad/defectos-david.csv).

Los archivos de Nancy contienen 27 registros de tiempo y 21 defectos acumulados hasta la revisión informada. Algunas fechas de defectos de E1 se reconstruyeron a partir de su cronología de trabajo.

## 5. Limitaciones y pendientes declarados

1. **Fiabilidad:** la evidencia disponible no acredita todavía siete días completos de operación. La ausencia de fallas impide estimar MTBF y MTTR observados de manera informativa. No se asignan valores ficticios.
2. **Banxico:** el modelo seleccionado por RMSE no satisfizo el diagnóstico de independencia de residuos de Ljung-Box; se mantiene como una limitación estadística.
3. **Pruebas y seguridad:** las comprobaciones se refieren al alcance y fecha de las evidencias documentadas, no a garantías absolutas de ausencia de defectos o vulnerabilidades.
4. **Cierre de entrega:** verificar el enlace del tablero, la versión final de la relatoría y la etiqueta `e1` antes de publicarlas como definitivas.

## 6. Relatoría y entregables

- [Relatoría E1](../relatoria-E1.md).
- [Matriz de requerimientos](matriz_requerimientos.md).
- [Plan SQA](plan_sqa.md).
- [Evidencias estadísticas](estadistica/analisis_series_temporales.md).

## 7. Control de versiones

El commit `02dc26e` registra el workflow de calidad E1, la matriz de requerimientos, el plan SQA y correcciones de Ruff. La ejecución general de GitHub Actions asociada al commit se observó exitosa.

**Actualización del 13 de noviembre:** David registró 131 pruebas aprobadas y 65 % de cobertura en el commit [`85d6cae`](https://github.com/NancyHaideVazquez/trusted-data-lab/commit/85d6cae), publicado en `e1parte1d`. Su PSP disponible documenta 7 sesiones (12 h 30 min) y 5 defectos (90 min de corrección) correspondientes al 6–8 de noviembre; el tiempo de T14 posterior sigue pendiente de registro.

**Pendiente para el equipo:** integrar los documentos en sus rutas, revisar enlaces en GitHub, verificar la integración de `e1parte1d` a `main` y el CI correspondiente, completar el PSP posterior de David y crear/verificar la etiqueta `e1` únicamente al finalizar el cierre.
