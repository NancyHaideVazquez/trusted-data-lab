
import pandas as pd
import pytest

from src.cuarentena import separar_cuarentena


def crear_datos():
    return pd.DataFrame({
        "fuente": ["inegi", "banxico", "inegi"],
        "serie_id": ["910402", "SF43783", "910402"],
        "indicador": [
            "Inflacion mensual",
            "TIIE a 28 dias",
            "Inflacion mensual"
        ],
        "periodo": ["2026-01", "2026-01", "2026-02"],
        "valor": [0.5, 7.5, 0.8],
        "unidad": [
            "porcentaje",
            "porcentaje anual",
            "porcentaje"
        ],
        "frecuencia": ["mensual", "mensual", "mensual"],
        "metodo": [
            "valor mensual original",
            "promedio mensual",
            "valor mensual original"
        ],
        "cobertura": [
            "nacional",
            "nacional",
            "nacional"
        ]
    })


def test_todos_validos():
    datos = crear_datos()

    validos, rechazados = separar_cuarentena(datos)

    assert len(validos) == 3
    assert len(rechazados) == 0


def test_separa_periodo_invalido():
    datos = crear_datos()
    datos.loc[0, "periodo"] = "2026-13"

    validos, rechazados = separar_cuarentena(datos)

    assert len(validos) == 2
    assert len(rechazados) == 1
    assert rechazados.iloc[0]["periodo"] == "2026-13"

def test_conserva_motivo_rechazo():
    datos = crear_datos()
    datos.loc[0, "periodo"] = "fecha_invalida"

    _, rechazados = separar_cuarentena(datos)

    motivo = rechazados.iloc[0]["motivo_rechazo"]

    assert "periodo" in motivo.lower()
    assert "AAAA-MM" in motivo

def test_separa_valor_faltante():
    datos = crear_datos()
    datos.loc[1, "valor"] = None

    validos, rechazados = separar_cuarentena(datos)

    assert len(validos) == 2
    assert len(rechazados) == 1
    assert pd.isna(rechazados.iloc[0]["valor"])

    assert "valor" in (
        rechazados.iloc[0]["motivo_rechazo"].lower()
    )


def test_separa_varios_errores():
    datos = crear_datos()

    datos.loc[0, "periodo"] = "2026-13"
    datos.loc[2, "unidad"] = ""

    validos, rechazados = separar_cuarentena(datos)

    assert len(validos) == 1
    assert len(rechazados) == 2


def test_no_pierde_registros():
    datos = crear_datos()
    datos.loc[0, "periodo"] = "2026-13"

    validos, rechazados = separar_cuarentena(datos)

    assert len(validos) + len(rechazados) == len(datos)


def test_no_modifica_originales():
    datos = crear_datos()
    copia = datos.copy(deep=True)

    separar_cuarentena(datos)

    pd.testing.assert_frame_equal(datos, copia)


def test_detiene_error_estructural():
    datos = crear_datos()

    datos = datos.drop(columns=["cobertura"])

    with pytest.raises(ValueError):
        separar_cuarentena(datos)


def test_separa_duplicado_con_motivo():
    datos = crear_datos()

    duplicado = datos.iloc[[0]].copy()

    datos = pd.concat(
        [datos, duplicado],
        ignore_index=True
    )

    validos, rechazados = separar_cuarentena(datos)

    assert len(validos) == 3
    assert len(rechazados) == 1

    assert len(validos) + len(rechazados) == len(datos)

    motivo = str(
        rechazados.iloc[0]["motivo_rechazo"]
    )

    assert motivo.strip()
    assert "duplic" in motivo.lower()

    # El duplicado no debe recibir errores falsos
    # sobre sus columnas, porque son datos validos.
    assert "fuente invalida" not in motivo.lower()
    assert "periodo invalido" not in motivo.lower()
    assert "valor invalido" not in motivo.lower()


def test_separa_valor_infinito_con_motivo():
    datos = crear_datos()

    # Infinito no es un valor numerico finito.
    datos.loc[1, "valor"] = float("inf")

    validos, rechazados = separar_cuarentena(datos)

    assert len(validos) == 2
    assert len(rechazados) == 1

    assert len(validos) + len(rechazados) == len(datos)

    motivo = str(
        rechazados.iloc[0]["motivo_rechazo"]
    )

    assert "valor" in motivo.lower()
    assert "finito" in motivo.lower()
