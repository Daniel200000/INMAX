"""
Endpoints para servicios de geolocalización
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer
import structlog

from app.models.campaign import GeoLocation, LocationType
from app.services.geolocation_service import GeolocationService
from app.services.auth_service import AuthService
from app.core.database import get_database
from app.core.exceptions import GeolocationError, ValidationError

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBearer()


async def get_current_user_id(token: str = Depends(security)):
    """Obtener ID del usuario actual desde el token"""
    auth_service = AuthService()
    try:
        user_data = await auth_service.verify_token(token.credentials)
        return user_data.get("user_id")
    except Exception as e:
        logger.error("Error verifying token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


@router.get("/search", response_model=List[dict])
async def search_locations(
    query: str = Query(..., min_length=2, description="Término de búsqueda"),
    country: Optional[str] = Query(None, description="Filtrar por país"),
    limit: int = Query(10, ge=1, le=50, description="Límite de resultados"),
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Buscar ubicaciones por nombre o dirección"""
    try:
        geolocation_service = GeolocationService(db)
        
        locations = await geolocation_service.search_locations(
            query=query,
            country=country,
            limit=limit
        )
        
        logger.info(
            "Location search completed",
            query=query,
            results_count=len(locations),
            user_id=current_user_id
        )
        
        return locations
        
    except GeolocationError as e:
        logger.error("Geolocation error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error searching locations", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching locations"
        )


@router.post("/reverse", response_model=dict)
async def reverse_geocode(
    latitude: float = Query(..., ge=-90, le=90, description="Latitud"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitud"),
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener información de ubicación a partir de coordenadas"""
    try:
        geolocation_service = GeolocationService(db)
        
        location_info = await geolocation_service.reverse_geocode(
            latitude=latitude,
            longitude=longitude
        )
        
        logger.info(
            "Reverse geocoding completed",
            latitude=latitude,
            longitude=longitude,
            user_id=current_user_id
        )
        
        return location_info
        
    except GeolocationError as e:
        logger.error("Geolocation error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error reverse geocoding", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error reverse geocoding"
        )


@router.post("/validate", response_model=dict)
async def validate_location(
    location: GeoLocation,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Validar una ubicación geográfica"""
    try:
        geolocation_service = GeolocationService(db)
        
        validation_result = await geolocation_service.validate_location(location)
        
        logger.info(
            "Location validation completed",
            location_type=location.type,
            user_id=current_user_id,
            is_valid=validation_result.get("is_valid", False)
        )
        
        return validation_result
        
    except ValidationError as e:
        logger.error("Validation error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except GeolocationError as e:
        logger.error("Geolocation error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error validating location", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error validating location"
        )


@router.get("/countries", response_model=List[dict])
async def get_countries(
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener lista de países disponibles"""
    try:
        geolocation_service = GeolocationService(db)
        
        countries = await geolocation_service.get_countries()
        
        logger.info(
            "Countries retrieved successfully",
            count=len(countries),
            user_id=current_user_id
        )
        
        return countries
        
    except Exception as e:
        logger.error("Error getting countries", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving countries"
        )


@router.get("/regions", response_model=List[dict])
async def get_regions(
    country_code: Optional[str] = Query(None, description="Código del país"),
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener lista de regiones/estados de un país"""
    try:
        geolocation_service = GeolocationService(db)
        
        regions = await geolocation_service.get_regions(country_code)
        
        logger.info(
            "Regions retrieved successfully",
            country_code=country_code,
            count=len(regions),
            user_id=current_user_id
        )
        
        return regions
        
    except Exception as e:
        logger.error("Error getting regions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving regions"
        )


@router.get("/cities", response_model=List[dict])
async def get_cities(
    country_code: Optional[str] = Query(None, description="Código del país"),
    region_code: Optional[str] = Query(None, description="Código de la región"),
    limit: int = Query(50, ge=1, le=200, description="Límite de resultados"),
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener lista de ciudades"""
    try:
        geolocation_service = GeolocationService(db)
        
        cities = await geolocation_service.get_cities(
            country_code=country_code,
            region_code=region_code,
            limit=limit
        )
        
        logger.info(
            "Cities retrieved successfully",
            country_code=country_code,
            region_code=region_code,
            count=len(cities),
            user_id=current_user_id
        )
        
        return cities
        
    except Exception as e:
        logger.error("Error getting cities", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving cities"
        )


@router.post("/distance", response_model=dict)
async def calculate_distance(
    point1: GeoLocation,
    point2: GeoLocation,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Calcular distancia entre dos puntos geográficos"""
    try:
        geolocation_service = GeolocationService(db)
        
        distance_info = await geolocation_service.calculate_distance(point1, point2)
        
        logger.info(
            "Distance calculated successfully",
            user_id=current_user_id,
            distance=distance_info.get("distance", 0)
        )
        
        return distance_info
        
    except ValidationError as e:
        logger.error("Validation error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except GeolocationError as e:
        logger.error("Geolocation error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error calculating distance", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error calculating distance"
        )
