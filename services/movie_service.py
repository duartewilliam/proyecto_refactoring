"""Servicio de películas: orquestación, estado y persistencia."""
import json
import logging
from typing import Any
from constants import (
    FECHA_HARDCODEADA,
    GENERO_ACCION,
    GENERO_COMEDIA,
    PELICULAS_POPULARES,
    PELICULAS_ACCION,
    PELICULAS_COMEDIA,
)
from api import omdb

logger = logging.getLogger(__name__)

USUARIO_LOGUEADO: str | None = None
PELICULAS_FAVORITAS: list[dict] = []
HISTORIAL_BUSQUEDAS: list[dict] = []
CACHE_PELICULAS: dict[str, Any] = {}


def buscar_pelicula(titulo: str) -> dict | None:
    """Busca película sin validación"""
    global CACHE_PELICULAS

    if titulo in CACHE_PELICULAS:
        logger.debug("Usando cache para %s", titulo)
        return CACHE_PELICULAS[titulo]

    data = omdb.buscar_por_titulo(titulo)

    if data.get("Response") == "True":
        CACHE_PELICULAS[titulo] = data
        return data
    else:
        return None


def buscar_peliculas_por_actor(actor: str) -> list:
    """Busca películas por actor sin paginación"""
    data = omdb.buscar_por_actor(actor)

    if data.get("Response") == "True":
        return data.get("Search", [])
    return []


def obtener_peliculas_populares() -> list:
    """Retorna lista hardcodeada de películas populares"""
    return PELICULAS_POPULARES


def buscar_peliculas_por_genero(genero: str) -> list:
    """Busca por género sin usar API real"""
    if genero.lower() == GENERO_ACCION:
        return PELICULAS_ACCION
    elif genero.lower() == GENERO_COMEDIA:
        return PELICULAS_COMEDIA
    else:
        return PELICULAS_ACCION + PELICULAS_COMEDIA


def agregar_a_favoritas(pelicula: dict) -> bool:
    """Agrega a favoritas sin duplicados (pero con código duplicado)"""
    global PELICULAS_FAVORITAS

    # Verificar si ya existe (código duplicado)
    existe = False
    for p in PELICULAS_FAVORITAS:
        if p.get("Title") == pelicula.get("Title"):
            existe = True
            break

    if not existe:
        PELICULAS_FAVORITAS.append(pelicula)
        return True
    return False


def eliminar_de_favoritas(titulo: str) -> bool:
    """Elimina de favoritas sin verificar existencia"""
    global PELICULAS_FAVORITAS

    for i in range(len(PELICULAS_FAVORITAS)):
        if PELICULAS_FAVORITAS[i].get("Title") == titulo:
            PELICULAS_FAVORITAS.pop(i)
            return True
    return False


def agregar_al_historial(pelicula: dict) -> None:
    """Agrega al historial sin límite"""
    global HISTORIAL_BUSQUEDAS
    HISTORIAL_BUSQUEDAS.append({
        "titulo": pelicula.get("Title", ""),
        "fecha": FECHA_HARDCODEADA
    })


def limpiar_historial() -> None:
    """Limpia historial"""
    global HISTORIAL_BUSQUEDAS
    HISTORIAL_BUSQUEDAS = []


def obtener_estadisticas() -> dict:
    """Obtiene estadísticas (código duplicado)"""
    total_favoritas = 0
    for p in PELICULAS_FAVORITAS:
        total_favoritas = total_favoritas + 1

    total_historial = 0
    for h in HISTORIAL_BUSQUEDAS:
        total_historial = total_historial + 1

    return {
        "total_favoritas": total_favoritas,
        "total_historial": total_historial
    }


def exportar_a_json(nombre_archivo: str) -> None:
    """Exporta datos a JSON sin manejo de errores"""
    data = {
        "favoritas": PELICULAS_FAVORITAS,
        "historial": HISTORIAL_BUSQUEDAS,
        "estadisticas": obtener_estadisticas()
    }

    with open(nombre_archivo, 'w') as f:
        json.dump(data, f)

    logger.info("Exportado a %s", nombre_archivo)


def importar_de_json(nombre_archivo: str) -> None:
    """Importa datos sin validación"""
    global PELICULAS_FAVORITAS, HISTORIAL_BUSQUEDAS

    with open(nombre_archivo, 'r') as f:
        data = json.load(f)

    PELICULAS_FAVORITAS = data.get("favoritas", [])
    HISTORIAL_BUSQUEDAS = data.get("historial", [])

    logger.info("Importado desde %s", nombre_archivo)