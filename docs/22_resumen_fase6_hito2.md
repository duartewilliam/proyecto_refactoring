# Resumen Fase 6 — Hito 2: Tests unitarios para cada servicio

## Objetivo

Escribir tests unitarios para `services/movie_service.py` y `services/series_service.py`,
sin llamadas reales a la red: se mockean las funciones de `api/omdb.py` y `api/tvmaze.py`
con `pytest-mock`. Alcance acordado: **solo servicios** — `config.py` queda medido de
forma incidental (se importa) pero sin tests propios (pendiente para Hito 3).

## Cambios realizados

### `tests/conftest.py` (nuevo)
- Fixture `reset_estado_servicios` (`autouse`, por test): limpia el estado global de los
  servicios `PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_PELICULAS` y
  `CACHE_SERIES` antes de cada test. Sin esto los tests se contaminarían entre sí,
  porque ambos servicios guardan estado a nivel de módulo vía `global`.

### `tests/test_movie_service.py` (nuevo, 23 casos)
- `buscar_pelicula`: cache (2ª llamada con el mismo título no vuelve a la API —
  `call_count == 1`); `Response == "True"` → devuelve los datos; `Response != "True"` →
  `None` y **no** se cachea (2ª llamada vuelve a llamar a la API).
- `buscar_peliculas_por_actor`: `Search` si `True`, `[]` si no.
- `obtener_peliculas_populares` → igual a `PELICULAS_POPULARES`.
- `buscar_peliculas_por_genero`: `"accion"` → lista de acción; `"COMEDIA"` (normaliza
  mayúsculas) → comedia; otro → combinación de ambas.
- Favoritos: agregar nueva → `True` y presente; duplicada por `Title` → `False` con una
  sola entrada; eliminar existente → `True`; inexistente → `False`.
- Historial: `agregar_al_historial` crea `{"titulo", "fecha": "hoy"}` y acumula;
  `limpiar_historial` vacía.
- `obtener_estadisticas`: conteos vacíos y con datos.
- E/S JSON con `tmp_path` (sin escribir en el directorio del repo): `exportar_a_json`
  escribe `favoritas`/`historial`/`estadisticas`; `importar_de_json` restaura el estado;
  y roundtrip exportar→limpiar→importar.

### `tests/test_series_service.py` (nuevo, 3 casos)
- `buscar_series`: passthrough del resultado de `tvmaze.buscar_por_nombre` + cache bajo
  clave `series_{nombre}` (mismo nombre → 1 sola llamada); nombres distintos → caches y
  llamadas separadas.
- `obtener_detalles_serie`: passthrough de `tvmaze.obtener_por_id` (verifica argumento).

## Verificación

1. `python3 -m pytest -v` (`.venv`):
   - **93 passed** (70 del Hito 1 + 23 nuevos de movie + 3 de series; series sumó 3 casos)
     en 1.30s.
   - Coverage por módulo objetivo: `services/movie_service.py` **100%**,
     `services/series_service.py` **100%**, `constants.py` **100%** (se importa),
     `ui/validation.py`, `models/*` y `exceptions/*` se mantienen al **100%**.
   - `api/*` queda parcial (~64–67%): las funciones mockeadas de OMDb/TVMaze no ejecutan
     su cuerpo (los mocks las reemplazan) — su cobertura plena es del Hito 3.
   - `config.py` al **51%** (solo vía import; sus funciones aún sin tests).
   - **Total global: 53%** (progreso: 23% → 53%). Quedan sin cubrir `ui/menu.py` y
     `ui/display.py` (0%), que requieren simular `input()`/`print()` — pendiente
     análisis para Hito 3.
2. Regresión: `echo "12" | python main.py` → exit code 0.
3. Sin cambios en código productivo: firmas y comportamiento preservados; los tests solo
   mockean la frontera de API.

## Estado del proyecto

- **Hito 2 de Fase 6 completo** ✅: tests unitarios de ambos servicios con mocks.
- Pendiente para el **Hito 3** (integración de APIs y meta ≥80%):
  - Tests de `api/` (OMDb, TVMaze, `http_client.hacer_request`) mockeando el transporte
    (`requests.get`) para cubrir la construcción de URLs y las respuestas sin red.
  - Cubrir o decidir el alcance de `config.py` (51% actual) de cara a la meta del 80%.
  - Analizar cobertura de `ui/menu.py`/`ui/display.py` (0%) — requieren simular entrada
    estándar; opción de tests de subproceso para `main.py`.
  - Medición final contra el objetivo de ≥80%.
- Aclaración de cobertura: los avisos `module-not-imported` de coverage desaparecieron
  porque ahora `config.py`/`constants.py` sí se importan en la corrida.

## Cómo correr solo los tests de este hito

```bash
source .venv/bin/activate
pytest tests/test_movie_service.py tests/test_series_service.py -v
```