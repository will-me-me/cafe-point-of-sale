# app/services/brand_service.py
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from database import db
from products.schemas.brand import Brand, BrandCreate, BrandUpdate

class BrandService:
    def __init__(self):
        self.collection = db["brands"]
        self.product_collection = db["products"]

    async def create_brand(self, brand_data: BrandCreate, user_id: str) -> Brand:
        """Create a new brand"""
        brand_dict = brand_data.dict()
        brand_dict["created_at"] = datetime.utcnow()
        brand_dict["updated_at"] = datetime.utcnow()
        brand_dict["created_by"] = user_id
        
        result = await self.collection.insert_one(brand_dict)
        brand_dict["id"] = str(result.inserted_id)
        
        return Brand(**self._serialize_object_id(brand_dict))

    async def get_brand(self, brand_id: str) -> Optional[Brand]:
        """Get a single brand by ID"""
        try:
            brand = await self.collection.find_one({"_id": ObjectId(brand_id)})
            if brand:
                return Brand(**self._serialize_object_id(brand))
            return None
        except:
            return None

    async def get_brand_by_name(self, name: str) -> Optional[Brand]:
        """Get a brand by name"""
        brand = await self.collection.find_one({"name": name})
        if brand:
            return Brand(**self._serialize_object_id(brand))
        return None

    async def get_brands(
        self, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Brand]:
        """Get all brands with filtering"""
        query = {}
        if is_active is not None:
            query["is_active"] = is_active
        
        cursor = self.collection.find(query).sort("name", 1).skip(skip).limit(limit)
        brands = await cursor.to_list(length=limit)
        
        # Get product count for each brand
        for brand in brands:
            product_count = await self.product_collection.count_documents({
                "brand_id": str(brand["_id"])
            })
            brand["product_count"] = product_count
        
        return [Brand(**self._serialize_object_id(brand)) for brand in brands]

    async def update_brand(
        self, 
        brand_id: str, 
        brand_data: BrandUpdate, 
        user_id: str
    ) -> Optional[Brand]:
        """Update a brand"""
        update_data = brand_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        update_data["updated_by"] = user_id
        
        result = await self.collection.update_one(
            {"_id": ObjectId(brand_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_brand(brand_id)
        return None

    async def delete_brand(self, brand_id: str) -> bool:
        """Soft delete a brand"""
        # Check if brand has products
        product_count = await self.product_collection.count_documents({
            "brand_id": brand_id
        })
        if product_count > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete brand with {product_count} products"
            )
        
        result = await self.collection.update_one(
            {"_id": ObjectId(brand_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def get_brand_products(self, brand_id: str, skip: int, limit: int):
        """Get all products for a brand"""
        query = {"brand_id": brand_id, "is_active": True}
        cursor = self.product_collection.find(query).skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        
        return [self._serialize_object_id(product) for product in products]

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