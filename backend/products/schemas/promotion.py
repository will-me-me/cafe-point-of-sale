# app/schemas/promotion.py
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal
from products.schemas.enums import BaseSchema, DiscountType


class PromotionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    code: Optional[str] = Field(None, max_length=50)
    discount_type: DiscountType
    discount_value: Decimal = Field(..., ge=0)
    minimum_order_amount: Optional[Decimal] = Field(None, ge=0)
    minimum_quantity: int = Field(default=1, ge=1)
    maximum_discount_amount: Optional[Decimal] = Field(None, ge=0)
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    applies_to_all_products: bool = False
    product_ids: Optional[List[str]] = []
    category_ids: Optional[List[str]] = []
    brand_ids: Optional[List[str]] = []
    customer_groups: Optional[List[str]] = []
    usage_limit: Optional[int] = Field(None, ge=0)
    usage_count: int = Field(default=0, ge=0)
    stackable: bool = False
    priority: int = Field(default=0, ge=0)

    @field_validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError("End date must be after start date")
        return v

    @field_validator('discount_value')
    def validate_discount_value(cls, v, values):
        if values.get('discount_type') == DiscountType.PERCENTAGE and v > 100:
            raise ValueError("Percentage discount cannot exceed 100%")
        return v

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    code: Optional[str] = Field(None, max_length=50)
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[Decimal] = Field(None, ge=0)
    minimum_order_amount: Optional[Decimal] = Field(None, ge=0)
    minimum_quantity: Optional[int] = Field(None, ge=1)
    maximum_discount_amount: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    applies_to_all_products: Optional[bool] = None
    product_ids: Optional[List[str]] = None
    category_ids: Optional[List[str]] = None
    brand_ids: Optional[List[str]] = None
    customer_groups: Optional[List[str]] = None
    usage_limit: Optional[int] = Field(None, ge=0)
    stackable: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=0)

class Promotion(PromotionBase, BaseSchema):
    pass

class PromotionUsage(BaseModel):
    promotion_id: str
    customer_id: Optional[str] = None
    order_id: str
    discount_applied: Decimal
    used_at: datetime = Field(default_factory=datetime.utcnow)