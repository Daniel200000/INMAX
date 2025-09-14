"""
Servicio para gestión de archivos multimedia
"""

import os
import uuid
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
import structlog
import boto3
from botocore.exceptions import ClientError

from app.models.media import (
    MediaFile, MediaFileCreate, MediaFileUpdate, MediaFileList,
    MediaUploadResponse, MediaProcessingStatus, MediaType, MediaStatus
)
from app.core.config import settings
from app.core.database import get_database
from app.core.exceptions import FileUploadError, NotFoundError, ValidationError, DatabaseError, ExternalServiceError

logger = structlog.get_logger()


class MediaService:
    """Servicio para operaciones de archivos multimedia"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.media_files
        self.s3_client = self._get_s3_client()
    
    def _get_s3_client(self):
        """Obtener cliente de S3"""
        try:
            if not all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY]):
                logger.warning("AWS credentials not configured, using local storage")
                return None
            
            return boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        except Exception as e:
            logger.error("Error creating S3 client", error=str(e))
            return None
    
    async def validate_file(self, file, file_type: MediaType) -> bool:
        """Validar archivo antes de subir"""
        try:
            # Verificar tamaño
            if file.size > settings.MAX_FILE_SIZE:
                raise FileUploadError(
                    f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE // (1024*1024)}MB"
                )
            
            # Verificar tipo MIME
            if file_type == MediaType.IMAGE and file.content_type not in settings.ALLOWED_IMAGE_TYPES:
                raise FileUploadError(
                    f"Invalid image type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
                )
            
            if file_type == MediaType.VIDEO and file.content_type not in settings.ALLOWED_VIDEO_TYPES:
                raise FileUploadError(
                    f"Invalid video type. Allowed types: {', '.join(settings.ALLOWED_VIDEO_TYPES)}"
                )
            
            return True
            
        except FileUploadError:
            raise
        except Exception as e:
            logger.error("Error validating file", error=str(e))
            raise FileUploadError("Error validating file")
    
    async def upload_file(
        self,
        file,
        campaign_id: str,
        user_id: str,
        file_type: MediaType
    ) -> MediaUploadResponse:
        """Subir archivo multimedia"""
        try:
            # Validar archivo
            await self.validate_file(file, file_type)
            
            # Generar nombre único para el archivo
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Determinar ruta de almacenamiento
            folder = "images" if file_type == MediaType.IMAGE else "videos"
            s3_key = f"campaigns/{campaign_id}/{folder}/{unique_filename}"
            
            # Subir archivo a S3 o almacenamiento local
            if self.s3_client and settings.AWS_S3_BUCKET:
                file_url = await self._upload_to_s3(file, s3_key)
            else:
                file_url = await self._upload_locally(file, s3_key)
            
            # Crear registro en la base de datos
            now = datetime.utcnow()
            media_data = {
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_type": file_type,
                "mime_type": file.content_type,
                "size": file.size,
                "url": file_url,
                "thumbnail_url": None,
                "status": MediaStatus.UPLOADING,
                "upload_date": now,
                "processed_date": None,
                "user_id": user_id,
                "campaign_id": campaign_id,
                "error_message": None,
                "image_metadata": None,
                "video_metadata": None
            }
            
            result = await self.collection.insert_one(media_data)
            file_id = str(result.inserted_id)
            
            # Iniciar procesamiento asíncrono
            await self._start_processing(file_id, file_type)
            
            logger.info(
                "File uploaded successfully",
                file_id=file_id,
                filename=unique_filename,
                user_id=user_id,
                campaign_id=campaign_id
            )
            
            return MediaUploadResponse(
                file_id=file_id,
                filename=unique_filename,
                url=file_url,
                status=MediaStatus.UPLOADING,
                message="File uploaded successfully, processing started"
            )
            
        except (FileUploadError, ValidationError):
            raise
        except Exception as e:
            logger.error("Error uploading file", error=str(e))
            raise FileUploadError("Error uploading file")
    
    async def _upload_to_s3(self, file, s3_key: str) -> str:
        """Subir archivo a S3"""
        try:
            file.file.seek(0)  # Resetear posición del archivo
            
            self.s3_client.upload_fileobj(
                file.file,
                settings.AWS_S3_BUCKET,
                s3_key,
                ExtraArgs={
                    'ContentType': file.content_type,
                    'ACL': 'public-read'
                }
            )
            
            file_url = f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
            
            logger.info("File uploaded to S3", s3_key=s3_key)
            
            return file_url
            
        except ClientError as e:
            logger.error("Error uploading to S3", error=str(e))
            raise ExternalServiceError("S3", "Error uploading file to S3")
        except Exception as e:
            logger.error("Error uploading to S3", error=str(e))
            raise ExternalServiceError("S3", "Error uploading file to S3")
    
    async def _upload_locally(self, file, local_path: str) -> str:
        """Subir archivo a almacenamiento local"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(f"uploads/{local_path}"), exist_ok=True)
            
            # Guardar archivo
            with open(f"uploads/{local_path}", "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            file_url = f"/uploads/{local_path}"
            
            logger.info("File uploaded locally", local_path=local_path)
            
            return file_url
            
        except Exception as e:
            logger.error("Error uploading locally", error=str(e))
            raise FileUploadError("Error uploading file locally")
    
    async def _start_processing(self, file_id: str, file_type: MediaType):
        """Iniciar procesamiento del archivo"""
        try:
            # Actualizar estado a procesando
            await self.collection.update_one(
                {"_id": ObjectId(file_id)},
                {"$set": {"status": MediaStatus.PROCESSING}}
            )
            
            # Aquí se implementaría el procesamiento real
            # Por ahora, marcamos como completado
            await self.collection.update_one(
                {"_id": ObjectId(file_id)},
                {"$set": {
                    "status": MediaStatus.READY,
                    "processed_date": datetime.utcnow()
                }}
            )
            
            logger.info("File processing completed", file_id=file_id)
            
        except Exception as e:
            logger.error("Error processing file", file_id=file_id, error=str(e))
            await self.collection.update_one(
                {"_id": ObjectId(file_id)},
                {"$set": {
                    "status": MediaStatus.ERROR,
                    "error_message": str(e)
                }}
            )
    
    async def get_file(self, file_id: str, user_id: str) -> Optional[MediaFile]:
        """Obtener archivo por ID"""
        try:
            if not ObjectId.is_valid(file_id):
                return None
            
            file_doc = await self.collection.find_one({
                "_id": ObjectId(file_id),
                "user_id": user_id
            })
            
            if not file_doc:
                return None
            
            file_doc["_id"] = str(file_doc["_id"])
            return MediaFile(**file_doc)
            
        except Exception as e:
            logger.error("Error getting file", file_id=file_id, error=str(e))
            raise DatabaseError("Error retrieving file")
    
    async def list_files(
        self,
        user_id: str,
        campaign_id: Optional[str] = None,
        file_type: Optional[MediaType] = None,
        page: int = 1,
        size: int = 10
    ) -> MediaFileList:
        """Listar archivos con paginación y filtros"""
        try:
            # Construir filtros
            filters = {"user_id": user_id}
            
            if campaign_id:
                filters["campaign_id"] = campaign_id
            
            if file_type:
                filters["file_type"] = file_type
            
            # Calcular skip
            skip = (page - 1) * size
            
            # Obtener total de documentos
            total = await self.collection.count_documents(filters)
            
            # Obtener archivos
            cursor = self.collection.find(filters).skip(skip).limit(size).sort("upload_date", -1)
            files_docs = await cursor.to_list(length=size)
            
            # Convertir a objetos MediaFile
            files = []
            for doc in files_docs:
                doc["_id"] = str(doc["_id"])
                files.append(MediaFile(**doc))
            
            # Calcular páginas
            pages = (total + size - 1) // size
            
            return MediaFileList(
                files=files,
                total=total,
                page=page,
                size=size,
                pages=pages
            )
            
        except Exception as e:
            logger.error("Error listing files", error=str(e))
            raise DatabaseError("Error listing files")
    
    async def delete_file(self, file_id: str, user_id: str) -> bool:
        """Eliminar archivo"""
        try:
            # Obtener información del archivo
            file_doc = await self.collection.find_one({
                "_id": ObjectId(file_id),
                "user_id": user_id
            })
            
            if not file_doc:
                raise NotFoundError("Media file", file_id)
            
            # Eliminar archivo del almacenamiento
            if file_doc.get("url"):
                await self._delete_from_storage(file_doc["url"])
            
            # Eliminar de la base de datos
            result = await self.collection.delete_one({
                "_id": ObjectId(file_id),
                "user_id": user_id
            })
            
            if result.deleted_count == 0:
                raise NotFoundError("Media file", file_id)
            
            logger.info("File deleted successfully", file_id=file_id, user_id=user_id)
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error deleting file", file_id=file_id, error=str(e))
            raise DatabaseError("Error deleting file")
    
    async def _delete_from_storage(self, file_url: str):
        """Eliminar archivo del almacenamiento"""
        try:
            if file_url.startswith("https://") and self.s3_client:
                # Extraer clave S3 de la URL
                s3_key = file_url.split(f"{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/")[1]
                
                self.s3_client.delete_object(
                    Bucket=settings.AWS_S3_BUCKET,
                    Key=s3_key
                )
                
                logger.info("File deleted from S3", s3_key=s3_key)
            else:
                # Eliminar archivo local
                local_path = file_url.replace("/uploads/", "uploads/")
                if os.path.exists(local_path):
                    os.remove(local_path)
                    logger.info("File deleted locally", local_path=local_path)
                    
        except Exception as e:
            logger.error("Error deleting file from storage", file_url=file_url, error=str(e))
    
    async def get_processing_status(self, file_id: str) -> MediaProcessingStatus:
        """Obtener estado de procesamiento del archivo"""
        try:
            file_doc = await self.collection.find_one({"_id": ObjectId(file_id)})
            
            if not file_doc:
                raise NotFoundError("Media file", file_id)
            
            # Calcular progreso basado en el estado
            progress = 0
            if file_doc["status"] == MediaStatus.UPLOADING:
                progress = 25
            elif file_doc["status"] == MediaStatus.PROCESSING:
                progress = 75
            elif file_doc["status"] == MediaStatus.READY:
                progress = 100
            elif file_doc["status"] == MediaStatus.ERROR:
                progress = 0
            
            return MediaProcessingStatus(
                file_id=file_id,
                status=file_doc["status"],
                progress=progress,
                message=file_doc.get("error_message")
            )
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error getting processing status", file_id=file_id, error=str(e))
            raise DatabaseError("Error getting processing status")
    
    async def reprocess_file(self, file_id: str) -> MediaProcessingStatus:
        """Reprocesar archivo"""
        try:
            # Verificar que el archivo existe
            file_doc = await self.collection.find_one({"_id": ObjectId(file_id)})
            if not file_doc:
                raise NotFoundError("Media file", file_id)
            
            # Reiniciar procesamiento
            await self.collection.update_one(
                {"_id": ObjectId(file_id)},
                {"$set": {
                    "status": MediaStatus.PROCESSING,
                    "error_message": None
                }}
            )
            
            # Iniciar procesamiento
            await self._start_processing(file_id, file_doc["file_type"])
            
            return MediaProcessingStatus(
                file_id=file_id,
                status=MediaStatus.PROCESSING,
                progress=75,
                message="Reprocessing started"
            )
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error reprocessing file", file_id=file_id, error=str(e))
            raise DatabaseError("Error reprocessing file")
