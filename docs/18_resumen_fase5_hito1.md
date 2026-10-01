# Resumen Fase 5 — Hito 1: Mover contraseñas a variables de entorno

## Objetivo

Sacar credenciales/API keys de `config.json` y resolverlas desde el entorno en
tiempo de ejecución, sin añadir dependencias (sin `python-dotenv`).

## Cambios realizados

### `config.py`
- `SECRET_ENV: dict[str, str]` — mapeo clave de config → variable de entorno:
  `omdb_api_key→OMDB_API_KEY`, `tmdb_api_key→TMDB_API_KEY`,
  `sender_email→SENDER_EMAIL`, `sender_password→SENDER_PASSWORD`,
  `proxy_username→PROXY_USERNAME`, `proxy_password→PROXY_PASSWORD`
  (decisión: los 6 campos sensibles, no solo contraseñas).
- `MASCARA_SECRETO = "***"`.
- `_cargar_dotenv(ruta=".env")` — parser estándar (stdlib):
  - ignora líneas vacías, comentarios `#` y líneas sin `=`;
  - soporta `KEY=valor`, espacios alrededor y comillas simples/dobles;
  - usa `os.environ.setdefault(...)` → la variable ya definida en el entorno
    real **gana** sobre el archivo `.env`.
- `_resolver_secretos()` — tras cargar el JSON, **overlay de secretos**:
  `_config[clave] = os.environ.get(variable, _config.get(clave, ""))`.
  El entorno manda sobre `config.json` en tiempo de ejecución.
- `load_config()` — ahora llama `_cargar_dotenv()` antes y `_resolver_secretos()`
  después de poblarse `_config` (aplica antes de los snapshots de import vía `get()`).
- `print_config()` — **enmascara** los valores de `SECRET_ENV` (imprime `***`),
  evitando filtrar contraseñas al log.

### `config.json`
- `omdb_api_key` pasa de `"trilogy"` a `""`.
- Resto de claves sensibles ya estaban en `""`. Las claves se conservan, de modo
  que `validate_config` sigue coherente.

### Nuevos archivos
- `.env.example` — plantilla con las 6 variables (solo placeholders).
- `.gitignore` — incluye `.env` (higiene; el repo aún no es git).

## Verificación

1. `py_compile` de `config.py` → OK.
2. `config.json` → 0 coincidencias de `"trilogy"` (sin secretos persistidos).
3. Precedencia de entorno: `OMDB_API_KEY=x_clave_secreta python3 -c "import api.omdb"` →
   `API_KEY_OMDB == "x_clave_secreta"`.
4. Sin env: `get("omdb_api_key") == ""`.
5. Carga `.env` (archivo temporal): variable nueva tomada, con espacios y comillas
   parseadas, y variable ya presente en el entorno respeta el valor real (`setdefault`).
6. Overlay: `PROXY_PASSWORD=pw_env` → `get("proxy_password") == "pw_env"` (manda env).
7. Enmascarado: `print_config()` con `OMDB_API_KEY=super_secreto_123` → el log muestra
   `omdb_api_key: ***` y **ningún** valor en claro.
8. App intacta:
   - opción 12 → exit 0 y "¡Hasta luego!";
   - exportar/importar e2e → "Exportado a respaldo.json", exit 0;
   - búsqueda con `OMDB_API_KEY=k_e2e` → se ejecuta y termina sin crashear (exit 0),
     mostrando mensaje de no encontrado (red real sin clave válida).

## Estado del proyecto

- Fases 1–4 completadas.
- Fase 5, Hito 1 completado. La única fuente de secretos en runtime son las
  variables de entorno (y `.env` local); `config.json` conserva claves vacías.
- Sin dependencias nuevas; sin cambios en firmas públicas ni lógica de negocio.