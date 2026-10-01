"""
Módulo centralizado de configuración del proyecto "Películas y Series".

Consolida la configuración de los 88 archivos *_config.py eliminados
en la Fase 2, Hito 1.

Uso:
    from config import get, set, load_config, save_config
    api_key = get("omdb_api_key")
    set("debug", False)
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Ruta del archivo de configuración
CONFIG_FILE = "config.json"

# Ruta del archivo de variables de entorno local
ENV_FILE = ".env"

# ============================================
# Claves sensibles y su variable de entorno
# ============================================
SECRET_ENV: dict[str, str] = {
    "omdb_api_key": "OMDB_API_KEY",
    "tmdb_api_key": "TMDB_API_KEY",
    "sender_email": "SENDER_EMAIL",
    "sender_password": "SENDER_PASSWORD",
    "proxy_username": "PROXY_USERNAME",
    "proxy_password": "PROXY_PASSWORD",
}

MASCARA_SECRETO = "***"

# ============================================
# Valores por defecto (consolidados)
# ============================================
DEFAULT_CONFIG: dict = {
    # --- App ---
    "app_name": "Mi App de Películas",
    "version": "1.0.0",
    "author": "Estudiante",
    "debug": True,
    "verbose": True,

    # --- APIs ---
    "omdb_api_key": os.getenv("OMDB_API_KEY", ""),
    "omdb_base_url": os.getenv("OMDB_BASE_URL", "http://www.omdbapi.com/"),
    "tvmaze_base_url": os.getenv("TVMAZE_BASE_URL", "http://api.tvmaze.com"),
    "tmdb_base_url": os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3/"),
    "tmdb_api_key": os.getenv("TMDB_API_KEY", ""),

    # --- Red ---
    "timeout": int(os.getenv("API_TIMEOUT", "30")),
    "max_retries": int(os.getenv("MAX_RETRIES", "3")),
    "retry_delay": int(os.getenv("RETRY_DELAY", "1")),
    "verify_ssl": os.getenv("VERIFY_SSL", "true").lower() == "true",
    "user_agent": os.getenv("USER_AGENT", "MovieExplorer/1.0"),
    "connection_pool_size": int(os.getenv("CONNECTION_POOL_SIZE", "10")),

    # --- Cache ---
    "cache_enabled": os.getenv("CACHE_ENABLED", "true").lower() == "true",
    "cache_expiry_hours": int(os.getenv("CACHE_EXPIRY_HOURS", "24")),
    "cache_max_size_mb": int(os.getenv("CACHE_MAX_SIZE_MB", "100")),
    "cache_responses": True,
    "enable_api_cache": True,
    "api_cache_size_mb": 50,
    "api_cache_expiry_hours": 12,

    # --- Logging ---
    "log_level": os.getenv("LOG_LEVEL", "DEBUG"),
    "log_file": os.getenv("LOG_FILE", "app.log"),

    # --- Datos ---
    "data_dir": os.getenv("DATA_DIR", "data"),
    "backup_dir": os.getenv("BACKUP_DIR", "backups"),
    "max_results": int(os.getenv("MAX_RESULTS", "10")),

    # --- Email (sensible) ---
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "use_tls": os.getenv("USE_TLS", "true").lower() == "true",
    "sender_email": os.getenv("SENDER_EMAIL", ""),
    "sender_password": os.getenv("SENDER_PASSWORD", ""),

    # --- Proxy ---
    "proxy_enabled": os.getenv("PROXY_ENABLED", "false").lower() == "true",
    "proxy_server": os.getenv("PROXY_SERVER", ""),
    "proxy_port": int(os.getenv("PROXY_PORT", "0")),
    "proxy_username": os.getenv("PROXY_USERNAME", ""),
    "proxy_password": os.getenv("PROXY_PASSWORD", ""),

    # --- Seguridad ---
    "privacy_analytics_enabled": False,
    "privacy_crash_reporting": False,

    # --- UI ---
    "theme_primary_color": "#4dabf7",
    "theme_secondary_color": "#69db7c",
    "theme_background_color": "#1a1b1e",
    "theme_text_color": "#ffffff",
    "language_available": ["es", "en", "pt"],
    "language_fallback": "en",

    # --- Mantenimiento ---
    "maintenance_mode": False,
    "maintenance_message": "Sistema en mantenimiento",
    "maintenance_contact": "admin@example.com",
}

# ============================================
# Singleton de configuración
# ============================================
_config: dict = {}


def _cargar_dotenv(ruta: str = ENV_FILE) -> None:
    """Carga variables desde un archivo .env a os.environ sin reemplazar las ya definidas."""
    if not os.path.exists(ruta):
        return
    with open(ruta, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, _, valor = linea.partition("=")
            clave = clave.strip()
            valor = valor.strip().strip('"').strip("'")
            if clave:
                os.environ.setdefault(clave, valor)


def _resolver_secretos() -> None:
    """Da prioridad a las variables de entorno sobre los valores del archivo JSON."""
    for clave, variable in SECRET_ENV.items():
        _config[clave] = os.environ.get(variable, _config.get(clave, ""))


def load_config() -> dict:
    """Carga configuración desde archivo JSON o crea desde defaults."""
    global _config
    _cargar_dotenv()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            _config = json.load(f)
    else:
        _config = DEFAULT_CONFIG.copy()
        save_config()
    _resolver_secretos()
    return _config


def save_config() -> None:
    """Guarda configuración actual a archivo JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(_config, f, indent=4)


def get(key: str, default=None):
    """Obtiene un valor de configuración por clave."""
    return _config.get(key, default)


def set(key: str, value) -> None:
    """Establece un valor de configuración y persiste."""
    _config[key] = value
    save_config()


def reset() -> None:
    """Resetea configuración a valores por defecto."""
    global _config
    _config = DEFAULT_CONFIG.copy()
    save_config()


def get_all() -> dict:
    """Retorna copia de toda la configuración."""
    return _config.copy()


def export_config(filename: str) -> None:
    """Exporta configuración a un archivo JSON externo."""
    with open(filename, "w") as f:
        json.dump(_config, f, indent=4)


def import_config(filename: str) -> None:
    """Importa configuración desde un archivo JSON externo."""
    global _config
    if os.path.exists(filename):
        with open(filename, "r") as f:
            _config = json.load(f)
        save_config()


def print_config() -> None:
    """Registra la configuración actual en el log (secretos enmascarados)."""
    for key, value in sorted(_config.items()):
        if key in SECRET_ENV:
            value = MASCARA_SECRETO
        logger.info("%s: %s", key, value)


def validate_config() -> list[str]:
    """Valida la configuración y retorna lista de errores."""
    errors = []

    required_keys = ["omdb_api_key", "timeout", "max_retries"]
    for key in required_keys:
        if key not in _config:
            errors.append(f"Falta clave requerida: {key}")

    if "timeout" in _config:
        if not isinstance(_config["timeout"], (int, float)):
            errors.append("timeout debe ser numérico")
        elif _config["timeout"] <= 0:
            errors.append("timeout debe ser mayor a 0")

    if "max_retries" in _config:
        if not isinstance(_config["max_retries"], int):
            errors.append("max_retries debe ser entero")

    return errors


def setup_logging(debug: bool = False, verbose: bool = False) -> None:
    """Configura el logger raíz a consola con nivel según flags de depuración."""
    nivel = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(nivel)


# ============================================
# Auto-load al importar el módulo
# ============================================
load_config()
