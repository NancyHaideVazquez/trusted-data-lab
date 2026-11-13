
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import src.analisis_faltantes as faltantes
import src.analisis_estacionariedad as estacionariedad


def crear_datos_estadisticos(n=72, fuente="inegi"):
    fechas = pd.date_range(
        "2019-01-01",
        periods=n,
        freq="MS",
    )

    rng = np.random.default_rng(2026)
    valores = rng.normal(0, 1, n).cumsum()

    return pd.DataFrame({
        "fuente": [fuente] * n,
        "periodo": fechas.strftime("%Y-%m"),
        "fecha": fechas,
        "valor": valores,
    })


def test_analisis_faltantes_genera_reporte(tmp_path, monkeypatch):
    archivo = tmp_path / "banxico.json"
    archivo.write_text("{}", encoding="utf-8")

    datos = pd.DataFrame({
        "fecha": [
            "2024-01-01",
            "2024-02-01",
            "2024-03-01",
            "2025-01-01",
            "2025-02-01",
        ],
        "dato": [
            "10.5",
            "N/E",
            "",
            "N/D",
            "8.5",
        ],
    })

    monkeypatch.setattr(
        faltantes, "RAIZ", tmp_path
    )
    monkeypatch.setattr(
        faltantes, "buscar_historico",
        lambda fuente, serie: archivo,
    )
    monkeypatch.setattr(
        faltantes, "cargar_dataframe",
        lambda ruta: datos.copy(),
    )

    faltantes.main()

    salida = (
        tmp_path
        / "data"
        / "reportes"
        / "faltantes_banxico_por_anio.csv"
    )

    assert salida.exists()

    reporte = pd.read_csv(salida)

    assert reporte["registros"].sum() == 5
    assert reporte["faltantes"].sum() == 3
    assert reporte["disponibles"].sum() == 2

    fila_2024 = reporte.loc[
        reporte["anio"] == 2024
    ].iloc[0]

    assert fila_2024["faltantes"] == 2
    assert fila_2024["porcentaje_faltantes"] == pytest.approx(
        66.67
    )


def test_estacionariedad_serie_vacia(tmp_path, monkeypatch):
    monkeypatch.setattr(
        estacionariedad,
        "CARPETA_SALIDA",
        tmp_path,
    )

    datos = crear_datos_estadisticos()

    with pytest.raises(ValueError, match="serie vacia"):
        estacionariedad.analizar_serie(
            "prueba",
            "fuente_inexistente",
            "Serie de prueba",
            datos,
        )


def test_estacionariedad_meses_faltantes(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        estacionariedad,
        "CARPETA_SALIDA",
        tmp_path,
    )

    datos = crear_datos_estadisticos()
    datos = datos.drop(index=10)

    with pytest.raises(ValueError, match="meses faltantes"):
        estacionariedad.analizar_serie(
            "prueba",
            "inegi",
            "Serie de prueba",
            datos,
        )


def test_estacionariedad_analisis_completo(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        estacionariedad,
        "CARPETA_SALIDA",
        tmp_path,
    )

    datos = crear_datos_estadisticos()

    estacionariedad.analizar_serie(
        "prueba",
        "inegi",
        "Serie de prueba",
        datos,
    )

    archivos = [
        "prueba_adf.txt",
        "prueba_acf_original.png",
        "prueba_pacf_original.png",
        "prueba_acf_diff1.png",
        "prueba_pacf_diff1.png",
    ]

    for nombre in archivos:
        assert (tmp_path / nombre).exists()

    contenido = (
        tmp_path / "prueba_adf.txt"
    ).read_text(encoding="utf-8")

    assert "Serie: prueba" in contenido
    assert "Serie original" in contenido
    assert "Primera diferencia" in contenido


def test_estacionariedad_main_sin_archivo(
    tmp_path, monkeypatch
):
    archivo = tmp_path / "no_existe.csv"

    monkeypatch.setattr(
        estacionariedad,
        "ARCHIVO_ORO",
        archivo,
    )

    with pytest.raises(
        FileNotFoundError,
        match="No se encontro",
    ):
        estacionariedad.main()


def test_estacionariedad_main_completo(
    tmp_path, monkeypatch
):
    archivo = tmp_path / "indicadores.csv"

    datos_inegi = crear_datos_estadisticos(
        n=72,
        fuente="inegi",
    )

    datos_banxico = crear_datos_estadisticos(
        n=72,
        fuente="banxico",
    )

    datos = pd.concat(
        [datos_inegi, datos_banxico],
        ignore_index=True,
    )

    datos.to_csv(archivo, index=False)

    monkeypatch.setattr(
        estacionariedad,
        "ARCHIVO_ORO",
        archivo,
    )
    monkeypatch.setattr(
        estacionariedad,
        "CARPETA_SALIDA",
        tmp_path / "resultados",
    )

    estacionariedad.main()

    carpeta = tmp_path / "resultados"

    assert (
        carpeta / "inegi_inflacion_adf.txt"
    ).exists()

    assert (
        carpeta / "banxico_tiie_adf.txt"
    ).exists()
