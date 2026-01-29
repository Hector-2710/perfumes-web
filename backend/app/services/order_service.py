from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.core import User
from app.services.cart_service import cart_service
from app.services.whatsapp_service import whatsapp_service
from app.core.config import settings
from app.core.exceptions import EssenciaRabeException, OutOfStockError

class OrderService:
    @staticmethod
    async def prepare_checkout(db: AsyncSession, user: User) -> dict:
        cart = await cart_service.get_or_create_cart(db, user.id)
        if not cart.items:
            raise EssenciaRabeException("Cart is empty", status_code=400)
        
        items_with_products = []
        for item in cart.items:
            product = item.product
            
            if product.stock_quantity < item.quantity:
                raise OutOfStockError(product.name, item.quantity, product.stock_quantity)
                
            items_with_products.append((product, item))
        
        header = whatsapp_service.generate_checkout_message(cart, user.username)
        body = whatsapp_service.format_order_summary(items_with_products)
        footer = f"\n\nQuedo atento a tus indicaciones de pago. ¡Gracias! ✨"
        
        full_message = header + body + footer
        whatsapp_link = whatsapp_service.generate_whatsapp_link(
            settings.WHATSAPP_PHONE_NUMBER, 
            full_message
        )
        
        return {
            "message": "Checkout prepared",
            "whatsapp_text": full_message,
            "whatsapp_link": whatsapp_link
        }

order_service = OrderService()
