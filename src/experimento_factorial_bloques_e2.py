
"""Experimento factorial 2^3 con bloques completos aleatorizados."""

import argparse
import itertools
import random
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter_ns

import pandas as pd

from src.calidad import validar_calidad
from src.experimento_factorial_e2 import preparar_muestra
from src.integracion import integrar_datos

RAIZ = Path(__file__).resolve().parent.parent
REPORTES = RAIZ / "data/reportes"
SEMILLA = 2026


def ejecutar_tratamiento(muestras, a, b, c):
    total = 200 if a == -1 else 500
    inegi, banxico = muestras[total]

    inicio = perf_counter_ns()

    integrado = integrar_datos(
        inegi,
        banxico,
        incluir_trazabilidad=(b == 1),
    )

    if c == 1:
        integrado = validar_calidad(integrado)

    fin = perf_counter_ns()

    if len(integrado) != total:
        raise RuntimeError("Cantidad de registros incorrecta.")

    return (fin - inicio) / 1_000_000, len(integrado)


def ejecutar_bloque(bloque):
    salida = REPORTES / f"factorial_2_3_bloque_{bloque}.csv"

    if salida.exists():
        raise FileExistsError(
            f"El bloque {bloque} ya fue ejecutado: {salida}"
        )

    inegi = pd.read_csv(
        REPORTES / "limpieza_preliminar_inegi.csv",
        dtype={"serie_id": str},
    )

    banxico = pd.read_csv(
        REPORTES / "reduccion_banxico.csv",
        dtype={"serie_id": str},
    )

    muestras = {
        total: preparar_muestra(inegi, banxico, total)
        for total in (200, 500)
    }

    tratamientos = list(
        itertools.product((-1, 1), repeat=3)
    )

    print(f"\n===== BLOQUE {bloque} =====")
    print("Calentamiento de ocho tratamientos...")

    for a, b, c in tratamientos:
        ejecutar_tratamiento(muestras, a, b, c)

    random.Random(SEMILLA + bloque).shuffle(tratamientos)

    resultados = []

    for orden, (a, b, c) in enumerate(
        tratamientos, start=1
    ):
        fecha = datetime.now(UTC).isoformat()

        tiempo, registros = ejecutar_tratamiento(
            muestras, a, b, c
        )

        resultados.append({
            "bloque": bloque,
            "orden": orden,
            "fecha_utc": fecha,
            "A": a,
            "B": b,
            "C": c,
            "registros": 200 if a == -1 else 500,
            "trazabilidad": b == 1,
            "pandera": c == 1,
            "tiempo_ms": tiempo,
            "registros_salida": registros,
        })

        print(
            f"Bloque {bloque} | "
            f"Corrida {orden}/8 | "
            f"A={a:+d} B={b:+d} C={c:+d} | "
            f"{tiempo:.4f} ms"
        )

    REPORTES.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(resultados).to_csv(
        salida,
        index=False,
    )

    print(f"\nBloque {bloque} completado.")
    print("Corridas:", len(resultados))
    print("Archivo:", salida)


def main():
    parser = argparse.ArgumentParser(
        description="Factorial 2^3 con bloques"
    )

    parser.add_argument(
        "--bloque",
        type=int,
        choices=[1, 2],
        required=True,
    )

    args = parser.parse_args()
    ejecutar_bloque(args.bloque)


if __name__ == "__main__":
    main()
