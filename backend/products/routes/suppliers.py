# app/api/routes/suppliers.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from datetime import datetime

from products.schemas.supplier import Supplier, SupplierCreate, SupplierUpdate, SupplierProduct
from products.services.supplier_service import SupplierService
from auth.jwt_handler import check_admin_permissions, get_current_user

router = APIRouter()

@router.post("/", response_model=Supplier, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier: SupplierCreate,
    current_user = Depends(check_admin_permissions),
    service: SupplierService = Depends()
):
    """Create a new supplier (Admin only)"""
    existing = await service.get_supplier_by_name(supplier.name)
    if existing:
        raise HTTPException(status_code=400, detail="Supplier with this name already exists")
    
    return await service.create_supplier(supplier, current_user["_id"])

@router.get("/", response_model=List[Supplier])
async def get_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    service: SupplierService = Depends()
):
    """Get all suppliers with filtering"""
    return await service.get_suppliers(skip, limit, is_active, search)

@router.get("/{supplier_id}", response_model=Supplier)
async def get_supplier(
    supplier_id: str,
    service: SupplierService = Depends()
):
    """Get a single supplier by ID"""
    supplier = await service.get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=Supplier)
async def update_supplier(
    supplier_id: str,
    supplier: SupplierUpdate,
    current_user = Depends(check_admin_permissions),
    service: SupplierService = Depends()
):
    """Update a supplier (Admin only)"""
    updated = await service.update_supplier(supplier_id, supplier, current_user["_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: str,
    current_user = Depends(check_admin_permissions),
    service: SupplierService = Depends()
):
    """Soft delete a supplier (Admin only)"""
    deleted = await service.delete_supplier(supplier_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return None

@router.get("/{supplier_id}/products")
async def get_supplier_products(
    supplier_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: SupplierService = Depends()
):
    """Get all products from a supplier"""
    return await service.get_supplier_products(supplier_id, skip, limit)

@router.get("/{supplier_id}/purchases")
async def get_supplier_purchases(
    supplier_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: SupplierService = Depends()
):
    """Get all purchase orders from a supplier"""
    return await service.get_supplier_purchases(supplier_id, skip, limit)

@router.post("/{supplier_id}/rate")
async def rate_supplier(
    supplier_id: str,
    rating: float = Query(..., ge=0, le=5),
    current_user = Depends(get_current_user),
    service: SupplierService = Depends()
):
    """Rate a supplier (1-5)"""
    updated = await service.rate_supplier(supplier_id, rating)
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"message": "Supplier rated successfully", "rating": rating}