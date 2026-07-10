# app/products/service.py
import mimetypes
import uuid
import datetime as dt  # Import as dt to avoid confusion
from typing import List, Optional, Dict, Any
from supabase import create_client, Client
from fastapi import UploadFile, HTTPException
import os
from dotenv import load_dotenv
from bson import ObjectId
from decimal import Decimal
import json

from database import db
from products.schemas.product import (
    Product, ProductCreate, ProductUpdate, ProductVariant,
    ProductVariantCreate, ProductVariantUpdate, ProductSearch
)
from products.schemas.category import Category
from products.schemas.inventory import Inventory, InventoryUpdate, StockStatus
from products.schemas.pricing import Pricing, PriceTier
from products.schemas.movement import InventoryMovement, InventoryMovementCreate, MovementType
from products.schemas.supplier import SupplierProduct
from products.schemas.branch import BranchInventory
from products.schemas.reports import ReportRequest, SalesReport, InventoryReport
from products.services.pricing_service import PricingService

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "product-images")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============ HELPER FUNCTIONS ============

def convert_decimal_to_float(obj):
    """Recursively convert Decimal objects to float for MongoDB serialization"""
    if isinstance(obj, dict):
        return {key: convert_decimal_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal_to_float(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dt.datetime):
        return obj.isoformat()
    return obj

def serialize_object_id(obj):
    """Convert ObjectId to string and handle datetime serialization"""
    if obj is None:
        return None
    
    if isinstance(obj, dict):
        serialized = {}
        for key, value in obj.items():
            # Convert _id to id
            if key == "_id":
                serialized["id"] = str(value)
                continue
            
            # Handle ObjectId
            if isinstance(value, ObjectId):
                serialized[key] = str(value)
            # Handle datetime
            elif isinstance(value, dt.datetime):
                serialized[key] = value.isoformat()
            # Handle list
            elif isinstance(value, list):
                serialized[key] = [
                    serialize_object_id(item) if isinstance(item, (dict, list)) else item
                    for item in value
                ]
            # Handle dict
            elif isinstance(value, dict):
                serialized[key] = serialize_object_id(value)
            # Handle Decimal
            elif isinstance(value, Decimal):
                serialized[key] = float(value)
            else:
                serialized[key] = value
        
        return serialized
    elif isinstance(obj, list):
        return [serialize_object_id(item) if isinstance(item, (dict, list)) else item for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dt.datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def parse_object_id(obj):
    """Convert string IDs to ObjectId for MongoDB queries"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key.endswith("_id") and isinstance(value, str) and len(value) == 24:
                obj[key] = ObjectId(value)
            elif isinstance(value, list):
                obj[key] = [parse_object_id(item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, dict):
                obj[key] = parse_object_id(value)
    return obj

# ============ PRODUCT SERVICE ============

class ProductService:
    """Service for product management"""
    
    def __init__(self):
        self.collection = db["products"]
        self.inventory_collection = db["inventory"]
        self.movement_collection = db["inventory_movements"]
        self.branch_inventory_collection = db["branch_inventory"]
        
    # ============ FILE UPLOAD ============
    
    @staticmethod
    async def upload_to_supabase(file: UploadFile, folder: str = "products") -> str:
        """Upload file to Supabase storage"""
        try:
            file_bytes = await file.read()
            extension = file.filename.split(".")[-1]
            unique_id = uuid.uuid4().hex
            timestamp = dt.datetime.utcnow().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{timestamp}_{unique_id}.{extension}"
            file_path = f"{folder}/{unique_filename}"

            content_type, _ = mimetypes.guess_type(file.filename)
            if not content_type:
                content_type = "application/octet-stream"

            result = supabase.storage.from_(SUPABASE_BUCKET).upload(
                file_path,
                file_bytes,
                {"content-type": content_type},
            )

            public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_path)
            return public_url
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    @staticmethod
    async def delete_from_supabase(file_url: str) -> bool:
        """Delete file from Supabase storage"""
        try:
            file_path = file_url.split("/")[-1]
            supabase.storage.from_(SUPABASE_BUCKET).remove([f"products/{file_path}"])
            return True
        except Exception:
            return False
    
    # ============ PRODUCT CRUD ============
    
    async def create_product(self, product_data: ProductCreate, user_id: str) -> Product:
        """Create a new product with dynamic variant pricing"""
        # Convert to dict for MongoDB
        product_dict = product_data.dict(exclude_unset=True)
        product_dict["created_at"] = dt.datetime.utcnow()
        product_dict["updated_at"] = dt.datetime.utcnow()
        product_dict["created_by"] = user_id
        
        # Initialize inventory
        if not product_dict.get("inventory"):
            product_dict["inventory"] = {
                "quantity": 0,
                "reserved": 0,
                "available": 0,
                "reorder_level": 0,
                "location": "",
                "created_at": dt.datetime.utcnow(),
                "updated_at": dt.datetime.utcnow()
            }
        else:
            # Set product_id in inventory
            product_dict["inventory"]["product_id"] = None  # Will be set after insert
        
        # Handle variants based on product type
        if product_dict.get("variants"):
            # Check if this is a bulk product (has unit_conversion)
            has_unit_conversion = product_dict.get("unit_conversion") is not None
            
            for idx, variant in enumerate(product_dict["variants"]):
                if "attributes" not in variant:
                    variant["attributes"] = {}
                
                # For bulk products, ensure weight_kg is present
                if has_unit_conversion:
                    # Convert weight from string to kg if needed
                    if "weight" in variant["attributes"] and "weight_kg" not in variant["attributes"]:
                        weight_str = variant["attributes"]["weight"]
                        variant["attributes"]["weight_kg"] = self._convert_weight_to_kg(weight_str)
                    elif "weight_kg" not in variant["attributes"]:
                        # For bulk products, weight_kg is required
                        raise ValueError(f"Variant '{variant.get('variant_name', '')}' must have 'weight_kg' in attributes")
                
                # Generate variant_id if not present
                if "id" not in variant:
                    variant["id"] = str(ObjectId())
                
                # Initialize variant inventory
                if "inventory" not in variant:
                    variant["inventory"] = {
                        "quantity": 0,
                        "reserved": 0,
                        "available": 0,
                        "reorder_level": 0,
                        "product_id": None,  # Will be set after insert
                        "variant_id": variant["id"],
                        "created_at": dt.datetime.utcnow(),
                        "updated_at": dt.datetime.utcnow()
                    }
                else:
                    variant["inventory"]["variant_id"] = variant["id"]
                    variant["inventory"]["product_id"] = None  # Will be set after insert
        
        # Convert Decimal to float for MongoDB
        product_dict = convert_decimal_to_float(product_dict)
        
        # Insert into database
        try:
            result = await self.collection.insert_one(product_dict)
            product_dict["id"] = str(result.inserted_id)
            
            # Update inventory with product_id after insert
            product_id = str(result.inserted_id)
            
            # Update main inventory
            await self.collection.update_one(
                {"_id": ObjectId(product_id)},
                {
                    "$set": {
                        "inventory.product_id": product_id,
                        "inventory.variant_id": None
                    }
                }
            )
            
            # Update variant inventories
            if product_dict.get("variants"):
                for variant in product_dict["variants"]:
                    if "id" in variant:
                        await self.collection.update_one(
                            {"_id": ObjectId(product_id), "variants.id": variant["id"]},
                            {
                                "$set": {
                                    "variants.$.inventory.product_id": product_id,
                                    "variants.$.inventory.variant_id": variant["id"]
                                }
                            }
                        )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")
        
        # Get the created product with computed pricing
        return await self.get_product(product_dict["id"])
    
    async def get_product(self, product_id: str) -> Optional[Product]:
        """Get a single product by ID with computed variant pricing"""
        try:
            product = await self.collection.find_one({"_id": ObjectId(product_id)})
            if product:
                serialized = serialize_object_id(product)
                # Convert to Product model
                product_obj = Product(**serialized)
                # Enrich variants with computed pricing
                if product_obj.has_variants and product_obj.variants:
                    enriched_variants = []
                    for variant in product_obj.variants:
                        enriched = PricingService.enrich_variant_with_pricing(
                            product_obj, variant
                        )
                        enriched_variants.append(enriched)
                    # Update variants with computed pricing
                    product_obj.variants = enriched_variants
                return product_obj
            return None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    async def get_product_by_sku(self, sku: str) -> Optional[Product]:
        """Get a product by SKU"""
        try:
            product = await self.collection.find_one({"sku": sku})
            if product:
                serialized_product = serialize_object_id(product)
                return Product(**serialized_product)
            return None
        except Exception as e:
            print(f"Error getting product by SKU: {e}")
            return None
    
    async def get_product_by_barcode(self, barcode: str) -> Optional[Product]:
        """Get a product by barcode"""
        try:
            product = await self.collection.find_one({"barcode": barcode})
            if product:
                serialized_product = serialize_object_id(product)
                return Product(**serialized_product)
            
            # Search in variants
            product = await self.collection.find_one({"variants.barcode": barcode})
            if product:
                serialized_product = serialize_object_id(product)
                return Product(**serialized_product)
            return None
        except Exception as e:
            print(f"Error getting product by barcode: {e}")
            return None
    
    async def get_products(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[ProductSearch] = None
    ) -> List[Product]:
        """Get all products with filtering"""
        query = {}
        
        if search:
            # Text search
            if search.query:
                query["$or"] = [
                    {"name": {"$regex": search.query, "$options": "i"}},
                    {"sku": {"$regex": search.query, "$options": "i"}},
                    {"description": {"$regex": search.query, "$options": "i"}},
                    {"barcode": {"$regex": search.query, "$options": "i"}}
                ]
            
            # Category filter
            if search.category_id:
                query["category_id"] = search.category_id
            
            # Brand filter
            if search.brand_id:
                query["brand_id"] = search.brand_id
            
            # Supplier filter
            if search.supplier_id:
                query["suppliers.supplier_id"] = search.supplier_id
            
            # Product type
            if search.product_type:
                query["product_type"] = search.product_type
            
            # Price range
            if search.min_price is not None or search.max_price is not None:
                price_query = {}
                if search.min_price is not None:
                    price_query["$gte"] = search.min_price
                if search.max_price is not None:
                    price_query["$lte"] = search.max_price
                query["pricing.selling_price"] = price_query
            
            # Stock filter
            if search.in_stock is not None:
                if search.in_stock:
                    query["inventory.available"] = {"$gt": 0}
                else:
                    query["inventory.available"] = {"$eq": 0}
            
            # Active filter
            if search.is_active is not None:
                query["is_active"] = search.is_active
            
            # Featured filter
            if search.is_featured is not None:
                query["is_featured"] = search.is_featured
            
            # On sale filter
            if search.is_on_sale is not None:
                query["is_on_sale"] = search.is_on_sale
            
            # Tags filter
            if search.tags:
                query["tags"] = {"$in": search.tags}
            
            # Attributes filter
            if search.attributes:
                for key, value in search.attributes.items():
                    query[f"attributes.{key}"] = value
        
        cursor = self.collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)

        result = []
        for product in products:
            serialized = serialize_object_id(product)
            product_obj = Product(**serialized)
            
            # Enrich variants with computed pricing
            if product_obj.has_variants and product_obj.variants:
                enriched_variants = []
                for variant in product_obj.variants:
                    enriched = PricingService.enrich_variant_with_pricing(
                        product_obj, variant
                    )
                    enriched_variants.append(enriched)
                product_obj.variants = enriched_variants
            
            result.append(product_obj)
        
        return result
        
        # return [Product(**serialize_object_id(product)) for product in products]
    def _convert_weight_to_kg(self, weight_str: str) -> float:
            """Convert weight string to kg"""
            if isinstance(weight_str, (int, float)):
                return float(weight_str)
            
            weight_str = weight_str.lower().strip()
            if 'kg' in weight_str:
                return float(weight_str.replace('kg', '').strip())
            elif 'g' in weight_str:
                return float(weight_str.replace('g', '').strip()) / 1000
            elif 'ml' in weight_str:
                return float(weight_str.replace('ml', '').strip()) / 1000
            elif 'l' in weight_str:
                return float(weight_str.replace('l', '').strip()) * 1000 / 1000
            else:
                return float(weight_str)
        
    async def update_product(self, product_id: str, product_data: ProductUpdate, user_id: str) -> Optional[Product]:
        """Update a product"""
        update_data = product_data.dict(exclude_unset=True)
        update_data["updated_at"] = dt.datetime.utcnow()
        update_data["updated_by"] = user_id
        
        # Handle nested updates
        if "inventory" in update_data:
            update_data["inventory.updated_at"] = dt.datetime.utcnow()
            # Calculate status if quantity changed
            if "quantity" in update_data["inventory"]:
                update_data["inventory.status"] = self._determine_stock_status(
                    update_data["inventory"]["quantity"]
                )
        
        if "pricing" in update_data:
            update_data["pricing.updated_at"] = dt.datetime.utcnow()
            # Calculate margin if prices changed
            cost = update_data["pricing"].get("cost_price")
            selling = update_data["pricing"].get("selling_price")
            if cost is not None and selling is not None:
                if cost > 0 and selling > 0:
                    update_data["pricing.margin"] = ((selling - cost) / selling) * 100
                else:
                    update_data["pricing.margin"] = 0
        
        # Convert Decimal to float
        update_data = convert_decimal_to_float(update_data)
        
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_product(product_id)
        return None
    
    async def delete_product(self, product_id: str) -> bool:
        """Soft delete a product (mark as inactive)"""
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"is_active": False, "updated_at": dt.datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    async def permanently_delete_product(self, product_id: str) -> bool:
        """Permanently delete a product"""
        product = await self.get_product(product_id)
        print(f"Permanently deleting product with ID: {product}")
        if product and product.media and product.media.images:
            for image in product.media.images:
                await self.delete_from_supabase(image.url)
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
    
    # ============ VARIANT MANAGEMENT ============
    
    async def add_variant(self, product_id: str, variant: ProductVariantCreate, user_id: str) -> Optional[Product]:
        """Add a variant to a product"""
        variant_dict = variant.dict()
        variant_dict["created_at"] = dt.datetime.utcnow()
        variant_dict["updated_at"] = dt.datetime.utcnow()
        variant_dict["created_by"] = user_id
        
        # Convert Decimal to float
        variant_dict = convert_decimal_to_float(variant_dict)
        
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$push": {"variants": variant_dict},
                "$set": {"has_variants": True, "updated_at": dt.datetime.utcnow()}
            }
        )
        
        if result.modified_count:
            return await self.get_product(product_id)
        return None
    
    async def update_variant(self, product_id: str, variant_id: str, variant_data: ProductVariantUpdate, user_id: str) -> Optional[Product]:
        """Update a product variant"""
        update_data = variant_data.dict(exclude_unset=True)
        update_data["updated_at"] = dt.datetime.utcnow()
        update_data["updated_by"] = user_id
        
        # Convert Decimal to float
        update_data = convert_decimal_to_float(update_data)
        
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id), "variants.id": variant_id},
            {"$set": {f"variants.$.{key}": value for key, value in update_data.items()}}
        )
        
        if result.modified_count:
            return await self.get_product(product_id)
        return None
    
    async def delete_variant(self, product_id: str, variant_id: str) -> Optional[Product]:
        """Delete a product variant"""
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$pull": {"variants": {"id": variant_id}}}
        )
        
        if result.modified_count:
            return await self.get_product(product_id)
        return None
    
    # ============ INVENTORY MANAGEMENT ============
    
    async def update_inventory(
        self, 
        product_id: str, 
        quantity_change: float,  # Changed to float for kg
        movement_type: MovementType,
        reason: str,
        user_id: str,
        reference_id: Optional[str] = None,
        variant_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        serial_numbers: Optional[List[str]] = None,
        batch_number: Optional[str] = None
    ) -> InventoryMovement:
        """Update inventory quantity in kg and create movement record"""
        
        # Get current product
        product = await self.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # If variant is specified, get its weight
        if variant_id:
            variant = next((v for v in product.variants if v.get('id') == variant_id), None)
            if variant:
                weight_kg = variant.get('attributes', {}).get('weight_kg', 0)
                # Convert quantity from number of units to kg
                quantity_kg = quantity_change * weight_kg
            else:
                quantity_kg = quantity_change
        else:
            quantity_kg = quantity_change
        
        # Get current quantity in kg
        current_quantity = product.inventory.quantity if product.inventory else 0
        new_quantity = max(0, current_quantity + quantity_kg)
        
        # Prepare update
        update_data = {
            "updated_at": dt.datetime.utcnow(),
            "updated_by": user_id,
            "inventory.quantity": new_quantity,
            "inventory.available": new_quantity - 0,
            "inventory.status": self._determine_stock_status(new_quantity),
            "inventory.updated_at": dt.datetime.utcnow()
        }
        
        # Update product inventory
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        
        if not result.modified_count:
            raise HTTPException(status_code=500, detail="Failed to update inventory")
        
        # Create inventory movement record
        movement = await self.create_movement(
            product_id=product_id,
            variant_id=variant_id,
            quantity=abs(quantity_kg),
            movement_type=movement_type,
            reason=reason,
            user_id=user_id,
            reference_id=reference_id,
            branch_id=branch_id,
            serial_numbers=serial_numbers,
            batch_number=batch_number,
            unit_cost=product.pricing.cost_price / product.unit_conversion.conversion_factor if product.pricing and product.unit_conversion else None
        )
        
        return movement
    
    def _determine_stock_status(self, quantity: int) -> str:
        """Determine stock status based on quantity"""
        if quantity <= 0:
            return StockStatus.OUT_OF_STOCK
        elif quantity < 10:
            return StockStatus.LOW_STOCK
        return StockStatus.IN_STOCK
    
    # ============ INVENTORY MOVEMENTS ============
    
    async def create_movement(
        self,
        product_id: str,
        variant_id: Optional[str],
        quantity: int,
        movement_type: MovementType,
        reason: str,
        user_id: str,
        reference_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        serial_numbers: Optional[List[str]] = None,
        batch_number: Optional[str] = None,
        unit_cost: Optional[Decimal] = None
    ) -> InventoryMovement:
        """Create an inventory movement record"""
        
        movement = InventoryMovementCreate(
            product_id=str(product_id),
            variant_id=variant_id,
            quantity=quantity,
            movement_type=movement_type,
            reason=reason,
            reference_id=reference_id,
            created_by=user_id,
            batch_number=batch_number,
            serial_numbers=serial_numbers or [],
            unit_cost=unit_cost,
            total_cost=unit_cost * quantity if unit_cost else 0,
            notes=f"Inventory {movement_type.value} - {reason}"
        )
        
        movement_dict = movement.dict()
        movement_dict["created_at"] = dt.datetime.utcnow()
        movement_dict["movement_date"] = dt.datetime.utcnow()
        
        if branch_id:
            movement_dict["to_location"] = branch_id
        
        # Convert Decimal to float
        movement_dict = convert_decimal_to_float(movement_dict)
        
        result = await self.movement_collection.insert_one(movement_dict)
        movement_dict["id"] = str(result.inserted_id)
        
        return InventoryMovement(**serialize_object_id(movement_dict))
    
    async def get_movements(
        self, 
        product_id: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[InventoryMovement]:
        """Get inventory movements with filters"""
        query = {}
        if product_id:
            query["product_id"] = product_id
        
        cursor = self.movement_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        movements = await cursor.to_list(length=limit)
        
        return [InventoryMovement(**serialize_object_id(movement)) for movement in movements]
    
    # ============ BRANCH INVENTORY ============
    
    async def update_branch_inventory(
        self,
        branch_id: str,
        product_id: str,
        quantity_change: int,
        variant_id: Optional[str] = None,
        reserved_change: int = 0
    ) -> BranchInventory:
        """Update inventory for a specific branch"""
        
        # Get current branch inventory
        branch_inv = await self.branch_inventory_collection.find_one({
            "branch_id": branch_id,
            "product_id": product_id,
            "variant_id": variant_id
        })
        
        if branch_inv:
            # Update existing
            new_quantity = max(0, branch_inv["quantity"] + quantity_change)
            new_reserved = max(0, branch_inv["reserved"] + reserved_change)
            
            update_data = {
                "quantity": new_quantity,
                "reserved": new_reserved,
                "available": new_quantity - new_reserved,
                "updated_at": dt.datetime.utcnow()
            }
            
            result = await self.branch_inventory_collection.update_one(
                {"_id": branch_inv["_id"]},
                {"$set": update_data}
            )
            
            branch_inv.update(update_data)
        else:
            # Create new
            branch_inv = {
                "branch_id": branch_id,
                "product_id": product_id,
                "variant_id": variant_id,
                "quantity": max(0, quantity_change),
                "reserved": max(0, reserved_change),
                "available": max(0, quantity_change - reserved_change),
                "reorder_level": 10,
                "created_at": dt.datetime.utcnow(),
                "updated_at": dt.datetime.utcnow()
            }
            
            result = await self.branch_inventory_collection.insert_one(branch_inv)
            branch_inv["id"] = str(result.inserted_id)
        
        return BranchInventory(**serialize_object_id(branch_inv))
    
    async def get_branch_inventory(
        self, 
        branch_id: str,
        product_id: Optional[str] = None
    ) -> List[BranchInventory]:
        """Get inventory for a branch"""
        query = {"branch_id": branch_id}
        if product_id:
            query["product_id"] = product_id
        
        cursor = self.branch_inventory_collection.find(query)
        inventory = await cursor.to_list(length=1000)
        
        return [BranchInventory(**serialize_object_id(item)) for item in inventory]
    
    # ============ BULK OPERATIONS ============
    
    async def bulk_update_prices(
        self, 
        product_ids: List[str], 
        price_change_percent: float
    ) -> int:
        """Bulk update product prices"""
        updated_count = 0
        for product_id in product_ids:
            product = await self.get_product(product_id)
            if product and product.pricing:
                new_price = float(product.pricing.selling_price) * (1 + price_change_percent / 100)
                new_price = max(0, new_price)
                
                result = await self.collection.update_one(
                    {"_id": ObjectId(product_id)},
                    {
                        "$set": {
                            "pricing.selling_price": new_price,
                            "pricing.updated_at": dt.datetime.utcnow()
                        }
                    }
                )
                if result.modified_count:
                    updated_count += 1
        
        return updated_count
    
    async def bulk_update_stock_status(self, threshold: int = 10) -> int:
        """Bulk update stock status based on quantity"""
        result1 = await self.collection.update_many(
            {"inventory.quantity": {"$lte": 0}},
            {"$set": {"inventory.status": StockStatus.OUT_OF_STOCK}}
        )
        
        result2 = await self.collection.update_many(
            {"inventory.quantity": {"$gt": 0, "$lte": threshold}},
            {"$set": {"inventory.status": StockStatus.LOW_STOCK}}
        )
        
        result3 = await self.collection.update_many(
            {"inventory.quantity": {"$gt": threshold}},
            {"$set": {"inventory.status": StockStatus.IN_STOCK}}
        )
        
        return result1.modified_count + result2.modified_count + result3.modified_count
    
    # ============ REPORTS ============
    
    async def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        query = {"inventory.quantity": {"$lte": threshold, "$gt": 0}}
        cursor = self.collection.find(query).sort("inventory.quantity", 1)
        products = await cursor.to_list(length=100)
        return [Product(**serialize_object_id(product)) for product in products]
    
    async def get_out_of_stock_products(self) -> List[Product]:
        """Get out of stock products"""
        query = {"inventory.quantity": {"$eq": 0}}
        cursor = self.collection.find(query)
        products = await cursor.to_list(length=100)
        return [Product(**serialize_object_id(product)) for product in products]
    
    async def get_inventory_value(self) -> Dict[str, Any]:
        """Calculate total inventory value"""
        pipeline = [
            {"$group": {
                "_id": None,
                "total_quantity": {"$sum": "$inventory.quantity"},
                "total_value": {"$sum": {"$multiply": ["$inventory.quantity", "$pricing.cost_price"]}},
                "total_retail_value": {"$sum": {"$multiply": ["$inventory.quantity", "$pricing.selling_price"]}}
            }}
        ]
        print("Calculating inventory value with pipeline:", pipeline)
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        print("Inventory value result:", result)
        return result[0] if result else {"total_quantity": 0, "total_value": 0, "total_retail_value": 0}
    
    async def get_category_count(self) -> Dict[str, int]:
        """Get product count by category"""
        pipeline = [
            {"$group": {
                "_id": "$category_id",
                "count": {"$sum": 1}
            }}
        ]
        
        results = await self.collection.aggregate(pipeline).to_list(length=100)
        return {str(r["_id"]): r["count"] for r in results if r["_id"]}
    
    # ============ SEARCH ============
    
    async def search_products(self, query: str, limit: int = 50) -> List[Product]:
        """Advanced product search"""
        search_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"sku": {"$regex": query, "$options": "i"}},
                {"barcode": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"tags": {"$in": [query]}},
                {"attributes": {"$regex": query, "$options": "i"}}
            ]
        }
        
        cursor = self.collection.find(search_query).limit(limit)
        products = await cursor.to_list(length=limit)
        
        return [Product(**serialize_object_id(product)) for product in products]
    
    # ============ EXPIRY MANAGEMENT ============
    
    async def get_expiring_products(self, days_threshold: int = 30) -> List[Product]:
        """Get products expiring soon"""
        expiry_date = dt.datetime.utcnow() + dt.timedelta(days=days_threshold)
        
        query = {
            "expiry.expiry_date": {"$lte": expiry_date, "$gt": dt.datetime.utcnow()}
        }
        
        cursor = self.collection.find(query)
        products = await cursor.to_list(length=100)
        
        return [Product(**serialize_object_id(product)) for product in products]
    
    async def get_expired_products(self) -> List[Product]:
        """Get expired products"""
        query = {
            "expiry.expiry_date": {"$lt": dt.datetime.utcnow()}
        }
        
        cursor = self.collection.find(query)
        products = await cursor.to_list(length=100)
        
        return [Product(**serialize_object_id(product)) for product in products]

# Singleton instance
product_service = ProductService()