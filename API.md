# API Documentation - Módulo de Campañas Inmax

## Información General

- **Base URL**: `http://localhost:8000/api/v1`
- **Autenticación**: Bearer Token (JWT)
- **Formato**: JSON
- **Versión**: 1.0.0

## Autenticación

### Headers Requeridos
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Obtener Token
```http
POST /api/v1/users/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "contraseña"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## Endpoints de Usuarios

### Registro de Usuario
```http
POST /api/v1/users/register
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "usuario@ejemplo.com",
  "password": "contraseña_segura",
  "full_name": "Nombre Completo"
}
```

**Respuesta:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "username": "nuevo_usuario",
  "email": "usuario@ejemplo.com",
  "full_name": "Nombre Completo",
  "role": "creator",
  "status": "active",
  "language": "es",
  "timezone": "UTC",
  "created_at": "2024-01-01T00:00:00Z",
  "is_verified": false
}
```

### Información del Usuario Actual
```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "username": "usuario",
  "email": "usuario@ejemplo.com",
  "full_name": "Nombre Completo",
  "role": "creator",
  "status": "active",
  "language": "es",
  "timezone": "UTC",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z",
  "is_verified": true
}
```

### Actualizar Perfil
```http
PUT /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "Nuevo Nombre",
  "language": "en",
  "timezone": "America/New_York"
}
```

## Endpoints de Campañas

### Listar Campañas
```http
GET /api/v1/campaigns?page=1&size=10&status=active&search=marketing
Authorization: Bearer <token>
```

**Parámetros de Query:**
- `page` (int): Número de página (default: 1)
- `size` (int): Tamaño de página (default: 10, max: 100)
- `status` (string): Filtrar por estado (draft, active, paused, finished, cancelled)
- `search` (string): Buscar por nombre

**Respuesta:**
```json
{
  "campaigns": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Campaña de Marketing",
      "description": "Descripción de la campaña",
      "budget": 5000.00,
      "channel": "social_media",
      "start_date": "2024-01-01T00:00:00Z",
      "end_date": "2024-01-31T23:59:59Z",
      "status": "active",
      "priority": "high",
      "target_locations": [
        {
          "type": "point",
          "coordinates": [-3.7038, 40.4168],
          "name": "Madrid",
          "address": "Madrid, España"
        }
      ],
      "media_files": ["507f1f77bcf86cd799439012"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "views_count": 1250,
      "clicks_count": 45,
      "conversions_count": 8
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### Crear Campaña
```http
POST /api/v1/campaigns
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Nueva Campaña",
  "description": "Descripción de la campaña",
  "budget": 3000.00,
  "channel": "display",
  "start_date": "2024-02-01T00:00:00Z",
  "end_date": "2024-02-28T23:59:59Z",
  "priority": "medium",
  "demographics": {
    "age": "25-35",
    "gender": "all",
    "interests": ["technology", "business"]
  },
  "target_locations": [
    {
      "type": "point",
      "coordinates": [-3.7038, 40.4168],
      "name": "Madrid",
      "address": "Madrid, España"
    }
  ],
  "media_files": []
}
```

**Respuesta:**
```json
{
  "id": "507f1f77bcf86cd799439013",
  "name": "Nueva Campaña",
  "description": "Descripción de la campaña",
  "budget": 3000.00,
  "channel": "display",
  "start_date": "2024-02-01T00:00:00Z",
  "end_date": "2024-02-28T23:59:59Z",
  "user_id": "507f1f77bcf86cd799439011",
  "status": "draft",
  "priority": "medium",
  "target_locations": [...],
  "media_files": [],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "views_count": 0,
  "clicks_count": 0,
  "conversions_count": 0
}
```

### Obtener Campaña
```http
GET /api/v1/campaigns/{campaign_id}
Authorization: Bearer <token>
```

### Actualizar Campaña
```http
PUT /api/v1/campaigns/{campaign_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Campaña Actualizada",
  "budget": 4000.00,
  "status": "active"
}
```

### Eliminar Campaña
```http
DELETE /api/v1/campaigns/{campaign_id}
Authorization: Bearer <token>
```

### Actualizar Estado de Campaña
```http
PATCH /api/v1/campaigns/{campaign_id}/status
Authorization: Bearer <token>
Content-Type: application/json

