---
name: python-pytest-testing
description: Diseña, genera y refactoriza pruebas automáticas en Python utilizando Pytest. Incluye unit testing, integración, fixtures reutilizables, parametrización con @pytest.mark.parametrize, mocking con pytest-mock/unittest.mock, assertions descriptivos y medición de cobertura de código.
---

# Skill: Python Automated Testing with Pytest

## Propósito

Este skill se encarga de crear, estructurar y mantener suites de pruebas unitarias y de integración para proyectos Python utilizando **`pytest`** como framework principal, siguiendo las mejores prácticas de testing para asegurar alta cobertura, mantenibilidad y rapidez en la ejecución.

## Cuándo usar este Skill

Aplica este skill cuando el usuario pida:

* Crear pruebas unitarias o de integración para código o módulos en Python.
* Añadir fixtures o mocks a pruebas existentes.
* Refactorizar tests desorganizados o lentos.
* Configurar parametrización (`@pytest.mark.parametrize`) para validar múltiples casos de borde.
* Evaluar o mejorar la cobertura de código (*code coverage*) con `pytest-cov`.

## Directrices de Implementación

### 1. Estructura y Convenciones del Proyecto

* **Ubicación de Tests:** Coloca los archivos dentro del directorio `tests/`, replicando la estructura de carpetas de la aplicación (ej. `tests/unit/`, `tests/integration/`).
* **Nomenclatura:**
  * Archivos: `test_*.py` o `*_test.py`.
  * Funciones de test: `test_*()`.
  * Clases de test (si aplican): `Test*`.
* **Patrón AAA (Arrange-Act-Assert):** Claramente separado en cada prueba mediante comentarios o saltos de línea legibles.

### 2. Uso de Fixtures y `conftest.py`

* Define recursos, datos de prueba o clientes en **fixtures** reutilizables con `@pytest.fixture`.
* Centraliza las fixtures globales o compartidas entre múltiples módulos dentro de `conftest.py`.
* Asigna el alcance (*scope*) correcto a cada fixture: `function` (por defecto), `module`, `session` para optimizar velocidad.
* Limpia adecuadamente los recursos creados usando `yield` en lugar de `return`.

### 3. Parametriza para Múltiples Escenarios

* Evita duplicar código de prueba para validar distintas combinaciones de entrada/salida.
* Usa `@pytest.mark.parametrize` indicando explícitamente el ID de cada caso para mejorar la legibilidad en el reporte CLI.

### 4. Aislamiento y Mocking Seguro

* Utiliza `unittest.mock` (o `mocker` de `pytest-mock`) para aislar componentes con dependencias externas (bases de datos, APIs, sistema de archivos, tiempo actual).
* Prohibido hacer peticiones a red reales o escrituras destructivas en disco en pruebas unitarias.
* Usa `monkeypatch` para sobrescribir variables de entorno o configuraciones en tiempo de ejecución.

### 5. Validación de Excepciones y Casos de Borde

* Utiliza `with pytest.raises(ExceptionType) as exc_info:` para asegurar que el código falla como se espera ante entradas inválidas.
* Verifica que el mensaje del error devuelto contenga el texto descriptivo esperado (`exc_info.value`).

### 6. Configuración Recomendada (`pyproject.toml`)

Si no existe, sugiere o genera la sección de configuración de `pytest` en el `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --strict-markers --cov=src --cov-report=term-missing"
testpaths = ["tests"]
python_files = ["test_*.py"]
markers = [
    "unit: pruebas unitarias aisladas y rápidas",
    "integration: pruebas de integración con servicios externos",
    "slow: pruebas de ejecución lenta",
]
```

## Flujo de Trabajo Requerido

1. **Identificación de Escenarios:** Determina el "camino feliz" (*happy path*), casos límite (*edge cases*) y condiciones de falla/excepción.
2. **Aislamiento de Dependencias:** Identifica qué servicios o I/O deben ser simulados con Mocks o Fixtures.
3. **Escritura del Test:** Aplica la convención AAA y asertos expresivos.
4. **Validación:** Si el entorno lo permite, ejecuta `pytest` para verificar que las pruebas pasen (`PASSED`).

## Ejemplo de Suite de Pruebas con Pytest

```python
from pathlib import Path
from typing import Generator
import pytest
from unittest.mock import MagicMock, patch

from src.services.user_service import UserService, UserNotFoundError, User


# 1. Fixtures compartidas
@pytest.fixture
def mock_user_repository() -> MagicMock:
    """Proporciona un mock del repositorio de usuarios."""
    repo = MagicMock()
    repo.get_by_id.return_value = User(id=1, name="Alice", is_active=True)
    return repo


@pytest.fixture
def user_service(mock_user_repository: MagicMock) -> UserService:
    """Instancia el servicio inyectando el repositorio simulado."""
    return UserService(repository=mock_user_repository)


# 2. Pruebas Unitarias con AAA
def test_get_user_success(user_service: UserService, mock_user_repository: MagicMock) -> None:
    # Arrange
    user_id = 1

    # Act
    result = user_service.get_user_by_id(user_id)

    # Assert
    assert result.id == user_id
    assert result.name == "Alice"
    mock_user_repository.get_by_id.assert_called_once_with(user_id)


# 3. Prueba de Excepciones
def test_get_user_not_found_raises_error(user_service: UserService, mock_user_repository: MagicMock) -> None:
    # Arrange
    mock_user_repository.get_by_id.return_value = None
    invalid_id = 999

    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.get_user_by_id(invalid_id)

    assert f"Usuario con ID {invalid_id} no encontrado" in str(exc_info.value)


# 4. Pruebas Parametrizadas
@pytest.mark.parametrize(
    "age, expected_category",
    [
        (12, "menor"),
        (18, "adulto"),
        (65, "senior"),
    ],
    ids=["menor_de_edad", "mayoria_de_edad", "tercera_edad"],
)
def test_categorize_user_by_age(user_service: UserService, age: int, expected_category: str) -> None:
    # Act
    category = user_service.categorize_by_age(age)

    # Assert
    assert category == expected_category


# 5. Prueba de Integración / Monkeypatch para Variables de Entorno
def test_service_initialization_with_env(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    # Act
    service = UserService.from_env()

    # Assert
    assert service.db_url == "sqlite:///:memory:"
```