"""Cliente de la API de OMDb (películas)."""
from typing import Any
from config import get
from constants import (
    URL_PARAM_TITULO,
    URL_PARAM_BUSQUEDA,
    URL_PARAM_TIPO_PELICULA,
    URL_PARAM_API_KEY,
)
from api.http_client import hacer_request

API_KEY_OMDB: str = get("omdb_api_key")
BASE_URL_OMDB: str = get("omdb_base_url")


def buscar_por_titulo(titulo: str) -> Any:
    """Busca por título en OMDb (respuesta cruda)."""
    url = f"{BASE_URL_OMDB}{URL_PARAM_TITULO}{titulo}{URL_PARAM_API_KEY}{API_KEY_OMDB}"
    return hacer_request(url)


def buscar_por_actor(actor: str) -> Any:
    """Busca películas por actor en OMDb (respuesta cruda)."""
    url = f"{BASE_URL_OMDB}{URL_PARAM_BUSQUEDA}{actor}{URL_PARAM_TIPO_PELICULA}{URL_PARAM_API_KEY}{API_KEY_OMDB}"
    return hacer_request(url)