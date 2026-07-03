# app/api/routes/categories.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from datetime import datetime

from auth.jwt_handler import check_admin_permissions
from products.schemas.category import Category, CategoryCreate, CategoryUpdate, CategoryTree
from products.services.category_service import CategoryService

router = APIRouter()

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    current_user = Depends(check_admin_permissions),
    service: CategoryService = Depends()
):
    """Create a new category (Admin only)"""
    # Check if category with same name exists
    existing = await service.get_category_by_name(category.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    return await service.create_category(category, current_user["_id"])

@router.get("/", response_model=List[Category])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    parent_id: Optional[str] = None,
    service: CategoryService = Depends()
):
    """Get all categories with filtering"""
    return await service.get_categories(skip, limit, is_active, parent_id)

@router.get("/tree", response_model=List[CategoryTree])
async def get_category_tree(
    service: CategoryService = Depends()
):
    """Get category hierarchy as a tree"""
    return await service.get_category_tree()

@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: str,
    service: CategoryService = Depends()
):
    """Get a single category by ID"""
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: str,
    category: CategoryUpdate,
    current_user = Depends(check_admin_permissions),
    service: CategoryService = Depends()
):
    """Update a category (Admin only)"""
    updated = await service.update_category(category_id, category, current_user["_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    current_user = Depends(check_admin_permissions),
    service: CategoryService = Depends()
):
    """Soft delete a category (Admin only)"""
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return None

@router.post("/{category_id}/move")
async def move_category(
    category_id: str,
    new_parent_id: Optional[str] = None,
    current_user = Depends(check_admin_permissions),
    service: CategoryService = Depends()
):
    """Move a category to a different parent"""
    moved = await service.move_category(category_id, new_parent_id)
    if not moved:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category moved successfully"}

@router.get("/{category_id}/products")
async def get_category_products(
    category_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: CategoryService = Depends()
):
    """Get all products in a category"""
    return await service.get_category_products(category_id, skip, limit)