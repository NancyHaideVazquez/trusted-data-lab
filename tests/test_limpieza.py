import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.limpieza import imputar


def test_interpolacion_por_fecha_y_grupo_sin_modificar_original():
    datos = pd.DataFrame({
        'serie_id': ['A', 'B', 'A', 'B', 'A', 'B'],
        'fecha': ['2026-01-01', '2026-01-01', '2026-02-01', '2026-02-01', '2026-03-01', '2026-03-01'],
        'valor': [10., 100., None, None, 30., 300.],
    })
    copia = datos.copy(deep=True)
    limpio, reporte = imputar(datos, {'fecha_col': 'fecha', 'grupo_col': 'serie_id', 'metodos': {'valor': 'interpolacion_temporal'}})
    assert limpio.loc[2, 'valor'] == pytest.approx(20.5084745763)
    assert limpio.loc[3, 'valor'] == pytest.approx(205.0847457627)
    assert limpio['valor_imputado'].tolist() == [False, False, True, True, False, False]
    assert reporte.iloc[0]['cantidad_imputada'] == 2
    assert_frame_equal(datos, copia)


def test_no_extrapola_ni_inventa_ceros():
    df = pd.DataFrame({'fecha': ['2026-01-01', '2026-02-01', '2026-03-01'], 'valor': [None, 5., None]})
    result, report = imputar(df, {'metodos': {'valor': 'interpolacion_temporal'}})
    assert result['valor'].isna().sum() == 2
    assert report.iloc[0]['cantidad_imputada'] == 0


def test_ffill_respetando_grupo_y_orden_temporal():
    df = pd.DataFrame({'grupo': ['A', 'B', 'A', 'B'], 'fecha': ['2026-02-01', '2026-02-01', '2026-01-01', '2026-01-01'], 'v': [None, None, 4., 7.]})
    result, _ = imputar(df, {'grupo_col': 'grupo', 'metodos': {'v': 'ffill'}})
    assert result['v'].tolist() == [4., 7., 4., 7.]


def test_mediana_por_grupo_no_global():
    df = pd.DataFrame({'grupo': ['A', 'A', 'A', 'B', 'B'], 'v': [1., None, 9., 100., None]})
    result, _ = imputar(df, {'grupo_col': 'grupo', 'metodos': {'v': 'mediana_por_grupo'}})
    assert result['v'].tolist() == [1., 5., 9., 100., 100.]


@pytest.mark.parametrize('columna', ['id', 'serie_id', 'fecha', 'clave_predio', 'codigo_fuente', 'periodo'])
def test_prohibe_identificadores(columna):
    df = pd.DataFrame({columna: [None, 'a']})
    with pytest.raises(ValueError, match='Prohibido'):
        imputar(df, {'metodos': {columna: 'ffill'}})


def test_n_e_no_se_imputa_silenciosamente():
    df = pd.DataFrame({'fecha': ['2026-01-01', '2026-02-01'], 'valor': ['N/E', None]})
    # Como 'N/E' no es NaN, la funciÃ³n debe detenerse antes de propagarlo.
    # Este caso se resuelve en el diagnÃ³stico/normalizaciÃ³n de marcadores.
    with pytest.raises(ValueError, match='marcadores'):
        imputar(df, {'metodos': {'valor': 'ffill'}})

from src.limpieza import detectar_atipicos_iqr


def test_iqr_marca_extremo_sin_eliminar_ni_modificar_original():
    datos = pd.DataFrame({"serie_id": ["A"] * 6, "valor": [1., 2., 2., 3., 3., 99.]})
    original = datos.copy(deep=True)
    resultado, reporte = detectar_atipicos_iqr(datos, "valor", "serie_id")
    assert len(resultado) == 6
    assert resultado["valor"].tolist() == datos["valor"].tolist()
    assert resultado["es_atipico"].tolist() == [False] * 5 + [True]
    assert resultado.loc[5, "clasificacion_atipico"] == "por_revisar"
    assert int(reporte.loc[0, "cantidad_atipicos"]) == 1
    assert_frame_equal(datos, original)


def test_iqr_no_mezcla_series():
    datos = pd.DataFrame({"serie": ["A"] * 5 + ["B"] * 5,
                          "valor": [1., 1., 1., 1., 1., 100., 100., 100., 100., 100.]})
    resultado, reporte = detectar_atipicos_iqr(datos, "valor", "serie")
    assert not resultado["es_atipico"].any()
    assert len(reporte) == 2


