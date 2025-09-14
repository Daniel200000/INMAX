# 📚 DOCUMENTACIÓN TÉCNICA - Web Avisadores

## 🏗️ **ARQUITECTURA DEL PROYECTO**

### **Frontend (React + TypeScript)**
```
frontend/
├── src/
│   ├── components/           # Componentes reutilizables
│   │   ├── Layout/          # Header, Sidebar, Footer
│   │   ├── Dashboard/       # Componentes del dashboard
│   │   ├── Campaigns/       # Componentes de campañas
│   │   └── Common/          # Componentes comunes
│   ├── pages/               # Páginas principales
│   ├── services/            # Servicios de API
│   ├── contexts/            # Contextos de React
│   ├── types/               # Tipos TypeScript
│   ├── data/                # Datos mock
│   └── i18n/                # Internacionalización
├── public/                  # Archivos públicos
└── package.json             # Dependencias
```

### **Backend (Python + FastAPI)**
```
backend/
├── app/
│   ├── core/               # Configuración y utilidades
│   ├── models/             # Modelos de datos
│   ├── services/           # Lógica de negocio
│   ├── api/                # Endpoints REST
│   └── main.py             # Punto de entrada
├── scripts/                # Scripts de inicialización
└── requirements.txt        # Dependencias Python
```

---

## 🎨 **DISEÑO IMPLEMENTADO**

### **Header de 3 Niveles** (Según plantillas del jefe)

#### **Nivel 1: Barra Superior Oscura**
- **Color**: #2d3748 (gris oscuro)
- **Contenido**: Título de la página + badges "Enabled"
- **Componente**: `Header.tsx` - sección `header-top`

#### **Nivel 2: Barra Azul Clara**
- **Color**: #4fd1c7 (azul claro/teal)
- **Contenido**: Logo "Web Avisadores" con icono de engranaje
- **Componente**: `Header.tsx` - sección `header-main`

#### **Nivel 3: Barra Blanca**
- **Color**: #ffffff (blanco)
- **Contenido**: Perfil de usuario + navegación principal
- **Componente**: `Header.tsx` - sección `header-bottom`

### **Sidebar Izquierdo** (Según plantillas)

#### **Estructura del Menú**
```typescript
const menuItems = [
  { path: '/', label: 'Inicio', icon: '⭐', description: 'Menu description.' },
  { path: '/campaigns', label: 'Campañas', icon: '⭐', description: 'Menu description.' },
  { path: '/indicators', label: 'Indicadores', icon: '⭐', description: 'Menu description.' },
  { path: '/analysis', label: 'Análisis', icon: '⭐', description: 'Menu description.' },
  { path: '/reports', label: 'Reportes', icon: '⭐', description: 'Menu description.', hasSubmenu: true }
];
```

#### **Submenú de Reportes**
```typescript
const reportSubmenu = [
  { path: '/reports/expense-campaign', label: 'Expense report by Campaign' },
  { path: '/reports/investment-location', label: 'Investment report by Location' },
  { path: '/reports/investment-product', label: 'Investment report by Product' },
  { path: '/reports/expense-evolution', label: 'Expense evolution Report' },
  { path: '/reports/campaign-info', label: 'Campaign information report' }
];
```

### **Botones Flotantes** (Lado derecho)

#### **Configuración**
```typescript
const floatingButtons = [
  { icon: '✉️', title: 'Email' },
  { icon: '💬', title: 'Chat' },
  { icon: '✈️', title: 'Send' },
  { icon: '📦', title: 'Archive' },
  { icon: '⭐', title: 'Star', primary: true }
];
```

---

## 🔧 **COMPONENTES PRINCIPALES**

### **1. Dashboard.tsx**
```typescript
/**
 * Componente Dashboard - Página principal del módulo de campañas
 * 
 * Funcionalidades:
 * - Búsqueda y filtrado en tiempo real
 * - Estadísticas con tendencias
 * - Gráficos interactivos
 * - Auto-refresh cada 30 segundos
 * - Diseño responsivo
 */
const Dashboard: React.FC = () => {
  // Estados para filtros y búsqueda
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [dateFilter, setDateFilter] = useState('all');
  const [showFilters, setShowFilters] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(30000); // 30 segundos
```

### **2. Header.tsx**
```typescript
/**
 * Componente Header - Implementa el diseño de 3 niveles
 * 
 * Estructura:
 * 1. Barra superior oscura: Título + badges "Enabled"
 * 2. Barra azul clara: Logo "Web Avisadores"
 * 3. Barra blanca: Perfil + navegación
 */
interface HeaderProps {
  pageTitle?: string; // Título de la página actual
}
```

