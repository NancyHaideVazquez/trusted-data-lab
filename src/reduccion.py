
import pandas as pd


def reducir_datos(df):
    # Trabajar con una copia para no modificar el original
    datos = df.copy()

    # Convertir fechas y valores
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos["valor"] = pd.to_numeric(datos["valor"], errors="coerce")

    # Obtener el mes de cada registro
    datos["periodo"] = datos["fecha"].dt.to_period("M")

    # Agrupar por fuente, serie y mes
    resultado = datos.groupby(
        ["fuente", "serie_id", "periodo"]
    ).agg(
        valor=("valor", "mean"),
        registros_originales=("valor", "size"),
        registros_validos=("valor", "count")
    ).reset_index()

    # Convertir el periodo a texto
    resultado["periodo"] = resultado["periodo"].astype(str)

    # Conservar información sobre la serie
    resultado["unidad_original"] = "porcentaje anual"
    resultado["metodo_reduccion"] = "promedio mensual"

    return resultado
