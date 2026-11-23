from pathlib import Path

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import shapiro

RAIZ = Path(__file__).resolve().parent.parent

ENTRADA = (
    RAIZ / "data/reportes/experimento_factorial_2_4_fraccionado.csv"
)

SALIDA = (
    RAIZ / "data/reportes/anova_factorial_2_4_fraccionado.csv"
)


def main():
    datos = pd.read_csv(ENTRADA)

    if len(datos) != 16:
        raise ValueError("Se esperaban 16 corridas.")

    # Modelo con los siete contrastes independientes.
    formula = (
        "tiempo_ms ~ A + B + C + D "
        "+ A:B + A:C + A:D"
    )

    modelo = smf.ols(formula, data=datos).fit()

    anova = sm.stats.anova_lm(modelo, typ=2)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    anova.to_csv(SALIDA, index_label="termino")

    print("===== ANOVA FACTORIAL FRACCIONADO 2^4-1 =====")
    print(anova.round(6).to_string())

    print("\n===== EFECTOS ESTIMADOS Y ALIAS =====")

    alias = {
        "A": "BCD",
        "B": "ACD",
        "C": "ABD",
        "D": "ABC",
        "A:B": "CD",
        "A:C": "BD",
        "A:D": "BC",
    }

    for termino, equivalente in alias.items():
        efecto = 2 * modelo.params[termino]
        p = anova.loc[termino, "PR(>F)"]

        print(
            f"{termino} = {equivalente}: "
            f"{efecto:+.4f} ms | p={p:.6f}"
        )

    print("\n===== DIAGNOSTICO =====")

    print(f"R2: {modelo.rsquared:.4f}")
    print(f"R2 ajustado: {modelo.rsquared_adj:.4f}")
    print(
        f"Desviacion residual: "
        f"{modelo.mse_resid**0.5:.4f} ms"
    )

    w, p = shapiro(modelo.resid)

    print(f"Shapiro-Wilk W: {w:.6f}")
    print(f"Shapiro-Wilk p: {p:.6f}")

    print("\n===== EFECTOS SIGNIFICATIVOS =====")

    significativos = anova[
        anova["PR(>F)"] < 0.05
    ]

    if significativos.empty:
        print("No se encontraron efectos significativos.")
    else:
        print(significativos[["F", "PR(>F)"]].to_string())

    print("\nResultados guardados en:", SALIDA)


if __name__ == "__main__":
    main()
