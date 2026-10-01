---
name: python-api-integration
description: Conecta a APIs REST en Python de forma robusta utilizando httpx/requests, Pydantic, manejo estricto de timeouts, retries con backoff exponencial, rate limiting y excepciones de dominio. Usar para construir clientes HTTP resilientes.
---

# API Integration - Conectar a APIs REST Robustamente

Skill para OpenCode enfocada en el diseño, implementación y refactorización de clientes e integraciones con **APIs REST en Python**, asegurando resiliencia, tolerancia a fallos, validación estricta de esquemas y rendimiento óptimo.

## Scope & Objetivos

Esta skill guía la construcción de clientes e integraciones de servicios web asegurando:
- **Resiliencia y Tolerancia a Fallos:** Implementación de retries con backoff exponencial y timeouts obligatorios.
- **Validación Estricta de Datos:** Tipado y serialización limpia utilizando `Pydantic`.
- **Rendimiento:** Uso de clientes asíncronos (`httpx`) o síncronos con pools de conexiones reutilizables.
- **Seguridad:** Manejo seguro de credenciales mediante variables de entorno o gestores de secretos.

---

## Directrices Principales para Integración de APIs

### 1. Manejo de Peticiones y Clientes HTTP
- **Timeouts Obligatorios:** Prohibido realizar peticiones sin definir timeouts explícitos (ej. `timeout=httpx.Timeout(10.0, connect=5.0)`).
- **Reutilización de Sesiones:** Usar clientes persistentes (`httpx.Client()`, `httpx.AsyncClient()` o `requests.Session()`) en lugar de funciones de nivel de módulo (`requests.get()`) para aprovechar el connection pooling.
- **Soporte Asíncrono:** Priorizar `httpx` o `aiohttp` para operaciones I/O intensivas o llamadas concurrentes.

### 2. Resiliencia, Retries y Rate Limiting
- **Estrategia de Reintentos (Backoff Exponencial):** Usar librerías maduras como `tenacity` o los adaptadores de `urllib3` para reintentar únicamente ante fallos transitorios (HTTP 502, 503, 504 o errores de red), **nunca** ante errores 4xx (salvo 429 Too Many Requests).
- **Manejo de Rate Limits (429):** Respetar cabeceras como `Retry-After` antes de reintentar una petición.

### 3. Validaciones con Pydantic
- **Parsing de Respuestas:** Mapear los JSON de respuesta a modelos `pydantic.BaseModel` con `model_validate()`.
- **Manejo de Campos Opcionales/Nulos:** Usar `Optional`, valores por defecto o alias (`Field(alias=...)`) cuando la API externa use convenciones `camelCase`.

### 4. Manejo de Errores y Excepciones Custom
- **Excepciones de Dominio:** Encapsular errores HTTP en excepciones personalizadas de la aplicación (`APIConnectionError`, `APIAuthenticationError`, `ResourceNotFoundError`).
- **Uso de `raise_for_status()`:** Validar respuestas HTTP exitosas antes de procesar el cuerpo JSON.

---

## Ejemplo de Implementación Robusta en Python

