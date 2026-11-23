# Relatoría E2 · Trusted Data Lab

**Proyecto:** Observatorio de Vivienda y Costos de Colima

**Equipo:** David Cuevas Farías y Nancy Haide Vázquez Ávalos

**Etapa:** E2 — Procesamiento geoespacial, trazabilidad, análisis estadístico y ética de datos

**Fecha de elaboración:** 22 de noviembre de 2026

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

El tiempo efectivo aproximado fue de 270 minutos, con 45 minutos adicionales de interrupciones, para un tiempo transcurrido estimado de 315 minutos.

Los horarios individuales se reconstruyeron a partir de estimaciones y no corresponden a una medición minuto a minuto.

Los registros PSP deben mantenerse actualizados conforme se realicen nuevas actividades.

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

### Calidad en los Sistemas de Información

Reforzamos la importancia de utilizar pruebas automatizadas, mantener un historial de cambios y registrar evidencias verificables.

Durante la validación técnica del proyecto se obtuvo un resultado de 145 pruebas aprobadas.

También identificamos que los registros PSP deben mantenerse actualizados y reflejar las actividades y tiempos reales de cada integrante.

La revisión de calidad es una actividad complementaria al desarrollo técnico y permite detectar inconsistencias antes de presentar los entregables finales.

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

La verificación posterior confirmó que la rama local y `origin/main` se encontraban sincronizadas en el commit `3e359ef`.

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

## 7. Uso de IA generativa

Durante el desarrollo de E2 se utilizó ChatGPT como herramienta de apoyo para explicar procedimientos técnicos, revisar comandos de PowerShell y Git, orientar el desarrollo de scripts y pruebas, y estructurar documentación.

La herramienta también apoyó en la interpretación de resultados estadísticos, la identificación de limitaciones y la redacción de documentos técnicos.

Las respuestas generadas por IA se contrastaron con los archivos, las ejecuciones y las evidencias disponibles en el repositorio.

La responsabilidad de verificar los resultados y entregar el proyecto corresponde a sus integrantes.

## 8. Pendientes de validación antes del cierre definitivo

1. Completar y verificar los registros PSP de E2 correspondientes a ambos integrantes.
2. Documentar las revisiones individuales de calidad realizadas por Nancy.
3. Confirmar que todos los requisitos oficiales de la etapa E2 estén cubiertos.
4. Revisar la correspondencia entre las evidencias y los documentos finales.
5. Confirmar la revisión definitiva de la entrega por parte del equipo.

---

**Estado de la etapa E2:**

La relatoría E2 documenta las actividades geoespaciales, de trazabilidad, integración y análisis estadístico desarrolladas durante la etapa.

Los experimentos factoriales 2³, 2⁴ y 2⁴⁻¹ cuentan con resultados y documentación técnica. Se realizaron comparaciones estadísticas entre los diseños completos y fraccionados, identificando sus ventajas y limitaciones.

Las pruebas automatizadas registraron 145 resultados aprobados y la revisión de Ruff no presentó errores.

Los cambios correspondientes al cierre estadístico fueron integrados en la rama principal del repositorio.

Permanecen pendientes las evidencias individuales de validación, los registros PSP que deban completarse y la revisión definitiva de los entregables por parte del equipo.
