"""
TRUSTED DATA LAB - extractores/base.py

Que hace este archivo
---------------------
Contiene la clase ExtractorEtico, que es la unica forma en que el proyecto
hace peticiones a internet. Asi las reglas de buen comportamiento viven en un
solo lugar y no hay que repetirlas en cada extractor.

Reglas que cumple
-----------------
1. Solo usa HTTPS.
2. Se identifica con un User-Agent honesto que incluye un contacto real.
3. Revisa robots.txt (si se le pide) y respeta su Crawl-delay.
4. Espera minimo 1.5 segundos entre peticiones al mismo dominio.
5. Si la fuente esta saturada (429) o falla (5xx), reintenta esperando cada
   vez mas tiempo (espera exponencial).
6. Nunca escribe tokens en los logs.
7. Entrega metadatos de cada captura (fecha UTC, URL sin token, estado, etc.).

Ejemplo de uso
--------------
    from extractores.base import ExtractorEtico

    ext = ExtractorEtico()
    respuesta, metadatos = ext.get("https://ejemplo.mx/api/datos")
    datos = respuesta.json()
    ext.cerrar()
"""

import csv
import json
import logging
import os
import time
import urllib.robotparser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

# Raiz del repositorio (la carpeta que contiene "extractores/").
# Se calcula a partir de este archivo, asi funciona sin importar desde que
# carpeta se ejecute el programa.
RAIZ = Path(__file__).resolve().parent.parent

# Si existe un archivo .env, sus variables se cargan aqui. Si ya existe una
# variable en el entorno (por ejemplo en GitHub Actions), esa tiene prioridad.
# Si python-dotenv no esta instalado, simplemente se omite este paso.
try:
    from dotenv import load_dotenv
    load_dotenv(RAIZ / ".env")
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Datos generales del proyecto
# ---------------------------------------------------------------------------

VERSION = "1.0.0"

# El contacto se toma de la variable de entorno TDL_CONTACTO.
# En GitHub Actions se define en el workflow. Cambia el valor por defecto
# por un correo real del equipo.
CONTACTO = os.getenv("TDL_CONTACTO", "equipo@correo.mx")

# Asi nos presentamos ante los servidores: quienes somos y como contactarnos.
# Si el .env define USER_AGENT completo, se usa ese; si no, se arma con CONTACTO.
UA = os.getenv("USER_AGENT") or (
    f"TDL-Observatorio/{VERSION} (proyecto academico; contacto: {CONTACTO})"
)

# Variables de entorno cuyo valor jamas debe aparecer en un log.
VARIABLES_SECRETAS = ("INEGI_TOKEN", "BANXICO_TOKEN")


def ahora_utc():
    """Fecha y hora actual en UTC (el mismo reloj en cualquier computadora)."""
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Registro de mensajes (logs)
# ---------------------------------------------------------------------------

def _crear_logger():
    """Crea un logger que escribe en logs/extraccion.log y en pantalla."""
    logger = logging.getLogger("TDL")

    # Si ya tiene "handlers", ya fue configurado: no lo duplicamos.
    if not logger.handlers:
        nivel = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, nivel, logging.INFO))

        carpeta = RAIZ / "logs"
        carpeta.mkdir(exist_ok=True)

        formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        archivo = logging.FileHandler(carpeta / "extraccion.log", encoding="utf-8")
        archivo.setFormatter(formato)
        logger.addHandler(archivo)

        # Tambien en pantalla, para ver lo que pasa en GitHub Actions.
        pantalla = logging.StreamHandler()
        pantalla.setFormatter(formato)
        logger.addHandler(pantalla)

    return logger


# ---------------------------------------------------------------------------
# La clase principal
# ---------------------------------------------------------------------------

