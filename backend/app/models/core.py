from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.core.enums import ProductType, OrderStatus

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
    size_ml: int 
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

class CartItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    cart_id: UUID = Field(foreign_key="cart.id", index=True)
    product_id: UUID = Field(foreign_key="product.id")
    quantity: int = Field(default=1)
    price_at_addition: float 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    cart: "Cart" = Relationship(back_populates="items")
    product: "Product" = Relationship()

class Cart(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship()
    items: List[CartItem] = Relationship(back_populates="cart")

class OrderItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="order.id", index=True)
    product_id: UUID = Field(foreign_key="product.id")
    quantity: int
    price_at_purchase: float
    
    # Relationships
    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship()

class Order(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    total_amount: float
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    whatsapp_message_sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship()
    items: List[OrderItem] = Relationship(back_populates="order")
