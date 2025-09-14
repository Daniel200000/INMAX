"""
Endpoints para gestión de archivos multimedia
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from fastapi.security import HTTPBearer
import structlog

from app.models.media import (
    MediaFile, MediaFileList, MediaUploadResponse, 
    MediaProcessingStatus, MediaType
)
from app.services.media_service import MediaService
from app.services.auth_service import AuthService
from app.core.database import get_database
from app.core.exceptions import FileUploadError, NotFoundError, ValidationError

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


@router.post("/upload", response_model=MediaUploadResponse)
async def upload_media_file(
    file: UploadFile = File(...),
    campaign_id: str = Form(...),
    file_type: MediaType = Form(...),
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Subir un archivo multimedia"""
    try:
        media_service = MediaService(db)
        
        # Validar el archivo
        await media_service.validate_file(file, file_type)
        
        # Subir el archivo
        upload_result = await media_service.upload_file(
            file=file,
            campaign_id=campaign_id,
            user_id=current_user_id,
            file_type=file_type
        )
        
        logger.info(
            "Media file uploaded successfully",
            file_id=upload_result.file_id,
            filename=upload_result.filename,
            user_id=current_user_id,
            campaign_id=campaign_id
        )
        
        return upload_result
        
    except FileUploadError as e:
        logger.error("File upload error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except ValidationError as e:
        logger.error("Validation error uploading file", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error uploading file", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading file"
        )


@router.get("/", response_model=MediaFileList)
async def list_media_files(
    campaign_id: Optional[str] = Query(None, description="Filtrar por campaña"),
    file_type: Optional[MediaType] = Query(None, description="Filtrar por tipo de archivo"),
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Listar archivos multimedia con paginación"""
    try:
        media_service = MediaService(db)
        
        files_data = await media_service.list_files(
            user_id=current_user_id,
            campaign_id=campaign_id,
            file_type=file_type,
            page=page,
            size=size
        )
        
        logger.info(
            "Media files retrieved successfully",
            user_id=current_user_id,
            total=files_data.total
        )
        
        return files_data
        
    except Exception as e:
        logger.error("Error listing media files", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving media files"
        )


@router.get("/{file_id}", response_model=MediaFile)
async def get_media_file(
    file_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener un archivo multimedia específico"""
    try:
        media_service = MediaService(db)
        media_file = await media_service.get_file(file_id, current_user_id)
        
        if not media_file:
            raise NotFoundError("Media file", file_id)
        
        logger.info(
            "Media file retrieved successfully",
            file_id=file_id,
            user_id=current_user_id
        )
        
        return media_file
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media file with id '{file_id}' not found"
        )
    except Exception as e:
        logger.error("Error getting media file", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving media file"
        )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media_file(
    file_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Eliminar un archivo multimedia"""
    try:
        media_service = MediaService(db)
        
        # Verificar que el archivo existe y pertenece al usuario
        existing_file = await media_service.get_file(file_id, current_user_id)
        if not existing_file:
            raise NotFoundError("Media file", file_id)
        
        # Eliminar el archivo
        await media_service.delete_file(file_id, current_user_id)
        
        logger.info(
            "Media file deleted successfully",
            file_id=file_id,
            user_id=current_user_id
        )
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media file with id '{file_id}' not found"
        )
    except Exception as e:
        logger.error("Error deleting media file", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting media file"
        )


@router.get("/{file_id}/status", response_model=MediaProcessingStatus)
async def get_processing_status(
    file_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Obtener el estado de procesamiento de un archivo"""
    try:
        media_service = MediaService(db)
        
        # Verificar que el archivo existe y pertenece al usuario
        existing_file = await media_service.get_file(file_id, current_user_id)
        if not existing_file:
            raise NotFoundError("Media file", file_id)
        
        # Obtener estado de procesamiento
        status = await media_service.get_processing_status(file_id)
        
        logger.info(
            "Processing status retrieved successfully",
            file_id=file_id,
            status=status.status,
            user_id=current_user_id
        )
        
        return status
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media file with id '{file_id}' not found"
        )
    except Exception as e:
        logger.error("Error getting processing status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving processing status"
        )


@router.post("/{file_id}/reprocess", response_model=MediaProcessingStatus)
async def reprocess_file(
    file_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_database)
):
    """Reprocesar un archivo multimedia"""
    try:
        media_service = MediaService(db)
        
        # Verificar que el archivo existe y pertenece al usuario
        existing_file = await media_service.get_file(file_id, current_user_id)
        if not existing_file:
            raise NotFoundError("Media file", file_id)
        
        # Reprocesar el archivo
        status = await media_service.reprocess_file(file_id)
        
        logger.info(
            "File reprocessing started",
            file_id=file_id,
            user_id=current_user_id
        )
        
        return status
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media file with id '{file_id}' not found"
        )
    except Exception as e:
        logger.error("Error reprocessing file", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error reprocessing file"
        )
