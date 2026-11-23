"""Graficas comparativas de los disenos factoriales 2^4."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RAIZ = Path(__file__).resolve().parent.parent

ENTRADA = RAIZ / "data/reportes/comparacion_factorial_2_4.csv"
SALIDA = RAIZ / "data/reportes/graficas_comparacion_2_4"


def guardar(nombre):
    plt.tight_layout()
    plt.savefig(SALIDA / nombre, dpi=200, bbox_inches="tight")
    plt.close()
    print("Generada:", nombre)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)

    datos = pd.read_csv(ENTRADA)

    # 1. Comparacion de efectos principales
    factores = datos[
        datos["efecto"].isin(["A", "B", "C", "D"])
    ]

    completos = factores[
        factores["diseno"] == "Completo 2^4"
    ].set_index("efecto")

    fraccionados = factores[
        factores["diseno"] == "Fraccionado 2^4-1"
    ].set_index("efecto")

    nombres = ["A", "B", "C", "D"]
    x = np.arange(len(nombres))
    ancho = 0.35

    plt.figure(figsize=(9, 5))

    plt.bar(
        x - ancho / 2,
        completos.loc[nombres, "efecto_ms"],
        ancho,
        label="Completo 2^4",
    )

    plt.bar(
        x + ancho / 2,
        fraccionados.loc[nombres, "efecto_ms"],
        ancho,
        label="Fraccionado 2^4-1",
    )

    plt.axhline(0, linestyle="--")
    plt.xticks(x, nombres)
    plt.ylabel("Efecto estimado (ms)")
    plt.title("Comparacion de efectos principales")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    guardar("01_efectos_principales.png")

    # 2. Comparacion de significancia estadistica
    plt.figure(figsize=(11, 7))

    posiciones = np.arange(len(datos))

    valores_p = datos["valor_p"].clip(lower=1e-12)

    plt.barh(
        posiciones,
        -np.log10(valores_p),
    )

    plt.axvline(
        -np.log10(0.05),
        linestyle="--",
        label="Umbral p = 0.05",
    )

    etiquetas = [
        f"{fila.diseno} | {fila.alias}"
        for fila in datos.itertuples()
    ]

    plt.yticks(posiciones, etiquetas)
    plt.xlabel("-log10(valor p)")
    plt.title("Significancia estadistica de los efectos")
    plt.legend()
    plt.grid(axis="x", alpha=0.3)
    plt.gca().invert_yaxis()

    guardar("02_significancia_estadistica.png")

    # 3. Comparacion del numero de corridas
    nombres_disenos = [
        "Completo 2^4",
        "Fraccionado 2^4-1",
    ]

    corridas = [32, 16]

    plt.figure(figsize=(8, 5))

    barras = plt.bar(nombres_disenos, corridas)

    plt.bar_label(barras, padding=3)
    plt.ylabel("Numero de corridas")
    plt.title("Reduccion del esfuerzo experimental")
    plt.grid(axis="y", alpha=0.3)

    guardar("03_numero_corridas.png")

    print("\nTotal: 3 graficas.")
    print("Carpeta:", SALIDA)


if __name__ == "__main__":
    main()
