
import numpy as np
import pandas as pd
import pandera.pandas as pa


def crear_esquema_calidad():
    """Define las reglas de calidad para la integración mensual."""

    texto_obligatorio = pa.Check(
        lambda serie: serie.str.strip().str.len() > 0
    )

    esquema = pa.DataFrameSchema(
        {
            "fuente": pa.Column(
                str,
                checks=pa.Check.isin(["inegi", "banxico"]),
                nullable=False
            ),
            "serie_id": pa.Column(
                str,
                checks=texto_obligatorio,
                nullable=False
            ),
            "indicador": pa.Column(
                str,
                checks=texto_obligatorio,
                nullable=False
            ),
            "periodo": pa.Column(
                str,
                checks=pa.Check.str_matches(
                    r"^\d{4}-(0[1-9]|1[0-2])$"
                ),
                nullable=False
            ),
            "valor": pa.Column(
                float,
                checks=pa.Check(
                    lambda serie: np.isfinite(serie)
                ),
                nullable=False,
                coerce=True
            ),
            "unidad": pa.Column(
                str,
                checks=texto_obligatorio,
                nullable=False
            ),
            "frecuencia": pa.Column(
                str,
                checks=pa.Check.eq("mensual"),
                nullable=False
            ),
            "metodo": pa.Column(
                str,
                checks=texto_obligatorio,
                nullable=False
            ),
            "cobertura": pa.Column(
                str,
                checks=texto_obligatorio,
                nullable=False
            ),
        },
        checks=pa.Check(
            lambda df: ~df.duplicated(
                subset=["fuente", "serie_id", "periodo"]
            ),
            error="No debe haber periodos duplicados por serie"
        ),
        strict=True
    )

    return esquema


def validar_calidad(datos):
    """Valida sin modificar el DataFrame original."""
    esquema = crear_esquema_calidad()
    return esquema.validate(datos.copy(), lazy=True)
