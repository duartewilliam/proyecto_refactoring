"""
Módulo de constantes del proyecto "Películas y Series".

Centraliza los valores hardcodeados (números mágicos, textos de UI,
parámetros de API y datos mock) extraídos en la Fase 2, Hito 2.
"""

# ============================================
# Sistema
# ============================================
SISTEMA_TITULO = "SISTEMA DE PELÍCULAS Y SERIES"
EXTENSION_JSON = ".json"
EXIT_OK = 0
EXIT_ERROR = 1

# ============================================
# Comandos de sistema operativo
# ============================================
CLS_NT = "cls"
CLS_UNIX = "clear"

# ============================================
# UI / Display
# ============================================
SEPARADOR = "="
SEPARADOR_LONGITUD = 60
ANCHO_CENTRADO = 60
RESUMEN_MAX_LONGITUD = 200
SUFRAGO_RESUMEN = "..."
N_A = "N/A"
CONFIRMAR_SI = "s"
CONFIRMAR_NO = "n"
PREFIJO_NUMERACION = ". "
ABRIR_PARENTESIS = " ("
CERRAR_PARENTESIS_RATING = ") - "
CERRAR_PARENTESIS = ")"
MSG_PELICULA_DESCONOCIDA = "Película desconocida"
MSG_PRESIONAR_ENTER = "\nPresione Enter para continuar..."

# ============================================
# Parámetros y endpoints de APIs
# ============================================
URL_PARAM_TITULO = "?t="
URL_PARAM_BUSQUEDA = "?s="
URL_PARAM_TIPO_PELICULA = "&type=movie"
URL_PARAM_API_KEY = "&apikey="
URL_ENDPOINT_BUSCAR_SERIES = "/search/shows?q="
URL_ENDPOINT_DETALLES_SERIE = "/shows/"
PREFIX_CACHE_SERIES = "series_"

# ============================================
# Dominio
# ============================================
GENERO_ACCION = "accion"
GENERO_COMEDIA = "comedia"
FECHA_HARDCODEADA = "hoy"
MSG_GENEROS_DISPONIBLES = "Géneros disponibles: acción, comedia"

# ============================================
# Labels de campos de película
# ============================================
LABEL_TITULO = "Título: "
LABEL_ANIO = "Año: "
LABEL_RATING_IMDB = "Rating IMDB: "
LABEL_RATING = "Rating: "
LABEL_GENERO = "Género: "
LABEL_DIRECTOR = "Director: "
LABEL_ACTORES = "Actores: "
LABEL_TRAMA = "Trama: "
LABEL_PAIS = "País: "
LABEL_PREMIOS = "Premios: "

# ============================================
# Labels de campos de serie
# ============================================
LABEL_NOMBRE = "Nombre: "
LABEL_IDIOMA = "Idioma: "
LABEL_GENEROS = "Géneros: "
LABEL_ESTADO = "Estado: "
LABEL_ESTRENO = "Estreno: "
LABEL_FINAL = "Final: "
LABEL_EPISODIOS = "Episodios: "
LABEL_RESUMEN = "Resumen: "

# ============================================
# Mensajes y prompts de búsqueda
# ============================================
PROMPT_TITULO = "Ingrese el título de la película: "
PROMPT_ACTOR = "Ingrese el nombre del actor: "
PROMPT_SERIE = "Ingrese el nombre de la serie: "
PROMPT_GENERO = "Ingrese el género: "
MSG_BUSCANDO = "Buscando..."
MSG_BUSCANDO_ACTOR = "Buscando películas del actor..."
MSG_BUSCANDO_SERIES = "Buscando series..."
MSG_NO_ENCONTRADA = "No se encontró la película"
MSG_NO_ENCONTRADAS_ACTOR = "No se encontraron películas para ese actor"
MSG_NO_ENCONTRADAS_SERIES = "No se encontraron series"
MSG_BUSQUEDA_INVALIDA = "Búsqueda inválida (no puede estar vacía ni exceder 120 caracteres)"
MSG_GENERO_INVALIDO = "Género inválido. Use: acción o comedia"

