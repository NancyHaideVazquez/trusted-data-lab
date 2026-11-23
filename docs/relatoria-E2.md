# Relatoría E2 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima

**Equipo:** David Cuevas Farías y Nancy Haide Vázquez Ávalos

**Etapa:** E2 — Procesamiento geoespacial, trazabilidad y ética de datos

**Fecha de elaboración:** 22 de noviembre de 2026

**Repositorio:** https://github.com/NancyHaideVazquez/trusted-data-lab

**Rama de trabajo:** `e2david`

---

## 1. ¿Qué nos propusimos?

Durante la etapa E2 del proyecto Trusted Data Lab, el equipo continuó desarrollando el Observatorio de Vivienda y Costos de Colima, fortaleciendo el procesamiento de información, la integración de fuentes y la calidad de los datos.

El propósito principal fue incorporar información geoespacial oficial, mejorar la trazabilidad entre las capas Bronce, Plata y Oro, y establecer mecanismos de verificación que permitan utilizar los resultados de manera reproducible y responsable.

Los objetivos establecidos fueron:

1. Incorporar información del Marco Geoestadístico municipal 2026 del INEGI.
2. Procesar los límites municipales de Colima mediante herramientas geoespaciales.
3. Generar un mapa de los municipios de Colima y Villa de Álvarez.
4. Mejorar la integración de información entre las capas Bronce, Plata y Oro.
5. Incorporar mecanismos de trazabilidad para identificar el origen de los registros.
6. Verificar las transformaciones mediante pruebas automatizadas.
7. Documentar los principios éticos y las limitaciones de los datos.
8. Fortalecer la documentación técnica y los registros de calidad del proyecto.

Para organizar el cierre de E2 se definieron dos áreas complementarias de responsabilidad: implementación técnica y validación de calidad.

## 2. ¿Qué hicimos? Cronología del trabajo

### 2.1 Organización de responsabilidades

El equipo está integrado por David Cuevas Farías y Nancy Haide Vázquez Ávalos.

Para el cierre de la etapa E2 se estableció la siguiente distribución de responsabilidades:

| Integrante | Área de responsabilidad | Actividades |
|---|---|---|
| David Cuevas Farías | Implementación técnica | Incorporación de datos geográficos, desarrollo de scripts, integración de información y generación de productos |
| Nancy Haide Vázquez Ávalos | Validación y aseguramiento de calidad | Revisión de fuentes, comprobación de resultados, auditoría de trazabilidad, verificación de pruebas y revisión documental |

Esta distribución busca mantener un equilibrio entre la construcción de los componentes y la revisión de su calidad.

Las actividades técnicas ya implementadas cuentan con evidencia en Git. Las actividades de validación asignadas para el cierre deberán respaldarse con los resultados de revisión correspondientes.

### 2.2 Actividades técnicas documentadas

El historial de la rama `e2david` registra los siguientes avances el 22 de noviembre de 2026:

| Etapa | Actividad | Commit |
|---|---|---|
| G01 | Incorporación del Marco Geoestadístico municipal 2026 en Bronce | `b4fe64f` |
| G02 | Implementación del procesamiento geoespacial y pruebas | `8ef0ae2` |
| G03 | Generación del mapa municipal de Colima y Villa de Álvarez | `6f79137` |
| G04 | Incorporación de trazabilidad Bronce–Plata–Oro | `ce8b16a` |
| G05 | Documentación de ética y uso responsable de datos | `1a8adcf` |
| G06 | Elaboración del documento de entrega E2 | `d93ef88` |
| G07 | Elaboración de la relatoría y actualización de la entrega | `9fd82f6` |

Las fechas de los commits permiten verificar cuándo se registraron los cambios, pero no constituyen por sí mismas un registro de las horas dedicadas.

### 2.3 Incorporación de información geoespacial

Se incorporó a la capa Bronce información del Marco Geoestadístico municipal 2026 del INEGI.

El procesamiento permitió trabajar con los límites de los diez municipios del estado de Colima.

Se implementó el script `src/geoespacial.py`, encargado de procesar la información geográfica y generar un archivo GeoPackage en la capa Plata.

El resultado utiliza el sistema de referencia EPSG:4326, adecuado para el intercambio y visualización de coordenadas geográficas.

### 2.4 Generación del mapa municipal

Se desarrolló el script `src/mapa_colima.py`, con el cual se generó una representación cartográfica de los municipios de Colima.

El mapa destaca los municipios de Colima y Villa de Álvarez, que forman parte del enfoque territorial del observatorio.

La figura se encuentra en:

