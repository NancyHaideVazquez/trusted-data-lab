import hashlib

import pandas as pd
import pytest

import pipeline.ejecutar_pipeline as pipeline


def configurar_rutas(monkeypatch, tmp_path):
    """
    Crea archivos JSON simulados de Bronce.

    Todas las entradas y salidas de las pruebas
    permanecen en una carpeta temporal.
    """

    # 1. Crear datos originales simulados
    inegi = pd.DataFrame({
        "TIME_PERIOD": ["2026-01", "2026-02"],
        "OBS_VALUE": [0.5, 0.8]
    })

    banxico = pd.DataFrame({
        "fecha": ["01/01/2026", "01/02/2026"],
        "dato": ["7.5", "7.2"]
    })

    carpeta_bronce = tmp_path / "bronce"
    carpeta_bronce.mkdir()

    ruta_inegi = carpeta_bronce / "910402_historico.json"
    ruta_banxico = carpeta_bronce / "SF43783_historico.json"

    inegi.to_json(ruta_inegi, orient="records")
    banxico.to_json(ruta_banxico, orient="records")

    # 2. Simular la búsqueda de históricos
    def buscar_historico_falso(fuente, indicador):
        if fuente == "inegi" and indicador == "910402":
            return ruta_inegi

        if fuente == "banxico" and indicador == "SF43783":
            return ruta_banxico

        raise FileNotFoundError(
            f"Serie desconocida: {fuente}/{indicador}"
        )

    def cargar_dataframe_falso(ruta):
        return pd.read_json(ruta)


    # Ejecutar el diagnostico real con los JSON temporales,
    # sin generar reportes fuera de la carpeta de pruebas
    from src.diagnostico import diagnosticar as diagnosticar_real

    def diagnosticar_temporal(ruta, fuente, guardar_reporte=False):
        return diagnosticar_real(
            ruta, fuente, guardar_reporte=False
        )

    monkeypatch.setattr(
        pipeline,
        "diagnosticar",
        diagnosticar_temporal
    )

    monkeypatch.setattr(
        pipeline,
        "buscar_historico",
        buscar_historico_falso
    )

    monkeypatch.setattr(
        pipeline,
        "cargar_dataframe",
        cargar_dataframe_falso
    )

    # 3. Redirigir las salidas del pipeline
    plata = tmp_path / "plata" / "integracion.csv"

    oro = tmp_path / "oro" / "indicadores_mensuales.csv"

    cuarentena = (
        tmp_path / "cuarentena" / "registros" / "rechazados.csv"
    )

    reporte = (
        tmp_path / "cuarentena" / "reportes" / "reporte.csv"
    )

    monkeypatch.setattr(
        pipeline, "SALIDA_PLATA", plata
    )
    monkeypatch.setattr(
        pipeline, "SALIDA_ORO", oro
    )
    monkeypatch.setattr(
        pipeline, "SALIDA_CUARENTENA", cuarentena
    )
    monkeypatch.setattr(
        pipeline, "SALIDA_REPORTE", reporte
    )

    # Guardar la bitácora de pruebas en una ruta temporal
    bitacora_temporal = (
        tmp_path / "logs" / "pipeline_ejecuciones.csv"
    )

    monkeypatch.setattr(
        pipeline,
        "RUTA_BITACORA",
        bitacora_temporal
    )

    return ruta_inegi, ruta_banxico, plata, oro, cuarentena, reporte


def test_pipeline_publica_datos_validos(monkeypatch, tmp_path):
    _, _, plata, oro, cuarentena, reporte = configurar_rutas(
        monkeypatch, tmp_path
    )

    pipeline.ejecutar_pipeline()

    datos_plata = pd.read_csv(plata)
    datos_oro = pd.read_csv(oro)
    rechazados = pd.read_csv(cuarentena)
    resumen = pd.read_csv(reporte)

    assert len(datos_plata) == 4
    assert len(datos_oro) == 4
    assert len(rechazados) == 0
    assert resumen.loc[0, "estado"] == "SIN_RECHAZOS"


def test_pipeline_separa_registros_invalidos(
    monkeypatch, tmp_path
):
    ruta_inegi, _, plata, oro, cuarentena, reporte = (
        configurar_rutas(monkeypatch, tmp_path)
    )

    # Introducir un faltante solo en el JSON temporal
    datos = pd.read_json(ruta_inegi)
    datos.loc[0, "OBS_VALUE"] = None
    datos.to_json(ruta_inegi, orient="records")

    pipeline.ejecutar_pipeline()

    datos_plata = pd.read_csv(plata)
    datos_oro = pd.read_csv(oro)
    rechazados = pd.read_csv(cuarentena)
    resumen = pd.read_csv(reporte)

    assert len(datos_plata) == 3
    assert len(datos_oro) == 3
    assert len(rechazados) == 1
    assert pd.isna(rechazados.loc[0, "valor"])
    assert "valor" in rechazados.loc[
        0, "motivo_rechazo"
    ].lower()
    assert resumen.loc[0, "estado"] == "CON_RECHAZOS"


