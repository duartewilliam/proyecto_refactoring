"""Cliente HTTP compartido para las APIs OMDB y TVMaze."""
import logging
import requests
from typing import Any
from config import get

logger = logging.getLogger(__name__)

CONFIG: dict[str, Any] = {
    "debug": get("debug"),
    "verbose": get("verbose"),
    "timeout": get("timeout"),
    "max_retries": get("max_retries"),
}


def hacer_request(url: str, params: dict | None = None) -> Any:
    """Hace request sin manejo de errores"""
    logger.debug("Haciendo request a %s", url)

    response = requests.get(url, params=params, timeout=CONFIG["timeout"])

    logger.info("Status code: %s", response.status_code)

    return response.json()