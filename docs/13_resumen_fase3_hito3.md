# Resumen Fase 3 — Hito 3: Modelos de dominio `models/movie.py` y `models/series.py`

## Objetivo

Introducir modelos de dominio tipados (dataclasses) que substituyan los dicts ad-hoc
provenientes de las APIs, como primer paso hacia una capa de dominio explícita.
Scaffold puro: se crean los modelos con parsers y serialización, sin consumidores aún.

## Cambios realizados

### Creados (3 archivos)

| Archivo | Contenido |
|---|---|
| `models/__init__.py` | Marcador de paquete `models` |
| `models/movie.py` | Dataclass `Movie` (9 campos) + `from_omdb()` + `to_dict()` |
| `models/series.py` | Dataclass `Series` (10 campos) + `from_tvmaze()` + `to_dict()` |

### Modificados

- Ninguno. La aplicación sigue funcionando con dicts (los modelos no se consumen aún).

## Estructura de los modelos

### `Movie` (espejo de la respuesta OMDb por título)

| Campo | Default |
|---|---|
| `title`, `year`, `imdb_rating`, `genre`, `director`, `actors`, `plot`, `country`, `awards` | `""` |

- `Movie.from_omdb(data)` → mapea `data.get("Title")`, `"Year"`, `"imdbRating"`, `"Genre"`, `"Director"`, `"Actors"`, `"Plot"`, `"Country"`, `"Awards"` con default `""`.
- `to_dict()` → `dataclasses.asdict`.

### `Series` (espejo del show de TVMaze)

| Campo | Default |
|---|---|
| `id` (`int | None`) | `None` |
| `name`, `language`, `status` | `""` |
| `genres` (`list`) | `field(default_factory=list)` |
| `rating_average` (`float | None`) | `None` |
| `premiered`, `ended`, `summary` (`str | None`) | `None` |
| `runtime` (`int | None`) | `None` |

- `Series.from_tvmaze(data)` → desenvuelve el wrapper `"show"` si existe (`data.get("show", data)`), aplanando `rating.average` → `rating_average`. Válido tanto para items de `/search/shows` como para el dict directo de `/shows/{id}`.
- `to_dict()` → `dataclasses.asdict`.

Fuera de alcance (por ahora): los shapes de vista `{titulo, anio, rating}` (datos mock)
y `{titulo, fecha}` (historial) se mantienen como dicts.

## Decisiones aplicadas

- Opción A — scaffold puro (sin integración en servicios/UI). 0 archivos tocados.
- Campos en **English snake_case**, espejo 1:1 de las claves de API (no colisiona con los dicts en español).
- Solo stdlib (`dataclasses`, `field`); sin dependencias nuevas (`requests`, `json5`).

## Verificación

1. `py_compile` de los 3 archivos → OK.
2. `Movie.from_omdb` con fixture completo → 9 campos correctos; `to_dict()` → round-trip exacto.
3. `Movie.from_omdb` con dict incompleto → defaults `""`.
4. `Series.from_tvmaze` con wrapper `show` y con dict directo → instancias iguales (`==`).
5. `Series.from_tvmaze` con dict incompleto → `None`/`""`/`[]` según tipo.
6. `import main` → aplicación intacta (ningún módulo consume los modelos aún).

## Estado del proyecto

- Fase 2 completada (Hitos 1–5).
- Fase 3: Hitos 1 (api/services), 2 (ui/) y 3 (models/) completados.
- Sin cambios en lógica de negocio, firmas públicas ni dependencias.