# Plan de Aseguramiento de la Calidad del Software (SQA)

**Proyecto:** Trusted Data Lab
**Observatorio:** Vivienda y Costos de Colima
**Etapa:** E1 — Datos de confianza y pronóstico
**Equipo:** Nancy y David
**Versión del plan:** 1.0
**Fecha:** 13 de noviembre de 2026
**Referencia:** Estructura adaptada de IEEE 730

## 1. Propósito y alcance

El propósito de este plan es establecer los procedimientos, responsabilidades, métricas y evidencias necesarias para asegurar la calidad de Trusted Data Lab durante la etapa E1.

El alcance incluye:

- Extracción y almacenamiento de datos históricos de INEGI y Banco de México.
- Conservación de la capa Bronce.
- Limpieza, transformación, reducción e integración de datos.
- Validación mediante Pandera y separación de Cuarentena.
- Publicación de las capas Plata y Oro.
- Análisis estadístico y pronósticos.
- Pruebas automatizadas, seguridad, fiabilidad e integración continua.
- Documentación de requisitos, defectos, tiempos PSP y entrega.

Este documento describe tanto los controles implementados como los pendientes de verificación. No se considera que un procedimiento esté cumplido únicamente por estar definido en el plan.

## 2. Organización y responsabilidades

| Rol | Responsable |
|---|---|
| Ingeniería de Datos | Nancy |
| Análisis Estadístico | David |
| Aseguramiento de Calidad | Ambos |
| Revisión de la entrega | Ambos |

La asignación de responsabilidades se basa en el Plan de Trabajo realizado por ambos integrantes.

### Revisión cruzada

Cada integrante deberá poder explicar el código, las decisiones y las evidencias del otro.

Antes de publicar la entrega, ambos revisarán los requisitos y registrarán los defectos que encuentren.

## 3. Documentos, normas y referencias

El proyecto utiliza como referencias:

- Documento original del Proyecto Integrador y rúbrica E1.
- Plan de Trabajo E1 del equipo.
- IEEE 730 como referencia para estructurar el aseguramiento de calidad.
- Matriz de requerimientos verificables de E1.
- Diccionario de datos y documentación técnica del pipeline.
- Registros PSP de tiempo y defectos.

### Jerarquía de documentos

En caso de discrepancia, la rúbrica y los requisitos del documento original del Proyecto Integrador tienen prioridad sobre las recomendaciones del Plan de Trabajo.

### Documentos controlados

| Documento | Ruta |
|---|---|
| Matriz de requisitos | [matriz_requerimientos.md](matriz_requerimientos.md) |
| Diccionario de datos | [diccionario_datos.md](diccionario_datos.md) |
| Análisis del pipeline | [analisis_pipeline.md](analisis_pipeline.md) |
| Estadística y pronósticos | [analisis_series_temporales.md](estadistica/analisis_series_temporales.md) |
| Evidencia de pruebas | [evidencia_pruebas_cobertura.txt](evidencia_pruebas_cobertura.txt) |
| Evidencia de seguridad | [evidencia_seguridad.md](evidencia_seguridad.md) |
| Análisis de fiabilidad | [analisis_fiabilidad.md](analisis_fiabilidad.md) |

## 4. Objetivos y atributos de calidad

| Atributo | Objetivo verificable | Método de comprobación |
|---|---|---|
| Integridad | Bronce no cambia durante el procesamiento | Hashes SHA-256 y pruebas |
| Exactitud | Los datos inválidos no se publican como válidos | Validación Pandera |
| Trazabilidad | Cada registro conserva su fuente y serie | Diccionario y pruebas |
| Reproducibilidad | Ejecutar el pipeline con un solo comando | `python -m src.main` |
| Idempotencia | Reejecutar no duplica registros | Prueba automatizada |
| Recuperación | Una falla controlada no destruye las salidas anteriores | Prueba de publicación |
| Seguridad | Detectar secretos y vulnerabilidades conocidas | Gitleaks y pip-audit |
| Fiabilidad | Medir fallos y tiempos de recuperación | Bitácoras de siete días |
| Mantenibilidad | Detectar errores de código y regresiones | Pruebas, linter y revisión |
| Calidad estadística | Justificar modelos, errores e incertidumbre | ADF, ACF/PACF, MAE, RMSE, MAPE y Ljung-Box |

