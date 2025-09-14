# Guía de Desarrollo - Módulo de Campañas Inmax

## Configuración del Entorno de Desarrollo

### Prerrequisitos
- Docker y Docker Compose
- Node.js 18+ (para desarrollo frontend)
- Python 3.11+ (para desarrollo backend)
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd inmax-campaigns
```

2. **Configurar variables de entorno**
```bash
cp env.example .env
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

## Estructura del Proyecto

```
inmax-campaigns/
├── backend/                 # API Backend (FastAPI)
│   ├── app/
│   │   ├── core/           # Configuración y utilidades
│   │   ├── models/         # Modelos de datos
│   │   ├── services/       # Lógica de negocio
│   │   ├── api/            # Endpoints de la API
│   │   └── main.py         # Punto de entrada
│   ├── scripts/            # Scripts de inicialización
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Aplicación React
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── pages/          # Páginas de la aplicación
│   │   ├── contexts/       # Gestión de estado
│   │   ├── services/       # Servicios de API
│   │   ├── types/          # Definiciones TypeScript
│   │   └── i18n/           # Internacionalización
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml      # Orquestación de servicios
├── env.example            # Variables de entorno
└── README.md
```

## Desarrollo Backend

### Estructura de Archivos

#### Modelos (Pydantic)
```python
# app/models/campaign.py
class Campaign(BaseModel):
    id: str
    name: str
    budget: float
    # ... más campos
```

#### Servicios
```python
# app/services/campaign_service.py
class CampaignService:
    async def create_campaign(self, data: CampaignCreate) -> Campaign:
        # Lógica de negocio
        pass
```

#### Endpoints
```python
# app/api/v1/endpoints/campaigns.py
@router.post("/", response_model=Campaign)
async def create_campaign(campaign_data: CampaignCreate):
    # Lógica del endpoint
    pass
```

### Comandos Útiles

```bash
# Ejecutar tests
docker-compose exec backend pytest

# Ver logs del backend
docker-compose logs -f backend

# Acceder al shell del contenedor
docker-compose exec backend bash

# Reiniciar solo el backend
docker-compose restart backend
```

## Desarrollo Frontend

### Estructura de Componentes

#### Componentes de Página
```typescript
// src/pages/Dashboard.tsx
const Dashboard: React.FC = () => {
  const { campaigns, fetchCampaigns } = useCampaign();
  // Lógica del componente
};
```

#### Componentes Reutilizables
```typescript
// src/components/Campaigns/CampaignCard.tsx
interface CampaignCardProps {
  campaign: Campaign;
  showActions?: boolean;
}
```

#### Contextos
```typescript
// src/contexts/CampaignContext.tsx
export const CampaignProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // Lógica del contexto
};
```

### Comandos Útiles

```bash
# Instalar dependencias
cd frontend && npm install

# Ejecutar en modo desarrollo
cd frontend && npm start

# Ejecutar tests
cd frontend && npm test

# Construir para producción
cd frontend && npm run build

# Ver logs del frontend
docker-compose logs -f frontend
```

## Base de Datos

### MongoDB

#### Conexión
```python
# app/core/database.py
async def connect_to_mongo():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGO_DATABASE]
```

#### Colecciones
- `users`: Información de usuarios
- `campaigns`: Datos de campañas
- `media_files`: Archivos multimedia
- `locations`: Ubicaciones geográficas

#### Índices
```javascript
// backend/scripts/mongo-init.js
db.campaigns.createIndex({ "user_id": 1 });
db.campaigns.createIndex({ "target_locations": "2dsphere" });
```

### Redis

#### Configuración
```python
# app/core/redis_client.py
redis_client = redis.from_url(settings.REDIS_URL)
```

#### Uso
```python
# Caché de datos
await cache.set("key", data, expire=3600)
cached_data = await cache.get("key")
```

## API Endpoints

