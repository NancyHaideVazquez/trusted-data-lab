# Entrega E0 · Observatorio de Vivienda y Costos de Colima

**Equipo:** David Cuevas Farías y Nancy Haide Vázquez Ávalos  
**Etiqueta:** e0  
**Tablero:** No aplica para esta entrega  
**Repositorio:** [https://github.com/NancyHaideVazquez/trusted-data-lab.git](https://github.com/NancyHaideVazquez/trusted-data-lab.git)  
**Fecha:** 8 de noviembre de 2026

## Resumen en tres líneas
El Observatorio de Vivienda y Costos de Colima reúne datos públicos relacionados con vivienda, costos económicos y condiciones financieras para Colima y Villa de Álvarez. La captura inicial utiliza extractores en Python conectados con fuentes oficiales (INEGI y Banco de México), conservando los datos históricos para el planteamiento de los análisis de las siguientes etapas.

## Ingeniería de Datos
| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
| :--- | :--- | :--- |
| **Estructura y organización** | [Repositorio de GitHub](https://github.com/NancyHaideVazquez/trusted-data-lab.git) | El repositorio cuenta con la estructura de carpetas para las capas Bronce, Plata y Oro, además de las carpetas de calidad y documentación. |
| **Extracción de datos de INEGI** | [extractores/inegi.py](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/extractores/inegi.py) y [data/bronce/inegi/](https://github.com/NancyHaideVazquez/trusted-data-lab/tree/main/data/bronce/inegi) | Se capturó el indicador `910402` (nacional, mensual). Se recibieron 182 registros desde agosto de 2011. |
| **Extracción de datos de Banxico** | [extractores/banxico.py](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/extractores/banxico.py) y [data/bronce/banxico/](https://github.com/NancyHaideVazquez/trusted-data-lab/tree/main/data/bronce/banxico) | Se capturó la serie `SF43783` (TIIE a 28 días). Se recibieron 7,955 registros históricos. |
| **Código base y ejecución** | [extractores/base.py](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/extractores/base.py) y [extractores/main.py](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/extractores/main.py) | Ubicaciones del código del proyecto, incluyendo la clase `ExtractorEtico`. |
| **Automatización de captura** | [Ejecución de GitHub Actions](https://github.com/NancyHaideVazquez/trusted-data-lab/actions) | El workflow automatizado fue ejecutado y validado exitosamente. |
| **Bitácora de ejecución** | [logs/capturas.csv](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/logs/capturas.csv) | Registro de ejecuciones del sistema. |

**Aclaración sobre las fuentes:** El indicador INEGI `910402` aporta contexto de inflación de servicios nacional. La serie Banxico `SF43783` es la TIIE a 28 días nacional. Ninguna mide directamente rentas locales, pero aportan contexto macroeconómico.

## Análisis Estadístico
| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
| :--- | :--- | :--- |
| **Preguntas analíticas (E1, E2, E3)** | [docs/E0/propuesta.md](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/docs/E0/propuesta.md) | Se definieron los tres planteamientos analíticos para las siguientes etapas. |
| **E1. Análisis de serie temporal** | [docs/E0/propuesta.md](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/docs/E0/propuesta.md) | Pronóstico de serie mensual a seis meses evaluado con MAE y RMSE. |
| **E2. Experimento factorial** | [docs/E0/propuesta.md](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/docs/E0/propuesta.md) | Diseño factorial 2³ (procesos, parser y formato). |
| **E3. Comparación territorial** | [docs/E0/propuesta.md](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/docs/E0/propuesta.md) | Comparación de viviendas y servicios por municipio (PCA y MANOVA). |
| **Serie histórica identificada** | [data/bronce/](https://github.com/NancyHaideVazquez/trusted-data-lab/tree/main/data/bronce) | Las series descargadas (INEGI 182, Banxico 7955) superan los 36 periodos requeridos. |

## Calidad en los Sistemas de Información
| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
| :--- | :--- | :--- |
| **Registros PSP** | [calidad/](https://github.com/NancyHaideVazquez/trusted-data-lab/tree/main/calidad) | Se incluyen los 4 archivos individuales con registros reales de tiempo y defectos. |
| **Objetivos de calidad** | [docs/E0/propuesta.md](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/docs/E0/propuesta.md) | Metas definidas: Disponibilidad ≥95%, Completitud ≥95%, Cobertura de pruebas ≥60%. |
| **Entrevista de campo** | [docs/E0/propuesta.md](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/docs/E0/propuesta.md) | Realizada vía WhatsApp el 08/11/2026. Aprendizajes documentados. |

## Relatoría de etapa
La relatoría ampliada se encuentra en [docs/E0/relatoria-E0.md](https://github.com/NancyHaideVazquez/trusted-data-lab/blob/main/docs/E0/relatoria-E0.md). Incluye la cronología, decisiones técnicas, defectos encontrados, correcciones y aprendizajes.

## Issues de la entrega anterior
No aplica para la primera entrega.

## Validación final
- [x] URL del repositorio agregada y enlaces clicables.
- [x] Conteo de registros validado.
- [x] GitHub Actions verificado.
- [x] Entrevista de campo realizada y documentada.
- [x] Archivos PSP existentes.
- [x] Planteamientos E1, E2 y E3 incluidos.

---
**Fin de la entrega E0 — Trusted Data Lab**