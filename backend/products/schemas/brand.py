# app/schemas/brand.py
from typing import Optional
from pydantic import Field
from .enums import BaseModel, BaseSchema

class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    logo_url: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    is_active: bool = True

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    logo_url: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class Brand(BrandBase, BaseSchema):
    product_count: Optional[int] = 0