# Observatorio de Vivienda y Costos de Colima

**Proyecto Integrador · TRUSTED DATA LAB**
**Materias:** Ingeniería de Datos, Análisis Estadístico y Calidad en los Sistemas de Información.

## Descripción

Este proyecto desarrolla un observatorio de datos sobre la evolución de los costos asociados a la vivienda en Colima y Villa de Álvarez mediante la recopilación, procesamiento y análisis de información económica de fuentes oficiales.

**Pregunta central:** ¿Cómo evolucionan los costos económicos relacionados con la vivienda y las condiciones de financiamiento, y qué información pública permite describir las características y diferencias de vivienda entre Colima, Villa de Álvarez y otras zonas comparables?

El observatorio estudia series históricas e indicadores relacionados con la inflación, los servicios asociados a la vivienda y el costo del crédito. Los indicadores disponibles no sustituyen mediciones directas de rentas o precios inmobiliarios donde estas no existan en las fuentes consultadas.

## Objetivo general

Desarrollar un observatorio que integre información económica oficial, aplique técnicas estadísticas para identificar tendencias y producir pronósticos, y aporte trazabilidad y confiabilidad mediante validación y aseguramiento de calidad.

## Fuentes de datos

- **INEGI:** API de Indicadores; información histórica económica, incluida la serie de inflación analizada en E1.
- **Banco de México (Banxico):** API del Sistema de Información Económica (SIE); indicadores financieros, incluida la TIIE analizada en E1.

Las capturas originales se conservan en Bronce y se atribuyen a las instituciones de origen.

## Tecnologías

- Python 3.11, Requests y Pandas.
- Pandera para validación de estructuras y reglas de datos.
- Statsmodels para análisis de series temporales y pronósticos.
- Pytest y pytest-cov para pruebas y cobertura.
- Ruff para revisión estática de código.
- Git, GitHub y GitHub Actions para versionado y automatización.
- Gitleaks y pip-audit para revisiones de secretos y dependencias.

Las dependencias declaradas del proyecto están en [`requirements.txt`](requirements.txt).

## Arquitectura de datos

El proyecto utiliza un flujo de procesamiento **Bronce → Plata → Oro**, con una **Cuarentena** para los registros que incumplen reglas de calidad.

| Capa o componente | Función |
|---|---|
| **Bronce** | Conserva archivos originales y metadatos de las capturas para trazabilidad. |
| **Plata** | Contiene datos limpios, armonizados y validados procedentes de las fuentes oficiales. |
| **Oro** | Publica datos integrados y preparados para consumo analítico. |
| **Cuarentena** | Separa registros rechazados y registra sus motivos sin mezclarlos con los datos válidos. |
| **Reportes y pruebas** | Documentan diagnósticos, reglas de calidad, modelos y verificaciones reproducibles. |

### Estructura principal del repositorio

```text
trusted-data-lab/
├── .github/
│   └── workflows/
│       ├── captura.yml
│       └── calidad-e1.yml
├── calidad/
│   ├── tiempo-nancy.csv
│   ├── defectos-nancy.csv
│   ├── tiempo-david.csv
│   └── defectos-david.csv
├── data/
│   ├── bronce/
│   ├── plata/
│   ├── oro/
│   └── cuarentena/
├── docs/
│   ├── E0/
│   ├── E1/
│   │   ├── estadistica/
│   │   ├── plan_sqa.md
│   │   ├── matriz_requerimientos.md
│   │   └── ENTREGA.md          # Documento de cierre E1
│   └── relatoria-E1.md         # Documento de cierre E1
├── extractores/
├── src/
├── tests/
├── logs/
│   └── capturas.csv
├── requirements.txt
├── .env.example
└── README.md
```

Los documentos de cierre de E1 se encuentran enlazados a continuación. Su presencia y los enlaces relativos deben verificarse en la rama de trabajo antes del cierre.

## Requisitos e instalación

- Python 3.11 y Git.
- Acceso a Internet y tokens vigentes de las APIs para realizar nuevas capturas.
- No se requieren tokens para ejecutar las pruebas que usan datos de prueba y recursos locales.

Clonar el repositorio:

