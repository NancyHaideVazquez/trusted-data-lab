# Relatoría E2 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima

**Equipo:** David Cuevas Farías y Nancy Haide Vázquez Ávalos

**Etapa:** E2 — Procesamiento geoespacial, trazabilidad, análisis estadístico, ética y evaluación de calidad

**Periodo documentado:** 22–23 de noviembre de 2026

**Fecha de actualización:** 23 de noviembre de 2026

**Repositorio:** https://github.com/NancyHaideVazquez/trusted-data-lab

**Rama principal de integración:** `main`

---

## 1. ¿Qué nos propusimos?

Durante la etapa E2 del proyecto Trusted Data Lab, el equipo continuó desarrollando el Observatorio de Vivienda y Costos de Colima, fortaleciendo el procesamiento de información, la integración de fuentes, el análisis estadístico y la calidad de los datos.

El propósito principal fue incorporar información geoespacial oficial, mejorar la trazabilidad entre las capas Bronce, Plata y Oro, desarrollar experimentos estadísticos y establecer mecanismos de verificación que permitan utilizar los resultados de manera reproducible y responsable.

Los objetivos establecidos fueron:

1. Incorporar información del Marco Geoestadístico municipal 2026 del INEGI.
2. Procesar los límites municipales de Colima mediante herramientas geoespaciales.
3. Generar un mapa de los municipios de Colima y Villa de Álvarez.
4. Mejorar la integración de información entre las capas Bronce, Plata y Oro.
5. Incorporar mecanismos de trazabilidad para identificar el origen de los registros.
6. Verificar las transformaciones mediante pruebas automatizadas.
7. Documentar los principios éticos y las limitaciones de los datos.
8. Desarrollar experimentos factoriales para evaluar el comportamiento del procesamiento de datos.
9. Comparar diseños factoriales completos y fraccionados.
10. Fortalecer la documentación técnica y los registros de calidad del proyecto.

Para organizar el trabajo se establecieron dos áreas complementarias de responsabilidad: implementación técnica y validación de calidad.

## 2. ¿Qué hicimos? Cronología del trabajo

### 2.1 Organización de responsabilidades

El equipo está integrado por David Cuevas Farías y Nancy Haide Vázquez Ávalos.

Para el desarrollo y cierre de E2 se estableció la siguiente distribución:

| Integrante | Área de responsabilidad | Actividades |
|---|---|---|
| David Cuevas Farías | Implementación técnica | Incorporación de datos geográficos, desarrollo de scripts, integración de información, experimentos estadísticos y generación de productos |
| Nancy Haide Vázquez Ávalos | Validación y aseguramiento de calidad | Revisión de fuentes, comprobación de resultados, auditoría de trazabilidad, verificación de pruebas y revisión documental |

Esta distribución busca mantener un equilibrio entre la construcción de los componentes y la revisión de su calidad.

Las actividades técnicas cuentan con evidencia en Git. Las actividades individuales de validación deben respaldarse con sus respectivos resultados y registros PSP.

### 2.2 Actividades técnicas documentadas

El historial de Git registra los siguientes avances de la etapa E2:

| Etapa | Actividad | Commit |
|---|---|---|
| G01 | Incorporación del Marco Geoestadístico municipal 2026 en Bronce | `b4fe64f` |
| G02 | Implementación del procesamiento geoespacial y pruebas | `8ef0ae2` |
| G03 | Generación del mapa municipal de Colima y Villa de Álvarez | `6f79137` |
| G04 | Incorporación de trazabilidad Bronce–Plata–Oro | `ce8b16a` |
| G05 | Documentación de ética y uso responsable de datos | `1a8adcf` |
| G06 | Elaboración del documento de entrega E2 | `d93ef88` |
| G07 | Elaboración de la relatoría y actualización de la entrega | `9fd82f6` |
| G08 | Desarrollo del experimento factorial 2³ y análisis estadístico | `892c21f` |
| G09 | Comparación de diseños factoriales 2⁴ y 2⁴⁻¹ | `01f2421` |
| G10 | Corrección de importaciones y cumplimiento de Ruff | `2622d2e` |
| G11 | Documentación del ANOVA del experimento factorial 2³ | `3e359ef` |

Los commits permiten verificar los cambios registrados en el repositorio. No constituyen por sí mismos un registro de las horas dedicadas a cada actividad.

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

### 2.6 Experimento factorial completo 2³

Se desarrolló un experimento factorial completo 2³ para evaluar el comportamiento del flujo de integración de datos.

El objetivo fue analizar cómo influyen tres factores en el tiempo de procesamiento:

| Factor | Nivel bajo (-1) | Nivel alto (+1) |
|---|---|---|
| A: Cantidad de registros | 200 | 500 |
| B: Trazabilidad | Desactivada | Activada |
| C: Validación Pandera | Desactivada | Activada |

El diseño contempla ocho tratamientos y dos réplicas por tratamiento, para un total de 16 corridas experimentales.

Se realizaron dos tandas:

- Primera tanda: 16 corridas iniciales sin calentamiento previo.
- Segunda tanda: ocho ejecuciones de calentamiento y posteriormente 16 corridas de confirmación.

Las combinaciones se ejecutaron en orden aleatorizado utilizando la semilla 2026.

El tiempo se midió mediante `perf_counter_ns()` de Python. La lectura de los archivos CSV y la preparación de las muestras quedaron fuera del intervalo medido.

#### Resultados del ANOVA 2³ de confirmación

| Factor o interacción | Efecto (ms) | Valor p | Interpretación |
|---|---:|---:|---|
| A | +1.4528 | 0.083061 | No significativo |
| B | +7.4401 | 0.000008 | Significativo |
| A×B | -0.4013 | 0.599367 | No significativo |
| C | +13.7474 | 0.000000068 | Significativo |
| A×C | -0.0152 | 0.983980 | No significativo |
| B×C | +0.6679 | 0.389304 | No significativo |
| A×B×C | -1.2462 | 0.127873 | No significativo |

Los resultados muestran que la trazabilidad y la validación Pandera tuvieron efectos estadísticamente significativos sobre el tiempo de procesamiento en las condiciones evaluadas.

El factor A, correspondiente a la cantidad de registros, no alcanzó significancia estadística al nivel de 0.05.

#### Diagnóstico del modelo

| Indicador | Resultado |
|---|---:|
| R² | 0.9830 |
| R² ajustado | 0.9681 |
| Desviación residual | 1.4675 ms |
| Shapiro-Wilk W | 0.915498 |
| Shapiro-Wilk p | 0.142733 |

La prueba Shapiro-Wilk no proporcionó evidencia suficiente para rechazar la normalidad de los residuos en la tanda de confirmación.

