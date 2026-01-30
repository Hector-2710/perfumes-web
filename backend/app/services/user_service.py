from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.core import User
from app.models.user import UserRegister
from app.core.security import get_password_hash
from app.core.exceptions import DuplicateEntityError

class UserService:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user_data: UserRegister) -> User:
        if await UserService.get_by_email(db, user_data.email):
            raise DuplicateEntityError("User", "email", user_data.email)
        if await UserService.get_by_username(db, user_data.username):
            raise DuplicateEntityError("User", "username", user_data.username)

        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update(db: AsyncSession, db_user: User, user_data: dict) -> User:
        if "password" in user_data:
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        
        for key, value in user_data.items():
            setattr(db_user, key, value)
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete(db: AsyncSession, db_user: User) -> None:
        await db.delete(db_user)
        await db.commit()

user_service = UserService()