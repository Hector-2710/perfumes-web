from uuid import UUID
from fastapi import APIRouter
from app.services.cart_service import cart_service
from app.db.database import GetSession
from app.api.deps import GetCurrentUser
from app.models.cart import CartItemCreate, CartItemUpdate, CartResponse

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def read_cart(db: GetSession, current_user: GetCurrentUser):
    return await cart_service.get_cart_for_user(db, current_user.id)

@router.post("/items", response_model=dict)
async def add_cart_item(item_in: CartItemCreate, db: GetSession, current_user: GetCurrentUser):
    cart = await cart_service.get_or_create_cart(db, current_user.id)
    await cart_service.add_item(db, cart.id, item_in.product_id, item_in.quantity)
    return {"message": "Item added to cart"}

@router.put("/items/{item_id}", response_model=dict)
async def update_cart_item(item_id: UUID, item_in: CartItemUpdate, db: GetSession, current_user: GetCurrentUser):
    await cart_service.update_cart_item(db, current_user.id, item_id, item_in.quantity)
    return {"message": "Item updated"}

@router.delete("/items/{item_id}", response_model=dict)
async def remove_cart_item(item_id: UUID, db: GetSession, current_user: GetCurrentUser):
    await cart_service.remove_cart_item(db, current_user.id, item_id)
    return {"message": "Item removed"}

@router.delete("/", response_model=dict)
async def clear_cart(db: GetSession, current_user: GetCurrentUser):
    cart = await cart_service.get_or_create_cart(db, current_user.id)
    await cart_service.clear_cart(db, cart.id)
    return {"message": "Cart cleared"}
