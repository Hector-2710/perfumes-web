from typing import List, Optional
from uuid import UUID
import os
from sqlmodel import select, or_, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.core import Product, ProductType
from app.core.exceptions import ProductNotFoundError
import csv
import io
from datetime import datetime

class ProductService:
    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: UUID) -> Product:
        product = await db.get(Product, product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    async def list_products(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        type: Optional[ProductType] = None,
        brand: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock_only: bool = False
    ) -> List[Product]:
        statement = select(Product)
        
        conditions = []
        if type:
            conditions.append(Product.type == type)
        if brand:
            conditions.append(Product.brand.ilike(f"%{brand}%"))
        if search:
            conditions.append(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                    Product.brand.ilike(f"%{search}%")
                )
            )
        if min_price is not None:
            conditions.append(Product.price >= min_price)
        if max_price is not None:
            conditions.append(Product.price <= max_price)
        if in_stock_only:
            conditions.append(Product.stock_quantity > 0)
        
        if conditions:
            statement = statement.where(and_(*conditions))
            
        statement = statement.offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def sync_from_csv(self, db: AsyncSession) -> dict:
        csv_path = "perfumes.csv"
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                content = f.read()
                return await self.import_from_csv(db, content)
        return {"message": "CSV file not found, no sync performed"}


    @staticmethod
    async def import_from_csv(db: AsyncSession, file_content: bytes) -> dict:
        content = file_content.decode("utf-8")
        csv_file = io.StringIO(content)
        reader = csv.DictReader(csv_file)
        
        column_mapping = {
            "Nombre": "name",
            "Marca": "brand",
            "Tipo": "type",
            "ML": "size_ml",
            "Precio": "price",
            "Stock": "stock_quantity",
            "Descripcion": "description",
            "Familia Olfativa": "fragrance_family",
            "Notas Salida": "notes_top",
            "Notas Corazon": "notes_heart",
            "Notas Fondo": "notes_base"
        }

        summary = {"added": 0, "updated": 0, "errors": []}

        for index, row in enumerate(reader):
            try:
                mapped_row = {column_mapping.get(k, k): v for k, v in row.items()}
                
                name = mapped_row.get("name")
                brand = mapped_row.get("brand")
                
                if not name or not brand:
                    continue
                
                statement = select(Product).where(
                    and_(
                        Product.name == str(name),
                        Product.brand == str(brand)
                    )
                )
                result = await db.execute(statement)
                db_product = result.scalars().first()

                product_data = {
                    "name": str(name),
                    "brand": str(brand),
                    "type": mapped_row.get("type", ProductType.NONE),
                    "size_ml": int(mapped_row.get("size_ml", 0)) if mapped_row.get("size_ml") else 0,
                    "price": float(mapped_row.get("price", 0)) if mapped_row.get("price") else 0.0,
                    "stock_quantity": int(mapped_row.get("stock_quantity", 0)) if mapped_row.get("stock_quantity") else 0,
                    "description": str(mapped_row.get("description", "")),
                    "fragrance_family": str(mapped_row.get("fragrance_family", "")),
                    "notes_top": str(mapped_row.get("notes_top", "")) if mapped_row.get("notes_top") else None,
                    "notes_heart": str(mapped_row.get("notes_heart", "")) if mapped_row.get("notes_heart") else None,
                    "notes_base": str(mapped_row.get("notes_base", "")) if mapped_row.get("notes_base") else None,
                    "updated_at": datetime.utcnow()
                }

                if db_product:
                    for key, value in product_data.items():
                        setattr(db_product, key, value)
                    db.add(db_product)
                    summary["updated"] += 1
                else:
                    new_product = Product(**product_data)
                    db.add(new_product)
                    summary["added"] += 1

            except Exception as e:
                summary["errors"].append(f"Error en fila {index + 2}: {str(e)}")

        await db.commit()
        return summary

product_service = ProductService()