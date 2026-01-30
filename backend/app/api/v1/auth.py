from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import user_service
from app.services.auth_service import auth_service
from app.models.token import Token
from app.models.user import UserRegister, UserResponse
from app.db.database import GetSession

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserRegister, db: GetSession):
    return await user_service.create(db, user_in)


@router.post("/login", response_model=Token)
async def login(db: GetSession, form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.authenticate(db, form_data.username, form_data.password)
