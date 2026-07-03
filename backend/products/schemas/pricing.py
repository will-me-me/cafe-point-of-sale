# app/schemas/pricing.py
from typing import Optional, Dict, List
from pydantic import Field, validator, BaseModel
from decimal import Decimal
from datetime import datetime
from .enums import BaseSchema

class PriceTier(BaseModel):
    """Multiple price tiers for different customer types"""
    retail: Decimal = Field(..., ge=0)
    wholesale: Optional[Decimal] = Field(None, ge=0)
    dealer: Optional[Decimal] = Field(None, ge=0)
    vip: Optional[Decimal] = Field(None, ge=0)
    member: Optional[Decimal] = Field(None, ge=0)

    @validator('wholesale', 'dealer', 'vip', 'member')
    def validate_tier_prices(cls, v, values):
        if v is not None and 'retail' in values:
            if v > values['retail']:
                raise ValueError(f"Tier price cannot exceed retail price")
        return v

class CostHistory(BaseModel):
    purchase_date: datetime
    supplier_id: str
    quantity: int = Field(..., ge=1)
    unit_cost: Decimal = Field(..., ge=0)
    total_cost: Decimal = Field(..., ge=0)
    batch_number: Optional[str] = None
    purchase_order_id: Optional[str] = None
    notes: Optional[str] = None

class PricingBase(BaseModel):
    cost_price: Decimal = Field(..., ge=0)
    selling_price: Decimal = Field(..., ge=0)
    price_tiers: Optional[PriceTier] = None
    tax_id: Optional[str] = None
    is_taxable: bool = True
    margin: Optional[float] = Field(None, ge=0, le=100)
    markup: Optional[float] = Field(None, ge=0)

    @validator('selling_price')
    def validate_selling_price(cls, v, values):
        if 'cost_price' in values and v < values['cost_price']:
            raise ValueError("Selling price cannot be less than cost price")
        return v

class PricingCreate(PricingBase):
    pass

class PricingUpdate(BaseModel):
    cost_price: Optional[Decimal] = Field(None, ge=0)
    selling_price: Optional[Decimal] = Field(None, ge=0)
    price_tiers: Optional[PriceTier] = None
    tax_id: Optional[str] = None
    is_taxable: Optional[bool] = None
    margin: Optional[float] = Field(None, ge=0, le=100)
    markup: Optional[float] = Field(None, ge=0)

class Pricing(PricingBase, BaseSchema):
    current_cost: Optional[Decimal] = Field(None, ge=0)  # Made optional
    average_cost: Optional[Decimal] = Field(None, ge=0)  # Made optional
    cost_history: Optional[List[CostHistory]] = []