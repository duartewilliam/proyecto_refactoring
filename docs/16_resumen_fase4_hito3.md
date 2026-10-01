# Resumen Fase 4 — Hito 3: Logging con módulo `logging`

## Objetivo

Sustituir los `print("DEBUG: ...")` de depuración por el módulo estándar `logging`,
registrar los errores capturados (con traceback) y restaurar el catch-all de la
entrada. Nivel del logger raíz controlado en vivo por el `CONFIG` runtime
(`debug` → DEBUG, `verbose` → INFO).

## Cambios realizados

### `config.py`
Nueva función `setup_logging(debug, verbose)`:
- Handler único de **consola** (`StreamHandler`), formateado
  `"%(asctime)s - %(levelname)s - %(name)s - %(message)s"`.
- Nivel del raíz: `DEBUG` si `debug`, `INFO` si `verbose`, si no `WARNING`.
- Reemplaza la lista de handlers del raíz (evita duplicados al re-llamarse).
- No usa `log_file` (clave de config disponible para futuro).

### `api/http_client.py`
`logger = logging.getLogger(__name__)`; `print("DEBUG: Haciendo request a ...")` →
`logger.debug("Haciendo request a %s", url)`; `print("DEBUG: Status code: ...")` →
`logger.info("Status code: %s", response.status_code)`. Se eliminan los guards
`if CONFIG["debug"]` / `if CONFIG["verbose"]` (el nivel del raíz filtra).

### `services/movie_service.py`
`logger = logging.getLogger(__name__)`; `print("DEBUG: Usando cache para ...")` →
`logger.debug("Usando cache para %s", titulo)`. Se elimina el import de `CONFIG`
(quedaba sin uso).

### `services/series_service.py`
`logger = logging.getLogger(__name__)` (sin logs activos por ahora; queda listo).

### `ui/menu.py`
`logger = logging.getLogger(__name__)`; en `funcion_importar` se añade
`logger.exception("Error al importar %s", nombre)` conservando
`print(MSG_ERROR_IMPORTAR)`. En `funcion_configuracion`, los toggles de debug y
verbose rellaman `setup_logging(CONFIG["debug"], CONFIG["verbose"])` → nivel cambia
en vivo.

### `main.py`
- `import logging`; `logger = logging.getLogger("main")`.
- `setup_logging(CONFIG["debug"], CONFIG["verbose"])` antes de `menu_principal()`.
- `except AppError` → `logger.exception("Error de aplicación: %s", e)`.
- **Se restaura** el catch-all `except Exception` → `logger.exception("Error inesperado: %s", e)`
  (decisión D3; alineado con doc 04 H11).
- `KeyboardInterrupt` sin log (salida normal del usuario).
- Salidas de usuario y códigos de salida intactos (`EXIT_OK`/`EXIT_ERROR`).

## Verificación

1. `py_compile` de los 5 archivos → OK.
2. Niveles del raíz: `debug=True` → aparece `DEBUG` del request y `INFO` del status;
   `verbose=True` (debug off) → solo `INFO`+; ambos off → solo `WARNING`+.
3. `movie_service`: caché emite `DEBUG services.movie_service — Usando cache para ...`.
4. Toggle en vivo: con `debug=False` un `logger.debug` queda oculto; tras
   `funcion_configuracion` (opción 1) el `debug` pasa a `True` y el mensaje aparece.
5. `funcion_importar` con archivo inexistente → `print(MSG_ERROR_IMPORTAR)` +
   registro `ERROR ... Error al importar ...` con traceback.
6. `main.py` ejecutado con `menu_principal` que lanza `MovieNotFoundError` → log
   `Error de aplicación` + print + `EXIT_ERROR`.
7. `main.py` con `ValueError` genérico → log `Error inesperado` (catch-all) +
   print + `EXIT_ERROR`.
8. Un solo handler en el raíz (sin duplicados al reconfigurar).
9. `printf '12\n' | python3 main.py` → exit 0 y "¡Hasta luego!".
10. `grep "DEBUG:"` en módulos activos → 0 coincidencias.

## Estado del proyecto

- Fase 2 completada (Hitos 1–5).
- Fase 3 completada (Hitos 1–3).
- Fase 4: Hitos 1 (excepciones), 2 (capturas específicas) y 3 (logging)
  completados.
- Sin cambios en lógica de negocio ni firmas públicas. `log_file` de config queda
  disponible para un futuro destino a archivo.