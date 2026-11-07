"""
TRUSTED DATA LAB - extractores/inegi.py

Que hace este archivo
---------------------
Consulta un indicador del BISE (Banco de Indicadores) del INEGI y devuelve
la respuesta original junto con sus metadatos de captura.

Lo que necesitas antes de usarlo
--------------------------------
1. Un token gratuito del INEGI:
   https://www.inegi.org.mx/app/desarrolladores/generatoken/
2. Guardarlo en la variable de entorno INEGI_TOKEN. Nunca en el codigo.
3. El ID del indicador. Ejemplos oficiales:
   - 1002000001  -> PIB trimestral (variacion anual)
   - 628194       -> INPC mensual
   - 1002000002  -> PIB nominal
   Confirma en el catalogo del BISE que el indicador que elijas
   se actualiza con la frecuencia que necesitas.

Modos de consulta
-----------------
- "historico": toda la serie disponible.
- "oportuno":  solo el dato mas reciente (usa el parametro RECENT=1).
- "rango":     entre dos fechas AAAA-MM-DD (inicio y fin).

Ejemplo
-------
    from extractores.inegi import capturar

    paquete, resumen = capturar("1002000001", modo="oportuno")
    print(resumen["registros"], resumen["primera_fecha"], resumen["ultima_fecha"])
"""

import os
import re
from datetime import datetime

from .base import ExtractorEtico

# URL base del BISE. El token va al final de la ruta (por eso base.py lo tapa
# en los logs con [PROTEGIDO]).
URL_BASE = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml"

# Formato de fecha que usa el INEGI en sus respuestas: "AAAA/MM/DD" o "AAAA-MM-DD"
# segun el indicador. Probamos ambos al parsear.
FORMATOS_FECHA_INEGI = ("%Y/%m/%d", "%Y-%m-%d", "%Y-%m", "%Y")

# Indicador por defecto si el usuario no especifica uno (PIB trimestral).
INDICADOR_POR_DEFECTO = "1002000001"


def _leer_token():
    """Lee el token desde la variable de entorno. Falla con un mensaje claro."""
    token = os.getenv("INEGI_TOKEN")
    if not token:
        raise RuntimeError("Falta la variable de entorno INEGI_TOKEN")
    return token


def _parsear_fecha(texto):
    """Convierte la fecha del INEGI a date. Acepta varios formatos."""
    for formato in FORMATOS_FECHA_INEGI:
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    raise ValueError(f"Fecha del INEGI no reconocida: {texto!r}")


def construir_url(indicador_id, modo="historico", inicio=None, fin=None,
                  ubicacion="0700", banco="BISE", version="2.0"):
    """Arma la URL de consulta segun el modo elegido.

    Parametros oficiales del BISE:
      - indicador_id: ID numerico del indicador (solo digitos).
      - ubicacion:    clave geoestadistica (0700 = nacional).
      - banco:        BISE por defecto.
      - version:      2.0
    """
    if not re.fullmatch(r"[A-Za-z0-9]+", indicador_id or ""):
        raise ValueError("El ID del indicador solo puede tener letras y numeros")

    if not re.fullmatch(r"\d{4}", ubicacion or ""):
        raise ValueError("La ubicacion debe ser una clave de 4 digitos (ej. 0700)")

    token = _leer_token()

    # La base de la URL sin parámetros extras (el ?type=json lo agregamos después)
    url_base = f"{URL_BASE}/INDICATOR/{indicador_id}/es/{ubicacion}/false/{banco}/{version}/{token}"

    if modo == "historico":
        # Todo lo disponible para ese indicador.
        return f"{url_base}?type=json"

    if modo == "oportuno":
        # Solo el dato mas reciente.
        return f"{url_base}?type=json&RECENT=1"

    if modo == "rango":
        if not inicio or not fin:
            raise ValueError("El modo 'rango' necesita inicio y fin (AAAA-MM-DD)")
        datetime.strptime(inicio, "%Y-%m-%d")
        datetime.strptime(fin, "%Y-%m-%d")
        # El BISE espera fechas AAAA-MM-DD al final de la ruta.
        return f"{url_base}?type=json&STARTDATE={inicio}&ENDDATE={fin}"

    raise ValueError("Modo no valido: usa 'historico', 'oportuno' o 'rango'")


def resumir(crudo):
    """Revisa la respuesta del BISE y calcula un resumen para validarla.

    No modifica los datos: solo los lee. La estructura del BISE es:
      crudo["Series"][0]["OBSERVATIONS"] = [{"TIME_PERIOD": "...", "OBS_VALUE": "..."}]
    """
    try:
        series = crudo["Series"]
        if not series:
            raise KeyError
        serie = series[0]
        observaciones = serie.get("OBSERVATIONS") or []
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "La respuesta del INEGI no tiene la estructura esperada"
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
                fechas.append(_parsear_fecha(periodo))
            except ValueError:
                # Si una fecha viene rara, no rompemos el resumen: la ignoramos.
                continue

    return {
        "indicador": serie.get("INDICADOR"),
        "titulo": serie.get("TITULO") or serie.get("NOMBRE"),
        "registros": len(observaciones),
        "primera_fecha": min(fechas).isoformat() if fechas else None,
        "ultima_fecha": max(fechas).isoformat() if fechas else None,
        "fechas_duplicadas": len(fechas) - len(set(fechas)),
        "sin_dato": sin_dato,
    }


def capturar(indicador_id=INDICADOR_POR_DEFECTO, modo="historico",
             inicio=None, fin=None, ubicacion="0700",
             extractor=None, revisar_robots=True):
    """Consulta un indicador del BISE.

    Devuelve dos cosas:
      paquete: {"metadata": {...}, "data": <respuesta original del INEGI>}
               listo para guardarse en la capa bronce.
      resumen: diccionario con conteos para validar la captura.

    Como distinguir "sin dato nuevo" de "error":
      - Error: se lanza una excepcion (token malo, indicador inexistente, sin red).
      - Sin dato nuevo: la consulta funciona, pero la ultima_fecha del resumen
        es igual a la de la captura anterior. Esa comparacion la hace main.py.
    """
    # construir_url() ya valida el token y arma la ruta.
    url = construir_url(indicador_id, modo, inicio, fin, ubicacion)

    # Reutilizamos un extractor si nos lo pasan; si no, creamos uno y lo cerramos.
    propio = extractor is None
    if propio:
        extractor = ExtractorEtico(revisar_robots=revisar_robots)

    try:
        # El token viaja DENTRO de la URL (asi funciona el BISE).
        # base.py._url_segura() lo tapa en logs y metadatos.
        respuesta, metadatos = extractor.get(
            url,
            headers={"Accept": "application/json"},
        )
    finally:
        if propio:
            extractor.cerrar()

    try:
        crudo = respuesta.json()
    except ValueError:
        raise RuntimeError("El INEGI no devolvio un JSON valido") from None

    resumen = resumir(crudo)

    # En modo historico o rango esperamos al menos un registro.
    # En modo oportuno, cero registros no es un error.
    if resumen["registros"] == 0 and modo != "oportuno":
        raise RuntimeError(
            "El INEGI respondio sin registros: revisa el indicador y el rango"
        )

    metadatos.update({
        "source": "INEGI BISE",
        "indicator_id": indicador_id,
        "location": ubicacion,
        "mode": modo,
        "records": resumen["registros"],
        "first_date": resumen["primera_fecha"],
        "last_date": resumen["ultima_fecha"],
    })

    return {"metadata": metadatos, "data": crudo}, resumen