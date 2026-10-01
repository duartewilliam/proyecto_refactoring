# Resumen Fase 4 — Hito 1: Excepciones personalizadas (`exceptions/`)

## Objetivo

Introducir un paquete de excepciones de dominio tipado y jerárquico como base de la
Fase 4 "Manejo de Errores". Alineado con la propuesta del diagnóstico
`Docs/04_diagnostico_manejo_excepciones.md` (sección 5): base, API, no-encontrada,
datos inválidos, archivo y configuración.

Scaffold puro: se crean las excepciones sin integrarlas aún (los `except` existentes
se reemplazarán en hitos posteriores de la fase).

## Cambios realizados

### Creados (9 archivos)

| Archivo | Excepción(es) |
|---|---|
| `exceptions/__init__.py` | Re-exporta las 10 excepciones + `__all__` |
| `exceptions/base.py` | `AppError` (base del dominio) |
| `exceptions/movie_not_found.py` | `MovieNotFoundError` |
| `exceptions/series_not_found.py` | `SeriesNotFoundError` |
| `exceptions/api_error.py` | `ApiRequestError`, `ApiTimeoutError`, `ApiConnectionError`, `InvalidDataError` |
| `exceptions/storage_error.py` | `StorageError`, `DataImportError`, `DataExportError` |
| `exceptions/config_error.py` | `ConfigError` |

### Modificados

- Ninguno (sin consumidores aún).

## Jerarquía

```
Exception
└── AppError
    ├── MovieNotFoundError        (atributo .titulo)
    ├── SeriesNotFoundError       (atributo .nombre)
    ├── ApiRequestError           (atributo .endpoint)
    │   ├── ApiTimeoutError
    │   └── ApiConnectionError
    ├── InvalidDataError          (datos de API con formato inválido)
    ├── StorageError              (atributo .nombre_archivo)
    │   ├── DataImportError
    │   └── DataExportError
    └── ConfigError               (atributo .clave)
```

## Decisiones aplicadas

- Naming en **English** (consistente con los modelos del Hito 3 y con el nombre del archivo pedido `movie_not_found.py`).
- Cada excepción con un atributo de contexto (`.titulo`, `.nombre`, `.endpoint`, `.nombre_archivo`, `.clave`) opcional y un mensaje por defecto en español.
- Se evita el nombre `ImportError` (colisiona con el built-in de Python) → `DataImportError`.
- Solo stdlib; sin dependencias nuevas (`requests`, `json5`).

## Verificación

1. `py_compile` de los 9 archivos → OK.
2. Las 10 excepciones heredan de `AppError` (y de `Exception`).
3. Jerarquía interna: `ApiTimeoutError`/`ApiConnectionError` ⊂ `ApiRequestError`; `DataImportError`/`DataExportError` ⊂ `StorageError`.
4. Mensajes y atributos: `MovieNotFoundError('Matrix')` → `".titulo" == "Matrix"`, mensaje "No se encontró la película: Matrix". Mismo patrón para series, API, storage y config.
5. Captura vía base: `raise StorageError(...)` interceptable con `except AppError`.
6. `__all__` expone las 10 clases.
7. `import main` → aplicación intacta.

## Estado del proyecto

- Fase 2 completada (Hitos 1–5).
- Fase 3 completada (Hitos 1–3: `api/`+`services/`, `ui/`, `models/`).
- Fase 4, Hito 1 completado — paquete `exceptions/` listo para integrarse en los hitos 2–4 (manejo en servicios, UI y entrada).