from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from uuid import UUID

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserRegister(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: UUID


