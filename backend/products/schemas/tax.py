# app/schemas/tax.py
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal
from .enums import BaseSchema, TaxType

class TaxBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=20)
    tax_type: TaxType
    percentage: Decimal = Field(..., ge=0, le=100)
    inclusive: bool = True  # Is tax included in price
    is_active: bool = True
    description: Optional[str] = Field(None, max_length=200)

class TaxCreate(TaxBase):
    pass

class TaxUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    tax_type: Optional[TaxType] = None
    percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    inclusive: Optional[bool] = None
    is_active: Optional[bool] = None
    description: Optional[str] = Field(None, max_length=200)

class Tax(TaxBase, BaseSchema):
    pass

class TaxGroup(BaseModel):
    name: str
    taxes: List[str]  # Tax IDs
    is_default: bool = False