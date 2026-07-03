# app/api/routes/products.py
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Depends, status
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from auth.jwt_handler import get_current_user, get_product_service
from products.schemas.branch import BranchInventory
from products.schemas.product import Product, ProductCreate, ProductSearch, ProductUpdate, ProductVariantCreate, ProductVariantUpdate

from products.schemas.movement import InventoryMovement, MovementType
from products.service import ProductService


router = APIRouter()

# ============ PRODUCT CRUD ============

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    current_user = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    """Create a new product"""
    # Check if SKU already exists
    existing = await service.get_product_by_sku(product.sku)
    if existing:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    
    return await service.create_product(product, current_user["_id"])

@router.get("/", response_model=List[Product])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    query: Optional[str] = None,
    category_id: Optional[str] = None,
    brand_id: Optional[str] = None,
    supplier_id: Optional[str] = None,
    product_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    is_active: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    is_on_sale: Optional[bool] = None,
    service: ProductService = Depends(get_product_service)
):
    """Get all products with filtering"""
    search = ProductSearch(
        query=query,
        category_id=category_id,
        brand_id=brand_id,
        supplier_id=supplier_id,
        product_type=product_type,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        is_active=is_active,
        is_featured=is_featured,
        is_on_sale=is_on_sale
    )
    return await service.get_products(skip, limit, search)

@router.get("/search", response_model=List[Product])
async def search_products(
    q: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    service: ProductService = Depends(get_product_service)
):
    """Search products by name, SKU, barcode, or description"""
    return await service.search_products(q, limit)

@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    """Get a single product by ID"""
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/sku/{sku}", response_model=Product)
async def get_product_by_sku(
    sku: str,
    service: ProductService = Depends(get_product_service)
):
    """Get a product by SKU"""
    product = await service.get_product_by_sku(sku)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/barcode/{barcode}", response_model=Product)
