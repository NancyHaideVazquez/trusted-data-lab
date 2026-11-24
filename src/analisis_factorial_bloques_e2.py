
"""ANOVA factorial 2^3 con bloques completos aleatorizados."""

import itertools
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import shapiro

RAIZ = Path(__file__).resolve().parent.parent
REPORTES = RAIZ / "data/reportes"
FIGURAS = RAIZ / "reportes/figuras/factorial_bloques"
ALFA = 0.05


def analizar_experimento():
    datos = pd.concat(
        [
            pd.read_csv(
                REPORTES / f"factorial_2_3_bloque_{bloque}.csv"
            )
            for bloque in (1, 2)
        ],
        ignore_index=True,
    )

    if len(datos) != 16:
        raise ValueError("Se esperaban 16 corridas.")

    tratamientos = set(
        itertools.product((-1, 1), repeat=3)
    )

    for bloque in (1, 2):
        grupo = datos[datos["bloque"] == bloque]

        combinaciones = set(
            grupo[["A", "B", "C"]].itertuples(
                index=False,
                name=None,
            )
        )

        if len(grupo) != 8 or combinaciones != tratamientos:
            raise ValueError(
                f"Diseno incompleto en el bloque {bloque}."
            )

    # Renombrar C para evitar conflictos con Patsy.
    datos = datos.rename(columns={"C": "factor_c"})

    modelo = smf.ols(
        "tiempo_ms ~ C(bloque) + A * B * factor_c",
        data=datos,
    ).fit()

    anova = sm.stats.anova_lm(modelo, typ=2)

    anova["media_cuadratica"] = (
        anova["sum_sq"] / anova["df"]
    )

    anova["significativo"] = anova["PR(>F)"].apply(
        lambda p: (
            "No aplica"
            if pd.isna(p)
            else "Si" if p < ALFA else "No"
        )
    )

    anova.to_csv(
        REPORTES / "anova_factorial_bloques_e2.csv"
    )

    efectos = pd.DataFrame([
        {
            "factor": termino.replace("factor_c", "C"),
            "efecto_ms": 2 * modelo.params[termino],
            "valor_p": modelo.pvalues[termino],
        }
        for termino in (
            "A",
            "B",
            "factor_c",
            "A:B",
            "A:factor_c",
            "B:factor_c",
            "A:B:factor_c",
        )
    ])

    efectos.to_csv(
        REPORTES / "efectos_factorial_bloques_e2.csv",
        index=False,
    )

    resumen = (
        datos.groupby("bloque")["tiempo_ms"]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
    )

    resumen.to_csv(
        REPORTES / "resumen_factorial_bloques_e2.csv",
        index=False,
    )

    residuos = modelo.resid
    ajustados = modelo.fittedvalues

    w, p_shapiro = shapiro(residuos)

    diagnostico = pd.DataFrame([{
        "r2": modelo.rsquared,
        "r2_ajustado": modelo.rsquared_adj,
        "desviacion_residual": modelo.mse_resid ** 0.5,
        "shapiro_w": w,
        "shapiro_p": p_shapiro,
        "p_bloque": anova.loc["C(bloque)", "PR(>F)"],
    }])

    diagnostico.to_csv(
        REPORTES / "diagnostico_factorial_bloques_e2.csv",
        index=False,
    )

    FIGURAS.mkdir(parents=True, exist_ok=True)

    # Efectos factoriales.
    plt.figure(figsize=(9, 5))
    plt.bar(efectos["factor"], efectos["efecto_ms"])
    plt.axhline(0, linestyle="--")
    plt.ylabel("Efecto estimado (ms)")
    plt.title("Efectos factoriales ajustados por bloque")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "01_efectos_factoriales.png",
        dpi=200,
    )
    plt.close()

    # Comparacion entre bloques.
    plt.figure(figsize=(7, 5))
    plt.bar(
        resumen["bloque"].astype(str),
        resumen["mean"],
    )
    plt.xlabel("Bloque experimental")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Comparacion entre sesiones")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "02_comparacion_bloques.png",
        dpi=200,
    )
    plt.close()

    # Residuos contra valores ajustados.
    plt.figure(figsize=(8, 5))
    plt.scatter(ajustados, residuos)
    plt.axhline(0, linestyle="--")
    plt.xlabel("Valores ajustados (ms)")
    plt.ylabel("Residuos (ms)")
    plt.title("Residuos del modelo con bloques")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "03_residuos.png",
        dpi=200,
    )
    plt.close()

    # Grafica Q-Q.
    sm.qqplot(residuos, line="s")
    plt.title("Normalidad de residuos")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "04_qqplot.png",
        dpi=200,
    )
    plt.close()

    # Residuos por orden experimental.
    plt.figure(figsize=(9, 5))
    plt.plot(
        range(1, len(datos) + 1),
        residuos,
        marker="o",
    )
    plt.axhline(0, linestyle="--")
    plt.axvline(8.5, linestyle=":")
    plt.xlabel("Orden global de ejecucion")
    plt.ylabel("Residuos (ms)")
    plt.title("Residuos por orden y bloque")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "05_residuos_orden.png",
        dpi=200,
    )
    plt.close()

    print("\n===== ANOVA FACTORIAL CON BLOQUES =====")
    print(anova.to_string())

    print("\n===== EFECTOS FACTORIALES =====")
    print(efectos.to_string(index=False))

    print("\n===== RESUMEN POR BLOQUE =====")
    print(resumen.to_string(index=False))

    print("\n===== DIAGNOSTICO DEL MODELO =====")
    print(diagnostico.to_string(index=False))

    print("\nAnalisis completado.")
    print("Graficas:", FIGURAS)


if __name__ == "__main__":
    analizar_experimento()
