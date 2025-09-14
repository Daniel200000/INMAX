"""
Servicio de autenticación y autorización
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import structlog

from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ValidationError

logger = structlog.get_logger()


class AuthService:
    """Servicio para autenticación y autorización"""
    
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Crear token de acceso JWT"""
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
            to_encode.update({"exp": expire})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            
            logger.info("Access token created successfully", user_id=data.get("user_id"))
            
            return encoded_jwt
            
        except Exception as e:
            logger.error("Error creating access token", error=str(e))
            raise ValidationError("Error creating access token")
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Verificar que el token no haya expirado
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                raise UnauthorizedError("Token has expired")
            
            logger.info("Token verified successfully", user_id=payload.get("user_id"))
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise UnauthorizedError("Token has expired")
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            raise UnauthorizedError("Invalid token")
        except Exception as e:
            logger.error("Error verifying token", error=str(e))
            raise UnauthorizedError("Error verifying token")
    
    async def authenticate_user(
        self, 
        username: str, 
        password: str, 
        user_service
    ) -> Optional[Any]:
        """Autenticar usuario con credenciales"""
        try:
            # Obtener usuario por username
            user = await user_service.get_user_by_username(username)
            if not user:
                logger.warning("User not found", username=username)
                return None
            
            # Verificar contraseña
            if not await user_service.verify_password(password, user.hashed_password):
                logger.warning("Invalid password", username=username)
                return None
            
            # Verificar que el usuario esté activo
            if user.status != "active":
                logger.warning("User account is not active", username=username, status=user.status)
                return None
            
            logger.info("User authenticated successfully", user_id=user.id, username=username)
            
            return user
            
        except Exception as e:
            logger.error("Error authenticating user", username=username, error=str(e))
            return None
    
    def hash_password(self, password: str) -> str:
        """Hashear contraseña"""
        try:
            from passlib.context import CryptContext
            
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed = pwd_context.hash(password)
            
            return hashed
            
        except Exception as e:
            logger.error("Error hashing password", error=str(e))
            raise ValidationError("Error hashing password")
    
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        try:
            from passlib.context import CryptContext
            
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            is_valid = pwd_context.verify(plain_password, hashed_password)
            
            return is_valid
            
        except Exception as e:
            logger.error("Error verifying password", error=str(e))
            return False
    
    def create_password_reset_token(self, user_id: str) -> str:
        """Crear token para reset de contraseña"""
        try:
            data = {
                "user_id": user_id,
                "type": "password_reset",
                "exp": datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
            }
            
            token = jwt.encode(data, self.secret_key, algorithm=self.algorithm)
            
            logger.info("Password reset token created", user_id=user_id)
            
            return token
            
        except Exception as e:
            logger.error("Error creating password reset token", error=str(e))
            raise ValidationError("Error creating password reset token")
    
    async def verify_password_reset_token(self, token: str) -> Optional[str]:
        """Verificar token de reset de contraseña"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Verificar que sea un token de reset de contraseña
            if payload.get("type") != "password_reset":
                raise UnauthorizedError("Invalid token type")
            
            # Verificar que no haya expirado
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                raise UnauthorizedError("Token has expired")
            
            user_id = payload.get("user_id")
            if not user_id:
                raise UnauthorizedError("Invalid token")
            
            logger.info("Password reset token verified", user_id=user_id)
            
            return user_id
            
        except jwt.ExpiredSignatureError:
            logger.error("Password reset token has expired")
            raise UnauthorizedError("Token has expired")
        except jwt.InvalidTokenError:
            logger.error("Invalid password reset token")
            raise UnauthorizedError("Invalid token")
        except Exception as e:
            logger.error("Error verifying password reset token", error=str(e))
            raise UnauthorizedError("Error verifying token")
