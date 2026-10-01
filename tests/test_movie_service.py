"""Tests unitarios de services/movie_service.py (API OMDb mockeada)."""
import json

from api import omdb
from constants import PELICULAS_ACCION, PELICULAS_COMEDIA, PELICULAS_POPULARES
from services import movie_service

RESPUESTA_VERDADERA = {
    "Title": "Inception",
    "Year": "2010",
    "Response": "True",
}

RESPUESTA_NO_ENCONTRADA = {
    "Response": "False",
    "Error": "Movie not found!",
}


# ---------------------------------------------------------------
# buscar_pelicula (con cache)
# ---------------------------------------------------------------
def test_buscar_pelicula_devuelve_data_y_usa_cache(mocker):
    mock_titulo = mocker.patch.object(omdb, "buscar_por_titulo", return_value=RESPUESTA_VERDADERA)

    resultado_1 = movie_service.buscar_pelicula("Inception")
    resultado_2 = movie_service.buscar_pelicula("Inception")

    assert resultado_1 == RESPUESTA_VERDADERA
    assert resultado_2 == RESPUESTA_VERDADERA
    assert mock_titulo.call_count == 1
    assert movie_service.CACHE_PELICULAS["Inception"] == RESPUESTA_VERDADERA


def test_buscar_pelicula_sin_response_devuelve_none_sin_cachear(mocker):
    mock_titulo = mocker.patch.object(omdb, "buscar_por_titulo", return_value=RESPUESTA_NO_ENCONTRADA)

    assert movie_service.buscar_pelicula("Inexistente") is None
    assert movie_service.buscar_pelicula("Inexistente") is None
    assert mock_titulo.call_count == 2
    assert "Inexistente" not in movie_service.CACHE_PELICULAS


# ---------------------------------------------------------------
# buscar_peliculas_por_actor
# ---------------------------------------------------------------
def test_buscar_peliculas_por_actor_devuelve_search(mocker):
    search = [{"Title": "Inception"}, {"Title": "Memento"}]
    mocker.patch.object(
        omdb, "buscar_por_actor", return_value={"Response": "True", "Search": search}
    )

    assert movie_service.buscar_peliculas_por_actor("DiCaprio") == search


def test_buscar_peliculas_por_actor_sin_response_devuelve_lista_vacia(mocker):
    mocker.patch.object(omdb, "buscar_por_actor", return_value=RESPUESTA_NO_ENCONTRADA)

    assert movie_service.buscar_peliculas_por_actor("Inexistente") == []


# ---------------------------------------------------------------
# obtener_peliculas_populares y buscar_peliculas_por_genero
# ---------------------------------------------------------------
def test_obtener_peliculas_populares():
    assert movie_service.obtener_peliculas_populares() == PELICULAS_POPULARES


def test_buscar_peliculas_por_genero_accion():
    assert movie_service.buscar_peliculas_por_genero("accion") == PELICULAS_ACCION


def test_buscar_peliculas_por_genero_comedia_normaliza_mayusculas():
    assert movie_service.buscar_peliculas_por_genero("COMEDIA") == PELICULAS_COMEDIA


def test_buscar_peliculas_por_genero_desconocido_devuelve_todas():
    assert movie_service.buscar_peliculas_por_genero("horror") == PELICULAS_ACCION + PELICULAS_COMEDIA


# ---------------------------------------------------------------
# Favoritos
# ---------------------------------------------------------------
def test_agregar_a_favoritas_nueva():
    assert movie_service.agregar_a_favoritas(RESPUESTA_VERDADERA) is True
    assert movie_service.PELICULAS_FAVORITAS == [RESPUESTA_VERDADERA]


def test_agregar_a_favoritas_duplicada_por_titulo():
    assert movie_service.agregar_a_favoritas(RESPUESTA_VERDADERA) is True
    assert movie_service.agregar_a_favoritas(RESPUESTA_VERDADERA) is False
    assert len(movie_service.PELICULAS_FAVORITAS) == 1


def test_eliminar_de_favoritas_existente():
    movie_service.PELICULAS_FAVORITAS.append(RESPUESTA_VERDADERA)
    assert movie_service.eliminar_de_favoritas("Inception") is True
    assert movie_service.PELICULAS_FAVORITAS == []


def test_eliminar_de_favoritas_inexistente():
    assert movie_service.eliminar_de_favoritas("No existe") is False


# ---------------------------------------------------------------
# Historial
# ---------------------------------------------------------------
def test_agregar_al_historial():
    movie_service.agregar_al_historial(RESPUESTA_VERDADERA)
    assert movie_service.HISTORIAL_BUSQUEDAS == [
        {"titulo": "Inception", "fecha": "hoy"}
    ]


def test_agregar_al_historial_acumula():
    movie_service.agregar_al_historial(RESPUESTA_VERDADERA)
    movie_service.agregar_al_historial({"Title": "Memento", "Response": "True"})
    assert len(movie_service.HISTORIAL_BUSQUEDAS) == 2


def test_limpiar_historial():
    movie_service.agregar_al_historial(RESPUESTA_VERDADERA)
    movie_service.limpiar_historial()
    assert movie_service.HISTORIAL_BUSQUEDAS == []


# ---------------------------------------------------------------
# Estadísticas
# ---------------------------------------------------------------
def test_obtener_estadisticas_vacias():
    assert movie_service.obtener_estadisticas() == {"total_favoritas": 0, "total_historial": 0}


def test_obtener_estadisticas_con_datos():
    movie_service.agregar_a_favoritas(RESPUESTA_VERDADERA)
    movie_service.agregar_a_favoritas({"Title": "Memento", "Response": "True"})
    for _ in range(3):
        movie_service.agregar_al_historial(RESPUESTA_VERDADERA)

    assert movie_service.obtener_estadisticas() == {"total_favoritas": 2, "total_historial": 3}


# ---------------------------------------------------------------
# Exportar / importar JSON
# ---------------------------------------------------------------
def test_exportar_a_json_escribe_archivo(tmp_path):
    movie_service.agregar_a_favoritas(RESPUESTA_VERDADERA)
    movie_service.agregar_al_historial(RESPUESTA_VERDADERA)

    ruta = tmp_path / "datos.json"
    movie_service.exportar_a_json(str(ruta))

    with open(ruta, "r") as f:
        datos = json.load(f)
    assert set(datos) == {"favoritas", "historial", "estadisticas"}
    assert datos["favoritas"] == [RESPUESTA_VERDADERA]
    assert datos["estadisticas"] == {"total_favoritas": 1, "total_historial": 1}


def test_importar_de_json_restaura_estado(tmp_path):
    ruta = tmp_path / "datos.json"
    with open(ruta, "w") as f:
        json.dump({"favoritas": [RESPUESTA_VERDADERA], "historial": [{"titulo": "A", "fecha": "hoy"}]}, f)

    movie_service.importar_de_json(str(ruta))

    assert movie_service.PELICULAS_FAVORITAS == [RESPUESTA_VERDADERA]
    assert movie_service.HISTORIAL_BUSQUEDAS == [{"titulo": "A", "fecha": "hoy"}]


def test_exportar_e_importar_roundtrip(tmp_path):
    movie_service.agregar_a_favoritas(RESPUESTA_VERDADERA)
    movie_service.agregar_al_historial(RESPUESTA_VERDADERA)

    ruta = tmp_path / "datos.json"
    movie_service.exportar_a_json(str(ruta))

    movie_service.limpiar_historial()
    movie_service.PELICULAS_FAVORITAS.clear()
    assert movie_service.obtener_estadisticas() == {"total_favoritas": 0, "total_historial": 0}

    movie_service.importar_de_json(str(ruta))
    assert movie_service.obtener_estadisticas() == {"total_favoritas": 1, "total_historial": 1}
    assert movie_service.PELICULAS_FAVORITAS == [RESPUESTA_VERDADERA]