
"""
TRUSTED DATA LAB - extractores/main.py

Orquestador principal.

Ejecuta los extractores de INEGI y Banxico,
guarda la informacion en Bronce y registra
las ejecuciones en logs/capturas.csv.

Uso:
    python -m extractores.main
    python -m extractores.main --historico
"""

import argparse
import time

from .base import guardar_bronce, registrar_ejecucion
from . import banxico, inegi


# -----------------------------------------
# CAPTURA DE BANXICO
# -----------------------------------------

def ejecutar_banxico(modo="oportuno"):

    print(
        f"\n--- Iniciando captura Banxico "
        f"(Modo: {modo}) ---"
    )

    inicio = time.time()

    serie_id = "SF43783"

    try:

        paquete, resumen = banxico.capturar(
            serie_id,
            modo=modo
        )

        ruta = guardar_bronce(
            fuente="banxico",
            nombre=f"{serie_id}_{modo}",
            metadatos=paquete["metadata"],
            datos=paquete["data"]
        )

        duracion = time.time() - inicio

        registrar_ejecucion(
            "banxico",
            serie_id,
            True,
            duracion,
            f"Guardado en {ruta.name}"
        )

        print(
            f"Banxico OK: {resumen['registros']} registros. "
            f"Ultima fecha: {resumen['ultima_fecha']}"
        )

        return True

    except Exception as e:

        duracion = time.time() - inicio

        registrar_ejecucion(
            "banxico",
            serie_id,
            False,
            duracion,
            str(e)
        )

        print(f"Error en Banxico: {e}")

        return False


# -----------------------------------------
# CAPTURA DE INEGI
# -----------------------------------------

def ejecutar_inegi(modo="oportuno"):

    print(
        f"\n--- Iniciando captura INEGI "
        f"(Modo: {modo}) ---"
    )

    inicio = time.time()

    # Indicador economico seleccionado
    indicador_id = "910402"

    # Banco de indicadores economicos
    banco = "BIE-BISE"

    try:

        paquete, resumen = inegi.capturar(

            indicador_id=indicador_id,

            modo=modo,

            ubicacion="00",

            banco=banco,

            revisar_robots=False

        )

        # Guardar informacion en Bronce
        ruta = guardar_bronce(

            fuente="inegi",

            nombre=f"{indicador_id}_{modo}",

            metadatos=paquete["metadata"],

            datos=paquete["data"]

        )

        duracion = time.time() - inicio

        registrar_ejecucion(

            "inegi",

            indicador_id,

            True,

            duracion,

            f"Guardado en {ruta.name}"

        )

        print(
            f"INEGI OK: {resumen['registros']} registros. "
            f"Ultima fecha: {resumen['ultima_fecha']}"
        )

        print(f"Banco utilizado: {banco}")

        return True

    except Exception as e:

        duracion = time.time() - inicio

        registrar_ejecucion(

            "inegi",

            indicador_id,

            False,

            duracion,

            str(e)

        )

        print(f"Error en INEGI: {e}")

        return False


# -----------------------------------------
# ORQUESTADOR PRINCIPAL
# -----------------------------------------

def main():

    parser = argparse.ArgumentParser(

        description="Trusted Data Lab - Orquestador"

    )

    parser.add_argument(

        "--historico",

        action="store_true",

        help="Descargar historia completa"

    )

    args = parser.parse_args()

    modo = (
        "historico"
        if args.historico
        else "oportuno"
    )

    print("========================================")

    print(
        f" INICIANDO CAPTURA TDL - "
        f"MODO: {modo.upper()}"
    )

    print("========================================")

    # Ejecutamos las dos fuentes
    resultado_inegi = ejecutar_inegi(
        modo=modo
    )

    resultado_banxico = ejecutar_banxico(
        modo=modo
    )

    print("\n========================================")

    print(" CAPTURA FINALIZADA")

    print(" Revisa data/bronce/ y logs/capturas.csv")

    print("========================================")

    if not resultado_inegi or not resultado_banxico:

        print(
            "Una o mas fuentes presentaron errores"
        )

        return 1

    print(
        "Ambas fuentes se ejecutaron correctamente"
    )

    return 0


if __name__ == "__main__":

    raise SystemExit(main())