class ExtractorEtico:
    """Hace peticiones GET de forma respetuosa y segura."""

    def __init__(self, pausa=None, revisar_robots=True, timeout=None):
        # Segundos minimos entre dos peticiones al mismo dominio.
        # Si no se indica, se lee REQUEST_DELAY_SECONDS del .env (o 1.5).
        # Aunque pidan menos, nunca bajamos de 1.5.
        if pausa is None:
            pausa = float(os.getenv("REQUEST_DELAY_SECONDS", "1.5"))
        self.pausa = max(pausa, 1.5)

        # True: consulta robots.txt antes de pedir cada ruta.
        self.revisar_robots = revisar_robots

        # Segundos maximos que esperamos una respuesta antes de rendirnos.
        # Si no se indica, se lee REQUEST_TIMEOUT del .env (o 20).
        if timeout is None:
            timeout = float(os.getenv("REQUEST_TIMEOUT", "20"))
        self.timeout = timeout

        if self.timeout <= 0:
            raise ValueError("El timeout debe ser mayor que cero")

        # Reglas de robots.txt ya descargadas, una por dominio.
        self.robots = {}

        # Momento de la ultima peticion a cada dominio.
        self.ultimo = {}

        # Una sesion reutiliza la conexion y manda siempre el mismo User-Agent.
        self.sesion = requests.Session()
        self.sesion.headers["User-Agent"] = UA

        self.logger = _crear_logger()

        # Aviso: un contacto de ejemplo contradice la regla del User-Agent honesto.
        if "CAMBIAR" in UA or "equipo@correo.mx" in UA:
            self.logger.warning(
                "El User-Agent tiene un contacto de ejemplo. "
                "Define un correo real en .env o en TDL_CONTACTO."
            )

    # -- robots.txt ---------------------------------------------------------

    def _reglas(self, url):
        """Devuelve las reglas de robots.txt del dominio de esta URL.

        Se descarga robots.txt una sola vez por dominio y se guarda.
        """
        partes = urlparse(url)
        base = f"{partes.scheme}://{partes.netloc}"

        if base not in self.robots:
            # Tambien esta peticion respeta la pausa entre solicitudes.
            self._esperar(partes.netloc, self.pausa)

            try:
                r = self.sesion.get(base + "/robots.txt", timeout=self.timeout)
            except requests.RequestException:
                raise RuntimeError(
                    f"No se pudo leer robots.txt de {partes.netloc}"
                ) from None

            reglas = urllib.robotparser.RobotFileParser()

            if r.status_code == 200:
                # El sitio publica reglas: las leemos.
                reglas.parse(r.text.splitlines())
            elif r.status_code in (401, 403):
                # El sitio prohibe el acceso: no pedimos nada.
                reglas.disallow_all = True
            elif 400 <= r.status_code < 500:
                # 404 y similares: el sitio no publica reglas.
                reglas.allow_all = True
            else:
                # Error del servidor: no sabemos que reglas hay, mejor parar.
                raise RuntimeError(
                    f"robots.txt de {partes.netloc} respondio HTTP {r.status_code}"
                )

            self.robots[base] = reglas

        return self.robots[base]

    # -- Espera entre peticiones --------------------------------------------

    def _esperar(self, dominio, segundos):
        """Espera lo necesario para que pasen `segundos` desde la ultima
        peticion a este dominio. Si ya paso suficiente tiempo, no espera."""
        anterior = self.ultimo.get(dominio)

        if anterior is not None:
            falta = segundos - (time.monotonic() - anterior)
            if falta > 0:
                time.sleep(falta)

        # Anotamos el momento de esta nueva peticion.
        self.ultimo[dominio] = time.monotonic()

    # -- Seguridad ----------------------------------------------------------

    def _url_segura(self, url):
        """Devuelve la URL sin parametros y con los tokens tapados.

        Algunas APIs (como INEGI) ponen el token dentro de la ruta de la URL.
        Por eso nunca guardamos ni mostramos la URL tal cual.
        """
        partes = urlparse(url)
        ruta = partes.path

        for variable in VARIABLES_SECRETAS:
            token = os.getenv(variable)
            if token:
                ruta = ruta.replace(token, "[PROTEGIDO]")

        return f"{partes.scheme}://{partes.netloc}{ruta}"

    # -- Metadatos ----------------------------------------------------------

    def _metadatos(self, url, respuesta, duracion, intentos):
        """Informacion sobre la captura, para guardarla junto a los datos."""
        return {
            "captured_at_utc": ahora_utc().isoformat(),
            "source_url": self._url_segura(url),
            "extractor_version": VERSION,
            "http_status": respuesta.status_code,
            # Tiempo total de la consulta, incluyendo esperas y reintentos.
            "duration_seconds": round(duracion, 3),
            "attempts": intentos,
        }

    # -- Peticion principal -------------------------------------------------

    def get(self, url, intentos=3, headers=None):
        """Hace una peticion GET y devuelve (respuesta, metadatos).

        Lanza una excepcion si la peticion no se puede completar:
        - ValueError: la URL no es HTTPS.
        - PermissionError: robots.txt no permite la ruta.
        - RuntimeError: la fuente fallo o se agotaron los intentos.
        """
        # Validar el numero de intentos
        if not isinstance(intentos, int) or intentos < 1:
            raise ValueError("El numero de intentos debe ser mayor que cero")
        partes = urlparse(url)

        # 1. Solo HTTPS, para que los datos y las llaves viajen cifrados.
        if partes.scheme != "https":
            raise ValueError("La URL debe utilizar HTTPS")

        dominio = partes.netloc
        pausa = self.pausa

        # 2. Revisar robots.txt si corresponde.
        if self.revisar_robots:
            reglas = self._reglas(url)

            if not reglas.can_fetch(UA, url):
                raise PermissionError("robots.txt no permite consultar esta ruta")

            # Si el sitio pide una pausa mayor, la respetamos.
            pausa = max(pausa, reglas.crawl_delay(UA) or 0)

        inicio = time.monotonic()
        motivo = "sin detalle"
        url_log = self._url_segura(url)

        # 3. Intentar la peticion, con reintentos si hay saturacion o fallas.
        for intento in range(1, intentos + 1):

            # Espera exponencial: 1.5 s, 3 s, 6 s... entre un intento y el
            # siguiente. Asi no insistimos de golpe a un servidor saturado.
            self._esperar(dominio, pausa * 2 ** (intento - 1))

            try:
                respuesta = self.sesion.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=False,
                )
            except requests.RequestException as error:
                # Solo guardamos el tipo de error: su texto podria traer la URL.
                motivo = type(error).__name__
                self.logger.warning(
                    "%s - fallo de conexion (%s). Intento %s de %s",
                    dominio, motivo, intento, intentos,
                )
                continue

            codigo = respuesta.status_code

            # Saturacion (429) o error del servidor (5xx): vale la pena reintentar.
            if codigo == 429 or 500 <= codigo <= 599:
                motivo = f"HTTP {codigo}"
                self.logger.warning(
                    "%s - %s. Intento %s de %s", dominio, motivo, intento, intentos
                )
                continue

            # Redireccion: no la seguimos sin revisarla, podria llevar a otro sitio.
            if 300 <= codigo <= 399:
                raise RuntimeError(
                    f"HTTP {codigo}: la fuente redirige. Revisa la URL"
                )

            # Cualquier otro codigo distinto de 200 es un error que no se reintenta
            # (por ejemplo 401 token invalido o 404 serie inexistente).
            if codigo != 200:
                detalle = getattr(respuesta, "text", "Sin información adicional")
                raise RuntimeError(
                    f"Error HTTP {codigo}. Detalle: {str(detalle)[:1000]}"
                    )

            # Exito.
            duracion = time.monotonic() - inicio
            self.logger.info("%s - consulta exitosa. HTTP %s. %s", dominio, codigo, url_log)
            return respuesta, self._metadatos(url, respuesta, duracion, intento)

        # Si llegamos aqui, todos los intentos fallaron.
        raise RuntimeError(f"Se agotaron los {intentos} intentos ({motivo})")

    # -- Cierre -------------------------------------------------------------

    def cerrar(self):
        """Cierra las conexiones abiertas."""
        self.sesion.close()

    # Permite usar:  with ExtractorEtico() as ext:  ... (se cierra solo)
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cerrar()