def test_iqr_grupos_pequenos_no_son_errores():
    datos = pd.DataFrame({"serie": ["A", "A", "A"], "valor": [1., 2., 50.]})
    resultado, reporte = detectar_atipicos_iqr(datos, "valor", "serie")
    assert not resultado["es_atipico"].any()
    assert (resultado["clasificacion_atipico"] == "no_evaluado").all()
    assert reporte.loc[0, "estado"] == "insuficientes_datos"


def test_iqr_rechaza_fechas_e_identificadores():
    datos = pd.DataFrame({"serie_id": [1, 2, 3, 4], "valor": [1., 2., 3., 4.]})
    with pytest.raises(ValueError, match="identificadores"):
        detectar_atipicos_iqr(datos, "serie_id")

from src.limpieza import preparar_serie, limpieza_conservadora


def test_banxico_n_e_se_conserva_como_no_publicado_sin_imputacion():
    entrada = pd.DataFrame({'fecha': ['1995-03-23', '1995-03-24', '1995-03-27', '1995-03-28'],
                            'dato': ['N/E', '5.5', 'N/E', '6.2']})
    copia = entrada.copy(deep=True)
    salida, reporte = preparar_serie(entrada, 'banxico')
    assert len(salida) == 4
    assert salida['valor'].isna().sum() == 2
    assert salida['valor_imputado'].sum() == 0
    assert (salida.loc[salida['valor'].isna(), 'motivo_revision'] == 'no_publicado').all()
    assert reporte.iloc[0]['faltantes_no_publicados'] == 2
    assert_frame_equal(entrada, copia)


def test_inegi_acepta_valores_negativos_y_sin_imputacion():
    entrada = pd.DataFrame({'TIME_PERIOD': ['2026-08-01', '2026-09-01', '2026-10-01', '2026-11-01'],
                            'OBS_VALUE': ['-0.24', '0.18', '0.30', '0.82']})
    salida, reporte, extremos = limpieza_conservadora(entrada, 'inegi')
    assert len(salida) == 4
    assert salida['valor'].min() == pytest.approx(-0.24)
    assert reporte.iloc[0]['registros_imputados'] == 0
    assert reporte.iloc[0]['faltantes_no_publicados'] == 0
    assert 'es_atipico' in salida
    assert len(extremos) == 1


def test_valor_no_numerico_tiene_motivo_sin_eliminar():
    df = pd.DataFrame({'fecha': ['2026-01-02', '2026-01-03'], 'dato': ['texto?', '1.25']})
    salida, reporte = preparar_serie(df, 'banxico')
    assert len(salida) == 2
    assert reporte.iloc[0]['valores_no_numericos'] == 1
    assert salida.iloc[0]['motivo_revision'] == 'valor_no_numerico'


def test_fechas_invalidas_se_marcan_y_conservan():
    df = pd.DataFrame({'fecha': ['no-fecha', '2026-01-03'], 'dato': ['2.3', '2.1']})
    salida, reporte = preparar_serie(df, 'banxico')
    assert len(salida) == 2
    assert reporte.iloc[0]['fechas_invalidas'] == 1
    assert salida.iloc[0]['estado_valor'] == 'fecha_invalida'


def test_limpieza_no_borra_atipico_extremo():
    df = pd.DataFrame({'fecha': pd.date_range('2026-01-01', periods=6).astype(str),
                       'dato': ['1', '2', '2', '3', '3', '90.5']})
    salida, resumen, _ = limpieza_conservadora(df, 'banxico')
    assert len(salida) == len(df)
    assert salida['es_atipico'].sum() == 1
    assert salida.iloc[-1]['clasificacion_atipico'] == 'por_revisar'
    assert resumen.iloc[0]['registros_eliminados'] == 0


def test_fecha_banxico_dia_mes_anio():
    datos = pd.DataFrame({'fecha': ['23/03/1995', '04/05/1995'], 'dato': ['10', '11']})
    salida, _ = preparar_serie(datos, 'banxico')
    assert salida['fecha'].dt.strftime('%Y-%m-%d').tolist() == ['1995-03-23', '1995-05-04']