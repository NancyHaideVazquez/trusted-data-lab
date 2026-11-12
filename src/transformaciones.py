
"""T07 - Normalizacion y estandarizacion de datos."""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def escalar_datos(df, columna="valor", parametros=None):
    """
    Aplica Min-Max y Z-score sin modificar los datos originales.

    Si parametros es None, calcula los parametros con los datos
    recibidos (ajuste descriptivo o entrenamiento).

    Si recibe parametros, reutiliza esos valores sin recalcularlos.
    """

    if columna not in df.columns:
        raise ValueError(f"No existe la columna: {columna}")

    resultado = df.copy(deep=True)

    if not pd.api.types.is_numeric_dtype(resultado[columna]):
        raise ValueError("La columna debe ser numerica")

    validos = resultado[columna].notna()

    if validos.sum() == 0 and parametros is None:
        raise ValueError("No existen valores numericos validos")

    resultado[columna + "_minmax"] = float("nan")
    resultado[columna + "_zscore"] = float("nan")

    if parametros is None:
        minmax = MinMaxScaler()
        zscore = StandardScaler()

        valores = resultado.loc[validos, [columna]]

        minmax.fit(valores)
        zscore.fit(valores)

        parametros = {
            "columna": columna,
            "minmax": {
                "minimo": float(minmax.data_min_[0]),
                "maximo": float(minmax.data_max_[0])
            },
            "zscore": {
                "media": float(zscore.mean_[0]),
                "desviacion_estandar": float(zscore.scale_[0])
            }
        }

    else:
        if parametros["columna"] != columna:
            raise ValueError("Los parametros pertenecen a otra columna")

    minimo = parametros["minmax"]["minimo"]
    maximo = parametros["minmax"]["maximo"]
    media = parametros["zscore"]["media"]
    desviacion = parametros["zscore"]["desviacion_estandar"]

    rango = maximo - minimo

    if validos.any():
        if rango == 0:
            resultado.loc[validos, columna + "_minmax"] = 0.0
        else:
            resultado.loc[validos, columna + "_minmax"] = (
                (resultado.loc[validos, columna] - minimo) / rango
            )

        if desviacion == 0:
            resultado.loc[validos, columna + "_zscore"] = 0.0
        else:
            resultado.loc[validos, columna + "_zscore"] = (
                (resultado.loc[validos, columna] - media) / desviacion
            )

    return resultado, parametros
