from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.core import User
from app.core.security import get_password_hash

class UserService:
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        return await db.get(User, user_id)

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
    async def create(db: AsyncSession, user_data: dict) -> User:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        db_user = User(**user_data)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

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

    @staticmethod
    async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        statement = select(User).offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

user_service = UserService()