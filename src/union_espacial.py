
from pathlib import Path

import geopandas as gpd

RUTA_PLATA = Path(
    "data/plata/municipios_colima_2026.gpkg"
)

RUTA_RESULTADO = Path(
    "data/reportes/union_espacial_municipios_e2.csv"
)


def cargar_poligonos():
    """Carga los municipios de la capa Plata."""
    municipios = gpd.read_file(RUTA_PLATA)

    if municipios.crs is None:
        raise ValueError("La capa no tiene CRS.")

    if len(municipios) != 10:
        raise ValueError("Se esperaban 10 municipios.")

    return municipios.to_crs(epsg=4326)


def generar_puntos(municipios):
    """Genera referencias cartograficas interiores."""
    puntos = municipios[
        [
            "cvegeo",
            "archivo_origen",
            "sha256_origen",
            "geometry",
        ]
    ].copy()

    puntos = puntos.rename(
        columns={"cvegeo": "clave_esperada"}
    )

    puntos["geometry"] = (
        municipios.geometry.representative_point()
    )

    puntos["tipo_punto"] = "Referencia cartografica derivada"

    return puntos


def realizar_union_espacial():
    """Asigna cada punto a su municipio por ubicacion."""
    municipios = cargar_poligonos()

    puntos = generar_puntos(municipios)

    resultado = gpd.sjoin(
        puntos,
        municipios[["cvegeo", "nomgeo", "geometry"]],
        how="left",
        predicate="within",
    )

    if len(resultado) != len(puntos):
        raise ValueError("Existen asignaciones multiples.")

    resultado["asignacion_correcta"] = (
        resultado["clave_esperada"] == resultado["cvegeo"]
    )

    resultado["longitud"] = resultado.geometry.x
    resultado["latitud"] = resultado.geometry.y

    if resultado["cvegeo"].isna().any():
        raise ValueError("Existen puntos sin municipio.")

    if not resultado["asignacion_correcta"].all():
        raise ValueError("Existen asignaciones incorrectas.")

    return resultado


def guardar_resultado():
    """Guarda la evidencia de la union espacial."""
    resultado = realizar_union_espacial()

    RUTA_RESULTADO.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    columnas = [
        "clave_esperada",
        "cvegeo",
        "nomgeo",
        "longitud",
        "latitud",
        "tipo_punto",
        "asignacion_correcta",
        "archivo_origen",
        "sha256_origen",
    ]

    resultado[columnas].to_csv(
        RUTA_RESULTADO,
        index=False,
        encoding="utf-8",
    )

    print("=" * 60)
    print("E2 - UNION ESPACIAL CON GEOPANDAS")
    print("=" * 60)

    print("Puntos procesados:", len(resultado))

    print(
        "Asignaciones correctas:",
        resultado["asignacion_correcta"].sum(),
    )

    print(
        "Puntos sin municipio:",
        resultado["cvegeo"].isna().sum(),
    )

    print(
        resultado[
            [
                "cvegeo",
                "nomgeo",
                "asignacion_correcta",
            ]
        ].to_string(index=False)
    )

    print("\nArchivo generado:", RUTA_RESULTADO)

    return resultado


if __name__ == "__main__":
    guardar_resultado()
