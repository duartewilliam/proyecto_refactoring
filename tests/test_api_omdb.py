"""Tests de integración de api/omdb.py: construcción de URLs (hacer_request mockeado)."""
from api import omdb

RESPUESTA_OK = {"Response": "True", "Title": "Inception"}


def test_buscar_por_titulo_construye_url(mocker):
    mock_request = mocker.patch("api.omdb.hacer_request", return_value=RESPUESTA_OK)
    esperado = f"{omdb.BASE_URL_OMDB}?t=Inception&apikey={omdb.API_KEY_OMDB}"

    resultado = omdb.buscar_por_titulo("Inception")

    assert resultado == RESPUESTA_OK
    mock_request.assert_called_once_with(esperado)


def test_buscar_por_actor_construye_url(mocker):
    respuesta = {"Response": "True", "Search": []}
    mock_request = mocker.patch("api.omdb.hacer_request", return_value=respuesta)
    esperado = f"{omdb.BASE_URL_OMDB}?s=DiCaprio&type=movie&apikey={omdb.API_KEY_OMDB}"

    resultado = omdb.buscar_por_actor("DiCaprio")

    assert resultado == respuesta
    mock_request.assert_called_once_with(esperado)