#### Comparación entre las tandas

En la primera tanda se registró un tiempo extremo de 168.756 ms.

El análisis inicial presentó:

- R² = 0.5574.
- Desviación residual = 35.3814 ms.
- Shapiro-Wilk p = 0.000016.

En la tanda de confirmación, el tiempo máximo registrado fue de 29.1671 ms.

La segunda tanda presentó menor variabilidad. El calentamiento pudo contribuir a esta diferencia, aunque no se ha demostrado que fuera su única causa.

Las conclusiones se limitan a las condiciones experimentales evaluadas y a las dos réplicas por tratamiento.

#### Evidencias del experimento

Código:

- `src/experimento_factorial_e2.py`
- `src/analisis_factorial_2_3_e2.py`
- `src/graficas_factorial_e2.py`

Resultados:

- `data/reportes/experimento_factorial_e2.csv`
- `data/reportes/experimento_factorial_e2_original.csv`
- `data/reportes/experimento_factorial_e2_confirmacion.csv`
- `data/reportes/anova_factorial_2_3.csv`

Documentación:

- `docs/E2/analisis_estadistico/experimento_factorial_2_3.md`

### 2.7 Comparación de diseños factoriales 2⁴ y 2⁴⁻¹

Se desarrolló una segunda actividad estadística para comparar un diseño factorial completo 2⁴ con un diseño factorial fraccionado 2⁴⁻¹.

El propósito fue evaluar la capacidad de ambos diseños para identificar efectos sobre el tiempo de procesamiento, considerando cuatro factores experimentales.

Se trabajó con los siguientes factores:

- A: cantidad de registros.
- B: trazabilidad.
- C: validación Pandera.
- D: generación de un resumen estadístico del resultado integrado.

Los niveles experimentales fueron:

| Factor | Nivel bajo (-1) | Nivel alto (+1) |
|---|---|---|
| A | 200 registros | 500 registros |
| B | Trazabilidad desactivada | Trazabilidad activada |
| C | Pandera desactivada | Pandera activada |
| D | Generación del resumen desactivada | Generación del resumen activada |

El factor D se implementó mediante la función `generar_resumen(integrado)`, que calcula la cantidad de registros, el promedio, el mínimo y el máximo de la columna de valores.

#### Diseño factorial completo 2⁴

El diseño completo considera 16 combinaciones factoriales y dos réplicas, para un total de 32 corridas.

Se utilizó un modelo factorial completo para evaluar los efectos principales y las interacciones entre los cuatro factores.

#### Resultados de efectos principales

| Factor | Efecto estimado (ms) | Valor p | Interpretación |
|---|---:|---:|---|
| A | +1.5826 | 0.017880 | Significativo |
| B | +7.9747 | <0.001 | Significativo |
| C | +15.0554 | <0.001 | Significativo |
| D | -0.7806 | 0.211544 | No significativo |

La validación Pandera (C) presentó el mayor efecto estimado sobre el tiempo de procesamiento, seguida por la trazabilidad (B).

La cantidad de registros (A) también presentó significancia estadística en este diseño. La generación del resumen estadístico (D) no mostró evidencia suficiente de un efecto significativo.

#### Interacciones significativas

Se identificaron las siguientes interacciones con un nivel de significancia de 0.05:

| Interacción | Efecto estimado (ms) | Valor p |
|---|---:|---:|
| B×C | +1.3090 | 0.044326 |
| C×D | -1.5591 | 0.019360 |
| B×C×D | -1.4362 | 0.029237 |

Las interacciones indican que el efecto de algunos factores puede variar dependiendo de la combinación de niveles de otros factores.

#### Diagnóstico del modelo completo

- R² = 0.9814.
- R² ajustado = 0.9640.
- Desviación residual = 1.6964 ms.
- Shapiro-Wilk W = 0.943642.
- Shapiro-Wilk p = 0.095015.

El modelo explicó aproximadamente el 98.14 % de la variabilidad observada en el tiempo de procesamiento.

La prueba Shapiro-Wilk no mostró evidencia suficiente para rechazar la normalidad de los residuos al nivel de significancia de 0.05.

#### Diseño factorial fraccionado 2⁴⁻¹

Para reducir el esfuerzo experimental se construyó una fracción de resolución IV, utilizando el generador:

**D = ABC**

Su relación definitoria es:

**I = ABCD**

Este diseño conserva ocho tratamientos de los 16 posibles y mantiene dos réplicas por tratamiento, para un total de 16 corridas.

La reducción permite evaluar los factores principales y determinadas interacciones con la mitad de las ejecuciones del diseño completo.

El modelo utilizado fue:

`tiempo_ms ~ A + B + C + D + A:B + A:C + A:D`

Se estimaron siete contrastes independientes.

#### Resultados del diseño fraccionado

| Efecto estimado | Alias | Efecto (ms) | Valor p |
|---|---|---:|---:|
| A | A = BCD | +0.1464 | 0.749820 |
| B | B = ACD | +7.4573 | <0.000001 |
| C | C = ABD | +14.4215 | <0.000001 |
| D | D = ABC | -0.3164 | 0.495902 |
| A×B | AB = CD | -1.2311 | 0.024085 |
| A×C | AC = BD | -0.0253 | 0.955911 |
| A×D | AD = BC | +1.5458 | 0.008256 |

Los resultados identificaron efectos significativos en B, C, A×B y A×D.

Sin embargo, debido a la estructura de alias, las interacciones estimadas no pueden atribuirse de manera independiente a un solo efecto.

Por ejemplo, el contraste AB también representa CD, mientras que AD representa BC.

Por lo tanto, los resultados del diseño fraccionado deben interpretarse considerando la confusión entre efectos.

#### Diagnóstico del modelo fraccionado

- R² = 0.9942.
- R² ajustado = 0.9890.
- Desviación residual = 0.8871 ms.
- Shapiro-Wilk W = 0.995479.
- Shapiro-Wilk p = 0.999999.

La prueba Shapiro-Wilk no proporcionó evidencia suficiente para rechazar la normalidad de los residuos. Estos indicadores describen el ajuste del modelo en las corridas evaluadas, pero no eliminan las limitaciones ocasionadas por el alias.

#### Comparación del esfuerzo experimental

| Característica | Completo 2⁴ | Fraccionado 2⁴⁻¹ |
|---|---:|---:|
| Factores | 4 | 4 |
| Tratamientos | 16 | 8 |
| Réplicas | 2 | 2 |
| Corridas | 32 | 16 |
| Reducción de corridas | Referencia | 50 % |

El diseño fraccionado permite reducir a la mitad el número de corridas, aunque ofrece menor capacidad para separar efectos debido a su estructura de alias.

