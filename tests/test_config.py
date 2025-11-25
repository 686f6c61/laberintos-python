#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Tests del Modulo de Configuracion
=============================================================================

Descripcion:
    Tests unitarios para el modulo de configuracion. Verifica que todas
    las constantes y parametros del juego tengan valores validos y coherentes.

Clases de test:
    - TestConfiguracionVentana: Tests de dimensiones de ventana
    - TestConfiguracionColores: Tests de formato RGB de colores
    - TestConfiguracionLaberinto: Tests de parametros del laberinto
    - TestConfiguracionJugador: Tests de parametros del jugador
    - TestConfiguracionDificultad: Tests de niveles de dificultad
    - TestConfiguracionFuentes: Tests de tamanos de fuente
    - TestConfiguracionAnimaciones: Tests de duracion de animaciones

Repositorio:
    https://github.com/686f6c61/generador-laberintos-python

Autor:
    686f6c61 (https://github.com/686f6c61)

Version:
    0.2

Ultima actualizacion:
    Noviembre 2025
=============================================================================
"""

import pytest
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from configuracion.config import (
    ANCHO_VENTANA, ALTO_VENTANA, FPS, TITULO,
    NEGRO, BLANCO, GRIS, ROJO, VERDE, AZUL, AMARILLO, CELESTE, NARANJA, MORADO,
    TAMANO_CELDA, GROSOR_PARED,
    VELOCIDAD_JUGADOR, COLOR_JUGADOR, TAMANO_JUGADOR,
    COLOR_META,
    NIVELES_DIFICULTAD,
    TAMANO_FUENTE_PEQUENA, TAMANO_FUENTE_MEDIANA, TAMANO_FUENTE_GRANDE,
    DURACION_ANIMACION
)


class TestConfiguracionVentana:
    """Tests para la configuración de la ventana."""

    def test_dimensiones_ventana(self):
        """Verifica que las dimensiones de la ventana son válidas."""
        assert ANCHO_VENTANA > 0
        assert ALTO_VENTANA > 0

    def test_fps_valido(self):
        """Verifica que el FPS es un valor razonable."""
        assert 30 <= FPS <= 120

    def test_titulo_no_vacio(self):
        """Verifica que el título no está vacío."""
        assert len(TITULO) > 0


class TestConfiguracionColores:
    """Tests para la configuración de colores."""

    @pytest.mark.parametrize("color", [
        NEGRO, BLANCO, GRIS, ROJO, VERDE, AZUL, AMARILLO, CELESTE, NARANJA, MORADO
    ])
    def test_formato_color_rgb(self, color):
        """Verifica que los colores están en formato RGB válido."""
        assert isinstance(color, tuple)
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)

    def test_negro_correcto(self):
        """Verifica que el negro es (0, 0, 0)."""
        assert NEGRO == (0, 0, 0)

    def test_blanco_correcto(self):
        """Verifica que el blanco es (255, 255, 255)."""
        assert BLANCO == (255, 255, 255)


class TestConfiguracionLaberinto:
    """Tests para la configuración del laberinto."""

    def test_tamano_celda_positivo(self):
        """Verifica que el tamaño de celda es positivo."""
        assert TAMANO_CELDA > 0

    def test_grosor_pared_positivo(self):
        """Verifica que el grosor de pared es positivo."""
        assert GROSOR_PARED > 0

    def test_grosor_pared_menor_que_celda(self):
        """Verifica que el grosor de pared es menor que el tamaño de celda."""
        assert GROSOR_PARED < TAMANO_CELDA


class TestConfiguracionJugador:
    """Tests para la configuración del jugador."""

    def test_velocidad_positiva(self):
        """Verifica que la velocidad del jugador es positiva."""
        assert VELOCIDAD_JUGADOR > 0

    def test_tamano_jugador_positivo(self):
        """Verifica que el tamaño del jugador es positivo."""
        assert TAMANO_JUGADOR > 0

    def test_tamano_jugador_menor_que_celda(self):
        """Verifica que el jugador cabe en una celda."""
        assert TAMANO_JUGADOR < TAMANO_CELDA

    def test_color_jugador_valido(self):
        """Verifica que el color del jugador es válido."""
        assert isinstance(COLOR_JUGADOR, tuple)
        assert len(COLOR_JUGADOR) == 3


class TestConfiguracionDificultad:
    """Tests para la configuración de niveles de dificultad."""

    def test_niveles_existen(self):
        """Verifica que existen los niveles de dificultad esperados."""
        niveles_esperados = ["facil", "normal", "dificil", "muy dificil", "extremo"]
        for nivel in niveles_esperados:
            assert nivel in NIVELES_DIFICULTAD

    def test_estructura_nivel(self):
        """Verifica que cada nivel tiene la estructura correcta."""
        claves_esperadas = ["tamano", "complejidad", "densidad", "tiempo_limite"]
        for nivel, config in NIVELES_DIFICULTAD.items():
            for clave in claves_esperadas:
                assert clave in config, f"Falta '{clave}' en nivel '{nivel}'"

    def test_tamanos_validos(self):
        """Verifica que los tamaños son válidos."""
        for nivel, config in NIVELES_DIFICULTAD.items():
            filas, columnas = config["tamano"]
            assert filas > 0, f"Filas inválidas en '{nivel}'"
            assert columnas > 0, f"Columnas inválidas en '{nivel}'"

    def test_complejidad_rango_valido(self):
        """Verifica que la complejidad está entre 0 y 1."""
        for nivel, config in NIVELES_DIFICULTAD.items():
            assert 0 <= config["complejidad"] <= 1, f"Complejidad fuera de rango en '{nivel}'"

    def test_densidad_rango_valido(self):
        """Verifica que la densidad está entre 0 y 1."""
        for nivel, config in NIVELES_DIFICULTAD.items():
            assert 0 <= config["densidad"] <= 1, f"Densidad fuera de rango en '{nivel}'"

    def test_tiempo_limite_positivo(self):
        """Verifica que el tiempo límite es positivo."""
        for nivel, config in NIVELES_DIFICULTAD.items():
            assert config["tiempo_limite"] > 0, f"Tiempo límite inválido en '{nivel}'"

    def test_dificultad_progresiva_tamano(self):
        """Verifica que los tamaños aumentan con la dificultad."""
        niveles = ["facil", "normal", "dificil", "muy dificil", "extremo"]
        tamano_anterior = 0
        for nivel in niveles:
            filas, columnas = NIVELES_DIFICULTAD[nivel]["tamano"]
            tamano_actual = filas * columnas
            assert tamano_actual > tamano_anterior, \
                f"El tamaño no aumenta de forma progresiva en '{nivel}'"
            tamano_anterior = tamano_actual

    def test_dificultad_progresiva_complejidad(self):
        """Verifica que la complejidad aumenta con la dificultad."""
        niveles = ["facil", "normal", "dificil", "muy dificil", "extremo"]
        complejidad_anterior = 0
        for nivel in niveles:
            complejidad_actual = NIVELES_DIFICULTAD[nivel]["complejidad"]
            assert complejidad_actual >= complejidad_anterior, \
                f"La complejidad no aumenta de forma progresiva en '{nivel}'"
            complejidad_anterior = complejidad_actual


class TestConfiguracionFuentes:
    """Tests para la configuración de fuentes."""

    def test_tamanos_fuente_positivos(self):
        """Verifica que los tamaños de fuente son positivos."""
        assert TAMANO_FUENTE_PEQUENA > 0
        assert TAMANO_FUENTE_MEDIANA > 0
        assert TAMANO_FUENTE_GRANDE > 0

    def test_orden_tamanos_fuente(self):
        """Verifica que los tamaños de fuente están en orden."""
        assert TAMANO_FUENTE_PEQUENA < TAMANO_FUENTE_MEDIANA < TAMANO_FUENTE_GRANDE


class TestConfiguracionAnimaciones:
    """Tests para la configuración de animaciones."""

    def test_duracion_animacion_positiva(self):
        """Verifica que la duración de animación es positiva."""
        assert DURACION_ANIMACION > 0

    def test_duracion_animacion_razonable(self):
        """Verifica que la duración de animación es razonable (< 5 segundos)."""
        assert DURACION_ANIMACION < 5
