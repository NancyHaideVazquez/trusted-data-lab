from pathlib import Path

import pandas as pd

try:
    from src.integracion import integrar_datos
except ModuleNotFoundError:
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

    # Leer los identificadores como texto
    inegi = pd.read_csv(
        archivo_inegi,
        dtype={"serie_id": str},
    )

    banxico = pd.read_csv(
        archivo_banxico,
        dtype={"serie_id": str},
    )

    # Integrar con trazabilidad E2
    integrado = integrar_datos(
        inegi,
        banxico,
        incluir_trazabilidad=True,
    )

    # Verificar que la trazabilidad esté completa
    columnas_trazabilidad = [
        "archivo_origen",
        "fecha_ingesta_utc",
    ]

    assert len(integrado) == len(inegi) + len(banxico)
    assert integrado[columnas_trazabilidad].notna().all().all()

    # Guardar en un archivo independiente de E2
    archivo_salida = (
        carpeta_salida / "integracion_mensual_e2.csv"
    )

    integrado.to_csv(archivo_salida, index=False)

    print("================================")
    print(" E2 - INTEGRACION CON TRAZABILIDAD")
    print("================================")
    print("Registros INEGI:", len(inegi))
    print("Registros Banxico:", len(banxico))
    print("Registros integrados:", len(integrado))
    print("Columnas:", len(integrado.columns))
    print("Archivo generado:", archivo_salida)
    print("Integracion E2 completada correctamente.")


if __name__ == "__main__":
    main()