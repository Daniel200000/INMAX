"""
Configuración y conexión a MongoDB
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Cliente global de MongoDB
client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None


async def connect_to_mongo():
    """Conectar a MongoDB"""
    global client, database
    
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        # Verificar conexión
        await client.admin.command('ping')
        
        database = client[settings.MONGO_DATABASE]
        
        # Crear índices necesarios
        await create_indexes()
        
        logger.info("Successfully connected to MongoDB")
        
    except ConnectionFailure as e:
        logger.error("Failed to connect to MongoDB", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error connecting to MongoDB", error=str(e))
        raise


async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    global client
    
    if client:
        client.close()
        logger.info("Disconnected from MongoDB")


async def get_database() -> AsyncIOMotorDatabase:
    """Obtener instancia de la base de datos"""
    if database is None:
        raise Exception("Database not initialized")
    return database


async def create_indexes():
    """Crear índices necesarios en la base de datos"""
    try:
        db = await get_database()
        
        # Índices para la colección de campañas
        await db.campaigns.create_index("user_id")
        await db.campaigns.create_index("status")
        await db.campaigns.create_index("start_date")
        await db.campaigns.create_index("end_date")
        await db.campaigns.create_index([("location", "2dsphere")])  # Índice geoespacial
        
        # Índices para la colección de archivos multimedia
        await db.media_files.create_index("campaign_id")
        await db.media_files.create_index("file_type")
        await db.media_files.create_index("upload_date")
        
        # Índices para la colección de usuarios
        await db.users.create_index("email", unique=True)
        await db.users.create_index("username", unique=True)
        
        # Índices para la colección de ubicaciones
        await db.locations.create_index([("coordinates", "2dsphere")])
        await db.locations.create_index("name")
        await db.locations.create_index("country")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error("Error creating database indexes", error=str(e))
        raise
