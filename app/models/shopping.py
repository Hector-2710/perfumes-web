from datetime import datetime
from uuid import UUID, uuid4
from typing import List
from sqlmodel import SQLModel, Field, Relationship
from app.models.core import User, Product
from app.core.enums import OrderStatus

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
