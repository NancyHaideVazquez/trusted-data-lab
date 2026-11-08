
"""
TRUSTED DATA LAB - extractores/inegi.py

Extractor de indicadores economicos del INEGI.

Permite consultar:
- BISE
- BIE-BISE

Modos:
- historico
- oportuno
- rango (pendiente de implementacion)
"""

import os
import re
from datetime import datetime

from .base import ExtractorEtico


URL_BASE = (
    "https://www.inegi.org.mx/app/api/indicadores/"
    "desarrolladores/jsonxml"
)

FORMATOS_FECHA_INEGI = (
    "%Y/%m/%d",
    "%Y-%m-%d",
    "%Y/%m",
    "%Y-%m",
    "%Y"
)

INDICADOR_POR_DEFECTO = "910402"


def _leer_token():
    """Obtiene el token desde la variable de entorno."""

    token = os.getenv("INEGI_TOKEN")

    if not token:
        raise RuntimeError(
            "Falta la variable de entorno INEGI_TOKEN"
        )

    return token


def _parsear_fecha(texto):
    """Convierte fechas recibidas desde INEGI."""

    for formato in FORMATOS_FECHA_INEGI:
        try:
            return datetime.strptime(
                texto, formato
            ).date()

        except ValueError:
            continue

    raise ValueError(
        f"Fecha del INEGI no reconocida: {texto!r}"
    )


def construir_url(
    indicador_id,
    modo="historico",
    inicio=None,
    fin=None,
    ubicacion="00",
    banco="BISE",
    version="2.0"
):
    """Construye la URL oficial de consulta de INEGI."""

    indicador_id = str(indicador_id)
    ubicacion = str(ubicacion)

    if not re.fullmatch(r"\d+", indicador_id):
        raise ValueError(
            "El indicador debe ser numerico"
        )

    if not re.fullmatch(r"\d{2,5}", ubicacion):
        raise ValueError(
            "Clave geografica incorrecta"
        )

    if banco not in ("BISE", "BIE-BISE"):
        raise ValueError(
            "Banco de INEGI no valido"
        )

    if modo == "historico":
        recientes = "false"

    elif modo == "oportuno":
        recientes = "true"

    elif modo == "rango":
        raise ValueError(
            "El modo rango todavia no esta implementado"
        )

    else:
        raise ValueError(
            "Modo de consulta no valido"
        )

    token = _leer_token()

    url = (
        f"{URL_BASE}/INDICATOR/{indicador_id}/"
        f"es/{ubicacion}/{recientes}/"
        f"{banco}/{version}/{token}?type=json"
    )

    return url


def resumir(crudo):
    """Genera un resumen de la respuesta de INEGI."""

    try:
        series = crudo["Series"]

        if not series:
            raise KeyError

        serie = series[0]

        observaciones = (
            serie.get("OBSERVATIONS") or []
        )

    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "La respuesta del INEGI no tiene "
            "la estructura esperada"
        ) from None

    fechas = []
    sin_dato = 0

    for obs in observaciones:

        valor = obs.get("OBS_VALUE")

        if valor in (None, "", "N/E"):
            sin_dato += 1

        periodo = obs.get("TIME_PERIOD")

        if periodo:
            try:
                fecha = _parsear_fecha(periodo)
                fechas.append(fecha)

            except ValueError:
                continue

    return {
        "indicador": serie.get("INDICADOR"),
        "titulo": (
            serie.get("TITULO")
            or serie.get("NOMBRE")
        ),
        "registros": len(observaciones),
        "primera_fecha": (
            min(fechas).isoformat()
            if fechas else None
        ),
        "ultima_fecha": (
            max(fechas).isoformat()
            if fechas else None
        ),
        "fechas_duplicadas": (
            len(fechas) - len(set(fechas))
        ),
        "sin_dato": sin_dato,
    }


def capturar(
    indicador_id=INDICADOR_POR_DEFECTO,
    modo="historico",
    inicio=None,
    fin=None,
    ubicacion="00",
    extractor=None,
    revisar_robots=True,
    banco="BISE"
):
    """
    Consulta un indicador del INEGI.

    Devuelve:
        paquete: metadata y respuesta original.
        resumen: informacion de validacion.
    """

    indicador_id = str(indicador_id)

    # Construimos la URL utilizando el banco seleccionado.
    url = construir_url(
        indicador_id=indicador_id,
        modo=modo,
        inicio=inicio,
        fin=fin,
        ubicacion=ubicacion,
        banco=banco
    )

    # Reutilizamos el extractor si fue proporcionado.
    propio = extractor is None

    if propio:
        extractor = ExtractorEtico(
            revisar_robots=revisar_robots
        )

    try:

        respuesta, metadatos = extractor.get(
            url,
            headers={
                "Accept": "application/json"
            }
        )

    finally:

        if propio:
            extractor.cerrar()

    try:

        crudo = respuesta.json()

    except ValueError:

        raise RuntimeError(
            "El INEGI no devolvio un JSON valido"
        ) from None

    resumen = resumir(crudo)

    # Verificamos que la respuesta corresponda al ID solicitado.
    if resumen["registros"] > 0:

        if str(resumen["indicador"]) != indicador_id:
            raise RuntimeError(
                "El indicador devuelto por INEGI "
                "no coincide con el solicitado"
            )

    if resumen["registros"] == 0 and modo != "oportuno":

        raise RuntimeError(
            "El INEGI respondio sin registros"
        )

    # Agregamos metadatos de la captura.
    metadatos.update({

        "source": f"INEGI {banco}",

        "indicator_id": indicador_id,

        "location": ubicacion,

        "mode": modo,

        "bank": banco,

        "records": resumen["registros"],

        "first_date": resumen["primera_fecha"],

        "last_date": resumen["ultima_fecha"],

    })

    return {
        "metadata": metadatos,
        "data": crudo
    }, resumen
