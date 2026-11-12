
"""Pruebas de T08 - Discretizacion."""

import pandas as pd
import pytest

from src.discretizacion import discretizar_datos


def test_cut():
    df = pd.DataFrame({"valor": [10, 20, 30, 40, 50, 60]})

    resultado, parametros = discretizar_datos(df, metodo="cut")

    assert resultado["valor_cut"].tolist() == [
        "Bajo", "Bajo", "Medio", "Medio", "Alto", "Alto"
    ]

    assert parametros["metodo"] == "cut"


def test_qcut():
    df = pd.DataFrame({"valor": [10, 20, 30, 40, 50, 60]})

    resultado, parametros = discretizar_datos(df, metodo="qcut")

    assert resultado["valor_qcut"].tolist() == [
        "Bajo", "Bajo", "Medio", "Medio", "Alto", "Alto"
    ]

    assert parametros["metodo"] == "qcut"


def test_conserva_valores_originales():
    df = pd.DataFrame({"valor": [10, 20, 30]})

    copia = df.copy(deep=True)

    discretizar_datos(df)

    pd.testing.assert_frame_equal(df, copia)


def test_conserva_faltantes():
    df = pd.DataFrame({
        "valor": [10.0, None, 30.0, 50.0]
    })

    resultado, _ = discretizar_datos(df)

    assert pd.isna(resultado.loc[1, "valor_cut"])

    assert resultado["valor_cut"].notna().sum() == 3


def test_todos_los_validos_clasificados():
    df = pd.DataFrame({
        "valor": [10, 20, 30, 40, 50, 60]
    })

    for metodo in ["cut", "qcut"]:

        resultado, _ = discretizar_datos(
            df,
            metodo=metodo
        )

        assert resultado[
            "valor_" + metodo
        ].notna().sum() == 6


def test_limites_ordenados():
    df = pd.DataFrame({
        "valor": [10, 20, 30, 40, 50, 60]
    })

    for metodo in ["cut", "qcut"]:

        _, parametros = discretizar_datos(
            df,
            metodo=metodo
        )

        limites = parametros["limites"]

        assert len(limites) == 4

        assert all(
            limites[i] < limites[i + 1]
            for i in range(3)
        )


def test_columna_inexistente():
    df = pd.DataFrame({"valor": [10, 20, 30]})

    with pytest.raises(
        ValueError,
        match="no existe"
    ):
        discretizar_datos(
            df,
            columna="precio"
        )


def test_columna_no_numerica():
    df = pd.DataFrame({
        "valor": ["uno", "dos", "tres"]
    })

    with pytest.raises(
        ValueError,
        match="numerica"
    ):
        discretizar_datos(df)


def test_metodo_invalido():
    df = pd.DataFrame({"valor": [10, 20, 30]})

    with pytest.raises(
        ValueError,
        match="Metodo no valido"
    ):
        discretizar_datos(
            df,
            metodo="otro"
        )


def test_sin_valores_validos():
    df = pd.DataFrame({
        "valor": [None, None, None]
    })

    with pytest.raises(
        ValueError,
        match="No existen valores validos"
    ):
        discretizar_datos(df)


def test_valores_distintos_insuficientes():
    df = pd.DataFrame({
        "valor": [10, 10, 20, 20]
    })

    with pytest.raises(
        ValueError,
        match="tres valores distintos"
    ):
        discretizar_datos(df)
