#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Paquete del Jugador
=============================================================================

Descripcion:
    Paquete del jugador. Contiene la logica del personaje controlado por
    el usuario, incluyendo movimiento, colisiones y animaciones.

Contenido:
    - personaje.py: Clase Jugador con sistema de movimiento y colisiones

Caracteristicas:
    - Movimiento con teclas de flecha (arriba, abajo, izquierda, derecha)
    - Deteccion de colisiones con paredes del laberinto
    - Animacion de "respiracion" del personaje
    - Deteccion de llegada a la meta

Uso:
    >>> from jugador import Jugador
    >>> jugador = Jugador(laberinto)
    >>> jugador.manejar_evento(evento)  # Procesar input de teclado
    >>> jugador.actualizar()            # Actualizar posicion
    >>> jugador.dibujar(superficie)     # Renderizar jugador

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

# Exportar la clase Jugador
from .personaje import Jugador
