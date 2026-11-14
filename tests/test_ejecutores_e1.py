
import json

import pandas as pd
import pytest

import src.ejecutar_calidad as calidad
import src.ejecutar_cuarentena as cuarentena
import src.ejecutar_discretizacion as discretizacion
import src.ejecutar_escalado as escalado


def datos_ejemplo():
    return pd.DataFrame({
        "serie_id": ["SF43783", "SF43783", "910402"],
        "valor": [1.0, 2.0, 3.0],
    })


def test_calidad_archivo_inexistente(tmp_path, monkeypatch):
    monkeypatch.setattr(
        calidad, "ENTRADA", tmp_path / "no_existe.csv"
    )

    with pytest.raises(FileNotFoundError):
        calidad.ejecutar()


def test_calidad_aprobada(tmp_path, monkeypatch):
    entrada = tmp_path / "entrada.csv"
    reporte = tmp_path / "reportes" / "calidad.csv"

    datos_ejemplo().to_csv(entrada, index=False)

    monkeypatch.setattr(calidad, "ENTRADA", entrada)
    monkeypatch.setattr(calidad, "REPORTE", reporte)
    monkeypatch.setattr(
        calidad,
        "validar_calidad",
        lambda datos: datos.copy(),
    )

    calidad.ejecutar()

    assert reporte.exists()

    resultado = pd.read_csv(reporte)

    assert resultado.loc[0, "estado"] == "APROBADO"
    assert resultado.loc[0, "registros"] == 3
    assert resultado.loc[0, "registros_aprobados"] == 3
    assert resultado.loc[0, "errores_detectados"] == 0


def test_calidad_rechazada(tmp_path, monkeypatch):
    entrada = tmp_path / "entrada.csv"
    reporte = tmp_path / "reportes" / "calidad.csv"

    datos_ejemplo().to_csv(entrada, index=False)

    monkeypatch.setattr(calidad, "ENTRADA", entrada)
    monkeypatch.setattr(calidad, "REPORTE", reporte)

    class ErrorSimulado(calidad.SchemaErrors):
        @property
        def failure_cases(self):
            return pd.DataFrame({
                "failure_case": ["valor invalido", "duplicado"]
            })

    def rechazar(_datos):
        raise ErrorSimulado.__new__(ErrorSimulado)

    monkeypatch.setattr(
        calidad, "validar_calidad", rechazar
    )

    with pytest.raises(SystemExit) as error:
        calidad.ejecutar()

    assert error.value.code == 1

    resultado = pd.read_csv(reporte)
    assert resultado.loc[0, "estado"] == "RECHAZADO"
    assert resultado.loc[0, "errores_detectados"] == 2


def test_cuarentena_archivo_inexistente(tmp_path, monkeypatch):
    monkeypatch.setattr(
        cuarentena, "ENTRADA", tmp_path / "no_existe.csv"
    )

    with pytest.raises(FileNotFoundError):
        cuarentena.ejecutar()


@pytest.mark.parametrize(
    "cantidad_rechazados, estado",
    [
        (0, "SIN_RECHAZOS"),
        (1, "CON_RECHAZOS"),
    ],
)
def test_cuarentena_genera_reportes(
    tmp_path, monkeypatch, cantidad_rechazados, estado
):
    entrada = tmp_path / "entrada.csv"
    registros = tmp_path / "cuarentena" / "registros"
    reportes = tmp_path / "cuarentena" / "reportes"

    datos_ejemplo().to_csv(entrada, index=False)

    monkeypatch.setattr(cuarentena, "ENTRADA", entrada)
    monkeypatch.setattr(cuarentena, "REGISTROS", registros)
    monkeypatch.setattr(cuarentena, "REPORTES", reportes)

    def separar(datos):
        if cantidad_rechazados:
            validos = datos.iloc[1:].copy()
            rechazados = datos.iloc[:1].copy()
        else:
            validos = datos.copy()
            rechazados = datos.iloc[:0].copy()

        rechazados["motivo"] = "Dato de prueba"
        return validos, rechazados

    monkeypatch.setattr(
        cuarentena, "separar_cuarentena", separar
    )

    cuarentena.ejecutar()

    archivo_reporte = reportes / "reporte_cuarentena.csv"
    archivo_rechazados = (
        registros / "integracion_mensual_rechazados.csv"
    )

    assert archivo_reporte.exists()
    assert archivo_rechazados.exists()

    resultado = pd.read_csv(archivo_reporte)

    assert resultado.loc[0, "estado"] == estado
    assert resultado.loc[0, "registros_originales"] == 3
    assert (
        resultado.loc[0, "registros_rechazados"]
        == cantidad_rechazados
    )


def test_discretizacion_genera_archivos(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    carpeta = tmp_path / "data" / "reportes"
    carpeta.mkdir(parents=True)

    for fuente in ("banxico", "inegi"):
        datos_ejemplo().to_csv(
            carpeta / f"limpieza_preliminar_{fuente}.csv",
            index=False,
        )

    def discretizar(datos, metodo):
        resultado = datos.copy()
        resultado[f"valor_{metodo}"] = [
            "bajo", "medio", "alto"
        ]

        return resultado, {"metodo": metodo}

    monkeypatch.setattr(
        discretizacion, "discretizar_datos", discretizar
    )

    discretizacion.main()

    for fuente in ("banxico", "inegi"):
        archivo = carpeta / f"discretizacion_{fuente}.csv"
        assert archivo.exists()

        resultado = pd.read_csv(archivo)
        assert "valor_cut" in resultado.columns
        assert "valor_qcut" in resultado.columns

    archivo_json = carpeta / "parametros_discretizacion.json"
    assert archivo_json.exists()

    parametros = json.loads(
        archivo_json.read_text(encoding="utf-8")
    )

    assert set(parametros) == {"banxico", "inegi"}
    assert parametros["banxico"]["cut"]["metodo"] == "cut"
    assert parametros["inegi"]["qcut"]["metodo"] == "qcut"


def test_escalado_genera_archivos(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    carpeta = tmp_path / "data" / "reportes"
    carpeta.mkdir(parents=True)

    for fuente in ("banxico", "inegi"):
        datos_ejemplo().to_csv(
            carpeta / f"limpieza_preliminar_{fuente}.csv",
            index=False,
        )

    def escalar(datos):
        resultado = datos.copy()
        resultado["valor_escalado"] = (
            resultado["valor"] / 3.0
        )
        return resultado, {"metodo": "prueba"}

    monkeypatch.setattr(
        escalado, "escalar_datos", escalar
    )

    escalado.main()

    for fuente in ("banxico", "inegi"):
        archivo = carpeta / f"escalado_{fuente}.csv"
        assert archivo.exists()

        resultado = pd.read_csv(archivo)
        assert "valor_escalado" in resultado.columns

    archivo_json = carpeta / "parametros_escalado.json"
    assert archivo_json.exists()

    parametros = json.loads(
        archivo_json.read_text(encoding="utf-8")
    )

    assert set(parametros) == {"banxico", "inegi"}
    assert parametros["banxico"]["metodo"] == "prueba"