`reportes/figuras/mapa_municipios_colima_v2.png`

### 2.5 Integración y trazabilidad de datos

Se fortaleció el procesamiento de información económica procedente de INEGI y Banxico.

Las fuentes utilizadas incluyen:

- INEGI: indicador `910402`, correspondiente a inflación mensual de servicios subyacentes.
- Banxico: serie `SF43783`, correspondiente a la TIIE de 28 días.

Se documentó la procedencia de los datos y se incorporaron mecanismos para relacionar los registros procesados con sus fuentes de respaldo.

Los resultados generados incluyen:

| Capa | Producto | Registros |
|---|---|---:|
| Plata | `integracion_mensual_e2.csv` | 564 |
| Oro | `indicadores_mensuales_e2.csv` | 564 |

La conservación de registros entre ambas capas permite comprobar que el procesamiento no eliminó filas durante esa transformación.

### 2.6 Validación y aseguramiento de calidad

Para el cierre de E2, el área de validación contempla:

- Comprobar la correspondencia entre las fuentes originales y los metadatos.
- Verificar que el GeoPackage contenga los diez municipios esperados.
- Revisar la representación de Colima y Villa de Álvarez en el mapa.
- Comprobar los campos de procedencia de los registros.
- Revisar la conservación de registros entre Plata y Oro.
- Ejecutar las pruebas automatizadas y documentar sus resultados.
- Revisar la coherencia entre los documentos de entrega, trazabilidad, ética y relatoría.

Estas actividades forman parte de las responsabilidades asignadas a Nancy para el cierre. Sus resultados y tiempos deberán incorporarse a las evidencias PSP conforme se realicen.

### 2.7 Registro de tiempos PSP

El repositorio contiene los archivos:

- `calidad/tiempo-david.csv`
- `calidad/tiempo-nancy.csv`

Para David se preparó un registro estimado de las actividades G01–G07 realizadas el 22 de noviembre de 2026.

El tiempo efectivo aproximado fue de 270 minutos, con 45 minutos adicionales de interrupciones, para un tiempo transcurrido estimado de 315 minutos.

Los horarios individuales se reconstruyeron a partir de estimaciones y no corresponden a una medición minuto a minuto.

Los registros PSP de Nancy correspondientes a E2 permanecen pendientes de actualización con las actividades de revisión que efectivamente realice.

## 3. ¿Qué decidimos y por qué?

### 3.1 Utilizar fuentes institucionales

Se decidió incorporar información del Marco Geoestadístico del INEGI para contar con límites territoriales provenientes de una fuente oficial.

Esta decisión permite trabajar con información verificable y documentar su procedencia.

### 3.2 Mantener la arquitectura Bronce–Plata–Oro

Se conservó la separación de los datos en tres capas:

**Bronce:** almacena las fuentes originales y los metadatos de captura.

**Plata:** contiene información procesada, normalizada e integrada.

**Oro:** contiene indicadores preparados para consulta y análisis.

Esta arquitectura facilita la reproducibilidad y permite identificar los cambios realizados durante las transformaciones.

### 3.3 Normalizar los datos geográficos

Se utilizó el sistema de referencia EPSG:4326 para los resultados geoespaciales procesados.

Esto facilita la compatibilidad con herramientas de análisis geográfico y visualización.

### 3.4 Incorporar trazabilidad explícita

Se consideró necesario identificar el origen de los datos y distinguir las fechas de captura de las fechas de procesamiento.

Por ello se incorporaron campos de procedencia y se elaboró el documento `docs/E2/trazabilidad.md`.

### 3.5 Separar implementación y validación

Para el cierre de la etapa se estableció una distribución de responsabilidades entre desarrollo técnico y aseguramiento de calidad.

La finalidad es que los productos generados sean revisados de forma sistemática y que las observaciones se documenten antes de la entrega definitiva.

### 3.6 Mantener productos derivados reproducibles

Los archivos procesados de las capas Plata y Oro pueden generarse nuevamente mediante los scripts del repositorio.

Esto permite conservar las fuentes originales y reconstruir los resultados sin depender exclusivamente de archivos derivados almacenados manualmente.

## 4. ¿Qué salió mal y cómo lo atendimos?

### 4.1 Diferencias entre la escala territorial y los indicadores económicos

**Situación:** la información geográfica permite identificar municipios, mientras que los indicadores económicos disponibles corresponden a series nacionales.

**Tratamiento:** se documentó que los valores nacionales no deben interpretarse directamente como mediciones municipales.

**Resultado:** se estableció una limitación explícita para evitar interpretaciones estadísticas incorrectas.

