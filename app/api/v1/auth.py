from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import auth_service
from app.models.token import Token
from app.models.user import UserRegister
from app.db.database import GetSession

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(user_in: UserRegister, db: GetSession):
    return await auth_service.register(db, user_in.dict())


@router.post("/login", response_model=Token)
async def login(db: GetSession, form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.authenticate(
        db, 
        username_or_email=form_data.username, 
        password=form_data.password
    )
