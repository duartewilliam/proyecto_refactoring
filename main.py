import logging
import sys

from api.http_client import CONFIG
from config import setup_logging
from constants import (
    EXIT_OK,
    EXIT_ERROR,
    MSG_PROGRAMA_INTERRUMPIDO,
    MSG_ERROR_INESPERADO,
)
from exceptions import AppError
from ui.menu import menu_principal

logger = logging.getLogger("main")


# Programa principal
if __name__ == "__main__":
    setup_logging(CONFIG["debug"], CONFIG["verbose"])
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(MSG_PROGRAMA_INTERRUMPIDO)
        sys.exit(EXIT_OK)
    except AppError as e:
        logger.exception("Error de aplicación: %s", e)
        print(f"{MSG_ERROR_INESPERADO}{e}")
        sys.exit(EXIT_ERROR)
    except Exception as e:
        logger.exception("Error inesperado: %s", e)
        print(f"{MSG_ERROR_INESPERADO}{e}")
        sys.exit(EXIT_ERROR)