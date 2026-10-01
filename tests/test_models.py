"""Tests unitarios de los modelos de dominio (models/movie.py y models/series.py)."""
from models.movie import Movie
from models.series import Series


# ---------------------------------------------------------------
# Movie
# ---------------------------------------------------------------
def test_movie_valores_por_defecto():
    movie = Movie()
    assert movie.title == ""
    assert movie.year == ""
    assert movie.imdb_rating == ""
    assert movie.genre == ""
    assert movie.director == ""
    assert movie.actors == ""
    assert movie.plot == ""
    assert movie.country == ""
    assert movie.awards == ""


def test_movie_from_omdb_mapea_campos():
    data = {
        "Title": "Inception",
        "Year": "2010",
        "imdbRating": "8.8",
        "Genre": "Action, Sci-Fi",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio",
        "Plot": "A thief who steals corporate secrets.",
        "Country": "USA",
        "Awards": "Oscar",
    }
    movie = Movie.from_omdb(data)
    assert movie.title == "Inception"
    assert movie.year == "2010"
    assert movie.imdb_rating == "8.8"
    assert movie.genre == "Action, Sci-Fi"
    assert movie.director == "Christopher Nolan"
    assert movie.actors == "Leonardo DiCaprio"
    assert movie.plot == "A thief who steals corporate secrets."
    assert movie.country == "USA"
    assert movie.awards == "Oscar"


def test_movie_from_omdb_claves_faltantes_usan_default():
    movie = Movie.from_omdb({"Title": "Solo titulo"})
    assert movie.title == "Solo titulo"
    assert movie.year == ""
    assert movie.imdb_rating == ""
    assert movie.genre == ""


def test_movie_to_dict_roundtrip():
    data = {"Title": "Inception", "Year": "2010"}
    movie = Movie.from_omdb(data)
    salida = movie.to_dict()
    assert salida["title"] == "Inception"
    assert salida["year"] == "2010"
    assert salida["actors"] == ""
    assert len(salida) == 9


# ---------------------------------------------------------------
# Series
# ---------------------------------------------------------------
def test_series_valores_por_defecto():
    serie = Series()
    assert serie.id is None
    assert serie.name == ""
    assert serie.language == ""
    assert serie.genres == []
    assert serie.rating_average is None
    assert serie.status == ""
    assert serie.premiered is None
    assert serie.ended is None
    assert serie.runtime is None
    assert serie.summary is None


def test_series_from_tvmaze_desenvuelve_wrapper_show():
    data = {
        "score": 1.0,
        "show": {
            "id": 1,
            "name": "Breaking Bad",
            "language": "English",
            "genres": ["Drama"],
            "rating": {"average": 9.3},
            "status": "Ended",
            "premiered": "2008-01-20",
            "ended": "2013-09-29",
            "runtime": 45,
            "summary": "<p>Walter White.</p>",
        },
    }
    serie = Series.from_tvmaze(data)
    assert serie.id == 1
    assert serie.name == "Breaking Bad"
    assert serie.language == "English"
    assert serie.genres == ["Drama"]
    assert serie.rating_average == 9.3
    assert serie.status == "Ended"
    assert serie.premiered == "2008-01-20"
    assert serie.ended == "2013-09-29"
    assert serie.runtime == 45
    assert serie.summary == "<p>Walter White.</p>"


def test_series_from_tvmaze_sin_wrapper_y_sin_rating():
    data = {
        "id": 2,
        "name": "Elite",
        "rating": {},
    }
    serie = Series.from_tvmaze(data)
    assert serie.id == 2
    assert serie.name == "Elite"
    assert serie.rating_average is None
    assert serie.language == ""


def test_series_to_dict_roundtrip():
    serie = Series.from_tvmaze({"show": {"id": 3, "name": "Dark", "rating": {"average": 8.7}}})
    salida = serie.to_dict()
    assert salida["id"] == 3
    assert salida["name"] == "Dark"
    assert salida["rating_average"] == 8.7
    assert salida["genres"] == []
    assert len(salida) == 10