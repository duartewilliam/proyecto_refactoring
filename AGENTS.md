# AGENTS.md

Educational Python 3.12 app ("Películas y Series") being refactored phase-by-phase from an intentionally-poor codebase, driven by an AI agent per `Docs/*.md` (Spanish) phase reports.

## State and ground truth
- `Docs/*.md` (e.g. `Docs/20_resumen_fase5_hito3.md`) track what has been done and what is intentionally still wrong. Read the latest before editing.
- `README.md` is STALE — it still describes the original pre-refactor project (wildcards, ~100 files, no tests). Trust the code and `Docs/`, not README prose.
- Phases 1–5 are done. Fase 6 = testing (`Docs/21_resumen_fase6_hito1.md`, `Docs/22_resumen_fase6_hito2.md`, `Docs/23_resumen_fase6_hito3.md`): pytest infra + pure-logic + service unit tests (APIs mocked via `pytest-mock`) + API/integration + config + UI + e2e subprocess tests done. Coverage total ≈98% (target ≥80% met). `tests/conftest.py` has an autouse fixture that resets module-level service globals AND rebinds `ui.menu`'s references to them (reassignment via `limpiar_historial`/`importar_de_json` would otherwise break ordering). Known findings from Fase 6: fixed a latent `TypeError` in `config.validate_config` (non-numeric `timeout` → now `elif`); `main.py` is excluded from coverage (entry-point guard) but covered by subprocess e2e tests; `ui/menu.py` rests at ~94% (missing the `delay` body and the 1–11 dispatch `elif` branches in `menu_principal`).

## Commands
- Run: `python3 main.py` (interactive menu; OMDB lookups need `OMDB_API_KEY` in `.env`).
- Tests: `source .venv/bin/activate && pytest -v` (or `.venv/bin/python -m pytest`). Deps live in the `.venv`; system python has none of them. Coverage: pytest-cov is on by default via `pytest.ini` `addopts`.
- Verify non-test code the Docs-style way: `python3 -m py_compile <file>` or throwaway `python3 -c "..."` imports.
- No linter, formatter, or pre-commit is configured.
- `.venv/` and `tests/` exist; `*_manager.py` is still excluded from coverage in `.coveragerc` (dead code, imported nowhere).

## Config gotchas (`config.py`)
- Auto-runs `load_config()` on import; creates `config.json` from defaults if missing; loads `.env` with a hand-rolled parser (no python-dotenv in requirements).
- Secrets (keys in `SECRET_ENV`) always come from environment vars and override `config.json` — set `OMDB_API_KEY`, `SENDER_*`, `PROXY_*` in `.env`, never in `config.json`.
- `config.get()` is evaluated at import time. Module-level snapshots like `api/http_client.CONFIG` and `api/omdb.BASE_URL_OMDB` do NOT update after `config.set()` at runtime.
- The in-menu config screen mutates `api/http_client.CONFIG` in memory only; changes are not persisted via `config.set()`.

## Architecture / flow
- Entry: `main.py` → `ui/menu.py:menu_principal` → `services/movie_service.py` (holds module-level state via `global`) or `services/series_service.py` → `api/omdb.py` / `api/tvmaze.py` → `api/http_client.py:hacer_request`.
- `hacer_request` is deliberately raw `requests` with no error handling/retry — a known remaining bad practice.
- `models/` dataclasses (`Movie`, `Series`) exist but are not wired into services (which return raw dicts).
- All root `*_manager.py` files (audit/backup/cache/etc.) are DEAD CODE — imported nowhere. `user_manager.py` (plaintext passwords) is flagged for future hashing.

## Conventions
- Everything is Spanish: code comments, docs, UI strings, and `constants.py` messages. Add new UI strings to `constants.py` as Spanish constants, never hardcode.
- Input validation lives in `ui/validation.py`; services intentionally do NOT revalidate (behavior preservation is a documented constraint).
- When refactoring, preserve function signatures and business logic unless a phase explicitly allows changing them.