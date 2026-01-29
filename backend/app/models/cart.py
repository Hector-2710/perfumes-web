from sqlmodel import SQLModel
from typing import List, Optional
from uuid import UUID

class CartItemCreate(SQLModel):
    product_id: UUID
    quantity: int

class CartItemUpdate(SQLModel):
    quantity: int

class ProductInCart(SQLModel):
    id: UUID
    name: str
    brand: str
    price: float
    image_url: Optional[str] = None

class CartItemResponse(SQLModel):
    id: UUID
    product: ProductInCart
    quantity: int
    price_at_addition: float
    subtotal: float

class CartResponse(SQLModel):
    id: UUID
    items: List[CartItemResponse]
    total_amount: float
    total_items: int
    


