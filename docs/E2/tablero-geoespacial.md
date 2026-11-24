
# Tablero interactivo y unión espacial — E2

## 1. Objetivo

Incorporar herramientas de análisis y visualización geoespacial al Observatorio de Vivienda y Costos de Colima, utilizando GeoPandas, Streamlit y Plotly.

## 2. Fuentes de información

| Fuente | Información | Cobertura |
|---|---|---|
| INEGI - Marco Geoestadístico 2026 | Polígonos municipales | Estado de Colima |
| INEGI | Inflación mensual | Nacional |
| Banxico | TIIE a 28 días | Nacional |

Los indicadores económicos nacionales no se interpretan como mediciones municipales.

## 3. Unión espacial

Se implementó el módulo `src/union_espacial.py`, que realiza las siguientes operaciones:

1. Carga los polígonos municipales de la capa Plata.
2. Utiliza el sistema de coordenadas EPSG:4326.
3. Genera puntos representativos interiores.
4. Ejecuta una unión espacial mediante `geopandas.sjoin()`.
5. Utiliza el predicado espacial `within`.
6. Compara las claves municipales esperadas y obtenidas.
7. Conserva la ruta del archivo original y su SHA-256.
8. Exporta los resultados en formato CSV.

### Resultados

| Indicador | Resultado |
|---|---:|
| Municipios procesados | 10 |
| Puntos representativos | 10 |
| Asignaciones correctas | 10 |
| Puntos sin municipio | 0 |
| Porcentaje de asignación correcta | 100% |

El porcentaje corresponde exclusivamente a la validación de puntos derivados de los propios polígonos.

## 4. Tablero interactivo

El tablero fue desarrollado mediante Streamlit y Plotly.

### Mapa territorial

- Visualización de los diez municipios.
- Colima resaltado en azul.
- Villa de Álvarez resaltado en naranja.
- Puntos representativos municipales.
- Filtro territorial interactivo.

### Indicadores económicos

- Visualización de series históricas nacionales.
- Selección de indicadores.
- Filtro por periodo.
- Consulta de registros económicos.
- Indicadores descriptivos.

### Calidad de datos

- Validación de geometrías.
- Resultados de asignación espacial.
- Identificación de claves duplicadas.
- Consulta del sistema de coordenadas.
- Descarga de evidencia geoespacial en CSV.

### Trazabilidad

- Identificación de fuentes.
- Rutas de archivos originales.
- SHA-256 de procedencia geoespacial.
- Fechas de procesamiento.
- Linaje económico desde Oro hasta Bronce.

## 5. Validación técnica

Validación local realizada el 24 de noviembre de 2026.

| Indicador | Resultado |
|---|---|
| Pruebas anteriores | 145 |
| Pruebas nuevas de unión espacial | 10 |
| Pruebas nuevas del tablero | 8 |
| Total de pruebas aprobadas | 163 |
| Pruebas fallidas | 0 |
| Tiempo de ejecución general | 13.07 segundos |
| Ruff | Sin errores |
| Streamlit local | 1.67.0 |
| Plotly local | 6.9.0 |
| Python local | 3.14.3 |

Las pruebas automatizadas del tablero verifican su ejecución, título, pestañas, métricas geoespaciales y filtros territoriales.

La descarga de archivos y la interacción visual con todas las gráficas requieren comprobaciones funcionales adicionales.

## 6. Defectos detectados y corregidos

| Defecto | Solución |
|---|---|
| Plotly no estaba instalado localmente | Instalación de la dependencia |
| Ruta relativa incorrecta en AppTest | Uso de una ruta absoluta basada en pathlib |
| Advertencias de parámetros de Streamlit | Sustitución por width="stretch" |

Se actualizó la versión mínima declarada de Streamlit y se incorporó la carpeta tablero a la revisión automática de Ruff.

La compatibilidad en GitHub Actions con Python 3.11 queda pendiente de verificar mediante la publicación de estos cambios.

## 7. Instrucciones de ejecución

Desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
python -m src.union_espacial
python -m streamlit run tablero/app.py
```

El tablero se encuentra disponible localmente en:

http://localhost:8501

Para consultar las series económicas es necesario generar previamente la capa Oro E2 mediante el pipeline correspondiente.

## 8. Reproducción de pruebas

```bash
python -m ruff check src tests tablero
python -m pytest tests/test_union_espacial.py -v
python -m pytest tests/test_tablero.py -v
python -m pytest -q
```

## 9. Evidencias

- [Código de unión espacial](../../src/union_espacial.py)
- [Código del tablero](../../tablero/app.py)
- [Resultados de unión espacial](../../data/reportes/union_espacial_municipios_e2.csv)
- [GeoPackage municipal](../../data/plata/municipios_colima_2026.gpkg)
- [Pruebas geoespaciales](../../tests/test_union_espacial.py)
- [Pruebas del tablero](../../tests/test_tablero.py)
- [Dependencias](../../requirements.txt)
- [Configuración de GitHub Actions](../../.github/workflows/calidad-e1.yml)

Las capturas visuales se incorporarán como evidencia complementaria.

## 10. Limitaciones

Los puntos representativos se generan a partir de los polígonos municipales oficiales. No corresponden a viviendas, establecimientos ni observaciones económicas independientes.

La unión espacial demuestra el procedimiento de asignación territorial, pero no constituye una integración de observaciones georreferenciadas independientes.

Las series económicas conservan su cobertura nacional.

La fecha exacta de ingesta del archivo geoespacial original no fue recuperada. Se conserva la evidencia de descarga estimada, el primer commit y la verificación SHA-256.

## 11. Conclusión

Se implementó un tablero interactivo que permite consultar información territorial, indicadores económicos nacionales, métricas de calidad y procedencia de datos.

La validación local obtuvo 163 pruebas aprobadas y ninguna incidencia de Ruff.

## 12. Uso de inteligencia artificial

Se utilizó ChatGPT como apoyo para desarrollar el código, diseñar las pruebas, diagnosticar errores y preparar la documentación técnica.

Los resultados reportados corresponden a ejecuciones realizadas en el entorno local del proyecto.
