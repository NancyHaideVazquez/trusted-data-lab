# Relatoría E1 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima
**Equipo:** Nancy y David
**Periodo documentado:** 11 al 13 de noviembre de 2026, con registros PSP acumulados de etapas anteriores
**Etapa:** E1 — Datos de confianza y pronóstico
**Estado:** versión para revisión conjunta antes de publicarla

## 1. ¿Qué nos propusimos?

El propósito de E1 fue convertir los datos capturados de INEGI y Banxico en información confiable y reproducible, con controles explícitos para valores faltantes, atípicos, transformaciones, integración entre fuentes y rechazo de registros inválidos. También buscamos comparar métodos de pronóstico de series temporales y demostrar prácticas de calidad del software mediante pruebas, seguridad, fiabilidad, requerimientos verificables, plan SQA e integración continua.

Nos propusimos conservar la trazabilidad del dato desde Bronce hasta Plata y Oro, evitando alteraciones silenciosas de las capturas originales.

## 2. ¿Qué hicimos? Cronología del trabajo

### Actividades registradas por Nancy

| Fecha y horario | Fase | Actividad principal |
|---|---|---|
| 11 nov., 20:10–21:10 | Construcción | Estructura E1 e implementación del lector de Bronce, `src/lectura.py`. |
| 11 nov., 21:30–00:30 del 12 nov. | Construcción y pruebas | Limpieza controlada y pruebas en `src/limpieza.py` y `tests/test_limpieza.py` (40 min de interrupción registrados). |
| 12 nov., 09:20–09:40 | Pruebas | Revisión de limpieza con datos reales de INEGI y Banxico. |
| 12 nov., 16:40–18:40 | Construcción y pruebas | Puerta de calidad, `test_calidad.py` y ejecución de validaciones. |
| 12 nov., 18:45–19:44 | Construcción y pruebas | Cuarentena, pruebas, mensajes de rechazo y reporte. |
| 12 nov., 19:50–22:00 | Integración | Orquestación del proceso Bronce → Plata → Oro. |
| 12 nov., 22:05–22:55 | Pruebas | Revisiones de seguridad y fiabilidad. |
| 13 nov., 08:30–10:30 | Estadística | Series temporales, modelos y pronósticos finales. |
| 13 nov., 10:30–11:11 | Calidad | Mejoras y controles de calidad. |

El archivo [tiempo-nancy.csv](../calidad/tiempo-nancy.csv) contiene **27 sesiones acumuladas**, no solo las mostradas en este resumen de E1. Su archivo de defectos contiene **21 registros acumulados**, con numeración consecutiva. No se atribuye a estas sesiones todo el esfuerzo histórico de E1.

### Participación de David

Los registros PSP disponibles de David abarcan **7 sesiones del 6 al 8 de noviembre de 2026**, con **12 horas y 30 minutos** de trabajo y **5 defectos registrados** que suman **90 minutos de corrección**. El registro de tiempo de T14 del 13 de noviembre sigue pendiente de completar y no se incorpora una duración estimada como si fuera observada.

| Fecha y horario | Fase | Actividad registrada |
|---|---|---|
| 6 nov., 16:00–17:00 | Planeación | Clonación del repositorio y creación de rama local. |
| 6 nov., 17:00–19:00 | Código | Investigación de APIs de INEGI y Banxico e identificación de series. |
| 7 nov., 10:00–12:00 | Código | Pruebas del extractor `main.py` y validación de Bronce. |
| 7 nov., 12:00–14:30 | Pruebas | Depuración de URLs de INEGI y Banxico. |
| 7 nov., 15:00–16:00 | Revisión | Pull request y fusión con `main`; revisión de GitHub Actions. |
| 8 nov., 10:00–13:00 | Documentación | Fuentes y objetivos de calidad en `propuesta.md`. |
| 8 nov., 13:00–14:00 | Pruebas | Verificación de GitHub Actions. |