async def get_product_by_barcode(
    barcode: str,
    service: ProductService = Depends(get_product_service)
):
    """Get a product by barcode"""
    product = await service.get_product_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: str,
    product: ProductUpdate,
    current_user = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    """Update a product"""
    updated = await service.update_product(product_id, product, current_user["_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    current_user = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    """Soft delete a product"""
    deleted = await service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None

@router.delete("/{product_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
async def permanently_delete_product(
    product_id: str,
    current_user = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    """Permanently delete a product (admin only)"""
    # TODO: Check if user is admin
    is_admin = current_user.get("role") == "admin"
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    
    deleted = await service.permanently_delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None

# ============ VARIANTS ============

@router.post("/{product_id}/variants", response_model=Product)
async def add_variant(
    product_id: str,
    variant: ProductVariantCreate,
    current_user = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    """Add a variant to a product"""
    updated = await service.add_variant(product_id, variant, current_user["_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.put("/{product_id}/variants/{variant_id}", response_model=Product)
async def update_variant(
    product_id: str,
    variant_id: str,
    variant: ProductVariantUpdate,
    current_user = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    """Update a product variant"""
    updated = await service.update_variant(product_id, variant_id, variant, current_user["_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Variant not found")
    return updated

@router.delete("/{product_id}/variants/{variant_id}", response_model=Product)
async def delete_variant(
    product_id: str,
    variant_id: str,
    service: ProductService = Depends(get_product_service)
):
    """Delete a product variant"""
    updated = await service.delete_variant(product_id, variant_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Variant not found")
    return updated

# ============ INVENTORY ============

@router.patch("/{product_id}/inventory", response_model=InventoryMovement)
async def update_inventory(
    product_id: str,
    quantity: int = Query(..., description="Positive for addition, negative for removal"),
    movement_type: MovementType = Query(...),
    reason: str = Query(..., min_length=1),
    variant_id: Optional[str] = None,
    branch_id: Optional[str] = None,
    reference_id: Optional[str] = None,
    batch_number: Optional[str] = None,
    serial_numbers: Optional[List[str]] = Query(None),
    current_user = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    """Update inventory quantity for a product"""
    if quantity == 0:
        raise HTTPException(status_code=400, detail="Quantity change must not be zero")
    print(type(product_id), product_id)
    
    return await service.update_inventory(
        product_id=str(product_id),
        quantity_change=quantity,
        movement_type=movement_type,
        reason=reason,
        user_id=str(current_user["_id"]),
        variant_id=variant_id,
        branch_id=branch_id,
        reference_id=reference_id,
        serial_numbers=serial_numbers or [],
        batch_number=batch_number
    )

@router.get("/{product_id}/movements", response_model=List[InventoryMovement])
async def get_product_movements(
    product_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ProductService = Depends(get_product_service)
):
    """Get inventory movements for a product"""
    return await service.get_movements(product_id, skip, limit)

# ============ BRANCH INVENTORY ============

@router.get("/branches/{branch_id}/inventory", response_model=List[BranchInventory])
async def get_branch_inventory(
    branch_id: str,
    product_id: Optional[str] = None,
    service: ProductService = Depends(get_product_service)
):
    """Get inventory for a specific branch"""
    return await service.get_branch_inventory(branch_id, product_id)

@router.patch("/branches/{branch_id}/inventory")
async def update_branch_inventory(
    branch_id: str,
    product_id: str,
    quantity: int = Query(...),
    variant_id: Optional[str] = None,
    reserved_change: int = Query(0),
    service: ProductService = Depends(get_product_service)
):
    """Update branch inventory"""
    return await service.update_branch_inventory(
        branch_id=branch_id,
        product_id=product_id,
        quantity_change=quantity,
        variant_id=variant_id,
        reserved_change=reserved_change
    )

# ============ FILE UPLOAD ============

@router.post("/upload-image")
async def upload_product_image(
    file: UploadFile = File(...),
    service: ProductService = Depends(get_product_service)
):
    """Upload a product image to Supabase"""
    try:
        url = await service.upload_to_supabase(file, "products")
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ BULK OPERATIONS ============

@router.post("/bulk/update-prices")
async def bulk_update_prices(
    product_ids: List[str],
    price_change_percent: float = Query(..., description="Positive for increase, negative for decrease"),
    service: ProductService = Depends(get_product_service)
):
    """Bulk update prices for multiple products"""
    updated = await service.bulk_update_prices(product_ids, price_change_percent)
    return {
        "updated_count": updated,
        "message": f"Updated {updated} products"
    }

@router.post("/bulk/update-stock-status")
async def bulk_update_stock_status(
    threshold: int = Query(10, ge=0),
    service: ProductService = Depends(get_product_service)
):
    """Bulk update stock status for all products"""
    updated = await service.bulk_update_stock_status(threshold)
    return {
        "updated_count": updated,
        "message": f"Updated stock status for {updated} products"
    }

# ============ REPORTS ============

@router.get("/reports/low-stock", response_model=List[Product])
async def get_low_stock_products(
    threshold: int = Query(10, ge=0),
    service: ProductService = Depends(get_product_service)
):
    """Get products with low stock"""
    return await service.get_low_stock_products(threshold)

@router.get("/reports/out-of-stock", response_model=List[Product])
async def get_out_of_stock_products(
    service: ProductService = Depends(get_product_service)
):
    """Get out of stock products"""
    return await service.get_out_of_stock_products()

@router.get("/reports/inventory-value")
async def get_inventory_value(
    service: ProductService = Depends(get_product_service)
):
    """Get total inventory value"""
    return await service.get_inventory_value()

@router.get("/reports/category-count")
async def get_category_count(
    service: ProductService = Depends(get_product_service)
):
    """Get product count by category"""
    return await service.get_category_count()

@router.get("/reports/expiring", response_model=List[Product])
async def get_expiring_products(
    days_threshold: int = Query(30, ge=1),
    service: ProductService = Depends(get_product_service)
):
    """Get products expiring soon"""
    return await service.get_expiring_products(days_threshold)

@router.get("/reports/expired", response_model=List[Product])
async def get_expired_products(
    service: ProductService = Depends(get_product_service)
):
    """Get expired products"""
    return await service.get_expired_products()

# ============ STATISTICS ============

@router.get("/stats/dashboard")
async def get_dashboard_stats(
    service: ProductService = Depends(get_product_service)
):
    """Get dashboard statistics"""
    total_products = await service.collection.count_documents({})
    low_stock = await service.collection.count_documents({
        "inventory.quantity": {"$gt": 0, "$lte": 10}
    })
    out_of_stock = await service.collection.count_documents({
        "inventory.quantity": {"$eq": 0}
    })
    inventory_value = await service.get_inventory_value()
    print("Inventory Value:", inventory_value)
    categories = await service.get_category_count()
    
    return {
        "total_products": total_products,
        "low_stock_products": low_stock,
        "out_of_stock_products": out_of_stock,
        "inventory_value": inventory_value,
        "categories": categories
    }