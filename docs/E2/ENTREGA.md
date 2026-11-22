# Entrega E2 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima  
**Equipo:** David Cuevas Farías y Nancy Haide Vázquez Ávalos  
**Etapa:** E2 — Procesamiento geoespacial, trazabilidad y ética de datos  
**Fecha de preparación:** 22 de noviembre de 2026  
**Rama de trabajo:** `e2david`  
**Repositorio:** https://github.com/NancyHaideVazquez/trusted-data-lab

## 1. Resumen ejecutivo

Durante E2 se amplió el Observatorio de Vivienda y Costos de Colima mediante la incorporación de información geoespacial oficial, la generación de un mapa municipal y el fortalecimiento de la trazabilidad de datos.

Se trabajó con el Marco Geoestadístico 2026 del INEGI para identificar los municipios del estado de Colima y destacar las zonas de interés del observatorio: Colima y Villa de Álvarez.

También se incorporaron metadatos de procedencia a los procesos de integración de las capas Bronce, Plata y Oro, conservando referencias a los archivos de origen y fechas de captura.

Finalmente, se elaboró un documento de ética de datos que establece criterios para interpretar y presentar responsablemente la información pública.

## 2. Ingeniería de Datos

| Criterio | Evidencia | Resultado |
|---|---|---|
| Incorporación geoespacial | `data/bronce/inegi_marco_geoestadistico/2026/` | Incorporación del Marco Geoestadístico municipal 2026 |
| Procesamiento geoespacial | `src/geoespacial.py` | Transformación de información municipal a EPSG:4326 |
| Capa Plata geoespacial | `data/plata/municipios_colima_2026.gpkg` | Generación reproducible de información geográfica de diez municipios |
| Visualización territorial | `src/mapa_colima.py` | Mapa municipal que destaca Colima y Villa de Álvarez |
| Trazabilidad | `docs/E2/trazabilidad.md` | Documentación del recorrido Bronce → Plata → Oro |
| Integración de datos | `src/integracion.py`, `src/oro.py` | Conservación de metadatos de procedencia |

### Resultados geoespaciales

Se procesó la información de diez municipios del estado de Colima.

El mapa generado se encuentra en:

`reportes/figuras/mapa_municipios_colima_v2.png`

La transformación geoespacial permite utilizar los límites municipales como referencia para futuros análisis territoriales.

### Trazabilidad Bronce → Plata → Oro

Se incorporaron los campos:

- `archivo_origen`: referencia al archivo de procedencia.
- `fecha_ingesta_utc`: fecha de captura registrada en los metadatos disponibles.

La integración E2 produjo 564 registros mensuales en la capa Plata y conservó 564 registros en la capa Oro durante la ejecución verificada.

Los detalles y limitaciones de procedencia se encuentran en `docs/E2/trazabilidad.md`.

## 3. Estadística

### Alcance de los indicadores

El observatorio utiliza información de INEGI y Banco de México.

El indicador INEGI `910402` proporciona información nacional relacionada con inflación de servicios.

La serie Banxico `SF43783` corresponde a la TIIE a 28 días y proporciona contexto financiero nacional.

Estos indicadores no representan directamente los precios de terrenos, viviendas o rentas de Colima y Villa de Álvarez.

### Resultados y limitaciones

El trabajo geoespacial permite delimitar territorialmente los municipios de interés, pero no demuestra diferencias estadísticas entre ellos.

No se presentan resultados de un experimento factorial 2³ ni de comparaciones municipales inferenciales, porque esas ejecuciones no forman parte de las evidencias verificadas para este cierre.

## 4. Calidad de Software

| Criterio | Evidencia | Resultado |
|---|---|---|
| Pruebas geoespaciales | `tests/test_geoespacial.py` | Pruebas automatizadas del procesamiento geográfico |
| Pruebas de trazabilidad | `tests/test_trazabilidad_e2.py` | Verificación de metadatos y procedencia |
| Pruebas generales | Suite de `pytest` | 145 pruebas aprobadas en la ejecución local revisada |
| Validación de datos | `src/calidad.py` | Validación de campos de procedencia |
| Ética de datos | `docs/etica-datos.md` | Criterios de uso responsable de información |

### Evidencia de proceso personal (PSP)

Los registros PSP del equipo deben revisarse para verificar las actividades, tiempos y defectos correspondientes a E2.

Archivos de referencia:

- `calidad/tiempo-david.csv`
- `calidad/defectos-david.csv`
- `calidad/tiempo-nancy.csv`
- `calidad/defectos-nancy.csv`

No se reportan tiempos ni defectos de E2 sin comprobar previamente esos registros.

## 5. Limitaciones y pendientes declarados

1. Los indicadores económicos utilizados tienen cobertura nacional y no deben interpretarse como precios municipales de vivienda.
2. El mapa municipal representa límites territoriales y no contiene estimaciones de precios inmobiliarios.
3. Los archivos de Plata y Oro generados localmente son productos reproducibles y no necesariamente archivos versionados en Git.
4. Los metadatos de captura disponibles no deben confundirse con una fecha de procesamiento que no haya sido registrada.
5. Se encuentra pendiente verificar la evidencia del experimento factorial 2³ planteado en la propuesta inicial.
6. Se debe revisar la actualización de los registros PSP y el estado de integración de la rama a `main`.
7. La etiqueta de cierre `e2` deberá verificarse o crearse únicamente cuando el equipo confirme la entrega definitiva.

## 6. Relatoría y entregables

Documentos principales:

- `docs/E2/trazabilidad.md`
- `docs/etica-datos.md`
- `docs/relatoria-E2.md` — pendiente de elaboración.

Código y evidencias:

- `src/geoespacial.py`
- `src/mapa_colima.py`
- `src/trazabilidad.py`
- `tests/test_geoespacial.py`
- `tests/test_trazabilidad_e2.py`
- `reportes/figuras/mapa_municipios_colima_v2.png`

## 7. Control de versiones

| Commit | Actividad |
|---|---|
| `b4fe64f` | Incorporación del Marco Geoestadístico municipal 2026 |
| `8ef0ae2` | Procesamiento geoespacial y pruebas |
| `6f79137` | Generación del mapa municipal |
| `ce8b16a` | Trazabilidad Bronce → Plata → Oro |
| `1a8adcf` | Ética y uso responsable de datos |

Los cinco commits se registraron el 22 de noviembre de 2026 en la rama `e2david`.

La rama se encontraba sincronizada con `origin/e2david` después del commit G05.

**Estado:** Documentación preliminar de cierre E2, pendiente de revisión final del equipo.