
from pathlib import Path

from streamlit.testing.v1 import AppTest

RUTA_APP = Path(__file__).resolve().parents[1] / "tablero" / "app.py"


def cargar_tablero():
    app = AppTest.from_file(
        str(RUTA_APP),
        default_timeout=60,
    )

    app.run()

    assert len(app.exception) == 0

    return app


def test_archivo_tablero_existe():
    assert RUTA_APP.is_file()


def test_tablero_sin_excepciones():
    cargar_tablero()


def test_titulo_observatorio():
    app = cargar_tablero()

    assert any(
        "Observatorio de Vivienda y Costos de Colima"
        in titulo.value
        for titulo in app.title
    )


def test_pestanas_tablero():
    app = cargar_tablero()

    esperadas = {
        "Mapa territorial",
        "Indicadores económicos",
        "Calidad de datos",
        "Trazabilidad",
    }

    encontradas = {
        pestana.label for pestana in app.tabs
    }

    assert esperadas.issubset(encontradas)


def test_metricas_geoespaciales():
    app = cargar_tablero()

    metricas = {
        metrica.label: metrica.value
        for metrica in app.metric
    }

    assert metricas["Municipios"] == "10"
    assert metricas["Asignaciones espaciales"] == "10"
    assert metricas["Asignaciones correctas"] == "100%"


def test_filtro_colima():
    app = cargar_tablero()

    app.sidebar.selectbox[0].select("Colima").run()

    assert len(app.exception) == 0
    assert app.sidebar.selectbox[0].value == "Colima"

    tabla = app.dataframe[0].value

    assert len(tabla) == 1
    assert tabla.iloc[0]["cvegeo"] == "06002"


def test_filtro_villa_de_alvarez():
    app = cargar_tablero()

    app.sidebar.selectbox[0].select(
        "Villa de Álvarez"
    ).run()

    assert len(app.exception) == 0

    tabla = app.dataframe[0].value

    assert len(tabla) == 1
    assert tabla.iloc[0]["cvegeo"] == "06010"


def test_filtro_todos_municipios():
    app = cargar_tablero()

    app.sidebar.selectbox[0].select("Todos").run()

    assert len(app.exception) == 0
    assert len(app.dataframe[0].value) == 10
