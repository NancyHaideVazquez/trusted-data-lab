
import pandas as pd
import pytest

import pipeline.publicacion as publicacion


def test_publicacion_correcta(tmp_path):
    plata = tmp_path / "plata.csv"
    oro = tmp_path / "oro.csv"

    datos = pd.DataFrame({
        "valor": [1, 2, 3]
    })

    publicacion.publicar_tablas({
        plata: datos,
        oro: datos
    })

    assert plata.exists()
    assert oro.exists()

    assert len(pd.read_csv(plata)) == 3
    assert len(pd.read_csv(oro)) == 3


def test_recuperacion_si_falla_publicacion(
    monkeypatch, tmp_path
):
    plata = tmp_path / "plata.csv"
    oro = tmp_path / "oro.csv"

    plata.write_text(
        "version_anterior_plata",
        encoding="utf-8"
    )
    oro.write_text(
        "version_anterior_oro",
        encoding="utf-8"
    )

    datos_nuevos = pd.DataFrame({
        "valor": [100, 200]
    })

    reemplazar_original = publicacion.os.replace
    llamadas = {"cantidad": 0}

    def reemplazo_controlado(origen, destino):
        llamadas["cantidad"] += 1

        # Provocar error durante la segunda publicación
        if llamadas["cantidad"] == 2:
            raise OSError(
                "Error de escritura simulado"
            )

        return reemplazar_original(origen, destino)

    monkeypatch.setattr(
        publicacion.os,
        "replace",
        reemplazo_controlado
    )

    with pytest.raises(OSError):
        publicacion.publicar_tablas({
            plata: datos_nuevos,
            oro: datos_nuevos
        })

    assert plata.read_text(
        encoding="utf-8"
    ) == "version_anterior_plata"

    assert oro.read_text(
        encoding="utf-8"
    ) == "version_anterior_oro"

    # No deben quedar archivos temporales
    assert not list(tmp_path.glob(".tdl_*"))


def test_no_permite_rutas_duplicadas(tmp_path):
    ruta = tmp_path / "datos.csv"

    # Dos representaciones de la misma ruta
    tablas = {
        ruta: pd.DataFrame({"valor": [1]}),
        str(ruta): pd.DataFrame({"valor": [2]})
    }

    with pytest.raises(ValueError):
        publicacion.publicar_tablas(tablas)
