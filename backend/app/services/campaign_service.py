"""
Servicio para gestión de campañas
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId
import structlog

from app.models.campaign import (
    Campaign, CampaignCreate, CampaignUpdate, CampaignList, 
    CampaignStats, CampaignStatus
)
from app.core.database import get_database
from app.core.exceptions import NotFoundError, ValidationError, DatabaseError

logger = structlog.get_logger()


class CampaignService:
    """Servicio para operaciones de campañas"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.campaigns
    
    async def create_campaign(self, campaign_data: CampaignCreate, user_id: str) -> Campaign:
        """Crear una nueva campaña"""
        try:
            now = datetime.utcnow()
            
            campaign_dict = campaign_data.dict()
            campaign_dict.update({
                "user_id": user_id,
                "status": CampaignStatus.DRAFT,
                "created_at": now,
                "updated_at": now,
                "views_count": 0,
                "clicks_count": 0,
                "conversions_count": 0
            })
            
            # Insertar en la base de datos
            result = await self.collection.insert_one(campaign_dict)
            
            # Obtener la campaña creada
            campaign = await self.get_campaign_by_id(str(result.inserted_id))
            
            logger.info(
                "Campaign created successfully",
                campaign_id=campaign.id,
                user_id=user_id
            )
            
            return campaign
            
        except Exception as e:
            logger.error("Error creating campaign", error=str(e))
            raise DatabaseError("Error creating campaign")
    
    async def get_campaign(self, campaign_id: str, user_id: str) -> Optional[Campaign]:
        """Obtener una campaña por ID"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            
            if not campaign or campaign.user_id != user_id:
                return None
            
            return campaign
            
        except Exception as e:
            logger.error("Error getting campaign", campaign_id=campaign_id, error=str(e))
            raise DatabaseError("Error retrieving campaign")
    
    async def get_campaign_by_id(self, campaign_id: str) -> Optional[Campaign]:
        """Obtener campaña por ID sin verificar usuario"""
        try:
            if not ObjectId.is_valid(campaign_id):
                return None
            
            campaign_doc = await self.collection.find_one({"_id": ObjectId(campaign_id)})
            
            if not campaign_doc:
                return None
            
            campaign_doc["_id"] = str(campaign_doc["_id"])
            return Campaign(**campaign_doc)
            
        except Exception as e:
            logger.error("Error getting campaign by id", campaign_id=campaign_id, error=str(e))
            raise DatabaseError("Error retrieving campaign")
    
    async def list_campaigns(
        self,
        user_id: str,
        page: int = 1,
        size: int = 10,
        status: Optional[CampaignStatus] = None,
        search: Optional[str] = None
    ) -> CampaignList:
        """Listar campañas con paginación y filtros"""
        try:
            # Construir filtros
            filters = {"user_id": user_id}
            
            if status:
                filters["status"] = status
            
            if search:
                filters["name"] = {"$regex": search, "$options": "i"}
            
            # Calcular skip
            skip = (page - 1) * size
            
            # Obtener total de documentos
            total = await self.collection.count_documents(filters)
            
            # Obtener campañas
            cursor = self.collection.find(filters).skip(skip).limit(size).sort("created_at", -1)
            campaigns_docs = await cursor.to_list(length=size)
            
            # Convertir a objetos Campaign
            campaigns = []
            for doc in campaigns_docs:
                doc["_id"] = str(doc["_id"])
                campaigns.append(Campaign(**doc))
            
            # Calcular páginas
            pages = (total + size - 1) // size
            
            return CampaignList(
                campaigns=campaigns,
                total=total,
                page=page,
                size=size,
                pages=pages
            )
            
        except Exception as e:
            logger.error("Error listing campaigns", error=str(e))
            raise DatabaseError("Error listing campaigns")
    
    async def update_campaign(
        self,
        campaign_id: str,
        campaign_data: CampaignUpdate,
        user_id: str
    ) -> Campaign:
        """Actualizar una campaña"""
        try:
            # Verificar que la campaña existe y pertenece al usuario
            existing_campaign = await self.get_campaign(campaign_id, user_id)
            if not existing_campaign:
                raise NotFoundError("Campaign", campaign_id)
            
            # Preparar datos de actualización
            update_data = campaign_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            # Actualizar en la base de datos
            result = await self.collection.update_one(
                {"_id": ObjectId(campaign_id), "user_id": user_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise NotFoundError("Campaign", campaign_id)
            
            # Obtener la campaña actualizada
            updated_campaign = await self.get_campaign_by_id(campaign_id)
            
            logger.info(
                "Campaign updated successfully",
                campaign_id=campaign_id,
                user_id=user_id
            )
            
            return updated_campaign
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error updating campaign", campaign_id=campaign_id, error=str(e))
            raise DatabaseError("Error updating campaign")
    
    async def delete_campaign(self, campaign_id: str, user_id: str) -> bool:
        """Eliminar una campaña"""
        try:
            # Verificar que la campaña existe y pertenece al usuario
            existing_campaign = await self.get_campaign(campaign_id, user_id)
            if not existing_campaign:
                raise NotFoundError("Campaign", campaign_id)
            
            # Eliminar de la base de datos
            result = await self.collection.delete_one(
                {"_id": ObjectId(campaign_id), "user_id": user_id}
            )
            
            if result.deleted_count == 0:
                raise NotFoundError("Campaign", campaign_id)
            
            logger.info(
                "Campaign deleted successfully",
                campaign_id=campaign_id,
                user_id=user_id
            )
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error deleting campaign", campaign_id=campaign_id, error=str(e))
            raise DatabaseError("Error deleting campaign")
    
    async def update_campaign_status(
        self,
        campaign_id: str,
        new_status: CampaignStatus,
        user_id: str
    ) -> Campaign:
        """Actualizar el estado de una campaña"""
        try:
            # Verificar que la campaña existe y pertenece al usuario
            existing_campaign = await self.get_campaign(campaign_id, user_id)
            if not existing_campaign:
                raise NotFoundError("Campaign", campaign_id)
            
            # Validar transición de estado
            if not self._is_valid_status_transition(existing_campaign.status, new_status):
                raise ValidationError(
                    f"Invalid status transition from {existing_campaign.status} to {new_status}"
                )
            
            # Actualizar estado
            update_data = {
                "status": new_status,
                "updated_at": datetime.utcnow()
            }
            
            result = await self.collection.update_one(
                {"_id": ObjectId(campaign_id), "user_id": user_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise NotFoundError("Campaign", campaign_id)
            
            # Obtener la campaña actualizada
            updated_campaign = await self.get_campaign_by_id(campaign_id)
            
            logger.info(
                "Campaign status updated successfully",
                campaign_id=campaign_id,
                new_status=new_status,
                user_id=user_id
            )
            
            return updated_campaign
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error("Error updating campaign status", campaign_id=campaign_id, error=str(e))
            raise DatabaseError("Error updating campaign status")
    
    async def get_campaign_stats(self, campaign_id: str) -> CampaignStats:
        """Obtener estadísticas de una campaña"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign", campaign_id)
            
            # Calcular métricas
            ctr = (campaign.clicks_count / campaign.views_count * 100) if campaign.views_count > 0 else 0
            conversion_rate = (campaign.conversions_count / campaign.clicks_count * 100) if campaign.clicks_count > 0 else 0
            cost_per_click = (campaign.budget / campaign.clicks_count) if campaign.clicks_count > 0 else 0
            cost_per_conversion = (campaign.budget / campaign.conversions_count) if campaign.conversions_count > 0 else 0
            
            stats = CampaignStats(
                campaign_id=campaign_id,
                views=campaign.views_count,
                clicks=campaign.clicks_count,
                conversions=campaign.conversions_count,
                ctr=round(ctr, 2),
                conversion_rate=round(conversion_rate, 2),
                cost_per_click=round(cost_per_click, 2),
                cost_per_conversion=round(cost_per_conversion, 2),
                total_spent=campaign.budget,
                last_updated=datetime.utcnow()
            )
            
            logger.info(
                "Campaign stats retrieved successfully",
                campaign_id=campaign_id
            )
            
            return stats
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error getting campaign stats", campaign_id=campaign_id, error=str(e))
            raise DatabaseError("Error retrieving campaign stats")
    
    def _is_valid_status_transition(self, current_status: CampaignStatus, new_status: CampaignStatus) -> bool:
        """Validar si una transición de estado es válida"""
        valid_transitions = {
            CampaignStatus.DRAFT: [CampaignStatus.ACTIVE, CampaignStatus.CANCELLED],
            CampaignStatus.ACTIVE: [CampaignStatus.PAUSED, CampaignStatus.FINISHED, CampaignStatus.CANCELLED],
            CampaignStatus.PAUSED: [CampaignStatus.ACTIVE, CampaignStatus.FINISHED, CampaignStatus.CANCELLED],
            CampaignStatus.FINISHED: [],  # No se puede cambiar desde finished
            CampaignStatus.CANCELLED: []  # No se puede cambiar desde cancelled
        }
        
        return new_status in valid_transitions.get(current_status, [])
