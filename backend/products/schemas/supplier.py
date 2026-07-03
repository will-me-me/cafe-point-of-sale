# app/schemas/supplier.py
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from .enums import BaseSchema, Contact

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    contact: Contact
    tax_id: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=1000)
    is_active: bool = True
    rating: Optional[float] = Field(None, ge=0, le=5)

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    contact: Optional[Contact] = None
    tax_id: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None
    rating: Optional[float] = Field(None, ge=0, le=5)

class Supplier(SupplierBase, BaseSchema):
    product_count: Optional[int] = 0
    total_purchases: Optional[int] = 0
    total_spent: Optional[float] = 0

class SupplierProduct(BaseModel):
    supplier_id: str
    supplier_sku: Optional[str] = None
    supplier_product_name: Optional[str] = None
    lead_time_days: int = Field(default=7, ge=0)
    preferred: bool = False
    last_cost: Optional[float] = Field(None, ge=0)
    last_purchase_date: Optional[datetime] = None
    is_active: bool = True