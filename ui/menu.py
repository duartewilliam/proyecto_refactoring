"""Lógica de menú: flujo de opciones, entrada de usuario y dispatch."""
import json
import logging
import time
from api.http_client import CONFIG
from config import setup_logging
from constants import (
    EXTENSION_JSON,
    SISTEMA_TITULO,
    CONFIRMAR_SI,
    PREFIJO_NUMERACION,
    ABRIR_PARENTESIS,
    CERRAR_PARENTESIS,
    MSG_PRESIONAR_ENTER,
    MSG_GENEROS_DISPONIBLES,
    PROMPT_TITULO,
    PROMPT_ACTOR,
    PROMPT_SERIE,
    PROMPT_GENERO,
    MSG_BUSCANDO,
    MSG_BUSCANDO_ACTOR,
    MSG_BUSCANDO_SERIES,
    MSG_BUSQUEDA_INVALIDA,
    MSG_GENERO_INVALIDO,
    MSG_NO_ENCONTRADAS_ACTOR,
    MSG_NO_ENCONTRADAS_SERIES,
    PROMPT_AGREGAR_FAVORITOS,
    MSG_AGREGADA_FAVORITOS,
    MSG_YA_EN_FAVORITOS,
    PROMPT_ELIMINAR_FAVORITA,
    MSG_ELIMINADA_FAVORITOS,
    MSG_SIN_FAVORITAS,
    PROMPT_LIMPIAR_HISTORIAL,
    MSG_HISTORIAL_LIMPIADO,
    MSG_SIN_HISTORIAL,
    PROMPT_SELECCION_PELICULA,
    PROMPT_SELECCION_SERIE,
    MSG_SELECCION_INVALIDA,
    LABEL_TOTAL_FAVORITAS,
    LABEL_TOTAL_HISTORIAL,
    PROMPT_NOMBRE_ARCHIVO,
    MSG_ERROR_IMPORTAR,
    MSG_NOMBRE_ARCHIVO_INVALIDO,
    LABEL_DEBUG_CONFIG,
    LABEL_VERBOSE_CONFIG,
    LABEL_TIMEOUT_CONFIG,
    PROMPT_OPCION_CONFIG,
    MSG_DEBUG_ACTUAL,
    MSG_VERBOSE_ACTUAL,
    PROMPT_NUEVO_TIMEOUT,
    MSG_TIMEOUT_INVALIDO,
    HEADER_PELICULAS_POPULARES,
    HEADER_MIS_FAVORITOS,
    HEADER_HISTORIAL,
    HEADER_ESTADISTICAS,
    HEADER_CONFIGURACION,
    OPCION_MENU_1,
    OPCION_MENU_2,
    OPCION_MENU_3,
    OPCION_MENU_4,
    OPCION_MENU_5,
    OPCION_MENU_6,
    OPCION_MENU_7,
    OPCION_MENU_8,
    OPCION_MENU_9,
    OPCION_MENU_10,
    OPCION_MENU_11,
    OPCION_MENU_12,
    PROMPT_SELECCION_OPCION,
    MSG_HASTA_LUEGO,
    MSG_OPCION_INVALIDA,
)
from services.movie_service import (
    HISTORIAL_BUSQUEDAS,
    PELICULAS_FAVORITAS,
    agregar_a_favoritas,
    agregar_al_historial,
    buscar_pelicula,
    buscar_peliculas_por_actor,
    buscar_peliculas_por_genero,
    eliminar_de_favoritas,
    exportar_a_json,
    importar_de_json,
    limpiar_historial,
    obtener_estadisticas,
    obtener_peliculas_populares,
)
from services.series_service import (
    buscar_series,
    obtener_detalles_serie,
)
from ui.display import (
    clear_screen,
    print_header,
    mostrar_pelicula,
    mostrar_serie,
    mostrar_lista_peliculas,
)
from ui.validation import (
    TIMEOUT_MAXIMO,
    TIMEOUT_MINIMO,
    indice_seleccion,
    validar_entero,
    validar_genero,
    validar_nombre_archivo,
    validar_texto_busqueda,
)

logger = logging.getLogger(__name__)


def delay(seconds: float) -> None:
    """Delay innecesario"""
    time.sleep(seconds)


def funcion_buscar_pelicula() -> None:
    """Busca película"""
    titulo = validar_texto_busqueda(input(PROMPT_TITULO))
    if titulo is None:
        print(MSG_BUSQUEDA_INVALIDA)
        input(MSG_PRESIONAR_ENTER)
        return

    print(MSG_BUSCANDO)
    delay(1)  # Simular carga innecesaria

    pelicula = buscar_pelicula(titulo)
    mostrar_pelicula(pelicula)

    if pelicula is not None:
        agregar_al_historial(pelicula)
        opcion = input(PROMPT_AGREGAR_FAVORITOS)
        if opcion.lower() == CONFIRMAR_SI:
            if agregar_a_favoritas(pelicula):
                print(MSG_AGREGADA_FAVORITOS)
            else:
                print(MSG_YA_EN_FAVORITOS)

    input(MSG_PRESIONAR_ENTER)


