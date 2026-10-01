"""Tests de las excepciones personalizadas (exceptions/)."""
import pytest

from exceptions import (
    ApiConnectionError,
    ApiRequestError,
    ApiTimeoutError,
    AppError,
    ConfigError,
    DataExportError,
    DataImportError,
    InvalidDataError,
    MovieNotFoundError,
    SeriesNotFoundError,
    StorageError,
)

TODAS = [
    MovieNotFoundError,
    SeriesNotFoundError,
    ApiRequestError,
    ApiTimeoutError,
    ApiConnectionError,
    InvalidDataError,
    StorageError,
    DataImportError,
    DataExportError,
    ConfigError,
]


def test_app_error_es_exception():
    assert issubclass(AppError, Exception)


@pytest.mark.parametrize("exc_cls", TODAS)
def test_todas_las_excepciones_heredan_de_app_error(exc_cls):
    assert issubclass(exc_cls, AppError)


def test_app_error_mensaje():
    error = AppError("algo falló")
    assert str(error) == "algo falló"
    assert error.args == ("algo falló",)


def test_api_request_error_guarda_endpoint():
    error = ApiRequestError("/shows/1")
    assert error.endpoint == "/shows/1"
    assert "/shows/1" in str(error)


def test_api_request_error_sin_endpoint():
    error = ApiRequestError()
    assert error.endpoint == ""
    assert str(error) == "Error al consultar la API"


def test_subtipos_de_api_request_error_vacios():
    assert str(ApiTimeoutError()) == "Error al consultar la API"
    assert str(ApiConnectionError()) == "Error al consultar la API"


def test_excepciones_son_capturables_como_app_error():
    for exc_cls in TODAS:
        try:
            raise exc_cls()
        except AppError:
            pass
        else:
            raise AssertionError(f"{exc_cls.__name__} no fue capturada como AppError")