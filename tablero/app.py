
from datetime import timedelta
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
def cargar_datos(ruta_oro):
    municipios = gpd.read_file(RUTA_MAPA)

    municipios = municipios.to_crs(epsg=4326)

    municipios["cvegeo"] = municipios["cvegeo"].astype(str)

    union = pd.read_csv(
        RUTA_UNION,
        dtype={"cvegeo": str, "clave_esperada": str},
    )

    oro = None

    if ruta_oro.is_file():
        oro = pd.read_csv(
            ruta_oro,
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
    municipios, union, oro = cargar_datos(RUTA_ORO)

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

            ultimo = datos.iloc[-1]

            maximo = datos.loc[datos["valor"].idxmax()]
            minimo = datos.loc[datos["valor"].idxmin()]

            cambio = None

            if len(datos) >= 2:
                anterior = datos.iloc[-2]

                if (
                    ultimo["periodo"].to_period("M")
                    == anterior["periodo"].to_period("M") + 1
                ):
                    cambio = (
                        ultimo["valor"] - anterior["valor"]
                    )

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
                f"{ultimo['valor']:.2f} %",
            )

            c4, c5, c6 = st.columns(3)

            c4.metric(
                "Valor máximo",
                f"{maximo['valor']:.2f} %",
            )

            c4.caption(
                maximo["periodo"].strftime("%Y-%m")
            )

            c5.metric(
                "Valor mínimo",
                f"{minimo['valor']:.2f} %",
            )

            c5.caption(
                minimo["periodo"].strftime("%Y-%m")
            )

            c6.metric(
                "Cambio mensual",
                f"{cambio:+.2f} pp"
                if cambio is not None
                else "No disponible",
            )

            c6.caption(
                "Respecto al mes anterior seleccionado"
            )

            st.caption(
                f"Unidad: {ultimo['unidad']} | "
                f"Cobertura: {ultimo['cobertura']} | "
                "pp = puntos porcentuales."
            )


            st.subheader("Evolución histórica y tendencia")

            ventana = st.selectbox(
                "Periodo del promedio móvil",
                options=[3, 6, 12],
                index=2,
                format_func=lambda n: f"{n} meses",
                key="ventana_promedio_movil",
            )

            serie = (
                datos.set_index("periodo")["valor"]
                .sort_index()
                .asfreq("MS")
            )

            promedio_movil = serie.rolling(
                window=ventana,
                min_periods=ventana,
            ).mean()

            grafica = go.Figure()

            grafica.add_trace(
                go.Scatter(
                    x=serie.index,
                    y=serie,
                    mode="lines+markers"
                    if len(serie) <= 24
                    else "lines",
                    name="Valor mensual",
                    line={
                        "color": "#60a5fa",
                        "width": 1.8,
                    },
                    connectgaps=False,
                )
            )

            grafica.add_trace(
                go.Scatter(
                    x=promedio_movil.index,
                    y=promedio_movil,
                    mode="lines",
                    name=f"Promedio móvil ({ventana} meses)",
                    line={
                        "color": "#f59e0b",
                        "width": 3,
                    },
                    connectgaps=False,
                )
            )

            grafica.update_layout(
                title=indicador,
                xaxis_title="Periodo",
                xaxis_tickformat="%Y-%m",
                yaxis_title=ultimo["unidad"].capitalize(),
                hovermode="x unified",
                height=450,
                legend={
                    "orientation": "h",
                    "y": 1.12,
                },
            )

            if len(serie) == 1:
                grafica.update_xaxes(
                    range=[
                        pd.Timestamp(serie.index[0]).date() - timedelta(days=15),
                        pd.Timestamp(serie.index[0]).date() + timedelta(days=15),
                    ],
                    dtick="M1",
                )


            st.plotly_chart(
                grafica,
                width="stretch",
            )

            st.caption(
                "La línea azul muestra los valores originales. "
                "La línea naranja suaviza las fluctuaciones "
                "para facilitar la identificación de tendencias."
            )

            tendencias = promedio_movil.dropna()

            if len(tendencias) >= 2:
                diferencia = (
                    tendencias.iloc[-1]
                    - tendencias.iloc[0]
                )

                if diferencia > 0.005:
                    direccion = "ascendente"
                elif diferencia < -0.005:
                    direccion = "descendente"
                else:
                    direccion = "estable"

                st.info(
                    f"El promedio móvil presenta un cambio "
                    f"neto {direccion} de "
                    f"{diferencia:+.2f} puntos porcentuales "
                    "entre el primer y el último promedio "
                    "disponible del periodo seleccionado."
                )

            elif tendencias.empty:
                st.warning(
                    f"Se necesitan al menos {ventana} meses "
                    "consecutivos para calcular el promedio móvil."
                )


            st.divider()

            st.subheader("Comparación económica anual")

            anual = (
                datos.assign(
                    anio=datos["periodo"].dt.year
                )
                .groupby("anio", as_index=False)
                .agg(
                    promedio=("valor", "mean"),
                    minimo=("valor", "min"),
                    maximo=("valor", "max"),
                    meses=("periodo", "nunique"),
                )
            )

            anual["anio"] = anual["anio"].astype(str)

            anual["cobertura_anual"] = (
                anual["meses"]
                .map(
                    lambda n: "12 meses"
                    if n == 12
                    else "Año parcial"
                )
            )

            figura_anual = px.bar(
                anual,
                x="anio",
                y="promedio",
                color="cobertura_anual",
                text_auto=".2f",
                hover_data={
                    "meses": True,
                    "minimo": ":.2f",
                    "maximo": ":.2f",
                },
                color_discrete_map={
                    "12 meses": "#2563eb",
                    "Año parcial": "#f59e0b",
                },
                labels={
                    "anio": "Año",
                    "promedio": "Promedio mensual (%)",
                    "meses": "Meses disponibles",
                    "minimo": "Valor mínimo",
                    "maximo": "Valor máximo",
                    "cobertura_anual": "Cobertura",
                },
            )

            figura_anual.update_layout(
                height=450,
                xaxis_type="category",
                xaxis_categoryorder="array",
                xaxis_categoryarray=anual["anio"].tolist(),
                yaxis_title=ultimo["unidad"].capitalize(),
                legend_title_text="Cobertura anual",
            )

            st.plotly_chart(
                figura_anual,
                width="stretch",
                key="comparacion_anual",
            )

            mayor = anual.loc[
                anual["promedio"].idxmax()
            ]

            menor = anual.loc[
                anual["promedio"].idxmin()
            ]

            st.info(
                f"El año {mayor['anio']} presenta el mayor "
                f"promedio observado: "
                f"{mayor['promedio']:.2f} %, "
                f"con {mayor['meses']} meses disponibles. "
                f"El menor corresponde a {menor['anio']}, "
                f"con {menor['promedio']:.2f} % "
                f"y {menor['meses']} meses disponibles."
            )

            st.caption(
                "Las barras azules contienen 12 observaciones "
                "mensuales y las naranjas corresponden a años "
                "parciales. Los promedios no representan "
                "inflación anual acumulada. El último mes "
                "capturado también puede estar incompleto."
            )


            st.divider()

            st.subheader("Variaciones mensuales")

            variaciones = (
                serie.diff()
                .dropna()
                .rename("variacion")
                .reset_index()
            )

            if variaciones.empty:

                st.warning(
                    "Se necesitan al menos dos meses "
                    "consecutivos para calcular variaciones."
                )

            else:

                variaciones["direccion"] = (
                    variaciones["variacion"].map(
                        lambda v: "Aumento" if v > 0
                        else "Disminución" if v < 0
                        else "Sin cambio"
                    )
                )

                figura_variaciones = px.bar(
                    variaciones,
                    x="periodo",
                    y="variacion",
                    color="direccion",
                    color_discrete_map={
                        "Aumento": "#16a34a",
                        "Disminución": "#dc2626",
                        "Sin cambio": "#94a3b8",
                    },
                    labels={
                        "periodo": "Periodo",
                        "variacion": "Cambio mensual (pp)",
                        "direccion": "Dirección",
                    },
                    hover_data={
                        "variacion": ":.2f",
                    },
                )

                figura_variaciones.add_hline(
                    y=0,
                    line_color="#94a3b8",
                )

                figura_variaciones.update_layout(
                    height=450,
                    barmode="overlay",
                    hovermode="x unified",
                )

                st.plotly_chart(
                    figura_variaciones,
                    width="stretch",
                    key="variaciones_mensuales",
                )

                aumentos = int(
                    (variaciones["variacion"] > 0).sum()
                )

                disminuciones = int(
                    (variaciones["variacion"] < 0).sum()
                )

                sin_cambio = int(
                    (variaciones["variacion"] == 0).sum()
                )

                v1, v2, v3 = st.columns(3)

                v1.metric("Meses con aumento", aumentos)

                v2.metric(
                    "Meses con disminución",
                    disminuciones,
                )

                v3.metric(
                    "Meses sin cambio",
                    sin_cambio,
                )

                mayor_cambio = variaciones.loc[
                    variaciones["variacion"].abs().idxmax()
                ]

                st.info(
                    "El mayor cambio mensual en magnitud "
                    "se presentó en "
                    f"{mayor_cambio['periodo']:%Y-%m}, "
                    "con una variación de "
                    f"{mayor_cambio['variacion']:+.2f} "
                    "puntos porcentuales."
                )

                st.caption(
                    "Cada barra representa la diferencia "
                    "respecto al mes anterior. "
                    "Verde indica aumento y rojo disminución. "
                    "Los colores no implican que el cambio "
                    "sea favorable o desfavorable."
                )


            st.divider()

            st.subheader("Mapa de calor histórico")

            meses = [
                "Ene", "Feb", "Mar", "Abr",
                "May", "Jun", "Jul", "Ago",
                "Sep", "Oct", "Nov", "Dic",
            ]

            datos_calor = datos.assign(
                anio=datos["periodo"].dt.year,
                mes=datos["periodo"].dt.month,
            )

            matriz = datos_calor.pivot_table(
                index="anio",
                columns="mes",
                values="valor",
                aggfunc="mean",
            )

            matriz = matriz.reindex(
                columns=range(1, 13)
            ).sort_index()

            matriz.columns = meses

            figura_calor = go.Figure(
                data=go.Heatmap(
                    z=matriz.to_numpy(),
                    x=meses,
                    y=matriz.index.astype(str),
                    colorscale="Viridis",
                    texttemplate="%{z:.2f}",
                    hoverongaps=False,
                    colorbar={
                        "title": ultimo["unidad"],
                    },
                    hovertemplate=(
                        "Año: %{y}<br>"
                        "Mes: %{x}<br>"
                        "Valor: %{z:.2f} %"
                        "<extra></extra>"
                    ),
                )
            )

            figura_calor.update_layout(
                height=max(
                    450,
                    len(matriz) * 28 + 100,
                ),
                xaxis_title="Mes",
                yaxis_title="Año",
                yaxis={
                    "type": "category",
                    "autorange": "reversed",
                },
                margin={
                    "l": 50,
                    "r": 30,
                    "t": 30,
                    "b": 40,
                },
            )

            st.plotly_chart(
                figura_calor,
                width="stretch",
                key="mapa_calor_historico",
            )

            st.info(
                "El valor más alto del periodo corresponde a "
                f"{maximo['periodo']:%Y-%m}, "
                f"con {maximo['valor']:.2f} %. "
                "El valor más bajo corresponde a "
                f"{minimo['periodo']:%Y-%m}, "
                f"con {minimo['valor']:.2f} %."
            )

            st.caption(
                "Los colores oscuros representan valores "
                "más bajos y los claros valores más altos. "
                "Las celdas vacías indican meses sin datos "
                "dentro del periodo seleccionado. "
                "No representan valores iguales a cero."
            )


            st.divider()

            st.subheader("Relación entre inflación y TIIE")

            st.caption(
                "Comparación de los indicadores nacionales "
                "durante los meses coincidentes."
            )

            inflacion = oro.loc[
                oro["serie_id"] == "910402",
                ["periodo", "valor"],
            ].rename(
                columns={"valor": "inflacion"}
            )

            tiie = oro.loc[
                oro["serie_id"] == "SF43783",
                ["periodo", "valor"],
            ].rename(
                columns={"valor": "tiie"}
            )

            relacionados = inflacion.merge(
                tiie,
                on="periodo",
                how="inner",
                validate="one_to_one",
            )

            relacionados = relacionados.loc[
                relacionados["periodo"].between(
                    datos["periodo"].min(),
                    datos["periodo"].max(),
                )
            ].dropna(
                subset=["inflacion", "tiie"]
            ).sort_values("periodo").copy()

            if (
                len(relacionados) < 3
                or relacionados["inflacion"].nunique() < 2
                or relacionados["tiie"].nunique() < 2
            ):

                st.warning(
                    "No existen suficientes valores "
                    "coincidentes y distintos para "
                    "calcular la correlación."
                )

            else:

                correlacion = relacionados[
                    "inflacion"
                ].corr(
                    relacionados["tiie"]
                )

                magnitud = abs(correlacion)

                if magnitud >= 0.70:
                    intensidad = "fuerte"
                elif magnitud >= 0.30:
                    intensidad = "moderada"
                else:
                    intensidad = "débil"

                if magnitud < 0.005:
                    direccion_corr = "prácticamente nula"
                elif correlacion > 0:
                    direccion_corr = f"positiva {intensidad}"
                else:
                    direccion_corr = f"negativa {intensidad}"

                r1, r2, r3 = st.columns(3)

                r1.metric(
                    "Meses comparados",
                    len(relacionados),
                )

                r2.metric(
                    "Correlación de Pearson",
                    f"{correlacion:.3f}",
                )

                r3.metric(
                    "Tipo de relación",
                    direccion_corr.capitalize(),
                )

                relacionados["mes"] = (
                    relacionados["periodo"]
                    .dt.strftime("%Y-%m")
                )

                relacionados["anio"] = (
                    relacionados["periodo"].dt.year
                )

                figura_correlacion = px.scatter(
                    relacionados,
                    x="inflacion",
                    y="tiie",
                    color="anio",
                    color_continuous_scale="Viridis",
                    hover_name="mes",
                    hover_data={
                        "inflacion": ":.2f",
                        "tiie": ":.2f",
                    },
                    labels={
                        "inflacion": (
                            "Inflación mensual de servicios (%)"
                        ),
                        "tiie": (
                            "TIIE a 28 días (% anual)"
                        ),
                        "anio": "Año",
                    },
                )

                figura_correlacion.update_traces(
                    marker={
                        "size": 9,
                        "opacity": 0.75,
                    }
                )

                figura_correlacion.update_layout(
                    height=500,
                )

                st.plotly_chart(
                    figura_correlacion,
                    width="stretch",
                    key="correlacion_economica",
                )

                st.info(
                    f"Se observa una relación "
                    f"{direccion_corr}, con un coeficiente "
                    f"de Pearson de {correlacion:.3f}, "
                    f"a partir de {len(relacionados)} "
                    "meses coincidentes."
                )

                st.caption(
                    "Cada punto representa un mes. "
                    "La escala de colores identifica el año. "
                    "La clasificación de intensidad es "
                    "orientativa. Correlación no implica "
                    "causalidad. Las tendencias temporales "
                    "pueden influir en el resultado."
                )

                st.caption(
                    "Fuentes: INEGI, indicador 910402; "
                    "Banco de México, serie SF43783. "
                    "La inflación es una variación mensual "
                    "y la TIIE es una tasa anual promediada "
                    "por mes. Ambas tienen cobertura nacional."
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
