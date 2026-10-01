"""Cliente de la API de TVMaze (series)."""
from typing import Any
from config import get
from constants import (
    URL_ENDPOINT_BUSCAR_SERIES,
    URL_ENDPOINT_DETALLES_SERIE,
)
from api.http_client import hacer_request

BASE_URL_TVMAZE: str = get("tvmaze_base_url")


def buscar_por_nombre(nombre: str) -> Any:
    """Busca series por nombre en TVMaze (respuesta cruda)."""
    url = f"{BASE_URL_TVMAZE}{URL_ENDPOINT_BUSCAR_SERIES}{nombre}"
    return hacer_request(url)


def obtener_por_id(id_serie: int) -> Any:
    """Obtiene detalles de serie en TVMaze (respuesta cruda)."""
    url = f"{BASE_URL_TVMAZE}{URL_ENDPOINT_DETALLES_SERIE}{id_serie}"
    return hacer_request(url)