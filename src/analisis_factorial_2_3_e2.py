"""Analisis estadistico ANOVA del experimento factorial 2^3 de E2."""

from pathlib import Path

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import shapiro

RAIZ = Path(__file__).resolve().parent.parent

ENTRADA = RAIZ / "data/reportes/experimento_factorial_e2_confirmacion.csv"
SALIDA = RAIZ / "data/reportes/anova_factorial_2_3.csv"


def main():
    datos = pd.read_csv(ENTRADA)

    if len(datos) != 16:
        raise ValueError("Se esperaban 16 corridas.")

    tratamientos = datos.groupby(["A", "B", "C"]).size()

    if len(tratamientos) != 8 or not (tratamientos == 2).all():
        raise ValueError("El diseño no tiene 8 tratamientos con 2 replicas.")

    modelo = smf.ols(
        "tiempo_ms ~ A * B * C",
        data=datos,
    ).fit()

    anova = sm.stats.anova_lm(modelo, typ=2)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    anova.to_csv(SALIDA, index_label="termino")

    print("===== ANOVA FACTORIAL COMPLETO 2^3 =====")
    print(anova.round(8).to_string())

    print("\n===== EFECTOS PRINCIPALES =====")

    nombres = {
        "A": "Cantidad de registros",
        "B": "Trazabilidad",
        "C": "Validacion Pandera",
    }

    for factor, nombre in nombres.items():
        efecto = (
            datos.loc[datos[factor] == 1, "tiempo_ms"].mean()
            - datos.loc[datos[factor] == -1, "tiempo_ms"].mean()
        )

        p = anova.loc[factor, "PR(>F)"]

        print(
            f"{factor} ({nombre}): "
            f"{efecto:+.4f} ms | p={p:.6f}"
        )

    print("\n===== DIAGNOSTICO DEL MODELO =====")
    print(f"R2: {modelo.rsquared:.4f}")
    print(f"R2 ajustado: {modelo.rsquared_adj:.4f}")
    print(f"Desviacion residual: {modelo.mse_resid**0.5:.4f} ms")

    w, p = shapiro(modelo.resid)

    print(f"Shapiro-Wilk W: {w:.6f}")
    print(f"Shapiro-Wilk p: {p:.6f}")

    print("\n===== EFECTOS SIGNIFICATIVOS =====")

    significativos = anova[anova["PR(>F)"] < 0.05]

    if significativos.empty:
        print("No se encontraron efectos significativos.")
    else:
        print(significativos[["F", "PR(>F)"]].to_string())

    print("\nResultados guardados en:", SALIDA)
    print("ANALISIS COMPLETADO")


if __name__ == "__main__":
    main()
