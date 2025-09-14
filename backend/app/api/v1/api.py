"""
Router principal de la API v1
"""

from fastapi import APIRouter

from app.api.v1.endpoints import campaigns, media, users, geolocation

api_router = APIRouter()

# Incluir todos los routers de endpoints
api_router.include_router(
    campaigns.router,
    prefix="/campaigns",
    tags=["campaigns"]
)

api_router.include_router(
    media.router,
    prefix="/media",
    tags=["media"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    geolocation.router,
    prefix="/geolocation",
    tags=["geolocation"]
)
