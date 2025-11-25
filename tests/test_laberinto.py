#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Tests del Modulo de Laberintos
=============================================================================

Descripcion:
    Tests unitarios para el modulo de generacion de laberintos. Verifica
    la correcta generacion, solvibilidad y funcionamiento de los laberintos.

Clases de test:
    - TestLaberintoCreacion: Tests de creacion basica de laberintos
    - TestLaberintoSolvibilidad: Tests de verificacion de soluciones
    - TestLaberintoInicioMeta: Tests de posiciones de inicio y meta
    - TestLaberintoMetodos: Tests de metodos es_pared() y es_meta()
    - TestLaberintoMatriz: Tests de estructura de la matriz
    - TestLaberintoDimensiones: Tests de dimensiones calculadas

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
import numpy as np
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generador.laberinto import Laberinto


class TestLaberintoCreacion:
    """Tests para la creación básica de laberintos."""

    def test_crear_laberinto_basico(self):
        """Verifica que se puede crear un laberinto con parámetros básicos."""
        laberinto = Laberinto(15, 15)
        assert laberinto.filas == 15
        assert laberinto.columnas == 15
        assert laberinto.matriz.shape == (15, 15)

    def test_crear_laberinto_rectangular(self):
        """Verifica que se pueden crear laberintos rectangulares."""
        laberinto = Laberinto(10, 20)
        assert laberinto.filas == 10
        assert laberinto.columnas == 20
        assert laberinto.matriz.shape == (10, 20)

    def test_complejidad_y_densidad(self):
        """Verifica que los parámetros de complejidad y densidad se asignan correctamente."""
        laberinto = Laberinto(15, 15, complejidad=0.8, densidad=0.7)
        assert laberinto.complejidad == 0.8
        assert laberinto.densidad == 0.7

    @pytest.mark.parametrize("filas,columnas", [
        (15, 15),
        (25, 25),
        (35, 35),
        (45, 45),
        (55, 55),
    ])
    def test_tamanos_dificultad(self, filas, columnas):
        """Verifica que se pueden crear laberintos de todos los tamaños de dificultad."""
        laberinto = Laberinto(filas, columnas)
        assert laberinto.filas == filas
        assert laberinto.columnas == columnas


class TestLaberintoSolvibilidad:
    """Tests para verificar que los laberintos son solubles."""

    def _verificar_camino_existe(self, laberinto):
        """Verifica que existe un camino entre inicio y meta usando BFS."""
        from collections import deque

        visitado = set()
        cola = deque([laberinto.inicio])
        visitado.add(laberinto.inicio)

        direcciones = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while cola:
            x, y = cola.popleft()

            if (x, y) == laberinto.meta:
                return True

            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy

                if (0 <= nx < laberinto.filas and
                    0 <= ny < laberinto.columnas and
                    (nx, ny) not in visitado and
                    laberinto.matriz[nx, ny] == 0):
                    visitado.add((nx, ny))
                    cola.append((nx, ny))

        return False

    def test_laberinto_tiene_solucion(self):
        """Verifica que un laberinto básico tiene solución."""
        laberinto = Laberinto(15, 15)
        assert self._verificar_camino_existe(laberinto)

    @pytest.mark.parametrize("complejidad,densidad", [
        (0.5, 0.5),
        (0.6, 0.6),
        (0.7, 0.7),
        (0.8, 0.8),
        (0.9, 0.9),
    ])
    def test_laberinto_solucion_diferentes_dificultades(self, complejidad, densidad):
        """Verifica que laberintos con diferentes dificultades tienen solución."""
        laberinto = Laberinto(25, 25, complejidad=complejidad, densidad=densidad)
        assert self._verificar_camino_existe(laberinto)

    def test_multiples_laberintos_aleatorios(self):
        """Verifica que múltiples laberintos generados aleatoriamente tienen solución."""
        for _ in range(10):
            laberinto = Laberinto(15, 15)
            assert self._verificar_camino_existe(laberinto), \
                "Se generó un laberinto sin solución"


