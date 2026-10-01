"""Tests de ui/menu.py: entrada estándar y funciones de servicio mockeadas."""
import json

import pytest

from constants import (
    HEADER_PELICULAS_POPULARES,
    MSG_AGREGADA_FAVORITOS,
    MSG_BUSQUEDA_INVALIDA,
    MSG_DEBUG_ACTUAL,
    MSG_ELIMINADA_FAVORITOS,
    MSG_ERROR_IMPORTAR,
    MSG_GENERO_INVALIDO,
    MSG_HASTA_LUEGO,
    MSG_HISTORIAL_LIMPIADO,
    MSG_NO_ENCONTRADA,
    MSG_NO_ENCONTRADAS_ACTOR,
    MSG_NO_ENCONTRADAS_SERIES,
    MSG_NOMBRE_ARCHIVO_INVALIDO,
    MSG_OPCION_INVALIDA,
    MSG_SELECCION_INVALIDA,
    MSG_SIN_FAVORITAS,
    MSG_SIN_HISTORIAL,
    MSG_TIMEOUT_INVALIDO,
    MSG_YA_EN_FAVORITOS,
)
from services import movie_service
from ui import menu

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


@pytest.fixture(autouse=True)
def sin_delay(mocker):
    mocker.patch.object(menu, "delay")


# ---------------------------------------------------------------
# Buscar película
# ---------------------------------------------------------------
def test_funcion_buscar_pelicula_sin_favorito(capsys, mocker):
    mocker.patch.object(menu, "buscar_pelicula", return_value=PELICULA)
    mocker.patch("builtins.input", side_effect=["Inception", "n", ""])

    menu.funcion_buscar_pelicula()

    salida = capsys.readouterr().out
    assert "Inception" in salida
    assert MSG_AGREGADA_FAVORITOS not in salida


def test_funcion_buscar_pelicula_agrega_favorito(capsys, mocker):
    mocker.patch.object(menu, "buscar_pelicula", return_value=PELICULA)
    mocker.patch("builtins.input", side_effect=["Inception", "s", ""])

    menu.funcion_buscar_pelicula()

    assert MSG_AGREGADA_FAVORITOS in capsys.readouterr().out
    assert len(movie_service.PELICULAS_FAVORITAS) == 1


def test_funcion_buscar_pelicula_ya_en_favoritos(capsys, mocker):
    movie_service.agregar_a_favoritas(PELICULA)
    mocker.patch.object(menu, "buscar_pelicula", return_value=PELICULA)
    mocker.patch("builtins.input", side_effect=["Inception", "s", ""])

    menu.funcion_buscar_pelicula()

    assert MSG_YA_EN_FAVORITOS in capsys.readouterr().out


def test_funcion_buscar_pelicula_busqueda_invalida(capsys, mocker):
    mocker.patch.object(menu, "buscar_pelicula")
    mocker.patch("builtins.input", side_effect=["   ", ""])

    menu.funcion_buscar_pelicula()

    assert MSG_BUSQUEDA_INVALIDA in capsys.readouterr().out
    menu.buscar_pelicula.assert_not_called()


def test_funcion_buscar_pelicula_no_encontrada(capsys, mocker):
    mocker.patch.object(menu, "buscar_pelicula", return_value=None)
    mocker.patch("builtins.input", side_effect=["Inexistente", ""])

    menu.funcion_buscar_pelicula()

    assert MSG_NO_ENCONTRADA in capsys.readouterr().out


# ---------------------------------------------------------------
# Buscar por actor
# ---------------------------------------------------------------
def test_funcion_buscar_actor_selecciona_detalles(capsys, mocker):
    mocker.patch.object(
        menu, "buscar_peliculas_por_actor", return_value=[{"Title": "Inception"}]
    )
    mocker.patch.object(menu, "buscar_pelicula", return_value=PELICULA)
    mocker.patch("builtins.input", side_effect=["DiCaprio", "1", ""])

    menu.funcion_buscar_actor()

    assert MSG_NO_ENCONTRADAS_ACTOR not in capsys.readouterr().out
    menu.buscar_pelicula.assert_called_once_with("Inception")


