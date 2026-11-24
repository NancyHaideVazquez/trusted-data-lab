
"""Experimento ANOVA 3x2 de procesos y formatos de almacenamiento."""

import itertools
import random
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from time import perf_counter_ns

import pandas as pd

from src.integracion import integrar_datos

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data/reportes/experimento_anova_3_2.csv"
SEMILLA = 2026


def procesar_particion(tarea):
    datos, ruta, formato = tarea

    if formato == "CSV":
        datos.to_csv(ruta, index=False)
        return pd.read_csv(ruta, dtype=str, keep_default_na=False)

    datos.to_parquet(ruta, index=False)
    return pd.read_parquet(ruta)


def ejecutar_corrida(datos, procesos, formato):
    with tempfile.TemporaryDirectory() as temporal:
        tareas = []

        for i in range(procesos):
            particion = datos.iloc[i::procesos].copy()
            extension = formato.lower()
            ruta = Path(temporal) / f"parte_{i}.{extension}"
            tareas.append((particion, ruta, formato))

        inicio = perf_counter_ns()

        with ProcessPoolExecutor(max_workers=procesos) as executor:
            partes = list(executor.map(procesar_particion, tareas))

        resultado = pd.concat(partes, ignore_index=True)

        fin = perf_counter_ns()

        columnas_orden = ["periodo", "fuente", "serie_id"]

        resultado = resultado.sort_values(
            columnas_orden
        ).reset_index(drop=True)

        esperado = datos.sort_values(
            columnas_orden
        ).reset_index(drop=True)

        pd.testing.assert_frame_equal(resultado, esperado)

        tamano = sum(
            archivo.stat().st_size
            for archivo in Path(temporal).iterdir()
        )

        return {
            "tiempo_ms": (fin - inicio) / 1_000_000,
            "registros_salida": len(resultado),
            "tamano_bytes": tamano,
            "salida_equivalente": True,
        }


def ejecutar_experimento():
    inegi = pd.read_csv(
        RAIZ / "data/reportes/limpieza_preliminar_inegi.csv",
        dtype={"serie_id": str},
    )

    banxico = pd.read_csv(
        RAIZ / "data/reportes/reduccion_banxico.csv",
        dtype={"serie_id": str},
    )

    datos = integrar_datos(
        inegi,
        banxico,
        incluir_trazabilidad=True,
    ).astype(str)

    tratamientos = list(
        itertools.product(
            (1, 2, 4),
            ("CSV", "Parquet"),
        )
    )

    print("Registros de entrada:", len(datos))
    print("Calentamiento de los seis tratamientos...")

    for procesos, formato in tratamientos:
        ejecutar_corrida(datos, procesos, formato)

    corridas = [
        (replica, procesos, formato)
        for replica in (1, 2)
        for procesos, formato in tratamientos
    ]

    random.Random(SEMILLA).shuffle(corridas)

    resultados = []

    for orden, (replica, procesos, formato) in enumerate(
        corridas, start=1
    ):
        medicion = ejecutar_corrida(
            datos,
            procesos,
            formato,
        )

        resultados.append({
            "orden": orden,
            "replica": replica,
            "procesos": procesos,
            "formato": formato,
            **medicion,
        })

        print(
            f"Corrida {orden:02d}/12 | "
            f"Replica {replica} | "
            f"Procesos: {procesos} | "
            f"Formato: {formato} | "
            f"{medicion['tiempo_ms']:.3f} ms"
        )

    SALIDA.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(resultados).to_csv(
        SALIDA,
        index=False,
    )

    print("\nExperimento completado.")
    print("Corridas:", len(resultados))
    print("Resultados:", SALIDA)


if __name__ == "__main__":
    ejecutar_experimento()
