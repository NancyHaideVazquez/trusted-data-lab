# Relatoría E2 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima

**Equipo:** David Cuevas Farías y Nancy Haide Vázquez Ávalos

**Etapa:** E2 — Procesamiento geoespacial, trazabilidad y ética de datos

**Fecha de preparación:** 22 de noviembre de 2026

**Repositorio:** https://github.com/NancyHaideVazquez/trusted-data-lab

**Rama de trabajo:** `e2david`

---

## 1. ¿Qué nos propusimos?

Durante la etapa E2 buscamos fortalecer el Observatorio de Vivienda y Costos de Colima mediante la incorporación de información geográfica, la trazabilidad de los datos y la documentación de su uso responsable.

Los objetivos de trabajo fueron:

- Incorporar información oficial del Marco Geoestadístico del INEGI a la capa Bronce.
- Implementar el procesamiento geoespacial para obtener los límites municipales de Colima.
- Generar una representación cartográfica de Colima y Villa de Álvarez.
- Fortalecer la trazabilidad de los registros entre las capas Bronce, Plata y Oro.
- Verificar la integridad de las transformaciones mediante pruebas automatizadas.
- Documentar las consideraciones éticas, limitaciones y evidencias de la etapa.

Estos objetivos se relacionan con las materias de Ingeniería de Datos, Análisis Estadístico y Calidad en los Sistemas de Información.

## 2. ¿Qué hicimos? Cronología del trabajo

### Actividades registradas en la rama de David

El historial de Git registra los siguientes avances el 22 de noviembre de 2026:

| Actividad | Trabajo realizado | Evidencia |
|---|---|---|
| G01 | Incorporación del Marco Geoestadístico municipal 2026 en Bronce | `b4fe64f` |
| G02 | Implementación del procesamiento geoespacial y sus pruebas | `8ef0ae2` |
| G03 | Generación del mapa municipal de Colima y Villa de Álvarez | `6f79137` |
| G04 | Incorporación de trazabilidad entre Bronce, Plata y Oro | `ce8b16a` |
| G05 | Documentación de ética y uso responsable de datos | `1a8adcf` |
| G06 | Elaboración del documento de entrega E2 | `d93ef88` |

Las fechas corresponden a los commits registrados en Git y no necesariamente representan la totalidad del tiempo dedicado a cada actividad.

### Participación del equipo

**David Cuevas Farías:** los seis commits anteriores se encuentran documentados en la rama de trabajo `e2david`. Las actividades incluyen procesamiento geoespacial, visualización, trazabilidad, pruebas y documentación.

**Nancy Haide Vázquez Ávalos:** su participación específica durante E2 deberá incorporarse después de revisar sus registros y contribuciones correspondientes a esta etapa.

### Registro de tiempos

El repositorio contiene los archivos:

- `calidad/tiempo-david.csv`
- `calidad/tiempo-nancy.csv`

Sin embargo, antes de reportar horas totales de E2, es necesario verificar qué registros corresponden específicamente a esta etapa.

Por el momento no se declara un total de horas de E2 sin respaldo documental.

## 3. ¿Qué decidimos y por qué?

### 3.1 Utilizar información geográfica oficial

Se incorporó el Marco Geoestadístico municipal 2026 del INEGI para trabajar con delimitaciones territoriales provenientes de una fuente institucional.

Esta decisión permite establecer una referencia geográfica verificable para el observatorio.

### 3.2 Separar los datos originales de los transformados

Se mantuvo el enfoque de arquitectura por capas:

- **Bronce:** conservación de las fuentes originales y sus metadatos.
- **Plata:** transformación, integración y normalización de datos.
- **Oro:** preparación de indicadores para análisis y consulta.

La separación permite conservar las fuentes originales y reproducir los resultados derivados.

### 3.3 Normalizar la información geoespacial

El procesamiento geoespacial generó un archivo GeoPackage con los diez municipios de Colima, utilizando el sistema de referencia EPSG:4326.

Esta decisión facilita el uso posterior de los datos en herramientas de análisis y visualización geográfica.

### 3.4 Incorporar trazabilidad explícita

Se incorporaron campos de procedencia y fecha de captura para identificar las fuentes que respaldan los registros procesados.

La trazabilidad ayuda a distinguir el origen de la información y permite revisar cómo se relacionan los datos de Bronce, Plata y Oro.

### 3.5 Conservar productos derivados reproducibles

Los archivos generados de Plata y Oro pueden reconstruirse mediante los scripts correspondientes.

Esta decisión evita confundir los archivos originales de captura con los productos transformados.

## 4. ¿Qué salió mal y cómo lo atendimos?

### 4.1 Diferencias entre datos nacionales y municipales

Los indicadores económicos utilizados proceden de fuentes nacionales, mientras que la información geográfica corresponde a municipios de Colima.

