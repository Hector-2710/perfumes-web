from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.database import GetSession
from app.core.config import settings
from app.core.security import decode_token
from app.models.core import User
from typing import Annotated

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)

async def get_current_user(db: GetSession, token: str = Depends(reusable_oauth2)) -> User:
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject",
        )
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    return user

async def get_current_active_admin(db: GetSession, current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user


GetCurrentUser = Annotated[User, Depends(get_current_user)]
GetCurrentActiveAdmin = Annotated[User, Depends(get_current_active_admin)]