# ============================================
# Favoritos y historial
# ============================================
PROMPT_AGREGAR_FAVORITOS = "\n¿Agregar a favoritos? (s/n): "
MSG_AGREGADA_FAVORITOS = "¡Agregada a favoritos!"
MSG_YA_EN_FAVORITOS = "Ya está en favoritos"
PROMPT_ELIMINAR_FAVORITA = "\n¿Desea eliminar alguna? (número o Enter para volver): "
MSG_ELIMINADA_FAVORITOS = "Eliminada de favoritos"
MSG_SIN_FAVORITAS = "No tienes películas favoritas"
PROMPT_LIMPIAR_HISTORIAL = "\n¿Limpiar historial? (s/n): "
MSG_HISTORIAL_LIMPIADO = "Historial limpiado"
MSG_SIN_HISTORIAL = "No hay historial"

# ============================================
# Selección en listas
# ============================================
PROMPT_SELECCION_PELICULA = "\nSeleccione una película para ver detalles (0 para volver): "
PROMPT_SELECCION_SERIE = "\nSeleccione una serie para ver detalles (0 para volver): "
MSG_SELECCION_INVALIDA = "Selección inválida"

# ============================================
# Estadísticas
# ============================================
LABEL_TOTAL_FAVORITAS = "Total favoritas: "
LABEL_TOTAL_HISTORIAL = "Total historial: "

# ============================================
# Exportar / Importar
# ============================================
PROMPT_NOMBRE_ARCHIVO = "Nombre del archivo (sin extensión): "
MSG_ERROR_IMPORTAR = "Error al importar archivo"
MSG_NOMBRE_ARCHIVO_INVALIDO = "Nombre de archivo inválido"

# ============================================
# Configuración
# ============================================
LABEL_DEBUG_CONFIG = "1. Debug: "
LABEL_VERBOSE_CONFIG = "2. Verbose: "
LABEL_TIMEOUT_CONFIG = "3. Timeout: "
PROMPT_OPCION_CONFIG = "\nSeleccione opción a cambiar (0 para volver): "
MSG_DEBUG_ACTUAL = "Debug ahora es: "
MSG_VERBOSE_ACTUAL = "Verbose ahora es: "
PROMPT_NUEVO_TIMEOUT = "Nuevo timeout: "
MSG_TIMEOUT_INVALIDO = "Timeout inválido (debe ser un entero entre 1 y 300)"

# ============================================
# Headers y menú
# ============================================
HEADER_PELICULAS_POPULARES = "PELÍCULAS POPULARES"
HEADER_MIS_FAVORITOS = "MIS FAVORITOS"
HEADER_HISTORIAL = "HISTORIAL DE BÚSQUEDAS"
HEADER_ESTADISTICAS = "ESTADÍSTICAS"
HEADER_CONFIGURACION = "CONFIGURACIÓN"
OPCION_MENU_1 = "1. Buscar película por título"
OPCION_MENU_2 = "2. Buscar por actor"
OPCION_MENU_3 = "3. Buscar series"
OPCION_MENU_4 = "4. Ver películas populares"
OPCION_MENU_5 = "5. Buscar por género"
OPCION_MENU_6 = "6. Ver favoritos"
OPCION_MENU_7 = "7. Ver historial"
OPCION_MENU_8 = "8. Ver estadísticas"
OPCION_MENU_9 = "9. Exportar datos"
OPCION_MENU_10 = "10. Importar datos"
OPCION_MENU_11 = "11. Configuración"
OPCION_MENU_12 = "12. Salir"
PROMPT_SELECCION_OPCION = "\nSeleccione una opción: "
MSG_HASTA_LUEGO = "¡Hasta luego!"
MSG_OPCION_INVALIDA = "Opción inválida"
MSG_PROGRAMA_INTERRUMPIDO = "\n\nPrograma interrumpido"
MSG_ERROR_INESPERADO = "Error inesperado: "

# ============================================
# Datos mock (sin API)
# ============================================
PELICULAS_POPULARES = [
    {"titulo": "The Shawshank Redemption", "anio": 1994, "rating": 9.3},
    {"titulo": "The Godfather", "anio": 1972, "rating": 9.2},
    {"titulo": "The Dark Knight", "anio": 2008, "rating": 9.0},
    {"titulo": "Pulp Fiction", "anio": 1994, "rating": 8.9},
    {"titulo": "Forrest Gump", "anio": 1994, "rating": 8.8},
]

PELICULAS_ACCION = [
    {"titulo": "Die Hard", "anio": 1988, "rating": 8.2},
    {"titulo": "Mad Max Fury Road", "anio": 2015, "rating": 8.1},
]

PELICULAS_COMEDIA = [
    {"titulo": "Superbad", "anio": 2007, "rating": 7.6},
    {"titulo": "The Hangover", "anio": 2009, "rating": 7.7},
]