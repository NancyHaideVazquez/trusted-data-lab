
from scipy.stats import _finite_differences
import pandas as pd
from pandera.errors import SchemaErrors

from src.calidad import validar_calidad


def separar_cuarentena(datos):
    """
    Separa registros validos e invalidos.

    Si hay errores estructurales que no se pueden
    atribuir a filas, detiene el proceso.
    """

    originales = datos.copy(deep=True).reset_index(drop=True)

    try:
        validar_calidad(originales)

        validos = originales.copy()
        rechazados = originales.iloc[0:0].copy()
        rechazados["motivo_rechazo"] = pd.Series(dtype=str)

        return validos, rechazados

    except SchemaErrors as error:
        fallos = error.failure_cases.copy()

        # No permitir errores sin fila identificable
        if fallos.empty or fallos["index"].isna().any():
            raise ValueError(
                "Error estructural o global: "
                "no es seguro separar los registros."
            ) from error

        motivos = {}

        for _, fallo in fallos.iterrows():
            indice = fallo["index"]

            # Solo se aceptan indices enteros de filas
            if (
                isinstance(indice, bool)
                or not isinstance(indice, (int, float))
                or not float(indice).is_integer()
            ):
                raise ValueError(
                    "Pandera devolvio un indice no valido."
                ) from error

            indice = int(indice)

            if not 0 <= indice < len(originales):
                raise ValueError(
                    "Pandera devolvio un indice fuera de rango."
                ) from error

            columna = str(fallo.get("column", "desconocida"))
            regla = str(fallo.get("check", "regla_desconocida"))

            if columna == "periodo":
                mensaje = (
                    "Periodo invalido: se esperaba AAAA-MM "
                    "con un mes entre 01 y 12."
                )
            elif columna == "valor":
                mensaje = (
                    "Valor invalido: debe ser numerico, "
                    "finito y no estar vacio."
                )
            elif columna == "fuente":
                mensaje = (
                    "Fuente invalida: solo se permite "
                    "inegi o banxico."
                )
            elif columna == "frecuencia":
                mensaje = "Frecuencia invalida: se esperaba mensual."
            elif columna in [
                "serie_id", "indicador", "unidad",
                "metodo", "cobertura"
            ]:
                mensaje = f"{columna}: dato obligatorio invalido."
            else:
                mensaje = f"{columna}: incumple la regla {regla}"

            motivos.setdefault(indice, []).append(mensaje)


        indices_rechazados = sorted(motivos)

        rechazados = originales.iloc[
            indices_rechazados
        ].copy()

        rechazados["motivo_rechazo"] = [
            "; ".join(motivos[indice])
            for indice in indices_rechazados
        ]

        validos = originales.drop(
            index=indices_rechazados
        ).copy()

        # Verificar que los registros restantes sean validos
        validar_calidad(validos)

        # Comprobar que ningun registro se perdio
        assert len(validos) + len(rechazados) == len(originales)

        return (
            validos.reset_index(drop=True),
            rechazados.reset_index(drop=True)
        )
