"""
Servicio para gestión de usuarios
"""

from datetime import datetime
from typing import Optional
from bson import ObjectId
import structlog

from app.models.user import User, UserCreate, UserUpdate
from app.core.database import get_database
from app.core.exceptions import NotFoundError, ValidationError, DatabaseError
from app.services.auth_service import AuthService

logger = structlog.get_logger()


class UserService:
    """Servicio para operaciones de usuarios"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.users
        self.auth_service = AuthService()
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Crear un nuevo usuario"""
        try:
            # Verificar si el username ya existe
            existing_username = await self.get_user_by_username(user_data.username)
            if existing_username:
                raise ValidationError("Username already exists")
            
            # Verificar si el email ya existe
            existing_email = await self.get_user_by_email(user_data.email)
            if existing_email:
                raise ValidationError("Email already exists")
            
            # Hashear contraseña
            hashed_password = self.auth_service.hash_password(user_data.password)
            
            # Preparar datos del usuario
            now = datetime.utcnow()
            user_dict = user_data.dict()
            user_dict.pop("password")  # Remover contraseña en texto plano
            user_dict.update({
                "hashed_password": hashed_password,
                "created_at": now,
                "updated_at": now,
                "last_login": None,
                "is_verified": False,
                "verification_token": None,
                "reset_token": None,
                "reset_token_expires": None
            })
            
            # Insertar en la base de datos
            result = await self.collection.insert_one(user_dict)
            
            # Obtener el usuario creado
            user = await self.get_user_by_id(str(result.inserted_id))
            
            logger.info(
                "User created successfully",
                user_id=user.id,
                username=user.username
            )
            
            return user
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error("Error creating user", error=str(e))
            raise DatabaseError("Error creating user")
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID"""
        try:
            if not ObjectId.is_valid(user_id):
                return None
            
            user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
            
            if not user_doc:
                return None
            
            user_doc["_id"] = str(user_doc["_id"])
            return User(**user_doc)
            
        except Exception as e:
            logger.error("Error getting user by id", user_id=user_id, error=str(e))
            raise DatabaseError("Error retrieving user")
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario"""
        try:
            user_doc = await self.collection.find_one({"username": username.lower()})
            
            if not user_doc:
                return None
            
            user_doc["_id"] = str(user_doc["_id"])
            return User(**user_doc)
            
        except Exception as e:
            logger.error("Error getting user by username", username=username, error=str(e))
            raise DatabaseError("Error retrieving user")
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        try:
            user_doc = await self.collection.find_one({"email": email.lower()})
            
            if not user_doc:
                return None
            
            user_doc["_id"] = str(user_doc["_id"])
            return User(**user_doc)
            
        except Exception as e:
            logger.error("Error getting user by email", email=email, error=str(e))
            raise DatabaseError("Error retrieving user")
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> User:
        """Actualizar un usuario"""
        try:
            # Verificar que el usuario existe
            existing_user = await self.get_user_by_id(user_id)
            if not existing_user:
                raise NotFoundError("User", user_id)
            
            # Preparar datos de actualización
            update_data = user_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            # Verificar si se está cambiando el username
            if "username" in update_data and update_data["username"] != existing_user.username:
                username_exists = await self.get_user_by_username(update_data["username"])
                if username_exists:
                    raise ValidationError("Username already exists")
                update_data["username"] = update_data["username"].lower()
            
            # Verificar si se está cambiando el email
            if "email" in update_data and update_data["email"] != existing_user.email:
                email_exists = await self.get_user_by_email(update_data["email"])
                if email_exists:
                    raise ValidationError("Email already exists")
                update_data["email"] = update_data["email"].lower()
            
            # Actualizar en la base de datos
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise NotFoundError("User", user_id)
            
            # Obtener el usuario actualizado
            updated_user = await self.get_user_by_id(user_id)
            
            logger.info(
                "User updated successfully",
                user_id=user_id,
                username=updated_user.username
            )
            
            return updated_user
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error("Error updating user", user_id=user_id, error=str(e))
            raise DatabaseError("Error updating user")
    
    async def delete_user(self, user_id: str) -> bool:
        """Eliminar un usuario"""
        try:
            # Verificar que el usuario existe
            existing_user = await self.get_user_by_id(user_id)
            if not existing_user:
                raise NotFoundError("User", user_id)
            
            # Eliminar de la base de datos
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            
            if result.deleted_count == 0:
                raise NotFoundError("User", user_id)
            
            logger.info(
                "User deleted successfully",
                user_id=user_id,
                username=existing_user.username
            )
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error deleting user", user_id=user_id, error=str(e))
            raise DatabaseError("Error deleting user")
    
    async def update_last_login(self, user_id: str) -> bool:
        """Actualizar último login del usuario"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            
            if result.matched_count == 0:
                raise NotFoundError("User", user_id)
            
            logger.info("Last login updated", user_id=user_id)
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error updating last login", user_id=user_id, error=str(e))
            raise DatabaseError("Error updating last login")
    
    async def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verificar contraseña del usuario"""
        try:
            return await self.auth_service.verify_password(password, hashed_password)
            
        except Exception as e:
            logger.error("Error verifying password", error=str(e))
            return False
    
    async def change_password(
        self, 
        user_id: str, 
        current_password: str, 
        new_password: str
    ) -> bool:
        """Cambiar contraseña del usuario"""
        try:
            # Obtener usuario
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            # Verificar contraseña actual
            if not await self.verify_password(current_password, user.hashed_password):
                raise ValidationError("Current password is incorrect")
            
            # Hashear nueva contraseña
            new_hashed_password = self.auth_service.hash_password(new_password)
            
            # Actualizar contraseña
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {
                    "hashed_password": new_hashed_password,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            if result.matched_count == 0:
                raise NotFoundError("User", user_id)
            
            logger.info("Password changed successfully", user_id=user_id)
            
            return True
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error("Error changing password", user_id=user_id, error=str(e))
            raise DatabaseError("Error changing password")
    
    async def reset_password(self, user_id: str, new_password: str) -> bool:
        """Resetear contraseña del usuario"""
        try:
            # Verificar que el usuario existe
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            # Hashear nueva contraseña
            new_hashed_password = self.auth_service.hash_password(new_password)
            
            # Actualizar contraseña y limpiar tokens de reset
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {
                    "hashed_password": new_hashed_password,
                    "reset_token": None,
                    "reset_token_expires": None,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            if result.matched_count == 0:
                raise NotFoundError("User", user_id)
            
            logger.info("Password reset successfully", user_id=user_id)
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Error resetting password", user_id=user_id, error=str(e))
            raise DatabaseError("Error resetting password")
