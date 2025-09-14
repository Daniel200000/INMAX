"""
Modelos de datos para archivos multimedia
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from enum import Enum


class MediaType(str, Enum):
    """Tipos de archivos multimedia"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class MediaStatus(str, Enum):
    """Estados de procesamiento de archivos"""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"
    DELETED = "deleted"


class MediaFileBase(BaseModel):
    """Modelo base para archivos multimedia"""
    filename: str = Field(..., min_length=1, max_length=255)
    original_filename: str = Field(..., min_length=1, max_length=255)
    file_type: MediaType
    mime_type: str = Field(..., min_length=1, max_length=100)
    size: int = Field(..., gt=0)
    campaign_id: str
    metadata: Optional[Dict[str, Any]] = None
    
    @validator('size')
    def validate_size(cls, v):
        """Validar tamaño del archivo"""
        max_size = 50 * 1024 * 1024  # 50MB
        if v > max_size:
            raise ValueError(f'File size must be less than {max_size // (1024*1024)}MB')
        return v


class MediaFileCreate(MediaFileBase):
    """Modelo para crear un archivo multimedia"""
    pass


class MediaFileUpdate(BaseModel):
    """Modelo para actualizar un archivo multimedia"""
    filename: Optional[str] = Field(None, min_length=1, max_length=255)
    metadata: Optional[Dict[str, Any]] = None


class MediaFile(MediaFileBase):
    """Modelo completo de archivo multimedia"""
    id: str = Field(..., alias="_id")
    url: str
    thumbnail_url: Optional[str] = None
    status: MediaStatus = MediaStatus.UPLOADING
    upload_date: datetime
    processed_date: Optional[datetime] = None
    user_id: str
    error_message: Optional[str] = None
    
    # Metadatos específicos por tipo
    image_metadata: Optional[Dict[str, Any]] = None  # width, height, format, etc.
    video_metadata: Optional[Dict[str, Any]] = None  # duration, resolution, codec, etc.
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class MediaFileList(BaseModel):
    """Modelo para listar archivos multimedia con paginación"""
    files: list[MediaFile]
    total: int
    page: int
    size: int
    pages: int


class MediaUploadResponse(BaseModel):
    """Respuesta de carga de archivo"""
    file_id: str
    filename: str
    url: str
    status: MediaStatus
    message: str


class MediaProcessingStatus(BaseModel):
    """Estado de procesamiento de archivo"""
    file_id: str
    status: MediaStatus
    progress: int = Field(..., ge=0, le=100)  # Porcentaje de progreso
    message: Optional[str] = None
    error: Optional[str] = None


class ImageMetadata(BaseModel):
    """Metadatos específicos para imágenes"""
    width: int
    height: int
    format: str
    color_space: Optional[str] = None
    dpi: Optional[tuple[int, int]] = None
    exif_data: Optional[Dict[str, Any]] = None


class VideoMetadata(BaseModel):
    """Metadatos específicos para videos"""
    duration: float  # En segundos
    width: int
    height: int
    fps: float
    codec: str
    bitrate: Optional[int] = None
    audio_codec: Optional[str] = None
    audio_bitrate: Optional[int] = None