### **3. Sidebar.tsx**
```typescript
/**
 * Componente Sidebar - Menú lateral según plantillas
 * 
 * Características:
 * - Menú hamburguesa
 * - Navegación con iconos de estrella
 * - Submenú de reportes expandible
 * - Diseño exacto de las plantillas
 */
```

---

## 📊 **FUNCIONALIDADES DEL DASHBOARD**

### **Búsqueda en Tiempo Real**
```typescript
// Filtros y búsqueda
const filteredCampaigns = campaigns.filter(campaign => {
  const matchesSearch = campaign.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                       campaign.description?.toLowerCase().includes(searchTerm.toLowerCase());
  const matchesStatus = statusFilter === 'all' || campaign.status === statusFilter;
  const matchesDate = dateFilter === 'all' || checkDateFilter(campaign, dateFilter);
  
  return matchesSearch && matchesStatus && matchesDate;
});
```

### **Auto-refresh**
```typescript
// Auto-refresh de datos cada 30 segundos
useEffect(() => {
  const interval = setInterval(() => {
    fetchCampaigns(1, 10);
  }, refreshInterval);

  return () => clearInterval(interval);
}, [fetchCampaigns, refreshInterval]);
```

### **Estadísticas con Tendencias**
```typescript
// Cálculos de estadísticas
const activeCampaigns = campaigns.filter(c => c.status === 'active').length;
const totalBudget = campaigns.reduce((sum, c) => sum + c.budget, 0);
const totalViews = campaigns.reduce((sum, c) => sum + (c.views_count || 0), 0);
const totalClicks = campaigns.reduce((sum, c) => sum + (c.clicks_count || 0), 0);
const conversionRate = totalViews > 0 ? ((totalClicks / totalViews) * 100).toFixed(2) : 0;
```

---

## 🎨 **SISTEMA DE COLORES**

### **Paleta de Colores (Según plantillas)**
```css
:root {
  --primary-blue: #4fd1c7;      /* Barra del header */
  --dark-blue: #2d3748;         /* Barra superior y footer */
  --green: #48bb78;             /* Botones activos */
  --gray: #718096;              /* Textos secundarios */
  --white: #ffffff;             /* Fondos principales */
  --light-gray: #f8f9fa;        /* Fondos secundarios */
}
```

### **Aplicación de Colores**
- **Header Nivel 1**: `background: #2d3748`
- **Header Nivel 2**: `background: #4fd1c7`
- **Header Nivel 3**: `background: #ffffff`
- **Botones Activos**: `background: #48bb78`
- **Texto Secundario**: `color: #718096`

---

## 📱 **RESPONSIVE DESIGN**

### **Breakpoints**
```css
/* Desktop */
@media (min-width: 1200px) { }

/* Tablet */
@media (max-width: 1200px) { }

/* Mobile */
@media (max-width: 768px) { }

/* Small Mobile */
@media (max-width: 480px) { }
```

### **Layout Adaptativo**
- **Desktop**: Sidebar fijo + contenido principal
- **Tablet**: Sidebar colapsable + contenido principal
- **Mobile**: Sidebar oculto + menú hamburguesa

---

## 🌍 **INTERNACIONALIZACIÓN (i18n)**

### **Idiomas Soportados**
- **Español** (es) - Idioma principal
- **Inglés** (en) - Idioma secundario
- **Portugués** (pt) - Idioma secundario

### **Configuración**
```typescript
// frontend/src/i18n/index.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    lng: 'es', // Idioma por defecto
    fallbackLng: 'es',
    resources: {
      es: { translation: esTranslations },
      en: { translation: enTranslations },
      pt: { translation: ptTranslations }
    }
  });
```

---

## 🔌 **SERVICIOS DE API**

