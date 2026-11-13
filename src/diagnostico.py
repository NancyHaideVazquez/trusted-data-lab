
"""T03 - Diagnóstico de calidad de datos."""

from pathlib import Path
import pandas as pd

from src.lectura import cargar_dataframe, convertir_fecha

RAIZ = Path(__file__).resolve().parents[1]
BRONCE = RAIZ / "data" / "bronce"
REPORTES = RAIZ / "data" / "reportes"


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


def diagnosticar(ruta, fuente, guardar_reporte=True):
    """Analiza los datos sin modificar Bronce."""

    df = cargar_dataframe(ruta)

    if fuente == "inegi":
        columna_fecha = "TIME_PERIOD"
        columna_valor = "OBS_VALUE"
    else:
        columna_fecha = "fecha"
        columna_valor = "dato"


    # Comprobar el esquema antes de acceder a las columnas
    columnas_obligatorias = [
        columna_fecha,
        columna_valor
    ]

    faltantes_esquema = [
        columna
        for columna in columnas_obligatorias
        if columna not in df.columns
    ]

    if faltantes_esquema:
        raise ValueError(
            f"{fuente}: faltan columnas obligatorias: "
            f"{faltantes_esquema}"
        )

    valores = df[columna_valor].astype("string").str.strip()

    faltantes = valores.isna() | valores.isin(
        ["", "N/E", "N/D", "-"]
    )

    numeros = pd.to_numeric(
        valores.mask(faltantes),
        errors="coerce"
    )

    fechas = convertir_fecha(df[columna_fecha])

    duplicados_fecha = fechas[fechas.notna()].duplicated().sum()
    fechas_invalidas = fechas.isna().sum()
    valores_invalidos = (numeros.isna() & ~faltantes).sum()

    # Detectar filas completamente duplicadas.
    duplicados_exactos = df.duplicated().sum()

    # En cada archivo se analiza una sola serie.
    # Por ello, la fecha funciona como llave de la serie.
    duplicados_llave = fechas[fechas.notna()].duplicated().sum()

    # Crear un reporte detallado por columna.
    detalle = []

    for columna in df.columns:

        datos = df[columna].astype("string").str.strip()

        nulos = datos.isna() | datos.isin(
            ["", "N/E", "N/D", "-"]
        )

        cantidad_nulos = int(nulos.sum())
        total = len(df)

        if total > 0:
            completitud = (total - cantidad_nulos) / total * 100
        else:
            completitud = 0

        unicos = datos[~nulos].nunique()
        constante = unicos <= 1

        # Estadísticos numéricos solo para la columna de valor.
        minimo = None
        maximo = None
        promedio = None
        mediana = None
        q1 = None
        q3 = None
        desviacion = None

        if columna == columna_valor:
            minimo = numeros.min()
            maximo = numeros.max()
            promedio = numeros.mean()
            mediana = numeros.median()
            q1 = numeros.quantile(0.25)
            q3 = numeros.quantile(0.75)
            desviacion = numeros.std()

        detalle.append({
            "fuente": fuente,
            "columna": columna,
            "tipo": str(df[columna].dtype),
            "registros": total,
            "nulos": cantidad_nulos,
            "completitud_porcentaje": round(completitud, 2),
            "valores_unicos": int(unicos),
            "es_constante": bool(constante),
            "minimo": minimo,
            "maximo": maximo,
            "promedio": promedio,
            "mediana": mediana,
            "q1": q1,
            "q3": q3,
            "desviacion_estandar": desviacion
        })

    detalle_df = pd.DataFrame(detalle)

    
    if guardar_reporte:
        REPORTES.mkdir(parents=True, exist_ok=True)

        ruta_detalle = REPORTES / f"diagnostico_{fuente}.csv"

        detalle_df.to_csv(
            ruta_detalle,
            index=False,
            encoding="utf-8-sig"
        )

    # Mantener el reporte general de T03.
    return {
        "fuente": fuente,
        "archivo": str(ruta),
        "registros": len(df),
        "faltantes": int(faltantes.sum()),
        "completitud_porcentaje": round(
            (1 - faltantes.sum() / len(df)) * 100, 2
        ) if len(df) > 0 else 0,
        "duplicados_fecha": int(duplicados_fecha),
        "duplicados_exactos": int(duplicados_exactos),
        "duplicados_llave": int(duplicados_llave),
        "fechas_invalidas": int(fechas_invalidas),
        "valores_invalidos": int(valores_invalidos),
        "minimo": numeros.min(),
        "maximo": numeros.max(),
        "promedio": numeros.mean(),
        "mediana": numeros.median(),
        "q1": numeros.quantile(0.25),
        "q3": numeros.quantile(0.75),
        "desviacion_estandar": numeros.std()
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

        print(f"Reporte por columna generado: diagnostico_{fuente}.csv")

    reporte = pd.DataFrame(resultados)

    REPORTES.mkdir(parents=True, exist_ok=True)

    ruta_general = REPORTES / "diagnostico_calidad.csv"

    reporte.to_csv(
        ruta_general,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDIAGNÓSTICO DE CALIDAD")
    print(reporte.to_string(index=False))

    print(f"\nReporte general guardado en: {ruta_general}")


if __name__ == "__main__":
    main()
