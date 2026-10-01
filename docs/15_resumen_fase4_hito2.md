# Resumen Fase 4 — Hito 2: Reemplazo de `bare except` por excepciones específicas

## Objetivo

Eliminar las capturas genéricas (`except:`) en los módulos activos de la aplicación y
sustituirlas por excepciones específicas. Aplica el hallazgo del diagnóstico
`Docs/04_diagnostico_manejo_excepciones.md` (H1–H10): los `bare except` enmascaran
`KeyboardInterrupt`/`SystemExit` y ocultan errores reales.

Los `bare except` remanentes viven en código muerto (`utils.py`, `*_manager.py`,
`app.py`) — fuera del alcance de la app activa.

## Cambios realizados

### `ui/display.py` — 9 bloques en `mostrar_pelicula()`

| Antes | Después |
|---|---|
| `try: print(...); except:` | `try: print(...); except KeyError:` |

Los 9 accesos directos a dict (`pelicula['Title']`, `['Year']`, `['imdbRating']`,
`['Genre']`, `['Director']`, `['Actors']`, `['Plot']`, `['Country']`, `['Awards']`)
solo pueden fallar por `KeyError`. La estructura try/except se conserva y el fallback
`N_A` produce la misma salida. Ya no se enmascaran errores ajenos (p. ej. `TypeError`
si el dato no fuese dict).

### `ui/menu.py` — `funcion_importar()`

```python
import json  # añadido al módulo

try:
    importar_de_json(f"{nombre}{EXTENSION_JSON}")
except (FileNotFoundError, PermissionError, json.JSONDecodeError):
    print(MSG_ERROR_IMPORTAR)
```

Las excepciones reales de `importar_de_json`: archivo inexistente
(`FileNotFoundError`), permisos (`PermissionError`) y JSON inválido
(`json.JSONDecodeError`, subclase de `ValueError`). Mismo `MSG_ERROR_IMPORTAR`.

### `main.py` — aduana de dominio en la entrada

Inserción entre `except KeyboardInterrupt` y el catch-all final:

```python
from exceptions import AppError
...
except AppError as e:
    print(f"{MSG_ERROR_INESPERADO}{e}")
    sys.exit(EXIT_ERROR)
```

Prepara la entrada para los hitos 3–4, cuando los servicios empiecen a lanzar las
excepciones personalizadas del Hito 1.

## Verificación

1. `py_compile` de los 3 archivos → OK.
2. `mostrar_pelicula` con dict completo → 9 campos renderizados.
3. `mostrar_pelicula` con dict sin claves → 8 × `N_A` (idéntico al comportamiento previo).
4. `mostrar_pelicula(None)` → `MSG_NO_ENCONTRADA`.
5. `funcion_importar`: archivo inexistente → `MSG_ERROR_IMPORTAR`; JSON corrupto → `MSG_ERROR_IMPORTAR`; JSON válido → favoritas/historial cargados.
6. `python3 main.py` (input `12`) → menú completo y "¡Hasta luego!" (exit 0).
7. Handler `except AppError`: al lanzar `MovieNotFoundError('Matrix')` desde `menu_principal`, main imprime `MSG_ERROR_INESPERADO` + "No se encontró la película: Matrix" y sale con `EXIT_ERROR`.
8. `grep 'except:'` en `main.py`, `ui/`, `api/`, `services/`, `models/`, `exceptions/` → **0 coincidencias**.

## Estado del proyecto

- Fase 2 completada (Hitos 1–5).
- Fase 3 completada (Hitos 1–3).
- Fase 4: Hito 1 (paquete `exceptions/`) y Hito 2 (capturas específicas) completados.
- Sin cambios en lógica de negocio, firmas públicas ni dependencias.