## 5. Procedimientos de aseguramiento de calidad

### 5.1. Control de fuentes y capa Bronce

Las capturas históricas se almacenan en Bronce y no se modifican durante la limpieza o integración.

Se comprueba la integridad mediante hashes SHA-256 y pruebas automatizadas.

**Evidencias:**

- [Hashes de Bronce](hashes_bronce_inicial.csv).
- [Pruebas del pipeline](../../tests/test_pipeline.py).

### 5.2. Limpieza y tratamiento de datos

Se diagnostican valores faltantes, fechas inválidas y observaciones atípicas.

Los valores no publicados por la fuente oficial no se imputan automáticamente sin justificación.

Las observaciones atípicas se marcan para análisis en lugar de eliminarse de manera silenciosa.

**Evidencias:**

- [Análisis de faltantes](analisis_faltantes.md).
- [Análisis de atípicos](analisis_atipicos.md).
- [Pruebas de limpieza](../../tests/test_limpieza.py).

### 5.3. Transformación e integración

Se utilizan técnicas Min-Max, Z-score, discretización y reducción de frecuencia.

Las fuentes se integran respetando identificadores y unidades originales.

**Evidencias:**

- [Escalado](analisis_escalado.md).
- [Discretización](analisis_discretizacion.md).
- [Reducción](analisis_reduccion.md).
- [Integración](analisis_integracion.md).

### 5.4. Puerta de calidad y Cuarentena

La puerta de calidad utiliza Pandera para comprobar estructura, campos requeridos, frecuencia, periodos, valores finitos y unicidad.

Los registros inválidos identificables se envían a Cuarentena, conservando el motivo del rechazo.

Los errores estructurales que impiden procesar los datos de forma segura detienen el pipeline.

**Evidencias:**

- [Código de validación](../../src/calidad.py).
- [Código de Cuarentena](../../src/cuarentena.py).
- [Pruebas de Cuarentena](../../tests/test_cuarentena.py).

### 5.5. Publicación de Plata y Oro

La publicación debe realizarse únicamente después de superar las comprobaciones correspondientes.

Los archivos originales de Bronce no se sobrescriben.

Se ejecutan pruebas de recuperación ante excepciones durante la publicación. Estas pruebas no demuestran por sí solas recuperación completa frente a cualquier fallo operativo.

**Evidencias:**

- [Pruebas de publicación](../../tests/test_publicacion.py).
- [Documentación del pipeline](analisis_pipeline.md).

### 5.6. Análisis estadístico

El análisis estadístico debe conservar:

1. Caracterización y descomposición interpretadas.
2. Dickey-Fuller, ACF y PACF.
3. Suavizamiento exponencial simple, Holt, Holt-Winters y ARIMA.
4. Comparación en datos de prueba con MAE, RMSE y MAPE.
5. Ljung-Box e intervalos de pronóstico explicados.

La selección de modelos se realiza utilizando datos de prueba que no intervinieron en el ajuste.

**Evidencia:** [Análisis estadístico E1](estadistica/analisis_series_temporales.md).

La TIIE mantiene autocorrelación residual significativa bajo ARIMA(3,0,0); esta limitación se declara explícitamente.

## 6. Verificación, validación y pruebas

### 6.1. Pruebas automatizadas

Se utiliza pytest para comprobar componentes del pipeline y la publicación.

**Última ejecución documentada:** 85 pruebas aprobadas.

**Cobertura global documentada:** 54%.

Comando de verificación:

