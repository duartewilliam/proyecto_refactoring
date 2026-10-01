"""Excepciones de series no encontradas."""
from exceptions.base import AppError


class SeriesNotFoundError(AppError):
    """No se encontró ninguna serie en TVMaze."""

    def __init__(self, nombre: str = ""):
        self.nombre = nombre
        super().__init__(
            f"No se encontró la serie: {nombre}" if nombre
            else "No se encontró la serie"
        )