# Resumen Fase 5 — Hito 3: Agregar validación de entrada

## Objetivo

Validar las entradas de usuario en la capa UI antes de pasarlas a servicios/API o
al sistema de archivos, evitando campos vacíos, búsquedas absurdamente largas,
path traversal y crashes por entrada no numérica (p. ej. `int(input())`).

## Cambios realizados

### `ui/validation.py` (nuevo)
Validadores puros y testables:
- `LIMITE_LONGITUD_BUSQUEDA=120`, `LIMITE_LONGITUD_NOMBRE=100`,
  `TIMEOUT_MINIMO=1`, `TIMEOUT_MAXIMO=300`, `GENEROS_VALIDOS=("accion","comedia")`.
- `validar_texto_busqueda(texto)` → limpia con `strip()`; `None` si vacío o > 120.
- `validar_genero(genero)` → normaliza a minúsculas; `None` si no es "accion"/"comedia".
- `validar_nombre_archivo(nombre)` → limpia; `None` si vacío, `"."`/`".."`, largo,
  o contiene `/` o `\` (bloquea path traversal).
- `validar_entero(texto, minimo, maximo)` → `int` en rango o `None`.
- `indice_seleccion(opcion, tamano)` → opción numérica 1-based a índice 0-based
  dentro del rango, o `None` (reemplaza el patrón `isdigit()` + rango duplicado).

### `constants.py`
Nuevos mensajes: `MSG_BUSQUEDA_INVALIDA`, `MSG_GENERO_INVALIDO`,
`MSG_SELECCION_INVALIDA`, `MSG_NOMBRE_ARCHIVO_INVALIDO`, `MSG_TIMEOUT_INVALIDO`.

### `ui/menu.py`
Integración de validadores en cada entrada:
- Búsquedas (título, actor, serie): texto vacío o > 120 → mensaje y salida
  (sin llamar a la API).
- Género: solo "accion"/"comedia" (antes cualquier entrada devolvía listas).
- Selecciones en listas (actor, series, favoritos): `indice_seleccion()`; `Enter`/`0`
  siguen volviendo; entrada basura muestra `MSG_SELECCION_INVALIDA`.
- Exportar/importar: nombre de archivo validado (sin vacíos ni directorios);
  `../evil` se rechaza.
- Configuración: timeout con `validar_entero(1..300)` — antes un `int(input())`
  crasheaba con `ValueError`; opción de configuración inválida muestra mensaje.

## Verificación

1. `py_compile` de `ui/validation.py`, `ui/menu.py`, `constants.py` → OK.
2. Unit (validadores): vacío/espacios/longitud del texto, `Acción` inválido,
   `COMEDIA`→`comedia`, `../evil`, `dir\nombre`, `..`, `.`, 101 chars, enteros
   fuera de rango/`abc`, índices 0/6/`abc` → todos rechazados o normalizados.
3. Integración en menú (mocks): búsqueda vacía y larga → mensaje sin llamada a
   API; género `horror` → mensaje sin `buscar_peliculas_por_genero`; exportar
   `../evil` → mensaje sin `exportar_a_json`; selección basura → mensaje; timeout
   `abc` y `0` → mensaje y `CONFIG["timeout"]` intacto; timeout `42` → aplicado.
4. Extremo a extremo (`main.py`): opción 12 exit 0; exportar e2e "Exportado a
   respaldo.json" exit 0; opción 11→3 con `abc` → "Timeout inválido" exit 0;
   opción 5 con `Acción` → "Género inválido" exit 0.

## Estado del proyecto

- Fases 1–4 completadas.
- Fase 5 completada (Hitos 1-3): secretos a variables de entorno, eliminación de
  datos hardcodeados sensibles y validación de entrada.
- Validación aplicada en el límite de entrada (UI); la lógica de servicios no
  cambió (sigue sin revalidar, por diseño, preservando comportamiento).
- Pendiente anotado: `user_manager.py` (código muerto) guarda contraseñas en
  texto plano — candidato para un futuro hito de hashing.