from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import init_db, async_session_maker
from app.core.exceptions import EssenciaRabeException
from app.services.product_service import product_service

from app.api.v1 import auth, users, products, cart, orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    
    # Sync products from CSV on startup
    async with async_session_maker() as db:
        await product_service.sync_from_csv(db)
    
    yield
    # Shutdown logic (if any) can go here

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

@app.exception_handler(EssenciaRabeException)
async def essenciarabe_exception_handler(request: Request, exc: EssenciaRabeException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
        headers=exc.headers
    )

app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["users"])
app.include_router(products.router, prefix=f"{settings.API_V1_PREFIX}/products", tags=["products"])
app.include_router(cart.router, prefix=f"{settings.API_V1_PREFIX}/cart", tags=["cart"])
app.include_router(orders.router, prefix=f"{settings.API_V1_PREFIX}/orders", tags=["orders"])

# Set CORS middleware
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



