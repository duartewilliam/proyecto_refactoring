"""Tests unitarios de ui/display.py: salida capturada con capsys."""
import os

from constants import (
    ABRIR_PARENTESIS,
    CERRAR_PARENTESIS,
    CERRAR_PARENTESIS_RATING,
    MSG_NO_ENCONTRADA,
    MSG_PELICULA_DESCONOCIDA,
    PREFIJO_NUMERACION,
    SEPARADOR,
    SEPARADOR_LONGITUD,
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
)
from ui import display

PELICULA = {
    "Title": "Inception",
    "Year": "2010",
    "imdbRating": "8.8",
    "Genre": "Sci-Fi",
    "Director": "Nolan",
    "Actors": "DiCaprio",
    "Plot": "Un ladrón que roba secretos corporativos.",
    "Country": "USA",
    "Awards": "Oscar",
}


# ---------------------------------------------------------------
# clear_screen / separador / header
# ---------------------------------------------------------------
def test_clear_screen_usa_comando_del_sistema(mocker):
    mock_system = mocker.patch("ui.display.os.system")
    display.clear_screen()
    mock_system.assert_called_once_with("cls" if os.name == "nt" else "clear")


def test_print_separator(capsys):
    display.print_separator()
    assert capsys.readouterr().out == SEPARADOR * SEPARADOR_LONGITUD + "\n"


def test_print_header(capsys):
    display.print_header("Mi Título")
    salida = capsys.readouterr().out
    assert SEPARADOR * SEPARADOR_LONGITUD in salida
    assert "MI TÍTULO" in salida


# ---------------------------------------------------------------
# mostrar_pelicula
# ---------------------------------------------------------------
def test_mostrar_pelicula_none(capsys):
    display.mostrar_pelicula(None)
    assert MSG_NO_ENCONTRADA in capsys.readouterr().out


def test_mostrar_pelicula_completa(capsys):
    display.mostrar_pelicula(PELICULA)
    salida = capsys.readouterr().out
    assert f"{LABEL_TITULO}Inception" in salida
    assert f"{LABEL_ANIO}2010" in salida
    assert f"{LABEL_RATING_IMDB}8.8" in salida
    assert f"{LABEL_GENERO}Sci-Fi" in salida
    assert f"{LABEL_DIRECTOR}Nolan" in salida
    assert f"{LABEL_ACTORES}DiCaprio" in salida
    assert f"{LABEL_TRAMA}Un ladrón que roba secretos corporativos." in salida
    assert f"{LABEL_PAIS}USA" in salida
    assert f"{LABEL_PREMIOS}Oscar" in salida


def test_mostrar_pelicula_con_campos_faltantes(capsys):
    display.mostrar_pelicula({"Title": "Solo titulo"})
    salida = capsys.readouterr().out
    assert f"{LABEL_TITULO}Solo titulo" in salida
    assert f"{LABEL_ANIO}N/A" in salida
    assert f"{LABEL_RATING}N/A" in salida


def test_mostrar_pelicula_sin_titulo(capsys):
    display.mostrar_pelicula({})
    salida = capsys.readouterr().out
    assert f"{LABEL_TITULO}N/A" in salida


# ---------------------------------------------------------------
# mostrar_serie
# ---------------------------------------------------------------
def test_mostrar_serie_con_wrapper(capsys):
    serie = {
        "show": {
            "name": "Dark",
            "language": "Alemán",
            "genres": ["Drama"],
            "rating": {"average": 8.7},
            "status": "Ended",
            "premiered": "2017-12-01",
            "ended": "2020-06-27",
            "runTime": 53,
            "runtime": 53,
            "summary": "x" * 300,
        }
    }
    display.mostrar_serie(serie)
    salida = capsys.readouterr().out
    assert f"{LABEL_NOMBRE}Dark" in salida
    assert f"{LABEL_IDIOMA}Alemán" in salida
    assert f"{LABEL_GENEROS}['Drama']" in salida
    assert f"{LABEL_RATING}8.7" in salida
    assert f"{LABEL_ESTADO}Ended" in salida
    assert f"{LABEL_ESTRENO}2017-12-01" in salida
    assert f"{LABEL_FINAL}2020-06-27" in salida
    assert f"{LABEL_EPISODIOS}53" in salida
    assert f"{LABEL_RESUMEN}{'x' * 200}..." in salida


def test_mostrar_serie_sin_wrapper_usa_n_a(capsys):
    display.mostrar_serie({"name": "Elite"})
    salida = capsys.readouterr().out
    assert f"{LABEL_NOMBRE}Elite" in salida
    assert f"{LABEL_RATING}N/A" in salida
    assert f"{LABEL_ESTADO}N/A" in salida


# ---------------------------------------------------------------
# mostrar_lista_peliculas
# ---------------------------------------------------------------
def test_mostrar_lista_con_claves_minusculas(capsys):
    display.mostrar_lista_peliculas([{"titulo": "T", "anio": 2000, "rating": 7.5}])
    salida = capsys.readouterr().out
    assert f"1{PREFIJO_NUMERACION}T{ABRIR_PARENTESIS}2000{CERRAR_PARENTESIS_RATING}7.5" in salida


def test_mostrar_lista_con_claves_omdb(capsys):
    display.mostrar_lista_peliculas([{"Title": "Inception", "Year": "2010"}])
    salida = capsys.readouterr().out
    assert f"1{PREFIJO_NUMERACION}Inception{ABRIR_PARENTESIS}2010{CERRAR_PARENTESIS}" in salida


def test_mostrar_lista_sin_campos_reconocidos(capsys):
    display.mostrar_lista_peliculas([{"otro": "dato"}])
    assert MSG_PELICULA_DESCONOCIDA in capsys.readouterr().out