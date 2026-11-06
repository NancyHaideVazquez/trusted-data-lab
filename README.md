# Observatorio de Vivienda y Costos de Colima

**Proyecto Integrador TRUSTED DATA LAB**
Observatorio de datos certificado. Proyecto integrador de Ingeniería de Datos, Análisis Estadístico y Calidad en los Sistemas de Información. Proyecto de observatorio de datos para la recopilación, almacenamiento y análisis de información histórica.

## Descripción

Este proyecto tiene como objetivo desarrollar un observatorio de datos sobre la evolución de los costos asociados a la vivienda en Colima y Villa de Álvarez, mediante la recopilación, procesamiento y análisis de información económica de fuentes oficiales.

El observatorio permitirá estudiar el comportamiento histórico de indicadores relacionados con rentas, servicios de vivienda, inflación y costo del crédito, así como realizar comparaciones con otras ciudades mexicanas.

El desarrollo integra conocimientos de Ingeniería de Datos, Análisis Estadístico para Ciencia de Datos y Calidad en los Sistemas de Información.

## Objetivo general

Desarrollar un observatorio de datos que integre información económica de fuentes oficiales, aplique técnicas estadísticas para identificar tendencias y realizar pronósticos, y garantice la confiabilidad de sus resultados mediante procesos de validación y aseguramiento de calidad.

## Fuentes de datos

Se utilizarán principalmente dos fuentes oficiales:

- **INEGI:** API de Indicadores para consultar información histórica relacionada con vivienda y economía.
- **Banco de México (Banxico):** API del Sistema de Información Económica (SIE) para consultar indicadores financieros relacionados con el costo del crédito.

Los indicadores específicos se seleccionarán y verificarán durante la etapa inicial.

## Tecnologías

- Python 3.11
- Requests
- Pandas
- Git y GitHub
- GitHub Actions
- Pytest

Se incorporarán herramientas adicionales conforme avancen las etapas del proyecto.

## Estructura del proyecto

```text
tdl-equipo/
├── docs/
│   ├── E0/
│   ├── E1/
│   ├── E2/
│   ├── E3/
│   └── E4/
├── calidad/
├── extractores/
│   ├── __init__.py
│   ├── base.py
│   ├── inegi.py
│   ├── banxico.py
│   └── main.py
├── pipeline/
├── data/
│   ├── bronce/
│   ├── plata/
│   ├── oro/
│   └── cuarentena/
├── laboratorio/
├── tests/
├── logs/
├── .github/
│   └── workflows/
│       └── captura.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Las APIs de INEGI y Banxico requieren configurar los tokens de acceso correspondientes.

Para las ejecuciones automáticas, estos se almacenarán en **GitHub Actions Secrets** con los siguientes nombres:

- `INEGI_TOKEN`
- `BANXICO_TOKEN`

Las credenciales no deben incluirse directamente en el código ni publicarse en el repositorio.

## Ejecución

Una vez implementados y configurados los extractores, la captura podrá ejecutarse mediante:

```bash
python -m extractores.main
```

Los resultados se almacenarán en `data/bronce/`, organizados por fuente y fecha de captura.

La automatización se realizará mediante GitHub Actions.

## Etapas y entregables

El proyecto se desarrolla en cinco entregas que integran las actividades de las tres materias.

| Entrega | Fecha | Entregables principales |
|---|---|---|
| **E0 — Arranque** | 6 de noviembre | Propuesta del observatorio, entrevista, plan de recopilación, dos fuentes funcionando, serie histórica de al menos 36 periodos, captura automática y registros iniciales de calidad. |
| **E1 — Datos de confianza y pronóstico** | 13 de noviembre | Limpieza e integración de datos, capas Plata y Oro, puerta de calidad, modelos de pronóstico, métricas de fiabilidad, plan SQA y pruebas automatizadas. |
| **E2 — Experimento y auditoría** | 23 de noviembre | Fuente especializada, experimento factorial, análisis ANOVA, evaluación ISO/IEC 25010 y 25012, y auditoría cruzada. |
| **E3 — Mapa multivariado y sello** | 30 de noviembre | Análisis PCA y MANOVA, mapa multivariado, optimización del sistema, dataset publicado, cierre de auditoría y solicitud del Sello TDL. |
| **E4 — Demo Day y cierre** | 2 y 4 de diciembre | Presentación del observatorio, demostración en vivo, reporte de inteligencia, reporte técnico final, relatoría final, modelo de negocio y video de presentación. |

### Organización de las entregas

Cada entrega se documentará dentro de `docs/`, utilizando una carpeta independiente.

```text
docs/
├── E0/
│   ├── propuesta.md
│   └── ENTREGA.md
├── E1/
│   └── ENTREGA.md
├── E2/
│   └── ENTREGA.md
├── E3/
│   └── ENTREGA.md
└── E4/
    └── ENTREGA.md
```

El archivo `ENTREGA.md` incluirá las evidencias correspondientes a Ingeniería de Datos, Análisis Estadístico y Calidad en los Sistemas de Información, con enlaces al código, análisis y documentación.

Cada entrega deberá quedar registrada mediante una etiqueta de Git (`e0`, `e1`, `e2`, `e3` y `e4`) para conservar una versión verificable del proyecto.

Las etapas E1, E2 y E3 también incluirán una relatoría de máximo dos páginas, ubicada en `docs/relatoria-E1.md`, `docs/relatoria-E2.md` y `docs/relatoria-E3.md`, respectivamente.

## Calidad y reproducibilidad

El proyecto contempla registros individuales de tiempo y defectos, pruebas automatizadas, bitácoras de ejecución y validación de los datos.

Se conservarán los datos originales y sus metadatos de captura para permitir la trazabilidad de la información.

Los objetivos iniciales de calidad son:

- Disponibilidad de captura de al menos 95%.
- Completitud de datos de al menos 95%.
- Cobertura de pruebas automatizadas de al menos 60%.
- Cero credenciales expuestas en el repositorio.

## Integrantes

- **Nancy:** Data Engineer.
- **David:** Data Statistician.

Ambos integrantes participarán en las actividades de aseguramiento de calidad, revisión cruzada y documentación.

## Estado del proyecto

**Etapa actual: E0 — Arranque.**

El repositorio se encuentra en preparación para implementar la captura de datos históricos, configurar la automatización y documentar las fuentes de información.

---

**Proyecto académico — TRUSTED DATA LAB, noviembre-diciembre de 2026.**