# Resumen Fase 6 — Hito 1: Crear `tests/` con pytest

## Objetivo

Poner en marcha la infraestructura de testing del proyecto (Fase 6) y escribir los
primeros tests unitarios sobre los módulos de lógica pura —aquellos sin efectos de red
ni estado global— dejando los tests de servicios (Hito 2) y las integraciones con APIs
(Hito 3) para los hitos siguientes, según el plan de la Fase 6.

## Cambios realizados

### Dependencias y entorno
- `requirements.txt`: se añaden `pytest>=7.0`, `pytest-cov>=4.1` y `pytest-mock>=3.12`.
- Se crea el entorno virtual `.venv/` (venv del proyecto) y se instalan
  `pip install -r requirements.txt pytest pytest-cov pytest-mock`.
  Instalado en el entorno: pytest 9.1.1, coverage 7.16.1, pytest-mock 3.15.1.
- Nota: `json5` figura en `requirements.txt` pero no se importa en ningún módulo
  (dependencia muerta, heredada). Se instaló igual en `.venv` para que el entorno
  coincida con lo declarado.

### Configuración de testing
- `pytest.ini` (nuevo, raíz):
  - `testpaths = tests`
  - `pythonpath = .` → permite `import config`, `api.*`, `services.*`, etc. desde `tests/`.
  - `addopts = --cov=config --cov=constants --cov=exceptions --cov=models --cov=services
    --cov=ui --cov=api --cov-report=term-missing` → el reporte de coverage acompaña
    cada corrida para medir progreso hacia la meta del 80%.
- `.coveragerc` (nuevo, raíz):
  - `source` limita a los paquetes medibles del proyecto.
  - `omit` excluye `tests/*` y `*_manager.py` → los managers raíz son código muerto
    (no importados); si contaran, arrastrarían el % e impedirían alcanzar la meta.
- `.gitignore`: se añaden `.venv/`, `__pycache__/`, `.pytest_cache/` y `.coverage`.
  (Hasta ahora solo ignoraba `.env`).

### Tests creados
- `tests/test_validation.py` (40 casos parametrizados): cubre todos los validadores de
  `ui/validation.py` — `validar_texto_busqueda` (vacío/espacios/>120, longitud máxima),
  `validar_genero` (normalización a minúsculas, rechazo de "Acción"/"horror"),
  `validar_nombre_archivo` (`.`/`..`, path traversal `../evil`, separadores `/` y `\`,
  >100 caracteres), `validar_entero` (rango 1..300, no numérico) e
  `indice_seleccion` (1-based→0-based, fuera de rango). Reutiliza los casos unitarios
  ya documentados en `Docs/20_resumen_fase5_hito3.md`.
- `tests/test_models.py` (9 casos): `Movie.from_omdb` (mapeo de campos, claves faltantes
  → defaults, `to_dict`) y `Series.from_tvmaze` (desenvuelve el wrapper `show`,
  `rating.average`, item sin wrapper, `to_dict`).
- `tests/test_exceptions.py` (5 casos): jerarquía `AppError`→ todas las excepciones
  personalizadas, mensajes, `ApiRequestError` con/sin endpoint y captura como `AppError`.

## Verificación

1. `python3 -m pytest -v` (desde `.venv`):
   - **70 passed** en 0.23s.
   - Coverage por módulo objetivo: `ui/validation.py`, `models/*`, `exceptions/*` al
     **100%**; `api/*`, `services/*`, `ui/menu.py` y `ui/display.py` aún al 0% (son
     precisamente el alcance de Hitos 2 y 3).
   - **Total global: 23%** (Hitos 2/3 elevarán el número hacia el objetivo ≥80%).
   - `config.py` y `constants.py` no se importan todavía desde los tests, por lo que
     otros detalles no aparecen en el reporte (se abarcarán en el Hito 2); coverage
     emite dos avisos informativos al respecto (`module-not-imported`).
2. Regresión extremo a extremo: `echo "12" | python main.py` → imprime el menú y
   "¡Hasta luego!", exit code 0 (mismo control que en Hito 5.3).

## Estado del proyecto

- **Hito 1 de Fase 6 completo** ✅: infraestructura pytest operativa + primeros tests
  unitarios (validación, modelos, excepciones).
- Pendiente para el **Hito 2** (tests unitarios de servicios, con mockeo de APIs):
  - Fixtures de reseteo de estado global en `tests/conftest.py`
    (`PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_*`) — los servicios guardan
    estado a nivel de módulo con `global` y no se resetean solos.
  - Aislamiento de `config.py` en pruebas (p. ej. `monkeypatch` de `CONFIG_FILE` a
    `tmp_path`) para no leer ni persistir el `config.json` real.
  - Mock de `api/omdb.py` / `api/tvmaze.py` / `http_client.hacer_request` con
    `pytest-mock` (evitar llamadas reales a la red).
- Pendiente para el **Hito 3** (integración de APIs): pruebas de `hacer_request` y del
  flujo completo, y medición final del 80% de coverage.

## Cómo correr los tests

```bash
source .venv/bin/activate   # o usar .venv/bin/python directamente
pytest -v
```