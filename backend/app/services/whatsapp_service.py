import urllib.parse
from typing import List
from app.models.core import Cart

class WhatsAppService:
    @staticmethod
    def generate_checkout_message(cart: Cart, user_full_name: str) -> str:
        message = f"🌸 *Nuevo Pedido - Essenciarabe*\n\n"
        message += f"Hola Hector, me gustaría realizar un pedido:\n\n"
        message += f"👤 *Cliente:* {user_full_name}\n"
        message += f"📅 *Fecha:* {cart.updated_at.strftime('%d/%m/%Y %H:%M')}\n\n"
        message += f"🛒 *Detalle del Carrito:*\n"
        
        total_amount = 0
        for item in cart.items:
            subtotal = item.quantity * item.price_at_addition
            total_amount += subtotal
            pass

        return message

    @staticmethod
    def generate_whatsapp_link(phone_number: str, text: str) -> str:
        encoded_text = urllib.parse.quote(text)
        clean_phone = phone_number.replace("+", "").replace(" ", "")
        return f"https://wa.me/{clean_phone}?text={encoded_text}"
        
    @staticmethod
    def format_order_summary(items_with_products: List[tuple]) -> str:
        summary = ""
        total = 0
        for product, item in items_with_products:
            subtotal = item.quantity * item.price_at_addition
            total += subtotal
            type_label = "Sellado" if product.type == "sealed" else "Decant 5ml"
            summary += f"- {product.brand} {product.name} ({type_label}) x{item.quantity}: ${subtotal:,.0f}\n"
        
        summary += f"\n💰 *Total a pagar: ${total:,.0f}*"
        return summary

whatsapp_service = WhatsAppService()