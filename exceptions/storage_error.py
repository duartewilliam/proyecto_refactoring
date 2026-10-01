"""Excepciones de almacenamiento (importar/exportar JSON)."""
from exceptions.base import AppError


class StorageError(AppError):
    """Error de acceso a archivos de datos."""

    def __init__(self, nombre_archivo: str = ""):
        self.nombre_archivo = nombre_archivo
        super().__init__(
            f"Error de almacenamiento en: {nombre_archivo}" if nombre_archivo
            else "Error de almacenamiento"
        )


class DataImportError(StorageError):
    """Error al importar datos desde un archivo."""


class DataExportError(StorageError):
    """Error al exportar datos hacia un archivo."""