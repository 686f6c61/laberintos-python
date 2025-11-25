#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Modulo de Funciones Auxiliares
=============================================================================

Descripcion:
    Modulo de funciones auxiliares y utilidades. Contiene herramientas
    reutilizables que pueden ser utilizadas por diferentes componentes
    del juego.

Funciones de conversion de coordenadas:
    - calcular_centro_celda(): Celda (fila, columna) -> Pixeles (x, y)
    - calcular_posicion_celda(): Pixeles (x, y) -> Celda (fila, columna)

Funciones de formateo:
    - formatear_tiempo(): Segundos -> Formato "mm:ss"

Funciones de renderizado:
    - dibujar_texto(): Renderiza texto en superficie pygame
    - obtener_fuente(): Obtiene fuente cacheada (optimizacion)
    - interpolar_color(): Mezcla dos colores RGB

Clases:
    - Temporizador: Gestiona tiempo con soporte de pausa/reanudacion

Optimizaciones:
    - Cache de fuentes: Evita crear fuentes nuevas cada frame
    - Operaciones matematicas simples para rendimiento

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

import time      # Para medicion de tiempo en el Temporizador
import pygame    # Para renderizado de texto y fuentes
from typing import Tuple, List, Dict, Any, Optional


# =============================================================================
# CACHE DE FUENTES (OPTIMIZACION)
# =============================================================================
# Diccionario que almacena las fuentes creadas para evitar recrearlas
# en cada frame. Esto mejora el rendimiento significativamente ya que
# crear una fuente es una operacion costosa.
#
# Clave: tamano de fuente (int)
# Valor: objeto pygame.font.Font

_cache_fuentes: Dict[int, pygame.font.Font] = {}


# =============================================================================
# FUNCIONES DE CONVERSION DE COORDENADAS
# =============================================================================

def calcular_centro_celda(fila: int, columna: int, tamano_celda: int) -> Tuple[int, int]:
    """
    Calcula las coordenadas del centro de una celda en el laberinto.

    Esta funcion convierte coordenadas de celda (fila, columna) a
    coordenadas de pixeles (x, y), calculando el punto central de la celda.

    Sistema de coordenadas:
        - Las filas aumentan hacia abajo (eje Y)
        - Las columnas aumentan hacia la derecha (eje X)
        - El origen (0,0) esta en la esquina superior izquierda

    Calculo:
        x = columna * tamano_celda + tamano_celda // 2
        y = fila * tamano_celda + tamano_celda // 2

    Args:
        fila: Numero de fila de la celda (0 = primera fila, arriba).
        columna: Numero de columna de la celda (0 = primera columna, izquierda).
        tamano_celda: Tamano de la celda en pixeles (ancho = alto).

    Returns:
        Tupla (x, y) con las coordenadas en pixeles del centro de la celda.

    Example:
        >>> # Celda (0, 0) con celdas de 30 pixeles
        >>> calcular_centro_celda(0, 0, 30)
        (15, 15)

        >>> # Celda (2, 3) con celdas de 30 pixeles
        >>> calcular_centro_celda(2, 3, 30)
        (105, 75)
    """
    # x corresponde a la columna (eje horizontal)
    x = columna * tamano_celda + tamano_celda // 2

    # y corresponde a la fila (eje vertical)
    y = fila * tamano_celda + tamano_celda // 2

    return (x, y)


def calcular_posicion_celda(x: int, y: int, tamano_celda: int) -> Tuple[int, int]:
    """
    Calcula la fila y columna de una celda a partir de coordenadas en pixeles.

    Esta es la funcion inversa de calcular_centro_celda(). Convierte
    coordenadas de pixeles (x, y) a coordenadas de celda (fila, columna).

    Calculo:
        fila = y // tamano_celda
        columna = x // tamano_celda

    Nota:
        La division entera (//) asegura que cualquier punto dentro de una
        celda devuelva las mismas coordenadas de celda.

    Args:
        x: Coordenada x en pixeles.
        y: Coordenada y en pixeles.
        tamano_celda: Tamano de la celda en pixeles.

    Returns:
        Tupla (fila, columna) de la celda que contiene el punto.

    Example:
        >>> # Punto (15, 15) con celdas de 30 pixeles -> celda (0, 0)
        >>> calcular_posicion_celda(15, 15, 30)
        (0, 0)

        >>> # Punto (95, 65) con celdas de 30 pixeles -> celda (2, 3)
        >>> calcular_posicion_celda(95, 65, 30)
        (2, 3)
    """
    fila = y // tamano_celda
    columna = x // tamano_celda
    return (fila, columna)


