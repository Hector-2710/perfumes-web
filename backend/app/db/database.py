from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from sqlmodel import SQLModel
from typing import Annotated
from fastapi import Depends

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as eg:
        await eg.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    """Dependency for getting async database session"""
    async with async_session_maker() as session:
        yield session

GetSession = Annotated[AsyncSession, Depends(get_session)]