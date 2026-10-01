"""Tests unitarios de services/series_service.py (API TVMaze mockeada)."""
from api import tvmaze
from services import series_service

DATOS_SERIES = [{"show": {"id": 1, "name": "Dark"}}]


# ---------------------------------------------------------------
# buscar_series (con cache)
# ---------------------------------------------------------------
def test_buscar_series_devuelve_data_y_usa_cache(mocker):
    mock_buscar = mocker.patch.object(tvmaze, "buscar_por_nombre", return_value=DATOS_SERIES)

    resultado_1 = series_service.buscar_series("Dark")
    resultado_2 = series_service.buscar_series("Dark")

    assert resultado_1 == DATOS_SERIES
    assert resultado_2 == DATOS_SERIES
    assert mock_buscar.call_count == 1
    assert series_service.CACHE_SERIES["series_Dark"] == DATOS_SERIES


def test_buscar_series_claves_distintas_por_nombre(mocker):
    mock_buscar = mocker.patch.object(
        tvmaze, "buscar_por_nombre", side_effect=[DATOS_SERIES, [{"show": {"id": 2}}]]
    )

    series_service.buscar_series("Dark")
    resultado_otra = series_service.buscar_series("Otra")
    series_service.buscar_series("Dark")

    assert resultado_otra == [{"show": {"id": 2}}]
    assert mock_buscar.call_count == 2


# ---------------------------------------------------------------
# obtener_detalles_serie
# ---------------------------------------------------------------
def test_obtener_detalles_serie_passthrough(mocker):
    detalles = {"id": 5, "name": "Dark", "summary": "<p>...</p>"}
    mock_detalle = mocker.patch.object(tvmaze, "obtener_por_id", return_value=detalles)

    assert series_service.obtener_detalles_serie(5) == detalles
    mock_detalle.assert_called_once_with(5)