```powershell
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

La cobertura se utiliza como indicador de áreas que requieren pruebas adicionales. No se interpreta como una garantía de ausencia de defectos.

### 6.2. Revisión estática

Se deberán ejecutar comprobaciones de sintaxis y un linter sobre los archivos Python.

**Estado:** la revisión de sintaxis de los scripts estadísticos se realizó mediante `compileall`; la integración del linter en CI está pendiente de verificar.

### 6.3. Integración continua

El objetivo es que cada push ejecute automáticamente:

- Pruebas pytest.
- Linter de Python.
- Puerta de calidad de datos con una comprobación reproducible.

**Criterio de aceptación:** una falla en cualquiera de estas comprobaciones debe impedir que el workflow termine con estado satisfactorio.

**Estado:** pendiente de implementar y demostrar mediante un workflow de GitHub Actions.

### 6.4. Revisión cruzada

Antes de la entrega, ambos integrantes deberán:

- Ejecutar el pipeline y las pruebas.
- Revisar los cambios de código.
- Comprobar que las evidencias enlazadas existen.
- Explicar una decisión técnica y una corrección del otro integrante.

**Registro de revisión:** [COMPLETAR fecha y evidencia real].

## 7. Seguridad

### 7.1. Auditoría de dependencias

Se utiliza `pip-audit` para detectar vulnerabilidades conocidas en las dependencias analizadas.

**Resultado documentado:** no se encontraron vulnerabilidades conocidas.

### 7.2. Detección de secretos

Se utiliza Gitleaks para revisar el historial del repositorio y los archivos pertinentes.

El análisis documentado del historial Git no encontró secretos. El escaneo de directorio se repitió con exclusiones explícitas para dependencias del entorno virtual y el archivo local `.env`.

No se debe interpretar ese resultado como una comprobación completa de todos los archivos privados locales.

**Evidencia:** [Auditorías de seguridad](evidencia_seguridad.md).

### 7.3. Respaldo y recuperación

El proceso de publicación incluye mecanismos de respaldo y recuperación frente a fallos controlados.

La prueba de publicación simula una excepción y verifica la recuperación de archivos.

**Evidencia:** [test_recuperacion_si_falla_publicacion](../../tests/test_publicacion.py).

## 8. Fiabilidad y disponibilidad

La rúbrica E1 solicita medir:

- Tiempo medio entre fallos (MTBF).
- Tiempo medio de recuperación (MTTR).
- Disponibilidad.
- Evidencia basada en siete días de bitácoras.

En la revisión documentada se identificaron 24 capturas exitosas distribuidas en cinco días distintos.

La ausencia de fallos registrados no es suficiente para determinar el MTBF o el MTTR.

Tampoco es válido inferir disponibilidad continua a partir de la proporción de capturas exitosas.

**Estado:** requisito pendiente de completar con mediciones reales.

**Evidencia:** [Análisis de fiabilidad](analisis_fiabilidad.md).

## 9. Gestión de defectos y acciones correctivas

Los defectos deben registrarse utilizando los archivos PSP del equipo.

Cada registro debe identificar, cuando corresponda:

- Número de defecto.
- Fecha de detección.
- Componente afectado.
- Tipo de defecto.
- Actividad en la que se detectó.
- Tiempo dedicado a la corrección.
- Descripción y acción correctiva.

Los problemas detectados durante el desarrollo deben relacionarse con sus pruebas de regresión y commits cuando exista evidencia.

### Registros existentes

- [Defectos Nancy](../../calidad/defectos-nancy.csv).
- [Defectos David](../../calidad/defectos-david.csv).
- [Tiempo Nancy](../../calidad/tiempo-nancy.csv).
- [Tiempo David](../../calidad/tiempo-david.csv).

**Pendiente:** comprobar que todos los registros estén actualizados y que sus identificadores coincidan con la relatoría.

## 10. Gestión de configuración y cambios

El proyecto utiliza Git y GitHub para conservar el historial del código y la documentación.

Se mantienen ramas de trabajo e integraciones mediante Pull Requests cuando corresponde.

Los cambios deben someterse a pruebas y revisión antes de considerarse aprobados para la entrega.

Las capturas automáticas pueden agregar nuevos archivos a Bronce. Esos cambios deben preservarse durante la integración de ramas.

### Control de versiones

Cada entrega debe disponer de:

- Código y documentación versionados.
- Evidencias de pruebas.
- Revisión del estado del repositorio.
- Identificación del commit de entrega.
- Etiqueta de etapa, creada únicamente después de aprobar la revisión final.

## 11. Registros y evidencias de calidad

| Registro | Ubicación | Uso |
|---|---|---|
| Pruebas y cobertura | [evidencia_pruebas_cobertura.txt](evidencia_pruebas_cobertura.txt) | Verificación automatizada |
| Seguridad | [evidencia_seguridad.md](evidencia_seguridad.md) | Auditoría de dependencias y secretos |
| Fiabilidad | [analisis_fiabilidad.md](analisis_fiabilidad.md) | Seguimiento de capturas y limitaciones |
| Requisitos | [matriz_requerimientos.md](matriz_requerimientos.md) | Trazabilidad y aceptación |
| Estadística | [estadistica/analisis_series_temporales.md](estadistica/analisis_series_temporales.md) | Modelos y diagnósticos |
| PSP | [Carpeta calidad](../../calidad/) | Tiempos y defectos |
| Capturas | [logs/capturas.csv](../../logs/capturas.csv) | Bitácora de capturas |

## 12. Riesgos y medidas de mitigación

| Riesgo | Impacto | Medida de mitigación |
|---|---|---|
| Modificación accidental de Bronce | Pérdida de trazabilidad | Lectura controlada y verificación SHA-256 |
| Datos inválidos publicados | Resultados incorrectos | Pandera y Cuarentena |
| Pérdida de salidas durante publicación | Interrupción del servicio | Respaldos y pruebas de recuperación |
| Cambios sin pruebas | Regresiones | pytest e integración continua |
| Secretos expuestos | Compromiso de credenciales | Gitleaks y archivos privados fuera de Git |
| Dependencias vulnerables | Riesgos de seguridad | Auditoría pip-audit |
| Pronósticos poco confiables | Interpretación incorrecta | Evaluación en datos de prueba, Ljung-Box y comunicación de incertidumbre |
| Bitácoras insuficientes | Incumplimiento de la rúbrica de fiabilidad | Recopilar siete días reales de registros |
| Conflictos de Git | Pérdida de trabajo | Revisar diferencias y actualizar antes de publicar |

## 13. Auditorías y revisiones

La revisión de calidad de E1 deberá comprobar:

| Control | Evidencia requerida | Estado |
|---|---|---|
| Integridad de Bronce | Hashes y pruebas | Verificado |
| Puerta de datos | Pandera y Cuarentena | Verificado |
| Integración y publicación | Pruebas y salidas | Verificado |
| Pruebas automatizadas | pytest | Verificado: 85 aprobadas |
| Seguridad | Gitleaks y pip-audit | Revisado con las limitaciones documentadas |
| Respaldo y recuperación | Prueba de fallo controlado | Verificado en prueba automatizada |
| Modelos estadísticos | Métricas y diagnósticos | Ejecutados; Banxico con autocorrelación residual |
| Fiabilidad de siete días | MTBF, MTTR y disponibilidad | Pendiente |
| CI con pruebas, linter y puerta de datos | Ejecución satisfactoria de GitHub Actions | Pendiente |
| Registros PSP completos | CSV de ambos integrantes | Pendiente de revisión |
| Revisión cruzada | Evidencia de ambos integrantes | Pendiente |

## 14. Criterios de aprobación de la entrega

La entrega E1 podrá considerarse revisada cuando:

1. Los archivos de Bronce permanezcan íntegros.
2. El pipeline genere resultados válidos en Plata y Oro.
3. Las reglas de calidad y Cuarentena funcionen.
4. Los resultados estadísticos sean reproducibles y estén interpretados.
5. Las pruebas automatizadas terminen correctamente.
6. La revisión de seguridad esté documentada y sin hallazgos abiertos en el alcance requerido.
7. El respaldo y la recuperación estén probados.
8. Los requerimientos tengan criterios de aceptación y evidencia vinculada.
9. El workflow de CI ejecute pruebas, linter y puerta de datos en cada push.
10. Se disponga de la evidencia de fiabilidad exigida por la rúbrica.
11. Los CSV PSP estén actualizados y revisados.
12. Ambos integrantes aprueben la revisión final.
13. La ficha `ENTREGA.md` y la relatoría estén completas y enlacen las evidencias.

**No se creará la etiqueta `e1` mientras existan criterios críticos sin revisar.**

## 15. Aprobación y mantenimiento del plan

Este plan deberá actualizarse cuando cambien los requisitos, los mecanismos de validación, el workflow de CI o los criterios de aprobación.

| Integrante | Responsabilidad de aprobación | Estado |
|---|---|---|
| Nancy | Revisión técnica de ingeniería y pruebas | Pendiente de confirmación |
| David | Revisión estadística y documentación | Pendiente de confirmación |

**Estado del documento:** borrador adaptado al proyecto; pendiente de revisión y aprobación del equipo.