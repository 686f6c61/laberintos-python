#!/bin/bash

#######################################################
# Script de inicialización para el Generador de Laberintos
# Autor: github.com/686f6c61
# Versión: 0.2 - Noviembre 2025
#
# Este script automatiza el proceso de configuración del entorno
# y ejecución del juego, garantizando que todas las dependencias
# estén correctamente instaladas y gestionando posibles instancias
# duplicadas del proceso.
#######################################################

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado.${NC}"
    echo "Por favor, instálalo con: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

# Obtener directorio del script (para ejecutar desde cualquier ubicación)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Eliminar entorno virtual corrupto si existe y hay problemas
if [ -d ".venv" ] && [ ! -f ".venv/bin/activate" ]; then
    echo -e "${YELLOW}Entorno virtual corrupto detectado. Recreando...${NC}"
    rm -rf .venv
fi

# Crear un entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo -e "${GREEN}Creando entorno virtual...${NC}"
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error al crear el entorno virtual.${NC}"
        echo "Intenta instalar: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activar el entorno virtual
echo -e "${GREEN}Activando entorno virtual...${NC}"
source .venv/bin/activate

# Actualizar pip primero (evita warnings y problemas de compatibilidad)
echo -e "${GREEN}Actualizando pip...${NC}"
pip install --upgrade pip -q

# Instalar dependencias
echo -e "${GREEN}Instalando dependencias...${NC}"
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo -e "${RED}Error al instalar dependencias.${NC}"
    echo "Si pygame falla, intenta instalar las dependencias del sistema:"
    echo "  sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev"
    echo ""
    echo "Luego ejecuta: pip install pygame"
    exit 1
fi

# Verificar si el juego ya se está ejecutando
PROCESO=$(pgrep -f "python3 src/main.py" || true)
if [ -n "$PROCESO" ]; then
    echo -e "${YELLOW}El juego ya está en ejecución. Terminando proceso anterior...${NC}"
    kill $PROCESO 2>/dev/null
    sleep 1
fi

# Ejecutar el juego
echo -e "${GREEN}Iniciando el generador de laberintos...${NC}"
echo ""
python3 src/main.py
