# Hito 1: Diagnóstico de Variables Globales

**Objetivo:** Identificar, auditar y documentar todas las variables globales presentes en los archivos `api_movies.py` y `main.py`.

**Fecha:** 2026-09-17

**Regla aplicada:** Sin modificación de archivos — solo diagnóstico.

---

## Archivo: `api_movies.py`

### 1. Constantes de Configuración de APIs

| Línea | Variable | Tipo/Propósito | Lectores | Escritores | Riesgo | Propuesta |
|-------|----------|----------------|----------|------------|--------|-----------|
| 5 | `API_KEY_OMDB` | `str` — Key demo para OMDB API | `buscar_pelicula()`, `buscar_peliculas_por_actor()` | Ninguno | Hardcoded en código; acoplamiento | `os.environ.get("OMDB_API_KEY")` o dataclass `APIConfig` |
| 6 | `API_KEY_TMDB` | `str` — Key vacía (no usada) | Ninguno | Ninguno | Código muerto | Eliminar |
| 7 | `BASE_URL_OMDB` | `str` — URL base OMDB | `buscar_pelicula()`, `buscar_peliculas_por_actor()` | Ninguno | Hardcoded | Mover a `APIConfig` dataclass |
| 8 | `BASE_URL_TMDB` | `str` — URL base TMDB (no usada) | Ninguno | Ninguno | Código muerto | Eliminar |
| 9 | `BASE_URL_TVMAZE` | `str` — URL base TVMaze | `buscar_series()`, `obtener_detalles_serie()` | Ninguno | Hardcoded | Mover a `APIConfig` dataclass |

### 2. Estado Mutable de Sesión

| Línea | Variable | Tipo/Propósito | Lectores | Escritores | Riesgo | Propuesta |
|-------|----------|----------------|----------|------------|--------|-----------|
| 12 | `USUARIO_LOGUEADO` | `None` — Estado de sesión usuario | Ninguno (no se usa) | Ninguno | Código muerto; nunca implementado | Eliminar o implementar `UserSession` class |
| 13 | `PELICULAS_FAVORITAS` | `list[dict]` — Lista de películas favoritas | `obtener_estadisticas()`, `exportar_a_json()` | `agregar_a_favoritas()`, `eliminar_de_favoritas()`, `importar_de_json()` | **Alto**: mutación compartida, sin persistencia automática, acoplamiento global | Encapsular en `FavoritesRepository` class |
| 14 | `HISTORIAL_BUSQUEDAS` | `list[dict]` — Historial de búsquedas | `obtener_estadisticas()`, `exportar_a_json()` | `agregar_al_historial()`, `limpiar_historial()`, `importar_de_json()` | **Alto**: sin límite de tamaño, sin timestamp real ("hoy" hardcoded) | Encapsular en `HistoryRepository` class |
| 15 | `CACHE_PELICULAS` | `dict` — Cache en memoria para películas OMDB | `buscar_pelicula()` | `buscar_pelicula()` | **Medio**: sin expiración, crece indefinidamente, no thread-safe | Encapsular en `CacheService` class con TTL |
| 16 | `CACHE_SERIES` | `dict` — Cache en memoria para series TVMaze | `buscar_series()` | `buscar_series()` | **Medio**: mismo problema que `CACHE_PELICULAS` | Unificar con `CacheService` |
| 17-22 | `CONFIG` | `dict` — Configuración general (debug, verbose, timeout, max_retries) | `hacer_request()` | `main.py:funcion_configuracion()` | **Alto**: mutación directa sin validación, acoplamiento implícito con `main.py` | Dataclass `AppConfig` con validación |

### 3. Mapa de Side Effects

