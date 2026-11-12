"""E1 / T05: imputación controlada de valores faltantes.

Este módulo NO lee ni modifica archivos de la capa Bronce. Trabaja únicamente
con copias de DataFrames y aplica reglas que se le proporcionen explícitamente.

Ejemplo de configuración::

    config = {
        "fecha_col": "fecha",
        "grupo_col": "serie_id",  # opcional
        "metodos": {
            "valor": "interpolacion_temporal",
            "otro_valor": {"metodo": "mediana_por_grupo", "grupo_col": "serie_id"},
        },
    }

No se infiere el mecanismo MCAR/MAR/MNAR ni se sustituyen códigos como 'N/E'
por NaN de forma automática: esa decisión requiere el diagnóstico estadístico.
"""

from __future__ import annotations

import re
from typing import Any

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

METODOS_VALIDOS = {
    "interpolacion_temporal",
    "ffill",
    "mediana_por_grupo",
    "ninguno",
}

# La detección por nombre es una protección adicional, no sustituye la
# configuración explícita de 'columnas_protegidas'.
_IDENTIFICADORES = re.compile(
    r"(^id$|^id_|_id$|^fecha$|^fecha_|_fecha$|^date$|^date_|_date$|"
    r"^clave$|^clave_|_clave$|^codigo$|^codigo_|_codigo$|"
    r"^key$|^key_|_key$|^periodo$|^periodo_|_periodo$)",
    flags=re.IGNORECASE,
)


def _protegida(df: pd.DataFrame, columna: str, extras: set[str]) -> bool:
    """Detecta fechas, IDs y claves que no se deben imputar."""
    return (
        columna in extras
        or bool(_IDENTIFICADORES.search(columna))
        or is_datetime64_any_dtype(df[columna])
    )


def _regla(valor: Any) -> dict[str, Any]:
    """Acepta 'ffill' o {'metodo': 'ffill', ...}."""
    if isinstance(valor, str):
        return {"metodo": valor}
    if isinstance(valor, dict):
        return dict(valor)
    raise ValueError("Cada regla debe ser un método o un diccionario de opciones")


def _orden_temporal(
    df: pd.DataFrame, fecha_col: str, grupo_col: str | None
) -> pd.DataFrame:
    """Devuelve copia ordenada cronológicamente con índice temporal seguro."""
    if fecha_col not in df.columns:
        raise ValueError(f"No existe la columna de fechas: {fecha_col}")
    fechas = pd.to_datetime(df[fecha_col], errors="coerce")
    if fechas.isna().any():
        raise ValueError(
            f"La columna {fecha_col} contiene fechas nulas o inválidas; "
            "revísalas antes de imputar"
        )
    # Índice auxiliar exclusivo de esta copia; no altera los datos originales.
    tabla = df.copy()
    tabla["__orden_fecha__"] = fechas.to_numpy()
    orden = ([grupo_col] if grupo_col else []) + ["__orden_fecha__"]
    return tabla.sort_values(orden, kind="stable")


