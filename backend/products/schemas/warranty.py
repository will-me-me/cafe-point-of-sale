# app/schemas/warranty.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .enums import BaseSchema, WarrantyProvider

class WarrantyBase(BaseModel):
    months: int = Field(..., ge=0)
    provider: WarrantyProvider
    provider_name: Optional[str] = Field(None, max_length=100)
    terms: Optional[str] = Field(None, max_length=1000)
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    is_transferable: bool = False
    registration_required: bool = False
    registration_url: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    is_active: bool = True

class WarrantyCreate(WarrantyBase):
    pass

class WarrantyUpdate(BaseModel):
    months: Optional[int] = Field(None, ge=0)
    provider: Optional[WarrantyProvider] = None
    provider_name: Optional[str] = Field(None, max_length=100)
    terms: Optional[str] = Field(None, max_length=1000)
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    is_transferable: Optional[bool] = None
    registration_required: Optional[bool] = None
    registration_url: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class Warranty(WarrantyBase, BaseSchema):
    pass

class WarrantyClaim(BaseModel):
    warranty_id: str
    product_id: str
    variant_id: Optional[str] = None
    serial_number: Optional[str] = None
    claim_date: datetime = Field(default_factory=datetime.utcnow)
    description: str = Field(..., max_length=500)
    status: str = "pending"  # pending, approved, rejected, completed
    resolution: Optional[str] = Field(None, max_length=500)
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)