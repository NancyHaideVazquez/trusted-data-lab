# Observatorio de Vivienda y Costos de Colima

**Proyecto Integrador TRUSTED DATA LAB**
Observatorio de datos certificado. Proyecto integrador de Ingeniería de Datos, Análisis Estadístico y Calidad en los Sistemas de Información. Proyecto de observatorio de datos para la recopilación, almacenamiento y análisis de información histórica.

## Descripción

Este proyecto tiene como objetivo desarrollar un observatorio de datos sobre la evolución de los costos asociados a la vivienda en Colima y Villa de Álvarez, mediante la recopilación, procesamiento y análisis de información económica de fuentes oficiales.

**Pregunta central:** ¿Cómo evolucionan los costos económicos relacionados con la vivienda y las condiciones de financiamiento, y qué información pública permite describir las características y diferencias de vivienda entre Colima, Villa de Álvarez y otras zonas comparables?

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

## Arquitectura y estructura
Se utiliza una arquitectura por capas: Bronce conserva las respuestas originales y metadatos; Plata y Oro se desarrollarán en etapas posteriores. El orquestador coordina los extractores y registra las ejecuciones.

```text
tdl-equipo/
├── docs/
│   ├── EE0/
│   │   ├── propuesta.md
│   │   ├── relatoria-E0.md
│   │   ├── ENTREGA.md
│   │   └── evidencias/
│   ├── E1/
│   ├── E2/
│   ├── E3/
│   └── E4/
├── calidad/
│   ├── tiempo-nancy.csv
│   ├── defectos-nancy.csv
│   ├── tiempo-david.csv
│   └── defectos-david.csv
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
│   └── capturas.csv
├── .github/
│   └── workflows/
│       └── captura.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requisitos e instalación
- Python 3.11 (utilizado en GitHub Actions).
- Git y acceso a Internet para las APIs oficiales.
- Tokens personales vigentes de INEGI y Banxico.

Clonar el repositorio:

```bash
git clone https://github.com/NancyHaideVazquez/trusted-data-lab.git
cd trusted-data-lab
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En Linux o macOS, para activar el entorno virtual utiliza 
```bash
source .venv/bin/activate.
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Para ejecutar localmente, crea .env en la raíz del proyecto, tomando .env.example como referencia si está disponible:

- `INEGI_TOKEN=REEMPLAZAR_CON_TOKEN_REAL`
- `BANXICO_TOKEN=REEMPLAZAR_CON_TOKEN_REAL`
- `TDL_CONTACTO=correo-real-del-equipo@ejemplo.org`

Las APIs de INEGI y Banxico requieren configurar los tokens de acceso correspondientes.

En GitHub para las ejecuciones automáticas se configuran en Settings → Secrets and variables → Actions, los tokens se almacenarán en **GitHub Actions Secrets** con los siguientes nombres:

- `INEGI_TOKEN`
- `BANXICO_TOKEN`

El correo se almacena en Variables. El workflow los inyecta como variables de entorno con el siguiente nombre:
- `TDL_CONTACTO` 

Seguridad: nunca publicar .env, tokens, credenciales ni URLs completas que incluyan un token directamente en el código ni publicarse en el repositorio.

## Ejecución

Una vez implementados y configurados los extractores, la captura podrá ejecutarse mediante:

```bash
python -m extractores.main
```
Descarga del histórico disponible
```bash
python -m extractores.main --historico
```

LoLas capturas se almacenan en `data/bronce/<fuente>/<AAAA-MM-DD>/` y las ejecuciones se registran en logs/capturas.csv. Una captura diaria no implica que la institución publique un nuevo periodo cada día.
La automatización se realizará mediante GitHub Actions.

## Automatización con GitHub Actions
El workflow [`.github/workflows/captura.yml`](.github/workflows/captura.yml) contempla:

- Ejecución programada: 0 12 * * * (12:00 UTC).
- Ejecución manual: workflow_dispatch desde Actions.
- Instalación de Python 3.11 y dependencias.
- Captura con python -m extractores.main.
- Registro y commit de resultados cuando hay archivos nuevos y permisos suficientes.
- Verificación del resultado para detectar fallos de captura.

## Extracción ética, trazabilidad y calidad

extractores/base.py implementa consultas HTTPS con identificación mediante User-Agent, contacto del equipo, pausa mínima de 1.5 segundos por dominio, reintentos limitados ante HTTP 429/5xx y protección de tokens en las URLs registradas. Las consultas a INEGI y Banxico utilizan sus APIs oficiales.

Se revisaron las rutas de los archivos robots.txt de ambas instituciones y sus términos de uso: INEGI y Banco de México. Las rutas de API consultadas no coincidían con las restricciones identificadas; esto no representa autorización general para cualquier extracción. Se atribuirá la información a las instituciones de origen.

Los objetivos iniciales de calidad —metas, no resultados alcanzados— son:
- Disponibilidad de captura ≥ 95 %.
- Completitud de datos ≥ 95 %.
- Cobertura de pruebas automatizadas ≥ 60 %.
- Cero credenciales expuestas en el repositorio (medida complementaria de seguridad).
Cada integrante mantiene registros PSP de tiempo y defectos en calidad/; las evidencias y verificaciones se vinculan en la documentación de cada etapa.

## Documentación y evidencias E0

- [Propuesta del observatorio](docs/E0/propuesta.md): problema, preguntas E1–E3, entrevista y plan de recopilación.
- [Relatoría E0](docs/E0/relatoria-E0.md): cronología, decisiones, defectos y aprendizajes.
- [Ficha técnica de entrega](docs/E0/ENTREGA.md): requisitos y enlaces de evidencia.
- [Evidencias visuales](docs/E0/evidencias/): capturas de ejecución, validaciones, Bronce, entrevista y contribuciones, cuando estén publicadas y autorizadas.
La entrevista de campo se realizó mediante WhatsApp con una persona del sector inmobiliario. Se documentaron sus respuestas y aprendizajes; la duración y modalidad deben consignarse conforme a lo ocurrido y a lo aceptado por los docentes.

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


## Integrantes

- **Nancy:** Data Engineer.
- **David:** Data Statistician.

Ambos integrantes participarán en las actividades de aseguramiento de calidad, revisión cruzada y documentación.

## Estado del proyecto

**Etapa actual: E0 — Arranque.**

Se han comprobado ambas conexiones, el histórico mensual de INEGI y la ejecución manual del workflow. La validación final de la entrega requiere cotejar las evidencias publicadas, registros PSP y ejecución programada posterior.

---

**Proyecto académico — TRUSTED DATA LAB, noviembre-diciembre de 2026.**