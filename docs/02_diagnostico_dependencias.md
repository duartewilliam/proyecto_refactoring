# Hito 2: Diagnóstico de Dependencias e Importaciones

**Objetivo:** Mapear y analizar el árbol de dependencias e importaciones entre todos los módulos del proyecto.

**Fecha:** 2026-09-17

**Regla aplicada:** Sin modificación de archivos — solo diagnóstico.

---

## 1. Resumen Ejecutivo

**Hallazgo clave:** El proyecto tiene un acoplamiento paradójico — los módulos están **aislados a nivel de imports** (casi ninguno importa de otro), pero están **fuertemente acoplados a nivel de estado global** compartido.

---

## 2. Matriz de Dependencias Internas

### Única dependencia directa entre módulos del proyecto:

```
main.py ──wildcard──▶ api_movies.py
```

**No hay dependencias circulares** porque los módulos no se importan entre sí.

---

## 3. Diagrama Mermaid — Arquitectura Actual

```mermaid
graph TD
    subgraph "Entrada"
        MAIN["main.py"]
        APP["app.py<br/>(legacy/alternativo)"]
    end

    subgraph "Lógica de Negocio"
        API["api_movies.py"]
    end

    subgraph "Gestores (aislados, sin uso)"
        CM["cache_manager.py"]
        CFG["config_manager.py"]
        DM["data_manager.py"]
        FAV["favorites_manager.py"]
        HIST["history_manager.py"]
        ERR["error_manager.py"]
        LOG1["logger.py"]
        LOG2["log_manager.py"]
        EXP["export_manager.py"]
        UTILS["utils.py"]
        AUDIT["audit_manager.py"]
        BACKUP["backup_manager.py"]
        META["metadata_manager.py"]
        NOTIFY["notification_manager.py"]
        PERM["permission_manager.py"]
        PLUGIN["plugin_manager.py"]
        REPORT["report_manager.py"]
        SCHED["schedule_manager.py"]
        SETT["settings_manager.py"]
        STATE["state_manager.py"]
        STATS["stats_manager.py"]
        TAG["tag_manager.py"]
        USER["user_manager.py"]
        VER["version_manager.py"]
        FEAT["feature_manager.py"]
    end

    subgraph "Configuración (~85 archivos, aislados)"
        CACHE_CFG["cache_config.py"]
        API_CFG["api_config.py"]
        SEC["security_config.py"]
        OTROS["... 82 archivos *_config.py"]
    end

    MAIN -->|"from api_movies import *"| API
    APP -.->|"copia duplicada"| API

    style MAIN fill:#ff6b6b,stroke:#333
    style API fill:#ff6b6b,stroke:#333
    style APP fill:#ffa07a,stroke:#333
    style CM fill:#69db7c,stroke:#333
    style CFG fill:#69db7c,stroke:#333
    style DM fill:#69db7c,stroke:#333
    style FAV fill:#69db7c,stroke:#333
    style HIST fill:#69db7c,stroke:#333
    style ERR fill:#69db7c,stroke:#333
    style LOG1 fill:#69db7c,stroke:#333
    style LOG2 fill:#69db7c,stroke:#333
    style EXP fill:#69db7c,stroke:#333
    style UTILS fill:#69db7c,stroke:#333
```

---

## 4. Clasificación por Capas (Estado Actual)

| Capa | Archivos | Estado |
|------|----------|--------|
| **Entrada** | `main.py`, `app.py` | ❌ Duplicados, mezclan UI + lógica |
| **Lógica/API** | `api_movies.py` | ❌ Mezcla API + negocio + estado global |
| **Gestores** | 22 archivos `*_manager.py` | ⚠️ Aislados, **no importados por nadie** |
| **Configuración** | ~85 archivos `*_config.py` | ⚠️ Aislados, **no importados por nadie** |
| **Utilidades** | `utils.py` | ⚠️ Aislado, **no importado por nadie** |

---

## 5. Dependencias Estándar por Módulo

| Módulo | `os` | `json` | `time` | `datetime` | `csv` | `sys` | `random` | `requests` |
|--------|:----:|:------:|:------:|:----------:|:-----:|:-----:|:--------:|:----------:|
| `api_movies.py` | - | ✅ | - | - | - | - | - | ✅ |
| `main.py` | ✅ | - | ✅ | - | - | ✅ | ✅ | - |
| `app.py` | ✅ | ✅ | ✅ | - | - | ✅ | ✅ | ✅ |
| `*_manager.py` (22) | ✅ | ✅ | ✅ | ✅ | Algunos | - | - | - |
| `*_config.py` (~85) | ✅ | ✅ | ✅ | ✅ | - | - | - | - |
| `utils.py` | ✅ | - | ✅ | ✅ | - | ✅ | ✅ | - |

**Única dependencia externa:** `requests` (usada por `api_movies.py` y `app.py`)

---

## 6. Análisis de Acoplamiento

