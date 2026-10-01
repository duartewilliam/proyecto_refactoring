# Fase 2, Hito 2: Resumen de Ejecución — Módulo `constants.py`

**Fecha:** 2026-09-22

**Objetivo:** Centralizar los valores hardcodeados (números mágicos, textos de UI, parámetros de API y datos mock) en un módulo único `constants.py`, sin alterar lógica de negocio.

**Alcance (decisiones previas):**
- Los datos mock (películas populares/acción/comedia) se ubican en `constants.py`
- Se migran TODOS los mensajes/prompts de UI de `main.py` (no solo los mágicos/repetidos)

---

## 1. Archivo Creado — `constants.py` (185 líneas, 94 constantes)

| Sección | Constantes |
|---------|-----------|
| Sistema | `SISTEMA_TITULO`, `EXTENSION_JSON`, `EXIT_OK`, `EXIT_ERROR` |
| Comandos OS | `CLS_NT`, `CLS_UNIX` |
| UI / Display | `SEPARADOR`, `SEPARADOR_LONGITUD`, `ANCHO_CENTRADO`, `RESUMEN_MAX_LONGITUD`, `SUFRAGO_RESUMEN`, `N_A`, `CONFIRMAR_SI`, `CONFIRMAR_NO`, `PREFIJO_NUMERACION`, `ABRIR_PARENTESIS`, `CERRAR_PARENTESIS_RATING`, `CERRAR_PARENTESIS`, `MSG_PELICULA_DESCONOCIDA`, `MSG_PRESIONAR_ENTER` |
| APIs | `URL_PARAM_TITULO`, `URL_PARAM_BUSQUEDA`, `URL_PARAM_TIPO_PELICULA`, `URL_PARAM_API_KEY`, `URL_ENDPOINT_BUSCAR_SERIES`, `URL_ENDPOINT_DETALLES_SERIE`, `PREFIX_CACHE_SERIES` |
| Dominio | `GENERO_ACCION`, `GENERO_COMEDIA`, `FECHA_HARDCODEADA`, `MSG_GENEROS_DISPONIBLES` |
| Labels películas | `LABEL_TITULO`, `LABEL_ANIO`, `LABEL_RATING_IMDB`, `LABEL_RATING`, `LABEL_GENERO`, `LABEL_DIRECTOR`, `LABEL_ACTORES`, `LABEL_TRAMA`, `LABEL_PAIS`, `LABEL_PREMIOS` |
| Labels series | `LABEL_NOMBRE`, `LABEL_IDIOMA`, `LABEL_GENEROS`, `LABEL_ESTADO`, `LABEL_ESTRENO`, `LABEL_FINAL`, `LABEL_EPISODIOS`, `LABEL_RESUMEN` |
| Búsqueda | `PROMPT_TITULO`, `PROMPT_ACTOR`, `PROMPT_SERIE`, `PROMPT_GENERO`, `MSG_BUSCANDO`, `MSG_BUSCANDO_ACTOR`, `MSG_BUSCANDO_SERIES`, `MSG_NO_ENCONTRADA`, `MSG_NO_ENCONTRADAS_ACTOR`, `MSG_NO_ENCONTRADAS_SERIES` |
| Favoritos/Historial | `PROMPT_AGREGAR_FAVORITOS`, `MSG_AGREGADA_FAVORITOS`, `MSG_YA_EN_FAVORITOS`, `PROMPT_ELIMINAR_FAVORITA`, `MSG_ELIMINADA_FAVORITOS`, `MSG_SIN_FAVORITAS`, `PROMPT_LIMPIAR_HISTORIAL`, `MSG_HISTORIAL_LIMPIADO`, `MSG_SIN_HISTORIAL` |
| Selección en listas | `PROMPT_SELECCION_PELICULA`, `PROMPT_SELECCION_SERIE` |
| Estadísticas | `LABEL_TOTAL_FAVORITAS`, `LABEL_TOTAL_HISTORIAL` |
| Export/Import | `PROMPT_NOMBRE_ARCHIVO`, `MSG_ERROR_IMPORTAR` |
| Configuración | `LABEL_DEBUG_CONFIG`, `LABEL_VERBOSE_CONFIG`, `LABEL_TIMEOUT_CONFIG`, `PROMPT_OPCION_CONFIG`, `MSG_DEBUG_ACTUAL`, `MSG_VERBOSE_ACTUAL`, `PROMPT_NUEVO_TIMEOUT` |
| Headers / Menú | `HEADER_*` (5), `OPCION_MENU_1..12`, `PROMPT_SELECCION_OPCION`, `MSG_HASTA_LUEGO`, `MSG_OPCION_INVALIDA`, `MSG_PROGRAMA_INTERRUMPIDO`, `MSG_ERROR_INESPERADO` |
| Datos mock | `PELICULAS_POPULARES` (5), `PELICULAS_ACCION` (2), `PELICULAS_COMEDIA` (2) |

