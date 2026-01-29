import asyncio
import logging
from app.db.database import init_db, async_session_maker
from app.services.user_service import UserService
from app.config import settings
from app.models.core import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_admin():
    async with async_session_maker() as db:
        admin_user = await UserService.get_by_email(db, settings.ADMIN_EMAIL)
        if not admin_user:
            logger.info(f"Creating default admin user: {settings.ADMIN_EMAIL}")
            admin_in = {
                "email": settings.ADMIN_EMAIL,
                "username": settings.ADMIN_USERNAME,
                "password": settings.ADMIN_PASSWORD,
                "full_name": "System Administrator",
                "is_active": True,
                "is_admin": True
            }
            await UserService.create(db, admin_in)
            logger.info("Admin user created successfully.")
        else:
            logger.info("Admin user already exists.")

async def main():
    logger.info("Initializing database...")
    await init_db()
    await create_admin()
    logger.info("Database initialization complete.")

if __name__ == "__main__":
    asyncio.run(main())
