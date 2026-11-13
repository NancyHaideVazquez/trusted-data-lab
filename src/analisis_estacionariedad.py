
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller


# Rutas relativas a la raiz del repositorio
RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO_ORO = RAIZ / "data" / "oro" / "indicadores_mensuales.csv"
CARPETA_SALIDA = RAIZ / "docs" / "E1" / "estadistica"


def analizar_serie(nombre, fuente, titulo, datos):
    """Calcula ADF, ACF y PACF para una serie mensual."""

    grupo = datos.loc[datos["fuente"] == fuente].copy()
    grupo = grupo.sort_values("fecha")

    # Noviembre de 2026 aun no es un mes cerrado.
    # No se modifica el CSV original.
    if fuente == "banxico":
        grupo = grupo.loc[grupo["periodo"] < "2026-11"]

    serie = pd.Series(
        grupo["valor"].to_numpy(dtype=float),
        index=pd.DatetimeIndex(grupo["fecha"]),
        name=titulo,
    ).asfreq("MS")

    if serie.empty:
        raise ValueError(f"{nombre}: serie vacia")

    if serie.isna().any():
        raise ValueError(f"{nombre}: existen meses faltantes")

    if serie.index.has_duplicates:
        raise ValueError(f"{nombre}: existen meses duplicados")

    # Prueba Dickey-Fuller aumentada (ADF)
    adf_original = adfuller(
        serie, autolag="AIC", result_object=False
    )

    # Primera diferencia para evaluar estacionariedad
    diferencia = serie.diff().dropna()
    adf_diferencia = adfuller(
        diferencia, autolag="AIC", result_object=False
    )

    print(f"\n=== {nombre.upper()} ===")
    print(f"Observaciones: {len(serie)}")
    print(f"Inicio: {serie.index.min():%Y-%m}")
    print(f"Fin: {serie.index.max():%Y-%m}")

    resultados = [
        ("Serie original", adf_original),
        ("Primera diferencia", adf_diferencia),
    ]

    lineas = [
        f"Serie: {nombre}",
        f"Indicador: {titulo}",
        f"Observaciones: {len(serie)}",
        f"Periodo: {serie.index.min():%Y-%m} a {serie.index.max():%Y-%m}",
        "",
        "ADF: H0 = la serie tiene raiz unitaria.",
        "Criterio de decision: alfa = 0.05",
        "",
    ]

    for etiqueta, resultado in resultados:
        estadistico, p_valor, rezagos, observaciones = resultado[:4]

        conclusion = (
            "Se rechaza H0: evidencia de estacionariedad"
            if p_valor < 0.05
            else "No se rechaza H0: estacionariedad no demostrada"
        )

        print(f"\n{etiqueta}")
        print(f"  Estadistico ADF: {estadistico:.6f}")
        print(f"  p-valor: {p_valor:.6g}")
        print(f"  Rezagos: {rezagos}")
        print(f"  Observaciones: {observaciones}")
        print(f"  Interpretacion: {conclusion}")

        lineas.extend([
            etiqueta,
            f"Estadistico ADF: {estadistico:.6f}",
            f"p-valor: {p_valor:.6g}",
            f"Rezagos: {rezagos}",
            f"Observaciones: {observaciones}",
            f"Interpretacion: {conclusion}",
            "",
        ])

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

    ruta_txt = CARPETA_SALIDA / f"{nombre}_adf.txt"
    ruta_txt.write_text("\n".join(lineas), encoding="utf-8")

    # Gráficas ACF y PACF de ambas versiones
    versiones = [
        ("original", serie),
        ("diff1", diferencia),
    ]

    for sufijo, valores in versiones:
        # Número de rezagos apropiado para la longitud de la serie
        rezagos = min(36, len(valores) // 2 - 1)

        if rezagos < 1:
            raise ValueError(
                f"{nombre}: observaciones insuficientes para ACF/PACF"
            )

        fig, ax = plt.subplots(figsize=(11, 4))
        plot_acf(valores, lags=rezagos, ax=ax)
        ax.set_title(f"{titulo} - ACF ({sufijo})")
        ax.grid(alpha=0.25)
        fig.tight_layout()

        ruta_acf = CARPETA_SALIDA / f"{nombre}_acf_{sufijo}.png"
        fig.savefig(ruta_acf, dpi=160)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11, 4))
        plot_pacf(valores, lags=rezagos, method="ywm", ax=ax)
        ax.set_title(f"{titulo} - PACF ({sufijo})")
        ax.grid(alpha=0.25)
        fig.tight_layout()

        ruta_pacf = CARPETA_SALIDA / f"{nombre}_pacf_{sufijo}.png"
        fig.savefig(ruta_pacf, dpi=160)
        plt.close(fig)

    print(f"\nResultados guardados en: {CARPETA_SALIDA}")


def main():
    if not ARCHIVO_ORO.is_file():
        raise FileNotFoundError(
            f"No se encontro la capa Oro: {ARCHIVO_ORO}"
        )

    datos = pd.read_csv(ARCHIVO_ORO)
    datos["fecha"] = pd.to_datetime(
        datos["periodo"] + "-01",
        errors="raise",
    )

    series = [
        ("banxico_tiie", "banxico", "TIIE a 28 dias"),
        ("inegi_inflacion", "inegi", "Inflacion mensual"),
    ]

    for nombre, fuente, titulo in series:
        analizar_serie(nombre, fuente, titulo, datos)

    print("\nAnalisis ADF, ACF y PACF terminado correctamente.")


if __name__ == "__main__":
    main()