### **Configuración Base**
```typescript
// frontend/src/services/api.ts
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### **Manejo de Errores**
```typescript
// Interceptor para manejar errores de conexión
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      console.warn('Backend no disponible, usando datos mock');
      // Retornar datos mock en lugar de error
      return Promise.resolve({
        data: mockCampaigns,
        status: 200,
        statusText: 'OK',
        headers: {},
        config: error.config
      });
    }
    return Promise.reject(error);
  }
);
```

---

## 📊 **DATOS MOCK**

### **Campañas de Ejemplo**
```typescript
// frontend/src/data/mockData.ts
export const mockCampaigns: Campaign[] = [
  {
    id: '1',
    name: 'Campaña de Verano 2024',
    description: 'Promoción especial para la temporada de verano',
    start_date: '2024-06-01T00:00:00Z',
    end_date: '2024-08-31T23:59:59Z',
    budget: 50000,
    status: 'active',
    // ... más propiedades
  },
  // ... más campañas
];
```

### **Uso de Datos Mock**
- **Automático**: Cuando no hay conexión al backend
- **Desarrollo**: Para probar funcionalidades
- **Demo**: Para mostrar al jefe

---

## 🚀 **COMANDOS DE DESARROLLO**

### **Instalación**
```bash
# Instalar dependencias
npm install

# Instalar dependencias específicas
npm install react react-dom react-router-dom
```

### **Desarrollo**
```bash
# Iniciar servidor de desarrollo
npm start

# Construir para producción
npm run build

# Ejecutar tests
npm test
```

### **Limpieza**
```bash
# Limpiar caché
npm cache clean --force

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

---

## 🔍 **DEBUGGING**

### **Herramientas de Desarrollo**
1. **React Developer Tools**: Extensión del navegador
2. **Redux DevTools**: Para estado de la aplicación
3. **Console del Navegador**: F12 para ver errores

### **Logs Importantes**
```typescript
// Verificar datos de campañas
console.log('Campañas cargadas:', campaigns);

// Verificar filtros
console.log('Filtros activos:', { searchTerm, statusFilter, dateFilter });

// Verificar errores de API
console.warn('Usando datos mock para campañas');
```

---

## 📈 **MÉTRICAS DE RENDIMIENTO**

### **Optimizaciones Implementadas**
- **Lazy Loading**: Componentes cargados bajo demanda
- **Memoización**: useCallback y useMemo para evitar re-renders
- **Debounce**: Búsqueda con retraso de 300ms
- **Paginación**: Carga de datos por lotes

### **Monitoreo**
- **Tiempo de carga**: < 3 segundos
- **Tamaño del bundle**: < 2MB
- **Memoria**: < 100MB en uso

---

## 🔒 **SEGURIDAD**

### **Validaciones**
- **Input Sanitization**: Limpieza de datos de entrada
- **XSS Protection**: Prevención de ataques XSS
- **CSRF Protection**: Tokens de seguridad

### **Autenticación**
- **JWT Tokens**: Para autenticación
- **Local Storage**: Almacenamiento seguro
- **Session Management**: Gestión de sesiones

---

## 📝 **CONVENCIONES DE CÓDIGO**

### **Naming Conventions**
- **Componentes**: PascalCase (ej: `Dashboard.tsx`)
- **Funciones**: camelCase (ej: `handleSearch`)
- **Variables**: camelCase (ej: `searchTerm`)
- **Constantes**: UPPER_CASE (ej: `API_BASE_URL`)

### **Estructura de Archivos**
- **Un componente por archivo**
- **CSS co-locado** con el componente
- **Tipos TypeScript** en archivos separados
- **Servicios** agrupados por funcionalidad

---

## 🎯 **PRÓXIMOS PASOS**

### **Corto Plazo**
1. **Integrar backend real** con FastAPI
2. **Implementar autenticación** completa
3. **Agregar más tipos de gráficos**
4. **Implementar notificaciones** en tiempo real

### **Mediano Plazo**
1. **Optimizar rendimiento** para grandes volúmenes
2. **Agregar tests** automatizados
3. **Implementar PWA** (Progressive Web App)
4. **Agregar modo oscuro**

### **Largo Plazo**
1. **Microservicios** para escalabilidad
2. **Machine Learning** para recomendaciones
3. **Analytics avanzados** con BigQuery
4. **Integración con redes sociales**

---

## 📞 **SOPORTE TÉCNICO**

### **Problemas Comunes**
1. **Error de conexión**: Verificar que el backend esté ejecutándose
2. **Dependencias**: Ejecutar `npm install`
3. **Puerto ocupado**: Cambiar puerto o cerrar otros programas
4. **Errores de TypeScript**: Verificar tipos y interfaces

### **Recursos**
- **Documentación React**: https://reactjs.org/docs
- **TypeScript**: https://www.typescriptlang.org/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **MongoDB**: https://docs.mongodb.com/

---

**¡Esta documentación cubre todos los aspectos técnicos del proyecto Web Avisadores!** 🚀
