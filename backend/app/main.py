"""
Aplicación principal de FastAPI para el Módulo de Campañas de Inmax
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog
import time

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.redis_client import connect_to_redis, close_redis_connection
from app.api.v1.api import api_router
from app.core.exceptions import CustomException

# Configurar logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Crear aplicación FastAPI
app = FastAPI(
    title="Inmax Campaigns API",
    description="API para el módulo de campañas publicitarias con geolocalización",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de hosts confiables
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.inmax.com"]
)

# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log del request
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None
    )
    
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = time.time() - start_time
    
    # Log del response
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time
    )
    
    return response

# Incluir routers de la API
app.include_router(api_router, prefix="/api/v1")

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup_event():
    """Eventos que se ejecutan al iniciar la aplicación"""
    logger.info("Starting Inmax Campaigns API...")
    
    # Conectar a MongoDB
    await connect_to_mongo()
    logger.info("Connected to MongoDB")
    
    # Conectar a Redis
    await connect_to_redis()
    logger.info("Connected to Redis")
    
    logger.info("Application startup completed")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos que se ejecutan al cerrar la aplicación"""
    logger.info("Shutting down Inmax Campaigns API...")
    
    # Cerrar conexión a MongoDB
    await close_mongo_connection()
    logger.info("Disconnected from MongoDB")
    
    # Cerrar conexión a Redis
    await close_redis_connection()
    logger.info("Disconnected from Redis")
    
    logger.info("Application shutdown completed")

# Manejador global de excepciones
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    """Manejador personalizado para excepciones de la aplicación"""
    logger.error(
        "Custom exception occurred",
        exception_type=type(exc).__name__,
        message=exc.message,
        status_code=exc.status_code,
        url=str(request.url)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "type": type(exc).__name__,
            "status_code": exc.status_code
        }
    )

# Endpoint de salud
@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    return {
        "status": "healthy",
        "service": "inmax-campaigns-api",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

# Endpoint raíz
@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Inmax Campaigns API",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "Documentation not available in production"
    }
