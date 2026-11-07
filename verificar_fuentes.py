
"""
TRUSTED DATA LAB
Verificacion de fuentes: INEGI y Banxico

Ejecutar desde la raiz del proyecto:
    python verificar_fuentes.py

No imprime tokens ni guarda respuestas que los contengan.
"""

import json
import os
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


# --------------------------------------------------
# CONFIGURACION
# --------------------------------------------------

RAIZ = Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

INEGI_TOKEN = os.getenv("INEGI_TOKEN")
BANXICO_TOKEN = os.getenv("BANXICO_TOKEN")

BASE_INEGI = (
    "https://www.inegi.org.mx/app/api/"
    "indicadores/desarrolladores/jsonxml"
)

BASE_BANXICO = (
    "https://www.banxico.org.mx/"
    "SieAPIRest/service/v1"
)

SERIE_BANXICO = "SF43783"
MINIMO_PERIODOS = 36

SALIDA = RAIZ / "reportes" / "validacion_fuentes.json"

# Agregar codigos reales obtenidos del constructor INEGI.
# No escribir codigos supuestos.
#
# Ejemplo de configuracion:
# {
#     "nombre": "Nombre oficial del indicador",
#     "codigo": "CODIGO_REAL",
#     "area": "AREA_REAL",
#     "fuente": "BISE"
# }

INDICADORES_INEGI = []


# --------------------------------------------------
# FUNCIONES GENERALES
# --------------------------------------------------

def solicitar_json(url, headers=None):
    """Consulta una API y devuelve JSON sin mostrar el token."""

    try:
        respuesta = requests.get(
            url,
            headers=headers,
            params={"type": "json"} if "inegi.org.mx" in url else None,
            timeout=60,
            allow_redirects=False
        )

        if respuesta.status_code != 200:
            raise RuntimeError(
                f"La API respondio HTTP {respuesta.status_code}"
            )

        datos = respuesta.json()

        if not isinstance(datos, dict):
            raise ValueError("La respuesta no es un objeto JSON")

        return datos

    except requests.RequestException:
        raise RuntimeError(
            "Error de conexion con la API"
        ) from None

    except ValueError:
        raise RuntimeError(
            "La API no devolvio JSON valido"
        ) from None


def numero(valor):
    """Convierte un valor a numero cuando es posible."""

    if valor is None or isinstance(valor, bool):
        return None

    texto = str(valor).strip().replace(",", "")

    if texto.upper() in {
        "", "N/E", "N/D", "NA", "N/A",
        "NULL", "ND", "S/D", "-"
    }:
        return None

    try:
        resultado = float(texto)

        if resultado != resultado:
            return None

        if resultado in (float("inf"), float("-inf")):
            return None

        return resultado

    except (ValueError, TypeError):
        return None


