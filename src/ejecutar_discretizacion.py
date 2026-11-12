
"""T08 - Ejecutar discretizacion de INEGI y Banxico."""

import json
from pathlib import Path

import pandas as pd

from src.discretizacion import discretizar_datos


def main():

    carpeta = Path("data/reportes")
    carpeta.mkdir(parents=True, exist_ok=True)

    fuentes = ["banxico", "inegi"]

    parametros_generales = {}

    for fuente in fuentes:

        entrada = carpeta / f"limpieza_preliminar_{fuente}.csv"

        datos = pd.read_csv(entrada)

        # Aplicamos intervalos de igual amplitud.
        resultado_cut, parametros_cut = discretizar_datos(
            datos,
            metodo="cut"
        )

        # Aplicamos intervalos por cuantiles.
        resultado_qcut, parametros_qcut = discretizar_datos(
            resultado_cut,
            metodo="qcut"
        )

        # Guardamos ambas clasificaciones.
        salida = carpeta / f"discretizacion_{fuente}.csv"

        resultado_qcut.to_csv(salida, index=False)

        parametros_generales[fuente] = {
            "cut": parametros_cut,
            "qcut": parametros_qcut
        }

        print(f"\n{fuente.upper()}")
        print(f"Registros: {len(resultado_qcut)}")

        print("\nClasificacion CUT:")
        print(resultado_qcut["valor_cut"].value_counts(dropna=False))

        print("\nClasificacion QCUT:")
        print(resultado_qcut["valor_qcut"].value_counts(dropna=False))

        print(f"\nArchivo generado: {salida}")

    # Guardamos los limites utilizados.
    archivo_json = carpeta / "parametros_discretizacion.json"

    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(
            parametros_generales,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nParametros guardados en: {archivo_json}")


if __name__ == "__main__":
    main()
