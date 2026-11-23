"""Genera la capa Oro de E2 con trazabilidad."""

from pathlib import Path

import pandas as pd

from src.oro import preparar_oro


def main():
    raiz = Path(__file__).resolve().parent.parent

    entrada = raiz / "data/plata/integracion_mensual_e2.csv"
    salida = raiz / "data/oro/indicadores_mensuales_e2.csv"

    if not entrada.is_file():
        raise FileNotFoundError(
            f"No existe Plata E2: {entrada}"
        )

    # Mantener los identificadores de series como texto.
    plata = pd.read_csv(
        entrada,
        dtype={"serie_id": str},
    )

    # La trazabilidad es obligatoria para esta entrega.
    columnas_trazabilidad = [
        "archivo_origen",
        "fecha_ingesta_utc",
    ]

    faltantes = [
        columna
        for columna in columnas_trazabilidad
        if columna not in plata.columns
    ]

    if faltantes:
        raise ValueError(
            f"Faltan columnas de trazabilidad: {faltantes}"
        )

    if plata[columnas_trazabilidad].isna().any().any():
        raise ValueError(
            "Existen registros sin trazabilidad."
        )

    # Validar Plata y generar Oro.
    oro = preparar_oro(plata)

    # Verificar conservación de registros y valores.
    if len(oro) != len(plata):
        raise RuntimeError(
            "Oro no conserva todos los registros."
        )

    claves = ["fuente", "serie_id", "periodo"]

    comparacion = plata[
        claves + ["valor"]
    ].merge(
        oro[claves + ["valor"]],
        on=claves,
        suffixes=("_plata", "_oro"),
        validate="one_to_one",
    )

    if len(comparacion) != len(plata):
        raise RuntimeError(
            "No coinciden los registros de Plata y Oro."
        )

    if not (
        comparacion["valor_plata"]
        == comparacion["valor_oro"]
    ).all():
        raise RuntimeError(
            "Se modificaron valores durante la preparación de Oro."
        )

    # Guardar sin sobrescribir Oro de E1.
    salida.parent.mkdir(parents=True, exist_ok=True)
    oro.to_csv(salida, index=False)

    print("================================")
    print(" E2 - GENERACION DE ORO")
    print("================================")
    print("Registros Plata:", len(plata))
    print("Registros Oro:", len(oro))
    print("Columnas Oro:", len(oro.columns))
    print("Valores conservados:", len(comparacion))
    print("Archivo generado:", salida)
    print("Oro E2 generado correctamente.")


if __name__ == "__main__":
    main()