
import math
import re
from datetime import datetime, timezone

from extractores.base import ExtractorEtico
from extractores.inegi import construir_url

INDICADORES = {
    "910399": "Inflacion mensual general",
    "910402": "Inflacion mensual servicios subyacentes",
    "910409": "Inflacion anual servicios subyacentes",
}


def validar_meses(observaciones):
    meses = set()
    mes_actual = datetime.now(timezone.utc)
    limite = mes_actual.year * 12 + mes_actual.month - 1

    for obs in observaciones:
        periodo = str(obs.get("TIME_PERIOD", "")).strip()
        valor = str(obs.get("OBS_VALUE", "")).strip()

        if not re.fullmatch(r"\d{4}/(0[1-9]|1[0-2])", periodo):
            continue

        try:
            numero = float(valor)
            if not math.isfinite(numero):
                continue
        except ValueError:
            continue

        anio, mes = map(int, periodo.split("/"))
        indice_mes = anio * 12 + mes - 1

        if indice_mes <= limite:
            meses.add(indice_mes)

    # Encontrar la mayor secuencia consecutiva
    consecutivos = 0
    maximo = 0

    for mes in sorted(meses):
        if (mes - 1) in meses:
            consecutivos += 1
        else:
            consecutivos = 1

        maximo = max(maximo, consecutivos)

    fechas = sorted(meses)

    return {
        "meses_validos": len(meses),
        "meses_consecutivos": maximo,
        "primera_fecha": (
            f"{fechas[0] // 12:04d}-{fechas[0] % 12 + 1:02d}"
            if fechas else None
        ),
        "ultima_fecha": (
            f"{fechas[-1] // 12:04d}-{fechas[-1] % 12 + 1:02d}"
            if fechas else None
        ),
    }


def main():
    with ExtractorEtico(revisar_robots=False) as extractor:
        for indicador_id, nombre in INDICADORES.items():
            print(f"\n--- {indicador_id}: {nombre} ---")

            try:
                url = construir_url(
                    indicador_id=indicador_id,
                    modo="historico",
                    ubicacion="00",
                    banco="BIE-BISE"
                )

                respuesta, metadatos = extractor.get(url)
                datos = respuesta.json()

                series = datos.get("Series", [])

                if not series:
                    print("ERROR: respuesta sin series")
                    continue

                serie = series[0]
                observaciones = serie.get("OBSERVATIONS") or []

                resultado = validar_meses(observaciones)

                print("HTTP:", metadatos["http_status"])
                print("ID devuelto:", serie.get("INDICADOR"))
                print("Frecuencia:", serie.get("FREQ"))
                print("Observaciones:", len(observaciones))
                print("Meses validos:", resultado["meses_validos"])
                print("Meses consecutivos:", resultado["meses_consecutivos"])
                print("Primera fecha:", resultado["primera_fecha"])
                print("Ultima fecha:", resultado["ultima_fecha"])

                cumple_id = str(serie.get("INDICADOR")) == indicador_id
                cumple_meses = resultado["meses_consecutivos"] >= 36
                cumple = cumple_id and cumple_meses

                print("ID coincide:", cumple_id)
                print("Cumple 36 meses:", cumple_meses)
                print("Cumple criterio completo:", cumple)

            except Exception as error:
                print("ERROR:", type(error).__name__, str(error))

if __name__ == "__main__":
    main()
