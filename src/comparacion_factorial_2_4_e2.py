from pathlib import Path

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

RAIZ = Path(__file__).resolve().parent.parent

ARCHIVO_COMPLETO = (
    RAIZ / "data/reportes/experimento_factorial_2_4_completo.csv"
)

ARCHIVO_FRACCIONADO = (
    RAIZ / "data/reportes/experimento_factorial_2_4_fraccionado.csv"
)

SALIDA = (
    RAIZ / "data/reportes/comparacion_factorial_2_4.csv"
)


def analizar(datos, formula, nombre, alias):
    modelo = smf.ols(formula, data=datos).fit()
    anova = sm.stats.anova_lm(modelo, typ=2)

    resultados = []

    for termino in anova.index:
        if termino == "Residual":
            continue

        resultados.append({
            "diseno": nombre,
            "efecto": termino,
            "alias": alias.get(termino, termino),
            "efecto_ms": 2 * modelo.params[termino],
            "valor_p": anova.loc[termino, "PR(>F)"],
            "significativo": (
                anova.loc[termino, "PR(>F)"] < 0.05
            ),
        })

    return pd.DataFrame(resultados), modelo


def main():
    completo = pd.read_csv(ARCHIVO_COMPLETO)
    fraccionado = pd.read_csv(ARCHIVO_FRACCIONADO)

    formula_completo = "tiempo_ms ~ A * B * C * D"

    formula_fraccionado = (
        "tiempo_ms ~ A + B + C + D "
        "+ A:B + A:C + A:D"
    )

    alias_fraccionado = {
        "A": "A = BCD",
        "B": "B = ACD",
        "C": "C = ABD",
        "D": "D = ABC",
        "A:B": "AB = CD",
        "A:C": "AC = BD",
        "A:D": "AD = BC",
    }

    resultado_completo, modelo_completo = analizar(
        completo,
        formula_completo,
        "Completo 2^4",
        {},
    )

    resultado_fraccionado, modelo_fraccionado = analizar(
        fraccionado,
        formula_fraccionado,
        "Fraccionado 2^4-1",
        alias_fraccionado,
    )

    comparacion = pd.concat(
        [resultado_completo, resultado_fraccionado],
        ignore_index=True,
    )

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    comparacion.to_csv(SALIDA, index=False)

    print("===== COMPARACION DE DISENOS =====")
    print(comparacion.round(5).to_string(index=False))

    print("\n===== RESUMEN =====")

    for nombre, modelo, datos in [
        ("Completo", modelo_completo, completo),
        ("Fraccionado", modelo_fraccionado, fraccionado),
    ]:
        print(f"\n{nombre}")
        print("Corridas:", len(datos))
        print(f"R2: {modelo.rsquared:.4f}")
        print(f"R2 ajustado: {modelo.rsquared_adj:.4f}")
        print(
            f"Desviacion residual: "
            f"{modelo.mse_resid**0.5:.4f} ms"
        )

    print("\nArchivo generado:", SALIDA)
    print("COMPARACION COMPLETADA")


if __name__ == "__main__":
    main()
