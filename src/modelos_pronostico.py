
"""
Comparacion de cuatro modelos de pronostico para E1.

Modelos:
1. Suavizamiento exponencial simple
2. Holt
3. Holt-Winters aditivo
4. ARIMA con candidatos justificados

Datos:
    data/oro/indicadores_mensuales.csv

Resultados:
    docs/E1/estadistica/

No modifica los archivos de datos originales.
"""

import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import (
    ExponentialSmoothing,
    Holt,
    SimpleExpSmoothing,
)

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO_ORO = (
    RAIZ / "data" / "oro" / "indicadores_mensuales.csv"
)
SALIDA = RAIZ / "docs" / "E1" / "estadistica"

MESES_PRUEBA = 24
PERIODO_ESTACIONAL = 12

SERIES = {
    "banxico_tiie": {
        "fuente": "banxico",
        "titulo": "TIIE a 28 dias",
        "candidatos_arima": [
            (1, 0, 0),
            (3, 0, 0),
            (1, 0, 1),
        ],
    },
    "inegi_inflacion": {
        "fuente": "inegi",
        "titulo": "Inflacion mensual",
        "candidatos_arima": [
            (0, 1, 1),
            (1, 1, 0),
            (2, 1, 1),
        ],
    },
}


def preparar_serie(datos, fuente, titulo):
    grupo = datos.loc[datos["fuente"] == fuente].copy()

    # Noviembre de 2026 esta incompleto.
    if fuente == "banxico":
        grupo = grupo.loc[grupo["periodo"] < "2026-11"]

    grupo["fecha"] = pd.to_datetime(
        grupo["periodo"] + "-01",
        errors="raise",
    )

    if grupo["fecha"].duplicated().any():
        raise ValueError(
            f"{titulo}: existen periodos duplicados"
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
            f"{titulo}: contiene valores no finitos"
        )

    if len(serie) <= MESES_PRUEBA + 24:
        raise ValueError(
            f"{titulo}: datos insuficientes"
        )

    return serie


def calcular_metricas(reales, predichos):
    y = np.asarray(reales, dtype=float)
    p = np.asarray(predichos, dtype=float)

    if len(y) != len(p) or not np.isfinite(p).all():
        raise ValueError("Predicciones invalidas")

    errores = y - p

    mae = float(np.mean(np.abs(errores)))
    rmse = float(np.sqrt(np.mean(errores ** 2)))

    # MAPE requiere denominadores distintos de cero.
    # Para valores negativos el resultado es matematicamente
    # calculable con |y|, pero economicamente delicado.
    validos_mape = np.abs(y) > 1e-8
    n_excluidos = int((~validos_mape).sum())

    if validos_mape.any():
        mape = float(
            100 * np.mean(
                np.abs(
                    errores[validos_mape]
                    / y[validos_mape]
                )
            )
        )
    else:
        mape = np.nan

    # Para evaluar series cercanas a cero, MAE y RMSE
    # seran los indicadores principales.
    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE_pct": mape,
        "MAPE_excluidos": n_excluidos,
        "MAPE_advertencia": (
            "Interpretar con cautela: valores no positivos "
            "o proximos a cero"
            if np.any(y <= 0) or np.any(np.abs(y) < 0.05)
            else ""
        ),
    }


def ajustar_arima(entrenamiento, candidatos):
    """Elige el orden ARIMA por AIC usando SOLO entrenamiento."""

    evaluados = []
    mejor = None
    mejor_aic = float("inf")
    mejor_orden = None

    for orden in candidatos:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter(
                    "ignore", ConvergenceWarning
                )

                modelo = ARIMA(
                    entrenamiento,
                    order=orden,
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                ).fit()

            aic = float(modelo.aic)
            convergio = modelo.mle_retvals.get(
                "converged", True
            )

            evaluados.append({
                "orden": str(orden),
                "AIC": aic,
                "convergio": bool(convergio),
                "error": "",
            })

            # No aceptar modelos sin convergencia.
            if (
                convergio
                and np.isfinite(aic)
                and aic < mejor_aic
            ):
                mejor = modelo
                mejor_aic = aic
                mejor_orden = orden

        except (
            ValueError,
            np.linalg.LinAlgError,
            RuntimeError,
        ) as exc:
            evaluados.append({
                "orden": str(orden),
                "AIC": np.nan,
                "convergio": False,
                "error": str(exc),
            })

    if mejor is None:
        raise RuntimeError(
            "Ningun modelo ARIMA candidato convergio"
        )

    return mejor, mejor_orden, evaluados


