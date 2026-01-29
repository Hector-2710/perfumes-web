from typing import Tuple
from uuid import UUID
from sqlmodel import select, and_
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.core import Cart, CartItem
from app.models.cart import CartResponse, CartItemResponse, ProductInCart
from app.services.product_service import product_service
from app.core.exceptions import OutOfStockError, EntityNotFoundError, PermissionDeniedError

class CartService:
    @staticmethod
    async def get_or_create_cart(db: AsyncSession, user_id: UUID) -> Cart:
        statement = select(Cart).where(Cart.user_id == user_id).options(
            selectinload(Cart.items).selectinload(CartItem.product)
        )
        result = await db.execute(statement)
        cart = result.scalar_one_or_none()
        
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)
            statement = select(Cart).where(Cart.id == cart.id).options(
                selectinload(Cart.items).selectinload(CartItem.product)
            )
            result = await db.execute(statement)
            cart = result.scalar_one()
        
        return cart

    async def get_cart_for_user(self, db: AsyncSession, user_id: UUID) -> CartResponse:
        cart = await self.get_or_create_cart(db, user_id)
        total_amount, total_items = self.calculate_total(cart)
        
        items_response = []
        for item in cart.items:
            items_response.append(CartItemResponse(
                id=item.id,
                product=ProductInCart(
                    id=item.product.id,
                    name=item.product.name,
                    brand=item.product.brand,
                    price=item.product.price,
                    image_url=item.product.image_url
                ),
                quantity=item.quantity,
                price_at_addition=item.price_at_addition,
                subtotal=item.quantity * item.price_at_addition
            ))
            
        return CartResponse(
            id=cart.id,
            items=items_response,
            total_amount=total_amount,
            total_items=total_items
        )

    @staticmethod
    async def add_item(db: AsyncSession, cart_id: UUID, product_id: UUID, quantity: int) -> CartItem:
        product = await product_service.get_by_id(db, product_id)
        if product.stock_quantity < quantity:
            raise OutOfStockError(product.name, quantity, product.stock_quantity)
            
        statement = select(CartItem).where(
            and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
        )
        result = await db.execute(statement)
        cart_item = result.scalar_one_or_none()
        
        if cart_item:
            cart_item.quantity += quantity
            cart_item.price_at_addition = product.price
        else:
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                price_at_addition=product.price
            )
            db.add(cart_item)
            
        await db.commit()
        await db.refresh(cart_item)
        return cart_item

    async def update_cart_item(self, db: AsyncSession, user_id: UUID, item_id: UUID, quantity: int) -> None:
        cart_item = await db.get(CartItem, item_id)
        if not cart_item:
            raise EntityNotFoundError("CartItem", item_id)
            
        cart = await self.get_or_create_cart(db, user_id)
        if cart_item.cart_id != cart.id:
            raise PermissionDeniedError("Not authorized to update this item")
            
        product = await product_service.get_by_id(db, cart_item.product_id)
        if product.stock_quantity < quantity:
            raise OutOfStockError(product.name, quantity, product.stock_quantity)
            
        cart_item.quantity = quantity
        db.add(cart_item)
        await db.commit()

    async def remove_cart_item(self, db: AsyncSession, user_id: UUID, item_id: UUID) -> None:
        cart_item = await db.get(CartItem, item_id)
        if not cart_item:
            raise EntityNotFoundError("CartItem", item_id)
            
        cart = await self.get_or_create_cart(db, user_id)
        if cart_item.cart_id != cart.id:
            raise PermissionDeniedError("Not authorized to remove this item")
            
        await db.delete(cart_item)
        await db.commit()

    @staticmethod
    async def clear_cart(db: AsyncSession, cart_id: UUID) -> None:
        statement = select(CartItem).where(CartItem.cart_id == cart_id)
        result = await db.execute(statement)
        items = result.scalars().all()
        for item in items:
            await db.delete(item)
        await db.commit()

    @staticmethod
    def calculate_total(cart: Cart) -> Tuple[float, int]:
        total_amount = sum(item.quantity * item.price_at_addition for item in cart.items)
        total_items = sum(item.quantity for item in cart.items)
        return total_amount, total_items

cart_service = CartService()