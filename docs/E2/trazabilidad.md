\# Trazabilidad de datos — Entrega E2



\*\*Proyecto:\*\* Observatorio de Vivienda y Costos de Colima  

\*\*Etapa:\*\* E2 — Integración y trazabilidad de datos



\## 1. Objetivo



Documentar la procedencia y transformación de los indicadores económicos utilizados en el observatorio, desde los archivos históricos de Bronce hasta los conjuntos de datos de Plata y Oro.



\## 2. Fuentes de datos



\### INEGI



\- Serie: `910402`

\- Indicador: Inflación mensual

\- Registros: 183

\- Archivo de respaldo: `data/bronce/inegi/2026-11-12/910402\_historico\_130114\_649094\_60dc15f7.json`

\- Fecha de captura UTC: `2026-11-12T13:01:14.639577+00:00`



Se verificó la coincidencia de los 183 valores de la limpieza preliminar con el archivo histórico seleccionado.



\### Banco de México



\- Serie: `SF43783`

\- Indicador: TIIE a 28 días

\- Registros mensuales: 381

\- Archivo de respaldo: `data/bronce/banxico/2026-11-12/SF43783\_historico\_130116\_421967\_754519eb.json`

\- Fecha de captura UTC: `2026-11-12T13:01:16.368744+00:00`



La reducción mensual utiliza el promedio de los valores válidos. Se verificaron 380 promedios contra una captura anterior y el periodo restante, noviembre de 2026, contra la captura del 12 de noviembre, que contiene ocho observaciones y reproduce el promedio de 6.662925.



\## 3. Transformación Bronce → Plata



El procesamiento comprende la limpieza preliminar, reducción mensual de Banxico e integración de ambas fuentes.



El módulo `src/trazabilidad.py` permite consultar las rutas y fechas de captura de los archivos Bronce de respaldo.



El módulo `src/integracion.py` incorpora opcionalmente los campos:



\- `archivo\_origen`: ruta del archivo histórico que respalda los valores.

\- `fecha\_ingesta\_utc`: fecha de captura UTC obtenida del metadato `captured\_at\_utc`.



El archivo `data/plata/integracion\_mensual\_e2.csv` contiene 564 registros y 11 columnas.



La validación se realiza mediante `src/calidad.py`, utilizando Pandera.



\## 4. Transformación Plata → Oro



El módulo `src/oro.py` valida los registros de Plata y conserva las columnas de trazabilidad.



El ejecutor `src/ejecutar\_oro\_e2.py` genera:



`data/oro/indicadores\_mensuales\_e2.csv`



El archivo contiene 564 registros y 10 columnas.



Se comprobó que los 564 valores se conservan durante la transformación de Plata a Oro.



\## 5. Evidencias de calidad



\- 183 valores de INEGI coincidentes con Bronce.

\- 381 periodos mensuales de Banxico identificados.

\- 380 promedios de Banxico coincidentes con la captura del 8 de noviembre.

\- Promedio de noviembre de 2026 reproducido con la captura del 12 de noviembre.

\- 564 registros en Plata E2.

\- 564 registros en Oro E2.

\- Dos referencias de archivos Bronce.

\- Ningún registro con campos de trazabilidad nulos.

\- 145 pruebas automatizadas aprobadas.



\## 6. Limitaciones



Los archivos históricos seleccionados constituyen respaldo verificable de los valores, pero no necesariamente identifican los archivos utilizados en cada ejecución original del procesamiento.



La fecha `fecha\_ingesta\_utc` corresponde al metadato de captura del archivo de respaldo. No representa necesariamente la fecha en que se ejecutaron las transformaciones de Plata u Oro.



Los indicadores económicos de INEGI y Banxico tienen cobertura nacional. Su incorporación al observatorio no implica que sus valores representen mediciones específicas de los municipios de Colima o Villa de Álvarez.



\## 7. Reproducibilidad



Para regenerar las capas E2 desde los archivos intermedios:



```powershell

python -m src.ejecutar\_integracion

python -m src.ejecutar\_oro\_e2

```



Para ejecutar las pruebas:



```powershell

python -m pytest -q

```



La reproducción completa desde Bronce requiere ejecutar previamente los procesos de limpieza y reducción correspondientes.