#### Interpretación general de la comparación

El diseño completo permite estudiar los efectos principales y las interacciones incluidas en el modelo sin la confusión propia de la fracción seleccionada.

El diseño fraccionado requiere interpretar los efectos estimados de acuerdo con sus alias.

La comparación permitió identificar que ambos diseños pueden aportar información útil, pero su elección depende del esfuerzo experimental disponible y del nivel de detalle requerido.

Los resultados de significancia no deben interpretarse como equivalentes entre ambos diseños, debido a que sus modelos y estructuras experimentales son diferentes.

#### Evidencias de la comparación

Código:

- `src/experimento_factorial_2_4_e2.py`
- `src/analisis_factorial_2_4_e2.py`
- `src/analisis_fraccionado_2_4_e2.py`
- `src/comparacion_factorial_2_4_e2.py`
- `src/graficas_comparacion_2_4_e2.py`

Resultados:

- `data/reportes/experimento_factorial_2_4_completo.csv`
- `data/reportes/experimento_factorial_2_4_fraccionado.csv`
- `data/reportes/anova_factorial_2_4_completo.csv`
- `data/reportes/anova_factorial_2_4_fraccionado.csv`
- `data/reportes/comparacion_factorial_2_4.csv`

Gráficas:

- `data/reportes/graficas_comparacion_2_4/01_efectos_principales.png`
- `data/reportes/graficas_comparacion_2_4/02_significancia_estadistica.png`
- `data/reportes/graficas_comparacion_2_4/03_numero_corridas.png`

Documentación:

- `docs/E2/analisis_estadistico/comparacion_factorial_2_4.md`

### 2.8 Validación y aseguramiento de calidad

Para el cierre de E2 se contempló la revisión de los siguientes aspectos:

- Correspondencia entre las fuentes originales y los metadatos.
- Verificación de que el GeoPackage contenga los diez municipios esperados.
- Revisión de la representación de Colima y Villa de Álvarez en el mapa.
- Comprobación de los campos de procedencia de los registros.
- Conservación de registros entre Plata y Oro.
- Ejecución de pruebas automatizadas.
- Revisión de la coherencia entre los documentos de entrega, trazabilidad, ética y relatoría.

Durante la validación técnica del código se ejecutaron los siguientes comandos:

`python -m py_compile src/analisis_factorial_2_3_e2.py`

El script compiló correctamente.

`python -m ruff check src tests --output-format concise`

Resultado:

`All checks passed!`

También se ejecutaron las pruebas automatizadas:

`python -m pytest -q`

Resultado:

**145 pruebas aprobadas.**

Finalmente, se verificó la consistencia de los cambios documentales mediante:

`git diff --check`

La última revisión realizada no reportó errores de espacios en blanco ni problemas de formato en los cambios revisados.

Se realizaron verificaciones técnicas sobre los componentes desarrollados por David. Las revisiones individuales asignadas a Nancy deben respaldarse con sus propias evidencias.

### 2.9 Registro de tiempos PSP

El repositorio contiene los archivos:

- `calidad/tiempo-david.csv`
- `calidad/tiempo-nancy.csv`

Para David se preparó un registro estimado de las actividades G01–G07 realizadas durante el desarrollo de E2.

El registro inicial G01–G07 comprendió 270 minutos efectivos y 45 minutos de interrupciones. Las actividades adicionales se incorporaron posteriormente al PSP; el total actualizado se detalla en la sección 2.10.

Los horarios individuales se reconstruyeron a partir de estimaciones y no corresponden a una medición minuto a minuto.

Los registros PSP deben mantenerse actualizados conforme se realicen nuevas actividades.

### 2.10 Cronología complementaria y actualización PSP

| Fecha | Actividad | Ejecución documentada | Minutos efectivos estimados |
|---|---|---|---:|
| 22/11/2026 | G01–G07 | David | 270 |
| 22/11/2026 | G08 — Factorial 2³ | David | 30 |
| 22/11/2026 | G09 — Comparación 2⁴ | David | 30 |
| 22/11/2026 | G10 — Ruff | David | 30 |
| 22/11/2026 | G11 — ANOVA | David | 30 |
| 22/11/2026 | Entrega y relatoría | David | 30 |
| 22/11/2026 | Ética y legalidad | David | 15 |
| 23/11/2026 | Q02 — ISO 25012 | David | 30 |
| 23/11/2026 | Q01 — ISO 25010 | David en apoyo a Nancy | 30 |
| 23/11/2026 | Q03 — Normas | David en apoyo a Nancy | 45 |
| 23/11/2026 | X03 — ANOVA 3×2 | David | 20 |
| 23/11/2026 | Factorial 2³ con bloques | David | 25 |
| 23/11/2026 | Q03 — Actualización bibliográfica | David | 20 |
| 23/11/2026 | X05 — Confirmación experimental | David | 22 |
| 23/11/2026 | Corrección BLE001 y validación Ruff | David | 30 |
| | Total efectivo | | 657 |

Se registraron 105 minutos acumulados de descansos e interrupciones, para un total estimado de 762 minutos (12 h 42 min), de los cuales 657 minutos (10 h 57 min) corresponden a trabajo efectivo. El incremento fue de 117 minutos efectivos y 15 minutos de descanso. El CSV contiene 36 registros acumulados de E0–E2, incluidos descansos. No se inventaron horarios exactos para las actividades adicionales.

Las verificaciones G05–G07 documentadas en `docs/E2/validacion-calidad.md` suman 75 minutos estimados de apoyo de David; no se agregan nuevamente al total ni se atribuyen a Nancy. Nancy confirmó sus contribuciones personales y los tiempos estimados de su PSP.

### 2.11 Q01 — Evaluación del producto ISO/IEC 25010

La evaluación utiliza las ocho características solicitadas, distingue las ediciones 2011 y 2023 y documenta métricas, metas, resultados, evidencia y limitaciones. La preparación inicial fue realizada por David en apoyo a la actividad asignada a Nancy.

| Característica | Resultado observado | Alcance |
|---|---|---|
| Adecuación funcional | 145 pruebas aprobadas | No equivale a cobertura de todos los requisitos |
| Eficiencia | 13.9944 ms promedio; 517.5033 KiB promedio | Diez lecturas de 564 registros; memoria rastreada por Python |
| Compatibilidad | 5/5 comprobaciones | Pandas, DuckDB, JSON, GeoPackage y PNG |
| Interacción | 5/5 tareas | Un evaluador interno, sin usuarios externos |
| Fiabilidad | 8/10 ejecuciones de calidad exitosas | Ventana Actions #24–33; meta propuesta 95 % no alcanzada |
| Seguridad | 0 vulnerabilidades conocidas en resolución de requirements.txt | Auditoría global con hallazgos; sin Gitleaks |
| Mantenibilidad | 823/2261 sentencias cubiertas (36.4 %); Ruff aprobado | Cobertura limitada |
| Portabilidad | 2/2 entornos comprobados | Windows Python 3.14.3 y CI Ubuntu Python 3.11; alcance parcial |

