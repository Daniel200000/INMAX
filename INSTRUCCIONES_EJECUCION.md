# 🚀 INSTRUCCIONES PASO A PASO - Web Avisadores

## 📋 **REQUISITOS PREVIOS**

### 1. **Instalar Node.js** (OBLIGATORIO)
- **Descargar**: https://nodejs.org/
- **Versión recomendada**: LTS (Long Term Support)
- **Verificar instalación**: Abrir CMD y escribir `node --version`
- **Debe mostrar**: v16.x.x o superior

### 2. **Verificar que npm esté instalado**
- **Abrir CMD** y escribir: `npm --version`
- **Debe mostrar**: 8.x.x o superior

---

## 🎯 **PASOS PARA EJECUTAR EL PROGRAMA**

### **PASO 1: Abrir la Consola (CMD)**

#### **En Windows:**
1. **Presionar**: `Windows + R`
2. **Escribir**: `cmd`
3. **Presionar**: `Enter`

#### **O desde el Explorador:**
1. **Navegar** a la carpeta del proyecto: `C:\Users\danie\Desktop\INMAX AVISADORES`
2. **Hacer clic derecho** en la carpeta
3. **Seleccionar**: "Abrir en terminal" o "Abrir ventana de comandos aquí"

---

### **PASO 2: Verificar que estás en la carpeta correcta**

En la consola, escribir:
```cmd
cd "C:\Users\danie\Desktop\INMAX AVISADORES"
dir
```

**Debes ver**:
- `frontend` (carpeta)
- `backend` (carpeta)
- `start-frontend.bat` (archivo)
- `docker-compose.yml` (archivo)

---

### **PASO 3: Ejecutar el programa**

#### **OPCIÓN A: Script Automático (RECOMENDADO)**
```cmd
start-frontend.bat
```

#### **OPCIÓN B: Comandos Manuales**
```cmd
cd frontend
npm install
npm start
```

---

### **PASO 4: Abrir el navegador**

1. **Abrir** cualquier navegador (Chrome, Firefox, Edge)
2. **Ir a**: http://localhost:3000
3. **¡Listo!** El programa debe estar funcionando

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Error: "node no se reconoce"**
- **Problema**: Node.js no está instalado
- **Solución**: Instalar Node.js desde https://nodejs.org/
- **Reiniciar** la consola después de instalar

### **Error: "npm no se reconoce"**
- **Problema**: npm no está disponible
- **Solución**: Reinstalar Node.js (npm viene incluido)

### **Error: "Puerto 3000 en uso"**
- **Problema**: Otro programa usa el puerto 3000
- **Solución**: Cerrar otros programas o cambiar puerto
- **Comando**: `set PORT=3001 && npm start`

### **Error: "No se puede encontrar el módulo"**
- **Problema**: Dependencias no instaladas
- **Solución**: 
  ```cmd
  cd frontend
  npm install
  npm start
  ```

### **Pantalla en blanco**
- **Problema**: Error de JavaScript
- **Solución**: 
  1. Abrir **F12** (Herramientas de desarrollador)
  2. Ir a la pestaña **Console**
  3. Ver los errores y reportarlos

---

## 📱 **FUNCIONALIDADES DEL PROGRAMA**

### **Dashboard Principal**
- ✅ **Búsqueda**: Escribe en la barra de búsqueda
- ✅ **Filtros**: Haz clic en el botón "Filtros"
- ✅ **Estadísticas**: Observa las tarjetas con números
- ✅ **Gráficos**: Ve el gráfico de rendimiento
- ✅ **Campañas**: Navega por las campañas de ejemplo

### **Navegación**
- ✅ **Sidebar**: Menú lateral con opciones
- ✅ **Header**: 3 niveles según las plantillas
- ✅ **Botones flotantes**: Columna derecha
- ✅ **Footer**: Enlaces organizados

---

## 🎨 **DISEÑO IMPLEMENTADO**

### **Colores Exactos de las Plantillas**
- **Azul Claro**: #4fd1c7 (Barra del header)
- **Azul Oscuro**: #2d3748 (Barra superior y footer)
- **Verde**: #48bb78 (Botones activos)
- **Gris**: #718096 (Textos secundarios)

### **Estructura del Header (3 Niveles)**
1. **Barra superior oscura**: Título + badges "Enabled"
2. **Barra azul clara**: Logo "Web Avisadores"
3. **Barra blanca**: Perfil + navegación

---

## 📁 **ESTRUCTURA DEL PROYECTO**

```
INMAX AVISADORES/
├── frontend/                 # Aplicación React
│   ├── src/
│   │   ├── components/       # Componentes reutilizables
│   │   │   ├── Layout/       # Header, Sidebar, Footer
│   │   │   ├── Dashboard/    # Componentes del dashboard
│   │   │   └── Campaigns/    # Componentes de campañas
│   │   ├── pages/            # Páginas principales
│   │   ├── services/         # Servicios de API
│   │   ├── data/             # Datos mock
│   │   └── types/            # Tipos TypeScript
│   ├── package.json          # Dependencias
│   └── public/               # Archivos públicos
├── backend/                  # API Python (opcional)
├── start-frontend.bat        # Script de inicio
└── README.md                 # Documentación
```

---

## 🚀 **COMANDOS ÚTILES**

### **Desarrollo**
```cmd
# Instalar dependencias
npm install

# Iniciar servidor
npm start

# Construir para producción
npm run build

# Ver versión de Node.js
node --version

# Ver versión de npm
npm --version
```

### **Limpieza**
```cmd
# Limpiar caché
npm cache clean --force

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

---

## 📞 **SOPORTE**

### **Si algo no funciona:**
1. **Verificar** que Node.js esté instalado
2. **Revisar** que estés en la carpeta correcta
3. **Ejecutar** `npm install` en la carpeta frontend
4. **Abrir** F12 en el navegador para ver errores
5. **Reiniciar** la consola y el navegador

### **Contacto:**
- **Desarrollador**: Asistente AI
- **Proyecto**: Web Avisadores - Módulo de Campañas
- **Versión**: 1.0.0

---

## ✅ **CHECKLIST DE VERIFICACIÓN**

- [ ] Node.js instalado (`node --version`)
- [ ] npm disponible (`npm --version`)
- [ ] Consola abierta en la carpeta correcta
- [ ] Comando `start-frontend.bat` ejecutado
- [ ] Navegador abierto en http://localhost:3000
- [ ] Dashboard cargado correctamente
- [ ] Diseño coincide con las plantillas

**¡Si todos los puntos están marcados, el programa está funcionando correctamente!** 🎉
