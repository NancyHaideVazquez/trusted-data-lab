# T12 — Cuarentena de registros inválidos

## 1. Objetivo

Implementar un mecanismo de Cuarentena para identificar y separar registros que incumplan las reglas de la Puerta de Calidad desarrollada en T11.

El propósito es conservar los registros rechazados junto con sus motivos, sin modificar los datos originales ni permitir que errores no identificables pasen inadvertidos.

## 2. Herramientas utilizadas

- Python 3.14.3.
- pandas.
- Pandera 0.35.0.
- pytest.

## 3. Datos utilizados

Archivo de entrada:

`data/plata/integracion_mensual.csv`

El conjunto contiene 564 registros de las series integradas de INEGI y Banxico.

## 4. Implementación

Se desarrollaron los siguientes archivos:

- `src/cuarentena.py`: separación de registros válidos e inválidos.
- `src/ejecutar_cuarentena.py`: ejecución del proceso y generación de archivos.
- `tests/test_cuarentena.py`: pruebas automatizadas.

La función principal, `separar_cuarentena()`, utiliza las reglas de validación de Pandera definidas en T11.

Cuando se detectan incumplimientos asociados a registros específicos, se separan las filas correspondientes y se añade la columna `motivo_rechazo`.

Cuando se encuentran errores estructurales o globales que no pueden atribuirse con seguridad a filas específicas, el proceso se detiene en lugar de aprobar los datos automáticamente.

Los datos originales no se modifican.

## 5. Archivos de salida

El ejecutor genera:

**Registros rechazados:**

`data/cuarentena/registros/integracion_mensual_rechazados.csv`

**Reporte de Cuarentena:**

`data/cuarentena/reportes/reporte_cuarentena.csv`

El archivo de rechazos conserva las columnas originales y añade `motivo_rechazo`.

El reporte contiene los conteos de registros originales, válidos y rechazados, además del estado general de la ejecución.

## 6. Resultados con datos reales

Se ejecutó el proceso sobre los 564 registros del archivo integrado.

| Métrica | Resultado |
|---|---:|
| Registros originales | 564 |
| Registros válidos | 564 |
| Registros rechazados | 0 |
| Estado | SIN_RECHAZOS |

El archivo de rechazados contiene únicamente los encabezados, porque ningún registro del conjunto actual incumplió las reglas configuradas.

## 7. Prueba controlada de rechazo

Para comprobar el funcionamiento de la Cuarentena, se modificó únicamente en memoria el periodo de un registro de Banxico, asignándole el valor inválido `2026-13`.

Resultados:

| Métrica | Resultado |
|---|---:|
| Registros originales | 564 |
| Registros válidos | 563 |
| Registros rechazados | 1 |

Motivo registrado:

`Periodo invalido: se esperaba AAAA-MM con un mes entre 01 y 12.`

El rechazo fue guardado en:

`data/cuarentena/registros/prueba_rechazo_t12.csv`

Posteriormente se volvió a leer el archivo y se verificó que conservaba el registro rechazado y su motivo.

**Este archivo corresponde a una prueba simulada, no a un rechazo real de Banxico.**

## 8. Pruebas automatizadas

Se ejecutaron ocho pruebas específicas de T12 que verifican:

1. Aceptación de registros válidos.
2. Separación de periodos inválidos.
3. Conservación del motivo de rechazo.
4. Separación de valores faltantes.
5. Separación de varios registros con errores.
6. Conservación del número total de registros.
7. No modificación de los datos originales.
8. Detención ante errores estructurales.

**Resultado de T12: 8 pruebas aprobadas.**

También se ejecutó la suite completa del proyecto:

**Resultado general: 71 pruebas aprobadas, sin fallos.**

## 9. Limitaciones y siguientes pasos

La implementación actual permite separar errores asociados a filas, pero detiene el proceso ante errores estructurales o globales sin una ubicación identificable.

El reporte de ejecución usa nombres de archivo fijos; una nueva ejecución puede reemplazar los resultados anteriores. Todavía no se implementa un historial de rechazos por ejecución.

El ejecutor de T12 genera evidencia de Cuarentena, pero no publica automáticamente los registros válidos.

En T13 se integrarán las etapas de procesamiento, validación y Cuarentena en un pipeline que controle la publicación de datos.

## 10. Conclusión

Se implementó un mecanismo funcional para separar registros inválidos y conservar sus motivos de rechazo.

La ejecución sobre el conjunto actual no identificó registros inválidos. Una prueba controlada confirmó que un registro con un periodo incorrecto puede separarse, persistirse en CSV y recuperarse sin alterar los datos originales.

Las ocho pruebas de T12 y las 71 pruebas del proyecto se completaron satisfactoriamente.