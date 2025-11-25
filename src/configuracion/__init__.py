#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Paquete de Configuracion
=============================================================================

Descripcion:
    Paquete de configuracion global del juego. Contiene todas las constantes,
    parametros y configuraciones utilizadas por los diferentes modulos.

Contenido:
    - config.py: Constantes globales (colores, tamanos, dificultades, etc.)

Uso:
    Las configuraciones se importan automaticamente al importar el paquete:
    >>> from configuracion import ANCHO_VENTANA, ALTO_VENTANA
    >>> from configuracion import NIVELES_DIFICULTAD, EstadoJuego

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

# Exportar todas las configuraciones del modulo config
from .config import *
