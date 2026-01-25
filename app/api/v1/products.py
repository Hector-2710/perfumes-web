from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, UploadFile, File
from app.models.core import ProductType
from app.services.product_service import product_service
from app.db.database import GetSession
from app.api.deps import GetCurrentUser
from app.models.product import ProductResponse
from app.core.exceptions import PermissionDeniedError, EssenciaRabeException

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
    """List products with optional filters. Public access."""
    return product_service.list_products(
        db, skip, limit, type, brand, search, min_price, max_price, in_stock_only
    )

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product_by_id(product_id: UUID, db: GetSession):
    """Get single product details. Public access."""
    return await product_service.get_by_id(db, product_id)

@router.post("/import-excel", response_model=dict)
async def import_products_excel(db: GetSession, current_user: GetCurrentUser, file: UploadFile = File(...)):
    """Import products from an Excel file. Upsert by Name + Brand. Admin only."""
    if not current_user.is_admin:
        raise PermissionDeniedError()
        
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise EssenciaRabeException("Invalid file format. Please upload an Excel file.", status_code=400)
    
    content = await file.read()
    summary = await product_service.import_from_excel(db, content)
    return summary
