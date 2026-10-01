"""Tests de integración de api/tvmaze.py: construcción de URLs (hacer_request mockeado)."""
from api import tvmaze


def test_buscar_por_nombre_construye_url(mocker):
    respuesta = [{"show": {"id": 1, "name": "Dark"}}]
    mock_request = mocker.patch("api.tvmaze.hacer_request", return_value=respuesta)
    esperado = f"{tvmaze.BASE_URL_TVMAZE}/search/shows?q=Dark"

    resultado = tvmaze.buscar_por_nombre("Dark")

    assert resultado == respuesta
    mock_request.assert_called_once_with(esperado)


def test_obtener_por_id_construye_url(mocker):
    respuesta = {"id": 5, "name": "Dark"}
    mock_request = mocker.patch("api.tvmaze.hacer_request", return_value=respuesta)
    esperado = f"{tvmaze.BASE_URL_TVMAZE}/shows/5"

    resultado = tvmaze.obtener_por_id(5)

    assert resultado == respuesta
    mock_request.assert_called_once_with(esperado)