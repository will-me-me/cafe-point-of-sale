# app/schemas/category.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .enums import BaseSchema

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    parent_id: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class Category(CategoryBase, BaseSchema):
    path: Optional[str] = None  # Full path like "Food/Dairy/Milk"
    level: int = 0
    children: Optional[List['Category']] = None
    product_count: Optional[int] = 0

Category.model_rebuild()

class CategoryTree(BaseModel):
    category: Category
    children: List['CategoryTree'] = []

CategoryTree.model_rebuild()