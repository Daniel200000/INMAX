"""
Configuración y conexión a Redis
"""

import redis.asyncio as redis
from redis.exceptions import ConnectionError
import structlog
import json

from app.core.config import settings

logger = structlog.get_logger()

# Cliente global de Redis
redis_client: redis.Redis = None


async def connect_to_redis():
    """Conectar a Redis"""
    global redis_client
    
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        
        # Verificar conexión
        await redis_client.ping()
        
        logger.info("Successfully connected to Redis")
        
    except ConnectionError as e:
        logger.error("Failed to connect to Redis", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error connecting to Redis", error=str(e))
        raise


async def close_redis_connection():
    """Cerrar conexión a Redis"""
    global redis_client
    
    if redis_client:
        await redis_client.close()
        logger.info("Disconnected from Redis")


async def get_redis() -> redis.Redis:
    """Obtener instancia de Redis"""
    if redis_client is None:
        raise Exception("Redis not initialized")
    return redis_client


class RedisCache:
    """Clase para manejar caché en Redis"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    async def get(self, key: str) -> dict:
        """Obtener valor del caché"""
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("Error getting from cache", key=key, error=str(e))
            return None
    
    async def set(self, key: str, value: dict, expire: int = 3600):
        """Establecer valor en el caché"""
        try:
            await self.redis.setex(
                key, 
                expire, 
                json.dumps(value, default=str)
            )
        except Exception as e:
            logger.error("Error setting cache", key=key, error=str(e))
    
    async def delete(self, key: str):
        """Eliminar valor del caché"""
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error("Error deleting from cache", key=key, error=str(e))
    
    async def delete_pattern(self, pattern: str):
        """Eliminar valores que coincidan con un patrón"""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)
        except Exception as e:
            logger.error("Error deleting pattern from cache", pattern=pattern, error=str(e))


# Instancia global del caché
cache: RedisCache = None


async def get_cache() -> RedisCache:
    """Obtener instancia del caché"""
    global cache
    if cache is None:
        redis_client = await get_redis()
        cache = RedisCache(redis_client)
    return cache
