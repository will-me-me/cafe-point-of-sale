# app/schemas/branch.py
from typing import Optional, List
from fastapi.datastructures import Address
from pydantic import Field
from datetime import datetime
from .enums import BaseModel, BaseSchema

class BranchBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20)
    address: Address
    phone: str
    email: Optional[str] = None
    manager_id: Optional[str] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = Field(None, max_length=500)

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    address: Optional[Address] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    manager_id: Optional[str] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=500)

class Branch(BranchBase, BaseSchema):
    pass

class BranchInventory(BaseModel):
    branch_id: str
    product_id: str
    variant_id: Optional[str] = None
    quantity: int = Field(..., ge=0)
    reserved: int = Field(default=0, ge=0)
    available: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=0, ge=0)
    reorder_quantity: int = Field(default=0, ge=0)
    location: Optional[str] = None
    shelf_number: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)