La auditoría del entorno general reportó 9 paquetes afectados y 78 hallazgos, que pueden incluir duplicados y dependencias ajenas al proyecto. La auditoría de requisitos resolvió 162 paquetes sin vulnerabilidades conocidas reportadas. No constituye una garantía de seguridad.

La prueba del mapa comprobó apertura, identificación de Colima y Villa de Álvarez, comprensión de la leyenda y legibilidad. No representa una evaluación externa de usabilidad.

Los registros de captura mostraron 106 ejecuciones registradas como exitosas, incluyendo ejecuciones locales o manuales; no se interpretan como cumplimiento continuo de la programación de Actions.

El informe se publicó en `5299de2` y su revisión individual por Nancy permanece pendiente.

### 2.12 Q02 — Calidad de datos ISO/IEC 25012:2008

David evaluó las quince características mediante mediciones directas e indicadores aproximados, distinguiendo calidad inherente y dependiente del sistema.

| Característica | Evidencia o resultado | Limitación |
|---|---|---|
| Exactitud | 564/564 coincidencias Bronce–Oro | Tolerancia numérica 1e-9 |
| Completitud | 5640/5640 celdas | Diez columnas Oro |
| Consistencia | 564/564 registros | Reglas de periodo, valor y unicidad |
| Credibilidad | 564/564 identificaciones | Identificación de fuente y serie |
| Actualidad | INEGI: 3 días entre actualización y captura | Banxico sin fecha de publicación verificada |
| Accesibilidad | 2/2 archivos locales | No prueba acceso externo |
| Conformidad | 564/564 filas Plata con Pandera | Reglas implementadas |
| Confidencialidad | 4/4 patrones de exclusión comprobados | No es un escaneo de secretos |
| Eficiencia | 23.9783 ms de lectura | Una medición |
| Precisión | 564/564 valores conservados Plata–Oro | No mide precisión instrumental |
| Trazabilidad | 564/564 referencias; 2 hashes SHA-256 | Hashes como línea base |
| Comprensibilidad | 4 documentos existentes | No mide comprensión de usuarios |
| Disponibilidad | 2/2 archivos leídos | Disponibilidad local puntual |
| Portabilidad | 564 filas en lectura de retorno CSV | No cubre todos los entornos |
| Recuperabilidad | 564/564 valores reconstruidos desde Bronce | No equivale a restauración integral |

La comparación directa incluyó 381 registros de Banxico y 183 de INEGI. Para Banxico se calcularon promedios mensuales de observaciones numéricas; para INEGI se conservaron los valores mensuales originales. La diferencia máxima de Banxico fue aproximadamente 7.11e-15 y la de INEGI fue cero.

La antigüedad de la captura seleccionada fue aproximadamente 11.37 días al momento de la evaluación; no debe confundirse con retraso de publicación.

Se publicaron el script de métricas, los CSV de resultados y el informe en `8f42839`, con corrección de formato en `e2c8cb0`. La revisión por Nancy queda pendiente.

### 2.13 Q03 — Antecedentes normativos

Se documentaron las siguientes referencias y su relación con el proyecto:

| Norma | Aplicación |
|---|---|
| ISO/IEC 9126-1:2001 | Antecedente del modelo de calidad de software |
| ISO/IEC 25000:2014 | Familia SQuaRE |
| ISO/IEC 25010:2011 y 2023 | Calidad del producto y evolución del modelo |
| ISO/IEC 25012:2008 | Calidad de datos |
| ISO 9001:2015 e ISO 9000:2015 | Gestión de calidad y mejora de procesos |

Se relacionaron las normas con pruebas, trazabilidad, métricas, riesgos y registros PSP. No se declara certificación. El documento inicial se publicó en `ce79abf`. El 23 de noviembre David incorporó referencias a fichas oficiales de ISO y notas sobre ediciones y antecedentes. La actualización está disponible localmente en `docs/E2/calidad/antecedentes_normativos.md`; no implica lectura íntegra de las normas ni certificación. La revisión de Nancy permanece pendiente.

### 2.14 Q04 — Auditoría cruzada

La actividad se pospuso hasta conocer las indicaciones de la profesora Isis y el equipo asignado. No se han emitido ni recibido hallazgos de auditoría cruzada documentados. Cuando se realice, se registrarán criterio, evidencia, severidad, impacto, acción, responsable y cierre verificable.

### 2.15 X03 — ANOVA de dos factores 3×2

David realizó 12 corridas medidas: tres niveles de procesos (1, 2 y 4), dos formatos (CSV y Parquet) y dos réplicas por combinación. Se utilizaron 564 registros integrados, calentamiento y orden aleatorizado. El intervalo medido incluye creación y cierre del pool de procesos, escritura, lectura y concatenación; no incluye preparación de particiones ni comprobación de equivalencia.

| Procesos | CSV promedio (ms) | Parquet promedio (ms) |
|---:|---:|---:|
| 1 | 1235.6301 | 1238.1061 |
| 2 | 1223.3481 | 1259.6919 |
| 4 | 1337.1796 | 1389.7390 |

| Término | gl | F | p |
|---|---:|---:|---:|
| Procesos | 2 | 23.018435 | 0.001533 |
| Formato | 1 | 3.108528 | 0.128343 |
| Interacción | 2 | 0.729343 | 0.520555 |
| Residual | 6 | — | — |

El número de procesos presentó significancia al nivel 0.05, condicionada a los supuestos del modelo. El formato y la interacción no presentaron evidencia suficiente de significancia. Dos procesos con CSV obtuvieron el menor promedio exploratorio. Las salidas fueron equivalentes en las 12 corridas.

El modelo presentó R² = 0.894001 y Shapiro-Wilk p = 0.995404. La prueba de Levene resulta degenerada con dos observaciones por celda; no permite concluir de manera fiable sobre homogeneidad. No se midió memoria ni rendimiento del pipeline completo.

Informe: [ANOVA 3×2](E2/analisis_estadistico/anova_3_2.md).

### 2.16 Factorial 2³ con bloques

Se ejecutaron dos bloques completos de ocho tratamientos cada uno, mediante invocaciones separadas de Python, con calentamiento y aleatorización independiente por bloque. Los factores fueron cantidad de registros (A), trazabilidad (B) y validación Pandera (C). Se ajustó un modelo factorial con efecto aditivo de bloque.