def funcion_buscar_actor() -> None:
    """Busca actor"""
    actor = validar_texto_busqueda(input(PROMPT_ACTOR))
    if actor is None:
        print(MSG_BUSQUEDA_INVALIDA)
        input(MSG_PRESIONAR_ENTER)
        return

    print(MSG_BUSCANDO_ACTOR)

    peliculas = buscar_peliculas_por_actor(actor)

    if len(peliculas) > 0:
        mostrar_lista_peliculas(peliculas)

        opcion = input(PROMPT_SELECCION_PELICULA)
        indice = indice_seleccion(opcion, len(peliculas))
        if indice is not None:
            detalles = buscar_pelicula(peliculas[indice]["Title"])
            mostrar_pelicula(detalles)
        elif opcion.strip() not in ("", "0"):
            print(MSG_SELECCION_INVALIDA)
    else:
        print(MSG_NO_ENCONTRADAS_ACTOR)

    input(MSG_PRESIONAR_ENTER)


def funcion_buscar_series() -> None:
    """Busca series"""
    nombre = validar_texto_busqueda(input(PROMPT_SERIE))
    if nombre is None:
        print(MSG_BUSQUEDA_INVALIDA)
        input(MSG_PRESIONAR_ENTER)
        return

    print(MSG_BUSCANDO_SERIES)

    series = buscar_series(nombre)

    if len(series) > 0:
        i = 0
        while i < len(series):
            show = series[i].get("show", {})
            print(f"{i + 1}{PREFIJO_NUMERACION}{show.get('name', '')}{ABRIR_PARENTESIS}{show.get('status', '')}{CERRAR_PARENTESIS}")
            i += 1

        opcion = input(PROMPT_SELECCION_SERIE)
        indice = indice_seleccion(opcion, len(series))
        if indice is not None:
            id_serie = series[indice].get("show", {}).get("id")
            detalles = obtener_detalles_serie(id_serie)
            mostrar_serie(detalles)
        elif opcion.strip() not in ("", "0"):
            print(MSG_SELECCION_INVALIDA)
    else:
        print(MSG_NO_ENCONTRADAS_SERIES)

    input(MSG_PRESIONAR_ENTER)


def funcion_peliculas_populares() -> None:
    """Muestra películas populares"""
    print_header(HEADER_PELICULAS_POPULARES)
    peliculas = obtener_peliculas_populares()
    mostrar_lista_peliculas(peliculas)
    input(MSG_PRESIONAR_ENTER)


def funcion_buscar_por_genero() -> None:
    """Busca por género"""
    print(MSG_GENEROS_DISPONIBLES)
    genero = validar_genero(input(PROMPT_GENERO))
    if genero is None:
        print(MSG_GENERO_INVALIDO)
        input(MSG_PRESIONAR_ENTER)
        return

    print(MSG_BUSCANDO)

    peliculas = buscar_peliculas_por_genero(genero)
    mostrar_lista_peliculas(peliculas)

    input(MSG_PRESIONAR_ENTER)


def funcion_ver_favoritos() -> None:
    """Muestra favoritas"""
    print_header(HEADER_MIS_FAVORITOS)
    if len(PELICULAS_FAVORITAS) > 0:
        i = 0
        while i < len(PELICULAS_FAVORITAS):
            print(f"{i + 1}{PREFIJO_NUMERACION}{PELICULAS_FAVORITAS[i].get('Title', '')}")
            i += 1

        opcion = input(PROMPT_ELIMINAR_FAVORITA)
        indice = indice_seleccion(opcion, len(PELICULAS_FAVORITAS))
        if indice is not None:
            titulo = PELICULAS_FAVORITAS[indice].get("Title")
            if eliminar_de_favoritas(titulo):
                print(MSG_ELIMINADA_FAVORITOS)
        elif opcion.strip() not in ("", "0"):
            print(MSG_SELECCION_INVALIDA)
    else:
        print(MSG_SIN_FAVORITAS)

    input(MSG_PRESIONAR_ENTER)


def funcion_ver_historial() -> None:
    """Muestra historial"""
    print_header(HEADER_HISTORIAL)
    if len(HISTORIAL_BUSQUEDAS) > 0:
        i = 0
        while i < len(HISTORIAL_BUSQUEDAS):
            print(f"{i + 1}{PREFIJO_NUMERACION}{HISTORIAL_BUSQUEDAS[i]['titulo']}")
            i += 1

        opcion = input(PROMPT_LIMPIAR_HISTORIAL)
        if opcion.lower() == CONFIRMAR_SI:
            limpiar_historial()
            print(MSG_HISTORIAL_LIMPIADO)
    else:
        print(MSG_SIN_HISTORIAL)

    input(MSG_PRESIONAR_ENTER)


