# Entrega E2 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima

**Equipo:** David Cuevas Farías y Nancy Haide Vázquez Ávalos

**Etapa:** E2 — Procesamiento geoespacial, trazabilidad y ética de datos

**Fecha de preparación:** 22 de noviembre de 2026

**Rama de trabajo:** `e2david`

**Repositorio:** https://github.com/NancyHaideVazquez/trusted-data-lab

---

## 1. Resumen ejecutivo

Durante la etapa E2 del proyecto Trusted Data Lab se fortaleció el Observatorio de Vivienda y Costos de Colima mediante la incorporación de información geográfica oficial, el procesamiento de datos municipales, la integración de indicadores económicos y la implementación de mecanismos de trazabilidad y calidad.

Se incorporó información del Marco Geoestadístico municipal 2026 del INEGI, se procesaron los límites de los diez municipios del estado de Colima y se generó un mapa que destaca los municipios de Colima y Villa de Álvarez.

También se fortaleció la arquitectura Bronce–Plata–Oro, incorporando mecanismos para identificar el origen de los registros y conservar la reproducibilidad de las transformaciones.

Los resultados de integración generaron 564 registros mensuales en la capa Plata y 564 registros en la capa Oro. Durante la validación técnica se obtuvo un resultado de 145 pruebas automatizadas aprobadas.

Para organizar el cierre de la etapa se estableció una distribución de responsabilidades entre implementación técnica y aseguramiento de calidad.

La documentación incluye evidencias de procesamiento, trazabilidad, ética de datos, pruebas y control de versiones.

## 2. Ingeniería de Datos

### 2.1 Incorporación de información geoespacial

Se incorporó a la capa Bronce información del Marco Geoestadístico municipal 2026 del Instituto Nacional de Estadística y Geografía (INEGI).

La fuente geográfica se encuentra en:

`data/bronce/inegi_marco_geoestadistico/2026/`

Se conservaron el archivo de origen y los metadatos correspondientes para facilitar la identificación de la fuente.

### 2.2 Procesamiento de límites municipales

Se implementó el módulo:

`src/geoespacial.py`

Este módulo permite procesar la información geográfica y generar un producto normalizado en la capa Plata.

**Resultados principales:**

| Elemento | Resultado |
|---|---|
| Fuente | Marco Geoestadístico municipal 2026 del INEGI |
| Entidad federativa | Colima |
| Municipios procesados | 10 |
| Formato de salida | GeoPackage |
| Sistema de referencia de salida | EPSG:4326 |
| Archivo generado | `data/plata/municipios_colima_2026.gpkg` |

El archivo de salida es un producto derivado que puede regenerarse mediante el procesamiento correspondiente.

### 2.3 Generación del mapa municipal

Se desarrolló el script:

`src/mapa_colima.py`

Su ejecución permitió generar una representación cartográfica de los municipios de Colima, destacando Colima y Villa de Álvarez como territorios de interés del observatorio.

La evidencia gráfica se encuentra en:

`reportes/figuras/mapa_municipios_colima_v2.png`

Este mapa representa límites administrativos y no debe interpretarse como una visualización de precios de vivienda o indicadores económicos municipales.

### 2.4 Integración Bronce–Plata–Oro

Se fortaleció el procesamiento de información económica procedente de INEGI y Banxico.

Las fuentes consideradas fueron:

| Fuente | Identificador | Información |
|---|---|---|
| INEGI | `910402` | Inflación mensual de servicios subyacentes |
| Banxico | `SF43783` | TIIE de 28 días |

Los productos generados fueron:

| Capa | Archivo | Registros |
|---|---|---:|
| Plata | `data/plata/integracion_mensual_e2.csv` | 564 |
| Oro | `data/oro/indicadores_mensuales_e2.csv` | 564 |

La comparación de registros permite comprobar que las 564 filas se conservaron durante la transformación de Plata a Oro.

### 2.5 Trazabilidad de datos

Se incorporaron mecanismos para identificar la procedencia de los registros procesados.

Entre los campos utilizados se encuentran:

- `file_origin`: referencia al archivo de origen o respaldo.
- `fecha_ingesta_utc`: fecha de captura registrada para la fuente.

Es importante distinguir la fecha de captura de los datos de la fecha en que se ejecutó su procesamiento.

La implementación y documentación de trazabilidad se encuentran en:

- `src/trazabilidad.py`
- `docs/E2/trazabilidad.md`

La trazabilidad facilita la revisión de las fuentes y la reproducción de los resultados.

### 2.6 Evidencias de Ingeniería de Datos

| Actividad | Evidencia |
|---|---|
| Incorporación del Marco Geoestadístico | `b4fe64f` |
| Procesamiento geoespacial | `8ef0ae2` |
| Generación del mapa municipal | `6f79137` |
| Incorporación de trazabilidad | `ce8b16a` |

