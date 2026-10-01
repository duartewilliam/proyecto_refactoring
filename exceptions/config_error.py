"""Excepciones de configuración."""
from exceptions.base import AppError


class ConfigError(AppError):
    """Error en la configuración de la aplicación."""

    def __init__(self, clave: str = ""):
        self.clave = clave
        super().__init__(
            f"Error de configuración en: {clave}" if clave
            else "Error de configuración"
        )