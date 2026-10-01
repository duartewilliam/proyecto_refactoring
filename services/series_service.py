"""Servicio de series: orquestación y cache."""
import logging
from typing import Any
from constants import PREFIX_CACHE_SERIES
from api import tvmaze

logger = logging.getLogger(__name__)

CACHE_SERIES: dict[str, Any] = {}


def buscar_series(nombre: str) -> list:
    """Busca series en TVMaze"""
    global CACHE_SERIES

    cache_key = f"{PREFIX_CACHE_SERIES}{nombre}"
    if cache_key in CACHE_SERIES:
        return CACHE_SERIES[cache_key]

    data = tvmaze.buscar_por_nombre(nombre)

    CACHE_SERIES[cache_key] = data
    return data


def obtener_detalles_serie(id_serie: int) -> Any:
    """Obtiene detalles de serie"""
    return tvmaze.obtener_por_id(id_serie)