---

## 2. Archivos Modificados

### 2.1 `api_movies.py`
- Nuevo import `from constants import (...)` (13 símbolos)
- URL de OMDB título → `URL_PARAM_TITULO` + `URL_PARAM_API_KEY` (línea 44)
- URL de OMDB actor → `URL_PARAM_BUSQUEDA` + `URL_PARAM_TIPO_PELICULA` + `URL_PARAM_API_KEY` (línea 55)
- Cache key `"series_"` → `PREFIX_CACHE_SERIES` (línea 66)
- Endpoint TVMaze `/search/shows?q=` → `URL_ENDPOINT_BUSCAR_SERIES` (línea 70)
- Endpoint TVMaze `/shows/` → `URL_ENDPOINT_DETALLES_SERIE` (línea 78)
- `obtener_peliculas_populares()` → retorna `PELICULAS_POPULARES`
- `buscar_peliculas_por_genero()` → `GENERO_ACCION`, `GENERO_COMEDIA`, `PELICULAS_ACCION`, `PELICULAS_COMEDIA`
- Fecha `"hoy"` → `FECHA_HARDCODEADA` (línea 140)

### 2.2 `main.py`
- Nuevo import `from constants import (...)` (~70 símbolos)
- Comando `cls`/`clear` → `CLS_NT`/`CLS_UNIX`
- Separador `"=" * 60` → `SEPARADOR * SEPARADOR_LONGITUD`
- `.center(60)` → `.center(ANCHO_CENTRADO)`
- `[:200]` + `"..."` → `[:RESUMEN_MAX_LONGITUD]` + `SUFRAGO_RESUMEN`
- Todos los labels de películas/series → `LABEL_*`
- Todos los prompts, mensajes y headers → `PROMPT_*`, `MSG_*`, `HEADER_*`
- Extensión `".json"` → `EXTENSION_JSON`
- Opciones de menú → `OPCION_MENU_1..12` (impresiones individuales, sin cambiar el flujo de control)
- `sys.exit(0)`/`sys.exit(1)` → `EXIT_OK`/`EXIT_ERROR`

---

## 3. No Modificados (intencionalmente)

| Archivo | Por qué |
|---------|---------|
| `config.py` | Config dinámica persistida en JSON; no es ámbito de constantes estáticas |
| Managers y `utils.py` | Código muerto (diagnóstico 05); se refactorizan en hitos posteriores |
| Flujo de control (`if opcion == "1"` en menú/config) | Sin cambios de lógica; solo literales de display |

---

## 4. Verificación

| Prueba | Resultado |
|--------|:---------:|
| `python -m py_compile constants.py api_movies.py main.py` | ✅ |
| `import constants` | ✅ |
| `import api_movies` | ✅ |
| `import main` | ✅ |
| `obtener_peliculas_populares()` → 5 items, `[0]` = Shawshank | ✅ |
| `buscar_peliculas_por_genero('accion')` → 2, `('comedia')` → 2, otro → 4 | ✅ |
| `mostrar_pelicula()` → labels y fallbacks `N/A` correctos | ✅ |
| `mostrar_lista_peliculas()` → formato `1. Die Hard (1988) - 8.2` | ✅ |

---

## 5. Impacto Cuantitativo

| Métrica | Valor |
|---------|:-----:|
| Constantes centralizadas | **94** |
| Archivos creados | 1 |
| Archivos modificados | 2 |
| Archivos eliminados | 0 |
| Líneas de `constants.py` | 185 |

---

## Estado: Hito 2 Completo ✅

**Siguiente paso:** Aguardando instrucciones para el siguiente hito de la Fase 2 (eliminar wildcard imports, f-strings, type hints).