def test_pipeline_detiene_error_estructural(
    monkeypatch, tmp_path
):
    ruta_inegi, _, plata, oro, _, _ = configurar_rutas(
        monkeypatch, tmp_path
    )

    # Eliminar un campo obligatorio del JSON temporal
    datos = pd.read_json(ruta_inegi)
    datos = datos.drop(columns=["OBS_VALUE"])
    datos.to_json(ruta_inegi, orient="records")

    # Simular publicaciones anteriores
    plata.parent.mkdir(parents=True, exist_ok=True)
    oro.parent.mkdir(parents=True, exist_ok=True)

    plata.write_text("plata_anterior", encoding="utf-8")
    oro.write_text("oro_anterior", encoding="utf-8")

    with pytest.raises(ValueError):
        pipeline.ejecutar_pipeline()

    assert plata.read_text(
        encoding="utf-8"
    ) == "plata_anterior"

    assert oro.read_text(
        encoding="utf-8"
    ) == "oro_anterior"


def test_pipeline_publica_oro(monkeypatch, tmp_path):
    _, _, _, oro, _, _ = configurar_rutas(
        monkeypatch, tmp_path
    )

    pipeline.ejecutar_pipeline()

    assert oro.exists()

    datos = pd.read_csv(
        oro, dtype={"serie_id": str}
    )

    assert len(datos) == 4
    assert len(datos.columns) == 8


def test_pipeline_oro_conserva_series(monkeypatch, tmp_path):
    _, _, _, oro, _, _ = configurar_rutas(
        monkeypatch, tmp_path
    )

    pipeline.ejecutar_pipeline()

    datos = pd.read_csv(
        oro, dtype={"serie_id": str}
    )

    assert set(datos["fuente"]) == {"inegi", "banxico"}
    assert set(datos["serie_id"]) == {"910402", "SF43783"}

    assert len(datos[datos["fuente"] == "inegi"]) == 2
    assert len(datos[datos["fuente"] == "banxico"]) == 2


def test_pipeline_no_publica_si_falla_oro(
    monkeypatch, tmp_path
):
    _, _, plata, oro, _, _ = configurar_rutas(
        monkeypatch, tmp_path
    )

    plata.parent.mkdir(parents=True, exist_ok=True)
    plata.write_text(
        "publicacion_anterior",
        encoding="utf-8"
    )

    def fallar_preparacion(_datos):
        raise ValueError("Error simulado en Oro")

    monkeypatch.setattr(
        pipeline, "preparar_oro", fallar_preparacion
    )

    with pytest.raises(ValueError):
        pipeline.ejecutar_pipeline()

    assert plata.read_text(
        encoding="utf-8"
    ) == "publicacion_anterior"

    assert not oro.exists()


def test_pipeline_no_modifica_bronce(
    monkeypatch, tmp_path
):
    ruta_inegi, ruta_banxico, _, _, _, _ = configurar_rutas(
        monkeypatch, tmp_path
    )

    # Guardar los contenidos originales de los JSON
    antes_inegi = ruta_inegi.read_bytes()
    antes_banxico = ruta_banxico.read_bytes()

    pipeline.ejecutar_pipeline()

    # Comprobar que Bronce permanece idéntico
    assert ruta_inegi.read_bytes() == antes_inegi
    assert ruta_banxico.read_bytes() == antes_banxico

def test_pipeline_es_idempotente(monkeypatch, tmp_path):
    """Dos ejecuciones con el mismo Bronce generan salidas identicas."""

    _, _, plata, oro, cuarentena, reporte = configurar_rutas(
        monkeypatch, tmp_path
    )

    rutas = [plata, oro, cuarentena, reporte]

    # Primera ejecución
    pipeline.ejecutar_pipeline()

    hashes_primera = {
        str(ruta): hashlib.sha256(ruta.read_bytes()).hexdigest()
        for ruta in rutas
    }

    conteos_primera = {
        str(ruta): len(pd.read_csv(ruta))
        for ruta in rutas
    }

    # Segunda ejecución
    pipeline.ejecutar_pipeline()

    hashes_segunda = {
        str(ruta): hashlib.sha256(ruta.read_bytes()).hexdigest()
        for ruta in rutas
    }

    conteos_segunda = {
        str(ruta): len(pd.read_csv(ruta))
        for ruta in rutas
    }

    assert hashes_primera == hashes_segunda
    assert conteos_primera == conteos_segunda

    # No se acumulan duplicados entre ejecuciones
    datos_plata = pd.read_csv(plata)
    datos_oro = pd.read_csv(oro)

    claves = ["fuente", "serie_id", "periodo"]

    assert not datos_plata.duplicated(claves).any()
    assert not datos_oro.duplicated(claves).any()


def test_pipeline_omite_discretizacion_con_pocos_valores(
    monkeypatch, tmp_path, capsys
):
    """La falta de variedad no impide publicar datos validos."""

    _, _, plata, oro, _, _ = configurar_rutas(
        monkeypatch, tmp_path
    )

    pipeline.ejecutar_pipeline()

    mensajes = capsys.readouterr().out

    assert "Discretizacion INEGI: omitida" in mensajes
    assert "Discretizacion BANXICO: omitida" in mensajes

    assert plata.exists()
    assert oro.exists()

    assert len(pd.read_csv(plata)) == 4
    assert len(pd.read_csv(oro)) == 4
