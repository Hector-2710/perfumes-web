from fastapi import APIRouter
from app.services.user_service import user_service
from app.models.user import UserUpdate, UserResponse
from app.api.deps import GetCurrentUser
from app.db.database import GetSession

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: GetCurrentUser):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(user_in: UserUpdate, db: GetSession, current_user: GetCurrentUser):
    return await user_service.update(db, current_user, user_in.dict(exclude_unset=True))

@router.delete("/me", response_model=dict)
async def delete_user_me(db: GetSession, current_user: GetCurrentUser):
    await user_service.delete(db, current_user)
    return {"message": "User deleted successfully"}


