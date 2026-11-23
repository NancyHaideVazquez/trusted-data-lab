import hashlib
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

import pandas as pd

ORO = Path("data/oro/indicadores_mensuales_e2.csv")
PLATA = Path("data/plata/integracion_mensual_e2.csv")
SALIDA = Path("data/reportes/metricas_iso25012_e2.csv")

inicio = perf_counter()
df = pd.read_csv(ORO)
tiempo_ms = (perf_counter() - inicio) * 1000

total = len(df)
resultados = []

def registrar(nombre, formula, numerador, denominador, evidencia, limite):
    porcentaje = (
        round(numerador / denominador * 100, 4)
        if denominador else None
    )
    resultados.append({
        "caracteristica": nombre,
        "formula": formula,
        "numerador": numerador,
        "denominador": denominador,
        "resultado_porcentaje": porcentaje,
        "evidencia": evidencia,
        "limitacion": limite
    })

# Completitud
campos = [
    "periodo", "fuente", "serie_id", "indicador",
    "valor", "unidad", "metodo", "cobertura",
    "archivo_origen", "fecha_ingesta_utc"
]

presentes = df[campos].notna()
for campo in campos:
    presentes[campo] &= (
        df[campo].astype(str).str.strip().ne("")
    )

registrar(
    "Completitud",
    "Campos presentes / campos esperados",
    int(presentes.sum().sum()),
    total * len(campos),
    str(ORO),
    "Evalua los diez campos obligatorios"
)

# Consistencia
periodos = pd.to_datetime(
    df["periodo"], format="%Y-%m", errors="coerce"
)

valores = pd.to_numeric(df["valor"], errors="coerce")

duplicados = df.duplicated(
    subset=["periodo", "fuente", "serie_id"],
    keep=False
)

consistentes = (
    periodos.notna()
    & valores.notna()
    & ~duplicados
)

registrar(
    "Consistencia",
    "Filas con periodo, valor y llave validos / total",
    int(consistentes.sum()),
    total,
    str(ORO),
    "No sustituye la validacion integral de Pandera"
)

# Trazabilidad
fechas = pd.to_datetime(
    df["fecha_ingesta_utc"],
    errors="coerce",
    utc=True
)

origenes = df["archivo_origen"].apply(
    lambda ruta: Path(str(ruta)).is_file()
)

registrar(
    "Trazabilidad",
    "Filas con archivo existente y fecha valida / total",
    int((origenes & fechas.notna()).sum()),
    total,
    str(ORO),
    "Verifica referencias, no el valor original"
)

# Hash SHA-256 de archivos Bronce
hashes = []

for ruta in sorted(df["archivo_origen"].dropna().unique()):
    archivo = Path(ruta)

    if archivo.is_file():
        sha = hashlib.sha256(
            archivo.read_bytes()
        ).hexdigest()

        hashes.append({
            "archivo_origen": ruta,
            "sha256": sha
        })

# Conservacion de valores entre Plata y Oro
plata = pd.read_csv(PLATA)

llaves = ["periodo", "fuente", "serie_id"]

comparacion = df.merge(
    plata[llaves + ["valor"]],
    on=llaves,
    how="left",
    suffixes=("_oro", "_plata"),
    validate="one_to_one"
)

diferencia = (
    comparacion["valor_oro"]
    - comparacion["valor_plata"]
).abs()

coincidentes = diferencia.le(1e-9)

registrar(
    "Precision - conservacion Plata/Oro",
    "Valores conservados / total",
    int(coincidentes.sum()),
    total,
    str(PLATA),
    "Tolerancia 1e-9; no mide precision de la fuente"
)

# Credibilidad: identificacion de fuentes
fuentes_validas = (
    (
        df["fuente"].eq("banxico")
        & df["serie_id"].astype(str).eq("SF43783")
    )
    |
    (
        df["fuente"].eq("inegi")
        & df["serie_id"].astype(str).eq("910402")
    )
)

registrar(
    "Credibilidad - identificacion",
    "Filas con fuente y serie esperadas / total",
    int(fuentes_validas.sum()),
    total,
    str(ORO),
    "No acredita por si sola licencias ni exactitud"
)

# Disponibilidad local
registrar(
    "Disponibilidad local",
    "Archivos de datos legibles / archivos probados",
    2,
    2,
    f"{ORO}; {PLATA}",
    "Una comprobacion local, no disponibilidad continua"
)

# Guardar evidencias
SALIDA.parent.mkdir(parents=True, exist_ok=True)

pd.DataFrame(resultados).to_csv(
    SALIDA,
    index=False,
    encoding="utf-8"
)

pd.DataFrame(hashes).to_csv(
    SALIDA.parent / "hashes_bronce_e2.csv",
    index=False,
    encoding="utf-8"
)

print("=" * 60)
print("METRICAS ISO/IEC 25012 - E2")
print("=" * 60)

print("Fecha UTC:", datetime.now(UTC).isoformat())
print("Registros Oro:", total)
print("Columnas:", len(df.columns))
print("Tiempo de lectura:", round(tiempo_ms, 4), "ms")
print()

for resultado in resultados:
    print(
        resultado["caracteristica"],
        ":",
        resultado["numerador"],
        "/",
        resultado["denominador"],
        "=",
        resultado["resultado_porcentaje"],
        "%"
    )

print()
print("Archivos Bronce con SHA-256:", len(hashes))
print("Reporte:", SALIDA)
print("OK: mediciones finalizadas.")
