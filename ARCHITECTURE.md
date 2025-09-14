# Arquitectura del Módulo de Campañas - Inmax

## Resumen Ejecutivo

El Módulo de Campañas de Inmax es una solución completa para la gestión de campañas publicitarias con funcionalidades avanzadas de geolocalización. La arquitectura está diseñada para ser escalable, mantenible y preparada para el crecimiento futuro.

## Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido para Python
- **MongoDB**: Base de datos NoSQL para datos de geolocalización y multimedia
- **Redis**: Caché y gestión de sesiones
- **Docker**: Containerización para desarrollo y despliegue
- **Pydantic**: Validación de datos y serialización

### Frontend
- **React 18**: Biblioteca de UI con TypeScript
- **Leaflet**: Mapas interactivos para geolocalización
- **React Hook Form**: Manejo de formularios
- **Axios**: Cliente HTTP
- **i18next**: Internacionalización

### Servicios Externos
- **AWS S3**: Almacenamiento de archivos multimedia
- **Mapbox API**: Geocodificación y mapas avanzados

## Arquitectura del Sistema

### Patrón de Arquitectura
- **Arquitectura de Microservicios**: Cada dominio de negocio es un módulo independiente
- **API REST**: Comunicación entre frontend y backend
- **Arquitectura de Capas**: Separación clara de responsabilidades

### Estructura de Capas

#### Backend (FastAPI)
```
backend/
├── app/
│   ├── core/           # Configuración y utilidades base
│   ├── models/         # Modelos de datos (Pydantic)
│   ├── services/       # Lógica de negocio
│   ├── api/            # Endpoints de la API
│   └── main.py         # Punto de entrada
```

#### Frontend (React)
```
frontend/
├── src/
│   ├── components/     # Componentes reutilizables
│   ├── pages/          # Páginas de la aplicación
│   ├── contexts/       # Gestión de estado global
│   ├── services/       # Servicios de API
│   ├── types/          # Definiciones de TypeScript
│   └── i18n/           # Internacionalización
```

## Módulos de Negocio

### 1. Módulo de Usuarios
- **Responsabilidad**: Autenticación, autorización y gestión de perfiles
- **Endpoints**: `/api/v1/users/*`
- **Características**:
  - Registro y login de usuarios
  - Gestión de perfiles
  - Control de acceso basado en roles

### 2. Módulo de Campañas
- **Responsabilidad**: Gestión completa del ciclo de vida de campañas
- **Endpoints**: `/api/v1/campaigns/*`
- **Características**:
  - CRUD de campañas
  - Gestión de estados
  - Estadísticas y métricas

### 3. Módulo de Multimedia
- **Responsabilidad**: Gestión de archivos multimedia
- **Endpoints**: `/api/v1/media/*`
- **Características**:
  - Carga de archivos
  - Procesamiento de imágenes/videos
  - Integración con AWS S3

### 4. Módulo de Geolocalización
- **Responsabilidad**: Servicios de geolocalización y mapas
- **Endpoints**: `/api/v1/geolocation/*`
- **Características**:
  - Búsqueda de ubicaciones
  - Geocodificación inversa
  - Validación de coordenadas

## Flujo de Datos

### 1. Autenticación
```
Usuario → Frontend → API → JWT Token → Contexto Global
```

### 2. Creación de Campaña
```
Formulario → Validación → API → Base de Datos → Respuesta → UI
```

### 3. Carga de Multimedia
```
Archivo → Validación → AWS S3 → URL → Base de Datos → UI
```

### 4. Geolocalización
```
Búsqueda → Mapbox API → Resultados → Mapa → Selección → Base de Datos
```

## Seguridad

### Autenticación
- **JWT Tokens**: Autenticación stateless
- **Refresh Tokens**: Renovación automática de sesiones
- **Bcrypt**: Hashing seguro de contraseñas

### Autorización
- **Roles de Usuario**: admin, manager, creator, viewer
- **Middleware de Autorización**: Verificación en cada endpoint
- **CORS**: Configuración de orígenes permitidos

### Validación de Datos
- **Pydantic**: Validación automática de esquemas
- **Sanitización**: Limpieza de inputs del usuario
- **Rate Limiting**: Protección contra ataques de fuerza bruta

## Escalabilidad

### Horizontal
- **Docker Containers**: Fácil escalado horizontal
- **Load Balancer**: Distribución de carga
- **MongoDB Sharding**: Particionado de datos

### Vertical
- **Caché Redis**: Reducción de carga en la base de datos
- **CDN**: Distribución de archivos estáticos
- **Optimización de Consultas**: Índices optimizados

## Monitoreo y Logging

### Logging
- **Structlog**: Logging estructurado
- **Niveles de Log**: DEBUG, INFO, WARNING, ERROR
- **Contexto**: Información de usuario y request

### Métricas
- **Health Checks**: Monitoreo de salud de servicios
- **Performance**: Tiempo de respuesta de endpoints
- **Errores**: Tracking de errores y excepciones

## Internacionalización (i18n)

### Idiomas Soportados
- **Español**: Idioma por defecto
- **Inglés**: Soporte completo
- **Portugués**: Soporte completo

### Implementación
- **i18next**: Biblioteca de internacionalización
- **Detección Automática**: Idioma del navegador
- **Persistencia**: Guardado en localStorage

## Despliegue

### Desarrollo
```bash
docker-compose up -d
```

### Producción
- **Docker Swarm**: Orquestación de contenedores
- **Nginx**: Proxy reverso y balanceador
- **SSL/TLS**: Certificados de seguridad
- **Backup**: Respaldo automático de datos

## Consideraciones de Rendimiento

### Backend
- **Async/Await**: Programación asíncrona
- **Connection Pooling**: Pool de conexiones a MongoDB
- **Caché**: Redis para datos frecuentes

### Frontend
- **Code Splitting**: Carga lazy de componentes
- **Memoización**: Optimización de re-renders
- **CDN**: Servir archivos estáticos

### Base de Datos
- **Índices**: Optimización de consultas
- **Agregaciones**: Pipeline de MongoDB
- **Sharding**: Distribución de datos

## Próximos Pasos

### Fase 2 (Próximo Sprint)
- [ ] Sistema de notificaciones
- [ ] Reportes avanzados
- [ ] Integración con redes sociales
- [ ] Dashboard de analytics

### Fase 3 (Futuro)
- [ ] Machine Learning para optimización
- [ ] API pública
- [ ] Aplicación móvil
- [ ] Integración con más plataformas

## Conclusión

La arquitectura del Módulo de Campañas está diseñada para ser:
- **Escalable**: Preparada para el crecimiento
- **Mantenible**: Código limpio y bien documentado
- **Segura**: Múltiples capas de seguridad
- **Flexible**: Fácil de extender y modificar
- **Profesional**: Siguiendo mejores prácticas de la industria