| Módulo | Acoplamiento | Razón |
|--------|:------------:|-------|
| `api_movies.py` | **ALTO** | 6 variables globales mutables + wildcard import hacia `main.py` |
| `main.py` | **ALTO** | Depende 100% de `api_movies.py` vía wildcard, accede directo a su estado |
| `app.py` | **MEDIO** | Duplicado de `api_movies.py` + `main.py`, autocontenido |
| `*_manager.py` (22) | **BAJO** | Completamente aislados, pero **muertos** (nadie los usa) |
| `*_config.py` (~85) | **BAJO** | Completamente aislados, pero **muertos** (nadie los usa) |
| `utils.py` | **BAJO** | Completamente aislado, **muerto** (nadie lo usa) |

---

## 7. Problemas Críticos Identificados

### 7.1 Código Muerto Masivo
- **22 gestores** (`*_manager.py`) no son importados por ningún módulo
- **~85 archivos de configuración** no son importados por ningún módulo
- `utils.py` no es importado por ningún módulo
- `app.py` es una copia duplicada de `api_movies.py` + partes de `main.py`

### 7.2 Acoplamiento por Estado Global (no por imports)
Aunque los módulos no se importan entre sí, están acoplados implícitamente:
- `main.py` modifica `CONFIG` de `api_movies.py` directamente
- `main.py` lee/escribe `PELICULAS_FAVORITAS` y `HISTORIAL_BUSQUEDAS` de `api_movies.py`
- Todo el estado vive en variables globales mutables

### 7.3 Duplicación Funcional
| Funcionalidad | Implementaciones |
|---------------|------------------|
| Cache | `cache_manager.py`, `cache_manager_v2.py`, `cache_config.py`, `CACHE_PELICULAS`/`CACHE_SERIES` en `api_movies.py` |
| Logging | `logger.py`, `log_manager.py`, `log_config.py` |
| Configuración | `config_manager.py`, `config_manager_v2.py`, `api_config.py`, `CONFIG` en `api_movies.py` |
| Favoritos | `favorites_manager.py`, `PELICULAS_FAVORITAS` en `api_movies.py` |
| Historial | `history_manager.py`, `HISTORIAL_BUSQUEDAS` en `api_movies.py` |
| Exportación | `export_manager.py`, `exportar_a_json()` en `api_movies.py` |

---

## 8. Propuesta de Jerarquía de Capas (Target)

```mermaid
graph TD
    subgraph "Capa 3: Interfaz/UI"
        MENU["ui/menu.py"]
        DISPLAY["ui/display.py"]
        MAIN_NEW["main.py"]
    end

    subgraph "Capa 2: Servicios de Negocio"
        MOVIE_SVC["services/movie_service.py"]
        SERIES_SVC["services/series_service.py"]
        FAV_SVC["services/favorites_service.py"]
        HIST_SVC["services/history_service.py"]
    end

    subgraph "Capa 1: Acceso a Datos/APIs"
        OMDB["api/omdb_client.py"]
        TVMAZE["api/tvmaze_client.py"]
        CACHE["cache/cache_service.py"]
    end

    subgraph "Capa 0: Modelos y Config"
        MODELS["models/movie.py<br/>models/series.py"]
        CONFIG["config/settings.py"]
        EXC["exceptions/custom.py"]
    end

    MAIN_NEW --> MENU
    MENU --> MOVIE_SVC
    MENU --> SERIES_SVC
    MENU --> FAV_SVC
    MENU --> HIST_SVC
    DISPLAY --> MODELS

    MOVIE_SVC --> OMDB
    MOVIE_SVC --> CACHE
    SERIES_SVC --> TVMAZE
    SERIES_SVC --> CACHE
    FAV_SVC --> MODELS
    HIST_SVC --> MODELS

    OMDB --> CONFIG
    TVMAZE --> CONFIG
    CACHE --> CONFIG

    style MAIN_NEW fill:#4dabf7,stroke:#333
    style MENU fill:#4dabf7,stroke:#333
    style DISPLAY fill:#4dabf7,stroke:#333
    style MOVIE_SVC fill:#69db7c,stroke:#333
    style SERIES_SVC fill:#69db7c,stroke:#333
    style FAV_SVC fill:#69db7c,stroke:#333
    style HIST_SVC fill:#69db7c,stroke:#333
    style OMDB fill:#ffd43b,stroke:#333
    style TVMAZE fill:#ffd43b,stroke:#333
    style CACHE fill:#ffd43b,stroke:#333
    style MODELS fill:#da77f2,stroke:#333
    style CONFIG fill:#da77f2,stroke:#333
    style EXC fill:#da77f2,stroke:#333
```

---

## 9. Resumen Cuantitativo

| Métrica | Valor |
|---------|-------|
| Total archivos Python | 124 |
| Archivos con código vivo (usados) | 2 (`api_movies.py`, `main.py`) |
| Archivos muertos (no importados) | 122 |
| Archivos duplicados funcionales | ~6 (`app.py`, managers vs api_movies) |
| Dependencias externas | 1 (`requests`) |
| Dependencias circulares | 0 |
| Wildcard imports | 1 (crítico) |

---

## Estado: Diagnóstico Completo ✅

**Siguiente paso:** Aguardando instrucciones para la fase de refactorización.
