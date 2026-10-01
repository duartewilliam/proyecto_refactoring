"""Tests unitarios de config.py con aislamiento del config.json/.env reales."""
import json
import logging
import os

import config


# ---------------------------------------------------------------
# Carga y persistencia
# ---------------------------------------------------------------
def test_load_config_crea_desde_defaults_si_no_existe(tmp_path, monkeypatch):
    archivo = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_FILE", str(archivo))

    config.load_config()

    assert archivo.exists()
    assert config.get("app_name") == "Mi App de Películas"


def test_load_config_carga_json_existente(tmp_path, monkeypatch):
    archivo = tmp_path / "config.json"
    archivo.write_text(json.dumps({"app_name": "Personalizado", "timeout": 5}))
    monkeypatch.setattr(config, "CONFIG_FILE", str(archivo))

    config.load_config()

    assert config.get("app_name") == "Personalizado"
    assert config.get("timeout") == 5


def test_secretos_priorizan_env_sobre_archivo(tmp_path, monkeypatch):
    archivo = tmp_path / "config.json"
    archivo.write_text(json.dumps({"omdb_api_key": "DEL_ARCHIVO"}))
    monkeypatch.setattr(config, "CONFIG_FILE", str(archivo))
    monkeypatch.setenv("OMDB_API_KEY", "DEL_ENTORNO")

    config.load_config()

    assert config.get("omdb_api_key") == "DEL_ENTORNO"


def test_get_y_get_all(monkeypatch):
    monkeypatch.setattr(config, "_config", {"a": 1, "b": 2})

    assert config.get("a") == 1
    assert config.get("zzz", "por_defecto") == "por_defecto"
    assert config.get_all() == {"a": 1, "b": 2}


def test_set_actualiza_y_persiste(tmp_path, monkeypatch):
    archivo = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_FILE", str(archivo))
    config._config = {"timeout": 1}

    config.set("timeout", 30)

    assert config.get("timeout") == 30
    assert json.loads(archivo.read_text())["timeout"] == 30


def test_reset_restaura_defaults(tmp_path, monkeypatch):
    archivo = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_FILE", str(archivo))
    config._config = {"timeout": 1}

    config.reset()

    assert config._config == config.DEFAULT_CONFIG
    assert config.get("app_name") == "Mi App de Películas"


def test_export_config_escribe_archivo(tmp_path, monkeypatch):
    externo = tmp_path / "externo.json"
    monkeypatch.setattr(config, "CONFIG_FILE", str(tmp_path / "config.json"))
    config._config = {"app_name": "Exportado"}

    config.export_config(str(externo))

    assert json.loads(externo.read_text())["app_name"] == "Exportado"


def test_import_config_desde_archivo(tmp_path, monkeypatch):
    externo = tmp_path / "externo.json"
    externo.write_text(json.dumps({"app_name": "Importado"}))
    monkeypatch.setattr(config, "CONFIG_FILE", str(tmp_path / "config.json"))
    config._config = {}

    config.import_config(str(externo))

    assert config.get("app_name") == "Importado"
    assert (tmp_path / "config.json").exists()


def test_import_config_sin_archivo_no_cambia_estado(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_FILE", str(tmp_path / "config.json"))
    config._config = {"app_name": "Actual"}

    config.import_config(str(tmp_path / "no_existe.json"))

    assert config.get("app_name") == "Actual"


# ---------------------------------------------------------------
# validación
# ---------------------------------------------------------------
def test_validate_config_valida(monkeypatch):
    monkeypatch.setattr(
        config, "_config", {"omdb_api_key": "x", "timeout": 10, "max_retries": 3}
    )
    assert config.validate_config() == []


def test_validate_config_falta_claves(monkeypatch):
    monkeypatch.setattr(config, "_config", {})
    errores = config.validate_config()
    assert len(errores) == 3
    assert all("Falta clave requerida" in e for e in errores)


def test_validate_config_timeout_no_numerico_y_cero(monkeypatch):
    monkeypatch.setattr(config, "_config", {"omdb_api_key": "x", "timeout": 0, "max_retries": 3})
    errores = config.validate_config()
    assert "timeout debe ser mayor a 0" in errores

    monkeypatch.setattr(config, "_config", {"omdb_api_key": "x", "timeout": "treinta", "max_retries": 3})
    errores = config.validate_config()
    assert "timeout debe ser numérico" in errores


def test_validate_config_max_retries_no_entero(monkeypatch):
    monkeypatch.setattr(config, "_config", {"omdb_api_key": "x", "timeout": 10, "max_retries": "tres"})
    errores = config.validate_config()
    assert "max_retries debe ser entero" in errores


# ---------------------------------------------------------------
# Secretos y logging
# ---------------------------------------------------------------
def test_print_config_enmascara_secretos(caplog, monkeypatch):
    monkeypatch.setattr(config, "_config", {"sender_password": "secreto123", "debug": True})

    with caplog.at_level(logging.INFO, logger="config"):
        config.print_config()

    texto = caplog.text
    assert "***" in texto
    assert "secreto123" not in texto


def test_cargar_dotenv_lee_lineas_validas(tmp_path, monkeypatch):
    dotenv = tmp_path / ".env"
    dotenv.write_text("# comentario\n\nOMDB_API_KEY=123\nSENDER_EMAIL=  a@b.c  \n")
    monkeypatch.delenv("OMDB_API_KEY", raising=False)
    monkeypatch.delenv("SENDER_EMAIL", raising=False)

    config._cargar_dotenv(str(dotenv))

    assert os.environ["OMDB_API_KEY"] == "123"
    assert os.environ["SENDER_EMAIL"] == "a@b.c"


def test_cargar_dotenv_no_sobrescribe_existentes(tmp_path, monkeypatch):
    dotenv = tmp_path / ".env"
    dotenv.write_text("OMDB_API_KEY=123\n")
    monkeypatch.setenv("OMDB_API_KEY", "previa")

    config._cargar_dotenv(str(dotenv))

    assert os.environ["OMDB_API_KEY"] == "previa"


def test_cargar_dotenv_sin_archivo_no_falla(tmp_path):
    config._cargar_dotenv(str(tmp_path / "no_existe.env"))


def test_setup_logging_niveles():
    config.setup_logging(debug=True, verbose=False)
    assert logging.getLogger().level == logging.DEBUG

    config.setup_logging(debug=False, verbose=True)
    assert logging.getLogger().level == logging.INFO

    config.setup_logging(debug=False, verbose=False)
    assert logging.getLogger().level == logging.WARNING