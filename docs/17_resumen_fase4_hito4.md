# Resumen Fase 4 — Hito 4: Eliminar `print()` de depuración

## Objetivo

Eliminar todos los `print()` de capas no-UI (lógica de negocio y utilidades).
El módulo estándar `logging` (Hito 3) pasa a ser la única vía de salida de datos
informativos/diagnósticos fuera de la interfaz de usuario.

## Cambios realizados

### `services/movie_service.py`
- `exportar_a_json`: `print(f"Exportado a {nombre_archivo}")` →
  `logger.info("Exportado a %s", nombre_archivo)`.
- `importar_de_json`: `print(f"Importado desde {nombre_archivo}")` →
  `logger.info("Importado desde %s", nombre_archivo)`.

Las confirmaciones textuales (texto idéntico) se reubican en la capa UI
(ver `ui/menu.py`), preservando lo que ve el usuario.

### `ui/menu.py`
- `funcion_exportar`: tras `exportar_a_json(...)` añade
  `print(f"Exportado a {nombre}{EXTENSION_JSON}")`.
- `funcion_importar`: en la rama de éxito añade
  `print(f"Importado desde {nombre}{EXTENSION_JSON}")`; la rama de error
  (`logger.exception` + `MSG_ERROR_IMPORTAR`) queda intacta.

### `config.py`
- Se añade `logger = logging.getLogger(__name__)`.
- `print_config()`: docstring actualizado y el bucle pasa de `print(f"{key}: {value}")`
  a `logger.info("%s: %s", key, value)`. (Utilidad de diagnóstico; no usada por la
  app activa → sin cambio observable.)

## Capas sin cambios (output legítimo)

- `ui/menu.py` y `ui/display.py`: todos sus `print` son interfaz de usuario
  (menú, resultados, confirmaciones, mensajes) → se conservan.
- `main.py`: `print` solo para mensajes de usuario al salir (interrupción/error).

## Verificación

1. `py_compile` de los 3 archivos → OK.
2. `grep "print("` en `api/`, `services/`, `config.py`, `models/`, `exceptions/`
   → **0 coincidencias**.
3. Servicios llamados directamente: sin salida por stdout; los eventos quedan en log
   `INFO services.movie_service — Exportado a ... / Importado desde ...`.
4. Vía menú: `funcion_exportar` y `funcion_importar` muestran en stdout el texto
   idéntico al original (`Exportado a X.json` / `Importado desde X.json`).
5. Fallo de importación: `print(MSG_ERROR_IMPORTAR)` + `logger.exception` con
   traceback, intactos.
6. `print_config()` → registra `INFO config ...` sin tocar stdout.
7. Extremo a extremo en `main.py`:
   - opción 9 (exportar) → confirma en UI, crea `respaldo.json`, exit 0;
   - opción 10 (importar) → confirma en UI, exit 0;
   - "¡Hasta luego!" presente en ambos, salida limpia.

## Estado del proyecto

- Fase 2 completada (Hitos 1–5).
- Fase 3 completada (Hitos 1–3).
- Fase 4 completada (Hitos 1–4): excepciones propias, capturas específicas,
  logging y eliminación de `print()` de depuración.
- Separación por capas: `api/` (HTTP), `services/` (lógica+logging),
  `ui/` (única capa que imprime a usuario), `main.py` (orquestación simple).
- Sin cambios en lógica de negocio ni firmas públicas. Código muerto (legado) fuera
  de alcance.