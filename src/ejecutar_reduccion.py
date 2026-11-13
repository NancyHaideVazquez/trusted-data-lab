
from pathlib import Path

import pandas as pd

from reduccion import reducir_datos


def main():
    # Ubicar la carpeta principal del proyecto
    raiz = Path(__file__).resolve().parent.parent

    # Archivo de entrada
    entrada = raiz / "data/reportes/limpieza_preliminar_banxico.csv"

    # Archivo de salida
    salida = raiz / "data/reportes/reduccion_banxico.csv"

    # Leer los datos
    df = pd.read_csv(entrada)

    print("================================")
    print(" T09 - REDUCCION DE DATOS")
    print("================================")

    print("Filas antes:", len(df))
    print("Columnas antes:", len(df.columns))

    # Aplicar reduccion mensual
    resultado = reducir_datos(df)

    print("Filas despues:", len(resultado))
    print("Columnas despues:", len(resultado.columns))

    # Guardar el resultado
    salida.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(salida, index=False)

    print("Archivo generado:", salida)
    print("Reduccion completada correctamente.")


if __name__ == "__main__":
    main()
