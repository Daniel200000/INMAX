"""
Modelos de datos para campañas
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from enum import Enum


class CampaignStatus(str, Enum):
    """Estados posibles de una campaña"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class CampaignPriority(str, Enum):
    """Prioridades de campaña"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class LocationType(str, Enum):
    """Tipos de ubicación geográfica"""
    POINT = "point"
    POLYGON = "polygon"
    CIRCLE = "circle"
    COUNTRY = "country"
    REGION = "region"


class GeoLocation(BaseModel):
    """Modelo para ubicación geográfica"""
    type: LocationType
    coordinates: List[float] = Field(..., min_items=2, max_items=2)  # [longitude, latitude]
    radius: Optional[float] = Field(None, gt=0)  # Para círculos
    polygon_coordinates: Optional[List[List[float]]] = None  # Para polígonos
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    
    @validator('coordinates')
    def validate_coordinates(cls, v):
        """Validar coordenadas geográficas"""
        if len(v) != 2:
            raise ValueError('Coordinates must have exactly 2 values [longitude, latitude]')
        
        longitude, latitude = v
        if not (-180 <= longitude <= 180):
            raise ValueError('Longitude must be between -180 and 180')
        if not (-90 <= latitude <= 90):
            raise ValueError('Latitude must be between -90 and 90')
        
        return v


class MediaFile(BaseModel):
    """Modelo para archivos multimedia"""
    id: str = Field(..., alias="_id")
    filename: str
    original_filename: str
    file_type: str  # image, video
    mime_type: str
    size: int
    url: str
    thumbnail_url: Optional[str] = None
    upload_date: datetime
    campaign_id: str
    
    class Config:
        allow_population_by_field_name = True


class CampaignBase(BaseModel):
    """Modelo base para campañas"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    budget: float = Field(..., gt=0)
    demographics: Optional[Dict[str, Any]] = None
    channel: str = Field(..., min_length=1, max_length=100)
    start_date: datetime
    end_date: datetime
    priority: CampaignPriority = CampaignPriority.MEDIUM
    target_locations: List[GeoLocation] = Field(default_factory=list)
    media_files: List[str] = Field(default_factory=list)  # IDs de archivos multimedia
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        """Validar que la fecha de fin sea posterior a la de inicio"""
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class CampaignCreate(CampaignBase):
    """Modelo para crear una campaña"""
    pass


class CampaignUpdate(BaseModel):
    """Modelo para actualizar una campaña"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    budget: Optional[float] = Field(None, gt=0)
    demographics: Optional[Dict[str, Any]] = None
    channel: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    priority: Optional[CampaignPriority] = None
    target_locations: Optional[List[GeoLocation]] = None
    media_files: Optional[List[str]] = None
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        """Validar que la fecha de fin sea posterior a la de inicio"""
        if v and 'start_date' in values and values['start_date'] and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class Campaign(CampaignBase):
    """Modelo completo de campaña"""
    id: str = Field(..., alias="_id")
    user_id: str
    status: CampaignStatus = CampaignStatus.DRAFT
    created_at: datetime
    updated_at: datetime
    views_count: int = 0
    clicks_count: int = 0
    conversions_count: int = 0
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class CampaignList(BaseModel):
    """Modelo para listar campañas con paginación"""
    campaigns: List[Campaign]
    total: int
    page: int
    size: int
    pages: int


class CampaignStats(BaseModel):
    """Estadísticas de una campaña"""
    campaign_id: str
    views: int = 0
    clicks: int = 0
    conversions: int = 0
    ctr: float = 0.0  # Click-through rate
    conversion_rate: float = 0.0
    cost_per_click: float = 0.0
    cost_per_conversion: float = 0.0
    total_spent: float = 0.0
    last_updated: datetime
