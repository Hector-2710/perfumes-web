from fastapi import APIRouter
from app.services.order_service import order_service
from app.db.database import GetSession
from app.api.deps import GetCurrentUser

router = APIRouter()

@router.post("/checkout", response_model=dict)
async def checkout(db: GetSession, current_user: GetCurrentUser):
    return await order_service.prepare_checkout(db, current_user)