| Término | Efecto (ms) | p |
|---|---:|---:|
| Bloque | — | 0.706440 |
| A | 2.438212 | 0.282944 |
| B | 14.257538 | 0.000253 |
| C | 27.830038 | 0.000003 |
| AB | -0.246187 | 0.909820 |
| AC | 2.213262 | 0.326179 |
| BC | 1.805437 | 0.417668 |
| ABC | 0.312663 | 0.885653 |

B y C fueron significativos; no se encontró evidencia suficiente de efecto de bloque. R² = 0.969939, desviación residual = 4.19303 ms y Shapiro-Wilk p = 0.323063. Los dos bloques no representan equipos o entornos diferentes y no permiten generalizar a otras condiciones.

Informe: [Factorial con bloques](E2/analisis_estadistico/experimento_factorial_bloques.md).

### 2.17 X05 — Confirmación experimental

Se comparó la línea base de un proceso con CSV frente a la candidata de dos procesos con CSV, seleccionada a partir de X03. Se realizaron diez pares aleatorizados (20 corridas nuevas), con calentamiento y los mismos 564 registros. La línea base se definió antes de la confirmación, después de la exploración.

| Indicador | Resultado |
|---|---:|
| Promedio línea base | 3204.85569 ms |
| Promedio candidata | 3323.02324 ms |
| Diferencia base menos candidata | -118.16755 ms |
| Mejora relativa | -3.687141 % |
| IC 95 % de la diferencia | [-176.426822, -59.908278] ms |
| t pareada (9 gl) | -4.588344 |
| Valor p | 0.001312 |
| Corridas exitosas | 20/20 |
| Errores | 0 |
| Checksums distintos | 1 |

La candidata fue aproximadamente 3.69 % más lenta; la línea base fue más rápida en nueve de diez pares. Se decidió conservar un proceso con CSV para este escenario, sin modificar el pipeline. El checksum lógico SHA-256 común fue `0d521727ffc75e8555c2ac2f3ce32334dee13a779b1bc977134661a9ea6140d5`.

La sobrecarga de procesos es una explicación posible, no medida por separado. La prueba pareada no contó con comprobación formal de sus supuestos; los resultados corresponden a una sesión local y no se combinan con los tiempos exploratorios.

Informe: [Confirmación X05](E2/analisis_estadistico/confirmacion_experimental_x05.md).

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

### 3.7 Utilizar diseños factoriales

Se decidió utilizar experimentos factoriales para estudiar simultáneamente varios factores que pueden influir en el tiempo de procesamiento.

El diseño 2³ permitió analizar tres factores y sus interacciones.

Posteriormente, la comparación 2⁴ frente a 2⁴⁻¹ permitió estudiar la diferencia entre un diseño completo y uno fraccionado.

La elección de ambos diseños permitió comparar el nivel de información obtenido frente al esfuerzo experimental necesario.

### 3.8 Incorporar la generación de resúmenes como factor experimental

En la comparación factorial 2⁴ se incorporó un cuarto factor, correspondiente a la generación de un resumen estadístico.

Esta decisión permitió evaluar si calcular la cantidad de registros, el promedio, el mínimo y el máximo del resultado integrado incrementaba el tiempo de procesamiento.

Los resultados del diseño completo no mostraron evidencia suficiente de un efecto significativo para este factor.

### 3.9 Confirmar el rendimiento antes de cambiar la configuración

Se descartó adoptar automáticamente la candidata de X03. X05 mostró que dos procesos con CSV no mejoraron el tiempo frente a uno. Se mantuvo la configuración de referencia para el escenario evaluado, preservando la equivalencia de los datos y sin desactivar controles de calidad del pipeline.

### 3.10 Separar bloques y conservar evidencias

Se ejecutaron bloques completos independientes en orden aleatorio para considerar variaciones entre sesiones de ejecución. Se conservaron los resultados originales y se documentaron los límites de la inferencia con pocas réplicas.

## 4. ¿Qué salió mal y cómo lo atendimos?

### 4.1 Diferencias entre la escala territorial y los indicadores económicos

**Situación:** la información geográfica permite identificar municipios, mientras que los indicadores económicos disponibles corresponden a series nacionales.

**Tratamiento:** se documentó que los valores nacionales no deben interpretarse directamente como mediciones municipales.

**Resultado:** se estableció una limitación explícita para evitar interpretaciones estadísticas incorrectas.

### 4.2 Necesidad de fortalecer la trazabilidad

**Situación:** era necesario identificar las fuentes de respaldo y distinguir los datos originales de los transformados.

**Tratamiento:** se incorporaron campos de procedencia y se elaboró documentación específica de trazabilidad.

**Resultado:** se fortaleció la posibilidad de revisar el origen de los registros procesados.

### 4.3 Variabilidad en las mediciones experimentales

**Situación:** durante la primera tanda del experimento factorial 2³ se registró un tiempo extremo de 168.756 ms.

**Tratamiento:** se realizó una segunda tanda con ocho ejecuciones de calentamiento antes de medir las 16 corridas de confirmación.

**Resultado:** la segunda tanda presentó menor variabilidad y mejores indicadores de diagnóstico del modelo.

La diferencia observada no permite afirmar que el calentamiento fuera la única causa de la mejora.

### 4.4 Interpretación de los diseños fraccionados

**Situación:** el diseño factorial fraccionado 2⁴⁻¹ presenta efectos confundidos por su estructura de alias.

**Tratamiento:** se documentaron las relaciones de alias y se compararon los resultados con el diseño completo 2⁴.

**Resultado:** se identificó la reducción del esfuerzo experimental y la limitación para separar determinados efectos.

### 4.5 Archivos derivados no versionados

**Situación:** los productos generados en Plata y Oro no necesariamente se incluyen en los archivos versionados de Git.

**Tratamiento:** se mantuvieron los scripts que permiten reproducir los resultados y se documentaron las rutas de salida.

**Resultado:** se conserva la posibilidad de regenerar los productos derivados.

### 4.6 Advertencias de formato en la documentación y código

**Situación:** durante la preparación de los documentos y scripts se identificaron aspectos de formato y ordenamiento de importaciones.

**Tratamiento:** se realizaron correcciones mediante Ruff y se revisaron los cambios antes de integrarlos.

**Resultado:** se obtuvo una revisión satisfactoria de Ruff y se mantuvo la estructura del proyecto.

### 4.7 Registros PSP pendientes de completar

**Situación:** los registros PSP existentes no contenían inicialmente todas las actividades de E2.

