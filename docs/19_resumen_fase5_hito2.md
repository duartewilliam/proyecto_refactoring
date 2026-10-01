# Resumen Fase 5 — Hito 2: Eliminar datos hardcodeados sensibles

## Objetivo

Eliminar cualquier credencial/dato sensible escrito literalmente en el código o la
documentación operativa, dejando como única fuente de secretos las variables de
entorno (Fase 5, Hito 1).

## Auditoría realizada

- Búsqueda en todo el repo (código activo, legado, Docs, README, `.env.example`):
  tokens (`sk-`, `AKIA`, `Bearer`, `ghp_`…), claves privadas, literales no vacíos
  asignados a `password`/`secret`/`api_key`/`token`, emails personales, teléfonos.
- Único literal de credencial encontrado: `config.py:52`
  `os.getenv("OMDB_API_KEY", "trilogy")` — clave API hardcodeada como fallback en
  `DEFAULT_CONFIG` (reaparecía si se recreaba `config.json` sin variable de entorno).
- Referencias textuales a `"trilogy"` también en `README.md` (demo key) y en Docs
  históricos (6, 9, 11, 18) — estos últimos se conservan como historial del proceso.
- sin emails/personales reales (solo placeholders `example.com`); `.env.example` sin
  valores reales; no existe `.env` (`.gitignore` lo cubre).
- `user_manager.py` (código muerto) no contiene literales hardcodeados, pero guarda
  contraseñas en texto plano en `users.json` → anotado para un hito futuro de hashing.

## Cambios realizados

- `config.py` — fallback de `omdb_api_key` pasa de `"trilogy"` a `""`.
- `README.md` — se elimina la mención a la demo key `"trilogy"`; "Cómo Ejecutar"
  ahora indica configurar `OMDB_API_KEY` (export o `.env`, remitiendo a
  `.env.example`).

## Verificación

1. `py_compile` de `config.py` → OK.
2. `grep "trilogy"` en `config.py` y `README.md` → 0 coincidencias.
3. Camino de defaults: borrado temporal de `config.json` → `load_config()` recrea el
   archivo y devuelve `omdb_api_key == ""` (sin `"trilogy"`); `config.json`
   restaurado después; archivo recreado sin secretos (`grep trilogy` → 0).
4. El entorno sigue mandando: `OMDB_API_KEY=x` → `api.omdb.API_KEY_OMDB == "x"`.
5. App intacta: opción 12 → exit 0 y "¡Hasta luego!"; exportar e2e → exit 0 y
   "Exportado a respaldo.json".

## Estado del proyecto

- Fases 1–4 completadas.
- Fase 5: Hito 1 (secretos a variables de entorno) y Hito 2 (eliminar hardcodeados
  sensibles) completados.
- Restan para esta fase: `user_manager.py` con contraseñas en texto plano (código
  muerto, fuera del alcance de "hardcodeados") y otras mejoras de seguridad.