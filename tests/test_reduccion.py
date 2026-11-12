
import pandas as pd
from src.reduccion import reducir_datos


def test_reduccion_mensual():
    datos = pd.DataFrame({
        "fecha": [
            "2026-01-01",
            "2026-01-02",
            "2026-02-01"
        ],
        "valor": [4.0, 6.0, 8.0],
        "fuente": ["banxico"] * 3,
        "serie_id": ["SF43783"] * 3
    })

    resultado = reducir_datos(datos)

    assert len(resultado) == 2
    assert resultado.iloc[0]["valor"] == 5.0
    assert resultado.iloc[1]["valor"] == 8.0


def test_conserva_identificadores():
    datos = pd.DataFrame({
        "fecha": ["2026-01-01"],
        "valor": [4.5],
        "fuente": ["banxico"],
        "serie_id": ["SF43783"]
    })

    resultado = reducir_datos(datos)

    assert resultado.iloc[0]["fuente"] == "banxico"
    assert resultado.iloc[0]["serie_id"] == "SF43783"
    assert resultado.iloc[0]["periodo"] == "2026-01"


def test_no_modifica_datos_originales():
    datos = pd.DataFrame({
        "fecha": ["2026-01-01"],
        "valor": [4.5],
        "fuente": ["banxico"],
        "serie_id": ["SF43783"]
    })

    original = datos.copy()

    reducir_datos(datos)

    pd.testing.assert_frame_equal(datos, original)


def test_ignora_faltantes_en_promedio():
    datos = pd.DataFrame({
        "fecha": [
            "2026-01-01",
            "2026-01-02",
            "2026-01-03"
        ],
        "valor": [4.0, None, 6.0],
        "fuente": ["banxico"] * 3,
        "serie_id": ["SF43783"] * 3
    })

    resultado = reducir_datos(datos)

    assert resultado.iloc[0]["valor"] == 5.0
    assert resultado.iloc[0]["registros_originales"] == 3
    assert resultado.iloc[0]["registros_validos"] == 2
