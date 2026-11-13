
import pandas as pd
import pytest
import pandera.pandas as pa

from src.calidad import validar_calidad


def crear_datos_validos():
    return pd.DataFrame({
        "fuente": ["inegi", "banxico"],
        "serie_id": ["910402", "SF43783"],
        "indicador": ["Inflacion mensual", "TIIE a 28 dias"],
        "periodo": ["2026-01", "2026-01"],
        "valor": [0.5, 7.5],
        "unidad": ["porcentaje", "porcentaje anual"],
        "frecuencia": ["mensual", "mensual"],
        "metodo": ["valor mensual original", "promedio mensual"],
        "cobertura": ["nacional", "nacional"]
    })


def test_datos_validos():
    datos = crear_datos_validos()
    resultado = validar_calidad(datos)

    assert len(resultado) == 2


def test_rechaza_fuente_desconocida():
    datos = crear_datos_validos()
    datos.loc[0, "fuente"] = "otra_fuente"

    with pytest.raises(pa.errors.SchemaErrors):
        validar_calidad(datos)


def test_rechaza_periodo_invalido():
    datos = crear_datos_validos()
    datos.loc[0, "periodo"] = "2026-13"

    with pytest.raises(pa.errors.SchemaErrors):
        validar_calidad(datos)


def test_rechaza_valor_faltante():
    datos = crear_datos_validos()
    datos.loc[0, "valor"] = None

    with pytest.raises(pa.errors.SchemaErrors):
        validar_calidad(datos)


def test_rechaza_metadato_vacio():
    datos = crear_datos_validos()
    datos.loc[0, "unidad"] = ""

    with pytest.raises(pa.errors.SchemaErrors):
        validar_calidad(datos)


def test_rechaza_frecuencia_incorrecta():
    datos = crear_datos_validos()
    datos.loc[0, "frecuencia"] = "diaria"

    with pytest.raises(pa.errors.SchemaErrors):
        validar_calidad(datos)


def test_rechaza_duplicados():
    datos = crear_datos_validos()

    datos = pd.concat(
        [datos, datos.iloc[[0]]],
        ignore_index=True
    )

    with pytest.raises(pa.errors.SchemaErrors):
        validar_calidad(datos)


def test_no_modifica_originales():
    datos = crear_datos_validos()
    copia = datos.copy(deep=True)

    validar_calidad(datos)

    pd.testing.assert_frame_equal(datos, copia)


def test_rechaza_columnas_faltantes():
    datos = crear_datos_validos()
    datos = datos.drop(columns=["cobertura"])

    with pytest.raises(pa.errors.SchemaErrors):
        validar_calidad(datos)
