"""
Configuración de la aplicación usando Pydantic Settings
"""

from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Configuración principal de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME: str = "Inmax Campaigns API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Configuración de servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Configuración de CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Configuración de MongoDB
    MONGODB_URL: str = "mongodb://admin:password@localhost:27017/inmax_campaigns?authSource=admin"
    MONGO_DATABASE: str = "inmax_campaigns"
    
    # Configuración de Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Configuración de JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    
    # Configuración de Mapbox
    MAPBOX_ACCESS_TOKEN: Optional[str] = None
    
    # Configuración de archivos
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg",
        "image/png", 
        "image/gif",
        "image/webp"
    ]
    ALLOWED_VIDEO_TYPES: List[str] = [
        "video/mp4",
        "video/webm",
        "video/quicktime"
    ]
    
    # Configuración de email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Configuración de notificaciones
    ENABLE_EMAIL_NOTIFICATIONS: bool = False
    ENABLE_PUSH_NOTIFICATIONS: bool = False
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Validar y procesar CORS origins"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_IMAGE_TYPES", pre=True)
    def assemble_image_types(cls, v):
        """Validar tipos de imagen permitidos"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_VIDEO_TYPES", pre=True)
    def assemble_video_types(cls, v):
        """Validar tipos de video permitidos"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
