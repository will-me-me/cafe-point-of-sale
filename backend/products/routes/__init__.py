from fastapi import APIRouter

from .products import router as products_router
from .categories import router as categories_router
from .brands import router as brands_router
from .suppliers import router as suppliers_router
from .settings import router as settings_router

router = APIRouter()

router.include_router(settings_router, prefix="/settings", tags=["Settings"])
router.include_router(products_router, prefix="/products", tags=["Products"])
router.include_router(categories_router, prefix="/categories", tags=["Categories"])
router.include_router(brands_router, prefix="/brands", tags=["Brands"])
router.include_router(suppliers_router, prefix="/suppliers", tags=["Suppliers"])