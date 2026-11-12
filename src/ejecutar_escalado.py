
"""T07 - Ejecutar escalamiento de INEGI y Banxico."""

import json
from pathlib import Path

import pandas as pd

from src.transformaciones import escalar_datos


def main():
    carpeta = Path("data/reportes")
    carpeta.mkdir(parents=True, exist_ok=True)

    fuentes = ["banxico", "inegi"]
    parametros_generales = {}

    for fuente in fuentes:
        archivo = carpeta / f"limpieza_preliminar_{fuente}.csv"

        datos = pd.read_csv(archivo)

        escalados, parametros = escalar_datos(datos)

        salida = carpeta / f"escalado_{fuente}.csv"
        escalados.to_csv(salida, index=False)

        parametros_generales[fuente] = parametros

        print(f"{fuente.upper()}: {len(escalados)} registros")
        print(f"Archivo generado: {salida}")

    archivo_json = carpeta / "parametros_escalado.json"

    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(
            parametros_generales,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    print(f"Parametros guardados en: {archivo_json}")


if __name__ == "__main__":
    main()
