"""Modelo de dominio para series (TVMaze)."""
from dataclasses import dataclass, asdict, field


@dataclass
class Series:
    id: int | None = None
    name: str = ""
    language: str = ""
    genres: list = field(default_factory=list)
    rating_average: float | None = None
    status: str = ""
    premiered: str | None = None
    ended: str | None = None
    runtime: int | None = None
    summary: str | None = None

    @classmethod
    def from_tvmaze(cls, data: dict) -> "Series":
        """Parsea un item de TVMaze; desenvuelve el wrapper 'show' si existe."""
        show = data.get("show", data)
        rating = show.get("rating") or {}
        return cls(
            id=show.get("id"),
            name=show.get("name", ""),
            language=show.get("language", ""),
            genres=show.get("genres", []),
            rating_average=rating.get("average"),
            status=show.get("status", ""),
            premiered=show.get("premiered"),
            ended=show.get("ended"),
            runtime=show.get("runtime"),
            summary=show.get("summary"),
        )

    def to_dict(self) -> dict:
        """Serializa el modelo a dict."""
        return asdict(self)