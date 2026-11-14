
import numpy as np
import pandas as pd
import pytest

from src.modelos_pronostico import (
    calcular_metricas,
    preparar_serie,
)
from src.pronostico_final import (
    cargar_serie,
    diagnostico_residuos,
)


def crear_datos_mensuales(n=60, fuente="inegi"):
    """Genera datos simulados sin modificar Bronce."""
    fechas = pd.date_range(
        start="2020-01-01",
        periods=n,
        freq="MS",
    )

    return pd.DataFrame({
        "fuente": [fuente] * n,
        "periodo": fechas.strftime("%Y-%m"),
        "valor": np.linspace(1.0, 5.0, n),
    })


def test_preparar_serie_correcta():
    datos = crear_datos_mensuales(n=60)

    serie = preparar_serie(datos, "inegi", "Inflacion")

    assert len(serie) == 60
    assert serie.index.freqstr == "MS"
    assert serie.name == "Inflacion"


def test_preparar_serie_duplicados():
    datos = crear_datos_mensuales()
    datos = pd.concat([datos, datos.iloc[[0]]])

    with pytest.raises(ValueError, match="duplicados"):
        preparar_serie(datos, "inegi", "Inflacion")


def test_preparar_serie_meses_faltantes():
    datos = crear_datos_mensuales()
    datos = datos.drop(index=10)

    with pytest.raises(ValueError, match="meses faltantes"):
        preparar_serie(datos, "inegi", "Inflacion")


def test_preparar_serie_valor_infinito():
    datos = crear_datos_mensuales()
    datos.loc[0, "valor"] = np.inf

    with pytest.raises(ValueError, match="no finitos"):
        preparar_serie(datos, "inegi", "Inflacion")


def test_preparar_serie_insuficiente():
    datos = crear_datos_mensuales(n=24)

    with pytest.raises(ValueError, match="insuficientes"):
        preparar_serie(datos, "inegi", "Inflacion")


def test_preparar_serie_no_modifica_original():
    datos = crear_datos_mensuales(n=60)
    original = datos.copy(deep=True)

    preparar_serie(datos, "inegi", "Inflacion")

    pd.testing.assert_frame_equal(datos, original)


def test_calcular_metricas_perfectas():
    resultado = calcular_metricas(
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
    )

    assert resultado["MAE"] == pytest.approx(0)
    assert resultado["RMSE"] == pytest.approx(0)
    assert resultado["MAPE_pct"] == pytest.approx(0)


def test_calcular_metricas_con_errores():
    resultado = calcular_metricas(
        [10.0, 20.0],
        [8.0, 18.0],
    )

    assert resultado["MAE"] == pytest.approx(2.0)
    assert resultado["RMSE"] == pytest.approx(2.0)
    assert resultado["MAPE_pct"] == pytest.approx(15.0)


def test_calcular_metricas_longitudes_distintas():
    with pytest.raises(ValueError, match="invalidas"):
        calcular_metricas([1, 2, 3], [1, 2])


def test_calcular_metricas_prediccion_infinita():
    with pytest.raises(ValueError, match="invalidas"):
        calcular_metricas([1, 2], [1, np.inf])


def test_calcular_metricas_valores_cero():
    resultado = calcular_metricas([0, 0], [1, 1])

    assert np.isnan(resultado["MAPE_pct"])
    assert resultado["MAPE_excluidos"] == 2
    assert resultado["MAPE_advertencia"] != ""


def test_calcular_metricas_negativos():
    resultado = calcular_metricas([-2, 2], [-1, 1])

    assert resultado["MAE"] == pytest.approx(1.0)
    assert resultado["MAPE_advertencia"] != ""


def test_cargar_serie_correcta():
    datos = crear_datos_mensuales()

    serie = cargar_serie(datos, "inegi", "Inflacion")

    assert len(serie) == 60
    assert serie.index.freqstr == "MS"


def test_cargar_serie_duplicados():
    datos = crear_datos_mensuales()
    datos = pd.concat([datos, datos.iloc[[0]]])

    with pytest.raises(ValueError, match="duplicadas"):
        cargar_serie(datos, "inegi", "Inflacion")


def test_cargar_serie_meses_faltantes():
    datos = crear_datos_mensuales()
    datos = datos.drop(index=5)

    with pytest.raises(ValueError, match="meses faltantes"):
        cargar_serie(datos, "inegi", "Inflacion")


def test_cargar_serie_valor_infinito():
    datos = crear_datos_mensuales()
    datos.loc[0, "valor"] = np.inf

    with pytest.raises(ValueError, match="no finitos"):
        cargar_serie(datos, "inegi", "Inflacion")


def test_cargar_serie_no_modifica_original():
    datos = crear_datos_mensuales()
    original = datos.copy(deep=True)

    cargar_serie(datos, "inegi", "Inflacion")

    pd.testing.assert_frame_equal(datos, original)


def test_diagnostico_residuos():
    rng = np.random.default_rng(2026)
    residuos = rng.normal(size=100)

    resultado = diagnostico_residuos(residuos)

    assert "lb_p12" in resultado
    assert "lb_p24" in resultado
    assert 0 <= resultado["lb_p12"] <= 1
    assert 0 <= resultado["lb_p24"] <= 1