{
  "new_status": "active"
}
```

### Estadísticas de Campaña
```http
GET /api/v1/campaigns/{campaign_id}/stats
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "campaign_id": "507f1f77bcf86cd799439011",
  "views": 1250,
  "clicks": 45,
  "conversions": 8,
  "ctr": 3.6,
  "conversion_rate": 17.78,
  "cost_per_click": 111.11,
  "cost_per_conversion": 625.00,
  "total_spent": 5000.00,
  "last_updated": "2024-01-01T12:00:00Z"
}
```

## Endpoints de Multimedia

### Subir Archivo
```http
POST /api/v1/media/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <archivo>
campaign_id: "507f1f77bcf86cd799439011"
file_type: "image"
```

**Respuesta:**
```json
{
  "file_id": "507f1f77bcf86cd799439014",
  "filename": "imagen_123.jpg",
  "url": "https://s3.amazonaws.com/bucket/imagen_123.jpg",
  "status": "uploading",
  "message": "File uploaded successfully, processing started"
}
```

### Listar Archivos
```http
GET /api/v1/media?campaign_id=507f1f77bcf86cd799439011&file_type=image&page=1&size=10
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "files": [
    {
      "id": "507f1f77bcf86cd799439014",
      "filename": "imagen_123.jpg",
      "original_filename": "mi_imagen.jpg",
      "file_type": "image",
      "mime_type": "image/jpeg",
      "size": 1024000,
      "url": "https://s3.amazonaws.com/bucket/imagen_123.jpg",
      "thumbnail_url": "https://s3.amazonaws.com/bucket/thumb_imagen_123.jpg",
      "status": "ready",
      "upload_date": "2024-01-01T00:00:00Z",
      "processed_date": "2024-01-01T00:01:00Z",
      "user_id": "507f1f77bcf86cd799439011",
      "campaign_id": "507f1f77bcf86cd799439011"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### Eliminar Archivo
```http
DELETE /api/v1/media/{file_id}
Authorization: Bearer <token>
```

### Estado de Procesamiento
```http
GET /api/v1/media/{file_id}/status
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "file_id": "507f1f77bcf86cd799439014",
  "status": "processing",
  "progress": 75,
  "message": "Processing image...",
  "error": null
}
```

## Endpoints de Geolocalización

### Buscar Ubicaciones
```http
GET /api/v1/geolocation/search?query=Madrid&country=ES&limit=10
Authorization: Bearer <token>
```

**Respuesta:**
```json
[
  {
    "id": "place.123456",
    "name": "Madrid",
    "full_name": "Madrid, Comunidad de Madrid, España",
    "coordinates": [-3.7038, 40.4168],
    "place_type": ["place", "locality"],
    "context": [
      {
        "id": "region.123456",
        "text": "Comunidad de Madrid"
      },
      {
        "id": "country.123456",
        "text": "España"
      }
    ],
    "relevance": 0.99
  }
]
```

### Geocodificación Inversa
```http
POST /api/v1/geolocation/reverse?latitude=40.4168&longitude=-3.7038
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "coordinates": [-3.7038, 40.4168],
  "name": "Madrid",
  "full_name": "Madrid, Comunidad de Madrid, España",
  "place_type": ["place", "locality"],
  "context": [...],
  "relevance": 0.99
}
```

### Validar Ubicación
```http
POST /api/v1/geolocation/validate
Authorization: Bearer <token>
Content-Type: application/json

{
  "type": "point",
  "coordinates": [-3.7038, 40.4168],
  "name": "Madrid"
}
```

**Respuesta:**
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": []
}
```

### Obtener Países
```http
GET /api/v1/geolocation/countries
Authorization: Bearer <token>
```

**Respuesta:**
```json
[
  {
    "code": "ES",
    "name": "España"
  },
  {
    "code": "US",
    "name": "Estados Unidos"
  }
]
```

### Obtener Regiones
```http
GET /api/v1/geolocation/regions?country_code=ES
Authorization: Bearer <token>
```

**Respuesta:**
```json
[
  {
    "code": "MD",
    "name": "Madrid"
  },
  {
    "code": "CT",
    "name": "Cataluña"
  }
]
```

### Obtener Ciudades
```http
GET /api/v1/geolocation/cities?country_code=ES&region_code=MD&limit=50
Authorization: Bearer <token>
```

**Respuesta:**
```json
[
  {
    "name": "Madrid",
    "region": "MD",
    "coordinates": [-3.7038, 40.4168]
  },
  {
    "name": "Alcalá de Henares",
    "region": "MD",
    "coordinates": [-3.3700, 40.4833]
  }
]
```

### Calcular Distancia
```http
POST /api/v1/geolocation/distance
Authorization: Bearer <token>
Content-Type: application/json

{
  "point1": {
    "type": "point",
    "coordinates": [-3.7038, 40.4168]
  },
  "point2": {
    "type": "point",
    "coordinates": [-0.3763, 39.4699]
  }
}
```

**Respuesta:**
```json
{
  "distance_km": 352.5,
  "distance_miles": 218.8,
  "point1": {
    "coordinates": [-3.7038, 40.4168],
    "type": "point"
  },
  "point2": {
    "coordinates": [-0.3763, 39.4699],
    "type": "point"
  }
}
```

## Códigos de Error

### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "type": "ValidationError",
  "status_code": 400
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid authentication credentials",
  "type": "UnauthorizedError",
  "status_code": 401
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions",
  "type": "ForbiddenError",
  "status_code": 403
}
```

### 404 Not Found
```json
{
  "error": "Campaign with id '507f1f77bcf86cd799439011' not found",
  "type": "NotFoundError",
  "status_code": 404
}
```

### 422 Unprocessable Entity
```json
{
  "error": "Validation error",
  "type": "ValidationError",
  "status_code": 422,
  "details": {
    "name": ["This field is required"],
    "budget": ["Must be greater than 0"]
  }
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "type": "DatabaseError",
  "status_code": 500
}
```

## Rate Limiting

- **Límite**: 1000 requests por hora por IP
- **Headers de respuesta**:
  - `X-RateLimit-Limit`: Límite de requests
  - `X-RateLimit-Remaining`: Requests restantes
  - `X-RateLimit-Reset`: Timestamp de reset

## Paginación

### Parámetros
- `page`: Número de página (empezando en 1)
- `size`: Tamaño de página (máximo 100)

### Headers de respuesta
- `X-Total-Count`: Total de elementos
- `X-Page-Count`: Total de páginas
- `X-Current-Page`: Página actual
- `X-Per-Page`: Elementos por página

## Filtros y Búsqueda

### Campañas
- `status`: Filtrar por estado
- `search`: Buscar por nombre
- `start_date`: Filtrar por fecha de inicio
- `end_date`: Filtrar por fecha de fin
- `priority`: Filtrar por prioridad

### Archivos Multimedia
- `campaign_id`: Filtrar por campaña
- `file_type`: Filtrar por tipo (image, video, audio, document)
- `status`: Filtrar por estado de procesamiento

## Webhooks (Futuro)

### Eventos Disponibles
- `campaign.created`: Campaña creada
- `campaign.updated`: Campaña actualizada
- `campaign.deleted`: Campaña eliminada
- `media.uploaded`: Archivo subido
- `media.processed`: Archivo procesado

### Configuración
```http
POST /api/v1/webhooks
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://tu-servidor.com/webhook",
  "events": ["campaign.created", "media.uploaded"],
  "secret": "tu-secreto-webhook"
}
```
