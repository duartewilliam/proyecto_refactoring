"""Excepciones personalizadas de la aplicación."""
from exceptions.base import AppError
from exceptions.movie_not_found import MovieNotFoundError
from exceptions.series_not_found import SeriesNotFoundError
from exceptions.api_error import (
    ApiRequestError,
    ApiTimeoutError,
    ApiConnectionError,
    InvalidDataError,
)
from exceptions.storage_error import (
    StorageError,
    DataImportError,
    DataExportError,
)
from exceptions.config_error import ConfigError

__all__ = [
    "AppError",
    "MovieNotFoundError",
    "SeriesNotFoundError",
    "ApiRequestError",
    "ApiTimeoutError",
    "ApiConnectionError",
    "InvalidDataError",
    "StorageError",
    "DataImportError",
    "DataExportError",
    "ConfigError",
]