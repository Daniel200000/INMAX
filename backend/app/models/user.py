"""
Modelos de datos para usuarios
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
from bson import ObjectId
from enum import Enum


class UserRole(str, Enum):
    """Roles de usuario"""
    ADMIN = "admin"
    MANAGER = "manager"
    CREATOR = "creator"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """Estados de usuario"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class UserBase(BaseModel):
    """Modelo base para usuarios"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.CREATOR
    status: UserStatus = UserStatus.ACTIVE
    language: str = "es"  # Idioma por defecto
    timezone: str = "UTC"
    
    @validator('username')
    def validate_username(cls, v):
        """Validar formato del nombre de usuario"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, hyphens and underscores')
        return v.lower()


class UserCreate(UserBase):
    """Modelo para crear un usuario"""
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        """Validar fortaleza de la contraseña"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Modelo para actualizar un usuario"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        """Validar formato del nombre de usuario"""
        if v and not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, hyphens and underscores')
        return v.lower() if v else v


class User(UserBase):
    """Modelo completo de usuario"""
    id: str = Field(..., alias="_id")
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    is_verified: bool = False
    verification_token: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class UserLogin(BaseModel):
    """Modelo para login de usuario"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Modelo de respuesta para usuarios (sin datos sensibles)"""
    id: str
    username: str
    email: str
    full_name: str
    role: UserRole
    status: UserStatus
    language: str
    timezone: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_verified: bool


class Token(BaseModel):
    """Modelo para tokens de autenticación"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Datos del token"""
    username: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None