def imputar(df: pd.DataFrame, config: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Imputa datos bajo reglas explícitas, sin modificar ``df``.

    Parámetros
    ----------
    df : pandas.DataFrame
        Observaciones originales o de trabajo.
    config : dict
        ``metodos``: mapa de columna a método o a un diccionario de regla.
        Opcionales: ``fecha_col`` (predeterminado ``fecha``), ``grupo_col``,
        ``columnas_protegidas`` (lista de identificadores/fechas adicionales).

    Métodos
    -------
    interpolacion_temporal : interpola *solo huecos interiores* usando la
        distancia real entre fechas. No extrapola antes ni después.
    ffill : usa el valor anterior en orden cronológico, sin cruzar grupos.
    mediana_por_grupo : mediana dentro de un grupo, sin usar mediana global.
    ninguno : conserva los nulos; crea bandera en falso.

    Devuelve
    --------
    (DataFrame, DataFrame): datos copiados con banderas ``<col>_imputado``
        y reporte con ``columna``, ``metodo``, ``nulos_antes``,
        ``cantidad_imputada`` y ``nulos_despues``.

    Notas
    -----
    No convierte texto como 'N/E' en NaN. Nunca imputa IDs, claves o fechas.
    Rechaza nombres de columnas de salida que ya existan para no sobreescribir.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un pandas.DataFrame")
    if not isinstance(config, dict) or not isinstance(config.get("metodos"), dict):
        raise ValueError("config debe incluir un diccionario 'metodos'")
    if not df.columns.is_unique:
        raise ValueError("El DataFrame tiene nombres de columnas duplicados")
    if not df.index.is_unique:
        raise ValueError("El índice debe ser único para conservar el orden original")

    salida = df.copy(deep=True)
    fecha_col = config.get("fecha_col", "fecha")
    grupo_defecto = config.get("grupo_col")
    protegidas = set(config.get("columnas_protegidas", []))
    reporte: list[dict[str, Any]] = []

    # Validar TODO antes de transformar para evitar resultados parciales.
    reglas = {}
    for columna, especificacion in config["metodos"].items():
        if columna not in df.columns:
            raise ValueError(f"No existe la columna a imputar: {columna}")
        regla = _regla(especificacion)
        metodo = regla.get("metodo")
        if metodo not in METODOS_VALIDOS:
            raise ValueError(f"Método no reconocido para {columna}: {metodo}")
        if _protegida(df, columna, protegidas):
            raise ValueError(f"Prohibido imputar un ID, clave o fecha: {columna}")
        if f"{columna}_imputado" in df.columns:
            raise ValueError(f"Ya existe la bandera {columna}_imputado")
        grupo = regla.get("grupo_col", grupo_defecto)
        if grupo is not None and grupo not in df.columns:
            raise ValueError(f"No existe la columna de agrupación: {grupo}")
        # No propagar códigos de faltante como si fueran observaciones válidas.
        # El diagnóstico debe convertirlos explícitamente cuando proceda.
        if metodo != "ninguno" and df[columna].astype("string").str.strip().str.upper().isin(
            {"N/E", "N/D", "NULL", "N/A"}
        ).any():
            raise ValueError(
                f"La columna {columna} contiene marcadores de faltantes (p. ej. N/E); "
                "normaliza los marcadores antes de imputar"
            )
        if metodo in {"interpolacion_temporal", "mediana_por_grupo"} and not is_numeric_dtype(df[columna]):
            raise ValueError(f"{metodo} requiere columna numérica: {columna}")
        if metodo == "mediana_por_grupo" and not grupo:
            raise ValueError(f"mediana_por_grupo requiere grupo_col para {columna}")
        reglas[columna] = (metodo, grupo)

    for columna, (metodo, grupo) in reglas.items():
        antes = salida[columna].isna()
        original = salida[columna].copy()
        nueva = original.copy()

        if metodo == "interpolacion_temporal":
            tabla = _orden_temporal(salida, fecha_col, grupo)
            if grupo:
                grupos = tabla.groupby(grupo, dropna=False, sort=False)
                for _, parte in grupos:
                    serie = parte.set_index("__orden_fecha__")[columna]
                    if not serie.index.is_unique:
                        raise ValueError(
                            f"Fechas duplicadas en {fecha_col} dentro de un grupo: "
                            "no se puede interpolar temporalmente sin resolverlas"
                        )
                    calculada = serie.interpolate(method="time", limit_area="inside")
                    nueva.loc[parte.index] = calculada.to_numpy()
            else:
                serie = tabla.set_index("__orden_fecha__")[columna]
                if not serie.index.is_unique:
                    raise ValueError("Fechas duplicadas: resuélvelas antes de interpolar")
                calculada = serie.interpolate(method="time", limit_area="inside")
                nueva.loc[tabla.index] = calculada.to_numpy()

        elif metodo == "ffill":
            tabla = _orden_temporal(salida, fecha_col, grupo)
            if grupo:
                calculada = tabla.groupby(grupo, dropna=False, sort=False)[columna].ffill()
            else:
                calculada = tabla[columna].ffill()
            nueva.loc[tabla.index] = calculada.to_numpy()

        elif metodo == "mediana_por_grupo":
            medianas = salida.groupby(grupo, dropna=False)[columna].transform("median")
            nueva = original.fillna(medianas)

        # 'ninguno' conserva exactamente la columna.
        salida[columna] = nueva
        bandera = antes & nueva.notna()
        salida[f"{columna}_imputado"] = bandera.astype(bool)
        reporte.append(
            {
                "columna": columna,
                "metodo": metodo,
                "nulos_antes": int(antes.sum()),
                "cantidad_imputada": int(bandera.sum()),
                "nulos_despues": int(nueva.isna().sum()),
            }
        )

    return salida, pd.DataFrame(
        reporte,
        columns=["columna", "metodo", "nulos_antes", "cantidad_imputada", "nulos_despues"],
    )


def detectar_atipicos_iqr(
    df: pd.DataFrame,
    columna: str,
    grupo_col: str | None = None,
    factor: float = 1.5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Marca extremos según los límites de Tukey, sin borrar ni alterar valores.

    Calcula Q1, Q3 e IQR por grupo si se especifica grupo_col.
    Los atípicos quedan 'por_revisar': detectarlos NO demuestra un error.
    Los grupos sin valores o con menos de cuatro observaciones numéricas
    quedan sin evaluación para evitar límites poco informativos.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un DataFrame")
    if not df.columns.is_unique or not df.index.is_unique:
        raise ValueError("Columnas e índice deben ser únicos")
    if columna not in df.columns:
        raise ValueError(f"No existe la columna: {columna}")
    if grupo_col is not None and grupo_col not in df.columns:
        raise ValueError(f"No existe el grupo: {grupo_col}")
    if columna == grupo_col:
        raise ValueError("La columna de valores no puede ser el grupo")
    if _protegida(df, columna, set()):
        raise ValueError("No se calculan atípicos sobre identificadores ni fechas")
    if not is_numeric_dtype(df[columna]):
        raise ValueError("La columna evaluada debe ser numérica")
    if not isinstance(factor, (int, float)) or not 0 < factor < float('inf'):
        raise ValueError("factor debe ser un número finito mayor que cero")

    nombres = ["es_atipico", "clasificacion_atipico", "iqr_limite_inferior", "iqr_limite_superior"]
    if any(nombre in df.columns for nombre in nombres):
        raise ValueError("Ya existen columnas de salida de detección de atípicos")

    salida = df.copy(deep=True)
    salida["es_atipico"] = False
    salida["clasificacion_atipico"] = "no_evaluado"
    salida["iqr_limite_inferior"] = float('nan')
    salida["iqr_limite_superior"] = float('nan')
    resumen = []
    agrupados = (salida.groupby(grupo_col, dropna=False, sort=False)
                 if grupo_col else [("serie_completa", salida)])

    for grupo, parte in agrupados:
        numeros = parte[columna].dropna()
        n = len(numeros)
        if n < 4:
            resumen.append({"grupo": str(grupo), "columna": columna, "n_validos": n,
                            "q1": float('nan'), "q3": float('nan'), "iqr": float('nan'),
                            "limite_inferior": float('nan'), "limite_superior": float('nan'),
                            "cantidad_atipicos": 0, "estado": "insuficientes_datos"})
            continue
        q1 = float(numeros.quantile(.25))
        q3 = float(numeros.quantile(.75))
        iqr = q3 - q1
        inferior, superior = q1 - factor * iqr, q3 + factor * iqr
        posiciones = parte.index
        mascara = ((parte[columna] < inferior) | (parte[columna] > superior)).fillna(False)
        salida.loc[posiciones, "es_atipico"] = mascara.to_numpy(dtype=bool)
        salida.loc[posiciones, "clasificacion_atipico"] = "no_atipico"
        salida.loc[posiciones[mascara], "clasificacion_atipico"] = "por_revisar"
        salida.loc[posiciones, "iqr_limite_inferior"] = inferior
        salida.loc[posiciones, "iqr_limite_superior"] = superior
        resumen.append({"grupo": str(grupo), "columna": columna, "n_validos": n,
                        "q1": q1, "q3": q3, "iqr": iqr, "limite_inferior": inferior,
                        "limite_superior": superior, "cantidad_atipicos": int(mascara.sum()),
                        "estado": "evaluado"})

    return salida, pd.DataFrame(resumen)

# ---------------------------------------------------------------------------
# Preparación conservadora de las dos series reales de E1.
# Los diagnósticos indican: INEGI 910402 (183 filas, 0 faltantes),
# Banxico SF43783 (7958 filas, 200 "N/E", concentrados en 1995-1996).
# Estos conteos NO se fuerzan: se recalculan al leer los datos reales.
# ---------------------------------------------------------------------------


def preparar_serie(df: pd.DataFrame, fuente: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Normaliza fechas y valores, conservando el valor crudo y todos los registros.

    No imputa, no elimina, no altera Bronce. 'N/E' queda como NaN con
    motivo 'no_publicado': **no significa cero ni dato imputable**.

    Retorna (datos, reporte) con columnas canónicas: fuente, serie_id,
    fecha, valor_original, valor, estado_valor, motivo_revision.
    """
    campos = {
        'inegi': ('TIME_PERIOD', 'OBS_VALUE', '910402'),
        'banxico': ('fecha', 'dato', 'SF43783'),
    }
    if fuente not in campos:
        raise ValueError('fuente debe ser inegi o banxico')
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df debe ser un DataFrame')
    fecha_col, valor_col, serie = campos[fuente]
    if fecha_col not in df or valor_col not in df:
        raise ValueError(f'{fuente}: faltan columnas {fecha_col} y/o {valor_col}')

    salida = df.copy(deep=True)
    # La fecha original y el valor original se conservan para trazabilidad.
    salida['fuente'] = fuente
    salida['serie_id'] = serie
    salida['fecha_original'] = df[fecha_col]
    salida['valor_original'] = df[valor_col]
    # Reutiliza el conversor de T01: Banxico publica fechas DD/MM/AAAA.
    from src.lectura import convertir_fecha
    salida['fecha'] = convertir_fecha(df[fecha_col])
    texto = df[valor_col].astype('string').str.strip()
    marcadores = {'', '-', 'N/E', 'N/D', 'N/A', 'NULL'}
    es_marcador = texto.str.upper().isin(marcadores).fillna(False)
    salida['valor'] = pd.to_numeric(texto.mask(es_marcador), errors='coerce')
    fecha_invalida = salida['fecha'].isna()
    sin_publicacion = es_marcador | texto.isna()
    no_numerico = (~sin_publicacion) & salida['valor'].isna()
    salida['estado_valor'] = 'valido'
    salida.loc[sin_publicacion, 'estado_valor'] = 'faltante'
    salida.loc[no_numerico, 'estado_valor'] = 'no_numerico'
    salida.loc[fecha_invalida, 'estado_valor'] = 'fecha_invalida'
    salida['motivo_revision'] = ''
    salida.loc[sin_publicacion, 'motivo_revision'] = 'no_publicado'
    salida.loc[no_numerico, 'motivo_revision'] = 'valor_no_numerico'
    salida.loc[fecha_invalida, 'motivo_revision'] = 'fecha_invalida'
    salida['valor_imputado'] = False

    reporte = pd.DataFrame([{
        'fuente': fuente, 'serie_id': serie, 'registros': len(salida),
        'numericos_validos': int((salida['estado_valor'] == 'valido').sum()),
        'faltantes_no_publicados': int(sin_publicacion.sum()),
        'valores_no_numericos': int(no_numerico.sum()),
        'fechas_invalidas': int(fecha_invalida.sum()),
        'registros_eliminados': 0, 'registros_imputados': 0,
        'criterio': 'Sin imputacion automatica; revisar faltantes y extremos',
    }])
    return salida, reporte


def limpieza_conservadora(
    df: pd.DataFrame, fuente: str, factor_iqr: float = 1.5
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Prepara datos y marca extremos IQR; nunca borra, imputa ni cuarentena.

    Las observaciones sin publicar siguen presentes, con motivo de revisión.
    Pandera y el paso a Plata se gestionan en ``src/calidad.py``.
    """
    preparados, reporte = preparar_serie(df, fuente)
    marcados, reporte_iqr = detectar_atipicos_iqr(
        preparados, columna='valor', grupo_col='serie_id', factor=factor_iqr
    )
    reporte['atipicos_por_revisar'] = int(marcados['es_atipico'].sum())
    reporte['criterio'] = 'IQR 1.5 como alerta, no como exclusion; sin imputacion'
    return marcados, reporte, reporte_iqr


def ejecutar_diagnostico_limpieza(fuente: str = 'ambas') -> None:
    """Lee históricos existentes y genera CSV derivados en data/reportes/.

    Ejecutar desde la raíz: ``python -m src.limpieza --fuente ambas``.
    Nunca escribe en data/bronce, plata, oro ni cuarentena.
    """
    from pathlib import Path
    from src.lectura import cargar_dataframe
    from src.diagnostico import buscar_historico

    raiz = Path(__file__).resolve().parents[1]
    reportes = raiz / 'data' / 'reportes'
    reportes.mkdir(parents=True, exist_ok=True)
    fuentes = ('inegi', 'banxico') if fuente == 'ambas' else (fuente,)
    for origen in fuentes:
        serie = '910402' if origen == 'inegi' else 'SF43783'
        ruta = buscar_historico(origen, serie)
        crudo = cargar_dataframe(ruta)
        procesado, resumen, extremos = limpieza_conservadora(crudo, origen)
        procesado.to_csv(reportes / f'limpieza_preliminar_{origen}.csv', index=False, encoding='utf-8-sig')
        resumen['archivo_origen'] = ruta.relative_to(raiz).as_posix()
        resumen.to_csv(reportes / f'resumen_limpieza_{origen}.csv', index=False, encoding='utf-8-sig')
        extremos.to_csv(reportes / f'atipicos_iqr_{origen}.csv', index=False, encoding='utf-8-sig')
        print(f'\n{origen.upper()} - {ruta.name}')
        print(resumen.to_string(index=False))
    print(f'\nReportes generados en {reportes}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Preparación conservadora T05/T06 - E1')
    parser.add_argument('--fuente', choices=('inegi', 'banxico', 'ambas'), default='ambas')
    args = parser.parse_args()
    ejecutar_diagnostico_limpieza(args.fuente)
