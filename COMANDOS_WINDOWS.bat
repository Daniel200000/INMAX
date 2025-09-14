@echo off
echo ========================================
echo    Web Avisadores - Comandos Windows
echo ========================================
echo.

echo Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js no esta instalado
    echo.
    echo SOLUCION:
    echo 1. Ir a https://nodejs.org/
    echo 2. Descargar la version LTS
    echo 3. Instalar Node.js
    echo 4. Reiniciar esta ventana
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Node.js esta instalado
    node --version
)

echo.
echo Verificando npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: npm no esta disponible
    echo.
    echo SOLUCION:
    echo 1. Reinstalar Node.js
    echo 2. npm viene incluido con Node.js
    echo.
    pause
    exit /b 1
) else (
    echo ✅ npm esta disponible
    npm --version
)

echo.
echo Verificando carpeta del proyecto...
if not exist "frontend" (
    echo ❌ ERROR: No se encuentra la carpeta 'frontend'
    echo.
    echo SOLUCION:
    echo 1. Asegurate de estar en la carpeta correcta
    echo 2. La carpeta debe contener: frontend, backend, start-frontend.bat
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Carpeta 'frontend' encontrada
)

echo.
echo ========================================
echo    INICIANDO EL PROGRAMA
echo ========================================
echo.

echo Navegando a la carpeta frontend...
cd frontend

echo.
echo Instalando dependencias...
echo (Esto puede tomar unos minutos la primera vez)
npm install

if %errorlevel% neq 0 (
    echo ❌ ERROR: Fallo al instalar dependencias
    echo.
    echo SOLUCION:
    echo 1. Verificar conexion a internet
    echo 2. Ejecutar: npm cache clean --force
    echo 3. Intentar de nuevo
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Dependencias instaladas correctamente
)

echo.
echo Iniciando el servidor de desarrollo...
echo.
echo ========================================
echo    SERVIDOR INICIADO
echo ========================================
echo.
echo 🌐 Abre tu navegador en: http://localhost:3000
echo.
echo 📱 El programa esta funcionando!
echo.
echo ⚠️  IMPORTANTE:
echo - No cierres esta ventana
echo - Para detener el programa: Ctrl+C
echo - Si hay errores, revisa la consola del navegador (F12)
echo.

npm start
