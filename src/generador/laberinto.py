#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DE LABERINTOS - Modulo de Generacion de Laberintos
=============================================================================

Descripcion:
    Modulo principal de generacion de laberintos. Implementa el algoritmo
    DFS (Depth-First Search) modificado para crear laberintos procedurales
    con diferentes niveles de complejidad.

Algoritmo DFS Modificado:
    1. Inicializar matriz llena de paredes (1s)
    2. Elegir celda inicial aleatoria (posiciones impares)
    3. Usar pila para DFS: derribar paredes hacia vecinos no visitados
    4. Agregar complejidad: bifurcaciones y callejones sin salida
    5. Crear ciclos: derribar algunas paredes para multiples rutas
    6. Garantizar solvibilidad: verificar camino con BFS/DFS

Caracteristicas del laberinto generado:
    - Siempre tiene solucion (verificado algoritmicamente)
    - Inicio en zona superior izquierda
    - Meta en zona inferior derecha
    - Complejidad ajustable (0.0 - 1.0)
    - Densidad ajustable (0.0 - 1.0)

Estructura de datos:
    - Matriz NumPy uint8: 0 = camino, 1 = pared
    - Optimizada para memoria (8 bits por celda)

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

import random
import numpy as np
from typing import Tuple, List, Dict, Any, Optional

import pygame
from configuracion.config import TAMANO_CELDA, GROSOR_PARED, BLANCO, NEGRO, ROJO, VERDE
from utilidades.helpers import calcular_centro_celda


