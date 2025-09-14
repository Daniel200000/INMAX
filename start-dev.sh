#!/bin/bash

echo "========================================"
echo "   Web Avisadores - Modulo de Campanas"
echo "========================================"
echo
echo "Iniciando el entorno de desarrollo..."
echo

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker no está instalado o no está en el PATH"
    echo "Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar si Docker Compose está disponible
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose no está disponible"
    echo "Por favor instala Docker Compose"
    exit 1
fi

echo "Creando archivo de configuración..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "Archivo .env creado desde env.example"
    echo "Por favor revisa y ajusta la configuración si es necesario"
    echo
fi

echo "Construyendo y ejecutando contenedores..."
docker-compose up --build -d

echo
echo "========================================"
echo "   Servicios iniciados correctamente"
echo "========================================"
echo
echo "Frontend (React): http://localhost:3000"
echo "Backend API:      http://localhost:8000"
echo "API Docs:         http://localhost:8000/docs"
echo "MongoDB Express:  http://localhost:8081"
echo
echo "Para ver los logs: docker-compose logs -f"
echo "Para detener:     docker-compose down"
echo
echo "Presiona Enter para abrir el navegador..."
read

# Abrir el navegador (funciona en macOS y Linux)
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
fi

echo
echo "¡Listo! El módulo de campañas está ejecutándose."
echo
