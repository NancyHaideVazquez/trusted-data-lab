from pathlib import Path

import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.statespace.sarimax import SARIMAX


def cargar_serie_banxico():
    ruta = Path("data/oro/indicadores_mensuales.csv")

    df = pd.read_csv(ruta)

    datos = df.loc[
        (df["fuente"] == "banxico")
        & (df["serie_id"] == "SF43783")
        & (df["periodo"] < "2026-11")
    ].copy()

    datos["fecha"] = pd.to_datetime(datos["periodo"] + "-01")
    datos = datos.sort_values("fecha")

    serie = pd.Series(
        datos["valor"].to_numpy(dtype=float),
        index=pd.DatetimeIndex(datos["fecha"]),
        name="banxico_tiie"
    ).asfreq("MS")

    return serie


def evaluar_modelo(serie_entrenamiento, order, seasonal_order):
    modelo = SARIMAX(
        serie_entrenamiento,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    ajuste = modelo.fit(disp=False)

    residuos = ajuste.resid.dropna()

    lb = acorr_ljungbox(
        residuos,
        lags=[12, 24],
        return_df=True
    )

    return {
        "order": order,
        "seasonal_order": seasonal_order,
        "convergencia": bool(ajuste.mle_retvals.get("converged", False)),
        "aic": float(ajuste.aic),
        "lb_p12": float(lb.loc[12, "lb_pvalue"]),
        "lb_p24": float(lb.loc[24, "lb_pvalue"]),
    }


def main():
    salida = Path("docs/E1/estadistica")
    salida.mkdir(parents=True, exist_ok=True)

    serie = cargar_serie_banxico()

    # Mantener el mismo esquema de validacion:
    # ultimos 24 meses para prueba
    entrenamiento = serie.iloc[:-24]

    print("BANXICO: evaluacion final de candidatos")
    print("Entrenamiento:", len(entrenamiento), "meses")
    print()

    candidatos = [
        ((3, 0, 0), (0, 0, 0, 0)),
        ((3, 0, 1), (0, 0, 0, 0)),
        ((1, 0, 1), (1, 0, 0, 12)),
        ((2, 0, 1), (1, 0, 0, 12)),
        ((1, 0, 1), (0, 0, 1, 12)),
        ((1, 0, 1), (1, 1, 0, 12)),
        ((1, 0, 1), (0, 1, 1, 12)),
        ((2, 0, 1), (1, 1, 0, 12)),
        ((0, 1, 1), (0, 1, 1, 12)),
        ((1, 1, 1), (0, 1, 1, 12)),
    ]

    resultados = []

    for order, seasonal_order in candidatos:
        try:
            r = evaluar_modelo(
                entrenamiento,
                order,
                seasonal_order
            )
            resultados.append(r)

            print(
                f"ARIMA={r['order']} "
                f"Estacional={r['seasonal_order']}"
            )
            print("Convergencia:", r["convergencia"])
            print("AIC:", round(r["aic"], 3))
            print("Ljung-Box p(12):", round(r["lb_p12"], 6))
            print("Ljung-Box p(24):", round(r["lb_p24"], 6))
            print()

        except Exception as error:  # noqa: BLE001 - Un modelo fallido no debe detener la evaluacion de los demas
            print(
                f"ARIMA={order} Estacional={seasonal_order}"
            )
            print("Error:", error)
            print()

    tabla = pd.DataFrame(resultados)
    tabla = tabla.sort_values(
        by=["lb_p24", "lb_p12", "aic"],
        ascending=[False, False, True]
    ).reset_index(drop=True)

    archivo = salida / "banxico_evaluacion_sarima.csv"
    tabla.to_csv(archivo, index=False)

    print("Resumen guardado en:", archivo)
    print()
    print("Top 10 resultados:")
    print(tabla.to_string(index=False))


if __name__ == "__main__":
    main()