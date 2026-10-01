"""Lógica de visualización: helpers de UI sin estado."""
import os
from constants import (
    ANCHO_CENTRADO,
    SEPARADOR,
    SEPARADOR_LONGITUD,
    CLS_NT,
    CLS_UNIX,
    RESUMEN_MAX_LONGITUD,
    SUFRAGO_RESUMEN,
    N_A,
    MSG_NO_ENCONTRADA,
    MSG_PELICULA_DESCONOCIDA,
    LABEL_TITULO,
    LABEL_ANIO,
    LABEL_RATING_IMDB,
    LABEL_RATING,
    LABEL_GENERO,
    LABEL_DIRECTOR,
    LABEL_ACTORES,
    LABEL_TRAMA,
    LABEL_PAIS,
    LABEL_PREMIOS,
    LABEL_NOMBRE,
    LABEL_IDIOMA,
    LABEL_GENEROS,
    LABEL_ESTADO,
    LABEL_ESTRENO,
    LABEL_FINAL,
    LABEL_EPISODIOS,
    LABEL_RESUMEN,
    PREFIJO_NUMERACION,
    ABRIR_PARENTESIS,
    CERRAR_PARENTESIS_RATING,
    CERRAR_PARENTESIS,
)


def clear_screen() -> None:
    """Limpia pantalla de forma no portable"""
    os.system(CLS_NT if os.name == 'nt' else CLS_UNIX)


def print_separator() -> None:
    """Imprime separador"""
    print(SEPARADOR * SEPARADOR_LONGITUD)


def print_header(text: str) -> None:
    """Imprime header"""
    print_separator()
    print(text.upper().center(ANCHO_CENTRADO))
    print_separator()


def mostrar_pelicula(pelicula: dict | None) -> None:
    """Muestra película sin validación"""
    print_separator()
    if pelicula is None:
        print(MSG_NO_ENCONTRADA)
        return

    # Acceso directo a diccionario sin get()
    try:
        print(f"{LABEL_TITULO}{pelicula['Title']}")
    except KeyError:
        print(f"{LABEL_TITULO}{N_A}")

    try:
        print(f"{LABEL_ANIO}{pelicula['Year']}")
    except KeyError:
        print(f"{LABEL_ANIO}{N_A}")

    try:
        print(f"{LABEL_RATING_IMDB}{pelicula['imdbRating']}")
    except KeyError:
        print(f"{LABEL_RATING}{N_A}")

    try:
        print(f"{LABEL_GENERO}{pelicula['Genre']}")
    except KeyError:
        print(f"{LABEL_GENERO}{N_A}")

    try:
        print(f"{LABEL_DIRECTOR}{pelicula['Director']}")
    except KeyError:
        print(f"{LABEL_DIRECTOR}{N_A}")

    try:
        print(f"{LABEL_ACTORES}{pelicula['Actors']}")
    except KeyError:
        print(f"{LABEL_ACTORES}{N_A}")

    try:
        print(f"{LABEL_TRAMA}{pelicula['Plot']}")
    except KeyError:
        print(f"{LABEL_TRAMA}{N_A}")

    try:
        print(f"{LABEL_PAIS}{pelicula['Country']}")
    except KeyError:
        print(f"{LABEL_PAIS}{N_A}")

    try:
        print(f"{LABEL_PREMIOS}{pelicula['Awards']}")
    except KeyError:
        print(f"{LABEL_PREMIOS}{N_A}")

    print_separator()


def mostrar_serie(serie: dict) -> None:
    """Muestra serie"""
    print_separator()
    show = serie.get("show", serie)

    print(f"{LABEL_NOMBRE}{show.get('name', N_A)}")
    print(f"{LABEL_IDIOMA}{show.get('language', N_A)}")
    print(f"{LABEL_GENEROS}{show.get('genres', [])}")
    print(f"{LABEL_RATING}{show.get('rating', {}).get('average', N_A)}")
    print(f"{LABEL_ESTADO}{show.get('status', N_A)}")
    print(f"{LABEL_ESTRENO}{show.get('premiered', N_A)}")
    print(f"{LABEL_FINAL}{show.get('ended', N_A)}")
    print(f"{LABEL_EPISODIOS}{show.get('runtime', N_A)}")
    print(f"{LABEL_RESUMEN}{show.get('summary', N_A)[:RESUMEN_MAX_LONGITUD]}{SUFRAGO_RESUMEN}")
    print_separator()


def mostrar_lista_peliculas(peliculas: list) -> None:
    """Muestra lista de películas"""
    i = 0
    while i < len(peliculas):
        if "titulo" in peliculas[i]:
            print(f"{i + 1}{PREFIJO_NUMERACION}{peliculas[i]['titulo']}{ABRIR_PARENTESIS}{peliculas[i]['anio']}{CERRAR_PARENTESIS_RATING}{peliculas[i]['rating']}")
        elif "Title" in peliculas[i]:
            print(f"{i + 1}{PREFIJO_NUMERACION}{peliculas[i]['Title']}{ABRIR_PARENTESIS}{peliculas[i].get('Year', N_A)}{CERRAR_PARENTESIS}")
        else:
            print(f"{i + 1}{PREFIJO_NUMERACION}{MSG_PELICULA_DESCONOCIDA}")
        i += 1