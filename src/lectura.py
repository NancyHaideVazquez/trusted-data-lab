"""Inventario de archivos de la capa Bronce (solo lectura).

Desde la raí­z del repositorio:
    python -m src.lectura

Dependencias: pandas; pyarrow (o fastparquet) para archivos Parquet.
"""

import hashlib
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRONCE = RAIZ / "data" / "bronce"
REPORTE = RAIZ / "data" / "reportes" / "inventario_bronce.csv"
EXTENSIONES = {".json", ".csv", ".parquet"}


def calcular_sha256(ruta):
    """Obtiene una huella del archivo, sin modificarlo."""
    huella = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            huella.update(bloque)
    return huella.hexdigest()


def buscar_observaciones(objeto):
    """Ubica listas de observaciones en respuestas anidadas de INEGI/Banxico.

    No confunde un objeto de metadatos con una fila de datos.
    """
    if isinstance(objeto, list):
        if not objeto:
            return objeto
        # Las listas de series contienen metadatos, no observaciones.
        if (
            all(isinstance(elemento, dict) for elemento in objeto)
            and not any(
                any(
                    clave in elemento
                    for clave in ("OBSERVATIONS", "observations", "datos", "Datos")
                )
                for elemento in objeto
            )
        ):
            return objeto
        for elemento in objeto:
            encontrado = buscar_observaciones(elemento)
            if encontrado is not None:
                return encontrado
        return None

    if isinstance(objeto, dict):
        # Primero se buscan las listas que representan observaciones individuales.
        for clave in ("OBSERVATIONS", "observations", "observaciones", "datos", "Datos"):
            contenido = objeto.get(clave)
            if isinstance(contenido, list) and (not contenido or all(isinstance(x, dict) for x in contenido)):
                return contenido
        # Luego se atraviesan los envoltorios de ambas APIs y de la capa Bronce.
        for clave in ("Series", "series", "data", "bmx", "respuesta", "payload", "datos", "resultado"):
            if clave in objeto:
                encontrado = buscar_observaciones(objeto[clave])
                if encontrado is not None:
                    return encontrado
    return None


def cargar_dataframe(ruta):
    """Carga una tabla de observaciones; no altera el archivo original."""
    extension = ruta.suffix.lower()
    if extension == ".csv":
        return pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig", dtype=str)
    if extension == ".parquet":
        return pd.read_parquet(ruta)
    if extension == ".json":
        with ruta.open("r", encoding="utf-8-sig") as archivo:
            objeto = json.load(archivo)
        observaciones = buscar_observaciones(objeto)
        if observaciones is None:
            raise ValueError("JSON sin lista reconocible de observaciones; revisar estructura")
        return pd.json_normalize(observaciones)
    raise ValueError("ExtensiÃ³n no soportada")


def convertir_fecha(serie):
    """Acepta YYYY-MM-DD, YYYY/MM y fechas DD/MM/YYYY (Banxico)."""
    textos = serie.astype("string").str.strip()
    # Para fechas mensuales como 2011/08, se usa el primer dÃ­a del mes.
    mensuales = textos.str.fullmatch(r"\d{4}[-/]\d{1,2}").fillna(False)
    textos = textos.where(~mensuales, textos.str.replace("/", "-", regex=False) + "-01")
    fechas = pd.to_datetime(textos, errors="coerce", dayfirst=False, format="mixed")
    # Banxico suele usar DD/MM/YYYY; tratarlo de forma explÃ­cita.
    formato_banxico = textos.str.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}").fillna(False)
    if formato_banxico.any():
        fechas.loc[formato_banxico] = pd.to_datetime(
            textos.loc[formato_banxico], format="%d/%m/%Y", errors="coerce"
        )
    return fechas


def resumen_periodo(df):
    """Devuelve fecha mÃ­nima y mÃ¡xima; si no identifica fechas, deja campos vacÃ­os."""
    candidatas = ("TIME_PERIOD", "time_period", "fecha", "FECHA", "DATE", "date", "periodo")
    for columna in candidatas:
        if columna in df.columns:
            fechas = convertir_fecha(df[columna]).dropna()
            if not fechas.empty:
                return columna, fechas.min().date().isoformat(), fechas.max().date().isoformat()
    return "", "", ""


def inventariar(bronce=BRONCE, reporte=REPORTE):
    """Produce una fila de inventario por archivo, incluso cuando no se puede leer."""
    bronce = Path(bronce)
    reporte = Path(reporte)
    if not bronce.is_dir():
        raise FileNotFoundError(f"No existe la carpeta Bronce: {bronce}")

    filas = []
    archivos = sorted(p for p in bronce.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONES)
    for ruta in archivos:
        relativo = ruta.relative_to(bronce)
        fila = {
            "archivo": ruta.as_posix(),
            "ruta_relativa_bronce": relativo.as_posix(),
            "fuente": relativo.parts[0] if len(relativo.parts) > 1 else "sin_identificar",
            "formato": ruta.suffix.lower().lstrip("."),
            "sha256": "",
            "filas": "",
            "columnas": "",
            "nombres_columnas": "",
            "tipos": "",
            "nulos_por_columna": "",
            "columna_fecha": "",
            "periodo_min": "",
            "periodo_max": "",
            "error_lectura": "",
        }
        try:
            fila["sha256"] = calcular_sha256(ruta)
            df = cargar_dataframe(ruta)
            fila["filas"] = len(df)
            fila["columnas"] = len(df.columns)
            fila["nombres_columnas"] = json.dumps(df.columns.tolist(), ensure_ascii=False)
            fila["tipos"] = json.dumps({c: str(t) for c, t in df.dtypes.items()}, ensure_ascii=False)
            fila["nulos_por_columna"] = json.dumps(df.isna().sum().to_dict(), ensure_ascii=False)
            fila["columna_fecha"], fila["periodo_min"], fila["periodo_max"] = resumen_periodo(df)
        except (OSError, ValueError, TypeError, ImportError, json.JSONDecodeError) as error:
            fila["error_lectura"] = f"{type(error).__name__}: {error}"
        filas.append(fila)

    columnas = ["archivo", "ruta_relativa_bronce", "fuente", "formato", "sha256", "filas", "columnas",
                "nombres_columnas", "tipos", "nulos_por_columna", "columna_fecha",
                "periodo_min", "periodo_max", "error_lectura"]
    inventario = pd.DataFrame(filas, columns=columnas)
    reporte.parent.mkdir(parents=True, exist_ok=True)
    inventario.to_csv(reporte, index=False, encoding="utf-8-sig")
    return inventario


if __name__ == "__main__":
    resultado = inventariar()
    print(f"Archivos inventariados: {len(resultado)}")
    print(f"Archivos con error: {resultado['error_lectura'].ne('').sum()}")
    print(f"Reporte: {REPORTE}")
    if not resultado.empty:
        print(resultado[["fuente", "ruta_relativa_bronce", "filas", "periodo_min", "periodo_max", "error_lectura"]].to_string(index=False))