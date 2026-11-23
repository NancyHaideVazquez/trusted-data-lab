
import hashlib
import json
from datetime import UTC
from pathlib import Path

import geopandas as gpd

RUTA_BRONCE = Path(
    "data/bronce/inegi_marco_geoestadistico/2026"
)

ARCHIVO_ORIGINAL = RUTA_BRONCE / "2026_1_06_MUN.zip"
ARCHIVO_METADATOS = RUTA_BRONCE / "metadatos.json"

COLUMNAS_ESPERADAS = {
    "CVEGEO",
    "CVE_ENT",
    "CVE_MUN",
    "NOMGEO",
    "geometry",
}


def cargar_metadatos():
    """Lee los metadatos registrados en Bronce."""
    with ARCHIVO_METADATOS.open(
        "r", encoding="utf-8-sig"
    ) as archivo:
        return json.load(archivo)


def verificar_integridad(metadatos):
    """Comprueba que el ZIP coincide con su SHA-256."""
    sha256 = hashlib.sha256()

    with ARCHIVO_ORIGINAL.open("rb") as archivo:
        for bloque in iter(
            lambda: archivo.read(1024 * 1024), b""
        ):
            sha256.update(bloque)

    hash_actual = sha256.hexdigest().upper()
    hash_esperado = metadatos["sha256"].upper()

    if hash_actual != hash_esperado:
        raise ValueError(
            "El archivo Bronce no coincide con su SHA-256."
        )

    return hash_actual


def cargar_municipios():
    """Lee y valida los municipios del Marco Geoestadístico."""
    metadatos = cargar_metadatos()
    hash_verificado = verificar_integridad(metadatos)

    municipios = gpd.read_file(ARCHIVO_ORIGINAL)

    faltantes = COLUMNAS_ESPERADAS - set(municipios.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas obligatorias: {sorted(faltantes)}"
        )

    if len(municipios) != 10:
        raise ValueError(
            f"Se esperaban 10 municipios, se encontraron "
            f"{len(municipios)}."
        )

    if municipios.crs is None:
        raise ValueError("El archivo no tiene CRS definido.")

    if municipios["CVEGEO"].isna().any():
        raise ValueError("Existen claves municipales nulas.")

    if municipios["CVEGEO"].duplicated().any():
        raise ValueError("Existen claves municipales duplicadas.")

    if municipios.geometry.isna().any():
        raise ValueError("Existen geometrías nulas.")

    if municipios.geometry.is_empty.any():
        raise ValueError("Existen geometrías vacías.")

    if not municipios.geometry.is_valid.all():
        raise ValueError("Existen geometrías inválidas.")

    claves_requeridas = {"06002", "06010"}
    claves_encontradas = set(
        municipios["CVEGEO"].astype(str)
    )

    if not claves_requeridas.issubset(claves_encontradas):
        raise ValueError(
            "Faltan Colima o Villa de Álvarez."
        )

    return municipios, metadatos, hash_verificado



def preparar_plata():
    """
    Transforma los municipios validados a EPSG:4326
    e incorpora la trazabilidad del archivo original.
    """
    from datetime import datetime

    municipios, metadatos, hash_verificado = cargar_municipios()

    plata = municipios.copy()

    # Estandarizar nombres de columnas.
    plata = plata.rename(
        columns={
            "CVEGEO": "cvegeo",
            "CVE_ENT": "cve_ent",
            "CVE_MUN": "cve_mun",
            "NOMGEO": "nomgeo",
        }
    )

    # Transformar coordenadas para uso cartografico.
    plata = plata.to_crs(epsg=4326)

    # Incorporar procedencia.
    plata["fuente"] = metadatos["fuente"]
    plata["edicion"] = metadatos["edicion"]
    plata["archivo_origen"] = metadatos["ruta_bronce"]
    plata["sha256_origen"] = hash_verificado
    plata["procesado_utc"] = datetime.now(
        UTC
    ).isoformat()

    # Ordenar por clave municipal.
    plata = plata.sort_values("cvegeo").reset_index(drop=True)

    return plata


def guardar_plata():
    """
    Guarda los municipios procesados en la Capa Plata.
    """
    ruta_salida = Path(
        "data/plata/municipios_colima_2026.gpkg"
    )

    plata = preparar_plata()

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    plata.to_file(
        ruta_salida,
        layer="municipios_colima_2026",
        driver="GPKG",
        index=False
    )

    verificacion = gpd.read_file(
        ruta_salida,
        layer="municipios_colima_2026"
    )

    if len(verificacion) != 10:
        raise RuntimeError("No se guardaron los 10 municipios.")

    if verificacion.crs.to_epsg() != 4326:
        raise RuntimeError("El CRS guardado es incorrecto.")

    if not verificacion.geometry.is_valid.all():
        raise RuntimeError("Hay geometrías inválidas.")

    print("=" * 50)
    print("E2 - CAPA PLATA GEOESPACIAL")
    print("=" * 50)
    print("Archivo:", ruta_salida)
    print("Municipios guardados:", len(verificacion))
    print("CRS:", verificacion.crs)
    print("Geometrías válidas:", verificacion.geometry.is_valid.sum())
    print("GEOPACKAGE GENERADO CORRECTAMENTE")

    return ruta_salida


if __name__ == "__main__":
    municipios, metadatos, hash_verificado = cargar_municipios()

    print("=" * 50)
    print("E2 - VALIDACION GEOESPACIAL")
    print("=" * 50)

    print("Fuente:", metadatos["fuente"])
    print("Edicion:", metadatos["edicion"])
    print("Municipios:", len(municipios))
    print("CRS:", municipios.crs)
    print("Geometrias validas:", municipios.geometry.is_valid.sum())
    print("SHA-256 verificado:", hash_verificado)

    print("\nMUNICIPIOS:")
    print(
        municipios[
            ["CVEGEO", "NOMGEO"]
        ].sort_values("CVEGEO").to_string(index=False)
    )

    print("\nVALIDACION COMPLETADA CORRECTAMENTE")
