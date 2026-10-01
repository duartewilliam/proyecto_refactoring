"""Modelo de dominio para películas (OMDb)."""
from dataclasses import dataclass, asdict


@dataclass
class Movie:
    title: str = ""
    year: str = ""
    imdb_rating: str = ""
    genre: str = ""
    director: str = ""
    actors: str = ""
    plot: str = ""
    country: str = ""
    awards: str = ""

    @classmethod
    def from_omdb(cls, data: dict) -> "Movie":
        """Parsea una respuesta completa de OMDb (buscar por título)."""
        return cls(
            title=data.get("Title", ""),
            year=data.get("Year", ""),
            imdb_rating=data.get("imdbRating", ""),
            genre=data.get("Genre", ""),
            director=data.get("Director", ""),
            actors=data.get("Actors", ""),
            plot=data.get("Plot", ""),
            country=data.get("Country", ""),
            awards=data.get("Awards", ""),
        )

    def to_dict(self) -> dict:
        """Serializa el modelo a dict."""
        return asdict(self)