### 4.2 Necesidad de fortalecer la trazabilidad

**Situación:** era necesario identificar las fuentes de respaldo y distinguir los datos originales de los transformados.

**Tratamiento:** se incorporaron campos de procedencia y se elaboró documentación específica de trazabilidad.

**Resultado:** se fortaleció la posibilidad de revisar el origen de los registros procesados.

### 4.3 Archivos derivados no versionados

**Situación:** los productos generados en Plata y Oro no necesariamente se incluyen en los archivos versionados de Git.

**Tratamiento:** se mantuvieron los scripts que permiten reproducir los resultados y se documentaron las rutas de salida.

**Resultado:** se conserva la posibilidad de regenerar los productos derivados.

### 4.4 Advertencias de formato en la documentación

**Situación:** durante la preparación de `docs/E2/ENTREGA.md`, Git detectó espacios al final de algunas líneas.

**Tratamiento:** se corrigieron los espacios y se revisó que el contenido conservara su estructura.

**Resultado:** la actualización documental pasó la verificación de formato de Git.

### 4.5 Registros PSP pendientes de completar

**Situación:** los registros PSP existentes no contenían inicialmente las actividades de E2.

**Tratamiento:** se preparó el registro estimado de David y se identificó la necesidad de incorporar los registros de validación correspondientes a Nancy.

**Resultado:** el seguimiento de tiempos de E2 se encuentra parcialmente actualizado y requiere completar las evidencias individuales pendientes.

### Registro de defectos

Los archivos de defectos del proyecto son:

- `calidad/defectos-david.csv`
- `calidad/defectos-nancy.csv`

Los defectos anteriores a E2 se conservan como antecedentes del proyecto.

Los problemas descritos en esta relatoría no se consideran automáticamente defectos PSP. Su incorporación al registro de defectos requiere identificar la fecha, clasificación, fase y tiempo real de corrección.

## 5. ¿Qué aprendimos?

### Ingeniería de Datos

Durante E2 reforzamos la importancia de conservar las fuentes originales, documentar su procedencia y construir transformaciones reproducibles.

El procesamiento geoespacial permitió trabajar con información territorial oficial y generar productos que pueden utilizarse posteriormente en análisis municipales.

También identificamos la importancia de separar las responsabilidades de implementación y validación para facilitar la revisión de los resultados.

### Análisis Estadístico

Aprendimos que la disponibilidad de información geográfica no implica que existan indicadores económicos desagregados para cada municipio.

Es necesario diferenciar las series nacionales de los datos municipales y evitar conclusiones que no estén respaldadas por la escala de las fuentes.

También reconocimos la importancia de documentar la frecuencia, las unidades y las limitaciones de los indicadores.

El experimento factorial 2³ contemplado en la propuesta inicial de E2 sigue pendiente de verificación documental y no se declara ejecutado en esta relatoría.

### Calidad en los Sistemas de Información

Reforzamos la importancia de utilizar pruebas automatizadas, mantener un historial de cambios y registrar evidencias verificables.

Durante la validación técnica de E2 se obtuvo un resultado de 145 pruebas aprobadas.

También identificamos que los registros PSP deben mantenerse actualizados y reflejar las actividades y tiempos reales de cada integrante.

La revisión de calidad es una actividad complementaria al desarrollo técnico y permite detectar inconsistencias antes de presentar los entregables finales.

## 6. ¿Cuáles son las evidencias?

### 6.1 Ingeniería de Datos

| Evidencia | Ubicación |
|---|---|
| Marco Geoestadístico municipal | `data/bronce/inegi_marco_geoestadistico/2026/` |
| Procesamiento geoespacial | `src/geoespacial.py` |
| Generación del mapa | `src/mapa_colima.py` |
| Mapa municipal | `reportes/figuras/mapa_municipios_colima_v2.png` |
| Integración de datos | `src/integracion.py` |
| Indicadores de Oro | `src/oro.py` |
| Trazabilidad | `src/trazabilidad.py` |
| Documento de trazabilidad | `docs/E2/trazabilidad.md` |

### 6.2 Calidad de Software

| Evidencia | Ubicación |
|---|---|
| Pruebas geoespaciales | `tests/test_geoespacial.py` |
| Pruebas de trazabilidad | `tests/test_trazabilidad_e2.py` |
| Registro de tiempo de David | `calidad/tiempo-david.csv` |
| Registro de tiempo de Nancy | `calidad/tiempo-nancy.csv` |
| Registro de defectos de David | `calidad/defectos-david.csv` |
| Registro de defectos de Nancy | `calidad/defectos-nancy.csv` |

### 6.3 Documentación

