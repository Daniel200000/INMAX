# 🚀 Desarrollo Frontend - Web Avisadores

## Inicio Rápido (Sin Docker)

### Prerrequisitos
- **Node.js** (versión 16 o superior)
- **npm** (viene con Node.js)

### Instalación y Ejecución

1. **Instalar Node.js**:
   - Descarga desde: https://nodejs.org/
   - Instala la versión LTS (recomendada)

2. **Ejecutar el proyecto**:
   ```bash
   # Opción 1: Script automático
   start-frontend.bat
   
   # Opción 2: Comandos manuales
   cd frontend
   npm install
   npm start
   ```

3. **Acceder a la aplicación**:
   - Abre tu navegador en: http://localhost:3000

## 🎨 Diseño Implementado

### ✅ **Header de 3 Niveles** (Según plantillas)
- **Barra superior oscura**: Título de la página
- **Barra azul clara**: Logo "Web Avisadores" 
- **Barra blanca**: Perfil de usuario y navegación

### ✅ **Sidebar Izquierdo** (Según plantillas)
- Menú hamburguesa
- Navegación principal con iconos
- Submenú de reportes expandible
- Diseño exacto de las plantillas

### ✅ **Botones Flotantes** (Según plantillas)
- Columna de botones en el lado derecho
- Email, Chat, Send, Archive, Star
- Posicionamiento fijo

### ✅ **Footer** (Según plantillas)
- Enlaces organizados en columnas
- Redes sociales
- Estructura exacta de las plantillas

## 📱 Funcionalidades del Dashboard

### **Datos Mock Incluidos**
- 5 campañas de ejemplo con datos realistas
- Diferentes estados (activa, pausada, finalizada, etc.)
- Métricas variadas para mostrar funcionalidad
- Ubicaciones geográficas reales

### **Componentes Funcionales**
- ✅ Búsqueda en tiempo real
- ✅ Filtros por estado y fecha
- ✅ Estadísticas con tendencias
- ✅ Gráficos interactivos
- ✅ Métricas de rendimiento
- ✅ Actividad reciente
- ✅ Acciones rápidas

## 🎯 Páginas Implementadas

1. **Dashboard** (`/`) - Vista principal con estadísticas
2. **Lista de Campañas** (`/campaigns`) - Lista de todas las campañas
3. **Crear Campaña** (`/campaigns/create`) - Formulario de creación
4. **Geolocalización** (`/geolocation`) - Mapa interactivo
5. **Configuración** (`/settings`) - Panel de configuración

## 🔧 Comandos Útiles

### Desarrollo
```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start

# Construir para producción
npm run build

# Ejecutar tests
npm test
```

### Limpieza
```bash
# Limpiar caché de npm
npm cache clean --force

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

## 🐛 Solución de Problemas

### Puerto 3000 ocupado
```bash
# Cambiar puerto
set PORT=3001
npm start
```

### Error de dependencias
```bash
# Limpiar e instalar
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Error de memoria
```bash
# Aumentar memoria de Node.js
set NODE_OPTIONS=--max_old_space_size=4096
npm start
```

## 📁 Estructura del Proyecto

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Layout/          # Header, Sidebar, Footer
│   │   ├── Dashboard/       # Componentes del dashboard
│   │   ├── Campaigns/       # Componentes de campañas
│   │   └── Common/          # Componentes comunes
│   ├── pages/               # Páginas principales
│   ├── services/            # Servicios de API
│   ├── data/                # Datos mock
│   ├── types/               # Tipos TypeScript
│   └── i18n/                # Internacionalización
├── package.json
└── README.md
```

## 🎨 Colores y Diseño

### Esquema de Colores (Según plantillas)
- **Azul Principal**: #4fd1c7 (Barra del header)
- **Azul Oscuro**: #2d3748 (Barra superior y footer)
- **Verde**: #48bb78 (Botones activos)
- **Gris**: #718096 (Textos secundarios)

### Características Visuales
- Diseño exacto de las plantillas proporcionadas
- Header de 3 niveles como se especificó
- Sidebar con menú hamburguesa
- Botones flotantes en el lado derecho
- Footer con enlaces organizados

## 🚀 Próximos Pasos

1. **Instalar Docker** para el backend completo
2. **Configurar base de datos** MongoDB
3. **Implementar autenticación** real
4. **Agregar más funcionalidades** según necesidades

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que Node.js esté instalado
2. Ejecuta `npm install` en la carpeta frontend
3. Revisa la consola del navegador para errores
4. Limpia el caché: `npm cache clean --force`

¡El frontend está listo para mostrar a tu jefe! 🎉
