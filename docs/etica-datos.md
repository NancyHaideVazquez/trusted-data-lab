# Ética y uso responsable de datos

**Proyecto:** Observatorio de Vivienda y Costos de Colima

**Etapa:** E2 — Trusted Data Lab

## 1. Propósito

Establecer criterios éticos para la recopilación, procesamiento, análisis y publicación de información utilizada en el Observatorio de Vivienda y Costos de Colima.

El objetivo es promover la transparencia, la reproducibilidad y la interpretación responsable de los resultados.

## 2. Procedencia de los datos

El observatorio utiliza información de fuentes institucionales, principalmente:

- **INEGI:** indicadores económicos y Marco Geoestadístico.

- **Banco de México:** indicadores financieros, incluida la TIIE a 28 días.

Los archivos originales se conservan en la capa Bronce y se documentan sus transformaciones hacia las capas Plata y Oro.

La trazabilidad permite identificar archivos históricos que respaldan los indicadores procesados.

## 3. Privacidad y protección de datos

Los conjuntos de datos utilizados actualmente corresponden a indicadores económicos agregados e información geográfica municipal.

No se requiere recopilar nombres, domicilios particulares, teléfonos ni otros identificadores personales para realizar los análisis previstos.

Si posteriormente se incorporan encuestas, entrevistas o registros individuales, deberán aplicarse medidas adicionales de protección, como consentimiento informado, minimización de datos y restricciones de acceso.

## 4. Limitaciones territoriales

El observatorio se enfoca en los municipios de Colima y Villa de Álvarez.

Sin embargo, los indicadores económicos utilizados de INEGI y Banco de México tienen cobertura nacional.

Por lo tanto:

- No deben presentarse como mediciones exclusivas de Colima o Villa de Álvarez.

- No permiten determinar directamente el costo de vivienda de un municipio.

- Su uso debe identificarse como contexto económico general.

- Las comparaciones municipales requieren indicadores con desagregación territorial adecuada.

## 5. Riesgos de interpretación

Entre los principales riesgos se encuentran:

- Confundir correlación con causalidad.

- Interpretar indicadores nacionales como resultados municipales.

- Presentar datos históricos como si fueran actuales.

- Omitir valores faltantes o transformaciones.

- Utilizar mapas que exageren diferencias territoriales.

- Presentar pronósticos como resultados garantizados.

Para reducir estos riesgos, las visualizaciones y los reportes deben incluir fuentes, periodos, unidades y limitaciones.

## 6. Calidad y trazabilidad

El proyecto utiliza procedimientos de validación para comprobar la estructura y consistencia de los datos.

Las transformaciones se documentan y se mantienen separadas en las capas Bronce, Plata y Oro.

La trazabilidad de E2 conserva referencias a los archivos históricos de respaldo y sus fechas de captura.

Las fechas de captura no deben confundirse con las fechas de procesamiento.

## 7. Uso responsable de mapas

Los mapas municipales tienen una finalidad informativa y de análisis territorial.

Se deben respetar los límites geográficos oficiales y documentar el sistema de referencia espacial.

Los mapas no deben sugerir diferencias económicas entre municipios cuando no existan datos que respalden esas comparaciones.

## 8. Transparencia y reproducibilidad

El código y la documentación del proyecto permiten revisar las transformaciones realizadas.

Los resultados deben acompañarse de información sobre las fuentes utilizadas, los métodos de procesamiento y las limitaciones de los conjuntos de datos.

Cuando se modifiquen indicadores, procedimientos o criterios de validación, los cambios deberán documentarse en el repositorio.

## 9. Compromisos del equipo

El equipo se compromete a:

1\. Utilizar fuentes identificables y verificables.

2\. Evitar la publicación innecesaria de datos personales.

3\. Diferenciar los datos observados de las estimaciones.

4\. Documentar las transformaciones realizadas.

5\. Comunicar las limitaciones de los indicadores.

6\. Evitar conclusiones que excedan la evidencia disponible.

7\. Corregir errores detectados en los conjuntos de datos o reportes.

## 10. Conclusión

El uso ético de los datos es fundamental para que el Observatorio de Vivienda y Costos de Colima produzca información transparente y confiable.

La trazabilidad, la validación y la comunicación de limitaciones permiten reducir interpretaciones incorrectas y favorecer un uso responsable de los resultados.

## Condiciones de uso del Marco Geoestadistico del INEGI

El proyecto utiliza informacion del Marco Geoestadistico
municipal 2026 del INEGI.

Fuente oficial:
https://www.inegi.org.mx/temas/mg/

Terminos de uso:
https://www.inegi.org.mx/inegi/terminos.html

Los terminos permiten reproducir, publicar, adaptar
y analizar informacion, respetando sus condiciones.

Compromisos del proyecto:
- Reconocer al INEGI como fuente original.
- Conservar los metadatos de procedencia.
- Identificar las transformaciones realizadas.
- No presentar los resultados derivados como
  analisis oficiales del INEGI.

Referencia de atribucion:
Fuente: INEGI, Marco Geoestadistico municipal 2026.

La procedencia del archivo geografico fue verificada mediante
el archivo original conservado en Descargas y su historial Git.

- URL directa: https://www.inegi.org.mx/contenidos/descargadenue/MGdescarga/MGN2026/06/2026_1_06_MUN.zip
- Fecha estimada de descarga UTC: 2026-11-22T18:08:54Z.
- Primer commit de incorporacion: b4fe64f.
- Fecha del primer commit UTC: 2026-11-22T18:15:18Z.
- Evidencia de URL: campo HostUrl de Zone.Identifier.
- SHA-256: D58C6A6F77039C00A62D4D51FDE33A27AB70116F3B2CD9C90899463E46A11F00.

