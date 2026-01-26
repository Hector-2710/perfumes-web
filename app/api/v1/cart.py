from uuid import UUID
from fastapi import APIRouter
from app.models.shopping import CartItem
from app.services.cart_service import cart_service
from app.services.product_service import product_service
from app.db.database import GetSession
from app.api.deps import GetCurrentUser
from app.core.exceptions import PermissionDeniedError, EntityNotFoundError
from app.models.cart import CartItemCreate, CartItemUpdate, CartResponse

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def read_cart(db: GetSession, current_user: GetCurrentUser):
    cart = await cart_service.get_or_create_cart(db, current_user.id)
    total_amount, total_items = cart_service.calculate_total(cart)
    
    items_response = []
    for item in cart.items:
        product = await product_service.get_by_id(db, item.product_id)
        items_response.append({
            "id": item.id,
            "product": product,
            "quantity": item.quantity,
            "price_at_addition": item.price_at_addition,
            "subtotal": item.quantity * item.price_at_addition
        })
        
    return {
        "id": cart.id,
        "items": items_response,
        "total_amount": total_amount,
        "total_items": total_items
    }

@router.post("/items", response_model=dict)
async def add_cart_item(item_in: CartItemCreate, db: GetSession, current_user: GetCurrentUser):
    cart = await cart_service.get_or_create_cart(db, current_user.id)
    await cart_service.add_item(db, cart.id, item_in.product_id, item_in.quantity)
    return {"message": "Item added to cart"}

@router.put("/items/{item_id}", response_model=dict)
async def update_cart_item(item_id: UUID, item_in: CartItemUpdate, db: GetSession, current_user: GetCurrentUser):
    cart_item = await db.get(CartItem, item_id)
    if not cart_item:
        raise EntityNotFoundError("CartItem", item_id)
        
    cart = await cart_service.get_or_create_cart(db, current_user.id)
    if cart_item.cart_id != cart.id:
        raise PermissionDeniedError("Not authorized to update this item")
        
    await cart_service.update_item(db, cart_item, item_in.quantity)
    return {"message": "Item updated"}

@router.delete("/items/{item_id}", response_model=dict)
async def remove_cart_item(item_id: UUID, db: GetSession, current_user: GetCurrentUser):
    cart_item = await db.get(CartItem, item_id)
    if not cart_item:
        raise EntityNotFoundError("CartItem", item_id)
        
    cart = await cart_service.get_or_create_cart(db, current_user.id)
    if cart_item.cart_id != cart.id:
        raise PermissionDeniedError("Not authorized to remove this item")
        
    await cart_service.remove_item(db, cart_item)
    return {"message": "Item removed"}

@router.delete("/", response_model=dict)
async def clear_cart(db: GetSession, current_user: GetCurrentUser):
    cart = await cart_service.get_or_create_cart(db, current_user.id)
    await cart_service.clear_cart(db, cart.id)
    return {"message": "Cart cleared"}
