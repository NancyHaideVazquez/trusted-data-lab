
"""T03 - Diagnóstico de calidad de datos."""

from pathlib import Path
import pandas as pd

from src.lectura import cargar_dataframe, convertir_fecha

RAIZ = Path(__file__).resolve().parents[1]
BRONCE = RAIZ / "data" / "bronce"
REPORTE = RAIZ / "data" / "reportes" / "diagnostico_calidad.csv"


def buscar_historico(fuente, indicador):
    """Busca el archivo histórico más reciente."""

    carpeta = BRONCE / fuente

    archivos = list(carpeta.rglob(f"{indicador}_historico*.json"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos históricos de {fuente}"
        )

    archivos.sort(key=lambda ruta: (ruta.parent.name, ruta.name))

    return archivos[-1]


def diagnosticar(ruta, fuente):
    """Analiza la calidad de los datos sin modificar Bronce."""

    df = cargar_dataframe(ruta)

    if fuente == "inegi":
        columna_fecha = "TIME_PERIOD"
        columna_valor = "OBS_VALUE"
    else:
        columna_fecha = "fecha"
        columna_valor = "dato"

    valores = df[columna_valor].astype("string").str.strip()

    faltantes = valores.isna() | valores.isin(["", "N/E", "N/D"])

    numeros = pd.to_numeric(
        valores.mask(faltantes),
        errors="coerce"
    )

    fechas = convertir_fecha(df[columna_fecha])

    duplicados = fechas[fechas.notna()].duplicated().sum()
    fechas_invalidas = fechas.isna().sum()
    valores_invalidos = (numeros.isna() & ~faltantes).sum()

    return {
        "fuente": fuente,
        "archivo": ruta.relative_to(RAIZ).as_posix(),
        "registros": len(df),
        "faltantes": int(faltantes.sum()),
        "duplicados_fecha": int(duplicados),
        "fechas_invalidas": int(fechas_invalidas),
        "valores_invalidos": int(valores_invalidos),
        "minimo": numeros.min(),
        "maximo": numeros.max(),
        "promedio": numeros.mean(),
    }


def main():

    archivos = [
        (buscar_historico("inegi", "910402"), "inegi"),
        (buscar_historico("banxico", "SF43783"), "banxico"),
    ]

    resultados = []

    for ruta, fuente in archivos:
        print(f"\nAnalizando {fuente.upper()}...")
        print(f"Archivo seleccionado: {ruta.name}")

        resultado = diagnosticar(ruta, fuente)
        resultados.append(resultado)

    reporte = pd.DataFrame(resultados)

    REPORTE.parent.mkdir(parents=True, exist_ok=True)

    reporte.to_csv(
        REPORTE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDIAGNÓSTICO DE CALIDAD")
    print(reporte.to_string(index=False))

    print(f"\nReporte guardado en: {REPORTE}")


if __name__ == "__main__":
    main()
