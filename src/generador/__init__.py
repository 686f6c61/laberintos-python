#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Paquete de Generacion
=============================================================================

Descripcion:
    Paquete de generacion de laberintos. Contiene los algoritmos y clases
    necesarias para crear laberintos proceduralmente.

Contenido:
    - laberinto.py: Clase Laberinto con algoritmo DFS modificado

Algoritmo:
    El algoritmo principal es una version modificada de DFS (Depth-First Search)
    que genera laberintos perfectos con las siguientes caracteristicas:
    - Siempre existe exactamente un camino entre dos puntos
    - Se anaden bifurcaciones y callejones sin salida
    - Se crean ciclos opcionales para multiples rutas
    - Se garantiza solvibilidad mediante verificacion

Uso:
    >>> from generador import Laberinto
    >>> laberinto = Laberinto(filas=25, columnas=25, complejidad=0.6, densidad=0.6)
    >>> print(f"Inicio: {laberinto.inicio}, Meta: {laberinto.meta}")

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

# Exportar la clase Laberinto
from .laberinto import Laberinto
