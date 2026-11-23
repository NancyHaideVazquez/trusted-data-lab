"""Graficas del experimento factorial 2^3 de E2."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "data/reportes/experimento_factorial_e2_confirmacion.csv"
SALIDA = RAIZ / "data/reportes/graficas_e2_monico"

NOMBRES = {
    "A": "Cantidad de registros",
    "B": "Trazabilidad",
    "C": "Validacion Pandera",
}


def guardar(nombre):
    plt.tight_layout()
    plt.savefig(SALIDA / nombre, dpi=200, bbox_inches="tight")
    plt.close()
    print("Generada:", nombre)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)

    datos = pd.read_csv(ENTRADA)
    modelo = smf.ols("tiempo_ms ~ A * B * C", data=datos).fit()

    # 1. Efectos principales
    fig, ejes = plt.subplots(1, 3, figsize=(13, 4))

    for eje, factor in zip(ejes, ("A", "B", "C")):
        medias = datos.groupby(factor)["tiempo_ms"].mean()
        eje.plot([-1, 1], medias.loc[[-1, 1]], marker="o")
        eje.set_title(NOMBRES[factor])
        eje.set_xticks([-1, 1])
        eje.set_xticklabels(["Nivel bajo", "Nivel alto"])
        eje.set_ylabel("Tiempo promedio (ms)")
        eje.grid(alpha=0.3)

    fig.suptitle("Experimento factorial 2^3 - Efectos principales")
    guardar("01_efectos_principales.png")

    # 2. Interacciones
    pares = [("A", "B"), ("A", "C"), ("B", "C")]
    fig, ejes = plt.subplots(1, 3, figsize=(14, 4))

    for eje, (factor_x, factor_linea) in zip(ejes, pares):
        for nivel in (-1, 1):
            subconjunto = datos[datos[factor_linea] == nivel]
            medias = subconjunto.groupby(factor_x)["tiempo_ms"].mean()

            eje.plot(
                [-1, 1],
                medias.loc[[-1, 1]],
                marker="o",
                label=f"{factor_linea}={nivel:+d}",
            )

        eje.set_title(f"Interaccion {factor_x} x {factor_linea}")
        eje.set_xticks([-1, 1])
        eje.set_xlabel(NOMBRES[factor_x])
        eje.set_ylabel("Tiempo promedio (ms)")
        eje.legend()
        eje.grid(alpha=0.3)

    fig.suptitle("Experimento factorial 2^3 - Interacciones")
    guardar("02_interacciones.png")

    # 3. Residuos frente a valores ajustados
    plt.figure(figsize=(8, 5))
    plt.scatter(modelo.fittedvalues, modelo.resid)
    plt.axhline(0, linestyle="--")
    plt.xlabel("Tiempo ajustado (ms)")
    plt.ylabel("Residuo (ms)")
    plt.title("Diagnostico: residuos frente a valores ajustados")
    plt.grid(alpha=0.3)
    guardar("03_residuos.png")

    # 4. Grafica normal Q-Q
    sm.qqplot(modelo.resid, line="45", fit=True)
    plt.title("Grafica normal Q-Q de los residuos")
    guardar("04_qqplot.png")

    print("\nTotal: 4 graficas.")
    print("Carpeta:", SALIDA)


if __name__ == "__main__":
    main()
