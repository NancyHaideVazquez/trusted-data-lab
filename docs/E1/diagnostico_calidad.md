# Diagnóstico de calidad de datos — T03

**Proyecto:** Trusted Data Lab  
**Etapa:** E1 — Diagnóstico y preparación de datos  
**Fecha de actualización:** 12 de noviembre de 2026

## 1. Objetivo

Evaluar la calidad de los datos históricos de INEGI y Banco de México, identificando valores faltantes, fechas duplicadas, fechas inválidas y valores numéricos inválidos, sin modificar los archivos originales de la capa Bronce.

## 2. Archivos analizados

### INEGI

- **Indicador:** 910402
- **Registros:** 183
- **Periodo:** agosto de 2011 a octubre de 2026
- **Última observación:** 2026-10-01
- **Archivo:** `data/bronce/inegi/2026-11-12/910402_historico_130114_649094_60dc15f7.json`

### Banco de México

- **Serie:** SF43783
- **Indicador:** TIIE a 28 días
- **Registros:** 7,958
- **Periodo:** marzo de 1995 a noviembre de 2026
- **Última observación:** 2026-11-12
- **Archivo:** `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`

## 3. Resultados del diagnóstico

| Métrica | INEGI | Banxico |
|---|---:|---:|
| Registros analizados | 183 | 7,958 |
| Valores faltantes | 0 | 200 |
| Porcentaje de faltantes | 0% | 2.51% |
| Fechas duplicadas | 0 | 0 |
| Fechas inválidas | 0 | 0 |
| Valores numéricos inválidos adicionales | 0 | 0 |
| Valor mínimo | -0.24 | 3.2741 |
| Valor máximo | 0.82 | 90.50 |
| Promedio | 0.291475 | 9.938054 |

## 4. Análisis de valores faltantes

### INEGI

No se identificaron valores faltantes en las 183 observaciones históricas analizadas.

Tampoco se detectaron fechas duplicadas, fechas inválidas ni valores numéricos inválidos.

### Banco de México

Se identificaron 200 valores faltantes en un total de 7,958 observaciones, equivalentes aproximadamente al 2.51%.

Estos valores corresponden al marcador `N/E`, identificado en el campo `dato`.

Durante la revisión de la captura histórica anterior se observó la siguiente distribución:

| Año | Registros con N/E |
|---|---:|
| 1995 | 152 |
| 1996 | 48 |
| **Total** | **200** |

La nueva captura conserva la misma cantidad total de faltantes. Sin embargo, la distribución anual deberá verificarse nuevamente para confirmar que no haya cambiado.

La concentración temporal de los faltantes requiere investigación adicional y no permite clasificarlos definitivamente como MCAR, MAR o MNAR.

## 5. Validaciones realizadas

El programa `src/diagnostico.py` realiza las siguientes comprobaciones:

1. Localiza automáticamente la captura histórica más reciente de cada fuente.
2. Lee los archivos JSON mediante las funciones de `src/lectura.py`.
3. Identifica valores faltantes, incluidos los marcadores `N/E` y `N/D`.
4. Convierte los valores numéricos para identificar formatos inválidos.
5. Convierte las fechas y detecta fechas inválidas.
6. Identifica fechas duplicadas.
7. Calcula valores mínimos, máximos y promedios.
8. Genera el reporte `data/reportes/diagnostico_calidad.csv`.

## 6. Conclusiones

- Ambas capturas históricas pudieron analizarse correctamente.
- INEGI contiene 183 observaciones y no presentó valores faltantes.
- Banxico contiene 7,958 observaciones, de las cuales 200 no tienen un valor numérico disponible.
- No se detectaron fechas duplicadas, fechas inválidas ni valores numéricos inválidos adicionales.
- Los archivos originales de la capa Bronce permanecieron sin modificaciones.
- El análisis de los mecanismos de ausencia se continuará durante T04.

## 7. Evidencias

- `src/diagnostico.py`
- `data/reportes/diagnostico_calidad.csv`
- `docs/E1/diccionario_datos.md`
- `data/bronce/inegi/2026-11-12/910402_historico_130114_649094_60dc15f7.json`
- `data/bronce/banxico/2026-11-12/SF43783_historico_130116_421967_754519eb.json`

## 8. Ejecución

Desde la raíz del proyecto, ejecutar:

```powershell
python -m src.diagnostico
```

El programa selecciona las capturas históricas más recientes disponibles y genera el archivo CSV con los resultados del diagnóstico.