def evaluar_serie(nombre, configuracion, datos):
    titulo = configuracion["titulo"]
    fuente = configuracion["fuente"]

    serie = preparar_serie(datos, fuente, titulo)

    entrenamiento = serie.iloc[:-MESES_PRUEBA]
    prueba = serie.iloc[-MESES_PRUEBA:]

    print(f"\n{'=' * 65}")
    print(f"SERIE: {titulo}")
    print(f"{'=' * 65}")
    print(f"Total: {len(serie)} observaciones")
    print(
        f"Entrenamiento: {len(entrenamiento)} "
        f"({entrenamiento.index[0]:%Y-%m} "
        f"a {entrenamiento.index[-1]:%Y-%m})"
    )
    print(
        f"Prueba: {len(prueba)} "
        f"({prueba.index[0]:%Y-%m} "
        f"a {prueba.index[-1]:%Y-%m})"
    )

    pronosticos = {}
    detalles = {}

    # 1. Suavizamiento exponencial simple:
    # nivel sin tendencia o estacionalidad explicitas.
    simple = SimpleExpSmoothing(
        entrenamiento,
        initialization_method="estimated",
    ).fit(optimized=True)

    pronosticos["Simple"] = simple.forecast(
        MESES_PRUEBA
    ).to_numpy()

    detalles["Simple"] = {
        "modelo": simple,
        "parametros": simple.params,
    }

    # 2. Holt: nivel + tendencia aditiva.
    holt = Holt(
        entrenamiento,
        exponential=False,
        initialization_method="estimated",
    ).fit(optimized=True)

    pronosticos["Holt"] = holt.forecast(
        MESES_PRUEBA
    ).to_numpy()

    detalles["Holt"] = {
        "modelo": holt,
        "parametros": holt.params,
    }

    # 3. Holt-Winters:
    # tendencia y estacionalidad aditivas de 12 meses.
    # Se evita el modelo multiplicativo porque la
    # inflacion puede tomar valores negativos.
    hw = ExponentialSmoothing(
        entrenamiento,
        trend="add",
        seasonal="add",
        seasonal_periods=PERIODO_ESTACIONAL,
        initialization_method="estimated",
    ).fit(optimized=True)

    pronosticos["Holt-Winters"] = hw.forecast(
        MESES_PRUEBA
    ).to_numpy()

    detalles["Holt-Winters"] = {
        "modelo": hw,
        "parametros": hw.params,
    }

    # 4. ARIMA: los candidatos proceden del analisis
    # ADF, ACF y PACF ya documentado.
    arima, orden, candidatos = ajustar_arima(
        entrenamiento,
        configuracion["candidatos_arima"],
    )

    pronosticos["ARIMA"] = arima.forecast(
        steps=MESES_PRUEBA
    ).to_numpy()

    detalles["ARIMA"] = {
        "modelo": arima,
        "parametros": {
            "orden": str(orden),
            "AIC": float(arima.aic),
            "coeficientes": arima.params.to_dict(),
        },
    }

    # Guardar comparacion de candidatos ARIMA.
    pd.DataFrame(candidatos).to_csv(
        SALIDA / f"{nombre}_candidatos_arima.csv",
        index=False,
        encoding="utf-8",
    )

    # Evaluar TODOS los modelos sobre los mismos
    # meses que no se utilizaron para entrenar.
    resultados = []

    comparacion = pd.DataFrame({
        "periodo": prueba.index.strftime("%Y-%m"),
        "real": prueba.to_numpy(),
    })

    for modelo, valores in pronosticos.items():
        metricas = calcular_metricas(prueba, valores)

        resultados.append({
            "serie": nombre,
            "modelo": modelo,
            **metricas,
        })

        comparacion[modelo] = valores

    tabla = pd.DataFrame(resultados)
    tabla = tabla.sort_values(
        ["RMSE", "MAE"]
    ).reset_index(drop=True)

    ganador = tabla.iloc[0]["modelo"]

    print("\nComparacion de errores en datos de prueba:")
    print(
        tabla[
            ["modelo", "MAE", "RMSE", "MAPE_pct"]
        ].to_string(index=False)
    )

    print(
        f"\nMejor modelo por RMSE: {ganador}"
    )
    print(f"Orden ARIMA elegido por AIC: {orden}")

    # Guardar salidas numericas.
    tabla.to_csv(
        SALIDA / f"{nombre}_metricas.csv",
        index=False,
        encoding="utf-8",
    )

    comparacion.to_csv(
        SALIDA / f"{nombre}_predicciones_prueba.csv",
        index=False,
        encoding="utf-8",
    )

    # Guardar parametros estimados de los modelos.
    lineas = [
        f"SERIE: {titulo}",
        f"Entrenamiento: {len(entrenamiento)} meses",
        f"Prueba: {len(prueba)} meses",
        "Seleccion final: menor RMSE en prueba",
        f"Mejor modelo: {ganador}",
        "",
        "JUSTIFICACION DE MODELOS:",
        "Simple: nivel sin tendencia ni estacionalidad.",
        "Holt: nivel y tendencia aditiva.",
        (
            "Holt-Winters: tendencia y estacionalidad "
            "aditivas con periodo de 12 meses."
        ),
        (
            "ARIMA: orden candidato evaluado mediante AIC "
            "solo con datos de entrenamiento."
        ),
        "",
    ]

    for modelo, informacion in detalles.items():
        lineas.append(f"=== {modelo} ===")
        lineas.append(
            str(informacion["parametros"])
        )
        lineas.append("")

    lineas.extend([
        "NOTA SOBRE MAPE:",
        (
            "MAPE usa error porcentual absoluto y omite "
            "valores reales con magnitud <= 1e-8."
        ),
        (
            "Cuando los valores son negativos o cercanos "
            "a cero, MAPE puede ser poco interpretable."
        ),
        "MAE y RMSE son la base principal de seleccion.",
    ])

    (
        SALIDA / f"{nombre}_parametros_modelos.txt"
    ).write_text(
        "\n".join(lineas),
        encoding="utf-8",
    )

    # Grafica comparativa en el periodo de prueba.
    fig, ax = plt.subplots(figsize=(13, 6))

    ax.plot(
        entrenamiento.index[-24:],
        entrenamiento.iloc[-24:],
        label="Entrenamiento (ultimos 24 meses)",
        linewidth=2,
    )

    ax.plot(
        prueba.index,
        prueba,
        label="Real (prueba)",
        linewidth=2.5,
    )

    for modelo, valores in pronosticos.items():
        ax.plot(
            prueba.index,
            valores,
            label=modelo,
            linestyle="--",
            alpha=0.85,
        )

    ax.set_title(
        f"{titulo} - Comparacion de pronosticos"
    )
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Valor del indicador")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        SALIDA / f"{nombre}_comparacion_modelos.png",
        dpi=160,
    )
    plt.close(fig)

    print(
        f"\nEvidencias guardadas en: {SALIDA}"
    )

    return tabla


def main():
    if not ARCHIVO_ORO.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ARCHIVO_ORO}"
        )

    SALIDA.mkdir(parents=True, exist_ok=True)

    datos = pd.read_csv(ARCHIVO_ORO)

    requeridas = {
        "fuente", "periodo", "valor"
    }

    if not requeridas.issubset(datos.columns):
        raise ValueError(
            "El archivo Oro no contiene "
            "las columnas requeridas"
        )

    tablas = []

    for nombre, configuracion in SERIES.items():
        resultado = evaluar_serie(
            nombre,
            configuracion,
            datos,
        )
        tablas.append(resultado)

    resumen = pd.concat(
        tablas,
        ignore_index=True,
    )

    resumen.to_csv(
        SALIDA / "comparacion_general_modelos.csv",
        index=False,
        encoding="utf-8",
    )

    print("\n" + "=" * 65)
    print("ANALISIS DE LOS CUATRO MODELOS TERMINADO")
    print("=" * 65)
    print(
        "Se generaron metricas, predicciones, "
        "parametros y graficas."
    )
    print(
        "La seleccion se baso en datos de prueba "
        "no utilizados durante el ajuste."
    )


if __name__ == "__main__":
    main()