```bash
git clone https://github.com/NancyHaideVazquez/trusted-data-lab.git
cd trusted-data-lab
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo en **PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

En **Linux o macOS**:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuración y seguridad

Para realizar capturas locales, crear un archivo `.env` privado en la raíz, tomando `.env.example` como referencia:

```dotenv
INEGI_TOKEN=REEMPLAZAR_CON_TOKEN_REAL
BANXICO_TOKEN=REEMPLAZAR_CON_TOKEN_REAL
TDL_CONTACTO=correo-del-equipo@ejemplo.org
```

En GitHub, los tokens se almacenan como **Actions Secrets** (`INEGI_TOKEN` y `BANXICO_TOKEN`), y `TDL_CONTACTO` se configura como variable, según la configuración del workflow de captura.

**Nunca publicar** `.env`, tokens, credenciales o URLs que contengan secretos. Las revisiones con Gitleaks y pip-audit están documentadas en [Evidencia de seguridad E1](docs/E1/evidencia_seguridad.md).

## Captura y procesamiento

Ejecutar la captura con los extractores configurados:

```bash
python -m extractores.main
```

Solicitar descarga histórica disponible:

```bash
python -m extractores.main --historico
```

Las respuestas se almacenan bajo `data/bronce/`, y las ejecuciones se registran en [`logs/capturas.csv`](logs/capturas.csv). Una captura exitosa no significa que la fuente haya publicado un nuevo periodo.

El procesamiento posterior realiza diagnóstico, limpieza, integración, validación y publicación a Plata y Oro. La arquitectura y las etapas implementadas se explican en:

- [Análisis del pipeline E1](docs/E1/analisis_pipeline.md).
- [Integración de fuentes](docs/E1/analisis_integracion.md).
- [Validación de calidad](docs/E1/validacion_calidad.md).
- [Análisis de Cuarentena](docs/E1/analisis_cuarentena.md).

## Automatización con GitHub Actions

### Captura de fuentes

El workflow [`captura.yml`](.github/workflows/captura.yml) permite la ejecución programada y manual de los extractores, registra resultados y puede incorporar nuevas capturas al repositorio. En la configuración trabajada en E1, la programación es `*/5 * * * *` (cada cinco minutos en UTC); GitHub Actions no garantiza una ejecución exacta al minuto.

### Integración continua de calidad

El workflow [`calidad-e1.yml`](.github/workflows/calidad-e1.yml) se activa mediante `push`, `pull_request` o ejecución manual. Comprueba:

1. **Ruff** sobre `src` y `tests`.
2. **Pytest** sobre `tests/`.
3. **Pruebas de la puerta de calidad**, incluidas validaciones de datos, Cuarentena y pipeline.

La ejecución **Calidad E1 - Trusted Data Lab #1**, asociada al commit `02dc26e`, se observó completada satisfactoriamente en GitHub Actions. Esto demuestra la ejecución del workflow, sin implicar una auditoría exhaustiva de todas las capturas históricas.

Pruebas locales verificadas durante E1:

```bash
python -m ruff check src tests --output-format concise
python -m pytest tests/ -q
```

**Resultado local actualizado (13 de noviembre): 131 pruebas aprobadas y 65 % de cobertura de `src`**, superior a la meta del 60 %. Evidencia en [`docs/E1/evidencia_pruebas_cobertura.txt`](docs/E1/evidencia_pruebas_cobertura.txt), commit [`85d6cae`](https://github.com/NancyHaideVazquez/trusted-data-lab/commit/85d6cae) de `e1parte1d`. Ruff sin observaciones corresponde a la verificación anterior; la integración a `main` y el CI del nuevo commit están pendientes de comprobar.

## Resultados de Ingeniería de Datos · E1

Se desarrollaron los siguientes trabajos:

- Diagnóstico de valores faltantes y decisiones de tratamiento.
- Identificación y evaluación de valores atípicos y ruido.
- Escalado, discretización y reducción de datos con análisis comparativos.
- Integración de datos de INEGI y Banxico, con armonización de esquemas y valores.
- Puerta de calidad automatizada con Cuarentena y motivos de rechazo.
- Trazabilidad de archivos originales mediante huellas SHA-256.

**Evidencias:** [Faltantes](docs/E1/analisis_faltantes.md) · [Atípicos](docs/E1/analisis_atipicos.md) · [Escalado](docs/E1/analisis_escalado.md) · [Discretización](docs/E1/analisis_discretizacion.md) · [Reducción](docs/E1/analisis_reduccion.md) · [Diccionario de datos](docs/E1/diccionario_datos.md).

## Resultados de Análisis Estadístico · E1

Se analizaron series mensuales de **TIIE de Banxico** e **inflación de INEGI**, con descomposición temporal, pruebas ADF, gráficas ACF/PACF y comparación de cuatro familias de pronóstico: suavizamiento exponencial simple, Holt, Holt-Winters y ARIMA. La selección se apoyó en MAE, RMSE y MAPE sobre datos de prueba, y se examinaron los residuos mediante Ljung-Box.

| Serie | Modelo con menor RMSE de prueba | RMSE aproximado | Diagnóstico de residuos |
|---|---|---:|---|
| Banxico, TIIE | ARIMA(3,0,0) | 1.7604 | Ljung-Box no superado; autocorrelación residual pendiente. |
| INEGI, inflación | Holt-Winters aditivo | 0.0986 | Sin evidencia significativa de autocorrelación en los rezagos examinados. |

Los pronósticos e intervalos expresan incertidumbre y no son garantías de evolución futura. En particular, los límites inferiores negativos del pronóstico ARIMA de Banxico son artefactos posibles del modelo y requieren cautela interpretativa.

**Evidencias:** [Análisis estadístico](docs/E1/estadistica/analisis_series_temporales.md) · [Comparación de modelos](docs/E1/estadistica/comparacion_general_modelos.csv) · [Pronósticos finales](docs/E1/estadistica/pronosticos_finales_e1.csv).

## Calidad y fiabilidad · E1

- [Matriz de requerimientos verificables](docs/E1/matriz_requerimientos.md).
- [Plan SQA adaptado a IEEE 730](docs/E1/plan_sqa.md).
- [Evidencia de pruebas y cobertura](docs/E1/evidencia_pruebas_cobertura.txt).
- [Evidencia de seguridad](docs/E1/evidencia_seguridad.md).
- [Análisis de fiabilidad](docs/E1/analisis_fiabilidad.md).
- Registros PSP de tiempo y defectos en [`calidad/`](calidad/), mantenidos por Nancy y David.

**Metas iniciales de calidad** (no todas acreditadas como resultados): disponibilidad de captura ≥ 95 %, completitud de datos ≥ 95 %, cobertura automatizada ≥ 60 % y ausencia de credenciales expuestas en el repositorio.

**Limitación de fiabilidad:** hasta la revisión de E1 se contaba con registros de capturas exitosas en **cinco días distintos**, no en los siete días exigidos por la rúbrica. Al no observarse fallas en esa ventana, no se presentan valores inventados de MTBF o MTTR.

## Extracción ética y trazabilidad

El módulo `extractores/base.py` contempla consultas HTTPS, identificación mediante User-Agent y contacto del equipo, pausas entre solicitudes, reintentos limitados ante errores transitorios y protección de tokens en URLs registradas. Las consultas se realizan a las APIs oficiales.

La revisión de `robots.txt` y de términos de uso de las instituciones no constituye autorización general para realizar cualquier extracción. Se mantiene la atribución a INEGI y Banco de México.

## Documentación y entregas

### E0 · Arranque

- [Propuesta del observatorio](docs/E0/propuesta.md).
- [Relatoría E0](docs/E0/relatoria-E0.md).
- [Ficha de entrega E0](docs/E0/ENTREGA.md).

La entrevista de campo se realizó mediante WhatsApp con una persona del sector inmobiliario, según la documentación de E0.

### E1 · Datos de confianza y pronóstico

- [Ficha de entrega E1](docs/E1/ENTREGA.md) — documento actualizado para revisión del equipo.
- [Relatoría E1](docs/relatoria-E1.md) — documento actualizado para revisión del equipo.
- [Análisis del pipeline](docs/E1/analisis_pipeline.md).
- [Análisis de series temporales](docs/E1/estadistica/analisis_series_temporales.md).
- [Plan SQA](docs/E1/plan_sqa.md).

### Calendario académico

| Entrega | Fecha de referencia (2026) | Objetivo |
|---|---|---|
| **E0 — Arranque** | 6 de noviembre | Propuesta, entrevista, fuentes, histórico y automatización inicial. |
| **E1 — Datos de confianza y pronóstico** | 13 de noviembre | Limpieza, integración, capas Plata y Oro, pronósticos, seguridad y calidad. |
| **E2 — Experimento y auditoría** | 23 de noviembre | Fuente especializada, experimento factorial, ANOVA y auditoría cruzada. |
| **E3 — Mapa multivariado y sello** | 30 de noviembre | PCA, MANOVA, mapa multivariado, publicación y auditoría. |
| **E4 — Demo Day y cierre** | 2 y 4 de diciembre | Demostración, reportes finales, modelo de negocio y video. |

Cada entrega debe conservar evidencias de las tres materias. Cuando corresponda, el equipo creará la etiqueta Git de cierre (`e0`, `e1`, `e2`, `e3`, `e4`); **no se da por creada la etiqueta `e1` en este documento**.

## Integrantes

- **Nancy:** Data Engineer.
- **David:** Data Statistician.

Ambos integrantes participan en actividades de calidad, pruebas, documentación y revisión cruzada.

## Estado del proyecto

**Etapa actual: revisión y cierre documental de E1 (13 de noviembre de 2026).**

Se implementaron las capas Bronce, Plata, Oro y Cuarentena, se generaron análisis y pronósticos de dos series temporales, se aprobaron **131 pruebas locales con 65 % de cobertura** (commit `85d6cae` en `e1parte1d`) y se verificó anteriormente una ejecución satisfactoria del workflow de Calidad E1 (commit `02dc26e`). Continúan pendientes la revisión conjunta de los documentos de cierre, la integración a `main`, la comprobación del CI actualizado, el registro de tiempo posterior de David, la etiqueta `e1` y las limitaciones declaradas de fiabilidad y residuos de Banxico.

---

**Proyecto académico — TRUSTED DATA LAB, noviembre-diciembre de 2026.**
