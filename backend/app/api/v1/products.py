from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query
from app.models.core import ProductType
from app.services.product_service import product_service
from app.db.database import GetSession
from app.models.product import ProductResponse

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def read_products(
    db: GetSession,
    skip: int = 0,
    limit: int = 100,
    type: Optional[ProductType] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = Query(False),
):
    return await product_service.list_products(
        db, skip, limit, type, brand, search, min_price, max_price, in_stock_only
    )

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product_by_id(product_id: UUID, db: GetSession):
    return await product_service.get_by_id(db, product_id)

