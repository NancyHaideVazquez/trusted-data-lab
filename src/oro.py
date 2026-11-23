from src.calidad import validar_calidad

COLUMNAS_ORO = [
    "periodo",
    "fuente",
    "serie_id",
    "indicador",
    "valor",
    "unidad",
    "metodo",
    "cobertura",
]

COLUMNAS_TRAZABILIDAD = [
    "archivo_origen",
    "fecha_ingesta_utc",
]


def preparar_oro(datos_plata):
    """Valida Plata y prepara Oro conservando la trazabilidad."""

    validados = validar_calidad(datos_plata)

    columnas = COLUMNAS_ORO.copy()

    presentes = [
        columna
        for columna in COLUMNAS_TRAZABILIDAD
        if columna in validados.columns
    ]

    if presentes and len(presentes) != len(COLUMNAS_TRAZABILIDAD):
        raise ValueError(
            "La trazabilidad está incompleta: "
            "deben existir ambas columnas."
        )

    columnas.extend(presentes)

    oro = validados[columnas].copy()

    oro = oro.sort_values(
        ["periodo", "fuente", "serie_id"]
    ).reset_index(drop=True)

    if len(oro) != len(validados):
        raise RuntimeError(
            "La preparacion de Oro perdio registros."
        )

    return oro