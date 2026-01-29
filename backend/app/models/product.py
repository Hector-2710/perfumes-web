from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID
from app.models.core import ProductType

class ProductCreate(SQLModel):
    name: str
    brand: str
    type: ProductType
    size_ml: int
    price: float
    stock_quantity: int
    description: str
    fragrance_family: str
    notes_top: Optional[str] = None
    notes_heart: Optional[str] = None
    notes_base: Optional[str] = None
    image_url: Optional[str] = None


class ProductResponse(ProductCreate):
    id: UUID
    is_active: bool