## 3. Estadística

### 3.1 Alcance de los indicadores

El observatorio utiliza indicadores económicos nacionales que permiten contextualizar determinadas condiciones financieras y de precios.

Entre ellos se encuentran la inflación mensual de servicios subyacentes del INEGI y la TIIE de 28 días de Banxico.

Estos indicadores no representan directamente el costo de la vivienda en Colima ni en Villa de Álvarez.

### 3.2 Resultados y limitaciones

La incorporación de información geográfica permite identificar los municipios del estado de Colima y establecer una base territorial para análisis posteriores.

Sin embargo, la información económica procesada no constituye por sí misma una medición municipal de precios de vivienda.

Por lo tanto:

- No se atribuyen valores nacionales a municipios específicos.
- No se presentan comparaciones municipales de precios sin fuentes adecuadas.
- Se conserva la distinción entre indicadores económicos y delimitaciones territoriales.
- Se documentan las limitaciones de cobertura y escala de los datos.

### 3.3 Experimento estadístico previsto

En la propuesta inicial del proyecto se contempló para E2 un experimento factorial 2³ relacionado con el procesamiento y almacenamiento de datos.

No se dispone todavía de evidencia suficiente para declarar ejecutado ese experimento en esta entrega.

Su realización o documentación deberá verificarse antes del cierre definitivo de E2.

## 4. Calidad de Software

### 4.1 Pruebas automatizadas

Se incorporaron pruebas para verificar el procesamiento geoespacial y la trazabilidad.

Entre los archivos de pruebas se encuentran:

- `tests/test_geoespacial.py`
- `tests/test_trazabilidad_e2.py`

Durante la validación técnica de E2 se registraron **145 pruebas aprobadas**.

Estas pruebas permiten verificar aspectos del procesamiento, la estructura de los resultados y la conservación de información.

### 4.2 Documentación ética

Se elaboró el documento:

`docs/etica-datos.md`

Este documento aborda consideraciones relacionadas con el uso responsable de información, la procedencia de las fuentes, las limitaciones de los indicadores y la necesidad de evitar interpretaciones incorrectas.

### 4.3 Distribución de responsabilidades del equipo

Para el cierre de E2 se establecieron dos áreas complementarias de responsabilidad:

| Integrante | Área | Responsabilidades |
|---|---|---|
| David Cuevas Farías | Implementación técnica | Incorporación de información geográfica, desarrollo de scripts, procesamiento municipal, generación del mapa, integración y trazabilidad |
| Nancy Haide Vázquez Ávalos | Validación y aseguramiento de calidad | Revisión de fuentes y metadatos, validación de resultados geográficos, auditoría de trazabilidad, verificación de pruebas y revisión documental |

Esta distribución busca equilibrar las actividades de construcción técnica y revisión de calidad.

La implementación se encuentra respaldada por los commits de la rama `e2david`.

Las revisiones asignadas a Nancy se documentarán como completadas una vez que se ejecuten y se incorporen sus evidencias.

### 4.4 Evidencia de proceso personal (PSP)

El repositorio contiene registros de tiempo y defectos para ambos integrantes:

| Integrante | Registro de tiempo | Registro de defectos |
|---|---|---|
| David Cuevas Farías | `calidad/tiempo-david.csv` | `calidad/defectos-david.csv` |
| Nancy Haide Vázquez Ávalos | `calidad/tiempo-nancy.csv` | `calidad/defectos-nancy.csv` |

Para David se prepararon siete registros estimados correspondientes a las actividades G01–G07 del 22 de noviembre de 2026.

El tiempo efectivo aproximado fue de 270 minutos, con 45 minutos adicionales de interrupciones.

Los horarios individuales son estimaciones reconstruidas y no mediciones exactas.

Los registros PSP de Nancy para E2 deberán actualizarse con los tiempos y actividades de revisión efectivamente realizados.

Los registros de defectos anteriores se conservan como antecedentes. No se asignan defectos nuevos sin evidencia de su identificación y corrección.

## 5. Limitaciones y pendientes declarados

La etapa E2 presenta las siguientes limitaciones y actividades pendientes:

1. **Escala de los indicadores:** las series económicas nacionales no representan automáticamente condiciones municipales de vivienda.
2. **Alcance del mapa:** la visualización muestra límites administrativos, no precios ni valores económicos municipales.
3. **Archivos derivados:** algunos productos de Plata y Oro se generan mediante scripts y no necesariamente se encuentran versionados en Git.
4. **Trazabilidad temporal:** las fechas de captura no deben confundirse con fechas de procesamiento.
5. **Experimento factorial 2³:** pendiente de verificar su ejecución y resultados.
6. **PSP:** pendiente de completar y validar los registros individuales de E2.
7. **Validación de calidad:** pendiente de incorporar los resultados documentados de las revisiones asignadas a Nancy.
8. **Integración final:** pendiente de verificar el cierre del equipo y la integración de la rama de trabajo.

