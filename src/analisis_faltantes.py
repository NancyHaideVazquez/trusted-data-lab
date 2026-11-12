
"""T04 - Análisis de valores faltantes de Banxico."""

import pandas as pd

from src.diagnostico import buscar_historico
from src.lectura import cargar_dataframe, convertir_fecha
from src.diagnostico import RAIZ


def main():

    # Buscar la captura histórica más reciente
    ruta = buscar_historico("banxico", "SF43783")

    print("Archivo analizado:", ruta.name)

    # Leer los datos originales
    df = cargar_dataframe(ruta)

    # Convertir fechas
    df["fecha_convertida"] = convertir_fecha(df["fecha"])
    df["anio"] = df["fecha_convertida"].dt.year

    # Identificar valores faltantes
    valores = df["dato"].astype("string").str.strip()

    df["faltante"] = (
        valores.isna() |
        valores.isin(["", "N/E", "N/D"])
    )

    # Contar registros por año
    reporte = df.groupby("anio").agg(
        registros=("faltante", "size"),
        faltantes=("faltante", "sum")
    ).reset_index()

    # Calcular registros disponibles
    reporte["disponibles"] = (
        reporte["registros"] - reporte["faltantes"]
    )

    # Calcular porcentaje de faltantes por año
    reporte["porcentaje_faltantes"] = (
        reporte["faltantes"] / reporte["registros"] * 100
    ).round(2)

    # Guardar reporte
    salida = RAIZ / "data" / "reportes" / "faltantes_banxico_por_anio.csv"

    salida.parent.mkdir(parents=True, exist_ok=True)

    reporte.to_csv(
        salida,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nANÁLISIS DE FALTANTES POR AÑO")
    print(reporte.to_string(index=False))

    print("\nTotal de faltantes:", int(df["faltante"].sum()))
    print("Reporte guardado en:", salida)


if __name__ == "__main__":
    main()
