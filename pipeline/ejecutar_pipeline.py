
from pathlib import Path
import csv
from datetime import datetime, timezone

import pandas as pd

from pipeline.publicacion import publicar_tablas
from src.reduccion import reducir_datos
from src.integracion import integrar_datos
from src.cuarentena import separar_cuarentena
from src.calidad import validar_calidad
from src.oro import preparar_oro

from src.diagnostico import buscar_historico, diagnosticar
from src.lectura import cargar_dataframe
from src.limpieza import limpieza_conservadora
from src.transformaciones import escalar_datos
from src.discretizacion import discretizar_datos

BASE = Path(__file__).resolve().parent.parent

ENTRADA_INEGI = (
    BASE / "data/reportes/limpieza_preliminar_inegi.csv"
)

ENTRADA_BANXICO = (
    BASE / "data/reportes/limpieza_preliminar_banxico.csv"
)

SALIDA_PLATA = (
    BASE / "data/plata/integracion_mensual.csv"
)

SALIDA_ORO = (
    BASE / "data/oro/indicadores_mensuales.csv"
)

SALIDA_CUARENTENA = (
    BASE / "data/cuarentena/registros/"
    "integracion_mensual_rechazados.csv"
)

SALIDA_REPORTE = (
    BASE / "data/cuarentena/reportes/"
    "reporte_cuarentena.csv"
)

RUTA_BITACORA = BASE / "logs/pipeline_ejecuciones.csv"


def registrar_ejecucion(
    ruta_inegi,
    ruta_banxico,
    filas_inegi,
    filas_banxico,
    filas_banxico_mensual,
    filas_integradas,
    filas_validas,
    filas_rechazadas,
):
    """Registra una ejecución exitosa del pipeline en UTC."""

    RUTA_BITACORA.parent.mkdir(
        parents=True, exist_ok=True
    )

    registro = {
        "fecha_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "archivo_inegi": str(ruta_inegi),
        "archivo_banxico": str(ruta_banxico),
        "filas_inegi": filas_inegi,
        "filas_banxico": filas_banxico,
        "filas_banxico_mensual": filas_banxico_mensual,
        "filas_integradas": filas_integradas,
        "filas_validas": filas_validas,
        "filas_invalidas": filas_rechazadas,
        "salida_plata": str(SALIDA_PLATA),
        "salida_oro": str(SALIDA_ORO),
        "salida_cuarentena": str(SALIDA_CUARENTENA),
        "salida_reporte": str(SALIDA_REPORTE),
        "estado": "EXITOSO",
    }

    existe = (
        RUTA_BITACORA.exists()
        and RUTA_BITACORA.stat().st_size > 0
    )

    with RUTA_BITACORA.open(
        "a", newline="", encoding="utf-8"
    ) as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=list(registro.keys())
        )

        if not existe:
            escritor.writeheader()

        escritor.writerow(registro)



def analizar_transformaciones(datos, fuente):
    """
    Ejecuta T07 y T08 por separado para cada serie.

    Conserva los valores originales. Si no existen suficientes
    valores distintos para discretizar, registra la limitacion
    sin detener el pipeline.
    """

    # T07: escalado sin modificar el original
    escalados, parametros_escalado = escalar_datos(
        datos, columna="valor"
    )

    # T08 necesita al menos tres valores numericos distintos
    valores_distintos = datos["valor"].dropna().nunique()

    if valores_distintos < 3:
        print(
            f"Discretizacion {fuente.upper()}: omitida "
            f"({valores_distintos} valores distintos; se requieren 3)"
        )

        if not escalados["valor"].equals(datos["valor"]):
            raise RuntimeError(
                f"{fuente}: el escalado altero los valores originales"
            )

        return parametros_escalado, None

    discretizados, parametros_discretizacion = discretizar_datos(
        escalados, columna="valor", metodo="cut"
    )

    if not discretizados["valor"].equals(datos["valor"]):
        raise RuntimeError(
            f"{fuente}: las transformaciones alteraron los valores"
        )

    if len(discretizados) != len(datos):
        raise RuntimeError(
            f"{fuente}: las transformaciones cambiaron las filas"
        )

    categorias = discretizados["valor_cut"].value_counts()

    print(
        f"Transformaciones {fuente.upper()}:",
        len(discretizados),
        "registros"
    )

    print(
        "Categorias:",
        categorias.to_dict()
    )

    return parametros_escalado, parametros_discretizacion