def test_funcion_buscar_actor_seleccion_invalida(capsys, mocker):
    mocker.patch.object(menu, "buscar_peliculas_por_actor", return_value=[{"Title": "A"}])
    mocker.patch.object(menu, "buscar_pelicula")
    mocker.patch("builtins.input", side_effect=["A", "abc", ""])

    menu.funcion_buscar_actor()

    assert MSG_SELECCION_INVALIDA in capsys.readouterr().out
    menu.buscar_pelicula.assert_not_called()


def test_funcion_buscar_actor_seleccion_enter(capsys, mocker):
    mocker.patch.object(menu, "buscar_peliculas_por_actor", return_value=[{"Title": "A"}])
    mocker.patch.object(menu, "buscar_pelicula")
    mocker.patch("builtins.input", side_effect=["A", "", ""])

    menu.funcion_buscar_actor()

    assert MSG_SELECCION_INVALIDA not in capsys.readouterr().out


def test_funcion_buscar_actor_sin_resultados(capsys, mocker):
    mocker.patch.object(menu, "buscar_peliculas_por_actor", return_value=[])
    mocker.patch("builtins.input", side_effect=["A", ""])

    menu.funcion_buscar_actor()

    assert MSG_NO_ENCONTRADAS_ACTOR in capsys.readouterr().out


def test_funcion_buscar_actor_busqueda_invalida(capsys, mocker):
    mocker.patch.object(menu, "buscar_peliculas_por_actor")
    mocker.patch("builtins.input", side_effect=["", ""])

    menu.funcion_buscar_actor()

    assert MSG_BUSQUEDA_INVALIDA in capsys.readouterr().out
    menu.buscar_peliculas_por_actor.assert_not_called()


# ---------------------------------------------------------------
# Buscar series
# ---------------------------------------------------------------
def test_funcion_buscar_series_selecciona(capsys, mocker):
    series = [{"show": {"id": 1, "name": "Dark", "status": "Ended"}}]
    detalle = {"show": {"id": 1, "name": "Dark", "summary": "<p>x</p>"}}
    mocker.patch.object(menu, "buscar_series", return_value=series)
    mocker.patch.object(menu, "obtener_detalles_serie", return_value=detalle)
    mocker.patch("builtins.input", side_effect=["Dark", "1", ""])

    menu.funcion_buscar_series()

    salida = capsys.readouterr().out
    assert "Dark" in salida
    menu.obtener_detalles_serie.assert_called_once_with(1)


def test_funcion_buscar_series_seleccion_invalida(capsys, mocker):
    mocker.patch.object(
        menu, "buscar_series", return_value=[{"show": {"id": 1, "name": "A"}}]
    )
    mocker.patch.object(menu, "obtener_detalles_serie")
    mocker.patch("builtins.input", side_effect=["A", "abc", ""])

    menu.funcion_buscar_series()

    assert MSG_SELECCION_INVALIDA in capsys.readouterr().out
    menu.obtener_detalles_serie.assert_not_called()


def test_funcion_buscar_series_sin_resultados(capsys, mocker):
    mocker.patch.object(menu, "buscar_series", return_value=[])
    mocker.patch("builtins.input", side_effect=["Dark", ""])

    menu.funcion_buscar_series()

    assert MSG_NO_ENCONTRADAS_SERIES in capsys.readouterr().out


def test_funcion_buscar_series_busqueda_invalida(capsys, mocker):
    mocker.patch.object(menu, "buscar_series")
    mocker.patch("builtins.input", side_effect=["", ""])

    menu.funcion_buscar_series()

    assert MSG_BUSQUEDA_INVALIDA in capsys.readouterr().out
    menu.buscar_series.assert_not_called()


# ---------------------------------------------------------------
# Populares y género
# ---------------------------------------------------------------
def test_funcion_peliculas_populares(capsys, mocker):
    mocker.patch.object(
        menu, "obtener_peliculas_populares", return_value=[{"titulo": "Shawshank", "anio": 1994, "rating": 9.3}]
    )
    mocker.patch("builtins.input", side_effect=[""])

    menu.funcion_peliculas_populares()

    salida = capsys.readouterr().out
    assert HEADER_PELICULAS_POPULARES in salida
    assert "Shawshank" in salida


