# Resumen Fase 3 — Hito 1: Separación de `api_movies.py` en capas de API y Servicios

## Objetivo

Separar el monolito `api_movies.py` en paquetes con responsabilidades claras:

- `api/` → clientes HTTP de bajo nivel hacia OMDb y TVMaze.
- `services/` → orquestación, estado (caches, favoritas, historial) y persistencia.

Se conserva la lógica de negocio, las firmas públicas y el comportamiento observado.

## Cambios realizados

### Creados (7 archivos)

| Archivo | Responsabilidad |
|---|---|
| `api/__init__.py` | Marcador de paquete `api` |
| `api/http_client.py` | `CONFIG` (dict runtime) + `hacer_request()` (HTTP compartido) |
| `api/omdb.py` | `API_KEY_OMDB`, `BASE_URL_OMDB`, `buscar_por_titulo()`, `buscar_por_actor()` — respuesta cruda |
| `api/tvmaze.py` | `BASE_URL_TVMAZE`, `buscar_por_nombre()`, `obtener_por_id()` — respuesta cruda |
| `services/__init__.py` | Marcador de paquete `services` |
| `services/movie_service.py` | `USUARIO_LOGUEADO`, `PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_PELICULAS` + 11 funciones de dominio |
| `services/series_service.py` | `CACHE_SERIES` + `buscar_series()`, `obtener_detalles_serie()` |

### Modificado (1 archivo)

| Archivo | Cambio |
|---|---|
| `main.py` | Imports recableados: `from api.http_client import CONFIG`, `from services.movie_service import (...)`, `from services.series_service import (...)`. Cuerpo sin cambios. |

### Eliminado (1 archivo)

- `api_movies.py` — borrado tras recablear `main.py`.

## Migración de símbolos

| Símbolo | Origen | Destino |
|---|---|---|
| `CONFIG` | `api_movies` | `api.http_client` |
| `hacer_request()` | `api_movies` | `api.http_client` |
| `API_KEY_OMDB`, `BASE_URL_OMDB` | `api_movies` | `api.omdb` |
| `buscar_por_titulo()` / `buscar_por_actor()` | dentro de `buscar_pelicula` / `buscar_peliculas_por_actor` | `api.omdb` (nombres nuevos) |
| `BASE_URL_TVMAZE` | `api_movies` | `api.tvmaze` |
| `buscar_por_nombre()` / `obtener_por_id()` | dentro de `buscar_series` / `obtener_detalles_serie` | `api.tvmaze` (nombres nuevos) |
| `USUARIO_LOGUEADO`, `PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_PELICULAS` | `api_movies` | `services.movie_service` |
| `CACHE_SERIES` | `api_movies` | `services.series_service` |
| `buscar_pelicula`, `buscar_peliculas_por_actor`, `obtener_peliculas_populares`, `buscar_peliculas_por_genero`, `agregar_a_favoritas`, `eliminar_de_favoritas`, `agregar_al_historial`, `limpiar_historial`, `obtener_estadisticas`, `exportar_a_json`, `importar_de_json` | `api_movies` | `services.movie_service` (sin cambios) |
| `buscar_series`, `obtener_detalles_serie` | `api_movies` | `services.series_service` (sin cambios) |

## Decisiones de diseño

- **`hacer_request` + `CONFIG`** viven en `api/http_client.py` (opción A aprobada): se evita acoplar OMDb↔TVMaze y se centraliza el transporte HTTP compartido junto a su configuración runtime.
- **Clientes crudos vs. servicios**: `api/*` construyen URL y llaman a `hacer_request`; `services/*` orquestan cache, verificación `Response == "True"`, datos mock y persistencia. `main.py` solo conversa con los servicios (misma API pública).
- **Referencias por identidad**: `CONFIG`, `PELICULAS_FAVORITAS` y `HISTORIAL_BUSQUEDAS` son el mismo objeto compartido entre `main`, `http_client` y `movie_service` (mutación en caliente preservada).
- Imports absolutos (`from api import omdb`) — compatibles con ejecución `python main.py`.

## Verificación

1. `py_compile` de los 7 módulos nuevos + `main.py` → OK.
2. `import main` → wiring sin errores.
3. Identidad de estado: `main.CONFIG is api.http_client.CONFIG is services.movie_service.CONFIG`; favoritas e historial idénticos entre `main` y `movie_service`.
4. URLs generadas (monkeypatch de `requests.get`) byte-idénticas al comportamiento previo:
   - `buscar_pelicula('Matrix')` → `http://www.omdbapi.com/?t=Matrix&apikey=trilogy`
   - `buscar_peliculas_por_actor('Keanu')` → `http://www.omdbapi.com/?s=Keanu&type=movie&apikey=trilogy`
   - `buscar_series('Breaking')` → `http://api.tvmaze.com/search/shows?q=Breaking`
   - `obtener_detalles_serie(1)` → `http://api.tvmaze.com/shows/1`
   - timeout=30 correctamente propagado.
5. Caches: 1 solo request para 2 llamadas (`buscar_pelicula` y `buscar_series`).
6. Caminos negativos: `Response != "True"` → `None` / `[]`; `eliminar_de_favoritas` inexistente → `False`.
7. Salidas mock byte-idénticas: `obtener_peliculas_populares` ≡ `PELICULAS_POPULARES`; géneros según constants; default ≡ `PELICULAS_ACCION + PELICULAS_COMEDIA`.
8. Estadísticas, `exportar_a_json`/`importar_de_json` (ciclo completo) OK.
9. `grep -rn "api_movies" .` → 0 referencias residuales.

## Estado del proyecto

- Fase 2 completada (Hitos 1–5).
- Fase 3, Hito 1 completado — `api_movies.py` separado en `api/` y `services/`.
- Sin cambios en lógica de negocio, firmas públicas ni dependencias (`requests`, `json5`).