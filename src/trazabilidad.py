"""Referencias verificadas de Bronce para los indicadores mensuales."""

import json
from pathlib import Path


RUTAS_BRONCE = {
    "inegi": (
        "data/bronce/inegi/2026-11-12/"
        "910402_historico_130114_649094_60dc15f7.json"
    ),
    "banxico": (
        "data/bronce/banxico/2026-11-12/"
        "SF43783_historico_130116_421967_754519eb.json"
    ),
}


def obtener_trazabilidad(fuente, raiz=None):
    """Obtiene la referencia y fecha de captura del JSON verificado."""

    if fuente not in RUTAS_BRONCE:
        raise ValueError(f"Fuente desconocida: {fuente}")

    if raiz is None:
        raiz = Path(__file__).resolve().parent.parent

    ruta_relativa = RUTAS_BRONCE[fuente]
    ruta_absoluta = Path(raiz) / ruta_relativa

    if not ruta_absoluta.is_file():
        raise FileNotFoundError(
            f"No existe el archivo Bronce: {ruta_absoluta}"
        )

    with ruta_absoluta.open(encoding="utf-8-sig") as archivo:
        contenido = json.load(archivo)

    fecha = contenido.get("metadata", {}).get("captured_at_utc")

    if not fecha:
        raise ValueError(
            f"El archivo no tiene fecha de captura: {ruta_relativa}"
        )

    return {
        "archivo_origen": ruta_relativa,
        "fecha_ingesta_utc": fecha,
    }