# =============================================================================
# FUNCIONES DE FORMATEO
# =============================================================================

def formatear_tiempo(segundos: int) -> str:
    """
    Formatea un tiempo en segundos a formato mm:ss.

    Esta funcion convierte una cantidad de segundos a un string
    con formato de minutos y segundos, con ceros a la izquierda.

    Calculo:
        minutos = segundos // 60
        segundos_restantes = segundos % 60

    Args:
        segundos: Tiempo en segundos (entero positivo).

    Returns:
        Cadena con el tiempo formateado como "mm:ss".

    Example:
        >>> formatear_tiempo(0)
        '00:00'

        >>> formatear_tiempo(45)
        '00:45'

        >>> formatear_tiempo(125)
        '02:05'

        >>> formatear_tiempo(360)
        '06:00'
    """
    minutos = segundos // 60
    segundos_restantes = segundos % 60

    # El formato :02d asegura 2 digitos con ceros a la izquierda
    return f"{minutos:02d}:{segundos_restantes:02d}"


# =============================================================================
# FUNCIONES DE RENDERIZADO
# =============================================================================

def obtener_fuente(tamano: int) -> pygame.font.Font:
    """
    Obtiene una fuente del cache o la crea si no existe.

    Esta funcion implementa un patron de cache (memoizacion) para
    evitar crear fuentes nuevas en cada frame, lo cual es costoso.

    La primera vez que se solicita un tamano, se crea la fuente y
    se almacena en el cache. Las siguientes veces se devuelve
    la fuente cacheada.

    Args:
        tamano: Tamano de la fuente en puntos.

    Returns:
        Objeto pygame.font.Font con el tamano especificado.

    Example:
        >>> fuente = obtener_fuente(30)
        >>> # La misma fuente se reutiliza en llamadas posteriores
        >>> fuente2 = obtener_fuente(30)
        >>> fuente is fuente2
        True
    """
    # Verificar si la fuente ya esta en cache
    if tamano not in _cache_fuentes:
        # Crear nueva fuente y guardar en cache
        # None = fuente por defecto del sistema
        _cache_fuentes[tamano] = pygame.font.Font(None, tamano)

    return _cache_fuentes[tamano]


def dibujar_texto(superficie: pygame.Surface, texto: str, tamano: int,
                 x: int, y: int, color: Tuple[int, int, int],
                 centrado: bool = True) -> None:
    """
    Dibuja texto en una superficie de pygame.

    Esta funcion simplifica el proceso de renderizar texto en pygame,
    que normalmente requiere varios pasos:
    1. Crear/obtener fuente
    2. Renderizar texto a superficie
    3. Obtener rectangulo de posicion
    4. Dibujar en superficie destino

    Args:
        superficie: Superficie de pygame donde dibujar el texto.
        texto: Texto a dibujar (string).
        tamano: Tamano de la fuente en puntos.
        x: Coordenada x donde dibujar el texto.
        y: Coordenada y donde dibujar el texto.
        color: Color del texto en formato RGB (tupla de 3 enteros).
        centrado: Si es True, el texto se centra en (x, y).
                 Si es False, (x, y) es la esquina superior izquierda.

    Example:
        >>> # Dibujar texto centrado
        >>> dibujar_texto(pantalla, "Hola", 30, 400, 300, (255, 255, 255))

        >>> # Dibujar texto alineado a la izquierda
        >>> dibujar_texto(pantalla, "Hola", 20, 10, 10, (0, 0, 0), centrado=False)
    """
    # Obtener fuente del cache (optimizacion)
    fuente = obtener_fuente(tamano)

    # Renderizar texto a superficie temporal
    # True = anti-aliasing activado para bordes suaves
    superficie_texto = fuente.render(texto, True, color)

    # Obtener rectangulo para posicionamiento
    rect_texto = superficie_texto.get_rect()

    # Posicionar segun el parametro centrado
    if centrado:
        # Centro del texto en (x, y)
        rect_texto.center = (x, y)
    else:
        # Esquina superior izquierda en (x, y)
        rect_texto.topleft = (x, y)

    # Dibujar en la superficie destino
    superficie.blit(superficie_texto, rect_texto)