def test_funcion_buscar_por_genero_valido(capsys, mocker):
    mocker.patch.object(
        menu, "buscar_peliculas_por_genero",
        return_value=[{"titulo": "Mad Max", "anio": 2015, "rating": 8.1}],
    )
    mocker.patch("builtins.input", side_effect=["accion", ""])

    menu.funcion_buscar_por_genero()

    salida = capsys.readouterr().out
    assert "Mad Max" in salida
    menu.buscar_peliculas_por_genero.assert_called_once_with("accion")


def test_funcion_buscar_por_genero_invalido(capsys, mocker):
    mocker.patch.object(menu, "buscar_peliculas_por_genero")
    mocker.patch("builtins.input", side_effect=["horror", ""])

    menu.funcion_buscar_por_genero()

    assert MSG_GENERO_INVALIDO in capsys.readouterr().out
    menu.buscar_peliculas_por_genero.assert_not_called()


# ---------------------------------------------------------------
# Favoritos e historial
# ---------------------------------------------------------------
def test_funcion_ver_favoritos_elimina(capsys, mocker):
    movie_service.PELICULAS_FAVORITAS.append(PELICULA)
    mocker.patch("builtins.input", side_effect=["1", ""])

    menu.funcion_ver_favoritos()

    assert MSG_ELIMINADA_FAVORITOS in capsys.readouterr().out
    assert movie_service.PELICULAS_FAVORITAS == []


def test_funcion_ver_favoritos_enter_no_elimina(capsys, mocker):
    movie_service.PELICULAS_FAVORITAS.append(PELICULA)
    mocker.patch("builtins.input", side_effect=["", ""])

    menu.funcion_ver_favoritos()

    assert len(movie_service.PELICULAS_FAVORITAS) == 1


def test_funcion_ver_favoritos_seleccion_invalida(capsys, mocker):
    movie_service.PELICULAS_FAVORITAS.append(PELICULA)
    mocker.patch("builtins.input", side_effect=["abc", ""])

    menu.funcion_ver_favoritos()

    assert MSG_SELECCION_INVALIDA in capsys.readouterr().out


def test_funcion_ver_favoritos_vacio(capsys, mocker):
    mocker.patch("builtins.input", side_effect=[""])

    menu.funcion_ver_favoritos()

    assert MSG_SIN_FAVORITAS in capsys.readouterr().out


def test_funcion_ver_historial_limpia(capsys, mocker):
    movie_service.HISTORIAL_BUSQUEDAS.append({"titulo": "Inception", "fecha": "hoy"})
    mocker.patch("builtins.input", side_effect=["s", ""])

    menu.funcion_ver_historial()

    assert MSG_HISTORIAL_LIMPIADO in capsys.readouterr().out
    assert movie_service.HISTORIAL_BUSQUEDAS == []


def test_funcion_ver_historial_sin_limpiar(capsys, mocker):
    movie_service.HISTORIAL_BUSQUEDAS.append({"titulo": "Inception", "fecha": "hoy"})
    mocker.patch("builtins.input", side_effect=["n", ""])

    menu.funcion_ver_historial()

    assert len(movie_service.HISTORIAL_BUSQUEDAS) == 1


def test_funcion_ver_historial_vacio(capsys, mocker):
    mocker.patch("builtins.input", side_effect=[""])

    menu.funcion_ver_historial()

    assert MSG_SIN_HISTORIAL in capsys.readouterr().out


# ---------------------------------------------------------------
# Estadísticas
# ---------------------------------------------------------------
def test_funcion_estadisticas(capsys, mocker):
    movie_service.PELICULAS_FAVORITAS.append(PELICULA)
    movie_service.HISTORIAL_BUSQUEDAS.append({"titulo": "Inception", "fecha": "hoy"})
    mocker.patch("builtins.input", side_effect=[""])

    menu.funcion_estadisticas()

    salida = capsys.readouterr().out
    assert "Total favoritas: 1" in salida
    assert "Total historial: 1" in salida


