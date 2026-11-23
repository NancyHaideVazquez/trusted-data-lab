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

La fecha exacta de ingesta y la URL directa de
descarga no estan documentadas y no se inventan.

## 11. Revisi?n de robots.txt y condiciones de acceso

Se consultaron los archivos p?blicos robots.txt de las instituciones utilizadas como fuentes del observatorio.

### 11.1 INEGI

- URL: https://www.inegi.org.mx/robots.txt
- Resultado de consulta: HTTP 200.
- Fecha de revisi?n: 22 de noviembre de 2026.
- Agente general: User-Agent: *.

Entre las rutas expresamente permitidas se encuentran `/temas`, `/datos` y `/programas`.

Se identificaron restricciones espec?ficas, como `/auth/register/` y `/catalog/*/data-dictionary/*?file_name=*`.

Estas reglas no constituyen autorizaci?n general para extraer cualquier contenido.

### 11.2 Banco de M?xico

- URL: https://www.banxico.org.mx/robots.txt
- Resultado de consulta: HTTP 200.
- Fecha de revisi?n: 22 de noviembre de 2026.

Se identificaron restricciones para rutas como `/dyn`, `/dyn/` y `/ALEPH`.

El proyecto debe respetar las restricciones aplicables a las rutas y mecanismos de acceso utilizados.

### 11.3 Criterios de cumplimiento

El equipo establece los siguientes compromisos:

1. Priorizar archivos p?blicos y servicios oficiales de descarga.
2. Consultar las condiciones de uso antes de incorporar nuevas fuentes.
3. Respetar las restricciones aplicables de robots.txt.
4. Evitar mecanismos de extracci?n que eludan controles de acceso.
5. Conservar la identificaci?n y procedencia de las fuentes.
6. Revisar nuevamente las condiciones si cambian las rutas o m?todos de adquisici?n.

La consulta de robots.txt no sustituye la revisi?n de t?rminos de uso ni acredita por s? misma derechos de reproducci?n o redistribuci?n.

## 12. Licencias y condiciones de reutilizaci?n

### 12.1 INEGI

Fuente: Marco Geoestad?stico municipal 2026.

- P?gina oficial: https://www.inegi.org.mx/temas/mg/
- T?rminos institucionales: https://www.inegi.org.mx/inegi/terminos.html

El proyecto reconoce al INEGI como fuente original y conserva la referencia de procedencia.

La reproducci?n, adaptaci?n y publicaci?n de productos derivados debe sujetarse a las condiciones institucionales aplicables.

No se atribuye al INEGI la autor?a de los an?lisis derivados del observatorio.

### 12.2 Banco de M?xico

Fuente: serie SF43783, TIIE de 28 d?as.

- Sitio oficial: https://www.banxico.org.mx/
- Archivo robots.txt: https://www.banxico.org.mx/robots.txt

El equipo reconoce al Banco de M?xico como fuente de los indicadores financieros utilizados.

La autorizaci?n espec?fica de redistribuci?n y las condiciones aplicables al mecanismo de consulta deben verificarse en la documentaci?n oficial correspondiente antes de publicar conjuntos de datos derivados.

No se presume una licencia abierta espec?fica que no haya sido comprobada.

### 12.3 Alcance de la revisi?n

La presente declaraci?n documenta las fuentes utilizadas, las reglas de rastreo observadas y los compromisos ?ticos del equipo.

La revisi?n de robots.txt no sustituye la verificaci?n jur?dica de licencias y t?rminos espec?ficos.

Si se incorporan nuevas fuentes, deber?n documentarse sus condiciones de acceso, reutilizaci?n, atribuci?n y privacidad.
