"""ANOVA del experimento factorial completo 2^4 de E2."""

from pathlib import Path

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import shapiro


RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "data/reportes/experimento_factorial_2_4_completo.csv"
SALIDA = RAIZ / "data/reportes/anova_factorial_2_4_completo.csv"


def main():
    datos = pd.read_csv(ENTRADA)

    if len(datos) != 32:
        raise ValueError("Se esperaban 32 corridas.")

    modelo = smf.ols(
        "tiempo_ms ~ A * B * C * D",
        data=datos,
    ).fit()

    anova = sm.stats.anova_lm(modelo, typ=2)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    anova.to_csv(SALIDA, index_label="termino")

    print("===== ANOVA FACTORIAL COMPLETO 2^4 =====")
    print(anova.round(6).to_string())

    print("\n===== EFECTOS PRINCIPALES =====")
    for factor in ("A", "B", "C", "D"):
        efecto = (
            datos.loc[datos[factor] == 1, "tiempo_ms"].mean()
            - datos.loc[datos[factor] == -1, "tiempo_ms"].mean()
        )
        print(f"{factor}: {efecto:+.4f} ms")

    print("\n===== DIAGNOSTICO =====")
    print(f"R2: {modelo.rsquared:.4f}")
    print(f"R2 ajustado: {modelo.rsquared_adj:.4f}")
    print(f"Desviacion residual: {modelo.mse_resid**0.5:.4f} ms")

    _, p = shapiro(modelo.resid)
    print(f"Shapiro-Wilk p: {p:.6f}")

    print("\nResultados guardados en:", SALIDA)


if __name__ == "__main__":
    main()
