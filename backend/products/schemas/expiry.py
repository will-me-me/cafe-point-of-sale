# app/schemas/expiry.py
from typing import Optional
from pydantic import Field, model_validator
from datetime import datetime, date
from .enums import BaseModel, BaseSchema

class ExpiryBase(BaseModel):
    days_valid: Optional[int] = Field(None, ge=0)
    months_valid: Optional[int] = Field(None, ge=0)
    years_valid: Optional[int] = Field(None, ge=0)
    require_expiry: bool = False
    alert_days_before: int = Field(default=30, ge=0)
    alert_days_after: int = Field(default=7, ge=0)
    allow_sale_after_expiry: bool = False
    notes: Optional[str] = Field(None, max_length=500)

    @model_validator(mode='after')
    def validate_validity(self):
        """Validate that at least one validity period is set"""
        if self.days_valid is None and self.months_valid is None and self.years_valid is None:
            raise ValueError("At least one validity period must be set (days_valid, months_valid, or years_valid)")
        return self

class ExpiryCreate(ExpiryBase):
    pass

class ExpiryUpdate(BaseModel):
    days_valid: Optional[int] = Field(None, ge=0)
    months_valid: Optional[int] = Field(None, ge=0)
    years_valid: Optional[int] = Field(None, ge=0)
    require_expiry: Optional[bool] = None
    alert_days_before: Optional[int] = Field(None, ge=0)
    alert_days_after: Optional[int] = Field(None, ge=0)
    allow_sale_after_expiry: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=500)

class Expiry(ExpiryBase, BaseSchema):
    pass

class ExpiryTracking(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    batch_number: str
    expiry_date: date
    quantity: int = Field(..., ge=0)
    remaining: int = Field(..., ge=0)
    status: str = "active"  # active, expiring, expired
    days_remaining: Optional[int] = None

    @model_validator(mode='after')
    def calculate_days_remaining(self):
        """Calculate days remaining and determine status"""
        if self.expiry_date:
            days = (self.expiry_date - date.today()).days
            self.days_remaining = max(0, days)
            
            if days < 0:
                self.status = "expired"
            elif days < 30:  # 30 days threshold
                self.status = "expiring"
            else:
                self.status = "active"
        return self