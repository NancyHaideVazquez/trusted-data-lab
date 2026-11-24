
"""Confirmacion experimental X05 de rendimiento en Trusted Data Lab."""

import hashlib
import random
import tempfile
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter_ns

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t, ttest_rel

from src.experimento_anova_3_2_e2 import procesar_particion
from src.integracion import integrar_datos

RAIZ = Path(__file__).resolve().parent.parent
REPORTES = RAIZ / "data/reportes"
FIGURAS = RAIZ / "reportes/figuras/confirmacion_x05"

SEMILLA = 2027
REPLICAS = 10
COLUMNAS_ORDEN = ["periodo", "fuente", "serie_id"]

CONFIGURACIONES = {
    "baseline": 1,
    "candidata": 2,
}


def normalizar(datos):
    return datos.sort_values(
        COLUMNAS_ORDEN
    ).reset_index(drop=True)


def calcular_checksum(datos):
    contenido = normalizar(datos).to_csv(
        index=False,
        lineterminator="\n",
    ).encode("utf-8")

    return hashlib.sha256(contenido).hexdigest()


def ejecutar_corrida(datos, procesos):
    with tempfile.TemporaryDirectory() as temporal:
        tareas = []

        for i in range(procesos):
            particion = datos.iloc[i::procesos].copy()

            ruta = Path(temporal) / f"parte_{i}.csv"

            tareas.append((particion, ruta, "CSV"))

        inicio = perf_counter_ns()

        with ProcessPoolExecutor(
            max_workers=procesos
        ) as executor:
            partes = list(
                executor.map(procesar_particion, tareas)
            )

        resultado = pd.concat(partes, ignore_index=True)

        fin = perf_counter_ns()

        resultado = normalizar(resultado)
        esperado = normalizar(datos)

        pd.testing.assert_frame_equal(resultado, esperado)

        checksum = calcular_checksum(resultado)

        if checksum != calcular_checksum(esperado):
            raise ValueError("Checksum incorrecto.")

        tamano = sum(
            archivo.stat().st_size
            for archivo in Path(temporal).iterdir()
        )

        return {
            "tiempo_ms": (fin - inicio) / 1_000_000,
            "registros_salida": len(resultado),
            "tamano_bytes": tamano,
            "checksum_sha256": checksum,
            "salida_equivalente": True,
            "errores": 0,
            "detalle_error": "",
        }


def analizar_resultados(resultados):
    datos = pd.DataFrame(resultados)

    if datos["errores"].sum() != 0:
        print("Se detectaron errores experimentales.")
        print("Consultar el reporte de corridas.")
        return

    resumen = (
        datos.groupby("configuracion")["tiempo_ms"]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
    )

    resumen.to_csv(
        REPORTES / "resumen_confirmacion_x05.csv",
        index=False,
    )

    pares = datos.pivot(
        index="replica",
        columns="configuracion",
        values="tiempo_ms",
    )

    baseline = pares["baseline"]
    candidata = pares["candidata"]

    diferencias = baseline - candidata

    promedio_base = baseline.mean()
    promedio_candidata = candidata.mean()

    mejora = (
        (promedio_base - promedio_candidata)
        / promedio_base
    ) * 100

    diferencia_media = diferencias.mean()

    error_estandar = diferencias.sem()

    valor_critico = t.ppf(
        0.975,
        df=len(diferencias) - 1,
    )

    margen = valor_critico * error_estandar

    limite_inferior = diferencia_media - margen
    limite_superior = diferencia_media + margen

    estadistico, valor_p = ttest_rel(
        baseline,
        candidata,
    )

    if valor_p < 0.05 and diferencia_media > 0:
        conclusion = "Mejora estadisticamente significativa"
    elif valor_p < 0.05 and diferencia_media < 0:
        conclusion = "Empeoramiento estadisticamente significativo"
    else:
        conclusion = "No se confirma una diferencia significativa"

    comparacion = pd.DataFrame([{
        "replicas_por_configuracion": REPLICAS,
        "promedio_baseline_ms": promedio_base,
        "promedio_candidata_ms": promedio_candidata,
        "diferencia_media_ms": diferencia_media,
        "mejora_porcentaje": mejora,
        "ic95_inferior_ms": limite_inferior,
        "ic95_superior_ms": limite_superior,
        "estadistico_t": estadistico,
        "valor_p": valor_p,
        "errores_totales": datos["errores"].sum(),
        "checksums_distintos": datos["checksum_sha256"].nunique(),
        "conclusion": conclusion,
    }])

    comparacion.to_csv(
        REPORTES / "comparacion_confirmacion_x05.csv",
        index=False,
    )

    FIGURAS.mkdir(parents=True, exist_ok=True)

    # Grafica de tiempos promedio.
    plt.figure(figsize=(8, 5))

    plt.bar(
        ["1 proceso + CSV", "2 procesos + CSV"],
        [promedio_base, promedio_candidata],
        yerr=[baseline.std(), candidata.std()],
        capsize=6,
    )

    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Confirmacion experimental X05")
    plt.tight_layout()

    plt.savefig(
        FIGURAS / "01_comparacion_promedios.png",
        dpi=200,
    )

    plt.close()

    # Comparacion de replicas pareadas.
    plt.figure(figsize=(9, 5))

    plt.plot(
        pares.index,
        baseline,
        marker="o",
        label="Baseline: 1 proceso",
    )

    plt.plot(
        pares.index,
        candidata,
        marker="s",
        label="Candidata: 2 procesos",
    )

    plt.xlabel("Replica")
    plt.ylabel("Tiempo (ms)")
    plt.title("Comparacion por replica")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        FIGURAS / "02_comparacion_replicas.png",
        dpi=200,
    )

    plt.close()

    # Diferencias por replica.
    plt.figure(figsize=(9, 5))

    plt.bar(pares.index, diferencias)
    plt.axhline(0, linestyle="--")

    plt.xlabel("Replica")
    plt.ylabel("Baseline - candidata (ms)")
    plt.title("Diferencias pareadas de rendimiento")
    plt.tight_layout()

    plt.savefig(
        FIGURAS / "03_diferencias_pareadas.png",
        dpi=200,
    )

    plt.close()

    print("\n===== RESUMEN POR CONFIGURACION =====")
    print(resumen.to_string(index=False))

    print("\n===== CONFIRMACION EXPERIMENTAL X05 =====")
    print(comparacion.T.to_string(header=False))


def ejecutar_experimento():
    REPORTES.mkdir(parents=True, exist_ok=True)

    salida = REPORTES / "experimento_confirmacion_x05.csv"

    if salida.exists():
        raise FileExistsError(
            f"El experimento ya existe: {salida}"
        )

    inegi = pd.read_csv(
        REPORTES / "limpieza_preliminar_inegi.csv",
        dtype={"serie_id": str},
    )

    banxico = pd.read_csv(
        REPORTES / "reduccion_banxico.csv",
        dtype={"serie_id": str},
    )

    datos = integrar_datos(
        inegi,
        banxico,
        incluir_trazabilidad=True,
    ).astype(str)

    checksum_entrada = calcular_checksum(datos)

    print("===== EXPERIMENTO X05 =====")
    print("Registros:", len(datos))
    print("Checksum esperado:", checksum_entrada)
    print("Calentamiento de ambas configuraciones...")

    for procesos in CONFIGURACIONES.values():
        ejecutar_corrida(datos, procesos)

    generador = random.Random(SEMILLA)

    resultados = []
    orden = 0

    for replica in range(1, REPLICAS + 1):
        configuraciones = list(CONFIGURACIONES.items())

        generador.shuffle(configuraciones)

        for configuracion, procesos in configuraciones:
            orden += 1
            fecha = datetime.now(UTC).isoformat()

            try:
                medicion = ejecutar_corrida(
                    datos,
                    procesos,
                )

            except Exception as error:  # noqa: BLE001
                medicion = {
                    "tiempo_ms": None,
                    "registros_salida": None,
                    "tamano_bytes": None,
                    "checksum_sha256": "",
                    "salida_equivalente": False,
                    "errores": 1,
                    "detalle_error": str(error),
                }

            resultados.append({
                "orden": orden,
                "replica": replica,
                "fecha_utc": fecha,
                "configuracion": configuracion,
                "procesos": procesos,
                "formato": "CSV",
                "registros_entrada": len(datos),
                "checksum_entrada": checksum_entrada,
                **medicion,
            })

            print(
                f"Corrida {orden:02d}/20 | "
                f"Replica {replica:02d} | "
                f"{configuracion} | "
                f"Tiempo: {medicion['tiempo_ms']} ms | "
                f"Errores: {medicion['errores']}"
            )

    pd.DataFrame(resultados).to_csv(
        salida,
        index=False,
    )

    analizar_resultados(resultados)

    print("\n===== EXPERIMENTO COMPLETADO =====")
    print("Corridas:", len(resultados))
    print("Resultados:", salida)


if __name__ == "__main__":
    ejecutar_experimento()