def ejecutar_pipeline():
    print("T13 - PIPELINE AUTOMATIZADO")

    # 1. Localizar archivos historicos de Bronce
    ruta_inegi = buscar_historico("inegi", "910402")
    ruta_banxico = buscar_historico("banxico", "SF43783")

    print("Bronce INEGI:", ruta_inegi.name)
    print("Bronce Banxico:", ruta_banxico.name)

    # 2. Leer los JSON originales sin modificarlos
    crudo_inegi = cargar_dataframe(ruta_inegi)
    crudo_banxico = cargar_dataframe(ruta_banxico)


    # Diagnosticar los archivos originales sin escribir reportes
    diagnostico_inegi = diagnosticar(
        ruta_inegi, "inegi", guardar_reporte=False
    )

    diagnostico_banxico = diagnosticar(
        ruta_banxico, "banxico", guardar_reporte=False
    )

    print(
        "Diagnostico INEGI - faltantes:",
        diagnostico_inegi["faltantes"]
    )
    print(
        "Diagnostico Banxico - faltantes:",
        diagnostico_banxico["faltantes"]
    )

    # 3. Normalizar y detectar atípicos sin eliminar registros
    inegi, reporte_inegi, iqr_inegi = limpieza_conservadora(
        crudo_inegi, "inegi"
    )

    banxico, reporte_banxico, iqr_banxico = limpieza_conservadora(
        crudo_banxico, "banxico"
    )

    print(
        "Atipicos INEGI:",
        int(inegi["es_atipico"].sum())
    )

    print(
        "Atipicos Banxico:",
        int(banxico["es_atipico"].sum())
    )


    print("INEGI:", len(inegi))
    print("Banxico diarios:", len(banxico))

    # 4. Reducir Banxico a meses
    banxico_mensual = reducir_datos(banxico)
    print("Banxico mensual:", len(banxico_mensual))

    # T07 y T08: analizar cada indicador por separado
    analizar_transformaciones(inegi, "inegi")
    analizar_transformaciones(banxico_mensual, "banxico")

    # 5. Integrar sin publicar todavía
    integrado = integrar_datos(
        inegi, banxico_mensual
    )
    print("Integrados:", len(integrado))

    # 6. Separar registros inválidos
    validos, rechazados = separar_cuarentena(integrado)

    # 7. Verificar la partición
    if len(validos) + len(rechazados) != len(integrado):
        raise RuntimeError(
            "La separacion perdio registros."
        )

    # 8. Validar nuevamente antes de publicar
    validar_calidad(validos)

    # Preparar Oro únicamente con registros validados
    datos_oro = preparar_oro(validos)

    # 9. Preparar carpetas
    SALIDA_PLATA.parent.mkdir(
        parents=True, exist_ok=True
    )

    SALIDA_ORO.parent.mkdir(
    parents=True, exist_ok=True
    )

    SALIDA_CUARENTENA.parent.mkdir(
        parents=True, exist_ok=True
    )
    
    SALIDA_REPORTE.parent.mkdir(
        parents=True, exist_ok=True
    )


    # 10. Crear el reporte
    reporte = pd.DataFrame([{
        "registros_originales": len(integrado),
        "registros_validos": len(validos),
        "registros_rechazados": len(rechazados),
        "estado": (
            "CON_RECHAZOS"
            if len(rechazados)
            else "SIN_RECHAZOS"
        )
    }])


    # 11. Publicar las cuatro salidas de forma protegida
    publicar_tablas({
        SALIDA_PLATA: validos,
        SALIDA_ORO: datos_oro,
        SALIDA_CUARENTENA: rechazados,
        SALIDA_REPORTE: reporte
    })


    # 12. Registrar la ejecución exitosa en la bitácora
    registrar_ejecucion(
        ruta_inegi=ruta_inegi,
        ruta_banxico=ruta_banxico,
        filas_inegi=len(inegi),
        filas_banxico=len(banxico),
        filas_banxico_mensual=len(banxico_mensual),
        filas_integradas=len(integrado),
        filas_validas=len(validos),
        filas_rechazadas=len(rechazados),
    )


    print("Validos:", len(validos))
    print("Rechazados:", len(rechazados))
    print("Plata:", SALIDA_PLATA)
    print("Oro:", SALIDA_ORO)
    print("Cuarentena:", SALIDA_CUARENTENA)
    print("Reporte:", SALIDA_REPORTE)
    print("Pipeline completado correctamente.")



if __name__ == "__main__":
    ejecutar_pipeline()
