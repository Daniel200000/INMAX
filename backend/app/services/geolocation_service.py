"""
Servicio para operaciones de geolocalización
"""

from typing import List, Optional, Dict, Any
import httpx
import structlog

from app.models.campaign import GeoLocation, LocationType
from app.core.config import settings
from app.core.database import get_database
from app.core.exceptions import GeolocationError, ValidationError, ExternalServiceError

logger = structlog.get_logger()


class GeolocationService:
    """Servicio para operaciones de geolocalización"""
    
    def __init__(self, db):
        self.db = db
        self.mapbox_token = settings.MAPBOX_ACCESS_TOKEN
        self.base_url = "https://api.mapbox.com"
    
    async def search_locations(
        self,
        query: str,
        country: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Buscar ubicaciones por nombre o dirección"""
        try:
            if not self.mapbox_token:
                raise GeolocationError("Mapbox token not configured")
            
            # Construir parámetros de búsqueda
            params = {
                "access_token": self.mapbox_token,
                "q": query,
                "limit": limit,
                "types": "place,locality,neighborhood,address,poi"
            }
            
            if country:
                params["country"] = country
            
            # Realizar búsqueda
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/geocoding/v5/mapbox.places/{query}.json",
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise ExternalServiceError("Mapbox", f"Search failed: {response.text}")
                
                data = response.json()
                
                # Procesar resultados
                locations = []
                for feature in data.get("features", []):
                    location = {
                        "id": feature.get("id"),
                        "name": feature.get("text"),
                        "full_name": feature.get("place_name"),
                        "coordinates": feature.get("center"),  # [longitude, latitude]
                        "place_type": feature.get("place_type", []),
                        "context": feature.get("context", []),
                        "relevance": feature.get("relevance", 0)
                    }
                    locations.append(location)
                
                logger.info(
                    "Location search completed",
                    query=query,
                    results_count=len(locations)
                )
                
                return locations
                
        except httpx.TimeoutException:
            logger.error("Mapbox API timeout", query=query)
            raise ExternalServiceError("Mapbox", "Request timeout")
        except httpx.RequestError as e:
            logger.error("Mapbox API request error", query=query, error=str(e))
            raise ExternalServiceError("Mapbox", f"Request error: {str(e)}")
        except Exception as e:
            logger.error("Error searching locations", query=query, error=str(e))
            raise GeolocationError("Error searching locations")
    
    async def reverse_geocode(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """Obtener información de ubicación a partir de coordenadas"""
        try:
            if not self.mapbox_token:
                raise GeolocationError("Mapbox token not configured")
            
            # Realizar geocodificación inversa
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/geocoding/v5/mapbox.places/{longitude},{latitude}.json",
                    params={
                        "access_token": self.mapbox_token,
                        "types": "place,locality,neighborhood,address,poi"
                    },
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise ExternalServiceError("Mapbox", f"Reverse geocoding failed: {response.text}")
                
                data = response.json()
                
                # Procesar resultado
                if not data.get("features"):
                    return {
                        "coordinates": [longitude, latitude],
                        "name": "Unknown location",
                        "full_name": "Unknown location",
                        "place_type": [],
                        "context": []
                    }
                
                feature = data["features"][0]
                location_info = {
                    "coordinates": [longitude, latitude],
                    "name": feature.get("text"),
                    "full_name": feature.get("place_name"),
                    "place_type": feature.get("place_type", []),
                    "context": feature.get("context", []),
                    "relevance": feature.get("relevance", 0)
                }
                
                logger.info(
                    "Reverse geocoding completed",
                    latitude=latitude,
                    longitude=longitude,
                    location=location_info["full_name"]
                )
                
                return location_info
                
        except httpx.TimeoutException:
            logger.error("Mapbox API timeout", latitude=latitude, longitude=longitude)
            raise ExternalServiceError("Mapbox", "Request timeout")
        except httpx.RequestError as e:
            logger.error("Mapbox API request error", latitude=latitude, longitude=longitude, error=str(e))
            raise ExternalServiceError("Mapbox", f"Request error: {str(e)}")
        except Exception as e:
            logger.error("Error reverse geocoding", latitude=latitude, longitude=longitude, error=str(e))
            raise GeolocationError("Error reverse geocoding")
    
    async def validate_location(self, location: GeoLocation) -> Dict[str, Any]:
        """Validar una ubicación geográfica"""
        try:
            validation_result = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            # Validar coordenadas
            if location.type in [LocationType.POINT, LocationType.CIRCLE]:
                if not location.coordinates or len(location.coordinates) != 2:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append("Coordinates must have exactly 2 values [longitude, latitude]")
                else:
                    longitude, latitude = location.coordinates
                    if not (-180 <= longitude <= 180):
                        validation_result["is_valid"] = False
                        validation_result["errors"].append("Longitude must be between -180 and 180")
                    
                    if not (-90 <= latitude <= 90):
                        validation_result["is_valid"] = False
                        validation_result["errors"].append("Latitude must be between -90 and 90")
            
            # Validar radio para círculos
            if location.type == LocationType.CIRCLE:
                if not location.radius or location.radius <= 0:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append("Radius must be greater than 0 for circle locations")
                elif location.radius > 1000:  # 1000 km máximo
                    validation_result["warnings"].append("Radius is very large (>1000km)")
            
            # Validar coordenadas de polígono
            if location.type == LocationType.POLYGON:
                if not location.polygon_coordinates or len(location.polygon_coordinates) < 3:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append("Polygon must have at least 3 coordinate points")
                else:
                    for coords in location.polygon_coordinates:
                        if len(coords) != 2:
                            validation_result["is_valid"] = False
                            validation_result["errors"].append("Each polygon point must have exactly 2 coordinates")
                            break
                        
                        lon, lat = coords
                        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
                            validation_result["is_valid"] = False
                            validation_result["errors"].append("Invalid coordinates in polygon")
                            break
            
            # Validar información de país/región
            if location.type in [LocationType.COUNTRY, LocationType.REGION]:
                if not location.country and not location.region:
                    validation_result["warnings"].append("Country or region should be specified")
            
            logger.info(
                "Location validation completed",
                location_type=location.type,
                is_valid=validation_result["is_valid"],
                errors_count=len(validation_result["errors"])
            )
            
            return validation_result
            
        except Exception as e:
            logger.error("Error validating location", error=str(e))
            raise GeolocationError("Error validating location")
    
    async def get_countries(self) -> List[Dict[str, Any]]:
        """Obtener lista de países disponibles"""
        try:
            # Lista básica de países (en producción se obtendría de una API)
            countries = [
                {"code": "ES", "name": "España"},
                {"code": "US", "name": "Estados Unidos"},
                {"code": "MX", "name": "México"},
                {"code": "AR", "name": "Argentina"},
                {"code": "CO", "name": "Colombia"},
                {"code": "PE", "name": "Perú"},
                {"code": "CL", "name": "Chile"},
                {"code": "BR", "name": "Brasil"},
                {"code": "FR", "name": "Francia"},
                {"code": "DE", "name": "Alemania"},
                {"code": "IT", "name": "Italia"},
                {"code": "GB", "name": "Reino Unido"},
                {"code": "CA", "name": "Canadá"},
                {"code": "AU", "name": "Australia"},
                {"code": "JP", "name": "Japón"},
                {"code": "CN", "name": "China"},
                {"code": "IN", "name": "India"}
            ]
            
            logger.info("Countries retrieved", count=len(countries))
            
            return countries
            
        except Exception as e:
            logger.error("Error getting countries", error=str(e))
            raise GeolocationError("Error retrieving countries")
    
    async def get_regions(self, country_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener lista de regiones/estados de un país"""
        try:
            # Lista básica de regiones (en producción se obtendría de una API)
            regions_data = {
                "ES": [
                    {"code": "AN", "name": "Andalucía"},
                    {"code": "AR", "name": "Aragón"},
                    {"code": "AS", "name": "Asturias"},
                    {"code": "IB", "name": "Islas Baleares"},
                    {"code": "CN", "name": "Canarias"},
                    {"code": "CB", "name": "Cantabria"},
                    {"code": "CL", "name": "Castilla y León"},
                    {"code": "CM", "name": "Castilla-La Mancha"},
                    {"code": "CT", "name": "Cataluña"},
                    {"code": "CE", "name": "Ceuta"},
                    {"code": "EX", "name": "Extremadura"},
                    {"code": "GA", "name": "Galicia"},
                    {"code": "MD", "name": "Madrid"},
                    {"code": "ML", "name": "Melilla"},
                    {"code": "MC", "name": "Murcia"},
                    {"code": "NC", "name": "Navarra"},
                    {"code": "PV", "name": "País Vasco"},
                    {"code": "RI", "name": "La Rioja"},
                    {"code": "VC", "name": "Valencia"}
                ],
                "US": [
                    {"code": "CA", "name": "California"},
                    {"code": "TX", "name": "Texas"},
                    {"code": "FL", "name": "Florida"},
                    {"code": "NY", "name": "Nueva York"},
                    {"code": "IL", "name": "Illinois"},
                    {"code": "PA", "name": "Pensilvania"},
                    {"code": "OH", "name": "Ohio"},
                    {"code": "GA", "name": "Georgia"},
                    {"code": "NC", "name": "Carolina del Norte"},
                    {"code": "MI", "name": "Míchigan"}
                ]
            }
            
            if country_code and country_code in regions_data:
                regions = regions_data[country_code]
            else:
                # Si no se especifica país o no está en la lista, devolver todos
                regions = []
                for country_regions in regions_data.values():
                    regions.extend(country_regions)
            
            logger.info("Regions retrieved", country_code=country_code, count=len(regions))
            
            return regions
            
        except Exception as e:
            logger.error("Error getting regions", error=str(e))
            raise GeolocationError("Error retrieving regions")
    
    async def get_cities(
        self,
        country_code: Optional[str] = None,
        region_code: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Obtener lista de ciudades"""
        try:
            # Lista básica de ciudades (en producción se obtendría de una API)
            cities_data = {
                "ES": [
                    {"name": "Madrid", "region": "MD", "coordinates": [-3.7038, 40.4168]},
                    {"name": "Barcelona", "region": "CT", "coordinates": [2.1734, 41.3851]},
                    {"name": "Valencia", "region": "VC", "coordinates": [-0.3763, 39.4699]},
                    {"name": "Sevilla", "region": "AN", "coordinates": [-5.9845, 37.3891]},
                    {"name": "Zaragoza", "region": "AR", "coordinates": [-0.8891, 41.6488]},
                    {"name": "Málaga", "region": "AN", "coordinates": [-4.4214, 36.7213]},
                    {"name": "Murcia", "region": "MC", "coordinates": [-1.1307, 37.9922]},
                    {"name": "Palma", "region": "IB", "coordinates": [2.6502, 39.5696]},
                    {"name": "Las Palmas", "region": "CN", "coordinates": [-15.4300, 28.1248]},
                    {"name": "Bilbao", "region": "PV", "coordinates": [-2.9253, 43.2627]}
                ],
                "US": [
                    {"name": "New York", "region": "NY", "coordinates": [-74.0060, 40.7128]},
                    {"name": "Los Angeles", "region": "CA", "coordinates": [-118.2437, 34.0522]},
                    {"name": "Chicago", "region": "IL", "coordinates": [-87.6298, 41.8781]},
                    {"name": "Houston", "region": "TX", "coordinates": [-95.3698, 29.7604]},
                    {"name": "Phoenix", "region": "AZ", "coordinates": [-112.0740, 33.4484]},
                    {"name": "Philadelphia", "region": "PA", "coordinates": [-75.1652, 39.9526]},
                    {"name": "San Antonio", "region": "TX", "coordinates": [-98.4936, 29.4241]},
                    {"name": "San Diego", "region": "CA", "coordinates": [-117.1611, 32.7157]},
                    {"name": "Dallas", "region": "TX", "coordinates": [-96.7970, 32.7767]},
                    {"name": "San Jose", "region": "CA", "coordinates": [-121.8863, 37.3382]}
                ]
            }
            
            cities = []
            
            if country_code and country_code in cities_data:
                country_cities = cities_data[country_code]
                
                if region_code:
                    cities = [city for city in country_cities if city["region"] == region_code]
                else:
                    cities = country_cities
            else:
                # Si no se especifica país, devolver todas las ciudades
                for country_cities in cities_data.values():
                    cities.extend(country_cities)
            
            # Limitar resultados
            cities = cities[:limit]
            
            logger.info(
                "Cities retrieved",
                country_code=country_code,
                region_code=region_code,
                count=len(cities)
            )
            
            return cities
            
        except Exception as e:
            logger.error("Error getting cities", error=str(e))
            raise GeolocationError("Error retrieving cities")
    
    async def calculate_distance(
        self,
        point1: GeoLocation,
        point2: GeoLocation
    ) -> Dict[str, Any]:
        """Calcular distancia entre dos puntos geográficos"""
        try:
            from geopy.distance import geodesic
            
            # Validar que ambos puntos tengan coordenadas
            if not point1.coordinates or not point2.coordinates:
                raise ValidationError("Both points must have coordinates")
            
            if len(point1.coordinates) != 2 or len(point2.coordinates) != 2:
                raise ValidationError("Both points must have exactly 2 coordinates")
            
            # Calcular distancia usando la fórmula de Haversine
            distance = geodesic(
                (point1.coordinates[1], point1.coordinates[0]),  # (lat, lon)
                (point2.coordinates[1], point2.coordinates[0])   # (lat, lon)
            ).kilometers
            
            result = {
                "distance_km": round(distance, 2),
                "distance_miles": round(distance * 0.621371, 2),
                "point1": {
                    "coordinates": point1.coordinates,
                    "type": point1.type
                },
                "point2": {
                    "coordinates": point2.coordinates,
                    "type": point2.type
                }
            }
            
            logger.info(
                "Distance calculated",
                distance_km=distance,
                point1=point1.coordinates,
                point2=point2.coordinates
            )
            
            return result
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error("Error calculating distance", error=str(e))
            raise GeolocationError("Error calculating distance")
