@echo off
echo ========================================
echo    Web Avisadores - Verificador de Errores
echo ========================================
echo.

echo 🔍 Verificando el sistema...
echo.

echo 1. Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js NO instalado
    echo    SOLUCION: Instalar desde https://nodejs.org/
) else (
    echo ✅ Node.js OK
    node --version
)

echo.
echo 2. Verificando npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm NO disponible
    echo    SOLUCION: Reinstalar Node.js
) else (
    echo ✅ npm OK
    npm --version
)

echo.
echo 3. Verificando carpeta del proyecto...
if not exist "frontend" (
    echo ❌ Carpeta 'frontend' NO encontrada
    echo    SOLUCION: Ejecutar desde la carpeta correcta
) else (
    echo ✅ Carpeta 'frontend' OK
)

echo.
echo 4. Verificando archivos del proyecto...
if not exist "frontend\package.json" (
    echo ❌ package.json NO encontrado
    echo    SOLUCION: Verificar que el proyecto este completo
) else (
    echo ✅ package.json OK
)

if not exist "frontend\src" (
    echo ❌ Carpeta 'src' NO encontrada
    echo    SOLUCION: Verificar que el proyecto este completo
) else (
    echo ✅ Carpeta 'src' OK
)

echo.
echo 5. Verificando puerto 3000...
netstat -an | findstr :3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Puerto 3000 en uso
    echo    SOLUCION: Cerrar otros programas o usar puerto diferente
) else (
    echo ✅ Puerto 3000 disponible
)

echo.
echo 6. Verificando conexion a internet...
ping -n 1 google.com >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Sin conexion a internet
    echo    SOLUCION: Verificar conexion para instalar dependencias
) else (
    echo ✅ Conexion a internet OK
)

echo.
echo ========================================
echo    RESUMEN DE VERIFICACION
echo ========================================
echo.

echo Si todos los elementos muestran ✅, el programa deberia funcionar.
echo Si hay ❌, sigue las soluciones indicadas.
echo Si hay ⚠️, son advertencias que pueden causar problemas.

echo.
echo Para ejecutar el programa:
echo 1. Ejecutar: start-frontend.bat
echo 2. O ejecutar: COMANDOS_WINDOWS.bat
echo 3. Abrir navegador en: http://localhost:3000

echo.
pause
