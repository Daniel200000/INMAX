"""
Endpoints para gestión de campañas
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer
import structlog

from app.models.campaign import (
    Campaign, CampaignCreate, CampaignUpdate, CampaignList, 
    CampaignStats, CampaignStatus
)
from app.services.campaign_service import CampaignService
from app.services.auth_service import AuthService
from app.core.database import get_database
from app.core.redis_client import get_cache
from app.core.exceptions import NotFoundError, ValidationError

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


@router.post("/", response_model=Campaign, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Crear una nueva campaña"""
    try:
        campaign_service = CampaignService(db)
        campaign = await campaign_service.create_campaign(campaign_data, current_user_id)
        
        logger.info(
            "Campaign created successfully",
            campaign_id=campaign.id,
            user_id=current_user_id
        )
        
        return campaign
        
    except ValidationError as e:
        logger.error("Validation error creating campaign", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error creating campaign", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating campaign"
        )


@router.get("/", response_model=CampaignList)
async def list_campaigns(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    status: Optional[CampaignStatus] = Query(None, description="Filtrar por estado"),
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database),
    cache=Depends(get_cache)
):
    """Listar campañas del usuario con paginación"""
    try:
        campaign_service = CampaignService(db)
        
        # Intentar obtener del caché primero
        cache_key = f"campaigns:{current_user_id}:{page}:{size}:{status}:{search}"
        cached_result = await cache.get(cache_key)
        
        if cached_result:
            logger.info("Campaigns retrieved from cache", user_id=current_user_id)
            return CampaignList(**cached_result)
        
        # Obtener de la base de datos
        campaigns_data = await campaign_service.list_campaigns(
            user_id=current_user_id,
            page=page,
            size=size,
            status=status,
            search=search
        )
        
        # Guardar en caché por 5 minutos
        await cache.set(cache_key, campaigns_data.dict(), expire=300)
        
        logger.info(
            "Campaigns retrieved successfully",
            user_id=current_user_id,
            total=campaigns_data.total
        )
        
        return campaigns_data
        
    except Exception as e:
        logger.error("Error listing campaigns", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving campaigns"
        )


@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(
    campaign_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener una campaña específica"""
    try:
        campaign_service = CampaignService(db)
        campaign = await campaign_service.get_campaign(campaign_id, current_user_id)
        
        if not campaign:
            raise NotFoundError("Campaign", campaign_id)
        
        logger.info(
            "Campaign retrieved successfully",
            campaign_id=campaign_id,
            user_id=current_user_id
        )
        
        return campaign
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with id '{campaign_id}' not found"
        )
    except Exception as e:
        logger.error("Error getting campaign", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving campaign"
        )


@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database),
    cache=Depends(get_cache)
):
    """Actualizar una campaña"""
    try:
        campaign_service = CampaignService(db)
        
        # Verificar que la campaña existe y pertenece al usuario
        existing_campaign = await campaign_service.get_campaign(campaign_id, current_user_id)
        if not existing_campaign:
            raise NotFoundError("Campaign", campaign_id)
        
        # Actualizar la campaña
        updated_campaign = await campaign_service.update_campaign(
            campaign_id, 
            campaign_data, 
            current_user_id
        )
        
        # Invalidar caché relacionado
        await cache.delete_pattern(f"campaigns:{current_user_id}:*")
        await cache.delete(f"campaign:{campaign_id}")
        
        logger.info(
            "Campaign updated successfully",
            campaign_id=campaign_id,
            user_id=current_user_id
        )
        
        return updated_campaign
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with id '{campaign_id}' not found"
        )
    except ValidationError as e:
        logger.error("Validation error updating campaign", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error updating campaign", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating campaign"
        )


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database),
    cache=Depends(get_cache)
):
    """Eliminar una campaña"""
    try:
        campaign_service = CampaignService(db)
        
        # Verificar que la campaña existe y pertenece al usuario
        existing_campaign = await campaign_service.get_campaign(campaign_id, current_user_id)
        if not existing_campaign:
            raise NotFoundError("Campaign", campaign_id)
        
        # Eliminar la campaña
        await campaign_service.delete_campaign(campaign_id, current_user_id)
        
        # Invalidar caché relacionado
        await cache.delete_pattern(f"campaigns:{current_user_id}:*")
        await cache.delete(f"campaign:{campaign_id}")
        
        logger.info(
            "Campaign deleted successfully",
            campaign_id=campaign_id,
            user_id=current_user_id
        )
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with id '{campaign_id}' not found"
        )
    except Exception as e:
        logger.error("Error deleting campaign", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting campaign"
        )


@router.patch("/{campaign_id}/status", response_model=Campaign)
async def update_campaign_status(
    campaign_id: str,
    new_status: CampaignStatus,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database),
    cache=Depends(get_cache)
):
    """Actualizar el estado de una campaña"""
    try:
        campaign_service = CampaignService(db)
        
        # Verificar que la campaña existe y pertenece al usuario
        existing_campaign = await campaign_service.get_campaign(campaign_id, current_user_id)
        if not existing_campaign:
            raise NotFoundError("Campaign", campaign_id)
        
        # Actualizar el estado
        updated_campaign = await campaign_service.update_campaign_status(
            campaign_id, 
            new_status, 
            current_user_id
        )
        
        # Invalidar caché relacionado
        await cache.delete_pattern(f"campaigns:{current_user_id}:*")
        await cache.delete(f"campaign:{campaign_id}")
        
        logger.info(
            "Campaign status updated successfully",
            campaign_id=campaign_id,
            new_status=new_status,
            user_id=current_user_id
        )
        
        return updated_campaign
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with id '{campaign_id}' not found"
        )
    except Exception as e:
        logger.error("Error updating campaign status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating campaign status"
        )


@router.get("/{campaign_id}/stats", response_model=CampaignStats)
async def get_campaign_stats(
    campaign_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener estadísticas de una campaña"""
    try:
        campaign_service = CampaignService(db)
        
        # Verificar que la campaña existe y pertenece al usuario
        existing_campaign = await campaign_service.get_campaign(campaign_id, current_user_id)
        if not existing_campaign:
            raise NotFoundError("Campaign", campaign_id)
        
        # Obtener estadísticas
        stats = await campaign_service.get_campaign_stats(campaign_id)
        
        logger.info(
            "Campaign stats retrieved successfully",
            campaign_id=campaign_id,
            user_id=current_user_id
        )
        
        return stats
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with id '{campaign_id}' not found"
        )
    except Exception as e:
        logger.error("Error getting campaign stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving campaign stats"
        )
