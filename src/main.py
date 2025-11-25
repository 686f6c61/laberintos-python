#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Modulo Principal
=============================================================================

Descripcion:
    Modulo principal del generador de laberintos. Contiene la clase Juego que
    gestiona el bucle principal, los estados del juego y la coordinacion entre
    todos los componentes del sistema.

Funcionamiento:
    Este modulo implementa el patron de maquina de estados para gestionar
    las diferentes pantallas del juego:

    - MENU_PRINCIPAL: Pantalla inicial con opciones de juego
    - DIFICULTAD: Selector de nivel de dificultad
    - JUGANDO: Pantalla activa del juego
    - PAUSADO: Juego en pausa (tecla P)

Bucle Principal:
    El juego sigue el clasico bucle de juego:
    1. Procesar eventos (teclado, raton, cierre)
    2. Actualizar logica del estado actual
    3. Renderizar el estado actual
    4. Controlar FPS (60 frames por segundo)

Uso:
    Ejecutar directamente:
    >>> python3 src/main.py

    O importar la clase Juego:
    >>> from main import Juego
    >>> juego = Juego()
    >>> juego.ejecutar()

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

import sys
import pygame
from typing import Dict, Any, Optional

# Imports internos del proyecto
from configuracion.config import (
    ANCHO_VENTANA, ALTO_VENTANA, FPS, TITULO, NIVELES_DIFICULTAD, EstadoJuego,
    ALTO_PANEL_SUPERIOR, ALTO_PANEL_INFERIOR
)
from generador.laberinto import Laberinto
from jugador.personaje import Jugador
from renderizador.pantalla import MenuPrincipal, MenuDificultad, PantallaJuego
from utilidades.helpers import Temporizador


# =============================================================================
# CLASE PRINCIPAL DEL JUEGO
# =============================================================================