Se comprobo que el archivo original y el archivo conservado
en Bronce tienen exactamente el mismo SHA-256.

La fecha estimada de descarga se obtuvo de CreationTimeUtc.
El instante exacto de ingesta no fue registrado y no se inventa.

Los metadatos actualizados se encuentran en:
data/bronce/inegi_marco_geoestadistico/2026/metadatos.json.

## 11. Revisión de robots.txt y condiciones de acceso

Se consultaron los archivos públicos robots.txt de las instituciones utilizadas como fuentes del observatorio.

### 11.1 INEGI

- URL: https://www.inegi.org.mx/robots.txt
- Resultado de consulta: HTTP 200.
- Fecha de revisión: 22 de noviembre de 2026.
- Agente general: User-Agent: *.

Entre las rutas expresamente permitidas se encuentran `/temas`, `/datos` y `/programas`.

Se identificaron restricciones específicas, como `/auth/register/` y `/catalog/*/data-dictionary/*?file_name=*`.

Estas reglas no constituyen autorización general para extraer cualquier contenido.

### 11.2 Banco de México

- URL: https://www.banxico.org.mx/robots.txt
- Resultado de consulta: HTTP 200.
- Fecha de revisión: 22 de noviembre de 2026.

Se identificaron restricciones para rutas como `/dyn`, `/dyn/` y `/ALEPH`.

El proyecto debe respetar las restricciones aplicables a las rutas y mecanismos de acceso utilizados.

### 11.3 Criterios de cumplimiento

El equipo establece los siguientes compromisos:

1. Priorizar archivos públicos y servicios oficiales de descarga.
2. Consultar las condiciones de uso antes de incorporar nuevas fuentes.
3. Respetar las restricciones aplicables de robots.txt.
4. Evitar mecanismos de extracción que eludan controles de acceso.
5. Conservar la identificación y procedencia de las fuentes.
6. Revisar nuevamente las condiciones si cambian las rutas o métodos de adquisición.

La consulta de robots.txt no sustituye la revisión de términos de uso ni acredita por sí misma derechos de reproducción o redistribución.

## 12. Licencias y condiciones de reutilización

### 12.1 INEGI

Fuente: Marco Geoestadístico municipal 2026.

- Página oficial: https://www.inegi.org.mx/temas/mg/
- Términos institucionales: https://www.inegi.org.mx/inegi/terminos.html

El proyecto reconoce al INEGI como fuente original y conserva la referencia de procedencia.

La reproducción, adaptación y publicación de productos derivados debe sujetarse a las condiciones institucionales aplicables.

No se atribuye al INEGI la autoría de los análisis derivados del observatorio.

### 12.2 Banco de México

Fuente: Sistema de Información Económica (SIE), serie SF43783, TIIE a 28 días.

Referencias oficiales:

- Sitio institucional: https://www.banxico.org.mx/
- Salvedad y políticas de uso: https://www.banxico.org.mx/footer-es/salvedad-politicas-uso-banco-.html
- Documentación técnica de la API SIE: https://www.banxico.org.mx/SieAPIRest/swagger/index.html
- Archivo robots.txt: https://www.banxico.org.mx/robots.txt

#### Condiciones generales de reutilización

Las políticas institucionales del Banco de México establecen una autorización general para reproducir y utilizar la información difundida en su página oficial.

La reutilización requiere identificar la institución de procedencia e incluir su dirección de Internet para facilitar la verificación de los datos.

La información oportuna puede presentar diferencias respecto de las cifras definitivas.

Los análisis, interpretaciones y transformaciones realizados por terceros no constituyen resultados oficiales del Banco de México.

#### Aplicación al observatorio

El equipo establece los siguientes compromisos:

1. Reconocer al Banco de México como fuente de la serie SF43783.
2. Incluir la dirección oficial de procedencia.
3. Conservar los archivos originales y sus metadatos.
4. Identificar las fechas de captura y los periodos analizados.
5. Documentar las transformaciones realizadas en Plata y Oro.
6. Proteger los tokens de acceso mediante variables de entorno y secretos de GitHub Actions.
7. Respetar los límites de consulta aplicables a la API SIE.
8. Evitar solicitudes innecesarias durante los experimentos estadísticos.
9. Diferenciar los resultados académicos de las publicaciones oficiales de Banxico.
10. Revisar nuevamente las condiciones institucionales cuando cambie la fuente o el mecanismo de consulta.

#### Referencia de atribución

Fuente: Banco de México, Sistema de Información Económica, serie SF43783, TIIE a 28 días.

Sitio oficial: https://www.banxico.org.mx/

#### Alcance y limitaciones

Se verificó la autorización general de reutilización establecida en las políticas institucionales y se identificó la documentación técnica oficial de la API SIE.

No se confirmó una licencia independiente específica para la redistribución de respuestas completas de la API SIE. Por tanto, no se afirma que exista una licencia abierta específica ni una autorización ilimitada de redistribución.

Las condiciones particulares del servicio deberán contrastarse con su salvedad de uso y los términos de acceso asociados al token.

### 12.3 Alcance de la revisión

La presente declaración documenta las fuentes utilizadas, las reglas de rastreo observadas, las condiciones generales de reutilización y los compromisos éticos del equipo.

La revisión de robots.txt no sustituye la verificación jurídica de licencias y términos específicos.

Si se incorporan nuevas fuentes, deberán documentarse sus condiciones de acceso, reutilización, atribución y privacidad.

Esta revisión tiene finalidad académica y no constituye una certificación de cumplimiento jurídico.
