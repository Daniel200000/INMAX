# Módulo de Campañas - Red Social Inmax

## Descripción del Proyecto

Módulo especializado para la creación, gestión y monitoreo de campañas publicitarias con funcionalidades avanzadas de geolocalización para segmentación de audiencias.

## Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **MongoDB** - Base de datos NoSQL para datos de geolocalización
- **Redis** - Caché y sesiones
- **Docker** - Containerización
- **Pydantic** - Validación de datos

### Frontend
- **React 18** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Leaflet** - Mapas interactivos
- **React-Leaflet** - Integración React-Leaflet
- **Axios** - Cliente HTTP
- **React Hook Form** - Manejo de formularios

### Servicios Externos
- **AWS S3** - Almacenamiento de multimedia
- **Mapbox API** - Geocodificación y mapas avanzados

## Arquitectura del Proyecto

```
inmax-campaigns/
├── backend/                 # API Backend (FastAPI)
├── frontend/               # Aplicación React
├── docker-compose.yml      # Orquestación de servicios
├── .env.example           # Variables de entorno
└── README.md              # Documentación principal
```

## Instalación y Desarrollo

### Prerrequisitos
- Docker y Docker Compose
- Node.js 18+ (para desarrollo frontend)
- Python 3.11+ (para desarrollo backend)

### Desarrollo Local

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd inmax-campaigns
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Ejecutar con Docker Compose**
```bash
docker-compose up -d
```

4. **Acceder a la aplicación**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Funcionalidades del MVP

### Dashboard Principal
- Lista de campañas existentes
- Acceso rápido para crear nueva campaña
- Filtros y búsqueda

### Creación de Campañas
- Formulario con campos básicos
- Carga de archivos multimedia
- Componente de geolocalización interactivo
- Validación de datos

### Geolocalización
- Mapa interactivo con Leaflet
- Dibujo de áreas geográficas
- Selección de zonas específicas
- Colocación de pines de ubicación

## Estructura de la API

### Endpoints Principales
- `GET /api/v1/campaigns` - Listar campañas
- `POST /api/v1/campaigns` - Crear campaña
- `GET /api/v1/campaigns/{id}` - Obtener campaña
- `PUT /api/v1/campaigns/{id}` - Actualizar campaña
- `DELETE /api/v1/campaigns/{id}` - Eliminar campaña
- `POST /api/v1/campaigns/{id}/media` - Subir multimedia
- `GET /api/v1/geolocation/search` - Buscar ubicaciones

## Internacionalización (i18n)

El proyecto está preparado para múltiples idiomas:
- Español (es) - Idioma por defecto
- Inglés (en)
- Portugués (pt)

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
