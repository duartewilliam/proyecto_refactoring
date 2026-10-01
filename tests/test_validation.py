"""Tests unitarios de los validadores de entrada en ui/validation.py."""
import pytest

from ui.validation import (
    LIMITE_LONGITUD_BUSQUEDA,
    LIMITE_LONGITUD_NOMBRE,
    TIMEOUT_MAXIMO,
    TIMEOUT_MINIMO,
    indice_seleccion,
    validar_entero,
    validar_genero,
    validar_nombre_archivo,
    validar_texto_busqueda,
)


# ---------------------------------------------------------------
# validar_texto_busqueda
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    "entrada",
    [
        "",
        "   ",
        "\n\t",
        "x" * (LIMITE_LONGITUD_BUSQUEDA + 1),
    ],
)
def test_validar_texto_busqueda_invalido(entrada):
    assert validar_texto_busqueda(entrada) is None


def test_validar_texto_busqueda_limpia_y_normaliza():
    assert validar_texto_busqueda("  Inception  ") == "Inception"


def test_validar_texto_busqueda_longitud_maxima_aceptada():
    texto = "x" * LIMITE_LONGITUD_BUSQUEDA
    assert validar_texto_busqueda(texto) == texto


# ---------------------------------------------------------------
# validar_genero
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("accion", "accion"),
        ("  accion ", "accion"),
        ("comedia", "comedia"),
        ("COMEDIA", "comedia"),
        ("Accion", "accion"),
    ],
)
def test_validar_genero_normaliza(entrada, esperado):
    assert validar_genero(entrada) == esperado


@pytest.mark.parametrize(
    "entrada",
    [
        "",
        "   ",
        "horror",
        "Acción",
        "ciencia ficcion",
    ],
)
def test_validar_genero_invalido(entrada):
    assert validar_genero(entrada) is None


# ---------------------------------------------------------------
# validar_nombre_archivo
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    "entrada",
    [
        "",
        "   ",
        ".",
        "..",
        "../evil",
        "subdir/archivo.json",
        "subdir\\archivo.json",
        "a" * (LIMITE_LONGITUD_NOMBRE + 1),
    ],
)
def test_validar_nombre_archivo_invalido(entrada):
    assert validar_nombre_archivo(entrada) is None


def test_validar_nombre_archivo_valido():
    assert validar_nombre_archivo("  respaldo  ") == "respaldo"
    assert validar_nombre_archivo("peliculas.json\n") == "peliculas.json"
    assert "a" * LIMITE_LONGITUD_NOMBRE == validar_nombre_archivo("a" * LIMITE_LONGITUD_NOMBRE)


# ---------------------------------------------------------------
# validar_entero
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    "texto",
    [
        "abc",
        "",
        "1.5",
        "0",
        str(TIMEOUT_MINIMO - 1),
        str(TIMEOUT_MAXIMO + 1),
    ],
)
def test_validar_entero_invalido(texto):
    assert validar_entero(texto, TIMEOUT_MINIMO, TIMEOUT_MAXIMO) is None


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("42", 42),
        ("  5 ", 5),
        (str(TIMEOUT_MINIMO), TIMEOUT_MINIMO),
        (str(TIMEOUT_MAXIMO), TIMEOUT_MAXIMO),
        ("300", 300),
    ],
)
def test_validar_entero_valido(texto, esperado):
    assert validar_entero(texto, TIMEOUT_MINIMO, TIMEOUT_MAXIMO) == esperado


# ---------------------------------------------------------------
# indice_seleccion
# ---------------------------------------------------------------
@pytest.mark.parametrize(
    ("opcion", "tamano"),
    [
        ("", 5),
        ("0", 5),
        ("abc", 5),
        ("6", 5),
        ("1", 0),
        ("-1", 5),
    ],
)
def test_indice_seleccion_invalido(opcion, tamano):
    assert indice_seleccion(opcion, tamano) is None


@pytest.mark.parametrize(
    ("opcion", "tamano", "esperado"),
    [
        ("1", 5, 0),
        ("2", 5, 1),
        ("5", 5, 4),
        (" 3 ", 3, 2),
    ],
)
def test_indice_seleccion_valido(opcion, tamano, esperado):
    assert indice_seleccion(opcion, tamano) == esperado