Estas limitaciones se declaran para evitar presentar como terminadas actividades que todavía requieren evidencia.

## 6. Relatoría y entregables

### 6.1 Documentación

| Documento | Ubicación |
|---|---|
| Entrega E2 | `docs/E2/ENTREGA.md` |
| Relatoría E2 | `docs/relatoria-E2.md` |
| Trazabilidad | `docs/E2/trazabilidad.md` |
| Ética de datos | `docs/etica-datos.md` |

### 6.2 Productos técnicos

| Producto | Ubicación |
|---|---|
| Procesamiento geoespacial | `src/geoespacial.py` |
| Generación de mapa | `src/mapa_colima.py` |
| Trazabilidad | `src/trazabilidad.py` |
| Integración de datos | `src/integracion.py` |
| Indicadores Oro | `src/oro.py` |
| Pruebas geoespaciales | `tests/test_geoespacial.py` |
| Pruebas de trazabilidad | `tests/test_trazabilidad_e2.py` |
| Mapa municipal | `reportes/figuras/mapa_municipios_colima_v2.png` |

### 6.3 Evidencias de validación

La validación técnica documentada incluye el procesamiento de los diez municipios de Colima, la generación de los productos mensuales de Plata y Oro y la ejecución satisfactoria de 145 pruebas automatizadas.

Las revisiones adicionales de calidad asignadas a Nancy deberán documentarse mediante sus resultados y registros PSP.

### 6.4 Uso de IA generativa

Se utilizó ChatGPT como apoyo para explicar procedimientos técnicos, revisar comandos, orientar la implementación de scripts y pruebas, interpretar resultados y estructurar documentación.

Las respuestas generadas se contrastaron con los archivos y evidencias disponibles en el repositorio.

La responsabilidad de verificar los resultados y presentar la entrega corresponde al equipo.

## 7. Control de versiones

### 7.1 Repositorio

**Repositorio:** https://github.com/NancyHaideVazquez/trusted-data-lab

**Rama de trabajo:** `e2david`

### 7.2 Historial de commits

| Etapa | Commit | Descripción |
|---|---|---|
| G01 | `b4fe64f` | Incorporar Marco Geoestadístico municipal 2026 |
| G02 | `8ef0ae2` | Implementar procesamiento geoespacial y pruebas |
| G03 | `6f79137` | Generar mapa municipal |
| G04 | `ce8b16a` | Incorporar trazabilidad Bronce–Plata–Oro |
| G05 | `1a8adcf` | Documentar ética y uso responsable de datos |
| G06 | `d93ef88` | Documentar entrega y evidencias |
| G07 | `9fd82f6` | Documentar relatoría y actualizar entrega |

Los commits G01–G07 se registraron el 22 de noviembre de 2026.

### 7.3 Estado de la entrega

La implementación técnica, los productos geoespaciales, la trazabilidad y la documentación principal cuentan con evidencias en el repositorio.

El cierre de E2 requiere completar las revisiones de calidad asignadas, actualizar los registros PSP correspondientes y verificar el cumplimiento de los requisitos oficiales.

**Estado:** Entrega E2 actualizada con la distribución de responsabilidades del equipo. Pendiente de revisión y validación final.

## Evidencias complementarias de validacion G05-G07

El 22 de noviembre de 2026 se realizaron verificaciones
adicionales de calidad correspondientes a E2.

Resultados obtenidos:

- G05: revision del documento de etica de datos, aprobada.
- G06: 14 pruebas especificas de E2 aprobadas.
- G06: 145 pruebas generales aprobadas.
- G07: comprobaciones documentales y de formato aprobadas.

Tiempo total reportado: 75 minutos.

Evidencia disponible:
`docs/E2/validacion-calidad.md`

Estas verificaciones no implican que se hayan completado
las demas actividades de revision pendientes.

## Verificacion de procedencia y condiciones de uso

Se verifico la integridad del archivo original
2026_1_06_MUN.zip mediante SHA-256.

El hash calculado coincide con el registrado
en metadatos.json.

Fuente: INEGI, Marco Geoestadistico municipal 2026.

Condiciones de uso:
https://www.inegi.org.mx/inegi/terminos.html

La fecha exacta de ingesta y la URL directa
de descarga permanecen sin documentar.

La revision de procedencia y condiciones de uso
se encuentra registrada en docs/etica-datos.md.
