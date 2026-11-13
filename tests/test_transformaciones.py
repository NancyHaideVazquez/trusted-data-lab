import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.transformaciones import escalar_datos


def test_reutilizar_parametros_sin_fuga():
    entrenamiento = pd.DataFrame({"valor": [10, 20, 30]})
    prueba = pd.DataFrame({"valor": [40, 50]})

    _, parametros = escalar_datos(entrenamiento)

    resultado, parametros_usados = escalar_datos(
        prueba, parametros=parametros
    )

    assert resultado["valor_minmax"].tolist() == pytest.approx(
        [1.5, 2.0]
    )

    assert resultado["valor_zscore"].tolist() == pytest.approx(
        [2.449489743, 3.674234614]
    )

    assert parametros_usados == parametros
    assert parametros["minmax"]["maximo"] == 30


def test_reutilizar_parametros_con_faltantes():
    entrenamiento = pd.DataFrame({"valor": [10, 20, 30]})
    prueba = pd.DataFrame({"valor": [40.0, None, 50.0]})

    _, parametros = escalar_datos(entrenamiento)

    resultado, _ = escalar_datos(
        prueba, parametros=parametros
    )

    assert len(resultado) == 3
    assert pd.isna(resultado.loc[1, "valor_minmax"])
    assert pd.isna(resultado.loc[1, "valor_zscore"])
    assert resultado.loc[0, "valor_minmax"] == pytest.approx(1.5)


def test_rechaza_parametros_de_otra_columna():
    entrenamiento = pd.DataFrame({"valor": [10, 20, 30]})

    _, parametros = escalar_datos(entrenamiento)

    prueba = pd.DataFrame({"precio": [40, 50]})

    with pytest.raises(ValueError, match="otra columna"):
        escalar_datos(
            prueba,
            columna="precio",
            parametros=parametros
        )



def test_minmax():
    df = pd.DataFrame({"valor": [10, 20, 30]})

    resultado, _ = escalar_datos(df)

    assert resultado["valor_minmax"].tolist() == pytest.approx(
        [0.0, 0.5, 1.0]
    )


def test_zscore():
    df = pd.DataFrame({"valor": [10, 20, 30]})

    resultado, _ = escalar_datos(df)

    assert resultado["valor_zscore"].tolist() == pytest.approx(
        [-1.224744871, 0.0, 1.224744871]
    )


def test_conserva_original():
    df = pd.DataFrame({"valor": [10, 20, 30]})
    copia = df.copy(deep=True)

    resultado, _ = escalar_datos(df)

    assert_frame_equal(df, copia)
    assert resultado["valor"].tolist() == [10, 20, 30]


def test_valores_faltantes():
    df = pd.DataFrame({"valor": [10.0, None, 30.0]})

    resultado, _ = escalar_datos(df)

    assert pd.isna(resultado.loc[1, "valor_minmax"])
    assert pd.isna(resultado.loc[1, "valor_zscore"])
    assert resultado.loc[0, "valor_minmax"] == pytest.approx(0.0)
    assert resultado.loc[2, "valor_minmax"] == pytest.approx(1.0)


def test_parametros():
    df = pd.DataFrame({"valor": [10, 20, 30]})

    _, parametros = escalar_datos(df)

    assert parametros["minmax"]["minimo"] == 10
    assert parametros["minmax"]["maximo"] == 30
    assert parametros["zscore"]["media"] == 20


def test_columna_inexistente():
    df = pd.DataFrame({"valor": [10, 20, 30]})

    with pytest.raises(ValueError):
        escalar_datos(df, "precio")


def test_sin_valores_validos():
    df = pd.DataFrame({"valor": [None, None]})

    with pytest.raises(ValueError):
        escalar_datos(df)