def interpolar_color(color1: Tuple[int, int, int],
                    color2: Tuple[int, int, int],
                    factor: float) -> Tuple[int, int, int]:
    """
    Interpola entre dos colores segun un factor.

    Esta funcion realiza una interpolacion lineal entre dos colores
    RGB, util para crear transiciones suaves de color.

    Formula de interpolacion:
        resultado = color1 + (color2 - color1) * factor

    Args:
        color1: Color inicial en formato RGB (tupla de 3 enteros 0-255).
        color2: Color final en formato RGB (tupla de 3 enteros 0-255).
        factor: Factor de interpolacion entre 0 y 1.
               - 0.0 = color1 puro
               - 0.5 = mezcla 50/50
               - 1.0 = color2 puro

    Returns:
        Color interpolado en formato RGB.

    Example:
        >>> # Rojo puro (factor = 0)
        >>> interpolar_color((255, 0, 0), (0, 255, 0), 0)
        (255, 0, 0)

        >>> # Verde puro (factor = 1)
        >>> interpolar_color((255, 0, 0), (0, 255, 0), 1)
        (0, 255, 0)

        >>> # Amarillo (mezcla de rojo y verde)
        >>> interpolar_color((255, 0, 0), (0, 255, 0), 0.5)
        (127, 127, 0)
    """
    # Interpolar cada componente RGB por separado
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)

    return (r, g, b)


# =============================================================================
# CLASE TEMPORIZADOR
# =============================================================================

