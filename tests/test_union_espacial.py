
from src.union_espacial import (
    cargar_poligonos,
    generar_puntos,
    realizar_union_espacial,
)


def test_cantidad_poligonos():
    municipios = cargar_poligonos()

    assert len(municipios) == 10


def test_crs_poligonos():
    municipios = cargar_poligonos()

    assert municipios.crs.to_epsg() == 4326


def test_generacion_puntos():
    municipios = cargar_poligonos()
    puntos = generar_puntos(municipios)

    assert len(puntos) == 10
    assert puntos.geometry.geom_type.eq("Point").all()
    assert not puntos.geometry.is_empty.any()


def test_union_espacial_completa():
    resultado = realizar_union_espacial()

    assert len(resultado) == 10


def test_sin_puntos_no_asignados():
    resultado = realizar_union_espacial()

    assert resultado["cvegeo"].notna().all()


def test_asignaciones_correctas():
    resultado = realizar_union_espacial()

    assert resultado["asignacion_correcta"].all()


def test_claves_municipales_unicas():
    resultado = realizar_union_espacial()

    assert resultado["cvegeo"].is_unique


def test_municipios_objetivo():
    resultado = realizar_union_espacial()

    claves = set(resultado["cvegeo"].astype(str))

    assert {"06002", "06010"}.issubset(claves)


def test_trazabilidad_union_espacial():
    resultado = realizar_union_espacial()

    assert resultado["archivo_origen"].notna().all()
    assert resultado["sha256_origen"].notna().all()

    assert resultado["sha256_origen"].str.len().eq(64).all()


def test_coordenadas_validas():
    resultado = realizar_union_espacial()

    assert resultado["longitud"].between(-180, 180).all()
    assert resultado["latitud"].between(-90, 90).all()