### Autenticación
- `POST /api/v1/users/register` - Registro de usuario
- `POST /api/v1/users/login` - Inicio de sesión
- `GET /api/v1/users/me` - Información del usuario actual

### Campañas
- `GET /api/v1/campaigns` - Listar campañas
- `POST /api/v1/campaigns` - Crear campaña
- `GET /api/v1/campaigns/{id}` - Obtener campaña
- `PUT /api/v1/campaigns/{id}` - Actualizar campaña
- `DELETE /api/v1/campaigns/{id}` - Eliminar campaña

### Multimedia
- `POST /api/v1/media/upload` - Subir archivo
- `GET /api/v1/media` - Listar archivos
- `DELETE /api/v1/media/{id}` - Eliminar archivo

### Geolocalización
- `GET /api/v1/geolocation/search` - Buscar ubicaciones
- `POST /api/v1/geolocation/reverse` - Geocodificación inversa
- `POST /api/v1/geolocation/validate` - Validar ubicación

## Testing

### Backend
```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_campaigns.py
```

### Frontend
```bash
# Ejecutar tests
npm test

# Tests con cobertura
npm run test:coverage

# Tests en modo watch
npm run test:watch
```

## Internacionalización

### Agregar Nuevo Idioma

1. **Crear archivo de traducción**
```json
// src/i18n/locales/fr.json
{
  "common": {
    "loading": "Chargement...",
    "error": "Erreur"
  }
}
```

2. **Registrar en i18n**
```typescript
// src/i18n/index.ts
import fr from './locales/fr.json';

const resources = {
  es: { translation: es },
  en: { translation: en },
  pt: { translation: pt },
  fr: { translation: fr }
};
```

3. **Usar en componentes**
```typescript
const { t } = useTranslation();
return <h1>{t('common.loading')}</h1>;
```

## Despliegue

### Desarrollo Local
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Producción
```bash
# Construir imágenes
docker-compose build

# Ejecutar en producción
docker-compose -f docker-compose.prod.yml up -d
```

## Debugging

### Backend
```python
# Agregar breakpoints
import pdb; pdb.set_trace()

# Logging
logger.info("Debug info", extra={"data": data})
```

### Frontend
```typescript
// Console logs
console.log("Debug info", data);

// React DevTools
// Usar extensión del navegador
```

### Base de Datos
```bash
# Conectar a MongoDB
docker-compose exec mongodb mongo

# Ver colecciones
show collections

# Consultar datos
db.campaigns.find().pretty()
```

## Mejores Prácticas

### Código
- **TypeScript**: Usar tipos estrictos
- **ESLint**: Seguir reglas de linting
- **Prettier**: Formateo consistente
- **Commits**: Mensajes descriptivos

### Git
```bash
# Branch naming
feature/campaign-creation
bugfix/login-error
hotfix/security-patch

# Commit messages
feat: add campaign creation form
fix: resolve login validation error
docs: update API documentation
```

### Performance
- **Lazy Loading**: Cargar componentes bajo demanda
- **Memoización**: Usar React.memo y useMemo
- **Debouncing**: Para búsquedas y filtros
- **Paginación**: Para listas grandes

## Troubleshooting

### Problemas Comunes

#### Backend no inicia
```bash
# Ver logs
docker-compose logs backend

# Verificar puertos
netstat -tulpn | grep :8000

# Reconstruir imagen
docker-compose build --no-cache backend
```

#### Frontend no carga
```bash
# Verificar dependencias
cd frontend && npm install

# Limpiar caché
npm start -- --reset-cache

# Verificar proxy
# package.json: "proxy": "http://localhost:8000"
```

#### Base de datos no conecta
```bash
# Verificar MongoDB
docker-compose logs mongodb

# Verificar variables de entorno
docker-compose exec backend env | grep MONGO

# Reiniciar MongoDB
docker-compose restart mongodb
```

## Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Leaflet Documentation](https://leafletjs.com/)