```python
import logging
from typing import Optional
import httpx
from pydantic import BaseModel, Field, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class UserDTO(BaseModel):
    user_id: int = Field(alias="id")
    email: str
    is_active: bool = Field(default=True, alias="isActive")

class APIIntegrationError(Exception):
    """Excepción base para fallos de integración."""

class ExternalAPIClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
            timeout=httpx.Timeout(timeout),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException)),
        reraise=True,
    )
    def _execute_request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self._client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error HTTP {exc.response.status_code} llamando a {url}: {exc.response.text}")
            raise APIIntegrationError(f"Fallo en API externa ({exc.response.status_code})") from exc
        except (httpx.NetworkError, httpx.TimeoutException) as exc:
            logger.warning(f"Error de red o timeout al conectar con {url}: {exc}")
            raise

    def get_user(self, user_id: int) -> Optional[UserDTO]:
        data = self._execute_request("GET", f"/users/{user_id}")
        try:
            return UserDTO.model_validate(data)
        except ValidationError as exc:
            logger.error(f"Estructura JSON inválida para UserDTO: {exc}")
            raise APIIntegrationError("La respuesta de la API no coincide con el esquema esperado") from exc

    def close(self):
        self._client.close()
* Implementa esquemas de autenticación limpios (ej. custom `httpx.Auth` o clases de sesión dedicadas para refresco de tokens OAuth2).

### 5. Validación y Deserialización de Respuestas

* Convierte las respuestas JSON en objetos fuertemente tipados utilizando **Pydantic** (`pydantic.BaseModel`) o `@dataclass`.

* Valida la estructura del JSON recibido antes de consumirlo para evitar excepciones inesperadas por `KeyError` o datos incompletos.

* Maneja explícitamente errores de deserialización (`pydantic.ValidationError` / `json.JSONDecodeError`).

### 6. Manejo Riguroso de Excepciones HTTP

* Captura y envuelve las excepciones nativas del cliente HTTP (`httpx.HTTPError`, `requests.RequestException`) en excepciones de dominio personalizadas del proyecto (ej. `APIConnectionError`, `APIResponseError`, `RateLimitExceededError`).

* Utiliza siempre `raise_for_status()` de forma controlada o captura los códigos de estado no exitosos antes de procesar la respuesta.

## Flujo de Trabajo Requerido

Al crear o refactorizar una integración de API REST:

1. **Definición del Cliente:** Crea una clase wrapper dedicada (ej. `GitHubApiClient`, `PaymentGatewayClient`).
2. **Esquema de Datos:** Define los modelos Pydantic para los payloads de entrada y respuesta.
3. **Manejo de Errores:** Define excepciones personalizadas heredadas de una excepción base del cliente.
4. **Resiliencia:** Configura timeouts, reintentos y sesiones reutilizables.

## Ejemplo de Estructura de Integración

### ✅ Cliente API REST de Producción en Python

```python
import os
import logging
from typing import Any
import httpx
from pydantic import BaseModel, Field, ValidationError
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

# 1. Excepciones de Dominio
class APIClientError(Exception):
    """Excepción base para fallos en la API."""

class APIConnectionError(APIClientError):
    """Error de conexión o timeout."""

class APIValidationError(APIClientError):
    """Fallo de validación en la estructura del JSON."""


# 2. Modelos Pydantic
class UserResponse(BaseModel):
    user_id: int = Field(alias="id")
    username: str
    email: str


# 3. Cliente API
class UserApiClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = base_url or os.getenv("API_BASE_URL", "https://api.example.com")
        self.api_key = api_key or os.getenv("API_KEY")
        
        if not self.api_key:
            raise ValueError("API_KEY no configurada en las variables de entorno.")

        # Configuración de timeouts y headers por defecto
        self._session = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            },
            timeout=httpx.Timeout(connect=5.0, read=15.0),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(min=1, max=10),
        retry=retry_if_exception_type(APIConnectionError),
        reraise=True,
    )
    def get_user(self, user_id: int) -> UserResponse:
        """Obtiene y valida la información de un usuario desde la API REST."""
        try:
            response = self._session.get(f"/v1/users/{user_id}")
            response.raise_for_status()
            
            return UserResponse.model_validate(response.json())

        except httpx.TimeoutException as exc:
            logger.error("Timeout conectando a la API para el usuario %s", user_id)
            raise APIConnectionError("Tiempo de espera agotado al conectar con el servidor.") from exc

        except httpx.HTTPStatusError as exc:
            logger.error("Error HTTP %s recibido de la API: %s", exc.response.status_code, exc.response.text)
            raise APIClientError(f"Error en la API con código {exc.response.status_code}") from exc

        except (ValidationError, ValueError) as exc:
            logger.error("Error al parsear la respuesta JSON para el usuario %s", user_id)
            raise APIValidationError("La respuesta de la API no coincide con el esquema esperado.") from exc

    def close(self) -> None:
        """Cierra la sesión HTTP subyacente."""
        self._session.close()

    def __enter__(self) -> "UserApiClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
```
