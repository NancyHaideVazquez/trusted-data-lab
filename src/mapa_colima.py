
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


RUTA_PLATA = Path("data/plata/municipios_colima_2026.gpkg")
RUTA_SALIDA = Path("reportes/figuras/mapa_municipios_colima_v2.png")


def generar_mapa():
    """Genera el mapa municipal de Colima con dos municipios destacados."""

    # 1. Verificar que exista la capa Plata.
    if not RUTA_PLATA.is_file():
        raise FileNotFoundError(
            "No existe la capa Plata. "
            "Ejecuta primero guardar_plata()."
        )

    # 2. Cargar los municipios.
    municipios = gpd.read_file(RUTA_PLATA)

    if len(municipios) != 10:
        raise ValueError(
            f"Se esperaban 10 municipios, hay {len(municipios)}."
        )

    if municipios.crs is None:
        raise ValueError("La capa no tiene CRS definido.")

    municipios = municipios.to_crs(epsg=4326)

    # 3. Clasificar los municipios.
    municipios["grupo"] = "Otros municipios"

    municipios.loc[
        municipios["cvegeo"] == "06002", "grupo"
    ] = "Colima"

    municipios.loc[
        municipios["cvegeo"] == "06010", "grupo"
    ] = "Villa de Álvarez"

    colores = {
        "Otros municipios": "#D9E3EA",
        "Colima": "#2878B5",
        "Villa de Álvarez": "#E99A36",
    }

    # 4. Crear la figura.
    fig, ax = plt.subplots(figsize=(12, 9))

    # 5. Dibujar los diez municipios.
    for grupo, color in colores.items():
        seleccion = municipios[
            municipios["grupo"] == grupo
        ]

        if not seleccion.empty:
            seleccion.plot(
                ax=ax,
                color=color,
                edgecolor="#394B59",
                linewidth=0.8,
            )


    # 6. Ajustar la vista al territorio continental.
    # Las geometrías pueden incluir islas alejadas.
    # Utilizamos los polígonos continentales para
    # calcular una extensión cartográfica adecuada.

    from shapely.geometry import Polygon, MultiPolygon

    poligonos = []

    for geometria in municipios.geometry:
        if isinstance(geometria, Polygon):
            partes = [geometria]
        elif isinstance(geometria, MultiPolygon):
            partes = list(geometria.geoms)
        else:
            continue

        for parte in partes:
            # Conservar polígonos de tamaño significativo
            # ubicados en la región continental de Colima.
            centro = parte.representative_point()

            if (
                -105.5 < centro.x < -103.0
                and 18.0 < centro.y < 20.0
                and parte.area > 0.0001
            ):
                poligonos.append(parte)

    if not poligonos:
        raise ValueError(
            "No se encontraron polígonos continentales."
        )

    # Calcular límites únicamente con los polígonos
    # seleccionados, no con todas las islas.
    xmin = min(p.bounds[0] for p in poligonos)
    ymin = min(p.bounds[1] for p in poligonos)
    xmax = max(p.bounds[2] for p in poligonos)
    ymax = max(p.bounds[3] for p in poligonos)

    margen_x = (xmax - xmin) * 0.08
    margen_y = (ymax - ymin) * 0.08

    ax.set_xlim(xmin - margen_x, xmax + margen_x)
    ax.set_ylim(ymin - margen_y, ymax + margen_y)


    # 7. Etiquetar los municipios destacados.
    desplazamientos = {
        "Colima": (40, -25),
        "Villa de Álvarez": (-45, 30),
    }

    for _, municipio in municipios.iterrows():
        if municipio["grupo"] not in desplazamientos:
            continue

        punto = municipio.geometry.representative_point()

        ax.annotate(
            municipio["nomgeo"],
            xy=(punto.x, punto.y),
            xytext=desplazamientos[municipio["grupo"]],
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            ha="center",
            va="center",
            arrowprops={
                "arrowstyle": "-",
                "color": "#394B59",
                "linewidth": 0.8,
            },
            bbox={
                "facecolor": "white",
                "alpha": 0.9,
                "edgecolor": "none",
                "pad": 3,
            },
        )

    # 8. Crear leyenda.
    leyenda = [
        Patch(
            facecolor=color,
            edgecolor="#394B59",
            label=grupo,
        )
        for grupo, color in colores.items()
    ]

    ax.legend(
        handles=leyenda,
        title="Municipios",
        loc="lower left",
        fontsize=10,
        title_fontsize=11,
        frameon=True,
    )

    # 9. Título y formato.
    ax.set_title(
        "Marco Geoestadístico Municipal de Colima (2026)",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    ax.set_axis_off()
    ax.set_aspect("equal")

    fig.text(
        0.5,
        0.035,
        "Fuente: INEGI, Marco Geoestadístico 2026. "
        "Elaboración propia.",
        ha="center",
        fontsize=10,
    )

    # 10. Guardar imagen.
    RUTA_SALIDA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        fig.savefig(
            RUTA_SALIDA,
            dpi=200,
            facecolor="white",
        )
    finally:
        plt.close(fig)

    print("=" * 50)
    print("E2 - MAPA GEOESPACIAL")
    print("=" * 50)
    print("MAPA GENERADO CORRECTAMENTE")
    print("Archivo:", RUTA_SALIDA)
    print("Municipios representados:", len(municipios))
    print("Colima y Villa de Álvarez destacados")
    print("Tamaño en bytes:", RUTA_SALIDA.stat().st_size)

    return RUTA_SALIDA


if __name__ == "__main__":
    generar_mapa()
