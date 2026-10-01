# Resumen Fase 6 — Hito 3: Tests de integración para APIs (y cierre de la meta ≥80%)

## Objetivo

Cubrir la integración con las APIs (OMDb, TVMaze) sin llamadas reales a la red y cerrar
la meta de la Fase 6 de **≥80% de coverage**. Por acuerdo, el Hito 3 amplió su alcance a
`config.py`, `ui/display.py`, `ui/menu.py` y un e2e de `main.py` por subproceso, porque
las APIs por sí solas no alcanzaban el objetivo.

## Cambios realizados

### Tests de API (transporte mockeado)
- `tests/test_http_client.py` (2 casos): `hacer_request` llama a `requests.get` con
  `params` y `timeout` obtenido de `api.http_client.CONFIG` y devuelve `response.json()`.
- `tests/test_api_omdb.py` (2 casos): construcción de URL de `buscar_por_titulo`
  (`?t=...&apikey=...`) y `buscar_por_actor` (`?s=...&type=movie&apikey=...`).
- `tests/test_api_tvmaze.py` (2 casos): URLs `/search/shows?q=...` y `/shows/{id}`.
- Detalle de mockeo: como `omdb`/`tvmaze` hacen `from api.http_client import
  hacer_request`, el patch debe apuntar a la **referencia importada**
  (`api.omdb.hacer_request`), no al atributo de `http_client`.

### `tests/test_config.py` (18 casos)
- Con `CONFIG_FILE` apuntando a `tmp_path` (monkeypatch) para no tocar el `config.json`
  real: carga desde defaults si no existe, carga de JSON existente, secreto de entorno
  que prioriza sobre el archivo, `get`/`get_all`, `set` que persiste, `reset`,
  `export_config`/`import_config` (y sin archivo), `validate_config` (válido, claves
  faltantes, timeout no numérico/cero, `max_retries` no entero).
- `_cargar_dotenv` con un `.env` de prueba (líneas válidas, no sobrescribe existentes,
  sin archivo no falla), `print_config` que enmascara secretos (`caplog`) y
  `setup_logging` según flags.

### `tests/test_ui_display.py` (12 casos)
- `clear_screen` (mockea `os.system`), `print_separator`, `print_header`; `mostrar_pelicula`
  con `None`, completa, con campos faltantes y sin título (`N/A`); `mostrar_serie` con/ sin
  wrapper `show` y truncado de resumen a 200 + `...`; `mostrar_lista_peliculas` con claves
  `titulo`/`Title`/ninguna. Todo con `capsys`.

### `tests/test_ui_menu.py` (36 casos)
- Cada `funcion_*` con `input` mockeado (`side_effect`), `ui.menu.delay` y
  `ui.menu.clear_screen` parcheados, y funciones de servicio parcheadas en el propio
  paquete `ui.menu`. Cubre: búsqueda por título (con/sin favorito, repetida, inválida,
  no encontrada), actor, series, populares, género válido/inválido, favoritos
  (eliminar/enter/inválido/vacío), historial (limpiar/no/vacío), estadísticas,
  exportar/importar (con `monkeypatch.chdir(tmp_path)` y JSON), configuración
  (debug/verbose/timeout válido e inválido/opción inválida) y `menu_principal`
  (salida, opción inválida). Los tests de configuración restauran `CONFIG` al final.

### `tests/test_main_e2e.py` (2 casos)
- Subproceso `python main.py`: opción `12` → exit 0 + "¡Hasta luego!"; y flujo sin red
  (opción `4` populares → enter → `12`) → exit 0.

### Correcciones destapadas por los tests
- **`config.py` — bug latente en `validate_config`**: con `timeout` no numérico
  (p. ej. `"treinta"`) la línea `_config["timeout"] <= 0` crasheaba con `TypeError`
  (comparar `str` con `int`). Se corrige con `elif`, preservando los mensajes y la
  firma de la función.
- **`tests/conftest.py` — reset de estado incompleto**: `limpiar_historial` e
  `importar_de_json` *reasignan* los globales del módulo, así que las referencias
  capturadas por `ui.menu` (`from services.movie_service import HISTORIAL_BUSQUEDAS`)
  quedaban apuntando a listas antiguas y los tests dependían del orden de ejecución.
  El fixture ahora re-enlaza `menu.HISTORIAL_BUSQUEDAS`/`menu.PELICULAS_FAVORITAS` a las
  listas actuales de servicios antes de limpiarlas.

## Verificación

1. `python3 -m pytest -v` (`.venv`): **169 passed** (H1: 70, H2: 23, H3: 76) en ~2.1s.
2. Coverage global:**98%** (725 stmts).
   | Módulo | Cover |
   |--------|:-----:|
   | `config.py`, `constants.py` | 100% |
   | `api/*` (http_client, omdb, tvmaze) | 100% |
   | `services/*` | 100% |
   | `models/*`, `exceptions/*`, `ui/validation.py` | 100% |
   | `ui/display.py` | 100% |
   | `ui/menu.py` | 94% (faltan: cuerpo de `delay`, y los `elif` del dispatch de opciones 1-11 en `menu_principal`, que requieren recorrer el menú completo) |
   - `main.py` queda **fuera** de la medición (`source` de `.coveragerc`): solo contiene
     el guard `if __name__ == "__main__"`; se valida por subproceso e2e.
3. Regresión: `echo "12" | python main.py` → exit 0.
4. Meta **≥80% de coverage superada** (98%).

## Estado del proyecto

- **Hito 3 de Fase 6 completo** ✅ — Fase 6 y, con ello, el plan de 6 fases, **completo**.
- Pendientes conocidos (fuera de alcance de la Fase 6, documentados para el futuro):
  - `main.py` no cuenta para coverage (solo entrada + guard `__main__`); cubierto por e2e.
  - Dispatch completo del menú (opciones 1-11 vía `menu_principal`) por probar e2e de
    cada rama — requiere ejecutar el menú con entradas completas.
  - `json5` en `requirements.txt` es dependencia muerta (no se importa en ningún módulo);
    candidata a eliminar.
  - `user_manager.py` (código muerto) guarda contraseñas en texto plano: candidato a
    hashing en un próximo ciclo.
- Estado documental: `Docs/` cubre las 6 fases (01–23).

## Cómo correr los tests

```bash
source .venv/bin/activate
pytest -v
```