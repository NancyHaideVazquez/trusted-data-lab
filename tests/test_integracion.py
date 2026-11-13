
import pandas as pd

from src.integracion import integrar_datos


def crear_datos():
    # Datos de prueba de INEGI
    inegi = pd.DataFrame({
        "fuente": ["inegi", "inegi"],
        "serie_id": ["910402", "910402"],
        "fecha": ["2026-01-01", "2026-02-01"],
        "valor": [0.5, 0.8]
    })

    # Datos de prueba de Banxico
    banxico = pd.DataFrame({
        "fuente": ["banxico", "banxico"],
        "serie_id": ["SF43783", "SF43783"],
        "periodo": ["2026-01", "2026-02"],
        "valor": [7.5, 7.2]
    })

    return inegi, banxico


def test_cantidad_registros():
    inegi, banxico = crear_datos()
    resultado = integrar_datos(inegi, banxico)

    assert len(resultado) == 4


def test_conserva_fuentes():
    inegi, banxico = crear_datos()
    resultado = integrar_datos(inegi, banxico)

    assert set(resultado["fuente"]) == {"inegi", "banxico"}


def test_conserva_series():
    inegi, banxico = crear_datos()
    resultado = integrar_datos(inegi, banxico)

    assert set(resultado["serie_id"]) == {"910402", "SF43783"}


def test_periodos_mensuales():
    inegi, banxico = crear_datos()
    resultado = integrar_datos(inegi, banxico)

    assert set(resultado["periodo"]) == {"2026-01", "2026-02"}


def test_no_modifica_originales():
    inegi, banxico = crear_datos()

    copia_inegi = inegi.copy()
    copia_banxico = banxico.copy()

    integrar_datos(inegi, banxico)

    pd.testing.assert_frame_equal(inegi, copia_inegi)
    pd.testing.assert_frame_equal(banxico, copia_banxico)


def test_conserva_valores():
    inegi, banxico = crear_datos()
    resultado = integrar_datos(inegi, banxico)

    valores_inegi = resultado[
        resultado["fuente"] == "inegi"
    ]["valor"].tolist()

    valores_banxico = resultado[
        resultado["fuente"] == "banxico"
    ]["valor"].tolist()

    assert valores_inegi == [0.5, 0.8]
    assert valores_banxico == [7.5, 7.2]


def test_conserva_metadatos():
    inegi, banxico = crear_datos()
    resultado = integrar_datos(inegi, banxico)

    columnas = [
        "indicador",
        "unidad",
        "frecuencia",
        "metodo",
        "cobertura"
    ]

    for columna in columnas:
        assert columna in resultado.columns


def test_metadatos_por_fuente():
    inegi, banxico = crear_datos()
    resultado = integrar_datos(inegi, banxico)

    fila_inegi = resultado[
        resultado["fuente"] == "inegi"
    ].iloc[0]

    fila_banxico = resultado[
        resultado["fuente"] == "banxico"
    ].iloc[0]

    assert fila_inegi["indicador"] == "Inflacion mensual"
    assert fila_inegi["unidad"] == "porcentaje"
    assert fila_inegi["frecuencia"] == "mensual"

    assert fila_banxico["indicador"] == "TIIE a 28 dias"
    assert fila_banxico["unidad"] == "porcentaje anual"
    assert fila_banxico["metodo"] == "promedio mensual"
