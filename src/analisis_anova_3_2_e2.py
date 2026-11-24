
"""Analisis estadistico del experimento factorial 3x2."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import levene, shapiro

RAIZ = Path(__file__).resolve().parent.parent
REPORTES = RAIZ / "data/reportes"
FIGURAS = RAIZ / "reportes/figuras/anova_3_2"
ALFA = 0.05


def analizar_experimento():
    datos = pd.read_csv(
        REPORTES / "experimento_anova_3_2.csv"
    )

    FIGURAS.mkdir(parents=True, exist_ok=True)

    if len(datos) != 12:
        raise ValueError("Se esperaban 12 corridas.")

    conteos = datos.groupby(
        ["procesos", "formato"]
    ).size()

    if len(conteos) != 6 or not conteos.eq(2).all():
        raise ValueError("Diseno factorial incompleto.")

    modelo = smf.ols(
        "tiempo_ms ~ C(procesos) * C(formato)",
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

    anova.to_csv(REPORTES / "anova_3_2.csv")

    resumen = (
        datos.groupby(["procesos", "formato"])
        ["tiempo_ms"]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
    )

    resumen.to_csv(
        REPORTES / "resumen_anova_3_2.csv",
        index=False,
    )

    residuos = modelo.resid
    ajustados = modelo.fittedvalues

    w, p_shapiro = shapiro(residuos)

    grupos = [
        grupo["tiempo_ms"].to_numpy()
        for _, grupo in datos.groupby(
            ["procesos", "formato"]
        )
    ]

    estadistico_levene, p_levene = levene(
        *grupos,
        center="mean",
    )

    diagnostico = pd.DataFrame([{
        "r2": modelo.rsquared,
        "r2_ajustado": modelo.rsquared_adj,
        "desviacion_residual": modelo.mse_resid ** 0.5,
        "shapiro_w": w,
        "shapiro_p": p_shapiro,
        "levene_estadistico": estadistico_levene,
        "levene_p": p_levene,
    }])

    diagnostico.to_csv(
        REPORTES / "diagnostico_anova_3_2.csv",
        index=False,
    )

    # Grafica de efecto principal: procesos.
    medias = datos.groupby("procesos")["tiempo_ms"].mean()

    plt.figure(figsize=(8, 5))
    plt.plot(medias.index, medias.values, marker="o")
    plt.xticks([1, 2, 4])
    plt.xlabel("Numero de procesos")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Efecto principal del numero de procesos")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "01_efecto_procesos.png",
        dpi=200,
    )
    plt.close()

    # Grafica de efecto principal: formato.
    medias = datos.groupby("formato")["tiempo_ms"].mean()

    plt.figure(figsize=(8, 5))
    plt.bar(medias.index, medias.values)
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Efecto principal del formato")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "02_efecto_formato.png",
        dpi=200,
    )
    plt.close()

    # Grafica de interaccion.
    plt.figure(figsize=(8, 5))

    for formato, grupo in resumen.groupby("formato"):
        plt.plot(
            grupo["procesos"],
            grupo["mean"],
            marker="o",
            label=formato,
        )

    plt.xticks([1, 2, 4])
    plt.xlabel("Numero de procesos")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Interaccion procesos y formato")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "03_interaccion.png",
        dpi=200,
    )
    plt.close()

    # Residuos contra valores ajustados.
    plt.figure(figsize=(8, 5))
    plt.scatter(ajustados, residuos)
    plt.axhline(0, linestyle="--")
    plt.xlabel("Valores ajustados")
    plt.ylabel("Residuos")
    plt.title("Residuos contra valores ajustados")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "04_residuos.png",
        dpi=200,
    )
    plt.close()

    # Grafica Q-Q.
    sm.qqplot(residuos, line="s")
    plt.title("Grafica Q-Q de residuos")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "05_qqplot.png",
        dpi=200,
    )
    plt.close()

    # Residuos en orden de ejecucion.
    plt.figure(figsize=(8, 5))
    plt.plot(datos["orden"], residuos, marker="o")
    plt.axhline(0, linestyle="--")
    plt.xlabel("Orden de ejecucion")
    plt.ylabel("Residuos")
    plt.title("Residuos por orden experimental")
    plt.tight_layout()
    plt.savefig(
        FIGURAS / "06_residuos_orden.png",
        dpi=200,
    )
    plt.close()

    print("\n===== TABLA ANOVA 3x2 =====")
    print(anova.to_string())

    print("\n===== RESUMEN POR TRATAMIENTO =====")
    print(resumen.to_string(index=False))

    print("\n===== DIAGNOSTICO DEL MODELO =====")
    print(diagnostico.to_string(index=False))

    print("\n===== MEJOR TRATAMIENTO OBSERVADO =====")
    print(
        resumen.sort_values("mean")
        .head(1)
        .to_string(index=False)
    )

    print("\nAnalisis completado.")
    print("Graficas:", FIGURAS)


if __name__ == "__main__":
    analizar_experimento()
