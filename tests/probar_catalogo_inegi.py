
"""
Prueba de conexión con el catálogo de INEGI.
No imprime ni guarda el token.
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Localizamos el .env en la raíz del proyecto
RAIZ = Path(__file__).resolve().parents[1]

# Cargamos las variables del archivo .env
load_dotenv(RAIZ / ".env")

# Obtenemos el token de INEGI
TOKEN = os.getenv("INEGI_TOKEN")

if not TOKEN:
    raise SystemExit("No se encontró INEGI_TOKEN")

BASE = (
    "https://www.inegi.org.mx/app/api/"
    "indicadores/desarrolladores/jsonxml"
)

# Indicador oficial utilizado para comprobar la conexión
CODIGO = "1002000001"

url = (
    f"{BASE}/CL_INDICATOR/{CODIGO}/"
    f"es/BISE/2.0/{TOKEN}"
)

try:
    respuesta = requests.get(
        url,
        params={"type": "json"},
        timeout=30,
        allow_redirects=False
    )

    print("Estado HTTP:", respuesta.status_code)
    print(
        "Tipo de contenido:",
        respuesta.headers.get("Content-Type")
    )

    if respuesta.status_code != 200:
        raise RuntimeError("La consulta no fue exitosa")

    # Verificamos que la respuesta sea JSON
    datos = respuesta.json()

    if datos.get("id") != "CL_INDICATOR":
        raise ValueError("La respuesta no es el catálogo esperado")

    registros = datos.get("CODE", [])

    print("Catálogo:", datos.get("id"))
    print("Registros:", len(registros))

    for registro in registros[:5]:
        print("Código:", registro.get("value"))
        print("Descripción:", registro.get("Description"))

except requests.exceptions.JSONDecodeError:
    print("INEGI devolvió una respuesta que no es JSON.")

except (requests.RequestException, ValueError, RuntimeError) as error:
    print("Error:", type(error).__name__)
    print("Revisa la estructura de la consulta y el token.")