class Laberinto:
    """
    Clase que representa un laberinto y contiene la lógica para generarlo.
    
    Esta clase implementa el algoritmo de generación de laberintos usando
    el método de división recursiva, y proporciona métodos para dibujar
    y comprobar colisiones en el laberinto.
    """
    
    def __init__(self, filas: int, columnas: int, complejidad: float = 0.5,
                 densidad: float = 0.5, tamano_celda: int = None):
        """
        Inicializa un nuevo laberinto.

        Args:
            filas: Número de filas del laberinto.
            columnas: Número de columnas del laberinto.
            complejidad: Factor de complejidad del laberinto (0-1).
            densidad: Factor de densidad de paredes (0-1).
            tamano_celda: Tamaño de cada celda en píxeles. Si es None, usa TAMANO_CELDA.
        """
        self.filas = filas
        self.columnas = columnas
        self.complejidad = complejidad
        self.densidad = densidad
        self.tamano_celda = tamano_celda if tamano_celda is not None else TAMANO_CELDA
        self.ancho = columnas * self.tamano_celda
        self.alto = filas * self.tamano_celda
        
        # Inicializar la matriz del laberinto (0 = camino, 1 = pared)
        # Usar uint8 para optimizar memoria (8x menos que int64)
        self.matriz = np.zeros((filas, columnas), dtype=np.uint8)
        
        # Posiciones de inicio y meta
        self.inicio = (0, 0)
        self.meta = (filas - 1, columnas - 1)
        
        # Generar el laberinto
        self._generar()
    
    def _generar(self) -> None:
        """
        Genera un laberinto aleatorio usando una versión mejorada del algoritmo DFS
        con modificaciones para crear laberintos más complejos y desafiantes.
        """
        # Inicializar todas las celdas como paredes
        self.matriz.fill(1)
        
        # Definir direcciones: arriba, derecha, abajo, izquierda
        direcciones = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        
        # Elegir una celda inicial aleatoria (debe ser impar para que las paredes queden en posiciones pares)
        inicio_x = random.randrange(1, self.filas - 1, 2)
        inicio_y = random.randrange(1, self.columnas - 1, 2)
        
        # Marcar la celda inicial como camino
        self.matriz[inicio_x, inicio_y] = 0
        
        # Pila para el algoritmo DFS
        pila = [(inicio_x, inicio_y)]
        visitadas = set([(inicio_x, inicio_y)])
        
        # Lista para almacenar puntos de bifurcación potenciales
        bifurcaciones = []
        
        # Factor de ramificación (probabilidad de crear caminos adicionales)
        factor_ramificacion = min(0.3, self.complejidad * 0.4)  # Ajustar según complejidad
        
        # Mientras haya celdas en la pila
        while pila:
            # Obtener la celda actual
            x, y = pila[-1]
            
            # Encontrar vecinos no visitados (a 2 celdas de distancia)
            vecinos = []
            random.shuffle(direcciones)  # Aleatorizar direcciones para variedad
            
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                
                # Verificar que el vecino esté dentro de los límites
                if 1 <= nx < self.filas - 1 and 1 <= ny < self.columnas - 1:
                    # Si el vecino no ha sido visitado
                    if (nx, ny) not in visitadas:
                        vecinos.append((nx, ny, dx // 2, dy // 2))
            
            # Si hay vecinos no visitados
            if vecinos:
                # Si hay más de un vecino, este es un punto de bifurcación potencial
                if len(vecinos) > 1:
                    bifurcaciones.append((x, y, vecinos[1:]))
                
                # Elegir un vecino aleatorio
                nx, ny, wx, wy = vecinos[0]
                
                # Derribar la pared entre la celda actual y el vecino
                self.matriz[x + wx, y + wy] = 0
                
                # Marcar el vecino como camino
                self.matriz[nx, ny] = 0
                
                # Agregar el vecino a la pila y marcarlo como visitado
                pila.append((nx, ny))
                visitadas.add((nx, ny))
            else:
                # Si no hay vecinos no visitados, retroceder
                pila.pop()
        
        # Crear callejones sin salida adicionales y caminos alternativos
        self._agregar_complejidad(visitadas, bifurcaciones, factor_ramificacion)
        
        # Crear algunos ciclos para hacer el laberinto más desafiante
        self._crear_ciclos(visitadas, self.densidad * 0.15)
    
    def _agregar_complejidad(self, visitadas, bifurcaciones, factor_ramificacion):
        """
        Agrega complejidad adicional al laberinto creando callejones sin salida
        y caminos alternativos.
        
        Args:
            visitadas: Conjunto de celdas ya visitadas.
            bifurcaciones: Lista de puntos de bifurcación potenciales.
            factor_ramificacion: Probabilidad de crear caminos adicionales.
        """
        # Procesar puntos de bifurcación para crear callejones sin salida
        random.shuffle(bifurcaciones)  # Aleatorizar para variedad
        
        # Limitar el número de bifurcaciones para no hacer el laberinto demasiado fácil
        num_bifurcaciones = int(len(bifurcaciones) * factor_ramificacion)
        
        for i in range(min(num_bifurcaciones, len(bifurcaciones))):
            x, y, vecinos = bifurcaciones[i]
            
            # Elegir un vecino aleatorio para crear un callejon sin salida
            if vecinos:
                nx, ny, wx, wy = vecinos[0]
                
                # Verificar si el vecino aún no ha sido visitado (podría haber cambiado)
                if (nx, ny) not in visitadas:
                    # Derribar la pared
                    self.matriz[x + wx, y + wy] = 0
                    
                    # Marcar el vecino como camino
                    self.matriz[nx, ny] = 0
                    
                    # Crear un callejon sin salida de longitud variable
                    longitud = random.randint(1, 3)
                    self._crear_callejon(nx, ny, longitud, visitadas)
    
    def _crear_callejon(self, x, y, longitud, visitadas):
        """
        Crea un callejon sin salida de longitud variable.
        
        Args:
            x, y: Coordenadas iniciales.
            longitud: Longitud máxima del callejon.
            visitadas: Conjunto de celdas ya visitadas.
        """
        # Direcciones: arriba, derecha, abajo, izquierda
        direcciones = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        random.shuffle(direcciones)
        
        for _ in range(longitud):
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                
                # Verificar límites y que no haya sido visitada
                if (1 <= nx < self.filas - 1 and 1 <= ny < self.columnas - 1 and 
                    (nx, ny) not in visitadas):
                    # Derribar la pared
                    self.matriz[x + dx // 2, y + dy // 2] = 0
                    
                    # Marcar como camino
                    self.matriz[nx, ny] = 0
                    visitadas.add((nx, ny))
                    
                    # Continuar desde la nueva posición
                    x, y = nx, ny
                    break
            else:
                # No se encontró dirección válida, terminar
                break
    
    def _crear_ciclos(self, visitadas, probabilidad):
        """
        Crea ciclos en el laberinto derribando algunas paredes para hacer
        el laberinto más desafiante con múltiples rutas.
        
        Args:
            visitadas: Conjunto de celdas ya visitadas.
            probabilidad: Probabilidad de crear un ciclo.
        """
        # Recorrer celdas interiores
        for i in range(2, self.filas - 2, 2):
            for j in range(2, self.columnas - 2, 2):
                # Solo considerar paredes (no esquinas)
                if self.matriz[i, j] == 1:
                    # Verificar si es una pared horizontal o vertical
                    es_horizontal = (self.matriz[i-1, j] == 0 and self.matriz[i+1, j] == 0)
                    es_vertical = (self.matriz[i, j-1] == 0 and self.matriz[i, j+1] == 0)
                    
                    # Si es una pared válida y se cumple la probabilidad
                    if (es_horizontal or es_vertical) and random.random() < probabilidad:
                        # Derribar la pared para crear un ciclo
                        self.matriz[i, j] = 0
        
        # Asegurar que inicio y meta sean caminos
        self._establecer_inicio_meta()
        
        # Asegurar que el laberinto tenga solución
        self._garantizar_solucion()
    
    def _establecer_inicio_meta(self) -> None:
        """
        Establece las posiciones de inicio y meta, asegurando que estén en extremos opuestos
        del laberinto y que sean caminos válidos (no paredes).
        """
        # Encontrar todas las celdas que son caminos
        caminos = []
        for i in range(1, self.filas - 1):
            for j in range(1, self.columnas - 1):
                if self.matriz[i, j] == 0:
                    caminos.append((i, j))
        
        if not caminos:
            # Si no hay caminos, crear al menos uno
            self.matriz[1, 1] = 0
            self.matriz[self.filas - 2, self.columnas - 2] = 0
            self.inicio = (1, 1)
            self.meta = (self.filas - 2, self.columnas - 2)
            return
        
        # Dividir el laberinto en cuadrantes
        mitad_fila = self.filas // 2
        mitad_columna = self.columnas // 2
        
        # Buscar caminos en el cuadrante superior izquierdo para el inicio
        caminos_inicio = []
        for i, j in caminos:
            if i < mitad_fila and j < mitad_columna:
                caminos_inicio.append((i, j))
        
        # Si no hay caminos en ese cuadrante, buscar en la mitad izquierda
        if not caminos_inicio:
            for i, j in caminos:
                if j < mitad_columna:
                    caminos_inicio.append((i, j))
        
        # Si aún no hay caminos, usar cualquiera disponible
        if not caminos_inicio:
            caminos_inicio = caminos
        
        # Seleccionar el punto más cercano a la esquina superior izquierda
        self.inicio = min(caminos_inicio, key=lambda pos: pos[0] + pos[1])
        
        # Buscar caminos en el cuadrante inferior derecho para la meta
        caminos_meta = []
        for i, j in caminos:
            # Asegurar que esté lejos del inicio (al menos la mitad del tamaño del laberinto)
            distancia_al_inicio = abs(i - self.inicio[0]) + abs(j - self.inicio[1])
            if (i >= mitad_fila and j >= mitad_columna and 
                distancia_al_inicio > max(self.filas, self.columnas) // 2):
                caminos_meta.append((i, j))
        
        # Si no hay caminos en ese cuadrante, buscar en la mitad derecha
        if not caminos_meta:
            for i, j in caminos:
                if j >= mitad_columna and (i, j) != self.inicio:
                    caminos_meta.append((i, j))
        
        # Si aún no hay caminos, usar cualquiera disponible excepto el inicio
        if not caminos_meta:
            caminos_meta = [pos for pos in caminos if pos != self.inicio]
        
        # Si por alguna razón no hay otros caminos, crear uno
        if not caminos_meta:
            nueva_meta = (self.filas - 2, self.columnas - 2)
            self.matriz[nueva_meta] = 0
            self.meta = nueva_meta
            return
        
        # Seleccionar el punto más cercano a la esquina inferior derecha
        self.meta = max(caminos_meta, 
                        key=lambda pos: (self.filas - pos[0] - 1) + (self.columnas - pos[1] - 1))
        
        # Asegurar que inicio y meta sean caminos (no paredes)
        self.matriz[self.inicio] = 0
        self.matriz[self.meta] = 0
    
    def _garantizar_solucion(self) -> None:
        """
        Garantiza que exista al menos un camino entre el inicio y la meta.
        Utiliza un algoritmo de búsqueda en profundidad (DFS).
        """
        # Crear una copia de la matriz para marcar celdas visitadas
        visitado = np.zeros((self.filas, self.columnas), dtype=bool)
        
        # Función recursiva para DFS
        def dfs(x: int, y: int) -> bool:
            if (x, y) == self.meta:
                return True
            
            visitado[x, y] = True
            
            # Direcciones: arriba, derecha, abajo, izquierda
            direcciones = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            random.shuffle(direcciones)  # Aleatorizar para variedad
            
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                
                # Verificar límites
                if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                    # Si es un camino y no ha sido visitado
                    if self.matriz[nx, ny] == 0 and not visitado[nx, ny]:
                        if dfs(nx, ny):
                            return True
            
            return False
        
        # Verificar si hay un camino
        if not dfs(*self.inicio):
            # Si no hay camino, crear uno
            self._crear_camino()
    
    def _crear_camino(self) -> None:
        """
        Crea un camino directo entre el inicio y la meta.
        """
        x, y = self.inicio
        meta_x, meta_y = self.meta
        
        # Moverse primero horizontalmente
        while y != meta_y:
            y += 1 if y < meta_y else -1
            self.matriz[x, y] = 0
        
        # Luego moverse verticalmente
        while x != meta_x:
            x += 1 if x < meta_x else -1
            self.matriz[x, y] = 0
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el laberinto en la superficie proporcionada.
        
        Args:
            superficie: Superficie de pygame donde dibujar el laberinto.
        """
        # Asegurar que inicio y meta sean caminos antes de dibujar
        self.matriz[self.inicio] = 0
        self.matriz[self.meta] = 0
        
        # Dibujar celdas usando el tamaño de celda de esta instancia
        tc = self.tamano_celda
        for i in range(self.filas):
            for j in range(self.columnas):
                x = j * tc
                y = i * tc

                # Dibujar paredes o caminos
                if self.matriz[i, j] == 1:
                    pygame.draw.rect(superficie, NEGRO, (x, y, tc, tc))
                else:
                    pygame.draw.rect(superficie, BLANCO, (x, y, tc, tc))
                    # Dibujar borde de la celda
                    pygame.draw.rect(superficie, NEGRO, (x, y, tc, tc), GROSOR_PARED)

        # Dibujar inicio y meta
        inicio_x, inicio_y = calcular_centro_celda(*self.inicio, tc)
        meta_x, meta_y = calcular_centro_celda(*self.meta, tc)

        # Dibujar inicio (círculo rojo)
        pygame.draw.circle(superficie, ROJO, (inicio_y, inicio_x), tc // 3)

        # Dibujar meta (círculo verde)
        pygame.draw.circle(superficie, VERDE, (meta_y, meta_x), tc // 3)
    
    def es_pared(self, fila: int, columna: int) -> bool:
        """
        Verifica si una celda es una pared.
        
        Args:
            fila: Número de fila de la celda.
            columna: Número de columna de la celda.
            
        Returns:
            True si la celda es una pared, False en caso contrario.
        """
        # Verificar límites
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            return True
        
        return self.matriz[fila, columna] == 1
    
    def es_meta(self, fila: int, columna: int) -> bool:
        """
        Verifica si una celda es la meta.
        
        Args:
            fila: Número de fila de la celda.
            columna: Número de columna de la celda.
            
        Returns:
            True si la celda es la meta, False en caso contrario.
        """
        return (fila, columna) == self.meta
