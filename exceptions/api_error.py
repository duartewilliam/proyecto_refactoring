"""Excepciones de errores de API externa (OMDb, TVMaze)."""
from exceptions.base import AppError


class ApiRequestError(AppError):
    """Error al realizar un request a una API externa."""

    def __init__(self, endpoint: str = ""):
        self.endpoint = endpoint
        super().__init__(
            f"Error al consultar la API: {endpoint}" if endpoint
            else "Error al consultar la API"
        )


class ApiTimeoutError(ApiRequestError):
    """La API tardó demasiado en responder."""


class ApiConnectionError(ApiRequestError):
    """No se pudo conectar con la API."""


class InvalidDataError(AppError):
    """Los datos recibidos de la API no tienen el formato esperado."""