# ---------------------------------------------------------------------------
# Utilidades que usara main.py
# ---------------------------------------------------------------------------


def guardar_bronce(fuente, nombre, metadatos, datos):
    """
    Guarda los datos originales en la capa Bronce.
    Cada captura recibe un archivo independiente.
    """

    import uuid

    fecha_utc = ahora_utc()

    fecha = fecha_utc.strftime("%Y-%m-%d")
    hora = fecha_utc.strftime("%H%M%S_%f")

    carpeta = RAIZ / "data" / "bronce" / fuente / fecha
    carpeta.mkdir(parents=True, exist_ok=True)

    nombre_archivo = f"{nombre}_{hora}_{uuid.uuid4().hex[:8]}.json"
    ruta = carpeta / nombre_archivo

    contenido = {
        "metadata": metadatos,
        "data": datos
    }

    with ruta.open("x", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, ensure_ascii=False, indent=2)

    return ruta



def registrar_ejecucion(fuente, serie, exito, segundos, detalle=""):
    """Agrega una fila a logs/capturas.csv por cada ejecucion.

    De este archivo saldran en E1 la tasa de exito, el MTBF, el MTTR y la
    disponibilidad del observatorio.
    """
    ruta = RAIZ / "logs" / "capturas.csv"
    ruta.parent.mkdir(exist_ok=True)
    es_nuevo = not ruta.exists()

    with ruta.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if es_nuevo:
            escritor.writerow(
                ["fecha_utc", "fuente", "serie", "exito", "segundos", "detalle"]
            )
        escritor.writerow(
            [ahora_utc().isoformat(), fuente, serie, int(exito), round(segundos, 2), detalle]
        )
