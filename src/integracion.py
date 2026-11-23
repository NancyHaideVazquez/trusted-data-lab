import pandas as pd

from src.trazabilidad import obtener_trazabilidad


def integrar_datos(inegi, banxico, incluir_trazabilidad=False):
    """Integra las series mensuales y opcionalmente su trazabilidad."""

    datos_inegi = inegi.copy()
    datos_banxico = banxico.copy()

    datos_inegi["periodo"] = (
        pd.to_datetime(datos_inegi["fecha"], errors="coerce")
        .dt.strftime("%Y-%m")
    )

    datos_inegi["indicador"] = "Inflacion mensual"
    datos_inegi["unidad"] = "porcentaje"
    datos_inegi["frecuencia"] = "mensual"
    datos_inegi["metodo"] = "valor mensual original"
    datos_inegi["cobertura"] = "nacional"

    datos_banxico["indicador"] = "TIIE a 28 dias"
    datos_banxico["unidad"] = "porcentaje anual"
    datos_banxico["frecuencia"] = "mensual"
    datos_banxico["metodo"] = "promedio mensual"
    datos_banxico["cobertura"] = "nacional"

    columnas = [
        "fuente",
        "serie_id",
        "indicador",
        "periodo",
        "valor",
        "unidad",
        "frecuencia",
        "metodo",
        "cobertura",
    ]

    if incluir_trazabilidad:
        trazabilidad_inegi = obtener_trazabilidad("inegi")
        trazabilidad_banxico = obtener_trazabilidad("banxico")

        for columna, valor in trazabilidad_inegi.items():
            datos_inegi[columna] = valor

        for columna, valor in trazabilidad_banxico.items():
            datos_banxico[columna] = valor

        columnas += [
            "archivo_origen",
            "fecha_ingesta_utc",
        ]

    datos_inegi = datos_inegi[columnas]
    datos_banxico = datos_banxico[columnas]

    integrado = pd.concat(
        [datos_inegi, datos_banxico],
        ignore_index=True,
    )

    integrado = integrado.sort_values(
        ["periodo", "fuente", "serie_id"]
    ).reset_index(drop=True)

    return integrado