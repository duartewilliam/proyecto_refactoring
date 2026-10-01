# Resumen Fase 3 — Hito 2: Separación de `main.py` en `ui/menu.py` y `ui/display.py`

## Objetivo

Separar `main.py` (427 → 18 líneas) en:

- `ui/display.py` → lógica de visualización pura (sin estado, sin servicios).
- `ui/menu.py` → lógica de menú (flujo de opciones, input, dispatch y orquestación).
- `main.py` → solo punto de entrada.

Se conserva la lógica, las firmas públicas y el comportamiento observado. Única
modificación de comportamiento nulo: se elimina `import random` (muerto, nunca usado).

## Cambios realizados

### Creados (3 archivos)

| Archivo | Contenido |
|---|---|
| `ui/__init__.py` | Marcador de paquete `ui` |
| `ui/display.py` | `clear_screen`, `print_separator`, `print_header`, `mostrar_pelicula`, `mostrar_serie`, `mostrar_lista_peliculas` |
| `ui/menu.py` | `delay`, `funcion_buscar_pelicula`, `funcion_buscar_actor`, `funcion_buscar_series`, `funcion_peliculas_populares`, `funcion_buscar_por_genero`, `funcion_ver_favoritos`, `funcion_ver_historial`, `funcion_estadisticas`, `funcion_exportar`, `funcion_importar`, `funcion_configuracion`, `menu_principal` |

### Modificado (1 archivo)

| Archivo | Antes | Después |
|---|---|---|
| `main.py` | 427 líneas, 20 funciones, 4 imports std + 3 bloques de dominio | 18 líneas: `sys`, 4 constantes, `from ui.menu import menu_principal` y el bloque `if __name__ == "__main__"` con `try/except` intacto |

## Migración de funciones

| Función | Origen | Destino |
|---|---|---|
| `clear_screen`, `print_separator`, `print_header` | `main` | `ui.display` |
| `mostrar_pelicula`, `mostrar_serie`, `mostrar_lista_peliculas` | `main` | `ui.display` |
| `delay` | `main` | `ui.menu` (sus 2 llamadores viven allí) |
| 11 × `funcion_*` + `menu_principal` | `main` | `ui.menu` |
| `if __name__ == "__main__"` + `try/except` | `main` | `main` (sin cambios) |

## Comparativa de imports

| Módulo | Imports |
|---|---|
| `ui/display.py` | `os`, ~26 constantes (`CLS_*`, `SEPARADOR*`, `ANCHO_CENTRADO`, `RESUMEN_MAX_LONGITUD`, `SUFRAGO_RESUMEN`, `N_A`, `MSG_NO_ENCONTRADA`, `MSG_PELICULA_DESCONOCIDA`, `LABEL_*`, `PREFIJO_NUMERACION`, `ABRIR_PARENTESIS`, `CERRAR_PARENTESIS*`) — sin servicios |
| `ui/menu.py` | `time`; `CONFIG` de `api.http_client`; 13 símbolos de `services.movie_service`; 2 de `services.series_service`; 6 helpers de `ui.display`; ~58 constantes (`PROMPT_*`, `MSG_*`, `OPCION_MENU_*`, `HEADER_*`, `LABEL_*`) |
| `main.py` | `sys`, 4 constantes (`EXIT_OK`, `EXIT_ERROR`, `MSG_PROGRAMA_INTERRUMPIDO`, `MSG_ERROR_INESPERADO`), `menu_principal` |

Dependencias: `display → constants`; `menu → display + services + api`; `main → menu`. Sin circularidades.

## Decisiones aplicadas

- `import random` muerto se elimina (aprobado por el usuario). Solo persiste en `utils.py` (código muerto, fuera de alcance).
- `delay` se ubica en `ui/menu.py` (ambos llamadores residen en menú).
- Granularidad mínima: cada handler completo se mueve tal cual; `display.py` solo recibe las funciones 100 % de visualización. Los `print`/`input` inline de los handlers quedan en su flujo original.

## Verificación

1. `py_compile` de `main.py`, `ui/__init__.py`, `ui/display.py`, `ui/menu.py` → OK.
2. `import main` → wiring sin errores.
3. Identidad de estado: `menu.CONFIG is api.http_client.CONFIG`; `PELICULAS_FAVORITAS` y `HISTORIAL_BUSQUEDAS` compartidos entre `menu` y `movie_service`.
4. `menu_principal()` con `input`→`"12"` → imprime `MSG_HASTA_LUEGO` y rompe el lazo.
5. `funcion_configuracion()` con opción 1 → togglea `CONFIG['debug']` visible vía `api.http_client.CONFIG` (mismo dict).
6. `funcion_buscar_pelicula()` end-to-end (`requests.get` y `input` mockeados) → `MSG_AGREGADA_FAVORITOS`, historial=1, favorita=1 con título correcto.
7. `display.py`: `mostrar_pelicula(None)` → `MSG_NO_ENCONTRADA`; `mostrar_serie` y `mostrar_lista_peliculas` con salidas byte-idénticas en sus 3 ramas.
8. `grep "import random"` → solo en `utils.py`; `grep "api_movies\|from main import"` → 0 coincidencias.

## Estado del proyecto

- Fase 2 completada (Hitos 1–5).
- Fase 3: Hito 1 (api/services) y Hito 2 (ui/) completados.
- Sin cambios en lógica de negocio, firmas públicas ni dependencias (`requests`, `json5`).