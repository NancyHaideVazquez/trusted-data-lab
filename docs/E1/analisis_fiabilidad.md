# Análisis de fiabilidad de las capturas

## 1. Objetivo

Evaluar la fiabilidad observada de los procesos de captura de datos de INEGI y Banco de México utilizando los registros reales de ejecución.

El análisis busca identificar ejecuciones exitosas, fallos, cobertura temporal y disponibilidad de evidencia para calcular MTBF, MTTR y disponibilidad del sistema.

## 2. Fuente de información

Se utilizó la bitácora `logs/capturas.csv`, que contiene la fecha UTC, fuente, identificador de serie, estado de ejecución, duración y detalle.

El análisis se realizó sin modificar el archivo original.

## 3. Resultados observados

| Métrica | Resultado |
|---|---:|
| Capturas registradas | 24 |
| Capturas exitosas | 24 |
| Capturas fallidas | 0 |
| Capturas INEGI | 12 |
| Capturas Banxico | 12 |
| Días distintos con registros | 5 |
| Tasa de éxito observada | 100% |

**Primera captura:** 7 de noviembre de 2026, 19:29:54 UTC.

**Última captura:** 12 de noviembre de 2026, 07:43:58 UTC.

### Distribución diaria

| Fecha UTC | Capturas |
|---|---:|
| 2026-11-07 | 4 |
| 2026-11-08 | 2 |
| 2026-11-10 | 8 |
| 2026-11-11 | 6 |
| 2026-11-12 | 4 |
| **Total** | **24** |

No se encontraron registros correspondientes al 9 de noviembre dentro del periodo observado.

La ausencia de capturas en una fecha no demuestra por sí misma que el servicio haya estado fuera de operación.

## 4. Indicadores de fiabilidad

### Tasa de éxito de capturas

La tasa de éxito se calculó mediante:

Tasa de éxito = (capturas exitosas / capturas totales) × 100.

Resultado:

(24 / 24) × 100 = **100%**.

Este indicador representa exclusivamente el éxito de las ejecuciones registradas.

### MTBF: tiempo medio entre fallos

El MTBF requiere observar fallos y medir el tiempo de operación entre ellos.

No se registraron fallos durante el periodo analizado.

Por tanto, **el MTBF no puede estimarse de manera válida con la evidencia disponible**.

### MTTR: tiempo medio de recuperación

El MTTR requiere medir cuánto tarda el sistema en recuperarse después de un fallo.

Como no se registraron fallos ni procesos de recuperación, **el MTTR no puede calcularse**.

La columna `segundos` representa la duración de cada captura y no debe utilizarse directamente como tiempo de reparación.

### Disponibilidad

La disponibilidad operacional requiere conocer los periodos en los que el sistema estuvo disponible y los periodos en los que estuvo fuera de servicio.

La bitácora registra intentos de captura, pero no constituye un monitoreo continuo de disponibilidad.

Por tanto, no es posible demostrar la disponibilidad del sistema a partir de estos datos.

## 5. Limitaciones

El documento original del proyecto solicita métricas de MTBF, MTTR y disponibilidad basadas en siete días de bitácoras.

La evidencia actual contiene capturas en cinco días distintos, sin fallos registrados.

Esto permite demostrar una tasa de éxito del 100% en las capturas observadas, pero no cumple todavía el periodo completo de monitoreo solicitado para la evaluación de fiabilidad.

Para obtener indicadores adicionales será necesario mantener la bitácora durante el periodo requerido y registrar explícitamente los eventos de fallo, inicio de recuperación y restauración del servicio.

## 6. Conclusión

Durante el periodo analizado se registraron 24 capturas exitosas y ningún fallo, distribuidas entre las fuentes INEGI y Banxico.

La tasa de éxito observada fue del 100%.

No existe evidencia suficiente para calcular MTBF, MTTR o disponibilidad continua, y la cobertura temporal todavía no alcanza los siete días de registros solicitados.

Los resultados se presentan como una línea base de fiabilidad sustentada en datos reales, sin suponer tiempos de reparación ni periodos de disponibilidad no observados.