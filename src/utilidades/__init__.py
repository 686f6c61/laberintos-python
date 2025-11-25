#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Paquete de Utilidades
=============================================================================

Descripcion:
    Paquete de utilidades y funciones auxiliares. Contiene herramientas
    reutilizables que pueden ser utilizadas por diferentes componentes.

Contenido:
    - helpers.py: Funciones matematicas, de renderizado y clase Temporizador

Funciones disponibles:
    - calcular_centro_celda(): Convierte coordenadas de celda a pixeles
    - calcular_posicion_celda(): Convierte pixeles a coordenadas de celda
    - formatear_tiempo(): Formatea segundos a formato mm:ss
    - dibujar_texto(): Renderiza texto en superficie pygame
    - interpolar_color(): Interpola entre dos colores RGB
    - obtener_fuente(): Obtiene fuente cacheada (optimizacion)

Clases disponibles:
    - Temporizador: Gestiona tiempo transcurrido con soporte de pausa

Uso:
    >>> from utilidades import formatear_tiempo, Temporizador
    >>> print(formatear_tiempo(125))  # "02:05"
    >>> timer = Temporizador(tiempo_limite=60)
    >>> print(timer.obtener_tiempo_restante())

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

# Exportar todas las funciones y clases del modulo helpers
from .helpers import *
