"""
TRUSTED DATA LAB - extractores/banxico.py

Que hace este archivo
---------------------
Consulta una serie del SIE (Sistema de Informacion Economica) de Banxico y
devuelve la respuesta original junto con sus metadatos de captura.

Lo que necesitas antes de usarlo
--------------------------------
1. Un token gratuito de Banxico (https://www.banxico.org.mx/SieAPIRest/service/v1/token).
2. Guardarlo en la variable de entorno BANXICO_TOKEN. Nunca en el codigo.
3. La clave de la serie. Ejemplo oficial: SF43783 (TIIE a 28 dias).
   Confirma en el catalogo del SIE que la serie que elijas se actualiza
   a diario; no todas las series financieras lo hacen.

Modos de consulta
-----------------
- "historico": toda la serie disponible (para la serie historica de bronce).
- "oportuno":  solo el dato mas reciente (para la captura diaria).
- "rango":     entre dos fechas AAAA-MM-DD (inicio y fin).

Ejemplo
-------
    from extractores.banxico import capturar

    paquete, resumen = capturar("SF43783", modo="historico")
    print(resumen["registros"], resumen["primera_fecha"], resumen["ultima_fecha"])
"""

import os
import re
from datetime import datetime

from .base import ExtractorEtico

URL_BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"

# Formato de fecha que usa Banxico en sus respuestas: dia/mes/anio.
FORMATO_FECHA_BANXICO = "%d/%m/%Y"


def _leer_token():
    """Lee el token desde la variable de entorno. Falla con un mensaje claro."""
    token = os.getenv("BANXICO_TOKEN")
    if not token:
        raise RuntimeError("Falta la variable de entorno BANXICO_TOKEN")
    return token


def construir_url(serie_id, modo="historico", inicio=None, fin=None):
    """Arma la URL de consulta segun el modo elegido."""
    # La clave de serie solo puede tener letras y numeros. Esto evita que
    # alguien meta caracteres raros dentro de la URL.
    if not re.fullmatch(r"[A-Za-z0-9]+", serie_id or ""):
        raise ValueError("La clave de serie solo puede tener letras y numeros")

    if modo == "historico":
        return f"{URL_BASE}/{serie_id}/datos"

    if modo == "oportuno":
        return f"{URL_BASE}/{serie_id}/datos/oportuno"

    if modo == "rango":
        if not inicio or not fin:
            raise ValueError("El modo 'rango' necesita inicio y fin (AAAA-MM-DD)")
        # strptime lanza ValueError si la fecha esta mal escrita.
        datetime.strptime(inicio, "%Y-%m-%d")
        datetime.strptime(fin, "%Y-%m-%d")
        return f"{URL_BASE}/{serie_id}/datos/{inicio}/{fin}"

    raise ValueError("Modo no valido: usa 'historico', 'oportuno' o 'rango'")


def resumir(crudo):
    """Revisa la respuesta de Banxico y calcula un resumen para validarla.

    No modifica los datos: solo los lee. El resumen sirve para comprobar
    cuantos registros llegaron, de que fecha a que fecha, si hay fechas
    repetidas y cuantos valores vienen sin dato.
    """
    try:
        serie = crudo["bmx"]["series"][0]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("La respuesta de Banxico no tiene la estructura esperada") from None

    registros = serie.get("datos") or []
    fechas = []
    sin_dato = 0

    for registro in registros:
        fechas.append(datetime.strptime(registro["fecha"], FORMATO_FECHA_BANXICO).date())

        # Banxico usa "N/E" cuando el dato no esta disponible.
        if registro.get("dato") in (None, "", "N/E"):
            sin_dato += 1

    return {
        "serie": serie.get("idSerie"),
        "titulo": serie.get("titulo"),
        "registros": len(registros),
        "primera_fecha": min(fechas).isoformat() if fechas else None,
        "ultima_fecha": max(fechas).isoformat() if fechas else None,
        "fechas_duplicadas": len(fechas) - len(set(fechas)),
        "sin_dato": sin_dato,
    }


def capturar(serie_id, modo="historico", inicio=None, fin=None,
             extractor=None, revisar_robots=True):
    """Consulta una serie de Banxico.

    Devuelve dos cosas:
      paquete: {"metadata": {...}, "data": <respuesta original de Banxico>}
               listo para guardarse en la capa bronce.
      resumen: diccionario con conteos para validar la captura.

    Como distinguir "sin dato nuevo" de "error":
      - Error: se lanza una excepcion (token malo, serie inexistente, sin red).
      - Sin dato nuevo: la consulta funciona, pero la ultima_fecha del resumen
        es igual a la de la captura anterior. Esa comparacion la hace main.py.
    """
    token = _leer_token()
    url = construir_url(serie_id, modo, inicio, fin)

    # Si nos pasan un extractor lo reutilizamos; si no, creamos uno y lo cerramos.
    propio = extractor is None
    if propio:
        extractor = ExtractorEtico(revisar_robots=revisar_robots)

    try:
        # El token va en un encabezado (header), no en la URL.
        respuesta, metadatos = extractor.get(
            url,
            headers={"Bmx-Token": token, "Accept": "application/json"},
        )
    finally:
        if propio:
            extractor.cerrar()

    try:
        crudo = respuesta.json()
    except ValueError:
        raise RuntimeError("Banxico no devolvio un JSON valido") from None

    resumen = resumir(crudo)

    # En modo historico o rango esperamos al menos un registro.
    # En modo oportuno, cero registros no es un error.
    if resumen["registros"] == 0 and modo != "oportuno":
        raise RuntimeError("Banxico respondio sin registros: revisa la serie y el rango")

    metadatos.update({
        "source": "Banxico SIE",
        "series_id": serie_id,
        "mode": modo,
        "records": resumen["registros"],
        "first_date": resumen["primera_fecha"],
        "last_date": resumen["ultima_fecha"],
    })

    return {"metadata": metadatos, "data": crudo}, resumen
