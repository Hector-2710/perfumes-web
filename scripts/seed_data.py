import asyncio
import logging
from app.db.database import async_session_maker
from app.services.product_service import ProductService
from app.models.core import ProductType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PERFUMES_SEED = [
    {
        "name": "Sauvage",
        "brand": "Dior",
        "type": ProductType.SEALED,
        "size_ml": 100,
        "price": 120000,
        "stock_quantity": 5,
        "description": "Fresco, ambarino y amaderado. Una composición rotunda para un hombre auténtico.",
        "fragrance_family": "Oriental Fougère",
        "notes_top": "Bergamota de Calabria",
        "notes_heart": "Pimienta de Sichuan",
        "notes_base": "Ambroxan"
    },
    {
        "name": "Sauvage",
        "brand": "Dior",
        "type": ProductType.DECANT,
        "size_ml": 5,
        "price": 12000,
        "stock_quantity": 20,
        "description": "Muestra de 5ml de Sauvage Dior. Ideal para probar antes de comprar el frasco completo.",
        "fragrance_family": "Oriental Fougère"
    },
    {
        "name": "Bleu de Chanel",
        "brand": "Chanel",
        "type": ProductType.SEALED,
        "size_ml": 100,
        "price": 135000,
        "stock_quantity": 3,
        "description": "El elogio de la libertad masculina en una fragancia amaderada aromática de estela cautivadora.",
        "fragrance_family": "Amaderada Aromática",
        "notes_top": "Limón, Menta, Pimienta Rosa",
        "notes_heart": "Jengibre, Iso E Super, Jazmín",
        "notes_base": "Incienso, Vetiver, Cedro, Sándalo"
    },
    {
        "name": "Eros",
        "brand": "Versace",
        "type": ProductType.SEALED,
        "size_ml": 100,
        "price": 85000,
        "stock_quantity": 8,
        "description": "Masculina y segura, Eros es una fragancia sensual que fusiona notas amaderadas, orientales y frescas.",
        "fragrance_family": "Aromática Fougère"
    },
    {
        "name": "Eros",
        "brand": "Versace",
        "type": ProductType.DECANT,
        "size_ml": 5,
        "price": 8000,
        "stock_quantity": 15,
        "description": "Muestra de 5ml de Versace Eros.",
        "fragrance_family": "Aromática Fougère"
    },
    {
        "name": "Layton",
        "brand": "Parfums de Marly",
        "type": ProductType.SEALED,
        "size_ml": 125,
        "price": 240000,
        "stock_quantity": 2,
        "description": "Una fragancia adictiva y floral con una firma olfativa intensa.",
        "fragrance_family": "Oriental Floral"
    },
    {
        "name": "Layton",
        "brand": "Parfums de Marly",
        "type": ProductType.DECANT,
        "size_ml": 5,
        "price": 25000,
        "stock_quantity": 10,
        "description": "Muestra de 5ml de Layton. Lujo nicho a tu alcance.",
        "fragrance_family": "Oriental Floral"
    }
]

async def seed_data():
    async with async_session_maker() as db:
        logger.info("Seeding initial product data...")
        for perfume in PERFUMES_SEED:
            # Check if product already exists to avoid duplicates in dev
            from sqlmodel import select
            from app.models.core import Product
            statement = select(Product).where(
                Product.name == perfume["name"], 
                Product.brand == perfume["brand"],
                Product.type == perfume["type"]
            )
            result = await db.execute(statement)
            if not result.scalar_one_or_none():
                await ProductService.create(db, perfume)
                logger.info(f"Added product: {perfume['brand']} {perfume['name']} ({perfume['type']})")
            else:
                logger.info(f"Product already exists: {perfume['brand']} {perfume['name']}")
        
        logger.info("Data seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
