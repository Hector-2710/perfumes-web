from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.core import User
from app.services.cart_service import cart_service
from app.services.whatsapp_service import whatsapp_service
from app.core.config import settings
from app.core.exceptions import EssenciaRabeException, OutOfStockError

class OrderService:
    @staticmethod
    async def prepare_checkout(db: AsyncSession, user: User) -> dict:
        """
        Checkout process:
        1. Get current cart
        2. Validate stock
        3. Generate WhatsApp message
        4. Return message and WhatsApp link
        """
        cart = await cart_service.get_or_create_cart(db, user.id)
        if not cart.items:
            raise EssenciaRabeException("Cart is empty", status_code=400)
        
        items_with_products = []
        for item in cart.items:
            product = item.product
            
            if product.stock_quantity < item.quantity:
                raise OutOfStockError(product.name, item.quantity, product.stock_quantity)
                
            items_with_products.append((product, item))
        
        # Generate message
        header = f"🌸 *Nuevo Pedido - Essenciarabe*\n\n"
        header += f"Hola Hector, me gustaría realizar un pedido:\n\n"
        header += f"👤 *Cliente:* {user.username}\n"
        header += f"📧 *Email:* {user.email}\n\n"
        header += f"🛒 *Detalle del Carrito:*\n"
        
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
