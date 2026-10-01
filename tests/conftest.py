"""Fixtures compartidas para los tests de la Fase 6."""
import pytest

import services.movie_service as movie_service
import services.series_service as series_service
import ui.menu as menu


@pytest.fixture(autouse=True)
def reset_estado_servicios():
    """Resetea el estado global de los servicios antes de cada test.

    `limpiar_historial`/`importar_de_json` reasignan los globales de módulo, con lo que
    las referencias capturadas por `ui.menu` (from services.movie_service import ...)
    dejarían de apuntar a las mismas listas. Se re-enlazan antes de limpiar.
    """
    menu.HISTORIAL_BUSQUEDAS = movie_service.HISTORIAL_BUSQUEDAS
    menu.PELICULAS_FAVORITAS = movie_service.PELICULAS_FAVORITAS
    movie_service.PELICULAS_FAVORITAS.clear()
    movie_service.HISTORIAL_BUSQUEDAS.clear()
    movie_service.CACHE_PELICULAS.clear()
    series_service.CACHE_SERIES.clear()
    yield