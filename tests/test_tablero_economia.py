from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture
def tablero_economia(tmp_path):
    registros = []

    fechas = pd.date_range(
        "2024-01-01",
        periods=14,
        freq="MS",
    )

    for i, fecha in enumerate(fechas, start=1):
        for fuente, serie, indicador, valor, unidad in [
            (
                "inegi",
                "910402",
                "Inflacion mensual",
                i * 0.1,
                "porcentaje",
            ),
            (
                "banxico",
                "SF43783",
                "TIIE a 28 dias",
                4 + i * 0.2,
                "porcentaje anual",
            ),
        ]:
            registros.append(
                {
                    "periodo": fecha.strftime("%Y-%m"),
                    "fuente": fuente,
                    "serie_id": serie,
                    "indicador": indicador,
                    "valor": valor,
                    "unidad": unidad,
                    "metodo": "prueba",
                    "cobertura": "nacional",
                    "archivo_origen": "fixture.json",
                    "fecha_ingesta_utc": "2025-03-01T00:00:00Z",
                }
            )

    ruta_csv = tmp_path / "oro_prueba.csv"

    pd.DataFrame(registros).to_csv(
        ruta_csv,
        index=False,
    )

    codigo = (RAIZ / "tablero/app.py").read_text(
        encoding="utf-8"
    )

    codigo = codigo.replace(
        "RAIZ = Path(__file__).resolve().parents[1]",
        f"RAIZ = Path({str(RAIZ)!r})",
        1,
    )

    codigo = codigo.replace(
        'RUTA_ORO = RAIZ / "data/oro/indicadores_mensuales_e2.csv"',
        f"RUTA_ORO = Path({str(ruta_csv)!r})",
        1,
    )

    ruta_app = tmp_path / "app_prueba.py"

    ruta_app.write_text(
        codigo,
        encoding="utf-8",
    )

    tablero = AppTest.from_file(
        str(ruta_app),
        default_timeout=60,
    ).run()

    assert len(tablero.exception) == 0

    return tablero


def test_tarjetas_economicas(tablero_economia):
    metricas = {
        m.label: m.value
        for m in tablero_economia.metric
    }

    assert metricas["Observaciones"] == "14"
    assert metricas["Valor máximo"] == "1.40 %"
    assert metricas["Valor mínimo"] == "0.10 %"
    assert metricas["Cambio mensual"] == "+0.10 pp"


def test_graficas_economicas(tablero_economia):
    secciones = [
        s.value for s in tablero_economia.subheader
    ]

    assert "Evolución histórica y tendencia" in secciones
    assert "Comparación económica anual" in secciones
    assert "Variaciones mensuales" in secciones
    assert "Mapa de calor histórico" in secciones
    assert "Relación entre inflación y TIIE" in secciones

    assert len(
        tablero_economia.get("plotly_chart")
    ) == 6


def test_correlacion_economica(tablero_economia):
    metricas = {
        m.label: m.value
        for m in tablero_economia.metric
    }

    assert metricas["Meses comparados"] == "14"
    assert metricas["Correlación de Pearson"] == "1.000"


def test_cambio_indicador_tiie(tablero_economia):
    selector = next(
        s for s in tablero_economia.selectbox
        if "TIIE a 28 dias" in s.options
    )

    selector.select("TIIE a 28 dias").run()

    assert len(tablero_economia.exception) == 0

    metricas = {
        m.label: m.value
        for m in tablero_economia.metric
    }

    assert metricas["Último valor seleccionado"] == "6.80 %"


def test_promedio_movil(tablero_economia):
    selector = tablero_economia.selectbox(
        key="ventana_promedio_movil"
    )

    selector.set_value(3).run()

    assert len(tablero_economia.exception) == 0

    assert tablero_economia.selectbox(
        key="ventana_promedio_movil"
    ).value == 3


def test_periodo_un_mes(tablero_economia):
    fecha = pd.Timestamp("2025-02-01").date()

    tablero_economia.date_input[0].set_value(
        (fecha, fecha)
    ).run()

    assert len(tablero_economia.exception) == 0

    metricas = {
        m.label: m.value
        for m in tablero_economia.metric
    }

    assert metricas["Observaciones"] == "1"
    assert metricas["Cambio mensual"] == "No disponible"

    assert any(
        "meses consecutivos" in aviso.value
        for aviso in tablero_economia.warning
    )