```
api_movies.py
├── PELICULAS_FAVORITAS ←→ agregar_a_favoritas()
│                        ←→ eliminar_de_favoritas()
│                        ←→ obtener_estadisticas()
│                        ←→ exportar_a_json()
│                        ←→ importar_de_json()
│
├── HISTORIAL_BUSQUEDAS  ←→ agregar_al_historial()
│                        ←→ limpiar_historial()
│                        ←→ obtener_estadisticas()
│                        ←→ exportar_a_json()
│                        ←→ importar_de_json()
│
├── CACHE_PELICULAS      ←→ buscar_pelicula()
├── CACHE_SERIES         ←→ buscar_series()
├── CONFIG               ←→ hacer_request()
```

---

## Archivo: `main.py`

### 1. Importación Wildcard (Problema Crítico)

| Línea | Problema | Impacto | Propuesta |
|-------|----------|---------|-----------|
| 7 | `from api_movies import *` | Importa **todas** las variables globales de `api_movies.py` al namespace de `main.py`. Namespace pollution masivo. Imposible rastrear origen de variables. | Imports específicos: `from api_movies import buscar_pelicula, agregar_a_favoritas, ...` |

### 2. Variables Importadas Usadas en `main.py`

Estas variables son accedidas **directamente** desde `main.py` vía wildcard import:

| Línea | Variable (de api_movies) | Uso en main.py | Funciones que la usan | Riesgo |
|-------|--------------------------|----------------|----------------------|--------|
| 198 | `PELICULAS_FAVORITAS` | Lectura directa para iterar y mostrar | `funcion_ver_favoritos()` | Acoplamiento directo con estado global |
| 209 | `PELICULAS_FAVORITAS` | Lectura para obtener título al eliminar | `funcion_ver_favoritos()` | — |
| 219 | `HISTORIAL_BUSQUEDAS` | Lectura directa para iterar y mostrar | `funcion_ver_historial()` | Acoplamiento directo con estado global |
| 260-273 | `CONFIG` | Lectura/escritura directa para mostrar y modificar configuración | `funcion_configuracion()` | **Mutación directa** sin validación |

### 3. Funciones que Modifican Estado Global Indirectamente

| Línea | Función | Acción | Estado Afectado |
|-------|---------|--------|-----------------|
| 116-128 | `funcion_buscar_pelicula()` | Llama a `agregar_al_historial()` y `agregar_a_favoritas()` | `HISTORIAL_BUSQUEDAS`, `PELICULAS_FAVORITAS` |
| 209 | `funcion_ver_favoritos()` | Llama a `eliminar_de_favoritas()` | `PELICULAS_FAVORITAS` |
| 227 | `funcion_ver_historial()` | Llama a `limpiar_historial()` | `HISTORIAL_BUSQUEDAS` |
| 246 | `funcion_exportar()` | Llama a `exportar_a_json()` | Archivo externo |
| 252 | `funcion_importar()` | Llama a `importar_de_json()` | `PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS` |

---

## Resumen de Hallazgos

| Categoría | Cantidad | Severidad |
|-----------|----------|-----------|
| Constantes hardcoded | 5 | Media |
| Estado mutable global | 6 | **Alta** |
| Código muerto (variables no usadas) | 3 (`API_KEY_TMDB`, `BASE_URL_TMDB`, `USUARIO_LOGUEADO`) | Baja |
| Wildcard import | 1 | **Crítica** |
| Funciones con side effects no documentados | 10+ | Alta |

---

## Ranking de Prioridad de Refactorización

1. **`PELICULAS_FAVORITAS`** — Estado mutable compartido, sin persistencia, sin validación
2. **`HISTORIAL_BUSQUEDAS`** — Mismo problema + sin límite de tamaño + timestamp falso
3. **`CONFIG`** — Mutado directamente desde `main.py` sin validación
4. **`CACHE_PELICULAS` / `CACHE_SERIES`** — Cache sin expiración, crece indefinidamente
5. **Wildcard import** — Namespace pollution, imposible mantener
6. **Constantes de API** — Hardcoded, no configurables sin modificar código

---

## Estado: Diagnóstico Completo ✅

**Siguiente paso:** Aguardando instrucciones para definir la estrategia de refactorización.
