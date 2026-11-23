
import geopandas as gpd

from src.geoespacial import (
    ARCHIVO_ORIGINAL,
    cargar_metadatos,
    cargar_municipios,
    preparar_plata,
    verificar_integridad,
)


def test_archivo_bronce_existe():
    """El archivo original debe estar disponible."""
    assert ARCHIVO_ORIGINAL.is_file()


def test_integridad_sha256():
    """El archivo original debe coincidir con sus metadatos."""
    metadatos = cargar_metadatos()
    hash_verificado = verificar_integridad(metadatos)

    assert hash_verificado == metadatos["sha256"].upper()


def test_cantidad_municipios():
    """Colima debe tener exactamente 10 municipios."""
    municipios, _, _ = cargar_municipios()

    assert len(municipios) == 10


def test_claves_municipales_unicas():
    """No debe haber claves municipales repetidas."""
    municipios, _, _ = cargar_municipios()

    assert municipios["CVEGEO"].is_unique
    assert municipios["CVEGEO"].notna().all()


def test_colima_y_villa_de_alvarez():
    """Los dos municipios de interés deben estar presentes."""
    municipios, _, _ = cargar_municipios()

    claves = set(municipios["CVEGEO"].astype(str))

    assert {"06002", "06010"}.issubset(claves)


def test_geometrias_validas():
    """Todas las geometrías deben ser válidas."""
    municipios, _, _ = cargar_municipios()

    assert municipios.geometry.notna().all()
    assert not municipios.geometry.is_empty.any()
    assert municipios.geometry.is_valid.all()


def test_transformacion_epsg4326():
    """La capa Plata debe usar coordenadas EPSG:4326."""
    plata = preparar_plata()

    assert isinstance(plata, gpd.GeoDataFrame)
    assert plata.crs.to_epsg() == 4326
    assert len(plata) == 10


def test_trazabilidad_bronce():
    """Cada municipio debe conservar la procedencia del archivo."""
    plata = preparar_plata()
    metadatos = cargar_metadatos()

    assert plata["archivo_origen"].notna().all()
    assert (
        plata["archivo_origen"] == metadatos["ruta_bronce"]
    ).all()

    assert plata["sha256_origen"].notna().all()
    assert (
        plata["sha256_origen"] == metadatos["sha256"].upper()
    ).all()

    assert plata["procesado_utc"].notna().all()
