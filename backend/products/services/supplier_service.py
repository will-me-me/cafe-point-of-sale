# app/services/supplier_service.py
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from database import db
from products.schemas.supplier import Supplier, SupplierCreate, SupplierUpdate

class SupplierService:
    def __init__(self):
        self.collection = db["suppliers"]
        self.product_collection = db["products"]
        self.purchase_collection = db["purchases"]

    async def create_supplier(self, supplier_data: SupplierCreate, user_id: str) -> Supplier:
        """Create a new supplier"""
        supplier_dict = supplier_data.dict()
        supplier_dict["created_at"] = datetime.utcnow()
        supplier_dict["updated_at"] = datetime.utcnow()
        supplier_dict["created_by"] = user_id
        
        result = await self.collection.insert_one(supplier_dict)
        supplier_dict["id"] = str(result.inserted_id)
        
        return Supplier(**self._serialize_object_id(supplier_dict))

    async def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        """Get a single supplier by ID"""
        try:
            supplier = await self.collection.find_one({"_id": ObjectId(supplier_id)})
            if supplier:
                # Get statistics
                supplier = await self._add_supplier_stats(supplier)
                return Supplier(**self._serialize_object_id(supplier))
            return None
        except:
            return None

    async def get_supplier_by_name(self, name: str) -> Optional[Supplier]:
        """Get a supplier by name"""
        supplier = await self.collection.find_one({"name": name})
        if supplier:
            return Supplier(**self._serialize_object_id(supplier))
        return None

    async def get_suppliers(
        self, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Supplier]:
        """Get all suppliers with filtering"""
        query = {}
        
        if is_active is not None:
            query["is_active"] = is_active
        
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"contact.email": {"$regex": search, "$options": "i"}},
                {"contact.phone": {"$regex": search, "$options": "i"}},
                {"tax_id": {"$regex": search, "$options": "i"}}
            ]
        
        cursor = self.collection.find(query).sort("name", 1).skip(skip).limit(limit)
        suppliers = await cursor.to_list(length=limit)
        
        # Add statistics to each supplier
        for supplier in suppliers:
            supplier = await self._add_supplier_stats(supplier)
        print(f"all suppliers: {suppliers}")
        
        return [Supplier(**self._serialize_object_id(supplier)) for supplier in suppliers]

    async def update_supplier(
        self, 
        supplier_id: str, 
        supplier_data: SupplierUpdate, 
        user_id: str
    ) -> Optional[Supplier]:
        """Update a supplier"""
        update_data = supplier_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        update_data["updated_by"] = user_id
        
        result = await self.collection.update_one(
            {"_id": ObjectId(supplier_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_supplier(supplier_id)
        return None

    async def delete_supplier(self, supplier_id: str) -> bool:
        """Soft delete a supplier"""
        # Check if supplier has products
        product_count = await self.product_collection.count_documents({
            "suppliers.supplier_id": supplier_id
        })
        if product_count > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete supplier with {product_count} associated products"
            )
        
        result = await self.collection.update_one(
            {"_id": ObjectId(supplier_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def get_supplier_products(self, supplier_id: str, skip: int, limit: int):
        """Get all products from a supplier"""
        query = {
            "suppliers.supplier_id": supplier_id,
            "is_active": True
        }
        cursor = self.product_collection.find(query).skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        
        return [self._serialize_object_id(product) for product in products]

    async def get_supplier_purchases(self, supplier_id: str, skip: int, limit: int):
        """Get all purchase orders from a supplier"""
        query = {"supplier_id": supplier_id}
        cursor = self.purchase_collection.find(query).sort("order_date", -1).skip(skip).limit(limit)
        purchases = await cursor.to_list(length=limit)
        
        return [self._serialize_object_id(purchase) for purchase in purchases]

    async def rate_supplier(self, supplier_id: str, rating: float) -> bool:
        """Rate a supplier"""
        # Get current rating and count
        supplier = await self.get_supplier(supplier_id)
        print(f"Rating supplier {supplier} with rating {rating}")
        if not supplier:
            return False
        print(f"Current supplier rating: {supplier.rating}, count: {supplier.rating}")
        
        # Calculate new average
        current_rating = supplier.rating or 0
        rating_count = supplier.rating or 0
        new_rating = (current_rating * rating_count + rating) / (rating_count + 1)
        
        result = await self.collection.update_one(
            {"_id": ObjectId(supplier_id)},
            {
                "$set": {
                    "rating": new_rating,
                    "rating_count": rating_count + 1,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0

    async def _add_supplier_stats(self, supplier: dict) -> dict:
        """Add statistics to supplier data"""
        supplier_id = str(supplier["_id"])
        
        # Get product count
        product_count = await self.product_collection.count_documents({
            "suppliers.supplier_id": supplier_id
        })
        supplier["product_count"] = product_count
        
        # Get purchase statistics
        purchases = await self.purchase_collection.find({
            "supplier_id": supplier_id
        }).to_list(length=1000)
        
        supplier["total_purchases"] = len(purchases)
        supplier["total_spent"] = sum(p.get("total_amount", 0) for p in purchases)
        
        return supplier

    def _serialize_object_id(self, obj):
        if isinstance(obj, dict):
            serialized = {}

            for key, value in obj.items():

                if key == "_id":
                    serialized["id"] = str(value)
                    continue

                if isinstance(value, ObjectId):
                    serialized[key] = str(value)

                elif isinstance(value, datetime):
                    serialized[key] = value.isoformat()

                elif isinstance(value, list):
                    serialized[key] = [
                        self._serialize_object_id(item) if isinstance(item, dict) else item
                        for item in value
                    ]

                elif isinstance(value, dict):
                    serialized[key] = self._serialize_object_id(value)

                else:
                    serialized[key] = value

            return serialized

        return obj