# ---------------------------------------------------------------
# Exportar / importar
# ---------------------------------------------------------------
def test_funcion_exportar_escribe_archivo(capsys, mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    movie_service.PELICULAS_FAVORITAS.append(PELICULA)
    mocker.patch("builtins.input", side_effect=["respaldo", ""])

    menu.funcion_exportar()

    assert "Exportado a respaldo.json" in capsys.readouterr().out
    assert (tmp_path / "respaldo.json").exists()


def test_funcion_exportar_nombre_invalido(capsys, mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mocker.patch("builtins.input", side_effect=["..", ""])

    menu.funcion_exportar()

    assert MSG_NOMBRE_ARCHIVO_INVALIDO in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_funcion_importar_desde_archivo(capsys, mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "datos.json").write_text(json.dumps({"favoritas": [PELICULA], "historial": []}))
    mocker.patch("builtins.input", side_effect=["datos", ""])

    menu.funcion_importar()

    assert "Importado desde datos.json" in capsys.readouterr().out
    assert movie_service.PELICULAS_FAVORITAS == [PELICULA]


def test_funcion_importar_archivo_inexistente(capsys, mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mocker.patch("builtins.input", side_effect=["no-existe", ""])

    menu.funcion_importar()

    assert MSG_ERROR_IMPORTAR in capsys.readouterr().out


def test_funcion_importar_nombre_invalido(capsys, mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mocker.patch("builtins.input", side_effect=["../mal", ""])

    menu.funcion_importar()

    assert MSG_NOMBRE_ARCHIVO_INVALIDO in capsys.readouterr().out


# ---------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------
def test_funcion_configuracion_toggle_debug(capsys, mocker):
    original = menu.CONFIG["debug"]
    mocker.patch("builtins.input", side_effect=["1", ""])

    menu.funcion_configuracion()

    assert f"{MSG_DEBUG_ACTUAL}{not original}" in capsys.readouterr().out
    menu.CONFIG["debug"] = original


def test_funcion_configuracion_toggle_verbose(capsys, mocker):
    original = menu.CONFIG["verbose"]
    mocker.patch("builtins.input", side_effect=["2", ""])

    menu.funcion_configuracion()

    assert menu.CONFIG["verbose"] == (not original)
    menu.CONFIG["verbose"] = original


def test_funcion_configuracion_timeout_valido(capsys, mocker):
    original = menu.CONFIG["timeout"]
    mocker.patch("builtins.input", side_effect=["3", "42", ""])

    menu.funcion_configuracion()

    assert menu.CONFIG["timeout"] == 42
    menu.CONFIG["timeout"] = original


def test_funcion_configuracion_timeout_invalido(capsys, mocker):
    original = menu.CONFIG["timeout"]
    mocker.patch("builtins.input", side_effect=["3", "abc", ""])

    menu.funcion_configuracion()

    assert MSG_TIMEOUT_INVALIDO in capsys.readouterr().out
    assert menu.CONFIG["timeout"] == original


def test_funcion_configuracion_opcion_invalida(capsys, mocker):
    mocker.patch("builtins.input", side_effect=["9", ""])

    menu.funcion_configuracion()

    assert MSG_SELECCION_INVALIDA in capsys.readouterr().out


def test_funcion_configuracion_opcion_enter(capsys, mocker):
    mocker.patch("builtins.input", side_effect=["", ""])

    menu.funcion_configuracion()

    assert MSG_SELECCION_INVALIDA not in capsys.readouterr().out


# ---------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------
def test_menu_principal_salir(capsys, mocker):
    mocker.patch.object(menu, "clear_screen")
    mocker.patch("builtins.input", side_effect=["12"])

    menu.menu_principal()

    assert MSG_HASTA_LUEGO in capsys.readouterr().out


def test_menu_principal_opcion_invalida_y_salir(capsys, mocker):
    mocker.patch.object(menu, "clear_screen")
    mocker.patch("builtins.input", side_effect=["99", "12"])

    menu.menu_principal()

    salida = capsys.readouterr().out
    assert MSG_OPCION_INVALIDA in salida
    assert MSG_HASTA_LUEGO in salida