def funcion_estadisticas() -> None:
    """Muestra estadísticas"""
    print_header(HEADER_ESTADISTICAS)
    stats = obtener_estadisticas()
    print(f"{LABEL_TOTAL_FAVORITAS}{stats['total_favoritas']}")
    print(f"{LABEL_TOTAL_HISTORIAL}{stats['total_historial']}")
    input(MSG_PRESIONAR_ENTER)


def funcion_exportar() -> None:
    """Exporta datos"""
    nombre = validar_nombre_archivo(input(PROMPT_NOMBRE_ARCHIVO))
    if nombre is None:
        print(MSG_NOMBRE_ARCHIVO_INVALIDO)
        input(MSG_PRESIONAR_ENTER)
        return

    exportar_a_json(f"{nombre}{EXTENSION_JSON}")
    print(f"Exportado a {nombre}{EXTENSION_JSON}")
    input(MSG_PRESIONAR_ENTER)


def funcion_importar() -> None:
    """Importa datos"""
    nombre = validar_nombre_archivo(input(PROMPT_NOMBRE_ARCHIVO))
    if nombre is None:
        print(MSG_NOMBRE_ARCHIVO_INVALIDO)
        input(MSG_PRESIONAR_ENTER)
        return

    try:
        importar_de_json(f"{nombre}{EXTENSION_JSON}")
        print(f"Importado desde {nombre}{EXTENSION_JSON}")
    except (FileNotFoundError, PermissionError, json.JSONDecodeError):
        logger.exception("Error al importar %s", nombre)
        print(MSG_ERROR_IMPORTAR)
    input(MSG_PRESIONAR_ENTER)


def funcion_configuracion() -> None:
    """Configuración"""
    print_header(HEADER_CONFIGURACION)
    print(f"{LABEL_DEBUG_CONFIG}{CONFIG['debug']}")
    print(f"{LABEL_VERBOSE_CONFIG}{CONFIG['verbose']}")
    print(f"{LABEL_TIMEOUT_CONFIG}{CONFIG['timeout']}")

    opcion = input(PROMPT_OPCION_CONFIG)
    if opcion == "1":
        CONFIG["debug"] = not CONFIG["debug"]
        setup_logging(CONFIG["debug"], CONFIG["verbose"])
        print(f"{MSG_DEBUG_ACTUAL}{CONFIG['debug']}")
    elif opcion == "2":
        CONFIG["verbose"] = not CONFIG["verbose"]
        setup_logging(CONFIG["debug"], CONFIG["verbose"])
        print(f"{MSG_VERBOSE_ACTUAL}{CONFIG['verbose']}")
    elif opcion == "3":
        nuevo_timeout = validar_entero(
            input(PROMPT_NUEVO_TIMEOUT), TIMEOUT_MINIMO, TIMEOUT_MAXIMO
        )
        if nuevo_timeout is not None:
            CONFIG["timeout"] = nuevo_timeout
        else:
            print(MSG_TIMEOUT_INVALIDO)
    elif opcion.strip() not in ("", "0"):
        print(MSG_SELECCION_INVALIDA)

    input(MSG_PRESIONAR_ENTER)


def menu_principal() -> None:
    """Menú principal"""
    while True:
        clear_screen()
        print_header(SISTEMA_TITULO)
        print(OPCION_MENU_1)
        print(OPCION_MENU_2)
        print(OPCION_MENU_3)
        print(OPCION_MENU_4)
        print(OPCION_MENU_5)
        print(OPCION_MENU_6)
        print(OPCION_MENU_7)
        print(OPCION_MENU_8)
        print(OPCION_MENU_9)
        print(OPCION_MENU_10)
        print(OPCION_MENU_11)
        print(OPCION_MENU_12)

        opcion = input(PROMPT_SELECCION_OPCION)

        if opcion == "1":
            funcion_buscar_pelicula()
        elif opcion == "2":
            funcion_buscar_actor()
        elif opcion == "3":
            funcion_buscar_series()
        elif opcion == "4":
            funcion_peliculas_populares()
        elif opcion == "5":
            funcion_buscar_por_genero()
        elif opcion == "6":
            funcion_ver_favoritos()
        elif opcion == "7":
            funcion_ver_historial()
        elif opcion == "8":
            funcion_estadisticas()
        elif opcion == "9":
            funcion_exportar()
        elif opcion == "10":
            funcion_importar()
        elif opcion == "11":
            funcion_configuracion()
        elif opcion == "12":
            print(MSG_HASTA_LUEGO)
            break
        else:
            print(MSG_OPCION_INVALIDA)
            delay(1)