**Tratamiento:** se preparó el registro estimado de David y se identificó la necesidad de incorporar las actividades de validación correspondientes a Nancy.

**Resultado:** el seguimiento de tiempos de E2 se encuentra parcialmente actualizado y requiere completar las evidencias individuales pendientes.

### Registro de defectos

Los archivos de defectos del proyecto son:

- `calidad/defectos-david.csv`
- `calidad/defectos-nancy.csv`

Los defectos anteriores a E2 se conservan como antecedentes del proyecto.

Los problemas descritos en esta relatoría no se consideran automáticamente defectos PSP. Su incorporación al registro requiere identificar la fecha, clasificación, fase y tiempo real de corrección.

### 4.8 Defectos PSP de E2 registrados por David

| Número | Fecha | Defecto | Corrección |
|---|---|---|---|
| 6 | 22/11 | Espacios finales en ENTREGA.md | Revisión y corrección de formato |
| 7 | 22/11 | Imports desordenados | Ruff; `2622d2e` |
| 8 | 23/11 | Formato final de iso25012.md | `e2c8cb0` |
| 9 | 23/11 | Push rechazado por capturas remotas | Pull con rebase y push |
| 10 | 23/11 | DuckDB no disponible | Instalación y lectura de 564 registros |

| 11 | 23/11 | Ruff BLE001 en X05 | Excepción localizada con `# noqa: BLE001` y validación general de Ruff |

El registro histórico de David contiene once defectos, seis correspondientes a E2. Los 30 minutos de corrección y validación se registraron como actividad estimada; el tiempo exclusivo del defecto 11 quedó vacío. Los tiempos desconocidos no se inventaron. El PSP de Nancy conserva 21 defectos históricos y cuenta con la confirmación individual de sus actividades y tiempos estimados. La actualización anterior se publicó en `fefae1c`; los nuevos registros están incorporados localmente y pendientes de publicación.

## 5. ¿Qué aprendimos?

### Ingeniería de Datos

Durante E2 reforzamos la importancia de conservar las fuentes originales, documentar su procedencia y construir transformaciones reproducibles.

El procesamiento geoespacial permitió trabajar con información territorial oficial y generar productos que pueden utilizarse posteriormente en análisis municipales.

También fortalecimos la integración de datos y la trazabilidad entre las capas Bronce, Plata y Oro.

Aprendimos que la integración de fuentes con diferentes escalas territoriales requiere documentar cuidadosamente sus limitaciones para evitar interpretaciones incorrectas.

### Análisis Estadístico

Aprendimos a diseñar experimentos factoriales para estudiar el efecto de diferentes factores sobre una variable de respuesta.

El experimento 2³ permitió evaluar el comportamiento del tiempo de integración bajo distintas configuraciones.

El análisis ANOVA permitió identificar la significancia estadística de los factores de trazabilidad y validación Pandera.

También aprendimos a utilizar indicadores como R², R² ajustado y Shapiro-Wilk para complementar la interpretación de los modelos.

La comparación entre los diseños 2⁴ y 2⁴⁻¹ permitió comprender la relación entre el número de corridas, el esfuerzo experimental y la confusión de efectos.

Identificamos que los diseños fraccionados pueden reducir considerablemente el número de ejecuciones, pero requieren interpretar sus resultados considerando la estructura de alias.

También comprendimos que la generación de resultados experimentales debe realizarse bajo condiciones controladas, incluyendo calentamiento, aleatorización y réplicas.

Reconocimos que los resultados estadísticos deben interpretarse considerando el número de réplicas, las condiciones de ejecución y los supuestos del modelo.

El ANOVA 3×2 permitió distinguir los efectos del número de procesos y del formato. Aprendimos que una prueba de homogeneidad puede ser poco informativa con dos réplicas por celda. El bloqueo permitió estudiar variaciones entre ejecuciones, y X05 mostró la necesidad de confirmar una configuración candidata con mediciones nuevas antes de adoptarla. Un resultado negativo también aporta evidencia útil.

### Calidad en los Sistemas de Información

Reforzamos la importancia de utilizar pruebas automatizadas, mantener un historial de cambios y registrar evidencias verificables.

Durante la validación técnica del proyecto se obtuvo un resultado de 145 pruebas aprobadas.

También identificamos que los registros PSP deben mantenerse actualizados y reflejar las actividades y tiempos reales de cada integrante.

La revisión de calidad es una actividad complementaria al desarrollo técnico y permite detectar inconsistencias antes de presentar los entregables finales.

La evaluación ISO permitió distinguir calidad del producto, calidad de los datos y gestión de procesos. Aprendimos que aprobar pruebas no implica cobertura completa y que una auditoría de dependencias no sustituye una revisión integral de seguridad. También identificamos la importancia de definir denominadores, metas y limitaciones antes de interpretar porcentajes de calidad.

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

### 6.2 Análisis Estadístico

| Evidencia | Ubicación |
|---|---|
| Experimento factorial 2³ | `src/experimento_factorial_e2.py` |
| ANOVA factorial 2³ | `src/analisis_factorial_2_3_e2.py` |
| Resultados ANOVA 2³ | `data/reportes/anova_factorial_2_3.csv` |
| Gráficas factorial 2³ | `data/reportes/graficas_e2_monico/` |
| Informe factorial 2³ | `docs/E2/analisis_estadistico/experimento_factorial_2_3.md` |
| Experimento completo 2⁴ | `src/experimento_factorial_2_4_e2.py` |
| ANOVA completo 2⁴ | `src/analisis_factorial_2_4_e2.py` |
| ANOVA fraccionado 2⁴⁻¹ | `src/analisis_fraccionado_2_4_e2.py` |
| Comparación de diseños | `src/comparacion_factorial_2_4_e2.py` |
| Gráficas comparativas | `src/graficas_comparacion_2_4_e2.py` |
| Informe de comparación | `docs/E2/analisis_estadistico/comparacion_factorial_2_4.md` |
| Resultados factorial completo | `data/reportes/experimento_factorial_2_4_completo.csv` |
| Resultados factorial fraccionado | `data/reportes/experimento_factorial_2_4_fraccionado.csv` |
| Comparación estadística | `data/reportes/comparacion_factorial_2_4.csv` |
| X03 — Informe | [ANOVA 3×2](E2/analisis_estadistico/anova_3_2.md) |
| X03 — Código | `src/experimento_anova_3_2_e2.py`, `src/analisis_anova_3_2_e2.py` |
| X03 — Corridas y análisis | `data/reportes/experimento_anova_3_2.csv`, `data/reportes/anova_3_2.csv`, `data/reportes/resumen_anova_3_2.csv`, `data/reportes/diagnostico_anova_3_2.csv` |
| X03 — Gráficas | `reportes/figuras/anova_3_2/` |
| Bloques — Informe | [Factorial con bloques](E2/analisis_estadistico/experimento_factorial_bloques.md) |
| Bloques — Código | `src/experimento_factorial_bloques_e2.py`, `src/analisis_factorial_bloques_e2.py` |
| Bloques — Corridas | `data/reportes/factorial_2_3_bloque_1.csv`, `data/reportes/factorial_2_3_bloque_2.csv` |
| Bloques — Análisis | `data/reportes/anova_factorial_bloques_e2.csv`, `data/reportes/efectos_factorial_bloques_e2.csv`, `data/reportes/resumen_factorial_bloques_e2.csv`, `data/reportes/diagnostico_factorial_bloques_e2.csv` |
| Bloques — Gráficas | `reportes/figuras/factorial_bloques/` |
| X05 — Informe | [Confirmación experimental](E2/analisis_estadistico/confirmacion_experimental_x05.md) |
| X05 — Código | `src/experimento_confirmacion_x05_e2.py` |
| X05 — Resultados | `data/reportes/experimento_confirmacion_x05.csv`, `data/reportes/resumen_confirmacion_x05.csv`, `data/reportes/comparacion_confirmacion_x05.csv` |
| X05 — Gráficas | `reportes/figuras/confirmacion_x05/` |