**Trabajo posterior verificado (13 de noviembre):** David amplió las pruebas automatizadas de lectura, modelos estadísticos, análisis de faltantes y estacionariedad, y ejecutores de calidad, Cuarentena, discretización y escalado. La ejecución local final obtuvo **131 pruebas aprobadas y 65 % de cobertura**. Se guardó la evidencia en `docs/E1/evidencia_pruebas_cobertura.txt` y se publicó el commit [`85d6cae`](https://github.com/NancyHaideVazquez/trusted-data-lab/commit/85d6cae) en `e1parte1d`. La integración a `main` y el CI de este commit deben verificarse por separado.

### Actividades de cierre del equipo

Se prepararon la matriz de requerimientos y el plan SQA, se corrigieron las observaciones de Ruff y se verificaron inicialmente **85 pruebas aprobadas**; posteriormente David amplió la batería a **131 pruebas aprobadas y 65 % de cobertura**. El workflow de calidad incorporado en el commit `02dc26e` se observó ejecutado exitosamente en GitHub Actions.

## 3. ¿Qué decidimos y por qué?

**Arquitectura Bronce → Plata → Oro.** Mantuvimos las capturas originales separadas de los resultados tratados para favorecer la trazabilidad y permitir repetir las transformaciones.

**Puerta de calidad con Cuarentena.** Elegimos no descartar silenciosamente registros anómalos: un registro rechazado debe conservarse con su motivo. También diferenciamos la duplicidad de errores de contenido para evitar diagnósticos falsos.

**Tratamiento explícito de faltantes, atípicos y transformaciones.** Documentamos las decisiones y sus comparaciones en vez de aplicar un mismo tratamiento indiscriminadamente a todas las variables.

**Comparación de pronósticos con datos de prueba.** Evaluamos suavizamiento exponencial simple, Holt, Holt-Winters y ARIMA con MAE, RMSE y MAPE, y no únicamente con ajuste dentro de la muestra.

**Selección condicionada por diagnóstico.** Para Banxico, ARIMA(3,0,0) fue el mejor por RMSE, pero no lo declaramos completamente validado porque falló Ljung-Box. Para INEGI, Holt-Winters aditivo presentó el menor RMSE y un diagnóstico residual más favorable en los rezagos examinados.

**Calidad automatizada independiente de capturas.** Incorporamos `.github/workflows/calidad-e1.yml` sin modificar el workflow existente de captura automática. El nuevo flujo ejecuta linter y pruebas para detectar regresiones en los cambios del repositorio.

## 4. ¿Qué salió mal y cómo lo atendimos?

Los registros de Nancy incluyen los siguientes problemas relevantes de E1, entre otros:

| Problema | Acción o estado | Tiempo registrado |
|---|---|---|
| El lector no reconocía la estructura anidada `data.bmx.series.datos` de Banxico. | Se ajustó la lectura y se verificaron 26 archivos. | 15 min |
| El mensaje de Cuarentena era poco claro; después la prueba esperaba el texto anterior. | Se mejoró el motivo de rechazo y se ajustó la prueba. | 5 + 5 min |
| El pipeline no iniciaba correctamente desde Bronce. | Se ajustó su integración. | 20 min |
| La prueba de detención por error estructural requería corrección. | Se revisó el caso de prueba. | 10 min |
| Una transformación provocaba `ValueError` al exigir tres valores distintos. | Se revisó la condición de entrada. | 10 min |
| Un duplicado recibía motivos incorrectos de fuente, periodo, valor y frecuencia. | Se corrigió la asignación de motivos; en la prueba quedaron tres registros válidos y uno rechazado, sin pérdidas. | 15 min |
| Gitleaks no era encontrado por PowerShell tras la instalación. | Se revisó la disponibilidad del ejecutable. | No registrado |
| Gitleaks no podía leer un TOML con marca BOM UTF-8. | Se corrigió la codificación del archivo de configuración. | 18 min |
| ARIMA(3,0,0) no superó Ljung-Box pese a ganar por RMSE. | Se documentó la limitación; no se afirmó que estuviera resuelta. | 5 min de análisis |

La suma de duraciones consignadas para estos incidentes es **103 minutos**, sin incluir el tiempo no registrado de la configuración del ejecutable de Gitleaks. Esta suma no equivale necesariamente al tiempo total de depuración del proyecto. Algunas fechas de los defectos E1 se reconstruyeron correlacionando actividades y sesiones; conviene confirmarlas con el registro original cuando sea posible.

**Defectos registrados por David:** (1) importación incorrecta de `ExtractorEtico`, 15 min; (2) URL de INEGI y parámetro `?type=json`, 30 min; (3) indicador no mensual, 20 min; (4) `.gitignore` impedía incorporar evidencia de Bronce, 10 min; (5) sintaxis del workflow YAML, 15 min. Total: **5 defectos y 90 min** de corrección, según `calidad/defectos-david.csv`. Estos registros corresponden al 7–8 de noviembre y no se atribuyen artificialmente a T14.

**Fiabilidad:** los registros de captura revisados abarcan cinco días distintos, no una ventana completa de siete días, y no muestran fallas observadas. Por ello no presentamos un MTBF o MTTR calculado artificialmente.

## 5. ¿Qué aprendimos?

### Ingeniería de Datos

Aprendimos que tener archivos capturados no garantiza disponer de una fuente homogénea: las estructuras de INEGI y Banxico requieren lectura, validación y armonización diferenciadas. Una Cuarentena útil debe explicar de forma exacta por qué se rechaza cada registro y evitar confundir duplicados con errores de contenido. También reforzamos la importancia de preservar Bronce y de documentar las transformaciones.

### Análisis Estadístico

Aprendimos a separar entrenamiento y prueba, comparar varias familias de modelos y contrastar métricas de error con diagnósticos de autocorrelación de residuos. El mejor RMSE por sí solo no demuestra que un pronóstico cumpla todos los supuestos. Los intervalos y las limitaciones del modelo deben comunicarse junto con los valores centrales.

### Calidad de Software

Aprendimos que los tests, el linter, los controles de dependencias y secretos y la automatización en GitHub Actions aportan evidencias distintas y complementarias. Los registros PSP permiten relacionar actividades con defectos y detectar dónde se invierte esfuerzo. También aprendimos a distinguir entre evidencias disponibles y requisitos aún no demostrados, como los siete días de operación para fiabilidad.

## 6. ¿Cuáles son las evidencias?

- [Documento principal de entrega E1](E1/ENTREGA.md).
- [Análisis del pipeline](E1/analisis_pipeline.md), [integración](E1/analisis_integracion.md) y [puerta de calidad](E1/validacion_calidad.md).
- [Análisis de Cuarentena](E1/analisis_cuarentena.md) y [diagnóstico de calidad](E1/diagnostico_calidad.md).
- [Análisis estadístico](E1/estadistica/analisis_series_temporales.md), [comparación general de modelos](E1/estadistica/comparacion_general_modelos.csv) y [pronósticos finales](E1/estadistica/pronosticos_finales_e1.csv).
- [Plan SQA](E1/plan_sqa.md) y [matriz de requerimientos](E1/matriz_requerimientos.md).
- [Evidencia de pruebas y cobertura](E1/evidencia_pruebas_cobertura.txt), [seguridad](E1/evidencia_seguridad.md) y [fiabilidad](E1/analisis_fiabilidad.md).
- [Workflow de calidad](../.github/workflows/calidad-e1.yml), con ejecución exitosa observada para el commit `02dc26e`.
- [PSP Nancy: tiempo](../calidad/tiempo-nancy.csv) y [defectos](../calidad/defectos-nancy.csv).
- [PSP David: tiempo](../calidad/tiempo-david.csv) y [defectos](../calidad/defectos-david.csv).

## Uso de IA generativa

Se utilizó **ChatGPT** como apoyo para organizar evidencias, revisar comandos y mensajes de herramientas, proponer correcciones de estilo y código, estructurar el reporte y redactar borradores. Las decisiones técnicas, los resultados reportados y la publicación final requieren revisión del equipo. La asistencia de IA no sustituye las pruebas ejecutadas ni la verificación de los archivos del repositorio.

## Pendientes de validación antes del cierre

1. David: completar en `calidad/tiempo-david.csv` las sesiones posteriores al 8 de noviembre con horarios reales; no inventar duraciones.
2. Revisar y aceptar los enlaces relativos tras colocar ambos Markdown en el repositorio.
3. Confirmar URL del tablero y enlace directo a la ejecución de GitHub Actions si se desean incluir.
4. Verificar integración a `main`, resultado de CI para los cambios nuevos y estado de la etiqueta `e1` cuando se realice el cierre.

---

**Documento preparado para compartir y revisión conjunta; no constituye por sí solo una publicación en GitHub.**