class Temporizador:
    """
    Clase para manejar el tiempo transcurrido y limites de tiempo.

    Esta clase proporciona funcionalidad de cronometro con soporte para:
    - Medir tiempo transcurrido
    - Establecer tiempo limite
    - Pausar y reanudar
    - Detectar cuando se agota el tiempo

    El tiempo se mide usando time.time() que proporciona precision
    de milisegundos, suficiente para un juego.

    Attributes:
        tiempo_inicio (float): Timestamp del momento de inicio.
        tiempo_limite (int | None): Tiempo maximo en segundos, o None si no hay limite.
        tiempo_pausado (float): Tiempo total acumulado en estado de pausa.
        pausado (bool): True si el temporizador esta pausado.
        tiempo_pausa_inicio (float): Timestamp del inicio de la pausa actual.

    Example:
        >>> # Temporizador sin limite
        >>> timer = Temporizador()
        >>> print(timer.obtener_tiempo_transcurrido())

        >>> # Temporizador con limite de 60 segundos
        >>> timer = Temporizador(tiempo_limite=60)
        >>> print(timer.obtener_tiempo_restante())
    """

    def __init__(self, tiempo_limite: Optional[int] = None):
        """
        Inicializa un nuevo temporizador.

        Args:
            tiempo_limite: Tiempo limite en segundos.
                          Si es None, el temporizador no tiene limite
                          (modo cronometro infinito).
        """
        # Guardar el timestamp actual como inicio
        self.tiempo_inicio = time.time()

        # Tiempo limite opcional
        self.tiempo_limite = tiempo_limite

        # Variables para manejo de pausa
        self.tiempo_pausado = 0        # Tiempo total acumulado en pausa
        self.pausado = False           # Estado actual de pausa
        self.tiempo_pausa_inicio = 0   # Timestamp del inicio de la pausa

    def reiniciar(self, tiempo_limite: Optional[int] = None) -> None:
        """
        Reinicia el temporizador.

        Restablece el tiempo transcurrido a 0 y opcionalmente
        cambia el tiempo limite.

        Args:
            tiempo_limite: Nuevo tiempo limite en segundos.
                          Si es None, se mantiene el limite anterior.

        Example:
            >>> timer = Temporizador(60)
            >>> # ... pasa tiempo ...
            >>> timer.reiniciar()  # Reinicia con el mismo limite
            >>> timer.reiniciar(120)  # Reinicia con nuevo limite
        """
        # Nuevo timestamp de inicio
        self.tiempo_inicio = time.time()

        # Actualizar limite solo si se proporciona
        if tiempo_limite is not None:
            self.tiempo_limite = tiempo_limite

        # Resetear variables de pausa
        self.tiempo_pausado = 0
        self.pausado = False

    def pausar(self) -> None:
        """
        Pausa el temporizador.

        Cuando se pausa, el tiempo deja de correr hasta que se
        llame a reanudar(). Llamar a pausar() cuando ya esta
        pausado no tiene efecto.

        Example:
            >>> timer = Temporizador(60)
            >>> timer.pausar()
            >>> # El tiempo no avanza mientras esta pausado
            >>> timer.reanudar()
        """
        # Solo pausar si no esta ya pausado
        if not self.pausado:
            self.pausado = True
            # Guardar cuando empezo la pausa
            self.tiempo_pausa_inicio = time.time()

    def reanudar(self) -> None:
        """
        Reanuda el temporizador si estaba pausado.

        Calcula el tiempo que estuvo pausado y lo acumula para
        restarlo del tiempo transcurrido total.

        Example:
            >>> timer = Temporizador(60)
            >>> timer.pausar()
            >>> time.sleep(5)  # 5 segundos en pausa
            >>> timer.reanudar()
            >>> # Los 5 segundos de pausa no cuentan
        """
        if self.pausado:
            # Calcular tiempo que estuvo pausado y acumularlo
            self.tiempo_pausado += time.time() - self.tiempo_pausa_inicio
            self.pausado = False

    def obtener_tiempo_transcurrido(self) -> int:
        """
        Obtiene el tiempo transcurrido en segundos.

        Calcula el tiempo desde el inicio, descontando el tiempo
        que estuvo pausado.

        Returns:
            Tiempo transcurrido en segundos (entero redondeado hacia abajo).

        Example:
            >>> timer = Temporizador()
            >>> time.sleep(5)
            >>> print(timer.obtener_tiempo_transcurrido())  # ~5
        """
        if self.pausado:
            # Si esta pausado, usar el tiempo hasta el inicio de la pausa
            return int(self.tiempo_pausa_inicio - self.tiempo_inicio - self.tiempo_pausado)

        # Tiempo actual menos inicio menos tiempo pausado
        return int(time.time() - self.tiempo_inicio - self.tiempo_pausado)

    def obtener_tiempo_restante(self) -> Optional[int]:
        """
        Obtiene el tiempo restante en segundos.

        Calcula cuanto tiempo queda antes de que se agote el limite.
        Si no hay limite establecido, devuelve None.

        Returns:
            Tiempo restante en segundos (minimo 0), o None si no hay limite.

        Example:
            >>> timer = Temporizador(60)
            >>> time.sleep(10)
            >>> print(timer.obtener_tiempo_restante())  # ~50
        """
        # Si no hay limite, no hay tiempo restante que calcular
        if self.tiempo_limite is None:
            return None

        # Calcular restante: limite - transcurrido
        tiempo_restante = self.tiempo_limite - self.obtener_tiempo_transcurrido()

        # No devolver valores negativos
        return max(0, tiempo_restante)

    def ha_terminado(self) -> bool:
        """
        Verifica si se ha agotado el tiempo.

        Returns:
            True si hay un limite establecido y el tiempo restante es 0.
            False si no hay limite o aun queda tiempo.

        Example:
            >>> timer = Temporizador(60)
            >>> print(timer.ha_terminado())  # False
            >>> # ... pasan 60+ segundos ...
            >>> print(timer.ha_terminado())  # True
        """
        # Si no hay limite, nunca termina
        if self.tiempo_limite is None:
            return False

        # Verificar si el tiempo restante llego a 0
        return self.obtener_tiempo_restante() <= 0