### 6.3 Calidad de Software

| Evidencia | Ubicación |
|---|---|
| Pruebas geoespaciales | `tests/test_geoespacial.py` |
| Pruebas de trazabilidad | `tests/test_trazabilidad_e2.py` |
| Registro de tiempo de David | `calidad/tiempo-david.csv` |
| Registro de tiempo de Nancy | `calidad/tiempo-nancy.csv` |
| Registro de defectos de David | `calidad/defectos-david.csv` |
| Registro de defectos de Nancy | `calidad/defectos-nancy.csv` |

### 6.4 Documentación

| Documento | Ubicación |
|---|---|
| Entrega E2 | `docs/E2/ENTREGA.md` |
| Ética de datos | `docs/etica-datos.md` |
| Relatoría E2 | `docs/relatoria-E2.md` |
| Trazabilidad | `docs/E2/trazabilidad.md` |
| Validación de calidad | `docs/E2/validacion-calidad.md` |
| Análisis factorial 2³ | `docs/E2/analisis_estadistico/experimento_factorial_2_3.md` |
| Comparación factorial 2⁴ | `docs/E2/analisis_estadistico/comparacion_factorial_2_4.md` |

### 6.5 Control de versiones

Los commits G01–G11 documentan la incorporación de información geográfica, el desarrollo de scripts, la generación del mapa, la trazabilidad, los experimentos estadísticos y la elaboración de documentos.

Los cambios estadísticos fueron integrados a la rama principal mediante los siguientes commits:

| Commit | Actividad |
|---|---|
| `892c21f` | Experimento factorial 2³ |
| `01f2421` | Comparación de diseños factoriales 2⁴ |
| `2622d2e` | Corrección de importaciones para Ruff |
| `3e359ef` | Documentación del ANOVA factorial 2³ |

El commit `3e359ef` incorporó los siguientes archivos:

- `src/analisis_factorial_2_3_e2.py`
- `data/reportes/anova_factorial_2_3.csv`
- `docs/E2/analisis_estadistico/experimento_factorial_2_3.md`

El cierre estadístico se integró en `main` mediante un avance directo y se realizó el envío al repositorio remoto.

La verificación del cierre estadístico correspondió al commit `3e359ef`. Posteriormente se publicaron las evaluaciones de calidad y el PSP actualizado hasta `fefae1c`.

El repositorio se encuentra disponible en:

https://github.com/NancyHaideVazquez/trusted-data-lab

### 6.6 Evidencias de validación

Durante las verificaciones técnicas se obtuvieron los siguientes resultados:

| Verificación | Resultado |
|---|---|
| Pruebas automatizadas | 145 aprobadas |
| Ruff | Sin errores |
| Compilación del script ANOVA 2³ | Correcta |
| Revisión de diferencias con Git | Sin errores en la última comprobación |
| Geometrías municipales | 10 válidas |
| Geometrías vacías | 0 |
| Registros en Plata | 564 |
| Registros en Oro | 564 |
| Registros sin origen | 0 |

Las evidencias de validación y los resultados correspondientes se encuentran documentados en el repositorio.

### 6.7 Evidencias complementarias de calidad

| Evidencia | Enlace |
|---|---|
| Q01 | [ISO 25010](E2/calidad/iso25010.md) |
| Q02 | [ISO 25012](E2/calidad/iso25012.md) |
| Q03 | [Antecedentes normativos](E2/calidad/antecedentes_normativos.md) |
| Cobertura | [JSON](../data/reportes/cobertura_iso25010_e2.json) |
| Auditoría global | [JSON](../data/reportes/auditoria_dependencias_e2.json) |
| Auditoría de requisitos | [JSON](../data/reportes/auditoria_proyecto_e2.json) |
| Compatibilidad | [CSV](../data/reportes/compatibilidad_iso25010_e2.csv) |
| Eficiencia | [CSV](../data/reportes/eficiencia_iso25010_e2.csv) |
| Métricas ISO 25012 | [CSV](../data/reportes/metricas_iso25012_e2.csv) |
| Hashes Bronce | [CSV](../data/reportes/hashes_bronce_e2.csv) |
| Exactitud | [CSV](../data/reportes/exactitud_bronce_oro_e2.csv) |
| Script de métricas | [Python](../src/metricas_iso25012.py) |
| PSP David | [Tiempos](../calidad/tiempo-david.csv) y [defectos](../calidad/defectos-david.csv) |
| PSP Nancy | [Tiempos](../calidad/tiempo-nancy.csv) y [defectos](../calidad/defectos-nancy.csv) |

### 6.8 Commits complementarios

| Commit | Actividad |
|---|---|
| `5bc1963` | Actualización de entrega, relatoría y comparación factorial |
| `d6fc572` | Ética y legalidad; versión etiquetada e2 |
| `8f42839` | Q02 — Evaluación ISO 25012 |
| `e2c8cb0` | Corrección de formato Q02 |
| `5299de2` | Q01 — Evaluación ISO 25010 |
| `ce79abf` | Q03 — Antecedentes normativos |
| `fefae1c` | Actualización PSP de David |

La etiqueta `e2` se actualizó previamente de `d6fc572` a `052fbba` con autorización. Ese commit contiene las evaluaciones ISO, PSP y documentación de la entrega anterior. Las nuevas evidencias de X03, bloques, X05 y Q03 se encuentran localmente y aún no forman parte de la etiqueta. Su publicación y eventual actualización de etiqueta requieren el cierre de las verificaciones.

