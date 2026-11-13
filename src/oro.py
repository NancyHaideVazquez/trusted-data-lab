
import pandas as pd

from src.calidad import validar_calidad


COLUMNAS_ORO = [
    "periodo",
    "fuente",
    "serie_id",
    "indicador",
    "valor",
    "unidad",
    "metodo",
    "cobertura"
]


def preparar_oro(datos_plata):
    """
    Prepara una tabla de consulta mensual para Oro.

    No mezcla indicadores ni modifica los valores.
    """

    # Validar nuevamente la entrada
    validados = validar_calidad(datos_plata)

    # Seleccionar las columnas para consulta
    oro = validados[COLUMNAS_ORO].copy()

    # Ordenar los datos
    oro = oro.sort_values(
        ["periodo", "fuente", "serie_id"]
    ).reset_index(drop=True)

    # Conservar todos los registros
    if len(oro) != len(validados):
        raise RuntimeError(
            "La preparacion de Oro perdio registros."
        )

    return oro
