#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Modulo de Configuracion
=============================================================================

Descripcion:
    Modulo de configuracion global del juego. Contiene todas las constantes,
    parametros y configuraciones utilizadas en el juego, centralizadas para
    facilitar su modificacion y mantenimiento.

Secciones:
    1. Estados del juego (Enum)
    2. Configuracion de ventana
    3. Paleta de colores RGB
    4. Configuracion del laberinto
    5. Configuracion del jugador
    6. Niveles de dificultad
    7. Configuracion de fuentes
    8. Configuracion de animaciones
    9. Configuracion de camara e interfaz

Uso:
    >>> from configuracion.config import ANCHO_VENTANA, NIVELES_DIFICULTAD
    >>> print(f"Ventana: {ANCHO_VENTANA}x{ALTO_VENTANA}")
    >>> print(f"Dificultades: {list(NIVELES_DIFICULTAD.keys())}")

Repositorio:
    https://github.com/686f6c61/generador-laberintos-python

Autor:
    686f6c61 (https://github.com/686f6c61)

Version:
    0.2

Fecha de creacion:
    Abril 2025

Ultima actualizacion:
    Noviembre 2025

Licencia:
    Codigo abierto para uso educativo y personal.
=============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================

from enum import Enum, auto


# =============================================================================
# ESTADOS DEL JUEGO (ENUM)
# =============================================================================
# Usamos un Enum para mayor seguridad de tipos y legibilidad del codigo.
# Esto evita errores de tipeo al comparar strings y permite autocompletado
# en IDEs modernos.

class EstadoJuego(Enum):
    """
    Enumeracion de los estados posibles del juego.

    Estados disponibles:
        MENU_PRINCIPAL: Pantalla inicial con opciones
        DIFICULTAD: Selector de nivel de dificultad
        JUGANDO: Partida activa en curso
        PAUSADO: Juego pausado (tecla P)

    Example:
        >>> estado = EstadoJuego.JUGANDO
        >>> if estado == EstadoJuego.PAUSADO:
        ...     print("Juego en pausa")
    """
    MENU_PRINCIPAL = auto()  # Valor automatico: 1
    DIFICULTAD = auto()      # Valor automatico: 2
    JUGANDO = auto()         # Valor automatico: 3
    PAUSADO = auto()         # Valor automatico: 4


# =============================================================================
# CONFIGURACION DE LA VENTANA
# =============================================================================
# Parametros de la ventana principal del juego.
# La ventana usa 800x600 por defecto, un tamano estandar que funciona
# bien en la mayoria de monitores.

TITULO = "Generador de laberintos"  # Titulo mostrado en la barra de ventana
ANCHO_VENTANA = 800                 # Ancho de la ventana en pixeles
ALTO_VENTANA = 600                  # Alto de la ventana en pixeles
FPS = 60                            # Frames por segundo (60 es estandar)


# =============================================================================
# PALETA DE COLORES (FORMATO RGB)
# =============================================================================
# Colores predefinidos en formato RGB (Red, Green, Blue).
# Cada componente va de 0 a 255.
#
# Ejemplo: ROJO = (255, 0, 0)
#   - Red:   255 (maximo)
#   - Green: 0   (nada)
#   - Blue:  0   (nada)

NEGRO = (0, 0, 0)           # Color de las paredes del laberinto
BLANCO = (255, 255, 255)    # Color del fondo y caminos
GRIS = (128, 128, 128)      # Color de paneles de interfaz
ROJO = (255, 0, 0)          # Color del punto de inicio
VERDE = (0, 255, 0)         # Color del punto de meta
AZUL = (0, 0, 255)          # Color del jugador
AMARILLO = (255, 255, 0)    # Color de advertencias y pausa
CELESTE = (0, 191, 255)     # Color de hover en botones
NARANJA = (255, 165, 0)     # Color de dificultad "dificil"
MORADO = (128, 0, 128)      # Color de dificultad "muy dificil"


# =============================================================================
# CONFIGURACION DEL LABERINTO
# =============================================================================
# Parametros visuales del laberinto.
# TAMANO_CELDA define el tamano de cada celda en pixeles.
# Un laberinto de 25x25 celdas ocupara 750x750 pixeles.

TAMANO_CELDA = 30    # Tamano de cada celda en pixeles (30x30)
GROSOR_PARED = 2     # Grosor de las lineas de las paredes en pixeles


# =============================================================================
# CONFIGURACION DEL JUGADOR
# =============================================================================
# Parametros del personaje controlado por el usuario.
# El jugador es un circulo azul que se mueve por el laberinto.

VELOCIDAD_JUGADOR = 5                        # Pixeles por frame de movimiento
COLOR_JUGADOR = AZUL                         # Color del circulo del jugador
TAMANO_JUGADOR = int(TAMANO_CELDA * 0.7)     # Radio del jugador (70% de celda)


# =============================================================================
# CONFIGURACION DE LA META
# =============================================================================
# Parametros del punto de llegada (meta).

COLOR_META = VERDE  # Color del circulo de la meta


# =============================================================================
# NIVELES DE DIFICULTAD
# =============================================================================
# Diccionario con la configuracion de cada nivel de dificultad.
#
# Parametros por nivel:
#   - tamano: Tupla (filas, columnas) del laberinto
#   - complejidad: Factor 0-1 que afecta la cantidad de bifurcaciones
#   - densidad: Factor 0-1 que afecta la cantidad de paredes adicionales
#   - tiempo_limite: Segundos para completar el laberinto
#
# La dificultad aumenta progresivamente:
#   - Laberintos mas grandes
#   - Mayor complejidad (mas bifurcaciones)
#   - Mayor densidad (mas callejones sin salida)
#   - Mas tiempo (proporcional al tamano)

NIVELES_DIFICULTAD = {
    # Nivel facil: Ideal para principiantes
    # Laberinto pequeno de 15x15 con 2 minutos de tiempo
    "facil": {
        "tamano": (15, 15),       # 15x15 celdas = 450x450 pixeles
        "complejidad": 0.5,       # Complejidad media-baja
        "densidad": 0.5,          # Densidad media-baja
        "tiempo_limite": 120      # 2 minutos
    },

    # Nivel normal: Dificultad equilibrada (por defecto)
    # Laberinto mediano de 25x25 con 3 minutos de tiempo
    "normal": {
        "tamano": (25, 25),       # 25x25 celdas = 750x750 pixeles
        "complejidad": 0.6,       # Complejidad media
        "densidad": 0.6,          # Densidad media
        "tiempo_limite": 180      # 3 minutos
    },

    # Nivel dificil: Para jugadores experimentados
    # Laberinto grande de 35x35 con 4 minutos de tiempo
    "dificil": {
        "tamano": (35, 35),       # 35x35 celdas = 1050x1050 pixeles
        "complejidad": 0.7,       # Complejidad alta
        "densidad": 0.7,          # Densidad alta
        "tiempo_limite": 240      # 4 minutos
    },

    # Nivel muy dificil: Desafio serio
    # Laberinto muy grande de 45x45 con 5 minutos de tiempo
    "muy dificil": {
        "tamano": (45, 45),       # 45x45 celdas = 1350x1350 pixeles
        "complejidad": 0.8,       # Complejidad muy alta
        "densidad": 0.8,          # Densidad muy alta
        "tiempo_limite": 300      # 5 minutos
    },

    # Nivel extremo: Solo para expertos
    # Laberinto enorme de 55x55 con 6 minutos de tiempo
    "extremo": {
        "tamano": (55, 55),       # 55x55 celdas = 1650x1650 pixeles
        "complejidad": 0.9,       # Complejidad extrema
        "densidad": 0.9,          # Densidad extrema
        "tiempo_limite": 360      # 6 minutos
    }
}


# =============================================================================
# CONFIGURACION DE FUENTES
# =============================================================================
# Tamanos de fuente para diferentes usos en la interfaz.
# Usamos la fuente por defecto de pygame (None = fuente del sistema).

TAMANO_FUENTE_PEQUENA = 20   # Para informacion secundaria (version, autor)
TAMANO_FUENTE_MEDIANA = 30   # Para botones y textos normales
TAMANO_FUENTE_GRANDE = 40    # Para titulos y mensajes importantes


# =============================================================================
# CONFIGURACION DE ANIMACIONES
# =============================================================================
# Parametros para efectos visuales y animaciones.

DURACION_ANIMACION = 0.3  # Duracion en segundos de animaciones genericas


# =============================================================================
# CONFIGURACION DE LA CAMARA
# =============================================================================
# Parametros del sistema de camara que sigue al jugador.
# El factor de suavizado controla que tan rapido la camara sigue al jugador.
# Un valor bajo (0.1) da un seguimiento suave; un valor alto (1.0) es instantaneo.

FACTOR_SUAVIZADO_CAMARA = 0.1  # Factor de interpolacion para movimiento suave


# =============================================================================
# CONFIGURACION DEL INDICADOR DE META
# =============================================================================
# Parametros de la flecha que indica la direccion hacia la meta
# cuando esta fuera de la pantalla visible.

MARGEN_INDICADOR = 30         # Distancia desde el borde de la pantalla en pixeles
TAMANO_FLECHA_INDICADOR = 15  # Tamano de la flecha indicadora en pixeles


# =============================================================================
# CONFIGURACION DE PANELES DE INTERFAZ
# =============================================================================
# Parametros de los paneles superior e inferior del HUD.

ALTO_PANEL_SUPERIOR = 40  # Alto del panel con tiempo en pixeles
ALTO_PANEL_INFERIOR = 40  # Alto del panel con botones en pixeles
