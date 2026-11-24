
from pathlib import Path

import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]

RUTA_MAPA = RAIZ / "data/plata/municipios_colima_2026.gpkg"

RUTA_ORO = RAIZ / "data/oro/indicadores_mensuales_e2.csv"

RUTA_UNION = (
    RAIZ / "data/reportes/union_espacial_municipios_e2.csv"
)

st.set_page_config(
    page_title="Observatorio de Vivienda y Costos de Colima",
    page_icon="📊",
    layout="wide",
)

st.title("Observatorio de Vivienda y Costos de Colima")

st.caption(
    "Trusted Data Lab | Entrega E2 | "
    "Ingeniería de Datos, Estadística y Calidad"
)

st.markdown(
    """
    Este observatorio integra información económica nacional
    y datos geoespaciales del estado de Colima, con énfasis
    territorial en Colima y Villa de Álvarez.
    """
)


@st.cache_data
def cargar_datos():
    municipios = gpd.read_file(RUTA_MAPA)

    municipios = municipios.to_crs(epsg=4326)

    municipios["cvegeo"] = municipios["cvegeo"].astype(str)

    union = pd.read_csv(
        RUTA_UNION,
        dtype={"cvegeo": str, "clave_esperada": str},
    )

    oro = None

    if RUTA_ORO.is_file():
        oro = pd.read_csv(
            RUTA_ORO,
            dtype={"serie_id": str},
        )

        oro["periodo"] = pd.to_datetime(
            oro["periodo"],
            errors="raise",
        )

        oro["valor"] = pd.to_numeric(
            oro["valor"],
            errors="raise",
        )

    return municipios, union, oro


try:
    municipios, union, oro = cargar_datos()

except (OSError, ValueError) as error:
    st.error(f"No fue posible cargar los datos: {error}")
    st.stop()


# Indicadores generales

col1, col2, col3, col4 = st.columns(4)

col1.metric("Municipios", len(municipios))

col2.metric(
    "Registros económicos",
    len(oro) if oro is not None else "No disponible",
)

col3.metric(
    "Asignaciones espaciales",
    int(union["asignacion_correcta"].sum()),
)

col4.metric(
    "Asignaciones correctas",
    f"{union['asignacion_correcta'].mean():.0%}",
)

st.divider()


# Filtros territoriales

st.sidebar.header("Filtros del observatorio")

opciones = ["Todos"] + sorted(
    municipios["nomgeo"].unique().tolist()
)

municipio = st.sidebar.selectbox(
    "Seleccionar municipio",
    opciones,
)

if municipio == "Todos":
    mapa_datos = municipios.copy()
    puntos = union.copy()

else:
    mapa_datos = municipios[
        municipios["nomgeo"] == municipio
    ].copy()

    puntos = union[
        union["nomgeo"] == municipio
    ].copy()


# Secciones del tablero

tab_mapa, tab_economia, tab_calidad, tab_linaje = st.tabs(
    [
        "Mapa territorial",
        "Indicadores económicos",
        "Calidad de datos",
        "Trazabilidad",
    ]
)


# MAPA TERRITORIAL

with tab_mapa:

    st.subheader("Marco Geoestadístico de Colima")

    mapa_datos["clasificacion"] = "Otros municipios"

    mapa_datos.loc[
        mapa_datos["cvegeo"] == "06002",
        "clasificacion",
    ] = "Colima"

    mapa_datos.loc[
        mapa_datos["cvegeo"] == "06010",
        "clasificacion",
    ] = "Villa de Álvarez"

    geojson = mapa_datos.__geo_interface__

    figura = px.choropleth_map(
        mapa_datos,
        geojson=geojson,
        locations="cvegeo",
        featureidkey="properties.cvegeo",
        color="clasificacion",
        hover_name="nomgeo",
        hover_data=["cvegeo"],
        color_discrete_map={
            "Colima": "#2563eb",
            "Villa de Álvarez": "#f59e0b",
            "Otros municipios": "#94a3b8",
        },
        center={
            "lat": 19.20,
            "lon": -103.85,
        },
        zoom=8,
        map_style="carto-positron",
        opacity=0.65,
        height=600,
    )

    figura.add_trace(
        go.Scattermap(
            lat=puntos["latitud"],
            lon=puntos["longitud"],
            mode="markers",
            text=puntos["nomgeo"],
            name="Puntos representativos",
            marker={
                "size": 12,
                "color": "#172554",
            },
            hovertemplate=(
                "%{text}<br>"
                "Latitud: %{lat:.5f}<br>"
                "Longitud: %{lon:.5f}"
                "<extra></extra>"
            ),
        )
    )

    figura.update_layout(
        margin={
            "r": 0,
            "t": 0,
            "l": 0,
            "b": 0,
        },
        legend_title_text="Municipios",
    )

    st.plotly_chart(
        figura,
        width="stretch",
    )

    st.caption(
        "Fuente: INEGI, Marco Geoestadístico 2026. "
        "Los puntos se derivan de los polígonos municipales."
    )

    st.info(
        "Los puntos representan referencias cartográficas. "
        "No corresponden a viviendas, establecimientos "
        "ni observaciones económicas individuales."
    )

    st.subheader("Municipios seleccionados")

    st.dataframe(
        puntos[
            [
                "cvegeo",
                "nomgeo",
                "longitud",
                "latitud",
                "asignacion_correcta",
            ]
        ],
        width="stretch",
        hide_index=True,
    )