class TestLaberintoInicioMeta:
    """Tests para verificar las posiciones de inicio y meta."""

    def test_inicio_es_camino(self):
        """Verifica que la posición de inicio es un camino, no una pared."""
        laberinto = Laberinto(15, 15)
        assert laberinto.matriz[laberinto.inicio] == 0

    def test_meta_es_camino(self):
        """Verifica que la posición de meta es un camino, no una pared."""
        laberinto = Laberinto(15, 15)
        assert laberinto.matriz[laberinto.meta] == 0

    def test_inicio_y_meta_diferentes(self):
        """Verifica que inicio y meta son posiciones diferentes."""
        laberinto = Laberinto(15, 15)
        assert laberinto.inicio != laberinto.meta

    def test_inicio_en_zona_superior_izquierda(self):
        """Verifica que el inicio está en la zona superior izquierda."""
        laberinto = Laberinto(25, 25)
        mitad = 25 // 2
        # El inicio debe estar cerca de la esquina superior izquierda
        assert laberinto.inicio[0] <= mitad or laberinto.inicio[1] <= mitad

    def test_meta_en_zona_inferior_derecha(self):
        """Verifica que la meta está en la zona inferior derecha."""
        laberinto = Laberinto(25, 25)
        mitad = 25 // 2
        # La meta debe estar cerca de la esquina inferior derecha
        assert laberinto.meta[0] >= mitad or laberinto.meta[1] >= mitad


class TestLaberintoMetodos:
    """Tests para los métodos del laberinto."""

    def test_es_pared_en_pared(self):
        """Verifica que es_pared devuelve True para una pared."""
        laberinto = Laberinto(15, 15)
        # El borde siempre es pared
        assert laberinto.es_pared(0, 0) == True

    def test_es_pared_fuera_limites(self):
        """Verifica que es_pared devuelve True para posiciones fuera de límites."""
        laberinto = Laberinto(15, 15)
        assert laberinto.es_pared(-1, 0) == True
        assert laberinto.es_pared(0, -1) == True
        assert laberinto.es_pared(15, 0) == True
        assert laberinto.es_pared(0, 15) == True

    def test_es_pared_en_camino(self):
        """Verifica que es_pared devuelve False para un camino."""
        laberinto = Laberinto(15, 15)
        # El inicio siempre es un camino
        assert laberinto.es_pared(*laberinto.inicio) == False

    def test_es_meta_en_meta(self):
        """Verifica que es_meta devuelve True para la posición de meta."""
        laberinto = Laberinto(15, 15)
        assert laberinto.es_meta(*laberinto.meta) == True

    def test_es_meta_en_otra_posicion(self):
        """Verifica que es_meta devuelve False para otras posiciones."""
        laberinto = Laberinto(15, 15)
        assert laberinto.es_meta(*laberinto.inicio) == False


class TestLaberintoMatriz:
    """Tests para la estructura de la matriz del laberinto."""

    def test_matriz_solo_ceros_y_unos(self):
        """Verifica que la matriz solo contiene 0s (camino) y 1s (pared)."""
        laberinto = Laberinto(15, 15)
        valores_unicos = np.unique(laberinto.matriz)
        assert all(v in [0, 1] for v in valores_unicos)

    def test_matriz_tiene_caminos(self):
        """Verifica que la matriz tiene al menos algunos caminos (0s)."""
        laberinto = Laberinto(15, 15)
        num_caminos = np.sum(laberinto.matriz == 0)
        assert num_caminos > 0

    def test_matriz_tiene_paredes(self):
        """Verifica que la matriz tiene al menos algunas paredes (1s)."""
        laberinto = Laberinto(15, 15)
        num_paredes = np.sum(laberinto.matriz == 1)
        assert num_paredes > 0

    def test_bordes_son_mayormente_paredes(self):
        """Verifica que los bordes del laberinto son mayormente paredes."""
        laberinto = Laberinto(15, 15)
        # Verificar bordes
        borde_superior = laberinto.matriz[0, :]
        borde_inferior = laberinto.matriz[-1, :]
        borde_izquierdo = laberinto.matriz[:, 0]
        borde_derecho = laberinto.matriz[:, -1]

        # La mayoría de las celdas del borde deberían ser paredes
        total_bordes = len(borde_superior) + len(borde_inferior) + len(borde_izquierdo) + len(borde_derecho)
        paredes_borde = (np.sum(borde_superior == 1) + np.sum(borde_inferior == 1) +
                        np.sum(borde_izquierdo == 1) + np.sum(borde_derecho == 1))

        # Al menos 50% de los bordes deberían ser paredes
        assert paredes_borde >= total_bordes * 0.5


class TestLaberintoDimensiones:
    """Tests para las dimensiones del laberinto."""

    def test_ancho_correcto(self):
        """Verifica que el ancho se calcula correctamente."""
        laberinto = Laberinto(15, 20)
        from configuracion.config import TAMANO_CELDA
        assert laberinto.ancho == 20 * TAMANO_CELDA

    def test_alto_correcto(self):
        """Verifica que el alto se calcula correctamente."""
        laberinto = Laberinto(15, 20)
        from configuracion.config import TAMANO_CELDA
        assert laberinto.alto == 15 * TAMANO_CELDA
