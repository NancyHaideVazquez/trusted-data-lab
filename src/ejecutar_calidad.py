
from pathlib import Path

import pandas as pd
from pandera.errors import SchemaErrors

try:
    from src.calidad import validar_calidad
except ModuleNotFoundError:
    from calidad import validar_calidad


BASE = Path(__file__).resolve().parent.parent

ENTRADA = BASE / "data" / "plata" / "integracion_mensual.csv"
REPORTE = BASE / "data" / "reportes" / "validacion_calidad.csv"


def ejecutar():
    print("T11 - PUERTA DE CALIDAD")

    if not ENTRADA.exists():
        raise FileNotFoundError(
            f"No existe el archivo de entrada: {ENTRADA}"
        )

    datos = pd.read_csv(ENTRADA, dtype={"serie_id": str})

    REPORTE.parent.mkdir(parents=True, exist_ok=True)

    try:
        validados = validar_calidad(datos)

        reporte = pd.DataFrame([{
            "archivo": ENTRADA.name,
            "registros": len(datos),
            "registros_aprobados": len(validados),
            "errores_detectados": 0,
            "estado": "APROBADO"
        }])

        reporte.to_csv(REPORTE, index=False)

        print("Estado: APROBADO")
        print("Registros aprobados:", len(validados))
        print("Reporte generado:", REPORTE)

    except SchemaErrors as error:
        reporte = pd.DataFrame([{
            "archivo": ENTRADA.name,
            "registros": len(datos),
            "registros_aprobados": 0,
            "errores_detectados": len(error.failure_cases),
            "estado": "RECHAZADO"
        }])

        reporte.to_csv(REPORTE, index=False)

        print("Estado: RECHAZADO")
        print("Errores de validacion:", len(error.failure_cases))
        print(error.failure_cases.to_string(index=False))
        print("Reporte generado:", REPORTE)

        raise SystemExit(1)


if __name__ == "__main__":
    ejecutar()
