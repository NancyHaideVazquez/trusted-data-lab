
"""
Pronosticos finales E1 - Trusted Data Lab.

Banxico:
    ARIMA(3,0,0), intervalo predictivo del modelo.

INEGI:
    Holt-Winters aditivo, intervalo estimado por
    simulacion bootstrap de residuos.

Horizonte:
    Noviembre de 2026 a abril de 2027.

No modifica datos Bronce, Plata ni Oro.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO_ORO = (
    RAIZ / "data" / "oro" / "indicadores_mensuales.csv"
)
SALIDA = RAIZ / "docs" / "E1" / "estadistica"

HORIZONTE = 6
N_SIMULACIONES = 5000
SEMILLA = 2026
NIVEL = 0.95


def cargar_serie(datos, fuente, titulo):
    grupo = datos.loc[datos["fuente"] == fuente].copy()

    # El mes noviembre de 2026 aun no ha concluido.
    if fuente == "banxico":
        grupo = grupo.loc[grupo["periodo"] < "2026-11"]

    grupo["fecha"] = pd.to_datetime(
        grupo["periodo"] + "-01",
        errors="raise",
    )

    if grupo["fecha"].duplicated().any():
        raise ValueError(
            f"{titulo}: se encontraron fechas duplicadas"
        )

    grupo = grupo.sort_values("fecha")

    serie = pd.Series(
        grupo["valor"].to_numpy(dtype=float),
        index=pd.DatetimeIndex(grupo["fecha"]),
        name=titulo,
    ).asfreq("MS")

    if serie.empty or serie.isna().any():
        raise ValueError(
            f"{titulo}: serie vacia o con meses faltantes"
        )

    if not np.isfinite(serie.to_numpy()).all():
        raise ValueError(
            f"{titulo}: hay valores no finitos"
        )

    return serie


def diagnostico_residuos(residuos):
    prueba = acorr_ljungbox(
        residuos,
        lags=[12, 24],
        return_df=True,
    )

    return {
        "lb_p12": float(
            prueba.loc[12, "lb_pvalue"]
        ),
        "lb_p24": float(
            prueba.loc[24, "lb_pvalue"]
        ),
    }


def pronosticar_banxico(serie):
    modelo = ARIMA(
        serie,
        order=(3, 0, 0),
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit()

    prediccion = modelo.get_forecast(
        steps=HORIZONTE
    )

    promedio = prediccion.predicted_mean
    intervalo = prediccion.conf_int(alpha=1 - NIVEL)

    tabla = pd.DataFrame({
        "periodo": promedio.index.strftime("%Y-%m"),
        "pronostico": promedio.to_numpy(),
        "limite_inferior_95": intervalo.iloc[:, 0].to_numpy(),
        "limite_superior_95": intervalo.iloc[:, 1].to_numpy(),
    })

    # Omitir los residuos iniciales del proceso AR.
    diagnostico = diagnostico_residuos(
        modelo.resid.iloc[3:]
    )

    return tabla, diagnostico


def pronosticar_inegi(serie):
    modelo = ExponentialSmoothing(
        serie,
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated",
    ).fit(optimized=True)

    promedio = modelo.forecast(HORIZONTE)

    residuos = np.asarray(
        modelo.resid,
        dtype=float,
    )

    residuos = residuos[np.isfinite(residuos)]
    residuos = residuos - residuos.mean()

    if len(residuos) < 24:
        raise ValueError(
            "No hay suficientes residuos para estimar intervalos"
        )

    # Bootstrap de residuos:
    # Se toman errores historicos con reemplazo.
    # Son intervalos aproximados condicionales al modelo,
    # no incluyen incertidumbre de sus parametros.
    rng = np.random.default_rng(SEMILLA)

    errores = rng.choice(
        residuos,
        size=(N_SIMULACIONES, HORIZONTE),
        replace=True,
    )

    simulaciones = (
        promedio.to_numpy()[None, :] + errores
    )

    inferior = np.quantile(
        simulaciones, 0.025, axis=0
    )
    superior = np.quantile(
        simulaciones, 0.975, axis=0
    )

    tabla = pd.DataFrame({
        "periodo": promedio.index.strftime("%Y-%m"),
        "pronostico": promedio.to_numpy(),
        "limite_inferior_95": inferior,
        "limite_superior_95": superior,
    })

    diagnostico = diagnostico_residuos(
        modelo.resid
    )

    return tabla, diagnostico


def guardar_grafica(serie, tabla, titulo, nombre):
    fechas = pd.to_datetime(
        tabla["periodo"] + "-01"
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    # Mostrar los ultimos tres anos historicos.
    historico = serie.iloc[-36:]

    ax.plot(
        historico.index,
        historico.to_numpy(),
        label="Historico",
        linewidth=2,
    )

    ax.plot(
        fechas,
        tabla["pronostico"].to_numpy(),
        label="Pronostico",
        linewidth=2,
        marker="o",
    )

    ax.fill_between(
        fechas,
        tabla["limite_inferior_95"].to_numpy(),
        tabla["limite_superior_95"].to_numpy(),
        alpha=0.25,
        label="Intervalo estimado 95%",
    )

    ax.set_title(
        f"{titulo} - pronostico a seis meses"
    )
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Valor del indicador")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.tight_layout()

    ruta = SALIDA / f"{nombre}_pronostico_final.png"
    fig.savefig(ruta, dpi=160)
    plt.close(fig)

    return ruta


def ejecutar_serie(datos, nombre, fuente, titulo):
    serie = cargar_serie(datos, fuente, titulo)

    if fuente == "banxico":
        tabla, diagnostico = pronosticar_banxico(
            serie
        )
        modelo_nombre = "ARIMA(3,0,0)"
    else:
        tabla, diagnostico = pronosticar_inegi(
            serie
        )
        modelo_nombre = "Holt-Winters aditivo"

    tabla.insert(0, "fuente", fuente)
    tabla.insert(1, "modelo", modelo_nombre)

    archivo_csv = (
        SALIDA / f"{nombre}_pronostico_final.csv"
    )
    tabla.to_csv(
        archivo_csv,
        index=False,
        encoding="utf-8",
    )

    archivo_png = guardar_grafica(
        serie, tabla, titulo, nombre
    )

    print(f"\n=== {titulo.upper()} ===")
    print("Modelo:", modelo_nombre)
    print("Ultimo mes de entrenamiento:",
          serie.index[-1].strftime("%Y-%m"))
    print("\nPronostico:")
    print(tabla.to_string(index=False))

    print("\nLjung-Box del modelo final:")
    print("p(12):", diagnostico["lb_p12"])
    print("p(24):", diagnostico["lb_p24"])

    if (
        diagnostico["lb_p12"] > 0.05
        and diagnostico["lb_p24"] > 0.05
    ):
        print(
            "No se rechazo ausencia de autocorrelacion "
            "en los rezagos analizados."
        )
    else:
        print(
            "ADVERTENCIA: permanece autocorrelacion "
            "residual significativa."
        )

    print("\nArchivos:")
    print(archivo_csv)
    print(archivo_png)

    return tabla


def main():
    if not ARCHIVO_ORO.is_file():
        raise FileNotFoundError(
            f"No se encontro: {ARCHIVO_ORO}"
        )

    SALIDA.mkdir(parents=True, exist_ok=True)

    datos = pd.read_csv(ARCHIVO_ORO)

    banxico = ejecutar_serie(
        datos,
        nombre="banxico_tiie",
        fuente="banxico",
        titulo="TIIE a 28 dias",
    )

    inegi = ejecutar_serie(
        datos,
        nombre="inegi_inflacion",
        fuente="inegi",
        titulo="Inflacion mensual",
    )

    resumen = pd.concat(
        [banxico, inegi],
        ignore_index=True,
    )

    ruta_resumen = (
        SALIDA / "pronosticos_finales_e1.csv"
    )
    resumen.to_csv(
        ruta_resumen,
        index=False,
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("PRONOSTICOS FINALES GENERADOS")
    print("=" * 60)
    print("Resumen:", ruta_resumen)
    print(
        "Los intervalos son estimaciones bajo "
        "los supuestos de cada modelo."
    )


if __name__ == "__main__":
    main()
