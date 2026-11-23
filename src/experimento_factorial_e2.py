"""Experimento factorial 2^3 de rendimiento del flujo de integración E2."""

import itertools
import random
from pathlib import Path
from time import perf_counter_ns

import pandas as pd

from src.calidad import validar_calidad
from src.integracion import integrar_datos

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data/reportes/experimento_factorial_e2_confirmacion.csv"
SEMILLA = 2026


def preparar_muestra(inegi, banxico, total):
    """Construye una muestra proporcional de ambas fuentes."""
    n_inegi = round(total * len(inegi) / (len(inegi) + len(banxico)))
    n_banxico = total - n_inegi

    muestra_inegi = inegi.sample(
        n=n_inegi,
        random_state=SEMILLA,
    ).copy()

    muestra_banxico = banxico.sample(
        n=n_banxico,
        random_state=SEMILLA,
    ).copy()

    return muestra_inegi, muestra_banxico


def ejecutar_experimento():
    inegi = pd.read_csv(
        RAIZ / "data/reportes/limpieza_preliminar_inegi.csv",
        dtype={"serie_id": str},
    )
    banxico = pd.read_csv(
        RAIZ / "data/reportes/reduccion_banxico.csv",
        dtype={"serie_id": str},
    )

    muestras = {
        total: preparar_muestra(inegi, banxico, total)
        for total in (200, 500)
    }

    tratamientos = list(itertools.product((-1, 1), repeat=3))
    corridas = [
        (replica, a, b, c)
        for replica in (1, 2)
        for a, b, c in tratamientos
    ]

    # Calentamiento: ejecutar las 8 combinaciones sin medirlas.
    for a, b, c in tratamientos:
        total = 200 if a == -1 else 500
        muestra_inegi, muestra_banxico = muestras[total]

        integrado = integrar_datos(
            muestra_inegi,
            muestra_banxico,
            incluir_trazabilidad=(b == 1),
        )

        if c == 1:
            validar_calidad(integrado)

    print("Calentamiento completado: 8 combinaciones.")

    random.Random(SEMILLA).shuffle(corridas)

    resultados = []

    for orden, (replica, a, b, c) in enumerate(corridas, start=1):
        total = 200 if a == -1 else 500
        trazabilidad = b == 1
        usar_pandera = c == 1

        muestra_inegi, muestra_banxico = muestras[total]

        inicio = perf_counter_ns()

        integrado = integrar_datos(
            muestra_inegi,
            muestra_banxico,
            incluir_trazabilidad=trazabilidad,
        )

        if usar_pandera:
            integrado = validar_calidad(integrado)

        fin = perf_counter_ns()

        if len(integrado) != total:
            raise RuntimeError(
                f"Corrida {orden}: se esperaban {total} registros."
            )

        tiempo_ms = (fin - inicio) / 1_000_000

        resultados.append({
            "orden": orden,
            "replica": replica,
            "A": a,
            "B": b,
            "C": c,
            "registros": total,
            "trazabilidad": trazabilidad,
            "pandera": usar_pandera,
            "tiempo_ms": tiempo_ms,
            "registros_salida": len(integrado),
        })

        print(
            f"Corrida {orden:02d}/16 | "
            f"Replica {replica} | "
            f"A={a:+d} B={b:+d} C={c:+d} | "
            f"{tiempo_ms:.3f} ms"
        )

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(resultados).to_csv(SALIDA, index=False)

    print("\nExperimento completado.")
    print("Corridas:", len(resultados))
    print("Resultados:", SALIDA)


if __name__ == "__main__":
    ejecutar_experimento()
