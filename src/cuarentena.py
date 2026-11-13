import pandas as pd
from pandera.errors import SchemaErrors

from src.calidad import validar_calidad


def separar_cuarentena(datos):
    """
    Separa registros validos e invalidos.

    Los duplicados se identifican por fuente, serie_id
    y periodo. Se conserva la primera observacion y
    las posteriores se envian a Cuarentena con motivo.

    Los demas errores se validan mediante Pandera.

    Si existe un error estructural que no puede
    atribuirse a filas, se detiene el proceso.

    No modifica el DataFrame original.
    """

    originales = datos.copy(deep=True).reset_index(drop=True)

    # Comprobar primero la estructura necesaria para
    # identificar duplicados de manera segura.
    columnas_clave = ["fuente", "serie_id", "periodo"]

    # La validacion estructural completa sigue siendo
    # responsabilidad de Pandera.
    if not all(
        columna in originales.columns
        for columna in columnas_clave
    ):
        raise ValueError(
            "Error estructural: faltan columnas "
            "necesarias para identificar duplicados."
        )

    motivos = {}

    # Identificar duplicados conservando la primera fila.
    mascara_duplicados = originales.duplicated(
        subset=columnas_clave,
        keep="first"
    )

    indices_duplicados = originales.index[
        mascara_duplicados
    ].tolist()

    for indice in indices_duplicados:
        motivos[indice] = [
            "Registro duplicado: misma fuente, "
            "serie_id y periodo."
        ]

    # Excluir temporalmente los duplicados de la
    # validacion para evitar que la regla global
    # de Pandera genere motivos incorrectos.
    candidatos = originales.loc[
        ~mascara_duplicados
    ].copy()

    try:
        validar_calidad(candidatos)

    except SchemaErrors as error:
        fallos = error.failure_cases.copy()

        # Un error sin fila identificable no puede
        # enviarse a Cuarentena de forma segura.
        if (
            fallos.empty
            or "index" not in fallos.columns
            or fallos["index"].isna().any()
        ):
            raise ValueError(
                "Error estructural o global: "
                "no es seguro separar los registros."
            ) from error

        for _, fallo in fallos.iterrows():
            indice = fallo["index"]

            if (
                isinstance(indice, bool)
                or not isinstance(indice, (int, float))
                or not float(indice).is_integer()
            ):
                raise ValueError(
                    "Pandera devolvio un indice no valido."
                ) from error

            indice = int(indice)

            if indice not in candidatos.index:
                raise ValueError(
                    "Pandera devolvio un indice fuera "
                    "de los registros evaluados."
                ) from error

            columna = str(
                fallo.get("column", "desconocida")
            )

            regla = str(
                fallo.get("check", "regla_desconocida")
            )

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
                mensaje = (
                    "Frecuencia invalida: "
                    "se esperaba mensual."
                )

            elif columna in [
                "serie_id",
                "indicador",
                "unidad",
                "metodo",
                "cobertura"
            ]:
                mensaje = (
                    f"{columna}: dato obligatorio invalido."
                )

            else:
                # No inventar un motivo si Pandera
                # devuelve una regla desconocida.
                mensaje = (
                    f"{columna}: incumple la regla "
                    f"{regla}."
                )

            motivos.setdefault(indice, [])

            # Evitar repetir exactamente el mismo motivo.
            if mensaje not in motivos[indice]:
                motivos[indice].append(mensaje)

    # Separar los registros utilizando los indices
    # originales para conservar la trazabilidad.
    indices_rechazados = sorted(motivos)

    rechazados = originales.loc[
        indices_rechazados
    ].copy()

    rechazados["motivo_rechazo"] = [
        "; ".join(motivos[indice])
        for indice in indices_rechazados
    ]

    validos = originales.drop(
        index=indices_rechazados
    ).copy()

    # Comprobar que la tabla valida cumple Pandera.
    validar_calidad(validos)

    # Ningun registro puede desaparecer silenciosamente.
    if len(validos) + len(rechazados) != len(originales):
        raise RuntimeError(
            "Error de conciliacion: se perdieron registros."
        )

    return (
        validos.reset_index(drop=True),
        rechazados.reset_index(drop=True)
    )
