import pandas as pd
import pytest

from src.trazabilidad import obtener_trazabilidad
from src.integracion import integrar_datos
from src.oro import preparar_oro


def crear_datos():
    inegi = pd.DataFrame({
        "fuente": ["inegi"],
        "serie_id": ["910402"],
        "fecha": ["2026-10-01"],
        "valor": [0.44],
    })

    banxico = pd.DataFrame({
        "fuente": ["banxico"],
        "serie_id": ["SF43783"],
        "periodo": ["2026-11"],
        "valor": [6.662925],
    })

    return inegi, banxico


def test_trazabilidad_inegi():
    datos = obtener_trazabilidad("inegi")

    assert "archivo_origen" in datos
    assert "fecha_ingesta_utc" in datos
    assert "910402_historico" in datos["archivo_origen"]


def test_trazabilidad_banxico():
    datos = obtener_trazabilidad("banxico")

    assert "archivo_origen" in datos
    assert "fecha_ingesta_utc" in datos
    assert "SF43783_historico" in datos["archivo_origen"]


def test_rechaza_fuente_desconocida():
    with pytest.raises(ValueError):
        obtener_trazabilidad("desconocida")


def test_integracion_con_trazabilidad():
    inegi, banxico = crear_datos()

    resultado = integrar_datos(
        inegi,
        banxico,
        incluir_trazabilidad=True,
    )

    assert len(resultado) == 2
    assert "archivo_origen" in resultado.columns
    assert "fecha_ingesta_utc" in resultado.columns
    assert resultado["archivo_origen"].notna().all()
    assert resultado["fecha_ingesta_utc"].notna().all()


def test_oro_conserva_trazabilidad():
    inegi, banxico = crear_datos()

    plata = integrar_datos(
        inegi,
        banxico,
        incluir_trazabilidad=True,
    )

    oro = preparar_oro(plata)

    assert len(oro) == 2
    assert len(oro.columns) == 10
    assert oro["archivo_origen"].notna().all()
    assert oro["fecha_ingesta_utc"].notna().all()


def test_oro_conserva_valores():
    inegi, banxico = crear_datos()

    plata = integrar_datos(
        inegi,
        banxico,
        incluir_trazabilidad=True,
    )

    oro = preparar_oro(plata)

    valores_plata = plata.set_index(
        ["fuente", "serie_id", "periodo"]
    )["valor"].sort_index()

    valores_oro = oro.set_index(
        ["fuente", "serie_id", "periodo"]
    )["valor"].sort_index()

    pd.testing.assert_series_equal(
        valores_plata,
        valores_oro,
    )