from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.security import verify_password, create_access_token
from app.services.user_service import user_service
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.models.token import Token

class AuthService:
    @staticmethod
    async def authenticate(db: AsyncSession, username_or_email: str, password: str) -> Token:
        user = await user_service.get_by_username(db, username_or_email)
        
        if not user:
            user = await user_service.get_by_email(db, username_or_email)
            
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Incorrect username/email or password")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer"
        )

    @staticmethod
    async def register(db: AsyncSession, user_data: dict) -> dict:
        await user_service.create(db, user_data)
        return {"message": "User created successfully"}

auth_service = AuthService()
