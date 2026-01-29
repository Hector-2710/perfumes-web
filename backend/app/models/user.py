from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID
from pydantic import EmailStr

class UserRegister(SQLModel):
    email: EmailStr
    username: str
    password: str
    full_name: str = None

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class UserResponse(SQLModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: Optional[str]
    phone: Optional[str]
    is_active: bool
    is_admin: bool