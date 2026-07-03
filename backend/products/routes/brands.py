# app/api/routes/brands.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from datetime import datetime

from products.schemas.brand import Brand, BrandCreate, BrandUpdate
from products.services.brand_service import BrandService
from auth.jwt_handler import check_admin_permissions

router = APIRouter()

@router.post("/", response_model=Brand, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand: BrandCreate,
    current_user = Depends(check_admin_permissions),
    service: BrandService = Depends()
):
    """Create a new brand (Admin only)"""
    existing = await service.get_brand_by_name(brand.name)
    if existing:
        raise HTTPException(status_code=400, detail="Brand with this name already exists")
    
    return await service.create_brand(brand, current_user["_id"])

@router.get("/", response_model=List[Brand])
async def get_brands(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    service: BrandService = Depends()
):
    """Get all brands with filtering"""
    return await service.get_brands(skip, limit, is_active)

@router.get("/{brand_id}", response_model=Brand)
async def get_brand(
    brand_id: str,
    service: BrandService = Depends()
):
    """Get a single brand by ID"""
    brand = await service.get_brand(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.put("/{brand_id}", response_model=Brand)
async def update_brand(
    brand_id: str,
    brand: BrandUpdate,
    current_user = Depends(check_admin_permissions),
    service: BrandService = Depends()
):
    """Update a brand (Admin only)"""
    updated = await service.update_brand(brand_id, brand, current_user["_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Brand not found")
    return updated

@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    brand_id: str,
    current_user = Depends(check_admin_permissions),
    service: BrandService = Depends()
):
    """Soft delete a brand (Admin only)"""
    deleted = await service.delete_brand(brand_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Brand not found")
    return None

@router.get("/{brand_id}/products")
async def get_brand_products(
    brand_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: BrandService = Depends()
):
    """Get all products for a brand"""
    return await service.get_brand_products(brand_id, skip, limit)