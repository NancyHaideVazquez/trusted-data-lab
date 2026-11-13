
import json

import pandas as pd
import pytest

from src.lectura import (
    buscar_observaciones,
    calcular_sha256,
    cargar_dataframe,
    convertir_fecha,
    resumen_periodo,
    inventariar,
)


def test_buscar_observaciones_inegi():
    datos = {
        "Series": [
            {
                "OBSERVATIONS": [
                    {"TIME_PERIOD": "2026/01", "OBS_VALUE": "0.5"}
                ]
            }
        ]
    }

    resultado = buscar_observaciones(datos)

    assert len(resultado) == 1
    assert resultado[0]["OBS_VALUE"] == "0.5"


def test_buscar_observaciones_banxico():
    datos = {
        "data": {
            "bmx": {
                "series": [
                    {
                        "datos": [
                            {"fecha": "01/01/2026", "dato": "7.5"}
                        ]
                    }
                ]
            }
        }
    }

    resultado = buscar_observaciones(datos)

    assert len(resultado) == 1
    assert resultado[0]["dato"] == "7.5"


def test_buscar_observaciones_sin_datos():
    assert buscar_observaciones({"metadata": "ejemplo"}) is None


def test_cargar_dataframe_json(tmp_path):
    archivo = tmp_path / "datos.json"
    archivo.write_text(
        json.dumps({
            "OBSERVATIONS": [
                {"TIME_PERIOD": "2026/01", "OBS_VALUE": "1.2"}
            ]
        }),
        encoding="utf-8",
    )

    resultado = cargar_dataframe(archivo)

    assert len(resultado) == 1
    assert resultado.iloc[0]["OBS_VALUE"] == "1.2"


def test_cargar_dataframe_csv(tmp_path):
    archivo = tmp_path / "datos.csv"
    archivo.write_text(
        "fecha,valor\n2026-01-01,5.5\n",
        encoding="utf-8",
    )

    resultado = cargar_dataframe(archivo)

    assert len(resultado) == 1
    assert resultado.iloc[0]["valor"] == "5.5"


def test_cargar_dataframe_extension_invalida(tmp_path):
    archivo = tmp_path / "datos.txt"
    archivo.write_text("ejemplo", encoding="utf-8")

    with pytest.raises(ValueError):
        cargar_dataframe(archivo)


def test_convertir_fecha_mensual():
    fechas = convertir_fecha(pd.Series(["2026/01", "2026-02"]))

    assert fechas.iloc[0] == pd.Timestamp("2026-01-01")
    assert fechas.iloc[1] == pd.Timestamp("2026-02-01")


def test_convertir_fecha_banxico():
    fechas = convertir_fecha(pd.Series(["13/11/2026"]))

    assert fechas.iloc[0] == pd.Timestamp("2026-11-13")


def test_convertir_fecha_invalida():
    fechas = convertir_fecha(pd.Series(["fecha_invalida"]))

    assert pd.isna(fechas.iloc[0])


def test_resumen_periodo():
    datos = pd.DataFrame({
        "TIME_PERIOD": ["2026/01", "2026/03", "2026/02"]
    })

    columna, inicio, fin = resumen_periodo(datos)

    assert columna == "TIME_PERIOD"
    assert inicio == "2026-01-01"
    assert fin == "2026-03-01"


def test_resumen_periodo_sin_fecha():
    datos = pd.DataFrame({"valor": [1, 2, 3]})

    assert resumen_periodo(datos) == ("", "", "")


def test_calcular_sha256(tmp_path):
    archivo = tmp_path / "ejemplo.txt"
    archivo.write_text("contenido de prueba", encoding="utf-8")

    huella1 = calcular_sha256(archivo)
    huella2 = calcular_sha256(archivo)

    assert huella1 == huella2
    assert len(huella1) == 64


def test_inventariar_archivos(tmp_path):
    bronce = tmp_path / "bronce"
    bronce.mkdir()

    archivo = bronce / "datos.json"
    archivo.write_text(
        json.dumps({
            "OBSERVATIONS": [
                {"TIME_PERIOD": "2026/01", "OBS_VALUE": "0.5"}
            ]
        }),
        encoding="utf-8",
    )

    reporte = tmp_path / "reportes" / "inventario.csv"

    resultado = inventariar(bronce=bronce, reporte=reporte)

    assert len(resultado) == 1
    assert reporte.exists()
    assert resultado.iloc[0]["filas"] == 1
    assert resultado.iloc[0]["error_lectura"] == ""


def test_inventariar_carpeta_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        inventariar(
            bronce=tmp_path / "no_existe",
            reporte=tmp_path / "reporte.csv",
        )
