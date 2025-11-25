#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Paquete de Tests
=============================================================================

Descripcion:
    Paquete de tests unitarios para el generador de laberintos. Contiene
    pruebas automatizadas usando pytest para verificar el correcto
    funcionamiento de todos los componentes del juego.

Estructura de tests:
    - test_config.py: Tests para configuraciones y constantes
    - test_helpers.py: Tests para funciones auxiliares y Temporizador
    - test_laberinto.py: Tests para generacion y solvibilidad de laberintos

Ejecucion:
    Ejecutar todos los tests:
    >>> python3 -m pytest tests/ -v

    Ejecutar tests con cobertura:
    >>> python3 -m pytest tests/ --cov=src

    Ejecutar tests especificos:
    >>> python3 -m pytest tests/test_laberinto.py -v

Requisitos:
    - pytest
    - pygame (para tests de renderizado)
    - numpy (para tests de laberinto)

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

# Este archivo marca el directorio como un paquete Python
# Los tests se ejecutan con pytest, no requiere imports especiales
