from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.shopping import Cart, Order
from app.core.enums import ProductType

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    cart: Optional["Cart"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")

class ProductBase(SQLModel):
    name: str = Field(index=True)
    brand: str = Field(index=True)
    type: ProductType = Field(default=ProductType.NONE)
    size_ml: int = 
    price: float
    stock_quantity: int
    description: str
    fragrance_family: str
    notes_top: Optional[str] = None
    notes_heart: Optional[str] = None
    notes_base: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

class Product(ProductBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    cart_items: List["CartItem"] = Relationship(back_populates="product")
