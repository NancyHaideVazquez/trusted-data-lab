
from pathlib import Path

import pandas as pd

from integracion import integrar_datos


def main():
    carpeta_proyecto = Path(__file__).resolve().parent.parent

    archivo_inegi = (
        carpeta_proyecto
        / "data/reportes/limpieza_preliminar_inegi.csv"
    )

    archivo_banxico = (
        carpeta_proyecto
        / "data/reportes/reduccion_banxico.csv"
    )

    carpeta_salida = carpeta_proyecto / "data/plata"
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    # Leer archivos
    inegi = pd.read_csv(archivo_inegi)
    banxico = pd.read_csv(archivo_banxico)

    # Integrar
    integrado = integrar_datos(inegi, banxico)

    # Guardar resultado
    archivo_salida = carpeta_salida / "integracion_mensual.csv"
    integrado.to_csv(archivo_salida, index=False)

    print("T10 - INTEGRACION DE DATOS")
    print("Registros INEGI:", len(inegi))
    print("Registros Banxico:", len(banxico))
    print("Registros integrados:", len(integrado))
    print("Archivo generado:", archivo_salida)
    print("Integracion completada correctamente.")


if __name__ == "__main__":
    main()
