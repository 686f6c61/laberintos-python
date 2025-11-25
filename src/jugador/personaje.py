#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Modulo del Jugador
=============================================================================

Descripcion:
    Modulo del jugador. Contiene la clase Jugador que maneja toda la logica
    del personaje controlado por el usuario, incluyendo movimiento, colisiones
    y animaciones visuales.

Funcionalidad:
    - Control por teclado (flechas direccionales)
    - Deteccion de colisiones con paredes
    - Animacion de "respiracion" del personaje
    - Deteccion de llegada a la meta

Sistema de coordenadas:
    El jugador maneja dos sistemas de coordenadas:
    - Pixeles (x, y): Posicion exacta para renderizado
    - Celda (fila, columna): Posicion en la grilla del laberinto

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

import pygame
from typing import Tuple, List, Dict, Any, Optional

from configuracion.config import COLOR_JUGADOR, VELOCIDAD_JUGADOR
from generador.laberinto import Laberinto
from utilidades.helpers import calcular_centro_celda


class Jugador:
    """
    Clase que representa al jugador en el laberinto.
    
    Esta clase maneja el movimiento del jugador, las colisiones con las paredes
    y la detección de llegada a la meta.
    """
    
    def __init__(self, laberinto: Laberinto):
        """
        Inicializa un nuevo jugador.

        Args:
            laberinto: Instancia del laberinto donde se moverá el jugador.
        """
        self._laberinto = laberinto
        self._fila, self._columna = laberinto.inicio
        self._tamano_celda = laberinto.tamano_celda

        # Calcular posición inicial en píxeles
        centro_x, centro_y = calcular_centro_celda(self._fila, self._columna, self._tamano_celda)
        self._x = centro_y
        self._y = centro_x

        # Tamaño del jugador proporcional a la celda (70%)
        self._tamano = int(self._tamano_celda * 0.7)
        self._color = COLOR_JUGADOR
        self._velocidad = VELOCIDAD_JUGADOR
        
        # Estado del movimiento
        self._moviendo_arriba = False
        self._moviendo_abajo = False
        self._moviendo_izquierda = False
        self._moviendo_derecha = False
        
        # Animación de movimiento
        self._animacion_contador = 0
        self._animacion_max = 5  # Frames para completar una animación
    
    @property
    def posicion(self) -> Tuple[int, int]:
        """
        Obtiene la posición actual del jugador en píxeles.
        
        Returns:
            Tupla con las coordenadas (x, y) del jugador.
        """
        return (self._x, self._y)
    
    @property
    def celda(self) -> Tuple[int, int]:
        """
        Obtiene la celda actual del jugador (fila, columna).
        
        Returns:
            Tupla con (fila, columna) de la celda actual.
        """
        return (self._fila, self._columna)
    
    def reiniciar(self) -> None:
        """
        Reinicia la posición del jugador al inicio del laberinto.
        """
        self._fila, self._columna = self._laberinto.inicio
        centro_x, centro_y = calcular_centro_celda(self._fila, self._columna, self._tamano_celda)
        self._x = centro_y
        self._y = centro_x
        
        # Reiniciar estado de movimiento
        self._moviendo_arriba = False
        self._moviendo_abajo = False
        self._moviendo_izquierda = False
        self._moviendo_derecha = False
        self._animacion_contador = 0
    
    def manejar_evento(self, evento: pygame.event.Event) -> None:
        """
        Maneja los eventos de teclado para controlar al jugador.
        
        Args:
            evento: Evento de pygame a manejar.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self._moviendo_arriba = True
            elif evento.key == pygame.K_DOWN:
                self._moviendo_abajo = True
            elif evento.key == pygame.K_LEFT:
                self._moviendo_izquierda = True
            elif evento.key == pygame.K_RIGHT:
                self._moviendo_derecha = True
        
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_UP:
                self._moviendo_arriba = False
            elif evento.key == pygame.K_DOWN:
                self._moviendo_abajo = False
            elif evento.key == pygame.K_LEFT:
                self._moviendo_izquierda = False
            elif evento.key == pygame.K_RIGHT:
                self._moviendo_derecha = False
    
    def actualizar(self) -> None:
        """
        Actualiza la posición del jugador según las teclas presionadas.
        """
        # Guardar posición anterior
        x_anterior, y_anterior = self._x, self._y
        fila_anterior, columna_anterior = self._fila, self._columna
        
        # Actualizar posición según teclas presionadas
        if self._moviendo_arriba:
            self._y -= self._velocidad
        if self._moviendo_abajo:
            self._y += self._velocidad
        if self._moviendo_izquierda:
            self._x -= self._velocidad
        if self._moviendo_derecha:
            self._x += self._velocidad
        
        # Calcular nueva celda
        nueva_fila = self._y // self._tamano_celda
        nueva_columna = self._x // self._tamano_celda
        
        # Verificar colisiones con paredes
        if self._laberinto.es_pared(nueva_fila, nueva_columna):
            # Revertir movimiento
            self._x, self._y = x_anterior, y_anterior
            nueva_fila, nueva_columna = fila_anterior, columna_anterior
        
        # Actualizar celda actual
        self._fila, self._columna = nueva_fila, nueva_columna
        
        # Actualizar contador de animación
        if self._moviendo_arriba or self._moviendo_abajo or self._moviendo_izquierda or self._moviendo_derecha:
            self._animacion_contador = (self._animacion_contador + 1) % self._animacion_max
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja al jugador en la superficie proporcionada.
        
        Args:
            superficie: Superficie de pygame donde dibujar al jugador.
        """
        # Calcular tamaño de animación (efecto de "respiración")
        factor_animacion = abs(self._animacion_contador - self._animacion_max // 2) / (self._animacion_max // 2)
        tamano_animado = int(self._tamano * (0.9 + 0.1 * factor_animacion))
        
        # Dibujar jugador (círculo)
        pygame.draw.circle(superficie, self._color, (self._x, self._y), tamano_animado)
    
    def ha_llegado_meta(self) -> bool:
        """
        Verifica si el jugador ha llegado a la meta.
        
        Returns:
            True si el jugador está en la celda de la meta, False en caso contrario.
        """
        return self._laberinto.es_meta(self._fila, self._columna)
