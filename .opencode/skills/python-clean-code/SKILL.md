---
name: python-clean-code
description: Refactoriza y limpia código Python aplicando estándares PEP 8, Type Hints, Pythonic Idioms y eliminación de Code Smells. Usar para mejorar mantenibilidad, legibilidad y calidad general en proyectos Python.
---

# Skill: Python Clean Code & Refactoring

## Propósito
Este skill se encarga de analizar y refactorizar código Python existente para transformarlo en código idiomático (*pythonic*), mantenible, seguro y de alta calidad, alineado estricta y prioritariamente con **PEP 8** y las mejores prácticas del ecosistema moderno de Python.

---

## Cuándo usar este Skill
Aplica este skill cuando el usuario pida:
- Refactorizar, limpiar o mejorar código Python.
- Eliminar malas prácticas (*code smells*) o reducir deuda técnica en módulos Python.
- Aplicar convenciones **PEP 8** y tipado estático (**Type Hints**).
- Hacer que un script o clase sea más "Pythonic".

---

## Directrices de Refactorización

### 1. Adherencia a PEP 8 y Nombres
- **Variables y Funciones:** Utiliza `snake_case`.
- **Clases:** Utiliza `PascalCase`.
- **Constantes:** Utiliza `UPPER_SNAKE_CASE` a nivel de módulo o clase.
- **Módulos y Paquetes:** Nombres cortos en minúsculas sin guiones.
- **Imports:**
  - Estructura los imports en tres bloques separados por una línea en blanco:
    1. Biblioteca estándar de Python.
    2. Librerías de terceros (*third-party*).
    3. Módulos locales de la aplicación.
  - Elimina imports no utilizados (*dead imports*).

### 2. Type Hinting Estricto (Python 3.10+)
- Añade anotaciones de tipos explícitas para todos los parámetros de funciones y métodos, así como para sus valores de retorno.
- Utiliza la sintaxis moderna de tipos nativos:
  - Usa `list[str]` en lugar de `List[str]`.
  - Usa `dict[str, Any]` en lugar de `Dict[str, Any]`.
  - Usa la sintaxis de unión `str | None` en lugar de `Optional[str]`.
- Define dataclasses (`@dataclass`) o Pydantic models para estructuras de datos en lugar de tuplas o diccionarios genéricos complejos.

### 3. Idiomas Pythonicos (Pythonic Code)
- **Administradores de Contexto:** Sustituye la apertura/cierre manual de recursos (archivos, sockets, conexiones DB) por bloques `with`.
- **Comprensiones:** Utiliza *list/set/dict comprehensions* o expresiones generadoras cuando aumente la legibilidad, evitando bucles `for` imperativos innecesarios.
- **Iteración:** Usa `enumerate()` para índices y `zip()` para iterar múltiples colecciones en lugar de accesos por índice (`range(len(...))`).
- **Pathlib:** Prefiere `pathlib.Path` sobre la manipulación manual de strings con `os.path`.
- **F-Strings:** Reemplaza el formateo con `%` o `.format()` por f-strings interpolados.

### 4. Manejo Estructurado de Excepciones
- **Excepciones Específicas:** Prohibido capturar `except Exception:` o usar `except:` desnudos salvo en capas frontera de logging global. Captura siempre la excepción exacta (`ValueError`, `KeyError`, `FileNotFoundError`, etc.).
- **Prohibido el Silenciamiento:** Jamás dejes bloques `except` con un simple `pass` o vacíos. Registra el error o re-eleva la excepción.
- **Efectos Secundarios:** Mantén el bloque `try` lo más pequeño posible para aislar la instrucción propensa a fallar.

### 5. Reducción de Complejidad y Code Smells
- **Guard Clauses y Early Returns:** Elimina la anidación profunda de condicionales `if/else`. Valida las precondiciones al inicio de la función y retorna temprano.
- **Límites de Responsabilidad (SRP):** Descompón funciones largas (>25-30 líneas) o clases con múltiples responsabilidades en funciones/clases pequeñas y puras.
- **Código Muerto:** Elimina variables no utilizadas, parámetros que no se usan y bloques de código comentados.

---

## Flujo de Trabajo Requerido

Cuando ejecutes esta refactorización, debes seguir estos pasos:

1. **Análisis Inicial:** Examina el código objetivo e identifica las malas prácticas especificando qué reglas vulnera.
2. **Preservación de Lógica:** Garantiza que el comportamiento externo y las interfaces públicas de las funciones permanezcan intactas a menos que el usuario indique lo contrario.
3. **Aplicación de Cambios:** Aplica la refactorización siguiendo las directrices anteriores.
4. **Verificación:** Si hay tests configurados (`pytest`), sugiere ejecutar la suite de pruebas tras la modificación para validar la no-regresión.

---

## Ejemplo de Transformación

### ❌ Código Antes (Malas prácticas)
```python
import os, sys
from typing import List, Optional

def PROC_data(FILEPATH, opts=None):
    f = open(FILEPATH, 'r')
    lines = f.readlines()
    f.close()
    
    res = []
    for i in range(len(lines)):
        l = lines[i].strip()
        if len(l) > 0:
            if l.startswith("#") == False:
                try:
                    val = int(l)
                    res.append(val)
                except:
                    pass
    return res
```

### ✅ Código Después (Refactorizado con la Skill)
```python
from pathlib import Path

def process_numeric_data(file_path: str | Path) -> list[int]:
    """Lee un archivo de texto y extrae las líneas numéricas válidas ignorando comentarios.

    Args:
        file_path: Ruta al archivo que se va a procesar.

    Returns:
        Lista de enteros procesados.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"El archivo no existe: {path}")

    processed_values: list[int] = []

    with path.open(mode="r", encoding="utf-8") as file:
        for line in file:
            cleaned_line = line.strip()
            if not cleaned_line or cleaned_line.startswith("#"):
                continue

            try:
                processed_values.append(int(cleaned_line))
            except ValueError:
                # Se descartan las líneas que no son enteros válidos
                continue

    return processed_values
```