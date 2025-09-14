@echo off
echo ========================================
echo    Web Avisadores - Frontend Development
echo ========================================
echo.
echo Iniciando el frontend en modo desarrollo...
echo.

REM Verificar si Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js no esta instalado
    echo Por favor instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar si npm está disponible
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm no esta disponible
    echo Por favor instala npm
    pause
    exit /b 1
)

echo Instalando dependencias...
cd frontend
npm install

echo.
echo Iniciando el servidor de desarrollo...
echo.
echo ========================================
echo    Servidor iniciado correctamente
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

npm start
