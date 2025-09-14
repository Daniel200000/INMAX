"""
Excepciones personalizadas para la aplicación
"""

from typing import Optional, Dict, Any


class CustomException(Exception):
    """Excepción base personalizada"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(CustomException):
    """Error de validación de datos"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 422, details)


class NotFoundError(CustomException):
    """Error cuando no se encuentra un recurso"""
    
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} with id '{identifier}' not found"
        super().__init__(message, 404)


class UnauthorizedError(CustomException):
    """Error de autorización"""
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, 401)


class ForbiddenError(CustomException):
    """Error de permisos insuficientes"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


class ConflictError(CustomException):
    """Error de conflicto (recurso ya existe)"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 409, details)


class FileUploadError(CustomException):
    """Error en la carga de archivos"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 400, details)


class GeolocationError(CustomException):
    """Error en operaciones de geolocalización"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 400, details)


class DatabaseError(CustomException):
    """Error de base de datos"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 500, details)


class ExternalServiceError(CustomException):
    """Error en servicios externos (AWS, Mapbox, etc.)"""
    
    def __init__(self, service: str, message: str, details: Optional[Dict[str, Any]] = None):
        full_message = f"Error in {service}: {message}"
        super().__init__(full_message, 502, details)