class Juego:
    """
    Clase principal que gestiona el juego completo.

    Esta clase es el punto central de control del juego. Maneja:
    - Inicializacion de pygame y la ventana grafica
    - Gestion de estados del juego (menu, dificultad, jugando, pausado)
    - Bucle principal de eventos, actualizacion y renderizado
    - Transiciones entre estados

    Attributes:
        ventana (pygame.Surface): Superficie principal de renderizado.
        reloj (pygame.time.Clock): Controlador de FPS.
        estado_actual (EstadoJuego): Estado actual del juego (Enum).
        dificultad_actual (str): Nivel de dificultad seleccionado.
        menu_principal (MenuPrincipal): Instancia del menu principal.
        menu_dificultad (MenuDificultad): Instancia del menu de dificultad.
        laberinto (Laberinto): Instancia del laberinto generado.
        jugador (Jugador): Instancia del personaje jugable.
        pantalla_juego (PantallaJuego): Instancia de la pantalla de juego.

    Example:
        >>> juego = Juego()
        >>> juego.ejecutar()  # Inicia el bucle principal
    """

    def __init__(self):
        """
        Inicializa el juego.

        Este constructor realiza las siguientes operaciones:
        1. Inicializa el motor pygame
        2. Configura la ventana grafica (800x600 pixeles)
        3. Crea el reloj para control de FPS
        4. Establece el estado inicial (menu principal)
        5. Crea las instancias de los menus
        6. Inicializa los componentes del juego

        Raises:
            pygame.error: Si falla la inicializacion de pygame.
        """
        # ---------------------------------------------------------------------
        # Inicializacion de pygame
        # ---------------------------------------------------------------------
        pygame.init()  # Inicializa todos los modulos de pygame
        pygame.display.set_caption(TITULO)  # Establece el titulo de la ventana

        # ---------------------------------------------------------------------
        # Crear ventana principal
        # ---------------------------------------------------------------------
        # La ventana es de 800x600 pixeles por defecto (configurable en config.py)
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

        # Reloj para controlar los FPS (60 por defecto)
        self.reloj = pygame.time.Clock()

        # ---------------------------------------------------------------------
        # Estado inicial del juego
        # ---------------------------------------------------------------------
        # Usamos un Enum para mayor seguridad y legibilidad
        self.estado_actual = EstadoJuego.MENU_PRINCIPAL

        # Dificultad por defecto: normal (25x25 celdas, 3 minutos)
        self.dificultad_actual = "normal"

        # ---------------------------------------------------------------------
        # Crear menus
        # ---------------------------------------------------------------------
        self.menu_principal = MenuPrincipal()
        self.menu_dificultad = MenuDificultad()

        # ---------------------------------------------------------------------
        # Inicializar componentes del juego
        # ---------------------------------------------------------------------
        self._inicializar_juego()

    def _inicializar_juego(self) -> None:
        """
        Inicializa los componentes del juego segun la dificultad seleccionada.

        Este metodo crea nuevas instancias de:
        - Laberinto: Con tamano y complejidad segun la dificultad
        - Jugador: Posicionado en el inicio del laberinto
        - PantallaJuego: Para renderizar el laberinto y el jugador

        El laberinto se genera proceduralmente usando el algoritmo DFS
        modificado, garantizando que siempre exista una solucion.

        Note:
            Este metodo se llama al inicio y cada vez que se cambia
            la dificultad para regenerar el laberinto.
        """
        # ---------------------------------------------------------------------
        # Obtener configuracion de dificultad
        # ---------------------------------------------------------------------
        # NIVELES_DIFICULTAD es un diccionario con las configuraciones:
        # - tamano: (filas, columnas) del laberinto
        # - complejidad: factor 0-1 que afecta bifurcaciones
        # - densidad: factor 0-1 que afecta paredes adicionales
        # - tiempo_limite: segundos para completar el laberinto
        config_dificultad = NIVELES_DIFICULTAD[self.dificultad_actual]

        # Extraer parametros de configuracion
        filas, columnas = config_dificultad["tamano"]
        complejidad = config_dificultad["complejidad"]
        densidad = config_dificultad["densidad"]

        # ---------------------------------------------------------------------
        # Calcular tamaño de celda para que el laberinto quepa en la ventana
        # ---------------------------------------------------------------------
        # El área disponible es la ventana menos los paneles superior e inferior
        area_disponible_ancho = ANCHO_VENTANA
        area_disponible_alto = ALTO_VENTANA - ALTO_PANEL_SUPERIOR - ALTO_PANEL_INFERIOR

        # Calcular el tamaño máximo de celda que permite que quepa el laberinto
        tamano_celda_x = area_disponible_ancho // columnas
        tamano_celda_y = area_disponible_alto // filas
        tamano_celda = min(tamano_celda_x, tamano_celda_y)

        # ---------------------------------------------------------------------
        # Crear laberinto
        # ---------------------------------------------------------------------
        # El laberinto se genera automaticamente en el constructor
        # usando el algoritmo DFS modificado
        self.laberinto = Laberinto(filas, columnas, complejidad, densidad, tamano_celda)

        # ---------------------------------------------------------------------
        # Crear jugador
        # ---------------------------------------------------------------------
        # El jugador se posiciona automaticamente en la celda de inicio
        self.jugador = Jugador(self.laberinto)

        # ---------------------------------------------------------------------
        # Crear pantalla de juego
        # ---------------------------------------------------------------------
        self.pantalla_juego = PantallaJuego(self.laberinto, self.jugador)

        # Configurar tiempo limite segun la dificultad
        tiempo_limite = config_dificultad["tiempo_limite"]
        self.pantalla_juego.temporizador.reiniciar(tiempo_limite)

        # Actualizar la dificultad mostrada en el menu principal
        self.menu_principal.dificultad_actual = self.dificultad_actual

    def ejecutar(self) -> None:
        """
        Ejecuta el bucle principal del juego.

        Este es el corazon del juego. Implementa el clasico game loop:

        1. EVENTOS: Procesa todos los eventos de pygame (teclado, raton, etc.)
        2. ACTUALIZAR: Actualiza la logica del estado actual
        3. RENDERIZAR: Dibuja el estado actual en pantalla
        4. DISPLAY: Actualiza la pantalla con los cambios
        5. FPS: Controla la velocidad del juego (60 FPS)

        El bucle continua hasta que:
        - El usuario cierra la ventana (evento QUIT)
        - El usuario selecciona "Salir" en el menu
        - El usuario presiona ESC

        Note:
            Este metodo bloquea la ejecucion hasta que el juego termina.
            Al finalizar, limpia los recursos de pygame.
        """
        ejecutando = True

        # =====================================================================
        # BUCLE PRINCIPAL DEL JUEGO
        # =====================================================================
        while ejecutando:
            # -----------------------------------------------------------------
            # 1. PROCESAR EVENTOS
            # -----------------------------------------------------------------
            # pygame.event.get() devuelve todos los eventos pendientes
            for evento in pygame.event.get():
                # Evento de cierre de ventana (click en X o Alt+F4)
                if evento.type == pygame.QUIT:
                    ejecutando = False

                # Pasar el evento al manejador del estado actual
                self._manejar_evento_estado(evento)

            # -----------------------------------------------------------------
            # 2. ACTUALIZAR LOGICA
            # -----------------------------------------------------------------
            self._actualizar_estado()

            # -----------------------------------------------------------------
            # 3. RENDERIZAR
            # -----------------------------------------------------------------
            self._renderizar_estado()

            # -----------------------------------------------------------------
            # 4. ACTUALIZAR PANTALLA
            # -----------------------------------------------------------------
            # flip() actualiza toda la pantalla (mas eficiente que update())
            pygame.display.flip()

            # -----------------------------------------------------------------
            # 5. CONTROLAR FPS
            # -----------------------------------------------------------------
            # tick() pausa el tiempo necesario para mantener 60 FPS
            self.reloj.tick(FPS)

        # =====================================================================
        # LIMPIEZA Y CIERRE
        # =====================================================================
        pygame.quit()  # Libera recursos de pygame
        sys.exit()     # Termina el proceso de Python

    def _manejar_evento_estado(self, evento: pygame.event.Event) -> None:
        """
        Maneja un evento segun el estado actual del juego.

        Este metodo implementa el patron de maquina de estados para
        distribuir los eventos al manejador correspondiente segun
        el estado actual del juego.

        Args:
            evento: Evento de pygame a procesar. Puede ser:
                   - KEYDOWN/KEYUP: Eventos de teclado
                   - MOUSEBUTTONDOWN: Clicks de raton
                   - QUIT: Cierre de ventana

        Estados manejados:
            - MENU_PRINCIPAL: Botones Jugar, Dificultad, Salir
            - DIFICULTAD: Seleccion de nivel de dificultad
            - JUGANDO/PAUSADO: Control del jugador y pausa (tecla P)
        """
        # =====================================================================
        # ESTADO: MENU PRINCIPAL
        # =====================================================================
        if self.estado_actual == EstadoJuego.MENU_PRINCIPAL:
            accion = self.menu_principal.manejar_evento(evento)
            if accion:
                if accion == "jugar":
                    # Transicion a estado JUGANDO
                    self.estado_actual = EstadoJuego.JUGANDO
                elif accion == "dificultad":
                    # Transicion a estado DIFICULTAD
                    self.estado_actual = EstadoJuego.DIFICULTAD
                elif accion == "salir":
                    # Terminar el juego
                    pygame.quit()
                    sys.exit()

        # =====================================================================
        # ESTADO: SELECCION DE DIFICULTAD
        # =====================================================================
        elif self.estado_actual == EstadoJuego.DIFICULTAD:
            resultado = self.menu_dificultad.manejar_evento(evento)
            if resultado:
                accion = resultado.get("accion")
                if accion == "cambiar_dificultad":
                    # Cambiar dificultad y regenerar laberinto
                    self.dificultad_actual = resultado.get("dificultad")
                    self._inicializar_juego()
                    self.estado_actual = EstadoJuego.MENU_PRINCIPAL
                elif accion == "menu_principal":
                    # Volver al menu sin cambiar dificultad
                    self.estado_actual = EstadoJuego.MENU_PRINCIPAL

        # =====================================================================
        # ESTADO: JUGANDO O PAUSADO
        # =====================================================================
        elif self.estado_actual in (EstadoJuego.JUGANDO, EstadoJuego.PAUSADO):
            # -----------------------------------------------------------------
            # Manejar pausa con tecla P
            # -----------------------------------------------------------------
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                if self.estado_actual == EstadoJuego.JUGANDO:
                    # Pausar el juego
                    self.estado_actual = EstadoJuego.PAUSADO
                    self.pantalla_juego.temporizador.pausar()
                else:
                    # Reanudar el juego
                    self.estado_actual = EstadoJuego.JUGANDO
                    self.pantalla_juego.temporizador.reanudar()
                return  # No procesar mas eventos este frame

            # -----------------------------------------------------------------
            # Pasar evento a la pantalla de juego
            # -----------------------------------------------------------------
            accion = self.pantalla_juego.manejar_evento(evento)
            if accion:
                if accion == "menu_principal":
                    self.estado_actual = EstadoJuego.MENU_PRINCIPAL

    def _actualizar_estado(self) -> None:
        """
        Actualiza la logica del estado actual del juego.

        Cada estado tiene su propia logica de actualizacion:

        - MENU_PRINCIPAL: Actualiza hover de botones
        - DIFICULTAD: Actualiza hover de botones
        - JUGANDO: Actualiza posicion del jugador, colisiones,
                   temporizador, deteccion de victoria/derrota
        - PAUSADO: No actualiza nada (juego congelado)

        Note:
            Esta funcion se llama 60 veces por segundo (cada frame).
            Es importante que sea eficiente para mantener el rendimiento.
        """
        if self.estado_actual == EstadoJuego.MENU_PRINCIPAL:
            # Actualizar estado visual de los botones (hover)
            self.menu_principal.actualizar()

        elif self.estado_actual == EstadoJuego.DIFICULTAD:
            # Actualizar estado visual de los botones (hover)
            self.menu_dificultad.actualizar()

        elif self.estado_actual == EstadoJuego.JUGANDO:
            # Actualizar logica del juego (jugador, colisiones, tiempo)
            accion = self.pantalla_juego.actualizar()
            if accion == "menu_principal":
                self.estado_actual = EstadoJuego.MENU_PRINCIPAL

        elif self.estado_actual == EstadoJuego.PAUSADO:
            # En pausa no actualizamos nada - el juego esta congelado
            pass

    def _renderizar_estado(self) -> None:
        """
        Renderiza el estado actual del juego en pantalla.

        Cada estado tiene su propia pantalla de renderizado:

        - MENU_PRINCIPAL: Menu con botones y titulo
        - DIFICULTAD: Lista de niveles de dificultad
        - JUGANDO: Laberinto, jugador, HUD (tiempo, distancia)
        - PAUSADO: Laberinto + overlay de pausa

        Note:
            El renderizado se hace en la superficie principal (self.ventana)
            y se muestra en pantalla con pygame.display.flip()
        """
        if self.estado_actual == EstadoJuego.MENU_PRINCIPAL:
            self.menu_principal.dibujar(self.ventana)

        elif self.estado_actual == EstadoJuego.DIFICULTAD:
            self.menu_dificultad.dibujar(self.ventana)

        elif self.estado_actual == EstadoJuego.JUGANDO:
            self.pantalla_juego.dibujar(self.ventana)

        elif self.estado_actual == EstadoJuego.PAUSADO:
            # En pausa mostramos el juego con overlay de pausa
            self.pantalla_juego.dibujar(self.ventana, pausado=True)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    # Crear instancia del juego
    juego = Juego()

    # Iniciar bucle principal
    # (Este metodo bloquea hasta que el usuario cierra el juego)
    juego.ejecutar()