def guardar_reporte(reporte):
    """Guarda solamente resultados de validacion."""

    SALIDA.parent.mkdir(parents=True, exist_ok=True)

    SALIDA.write_text(
        json.dumps(
            reporte,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"\nReporte guardado en: {SALIDA}")


def meses_consecutivos(meses):
    """Obtiene la racha mas larga de meses seguidos."""

    ordenados = sorted(set(meses))

    if not ordenados:
        return 0

    mejor = 1
    actual = 1

    for anterior, siguiente in zip(
        ordenados, ordenados[1:]
    ):
        if siguiente - anterior == 1:
            actual += 1
        else:
            actual = 1

        mejor = max(mejor, actual)

    return mejor


def periodo_mensual(texto):
    """Convierte YYYY-MM o YYYY/MM a un numero de mes."""

    texto = str(texto).strip()

    coincidencia = re.fullmatch(
        r"(\d{4})[-/](\d{1,2})",
        texto
    )

    if not coincidencia:
        return None

    anio = int(coincidencia.group(1))
    mes = int(coincidencia.group(2))

    if not 1 <= mes <= 12:
        return None

    return anio * 12 + mes


def mostrar_resultado(nombre, resultado):
    """Imprime un resumen sin credenciales."""

    print(f"\n--- {nombre} ---")

    for clave, valor in resultado.items():
        if clave != "error":
            print(f"{clave}: {valor}")

    if "error" in resultado:
        print("Error:", resultado["error"])


# --------------------------------------------------
# VALIDACION DE BANXICO
# --------------------------------------------------

def convertir_fecha_banxico(texto):
    """Banxico normalmente devuelve fechas DD/MM/YYYY."""

    texto = str(texto).strip()

    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(
                texto, formato
            ).date()
        except ValueError:
            continue

    return None


def verificar_banxico():
    """Comprueba la serie TIIE a 28 dias."""

    resultado = {
        "institucion": "Banxico",
        "serie": SERIE_BANXICO,
        "estado": "PENDIENTE"
    }

    if not BANXICO_TOKEN:
        resultado["error"] = "Falta BANXICO_TOKEN"
        return resultado

    url = (
        f"{BASE_BANXICO}/series/"
        f"{SERIE_BANXICO}/datos"
    )

    try:
        datos = solicitar_json(
            url,
            headers={
                "Bmx-Token": BANXICO_TOKEN,
                "Accept": "application/json"
            }
        )

        series = datos.get("bmx", {}).get("series", [])

        if not series:
            raise ValueError("La respuesta no contiene series")

        serie = next(
            (
                s for s in series
                if s.get("idSerie") == SERIE_BANXICO
            ),
            None
        )

        if serie is None:
            raise ValueError(
                "La respuesta no corresponde a la serie solicitada"
            )

        titulo = serie.get("titulo", "")
        observaciones = serie.get("datos") or []

        fechas = []
        fechas_validas = []
        sin_dato = 0
        invalidas = 0
        futuras = 0

        hoy = date.today()

        for registro in observaciones:
            fecha = convertir_fecha_banxico(
                registro.get("fecha", "")
            )

            valor = numero(registro.get("dato"))

            if fecha is None:
                invalidas += 1
                continue

            fechas.append(fecha)

            if valor is None:
                sin_dato += 1
                continue

            if fecha > hoy:
                futuras += 1
                continue

            fechas_validas.append(fecha)

        conteos = Counter(fechas_validas)

        duplicados_validos = sum(
            cantidad - 1
            for cantidad in conteos.values()
            if cantidad > 1
        )

        periodos_validos = len(conteos)

        nombre_correcto = (
            "TIIE" in titulo.upper()
            and "28" in titulo
        )

        cumple = (
            nombre_correcto
            and periodos_validos >= MINIMO_PERIODOS
            and duplicados_validos == 0
        )

        resultado.update({
            "titulo": titulo,
            "registros_totales": len(observaciones),
            "primera_fecha": (
                min(fechas).isoformat() if fechas else None
            ),
            "ultima_fecha": (
                max(fechas).isoformat() if fechas else None
            ),
            "valores_sin_dato": sin_dato,
            "fechas_invalidas": invalidas,
            "valores_futuros": futuras,
            "duplicados_validos": duplicados_validos,
            "periodos_validos": periodos_validos,
            "cumple_36_periodos": (
                periodos_validos >= MINIMO_PERIODOS
            ),
            "estado": "VALIDADO" if cumple else "REVISAR"
        })

    except (RuntimeError, ValueError, TypeError) as error:
        resultado["estado"] = "ERROR"
        resultado["error"] = str(error)

    return resultado


# --------------------------------------------------
# CONEXION CON INEGI
# --------------------------------------------------

def verificar_conexion_inegi():
    """Comprueba el token con un indicador oficial conocido."""

    resultado = {
        "institucion": "INEGI",
        "prueba": "Conexion API de Indicadores",
        "estado": "PENDIENTE"
    }

    if not INEGI_TOKEN:
        resultado["error"] = "Falta INEGI_TOKEN"
        return resultado

    # Poblacion total: solo se usa para probar la API.
    codigo = "1002000001"

    url = (
        f"{BASE_INEGI}/CL_INDICATOR/"
        f"{codigo}/es/BISE/2.0/{INEGI_TOKEN}"
    )

    try:
        datos = solicitar_json(url)

        registros = datos.get("CODE", [])

        encontrado = next(
            (
                item for item in registros
                if str(item.get("value")) == codigo
            ),
            None
        )

        if encontrado is None:
            raise ValueError(
                "No se encontro el indicador de prueba"
            )

        resultado.update({
            "codigo": codigo,
            "descripcion": encontrado.get("Description"),
            "respuesta_valida": True,
            "estado": "VALIDADO"
        })

    except (RuntimeError, ValueError, TypeError) as error:
        resultado["estado"] = "ERROR"
        resultado["error"] = str(error)

    return resultado


# --------------------------------------------------
# INDICADORES REALES DE INEGI
# --------------------------------------------------

def verificar_indicador_inegi(config):
    """Comprueba frecuencia e historia de un indicador."""

    nombre = config.get("nombre", "Sin nombre")
    codigo = str(config.get("codigo", "")).strip()
    area = str(config.get("area", "")).strip()
    fuente = str(config.get("fuente", "BISE")).strip()

    resultado = {
        "institucion": "INEGI",
        "nombre": nombre,
        "codigo": codigo,
        "area_solicitada": area,
        "fuente": fuente,
        "estado": "PENDIENTE"
    }

    if not INEGI_TOKEN:
        resultado["error"] = "Falta INEGI_TOKEN"
        return resultado

    if not codigo or not area:
        resultado["error"] = (
            "Falta codigo o area verificada"
        )
        return resultado

    if fuente not in ("BISE", "BIE-BISE"):
        resultado["error"] = "Fuente INEGI no valida"
        return resultado

    # Descargamos el historico completo con false.
    url = (
        f"{BASE_INEGI}/INDICATOR/{codigo}/"
        f"es/{area}/false/{fuente}/2.0/{INEGI_TOKEN}"
    )

    try:
        datos = solicitar_json(url)

        series = datos.get("Series", [])

        if not series:
            raise ValueError(
                "No se encontraron series historicas"
            )

        # Filtramos las series del indicador solicitado.
        series_correctas = [
            s for s in series
            if str(s.get("INDICADOR", codigo)) == codigo
        ]

        if not series_correctas:
            raise ValueError(
                "La respuesta no coincide con el codigo"
            )

        evaluaciones = []

        for serie in series_correctas:

            observaciones = serie.get("OBSERVATIONS") or []

            meses = []
            fechas_no_mensuales = 0
            sin_dato = 0
            futuras = 0

            hoy = date.today()

            for obs in observaciones:
                valor = numero(obs.get("OBS_VALUE"))

                if valor is None:
                    sin_dato += 1
                    continue

                periodo = str(
                    obs.get("TIME_PERIOD", "")
                ).strip()

                indice_mes = periodo_mensual(periodo)

                if indice_mes is None:
                    fechas_no_mensuales += 1
                    continue

                anio = (indice_mes - 1) // 12
                mes = (indice_mes - 1) % 12 + 1

                if date(anio, mes, 1) > hoy:
                    futuras += 1
                    continue

                meses.append(indice_mes)

            conteos = Counter(meses)

            duplicados = sum(
                cantidad - 1
                for cantidad in conteos.values()
                if cantidad > 1
            )

            periodos_unicos = len(conteos)
            consecutivos = meses_consecutivos(meses)

            evaluaciones.append({
                "frecuencia_reportada": serie.get("FREQ"),
                "area_reportada": serie.get("GEO_AREA"),
                "total_observaciones": len(observaciones),
                "periodos_mensuales_validos": periodos_unicos,
                "racha_meses_consecutivos": consecutivos,
                "sin_dato": sin_dato,
                "fechas_no_mensuales": fechas_no_mensuales,
                "fechas_futuras": futuras,
                "duplicados": duplicados,
                "primer_periodo_indice": (
                    min(meses) if meses else None
                ),
                "ultimo_periodo_indice": (
                    max(meses) if meses else None
                )
            })

        # No sumamos meses de diferentes geografias.
        mejor = max(
            evaluaciones,
            key=lambda r: r["racha_meses_consecutivos"]
        )

        cumple_meses = (
            mejor["racha_meses_consecutivos"] >= 36
        )

        resultado.update({
            "series_recibidas": len(series_correctas),
            "evaluaciones": evaluaciones,
            "cumple_36_meses_consecutivos": cumple_meses,
            "estado": (
                "HISTORICO_VALIDADO"
                if cumple_meses else "REVISAR"
            ),
            "observacion": (
                "Verificar que la descripcion oficial y "
                "la geografia correspondan al proyecto."
            )
        })

    except (RuntimeError, ValueError, TypeError) as error:
        resultado["estado"] = "ERROR"
        resultado["error"] = str(error)

    return resultado


# --------------------------------------------------
# PROGRAMA PRINCIPAL
# --------------------------------------------------

def main():

    print("=" * 55)
    print("TRUSTED DATA LAB - VALIDACION DE FUENTES")
    print("=" * 55)

    reporte = {
        "fecha_verificacion_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "proyecto": "Observatorio de Vivienda y Costos de Colima",
        "banxico": {},
        "inegi_conexion": {},
        "inegi_indicadores": []
    }

    # PRUEBA 1: BANXICO
    print("\n1. Verificando Banxico...")

    reporte["banxico"] = verificar_banxico()

    mostrar_resultado(
        "BANXICO",
        reporte["banxico"]
    )

    # PRUEBA 2: INEGI
    print("\n2. Verificando conexion INEGI...")

    reporte["inegi_conexion"] = verificar_conexion_inegi()

    mostrar_resultado(
        "INEGI - CONEXION",
        reporte["inegi_conexion"]
    )

    # PRUEBA 3: INDICADORES INEGI
    print("\n3. Verificando indicadores INEGI...")

    if not INDICADORES_INEGI:
        print(
            "PENDIENTE: faltan codigos reales "
            "de indicadores de vivienda."
        )

    for indicador in INDICADORES_INEGI:

        resultado = verificar_indicador_inegi(
            indicador
        )

        reporte["inegi_indicadores"].append(
            resultado
        )

        mostrar_resultado(
            indicador["nombre"],
            resultado
        )

    # RESUMEN
    banxico_ok = (
        reporte["banxico"].get("estado") == "VALIDADO"
    )

    inegi_conexion_ok = (
        reporte["inegi_conexion"].get("estado")
        == "VALIDADO"
    )

    inegi_historico_ok = any(
        item.get("estado") == "HISTORICO_VALIDADO"
        for item in reporte["inegi_indicadores"]
    )

    print("\n" + "=" * 55)
    print("RESUMEN FINAL")
    print("=" * 55)

    print(
        "Banxico:",
        "VALIDADO" if banxico_ok else "PENDIENTE"
    )

    print(
        "Conexion INEGI:",
        "VALIDADA" if inegi_conexion_ok else "PENDIENTE"
    )

    print(
        "Historico mensual INEGI:",
        "VALIDADO" if inegi_historico_ok else "PENDIENTE"
    )

    print(
        "E0 - Validacion de fuentes:",
        "REQUIERE REVISION"
        if not (banxico_ok and inegi_historico_ok)
        else "HISTORICOS DISPONIBLES; REVISAR COBERTURA"
    )

    reporte["resumen"] = {
        "banxico_validado": banxico_ok,
        "inegi_conexion_validada": inegi_conexion_ok,
        "inegi_historico_validado": inegi_historico_ok,
        "e0_fuentes_completas": False
    }

    # E0 aun requiere confirmar cobertura, datos,
    # captura automatica y evidencias.
    guardar_reporte(reporte)


if __name__ == "__main__":
    main()
