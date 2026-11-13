
from pathlib import Path

import pandas as pd

try:
    from src.cuarentena import separar_cuarentena
except ModuleNotFoundError:
    from cuarentena import separar_cuarentena


BASE = Path(__file__).resolve().parent.parent

ENTRADA = BASE / "data" / "plata" / "integracion_mensual.csv"

CARPETA_CUARENTENA = BASE / "data" / "cuarentena"
REGISTROS = CARPETA_CUARENTENA / "registros"
REPORTES = CARPETA_CUARENTENA / "reportes"


def ejecutar():
    print("T12 - CUARENTENA DE REGISTROS")

    if not ENTRADA.exists():
        raise FileNotFoundError(
            f"No existe el archivo de entrada: {ENTRADA}"
        )

    datos = pd.read_csv(
        ENTRADA,
        dtype={"serie_id": str}
    )

    validos, rechazados = separar_cuarentena(datos)

    REGISTROS.mkdir(parents=True, exist_ok=True)
    REPORTES.mkdir(parents=True, exist_ok=True)

    archivo_rechazados = (
        REGISTROS / "integracion_mensual_rechazados.csv"
    )

    archivo_reporte = (
        REPORTES / "reporte_cuarentena.csv"
    )

    # Conservar los registros rechazados y sus motivos
    rechazados.to_csv(archivo_rechazados, index=False)

    reporte = pd.DataFrame([{
        "archivo": ENTRADA.name,
        "registros_originales": len(datos),
        "registros_validos": len(validos),
        "registros_rechazados": len(rechazados),
        "estado": (
            "CON_RECHAZOS" if len(rechazados) else "SIN_RECHAZOS"
        )
    }])

    reporte.to_csv(archivo_reporte, index=False)

    print("Registros originales:", len(datos))
    print("Registros validos:", len(validos))
    print("Registros rechazados:", len(rechazados))
    print("Archivo de rechazados:", archivo_rechazados)
    print("Reporte generado:", archivo_reporte)


if __name__ == "__main__":
    ejecutar()
