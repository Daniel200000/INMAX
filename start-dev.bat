@echo off
echo ========================================
echo    Web Avisadores - Modulo de Campanas
echo ========================================
echo.
echo Iniciando el entorno de desarrollo...
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker no esta instalado o no esta en el PATH
    echo Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Verificar si Docker Compose está disponible
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose no esta disponible
    echo Por favor instala Docker Compose
    pause
    exit /b 1
)

echo Creando archivo de configuracion...
if not exist .env (
    copy env.example .env
    echo Archivo .env creado desde env.example
    echo Por favor revisa y ajusta la configuracion si es necesario
    echo.
)

echo Construyendo y ejecutando contenedores...
docker-compose up --build -d

echo.
echo ========================================
echo    Servicios iniciados correctamente
echo ========================================
echo.
echo Frontend (React): http://localhost:3000
echo Backend API:      http://localhost:8000
echo API Docs:         http://localhost:8000/docs
echo MongoDB Express:  http://localhost:8081
echo.
echo Para ver los logs: docker-compose logs -f
echo Para detener:     docker-compose down
echo.
echo Presiona cualquier tecla para abrir el navegador...
pause >nul

REM Abrir el navegador
start http://localhost:3000

echo.
echo ¡Listo! El modulo de campanas esta ejecutandose.
echo.
