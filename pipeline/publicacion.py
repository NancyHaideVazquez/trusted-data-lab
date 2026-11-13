
import os
import shutil
import tempfile
from pathlib import Path


def crear_temporal(carpeta, sufijo):
    """Crea una ruta temporal dentro de la carpeta destino."""
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=carpeta,
        prefix=".tdl_",
        suffix=sufijo,
        delete=False
    ) as archivo:
        return Path(archivo.name)


def publicar_tablas(tablas):
    """
    Publica varios DataFrames de forma protegida.

    1. Prepara todos los CSV temporales.
    2. Respalda las versiones anteriores.
    3. Reemplaza los archivos finales.
    4. Si falla un reemplazo, intenta restaurar
       los archivos que ya fueron reemplazados.
    """
    temporales = {}
    respaldos = {}
    reemplazados = []
    destinos = [Path(ruta) for ruta in tablas]

    if len(set(destinos)) != len(destinos):
        raise ValueError("Hay rutas de salida duplicadas.")

    try:
        # Preparar todas las salidas antes de publicar
        for destino, datos in tablas.items():
            destino = Path(destino)
            destino.parent.mkdir(parents=True, exist_ok=True)

            temporal = crear_temporal(
                destino.parent, ".csv"
            )
            temporales[destino] = temporal

            datos.to_csv(temporal, index=False)

        # Respaldar las publicaciones anteriores
        for destino in destinos:
            if destino.exists():
                respaldo = crear_temporal(
                    destino.parent, ".bak"
                )
                respaldos[destino] = respaldo
                shutil.copy2(destino, respaldo)

        # Publicar las salidas preparadas
        for destino in destinos:
            os.replace(temporales[destino], destino)
            reemplazados.append(destino)

    except Exception:
        # Intentar recuperar la situación anterior
        errores_recuperacion = []

        for destino in reversed(reemplazados):
            try:
                if destino in respaldos:
                    os.replace(
                        respaldos[destino], destino
                    )
                else:
                    destino.unlink(missing_ok=True)
            except OSError as error:
                errores_recuperacion.append(
                    f"{destino}: {error}"
                )

        if errores_recuperacion:
            raise RuntimeError(
                "Fallo la publicacion y no se pudo "
                "restaurar todo: "
                + "; ".join(errores_recuperacion)
            )

        raise

    finally:
        # Limpiar archivos temporales restantes
        for temporal in temporales.values():
            temporal.unlink(missing_ok=True)

        for respaldo in respaldos.values():
            respaldo.unlink(missing_ok=True)
