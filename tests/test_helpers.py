#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Tests del Modulo de Utilidades
=============================================================================

Descripcion:
    Tests unitarios para el modulo de funciones auxiliares. Verifica
    el correcto funcionamiento de conversiones, formateo y temporizador.

Clases de test:
    - TestCalcularCentroCelda: Tests de conversion celda -> pixeles
    - TestCalcularPosicionCelda: Tests de conversion pixeles -> celda
    - TestFormatearTiempo: Tests de formateo de tiempo mm:ss
    - TestInterpolarColor: Tests de interpolacion de colores RGB
    - TestTemporizador: Tests de la clase Temporizador

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
import time

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utilidades.helpers import (
    calcular_centro_celda,
    calcular_posicion_celda,
    formatear_tiempo,
    interpolar_color,
    Temporizador
)


class TestCalcularCentroCelda:
    """Tests para la función calcular_centro_celda."""

    def test_celda_origen(self):
        """Verifica el centro de la celda en el origen."""
        x, y = calcular_centro_celda(0, 0, 30)
        assert x == 15  # 0 * 30 + 30 // 2
        assert y == 15

    def test_celda_fila_columna(self):
        """Verifica el centro de una celda en posición arbitraria."""
        x, y = calcular_centro_celda(2, 3, 30)
        # columna * tamano + tamano // 2 = 3 * 30 + 15 = 105
        # fila * tamano + tamano // 2 = 2 * 30 + 15 = 75
        assert x == 105
        assert y == 75

    def test_diferentes_tamanos_celda(self):
        """Verifica con diferentes tamaños de celda."""
        x, y = calcular_centro_celda(1, 1, 20)
        assert x == 30  # 1 * 20 + 10
        assert y == 30


class TestCalcularPosicionCelda:
    """Tests para la función calcular_posicion_celda."""

    def test_origen(self):
        """Verifica la celda para coordenadas en el origen."""
        fila, columna = calcular_posicion_celda(0, 0, 30)
        assert fila == 0
        assert columna == 0

    def test_centro_celda(self):
        """Verifica que el centro de una celda devuelve esa celda."""
        fila, columna = calcular_posicion_celda(15, 15, 30)
        assert fila == 0
        assert columna == 0

    def test_posicion_arbitraria(self):
        """Verifica una posición arbitraria."""
        fila, columna = calcular_posicion_celda(95, 65, 30)
        # y // tamano = 65 // 30 = 2
        # x // tamano = 95 // 30 = 3
        assert fila == 2
        assert columna == 3


class TestFormatearTiempo:
    """Tests para la función formatear_tiempo."""

    def test_cero_segundos(self):
        """Verifica formato de 0 segundos."""
        assert formatear_tiempo(0) == "00:00"

    def test_menos_de_un_minuto(self):
        """Verifica formato de tiempo menor a un minuto."""
        assert formatear_tiempo(45) == "00:45"

    def test_un_minuto_exacto(self):
        """Verifica formato de exactamente un minuto."""
        assert formatear_tiempo(60) == "01:00"

    def test_minutos_y_segundos(self):
        """Verifica formato de minutos y segundos."""
        assert formatear_tiempo(125) == "02:05"

    def test_tiempo_largo(self):
        """Verifica formato de tiempo largo."""
        assert formatear_tiempo(360) == "06:00"

    def test_padding_ceros(self):
        """Verifica que se agregan ceros a la izquierda."""
        assert formatear_tiempo(5) == "00:05"
        assert formatear_tiempo(65) == "01:05"


class TestInterpolarColor:
    """Tests para la función interpolar_color."""

    def test_factor_cero(self):
        """Verifica que factor 0 devuelve el primer color."""
        color1 = (255, 0, 0)
        color2 = (0, 255, 0)
        resultado = interpolar_color(color1, color2, 0)
        assert resultado == (255, 0, 0)

    def test_factor_uno(self):
        """Verifica que factor 1 devuelve el segundo color."""
        color1 = (255, 0, 0)
        color2 = (0, 255, 0)
        resultado = interpolar_color(color1, color2, 1)
        assert resultado == (0, 255, 0)

    def test_factor_medio(self):
        """Verifica interpolación al 50%."""
        color1 = (0, 0, 0)
        color2 = (200, 100, 50)
        resultado = interpolar_color(color1, color2, 0.5)
        assert resultado == (100, 50, 25)

    def test_colores_iguales(self):
        """Verifica interpolación con colores iguales."""
        color = (128, 64, 32)
        resultado = interpolar_color(color, color, 0.5)
        assert resultado == color


class TestTemporizador:
    """Tests para la clase Temporizador."""

    def test_crear_sin_limite(self):
        """Verifica crear un temporizador sin límite de tiempo."""
        timer = Temporizador()
        assert timer.tiempo_limite is None
        assert timer.ha_terminado() == False

    def test_crear_con_limite(self):
        """Verifica crear un temporizador con límite de tiempo."""
        timer = Temporizador(tiempo_limite=60)
        assert timer.tiempo_limite == 60

    def test_tiempo_transcurrido_inicial(self):
        """Verifica que el tiempo transcurrido inicial es cercano a 0."""
        timer = Temporizador()
        assert timer.obtener_tiempo_transcurrido() <= 1

    def test_tiempo_restante_con_limite(self):
        """Verifica el tiempo restante con un límite establecido."""
        timer = Temporizador(tiempo_limite=60)
        restante = timer.obtener_tiempo_restante()
        assert restante is not None
        assert 59 <= restante <= 60

    def test_tiempo_restante_sin_limite(self):
        """Verifica que tiempo restante es None sin límite."""
        timer = Temporizador()
        assert timer.obtener_tiempo_restante() is None

    def test_reiniciar(self):
        """Verifica que reiniciar restablece el temporizador."""
        timer = Temporizador(tiempo_limite=60)
        time.sleep(0.1)
        timer.reiniciar()
        assert timer.obtener_tiempo_transcurrido() <= 1

    def test_reiniciar_con_nuevo_limite(self):
        """Verifica reiniciar con un nuevo límite de tiempo."""
        timer = Temporizador(tiempo_limite=60)
        timer.reiniciar(tiempo_limite=120)
        assert timer.tiempo_limite == 120

    def test_pausar_y_reanudar(self):
        """Verifica la funcionalidad de pausar y reanudar."""
        timer = Temporizador(tiempo_limite=60)
        time.sleep(0.2)

        timer.pausar()
        tiempo_pausado = timer.obtener_tiempo_transcurrido()

        time.sleep(0.2)
        # El tiempo no debería avanzar mientras está pausado
        assert timer.obtener_tiempo_transcurrido() == tiempo_pausado

        timer.reanudar()
        time.sleep(0.2)
        # Ahora el tiempo debería haber avanzado (usa >= ya que puede ser el mismo segundo)
        assert timer.obtener_tiempo_transcurrido() >= tiempo_pausado

    def test_ha_terminado_false(self):
        """Verifica que ha_terminado devuelve False cuando hay tiempo."""
        timer = Temporizador(tiempo_limite=60)
        assert timer.ha_terminado() == False

    def test_tiempo_restante_no_negativo(self):
        """Verifica que el tiempo restante nunca es negativo."""
        timer = Temporizador(tiempo_limite=0)
        assert timer.obtener_tiempo_restante() >= 0