# INDICADORES ECONOMICOS

with tab_economia:

    st.subheader("Comportamiento histórico nacional")

    st.info(
        "Las series económicas tienen cobertura nacional. "
        "El filtro municipal no modifica sus valores "
        "ni representa estadísticas municipales."
    )

    if oro is None:

        st.warning(
            "La capa Oro E2 no está disponible localmente. "
            "Debe generarse mediante el pipeline del proyecto."
        )

    else:

        indicadores = sorted(
            oro["indicador"].unique().tolist()
        )

        indicador = st.selectbox(
            "Indicador económico",
            indicadores,
        )

        datos = oro[
            oro["indicador"] == indicador
        ].copy()

        fecha_min = datos["periodo"].min().date()
        fecha_max = datos["periodo"].max().date()

        periodo = st.date_input(
            "Periodo de análisis",
            value=(fecha_min, fecha_max),
            min_value=fecha_min,
            max_value=fecha_max,
        )

        if len(periodo) == 2:

            datos = datos[
                datos["periodo"].between(
                    pd.Timestamp(periodo[0]),
                    pd.Timestamp(periodo[1]),
                )
            ]

        datos = datos.sort_values("periodo")

        if datos.empty:

            st.warning(
                "No existen registros en el periodo seleccionado."
            )

        else:

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Observaciones",
                len(datos),
            )

            c2.metric(
                "Promedio del periodo",
                f"{datos['valor'].mean():.2f} %",
            )

            c3.metric(
                "Último valor seleccionado",
                f"{datos.iloc[-1]['valor']:.2f} %",
            )

            grafica = px.line(
                datos,
                x="periodo",
                y="valor",
                color="fuente",
                title=indicador,
                labels={
                    "periodo": "Periodo",
                    "valor": "Porcentaje",
                    "fuente": "Fuente",
                },
            )

            st.plotly_chart(
                grafica,
                width="stretch",
            )

            st.dataframe(
                datos[
                    [
                        "periodo",
                        "fuente",
                        "indicador",
                        "valor",
                        "unidad",
                        "cobertura",
                    ]
                ],
                width="stretch",
                hide_index=True,
            )


# CALIDAD DE DATOS

with tab_calidad:

    st.subheader("Validación geoespacial")

    validas = int(
        municipios.geometry.is_valid.sum()
    )

    correctas = int(
        union["asignacion_correcta"].sum()
    )

    sin_asignar = int(
        union["cvegeo"].isna().sum()
    )

    calidad = pd.DataFrame(
        {
            "Indicador": [
                "Geometrías válidas",
                "Asignaciones correctas",
                "Puntos sin municipio",
                "Claves municipales duplicadas",
                "Sistema de coordenadas",
            ],
            "Resultado": [
                f"{validas}/{len(municipios)}",
                f"{correctas}/{len(union)}",
                str(sin_asignar),
                str(
                    municipios["cvegeo"]
                    .duplicated()
                    .sum()
                ),
                str(municipios.crs),
            ],
        }
    )

    st.dataframe(
        calidad,
        width="stretch",
        hide_index=True,
    )

    st.subheader("Evidencia de unión espacial")

    st.dataframe(
        union,
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        "Descargar evidencia geoespacial CSV",
        data=union.to_csv(index=False).encode("utf-8-sig"),
        file_name="union_espacial_municipios_e2.csv",
        mime="text/csv",
    )


# TRAZABILIDAD

with tab_linaje:

    st.subheader("Procedencia geoespacial")

    st.dataframe(
        mapa_datos[
            [
                "cvegeo",
                "nomgeo",
                "fuente",
                "edicion",
                "archivo_origen",
                "sha256_origen",
                "procesado_utc",
            ]
        ],
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "La fecha de procesamiento no equivale "
        "a la fecha original de ingesta."
    )

    st.subheader("Linaje económico: Oro a Bronce")

    if oro is not None:

        st.dataframe(
            oro[
                [
                    "periodo",
                    "fuente",
                    "serie_id",
                    "archivo_origen",
                    "fecha_ingesta_utc",
                ]
            ],
            width="stretch",
            hide_index=True,
        )

    else:

        st.warning("Capa Oro E2 no disponible.")


st.divider()

st.caption(
    "Trusted Data Lab | Observatorio de Vivienda "
    "y Costos de Colima | E2"
)
