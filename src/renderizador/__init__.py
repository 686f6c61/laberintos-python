#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Paquete de Renderizado
=============================================================================

Descripcion:
    Paquete de renderizado e interfaz grafica. Contiene todas las clases
    necesarias para visualizar el juego usando pygame.

Contenido:
    - pantalla.py: Clases de menus, botones y pantalla de juego

Clases principales:
    - Boton: Boton interactivo con efecto hover
    - Menu: Clase base abstracta para menus
    - MenuPrincipal: Menu inicial del juego
    - MenuDificultad: Selector de nivel de dificultad
    - PantallaCarga: Pantalla de carga (splash screen)
    - PantallaJuego: Pantalla principal del juego con HUD

Caracteristicas:
    - Sistema de camara que sigue al jugador
    - HUD con tiempo transcurrido y restante
    - Indicador de direccion hacia la meta
    - Pantallas de victoria, derrota y pausa

Uso:
    >>> from renderizador import MenuPrincipal, PantallaJuego
    >>> menu = MenuPrincipal()
    >>> menu.dibujar(superficie)

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

# Exportar las clases principales de renderizado
from .pantalla import MenuPrincipal, MenuDificultad, PantallaJuego, Boton
