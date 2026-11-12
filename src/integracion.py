
import pandas as pd


def integrar_datos(inegi, banxico):
    # Copiar los datos para no modificar los originales
    datos_inegi = inegi.copy()
    datos_banxico = banxico.copy()

    # Preparar los datos de INEGI
    datos_inegi["periodo"] = pd.to_datetime(
        datos_inegi["fecha"], errors="coerce"
    ).dt.strftime("%Y-%m")

    datos_inegi["indicador"] = "Inflacion mensual"
    datos_inegi["unidad"] = "porcentaje"
    datos_inegi["frecuencia"] = "mensual"
    datos_inegi["metodo"] = "valor mensual original"
    datos_inegi["cobertura"] = "nacional"

    # Preparar los datos de Banxico
    datos_banxico["indicador"] = "TIIE a 28 dias"
    datos_banxico["unidad"] = "porcentaje anual"
    datos_banxico["frecuencia"] = "mensual"
    datos_banxico["metodo"] = "promedio mensual"
    datos_banxico["cobertura"] = "nacional"

    # Seleccionar las columnas finales
    columnas = [
        "fuente",
        "serie_id",
        "indicador",
        "periodo",
        "valor",
        "unidad",
        "frecuencia",
        "metodo",
        "cobertura"
    ]

    datos_inegi = datos_inegi[columnas]
    datos_banxico = datos_banxico[columnas]

    # Integrar los registros
    integrado = pd.concat(
        [datos_inegi, datos_banxico],
        ignore_index=True
    )

    # Ordenar por periodo, fuente y serie
    integrado = integrado.sort_values(
        ["periodo", "fuente", "serie_id"]
    ).reset_index(drop=True)

    return integrado
