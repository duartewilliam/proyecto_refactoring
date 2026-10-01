"""Excepciones de películas no encontradas."""
from exceptions.base import AppError


class MovieNotFoundError(AppError):
    """No se encontró ninguna película en OMDb."""

    def __init__(self, titulo: str = ""):
        self.titulo = titulo
        super().__init__(
            f"No se encontró la película: {titulo}" if titulo
            else "No se encontró la película"
        )