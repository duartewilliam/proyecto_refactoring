"""Validación de entradas de usuario para la capa UI."""
from typing import Any

LIMITE_LONGITUD_BUSQUEDA = 120
LIMITE_LONGITUD_NOMBRE = 100
TIMEOUT_MINIMO = 1
TIMEOUT_MAXIMO = 300

GENEROS_VALIDOS = ("accion", "comedia")


def validar_texto_busqueda(texto: str) -> str | None:
    """Normaliza y valida un texto de búsqueda; None si es inválido."""
    texto_limpio = texto.strip()
    if not texto_limpio:
        return None
    if len(texto_limpio) > LIMITE_LONGITUD_BUSQUEDA:
        return None
    return texto_limpio


def validar_genero(genero: str) -> str | None:
    """Normaliza y valida un género; solo acepta los géneros conocidos."""
    genero_limpio = genero.strip().lower()
    if genero_limpio not in GENEROS_VALIDOS:
        return None
    return genero_limpio


def validar_nombre_archivo(nombre: str) -> str | None:
    """Normaliza y valida un nombre de archivo (sin directorios)."""
    nombre_limpio = nombre.strip()
    if not nombre_limpio:
        return None
    if len(nombre_limpio) > LIMITE_LONGITUD_NOMBRE:
        return None
    if nombre_limpio in (".", ".."):
        return None
    if "/" in nombre_limpio or "\\" in nombre_limpio:
        return None
    return nombre_limpio


def validar_entero(texto: str, minimo: int, maximo: int) -> int | None:
    """Convierte y valida un entero dentro del rango; None si es inválido."""
    try:
        valor = int(texto.strip())
    except ValueError:
        return None
    if valor < minimo or valor > maximo:
        return None
    return valor


def indice_seleccion(opcion: str, tamano: int) -> int | None:
    """Convierte una opción numérica a índice (1-based a 0-based); None si es inválida."""
    opcion_limpia = opcion.strip()
    if not opcion_limpia.isdigit():
        return None
    indice = int(opcion_limpia) - 1
    if indice < 0 or indice >= tamano:
        return None
    return indice