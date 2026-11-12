
"""T08 - Discretizacion de variables numericas."""

import pandas as pd


def discretizar_datos(df, columna="valor", metodo="cut"):
    """
    Divide una columna numerica en tres categorias.

    cut: intervalos de igual amplitud.
    qcut: intervalos por cuantiles.

    Conserva la columna original y los valores faltantes.
    """

    if columna not in df.columns:
        raise ValueError("La columna no existe")

    # Primero verificamos si todos los valores son faltantes.
    if df[columna].isna().all():
        raise ValueError("No existen valores validos")

    # Verificamos que la columna sea numerica.
    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise ValueError("La columna debe ser numerica")

    # Verificamos que el metodo sea valido.
    if metodo not in ["cut", "qcut"]:
        raise ValueError("Metodo no valido")

    # Copiamos los datos para no modificar el original.
    resultado = df.copy(deep=True)

    # Ignoramos los faltantes para calcular los intervalos.
    valores = resultado[columna].dropna()

    # Se necesitan al menos tres valores distintos.
    if valores.nunique() < 3:
        raise ValueError(
            "Se necesitan al menos tres valores distintos"
        )

    etiquetas = ["Bajo", "Medio", "Alto"]

    if metodo == "cut":

        categorias, limites = pd.cut(
            resultado[columna],
            bins=3,
            labels=etiquetas,
            retbins=True,
            include_lowest=True
        )

    else:

        categorias, limites = pd.qcut(
            resultado[columna],
            q=3,
            labels=etiquetas,
            retbins=True,
            duplicates="raise"
        )

    # Agregamos la nueva columna sin eliminar la original.
    resultado[columna + "_" + metodo] = categorias

    # Guardamos los parametros utilizados.
    parametros = {
        "columna": columna,
        "metodo": metodo,
        "etiquetas": etiquetas,
        "limites": [float(x) for x in limites]
    }

    return resultado, parametros