| Documento | Ubicación |
|---|---|
| Entrega E2 | `docs/E2/ENTREGA.md` |
| Ética de datos | `docs/etica-datos.md` |
| Relatoría E2 | `docs/relatoria-E2.md` |
| Trazabilidad | `docs/E2/trazabilidad.md` |

### 6.4 Control de versiones

Los commits G01–G07 documentan la incorporación de información geográfica, el desarrollo de scripts, la generación del mapa, la trazabilidad y la elaboración de documentos.

El repositorio se encuentra disponible en:

https://github.com/NancyHaideVazquez/trusted-data-lab

La rama utilizada para estos avances fue `e2david`.

### 6.5 Evidencias de validación pendientes

Para completar el cierre documental se deberán incorporar los resultados de las revisiones asignadas a Nancy, junto con sus registros PSP correspondientes.

También deberá verificarse el cumplimiento de los requisitos oficiales de la etapa E2.

## Uso de IA generativa

Durante el desarrollo de E2 se utilizó ChatGPT como herramienta de apoyo para explicar procedimientos técnicos, revisar comandos de PowerShell y Git, orientar el desarrollo de scripts y pruebas, y estructurar documentación.

La herramienta también apoyó en la interpretación de resultados, la identificación de limitaciones y la redacción de documentos técnicos.

Las respuestas generadas por IA se contrastaron con los archivos, las ejecuciones y las evidencias disponibles en el repositorio.

La responsabilidad de verificar los resultados y entregar el proyecto corresponde a sus integrantes.

## Pendientes de validación antes del cierre

1. Completar y verificar los registros PSP de E2 correspondientes a ambos integrantes.
2. Documentar las revisiones de calidad realizadas por Nancy.
3. Confirmar si se ejecutó el experimento factorial 2³ previsto en la propuesta.
4. Revisar los requisitos oficiales de la entrega E2.
5. Verificar la integración final de la rama de trabajo y las evidencias de cierre.

**Estado:** Relatoría E2 actualizada con la distribución de responsabilidades del equipo. Pendiente de completar las evidencias de validación y la revisión final.

## Evidencias complementarias de calidad G05-G07

Fecha: 2026-11-22.

Se realizaron las siguientes verificaciones:

| Actividad | Resultado | Tiempo estimado |
|---|---|---|
| G05 - Revision de etica de datos | Aprobada | 20 min |
| G06 - Pruebas automatizadas | 145 pruebas aprobadas | 35 min |
| G07 - Revision documental | Comprobaciones aprobadas | 20 min |

Tiempo total reportado: 75 minutos.

No se detectaron fallos en las pruebas automatizadas.

Evidencia:
`docs/E2/validacion-calidad.md`

La ejecucion de estas verificaciones corresponde a David.
Las revisiones individuales pendientes de Nancy conservan
su estado hasta contar con evidencia de su realizacion.

## Verificacion tecnica final de Ingenieria de Datos

El 22 de noviembre de 2026 se realizaron verificaciones
adicionales sobre los productos tecnicos de E2.

### Resultados geoespaciales

- Se comprobaron los 10 municipios de Colima.
- Las 10 geometrias resultaron validas.
- No se encontraron geometrias vacias.
- El GeoPackage utiliza EPSG:4326.
- Se verifico la integridad SHA-256 del archivo original.
- Se comprobo la existencia y apertura del mapa municipal.

### Resultados de trazabilidad

| Criterio | Plata | Oro |
|---|---:|---:|
| Registros | 564 | 564 |
| Banxico | 381 | 381 |
| INEGI | 183 | 183 |
| Registros sin origen | 0 | 0 |
| Registros sin fecha de ingesta | 0 | 0 |
| Archivos de origen inexistentes | 0 | 0 |
| Fechas de ingesta validas | 564 | 564 |

Los registros conservan referencias a sus archivos
originales en Bronce y fechas de ingesta verificables.

### Validacion automatizada

- Pruebas geoespaciales: 8 aprobadas.
- Pruebas de trazabilidad: 6 aprobadas.
- Pruebas generales del proyecto: 145 aprobadas.
- Ruff: sin errores.
- Git diff --check: sin errores.

### Evidencias de control de versiones

| Commit | Actividad |
|---|---|
| `3c58f28` | Evidencias de validacion y actualizacion de PSP |
| `691bb86` | Procedencia INEGI y correcciones de estilo |

Las verificaciones tecnicas se realizaron durante
la revision de la rama e2david.

Los resultados no sustituyen la auditoria individual
pendiente de Nancy ni la comprobacion de los requisitos
de las otras materias.