**Tratamiento:** se documentó que los indicadores nacionales no deben interpretarse automáticamente como mediciones específicas de Colima o Villa de Álvarez.

### 4.2 Necesidad de verificar la procedencia de los registros

Durante la revisión de trazabilidad fue necesario distinguir las fuentes de respaldo, las fechas de captura y los datos procesados.

**Tratamiento:** se incorporaron mecanismos de trazabilidad y se documentaron las limitaciones de las fechas y fuentes disponibles.

### 4.3 Reproducibilidad de los archivos derivados

Los archivos generados en Plata y Oro no forman necesariamente parte de los archivos versionados del repositorio.

**Tratamiento:** se conservaron los scripts necesarios para reproducir los productos derivados y se documentaron sus rutas.

### 4.4 Advertencias de formato en la documentación

Al preparar `docs/E2/ENTREGA.md`, Git detectó espacios al final de algunas líneas.

**Tratamiento:** se eliminaron los espacios sobrantes y se verificó que el documento mantuviera sus siete secciones y su contenido.

Este incidente se documenta como observación del proceso, pero no se le asigna un número de defecto PSP sin un registro correspondiente.

### Registro de defectos PSP

Los archivos `calidad/defectos-david.csv` y `calidad/defectos-nancy.csv` contienen antecedentes de etapas previas.

La clasificación y los tiempos de corrección correspondientes a E2 quedan pendientes de actualización y verificación.

## 5. ¿Qué aprendimos?

### Ingeniería de Datos

Aprendimos la importancia de conservar los datos originales, identificar su procedencia y separar las transformaciones de los productos finales.

También reforzamos el manejo de información geoespacial mediante GeoPackage, sistemas de referencia y procesamiento de límites municipales.

La trazabilidad entre capas facilita las auditorías, la depuración y la reproducción de resultados.

### Análisis Estadístico

Reconocimos que la disponibilidad de límites municipales no significa que existan indicadores económicos desagregados para esos municipios.

Los indicadores nacionales pueden utilizarse como contexto, pero no deben presentarse como estimaciones municipales sin un procedimiento estadístico que lo justifique.

También identificamos la necesidad de documentar claramente el alcance, las unidades, la frecuencia y las limitaciones de cada indicador.

El experimento factorial 2³ contemplado en la propuesta inicial de E2 requiere una verificación independiente antes de declararlo ejecutado.

### Calidad en los Sistemas de Información

Reforzamos la importancia de automatizar las verificaciones y mantener evidencia reproducible de los cambios.

La suite del proyecto registró 145 pruebas aprobadas durante la validación de E2.

También identificamos la necesidad de mantener actualizados los registros PSP de tiempos y defectos para que la documentación refleje el trabajo real.

## 6. ¿Cuáles son las evidencias?

### Ingeniería de Datos

| Evidencia | Ubicación |
|---|---|
| Fuente geográfica en Bronce | `data/bronce/inegi_marco_geoestadistico/2026/` |
| Procesamiento geoespacial | `src/geoespacial.py` |
| Generación del mapa | `src/mapa_colima.py` |
| Mapa municipal | `reportes/figuras/mapa_municipios_colima_v2.png` |
| Integración de datos | `src/integracion.py` |
| Procesamiento de indicadores Oro | `src/oro.py` |
| Documentación de trazabilidad | `docs/E2/trazabilidad.md` |

### Calidad de Software

| Evidencia | Ubicación |
|---|---|
| Pruebas geoespaciales | `tests/test_geoespacial.py` |
| Pruebas de trazabilidad | `tests/test_trazabilidad_e2.py` |
| Registro de tiempos de David | `calidad/tiempo-david.csv` |
| Registro de tiempos de Nancy | `calidad/tiempo-nancy.csv` |
| Registro de defectos de David | `calidad/defectos-david.csv` |
| Registro de defectos de Nancy | `calidad/defectos-nancy.csv` |

### Documentación

| Documento | Ubicación |
|---|---|
| Entrega E2 | `docs/E2/ENTREGA.md` |
| Ética de datos | `docs/etica-datos.md` |
| Relatoría E2 | `docs/relatoria-E2.md` |

### Evidencia de control de versiones

Los commits G01–G06 permiten identificar las principales modificaciones realizadas durante esta etapa.

Los cambios se encuentran en la rama `e2david` del repositorio:

https://github.com/NancyHaideVazquez/trusted-data-lab

## Uso de IA generativa

Se utilizó ChatGPT como herramienta de apoyo durante el desarrollo de E2 para:

- Explicar procedimientos técnicos y comandos de PowerShell y Git.
- Apoyar en la elaboración y revisión de scripts de procesamiento.
- Orientar la implementación de pruebas automatizadas.
- Revisar errores de ejecución y resultados de validación.
- Organizar la documentación de trazabilidad, ética y entrega.
- Redactar y estructurar la presente relatoría.

Los resultados técnicos se contrastaron