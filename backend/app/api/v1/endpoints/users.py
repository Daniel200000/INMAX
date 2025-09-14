"""
Endpoints para gestión de usuarios
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import structlog

from app.models.user import (
    User, UserCreate, UserUpdate, UserResponse, 
    UserLogin, Token
)
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.database import get_database
from app.core.exceptions import NotFoundError, ValidationError, UnauthorizedError

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db=Depends(get_database)
):
    """Registrar un nuevo usuario"""
    try:
        user_service = UserService(db)
        auth_service = AuthService()
        
        # Verificar si el usuario ya existe
        existing_user = await user_service.get_user_by_username(user_data.username)
        if existing_user:
            raise ValidationError("Username already exists")
        
        existing_email = await user_service.get_user_by_email(user_data.email)
        if existing_email:
            raise ValidationError("Email already exists")
        
        # Crear el usuario
        user = await user_service.create_user(user_data)
        
        logger.info(
            "User registered successfully",
            user_id=user.id,
            username=user.username
        )
        
        return UserResponse(**user.dict())
        
    except ValidationError as e:
        logger.error("Validation error registering user", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error registering user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user"
        )


@router.post("/login", response_model=Token)
async def login_user(
    login_data: UserLogin,
    db=Depends(get_database)
):
    """Iniciar sesión de usuario"""
    try:
        user_service = UserService(db)
        auth_service = AuthService()
        
        # Verificar credenciales
        user = await auth_service.authenticate_user(
            login_data.username, 
            login_data.password,
            user_service
        )
        
        if not user:
            raise UnauthorizedError("Invalid username or password")
        
        # Generar token
        token_data = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
        
        access_token = auth_service.create_access_token(token_data)
        
        # Actualizar último login
        await user_service.update_last_login(user.id)
        
        logger.info(
            "User logged in successfully",
            user_id=user.id,
            username=user.username
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=1800  # 30 minutos
        )
        
    except UnauthorizedError as e:
        logger.error("Authentication error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error logging in user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error logging in user"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_database)
):
    """Obtener información del usuario actual"""
    try:
        auth_service = AuthService()
        user_service = UserService(db)
        
        # Verificar token
        user_data = await auth_service.verify_token(credentials.credentials)
        user_id = user_data.get("user_id")
        
        if not user_id:
            raise UnauthorizedError("Invalid token")
        
        # Obtener usuario
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        logger.info(
            "Current user retrieved successfully",
            user_id=user.id,
            username=user.username
        )
        
        return UserResponse(**user.dict())
        
    except UnauthorizedError as e:
        logger.error("Authentication error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except NotFoundError as e:
        logger.error("User not found", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error getting current user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user information"
        )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_database)
):
    """Actualizar información del usuario actual"""
    try:
        auth_service = AuthService()
        user_service = UserService(db)
        
        # Verificar token
        user_data_token = await auth_service.verify_token(credentials.credentials)
        user_id = user_data_token.get("user_id")
        
        if not user_id:
            raise UnauthorizedError("Invalid token")
        
        # Verificar que el usuario existe
        existing_user = await user_service.get_user_by_id(user_id)
        if not existing_user:
            raise NotFoundError("User", user_id)
        
        # Verificar si el nuevo username ya existe (si se está cambiando)
        if user_data.username and user_data.username != existing_user.username:
            username_exists = await user_service.get_user_by_username(user_data.username)
            if username_exists:
                raise ValidationError("Username already exists")
        
        # Verificar si el nuevo email ya existe (si se está cambiando)
        if user_data.email and user_data.email != existing_user.email:
            email_exists = await user_service.get_user_by_email(user_data.email)
            if email_exists:
                raise ValidationError("Email already exists")
        
        # Actualizar usuario
        updated_user = await user_service.update_user(user_id, user_data)
        
        logger.info(
            "User updated successfully",
            user_id=user_id,
            username=updated_user.username
        )
        
        return UserResponse(**updated_user.dict())
        
    except UnauthorizedError as e:
        logger.error("Authentication error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except NotFoundError as e:
        logger.error("User not found", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except ValidationError as e:
        logger.error("Validation error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error updating user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_database)
):
    """Eliminar el usuario actual"""
    try:
        auth_service = AuthService()
        user_service = UserService(db)
        
        # Verificar token
        user_data = await auth_service.verify_token(credentials.credentials)
        user_id = user_data.get("user_id")
        
        if not user_id:
            raise UnauthorizedError("Invalid token")
        
        # Verificar que el usuario existe
        existing_user = await user_service.get_user_by_id(user_id)
        if not existing_user:
            raise NotFoundError("User", user_id)
        
        # Eliminar usuario
        await user_service.delete_user(user_id)
        
        logger.info(
            "User deleted successfully",
            user_id=user_id,
            username=existing_user.username
        )
        
    except UnauthorizedError as e:
        logger.error("Authentication error", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except NotFoundError as e:
        logger.error("User not found", error=str(e.message))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except Exception as e:
        logger.error("Error deleting user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )
