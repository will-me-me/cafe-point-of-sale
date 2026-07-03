# app/services/category_service.py
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from database import db
from products.schemas.category import Category, CategoryCreate, CategoryUpdate, CategoryTree

class CategoryService:
    def __init__(self):
        self.collection = db["categories"]
        self.product_collection = db["products"]

    async def create_category(self, category_data: CategoryCreate, user_id: str) -> Category:
        """Create a new category"""
        category_dict = category_data.dict()
        category_dict["created_at"] = datetime.utcnow()
        category_dict["updated_at"] = datetime.utcnow()
        category_dict["created_by"] = user_id
        
        # Calculate path and level
        if category_data.parent_id:
            parent = await self.get_category(category_data.parent_id)
            if parent:
                category_dict["path"] = f"{parent.path}/{category_data.name}" if parent.path else category_data.name
                category_dict["level"] = parent.level + 1
            else:
                category_dict["path"] = category_data.name
                category_dict["level"] = 0
        else:
            category_dict["path"] = category_data.name
            category_dict["level"] = 0
        
        result = await self.collection.insert_one(category_dict)
        category_dict["id"] = str(result.inserted_id)
        
        return Category(**self._serialize_object_id(category_dict))

    async def get_category(self, category_id: str) -> Optional[Category]:
        """Get a single category by ID"""
        try:
            category = await self.collection.find_one({"_id": ObjectId(category_id)})
            if category:
                return Category(**self._serialize_object_id(category))
            return None
        except:
            return None

    async def get_category_by_name(self, name: str) -> Optional[Category]:
        """Get a category by name"""
        category = await self.collection.find_one({"name": name})
        if category:
            return Category(**self._serialize_object_id(category))
        return None

    async def get_categories(
        self, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None,
        parent_id: Optional[str] = None
    ) -> List[Category]:
        """Get all categories with filtering"""
        query = {}
        if is_active is not None:
            query["is_active"] = is_active
        if parent_id:
            query["parent_id"] = parent_id
        
        cursor = self.collection.find(query).sort("sort_order", 1).skip(skip).limit(limit)
        categories = await cursor.to_list(length=limit)
        
        # Get product count for each category
        for cat in categories:
            product_count = await self.product_collection.count_documents({
                "category_id": str(cat["_id"])
            })
            cat["product_count"] = product_count
        
        return [Category(**self._serialize_object_id(cat)) for cat in categories]

    async def get_category_tree(self) -> List[CategoryTree]:
        """Get category hierarchy as a tree"""
        # Get all categories
        categories = await self.collection.find({"is_active": True}).sort("sort_order", 1).to_list(length=1000)
        
        # Build tree
        category_map = {}
        root_categories = []
        
        for cat in categories:
            cat_dict = self._serialize_object_id(cat)
            category_obj = Category(**cat_dict)
            category_map[str(cat["_id"])] = CategoryTree(category=category_obj, children=[])
        
        for cat in categories:
            cat_id = str(cat["_id"])
            parent_id = cat.get("parent_id")
            
            if parent_id and parent_id in category_map:
                category_map[parent_id].children.append(category_map[cat_id])
            else:
                root_categories.append(category_map[cat_id])
        
        return root_categories

    async def update_category(
        self, 
        category_id: str, 
        category_data: CategoryUpdate, 
        user_id: str
    ) -> Optional[Category]:
        """Update a category"""
        update_data = category_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        update_data["updated_by"] = user_id
        
        # If name changed, update path
        if "name" in update_data:
            old_category = await self.get_category(category_id)
            if old_category:
                old_path = old_category.path
                new_path = old_path.replace(old_category.name, update_data["name"])
                update_data["path"] = new_path
                
                # Update all children paths
                await self._update_child_paths(category_id, old_category.name, update_data["name"])
        
        # If parent changed, recalculate path and level
        if "parent_id" in update_data:
            if update_data["parent_id"]:
                parent = await self.get_category(update_data["parent_id"])
                if parent:
                    update_data["level"] = parent.level + 1
                    update_data["path"] = f"{parent.path}/{update_data.get('name', '')}"
                else:
                    raise HTTPException(status_code=404, detail="Parent category not found")
            else:
                update_data["level"] = 0
                update_data["path"] = update_data.get("name", "")
        
        result = await self.collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_category(category_id)
        return None

    async def delete_category(self, category_id: str) -> bool:
        """Soft delete a category"""
        # Check if category has products
        product_count = await self.product_collection.count_documents({
            "category_id": category_id
        })
        if product_count > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete category with {product_count} products"
            )
        
        result = await self.collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def move_category(self, category_id: str, new_parent_id: Optional[str]) -> bool:
        """Move a category to a different parent"""
        category = await self.get_category(category_id)
        if not category:
            return False
        
        # Prevent circular reference
        if new_parent_id:
            # Check if new parent is not a child of the category being moved
            await self._check_circular_reference(category_id, new_parent_id)
        
        update_data = {
            "parent_id": new_parent_id,
            "updated_at": datetime.utcnow()
        }
        
        if new_parent_id:
            parent = await self.get_category(new_parent_id)
            if parent:
                update_data["level"] = parent.level + 1
                update_data["path"] = f"{parent.path}/{category.name}"
        else:
            update_data["level"] = 0
            update_data["path"] = category.name
        
        result = await self.collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": update_data}
        )
        
        return result.modified_count > 0

    async def get_category_products(self, category_id: str, skip: int, limit: int):
        """Get all products in a category"""
        query = {"category_id": category_id, "is_active": True}
        cursor = self.product_collection.find(query).skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        
        return [self._serialize_object_id(product) for product in products]

    async def _update_child_paths(self, category_id: str, old_name: str, new_name: str):
        """Update paths for all children of a category"""
        children = await self.collection.find({"parent_id": category_id}).to_list(length=1000)
        for child in children:
            new_path = child["path"].replace(old_name, new_name, 1)
            await self.collection.update_one(
                {"_id": child["_id"]},
                {"$set": {"path": new_path}}
            )
            # Recursively update grandchildren
            await self._update_child_paths(str(child["_id"]), old_name, new_name)

    async def _check_circular_reference(self, category_id: str, new_parent_id: str):
        """Check if moving category would create a circular reference"""
        # Get all children of the category
        children = await self.collection.find({"parent_id": category_id}).to_list(length=1000)
        child_ids = [str(child["_id"]) for child in children]
        
        # Check if new parent is in children
        if new_parent_id in child_ids:
            raise HTTPException(
                status_code=400, 
                detail="Cannot move category to its own child"
            )
        
        # Recursively check deeper levels
        for child_id in child_ids:
            await self._check_circular_reference(child_id, new_parent_id)

    def _serialize_object_id(self, obj):
        """Convert ObjectId to string for JSON serialization"""
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