## 7. Uso de IA generativa

Durante el desarrollo de E2 se utilizó ChatGPT como herramienta de apoyo para explicar procedimientos técnicos, revisar comandos de PowerShell y Git, orientar el desarrollo de scripts y pruebas, y estructurar documentación.

La herramienta también apoyó en la interpretación de resultados estadísticos, la identificación de limitaciones y la redacción de documentos técnicos.

Las respuestas generadas por IA se contrastaron con los archivos, las ejecuciones y las evidencias disponibles en el repositorio.

La responsabilidad de verificar los resultados y entregar el proyecto corresponde a sus integrantes.

## 8. Pendientes de validación antes del cierre definitivo

1. Los registros PSP de Nancy y David fueron actualizados y confirmados.
2. Realizar las revisiones internas de calidad recomendadas por el plan de trabajo, sin considerarlas un entregable independiente salvo indicacion expresa de los docentes.
3. Confirmar que todos los requisitos oficiales de la etapa E2 estén cubiertos.
4. Revisar la correspondencia entre las evidencias y los documentos finales.
5. Confirmar la revisión definitiva de la entrega por parte del equipo.
6. Realizar Q04 cuando Isis indique el procedimiento y equipo asignado.
7. Revisar las referencias bibliográficas incorporadas en Q03 y contrastar las evidencias de X03, bloqueo y X05 con la rúbrica completa; los experimentos ya se ejecutaron y documentaron.
8. Verificar las condiciones especificas de redistribucion de Banxico. La URL geografica fue recuperada y la fecha estimada de descarga fue documentada; el instante exacto de ingesta no fue registrado originalmente.

---

**Estado de la etapa E2:**

La relatoría E2 documenta las actividades geoespaciales, de trazabilidad, integración y análisis estadístico desarrolladas durante la etapa.

Los experimentos factoriales 2³, 2⁴ y 2⁴⁻¹ cuentan con resultados y documentación técnica. Se realizaron comparaciones estadísticas entre los diseños completos y fraccionados, identificando sus ventajas y limitaciones.

Las pruebas automatizadas registraron 145 resultados aprobados y la revisión de Ruff no presentó errores.

Los cambios correspondientes al cierre estadístico fueron integrados en la rama principal del repositorio.

Q01-Q03, las 48 nuevas corridas experimentales, la ampliacion bibliografica, el PSP actualizado de David y los documentos de cierre fueron publicados en el commit `dbf974c`.

La validacion local registro 145 pruebas aprobadas en 12.40 segundos. Ruff y git diff --check finalizaron sin errores. GitHub Actions #39 aprobo el commit publicado.

La etiqueta `e2` fue actualizada y verificada tanto localmente como en el repositorio remoto, apuntando al commit `dbf974c5fd14ef5af2b0ecf5650bee27556836f3`.

Posteriormente se recupero la URL original del Marco Geoestadistico municipal 2026 mediante Zone.Identifier. La fecha estimada de descarga fue 2026-11-22T18:08:54Z y el primer commit de incorporacion a Bronce fue `b4fe64f`, registrado a las 18:15:18 UTC del mismo dia.

Se verifico que el SHA-256 del archivo original coincide exactamente con el archivo conservado en Bronce. Los metadatos fueron actualizados y validados localmente, conservando como desconocido el instante exacto de ingesta.

Permanecen pendientes Q04, las condiciones especificas de redistribucion de Banxico y la comprobacion final de los requisitos oficiales.

Las revisiones internas del equipo son recomendables conforme al plan de trabajo, sin afirmar que constituyan un entregable independiente obligatorio.

La relatoria ampliada conserva el detalle tecnico original; si se exige un maximo de dos paginas, debera presentarse una version breve adicional.

---

## Confirmacion de contribuciones personales de Nancy

El 24 de noviembre de 2026 Nancy confirmo su participacion en las siguientes actividades de E2:

- Planeacion y organizacion del proyecto.
- Revision de etica y legalidad.
- Participacion en analisis estadistico y experimentos.
- Q01: Evaluacion ISO 25010.
- Q03: Antecedentes normativos.
- Revision de la relatoria E2.
- Validacion tecnica final del repositorio.

La validacion personal obtuvo 145 pruebas aprobadas en 8.73 segundos y Ruff sin errores.

Las siete actividades fueron incorporadas al archivo calidad/tiempo-nancy.csv.

Nancy confirmo posteriormente las fechas y duraciones estimadas de sus siete actividades personales de E2. Los horarios exactos de inicio y fin no fueron recuperados.

Los 75 minutos de apoyo correspondientes a G05, G06 y G07 fueron ejecutados por David y no se contabilizan como tiempo personal de Nancy.

Se conservaron los 21 defectos previamente documentados. No se incorporaron defectos nuevos sin evidencia.

La auditoria cruzada Q04 permanece pendiente de cierre.

## Cierre del PSP personal de Nancy - E2

Nancy confirmo los siguientes tiempos personales estimados correspondientes a E2.

| Actividad | Fecha reportada | Minutos efectivos |
|---|---|---:|
| Planeacion y organizacion | 2026-11-23 | 25 |
| Revision de etica y legalidad | 2026-11-23 | 20 |
| Analisis estadistico y experimentos | 2026-11-23 | 25 |
| Q01 - Evaluacion ISO 25010 | 2026-11-23 | 30 |
| Q03 - Antecedentes normativos | 2026-11-23 | 35 |
| Revision de la relatoria E2 | 2026-11-23 | 45 |
| Validacion y actualizacion del PSP | 2026-11-23 | 20 |
| Total efectivo | | 200 |
| Descansos | | 40 |
| Total general | | 240 |

El tiempo efectivo personal de Nancy en E2 fue estimado en 3 horas y 20 minutos, con 40 minutos de descanso, para un total de 4 horas.

El archivo de tiempos contiene 38 registros acumulados, incluyendo siete actividades personales de E2 y un registro de descanso.

Los 75 minutos de apoyo ejecutados por David no forman parte de las horas personales de Nancy.

Se conservaron los 21 defectos acumulados. Nancy confirmo que no encontro defectos nuevos durante E2.

La comprobacion tecnica del 24 de noviembre obtuvo 145 pruebas aprobadas en 8.73 segundos y Ruff sin errores.

GitHub Actions #43 aprobo el commit f194db0 en 52 segundos.

Los tiempos son estimaciones retrospectivas. No se inventaron horarios exactos de inicio o fin.

El registro PSP personal de Nancy queda actualizado. La auditoria cruzada Q04 permanece pendiente.
