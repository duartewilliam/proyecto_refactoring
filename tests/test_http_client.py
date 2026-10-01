"""Tests de integración de api/http_client.py: transporte mockeado (sin red)."""
from api import http_client


def test_hacer_request_envia_get_con_params_y_timeout(mocker):
    respuesta = mocker.Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {"Resultado": "ok"}
    mock_get = mocker.patch("requests.get", return_value=respuesta)

    resultado = http_client.hacer_request("http://ejemplo.test/a", params={"t": "Inception"})

    assert resultado == {"Resultado": "ok"}
    mock_get.assert_called_once_with(
        "http://ejemplo.test/a",
        params={"t": "Inception"},
        timeout=http_client.CONFIG["timeout"],
    )


def test_hacer_request_devuelve_json_de_la_respuesta(mocker):
    respuesta = mocker.Mock()
    respuesta.json.return_value = [{"show": {"id": 1}}]
    mocker.patch("requests.get", return_value=respuesta)

    resultado = http_client.hacer_request("http://ejemplo.test/series")

    assert resultado == [{"show": {"id": 1}}]