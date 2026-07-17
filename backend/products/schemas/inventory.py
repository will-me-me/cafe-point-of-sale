# app/schemas/inventory.py
from typing import Optional, List
from pydantic import Field, validator, BaseModel
from decimal import Decimal
from datetime import datetime, date
from .enums import BaseSchema, StockStatus

class UnitConversion(BaseModel):
    """For products bought in bulk and sold in smaller units"""
    purchase_unit: str = Field(..., max_length=20)
    selling_unit: str = Field(..., max_length=20)
    conversion_factor: Decimal = Field(..., gt=0)
    
    @validator('conversion_factor')
    def validate_conversion(cls, v):
        if v <= 0:
            raise ValueError("Conversion factor must be greater than 0")
        return v

class BatchDetails(BaseModel):
    batch_number: Optional[str] = None
    manufacturing_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    supplier_batch: Optional[str] = None
    production_date: Optional[datetime] = None

class SerialNumber(BaseModel):
    serial: str = Field(..., min_length=1)
    imei: Optional[str] = Field(None, max_length=15)
    engine_number: Optional[str] = None
    is_sold: bool = False
    sold_date: Optional[datetime] = None
    customer_id: Optional[str] = None
    notes: Optional[str] = None

class StockLevel(BaseModel):
    minimum: Decimal = Field(default=Decimal("0"), ge=0)
    maximum: Optional[Decimal] = Field(None, ge=0)
    reorder_point: Decimal = Field(default=Decimal("0"), ge=0)
    reorder_quantity: Decimal = Field(default=Decimal("0"), ge=0)

class InventoryBase(BaseModel):
    product_id: Optional[str] = None  # Made optional
    variant_id: Optional[str] = None
    quantity: Decimal = Field(default=Decimal("0"), ge=0)
    reserved: Decimal = Field(default=Decimal("0"), ge=0)
    available: Optional[Decimal] = Field(None, ge=0)

    min_stock: Optional[Decimal] = Field(None, ge=0)
    max_stock: Optional[Decimal] = Field(None, ge=0)
    reorder_level: Decimal = Field(default=Decimal("0"), ge=0)
    location: Optional[str] = None
    shelf_number: Optional[str] = None
    batch_details: Optional[BatchDetails] = None
    serial_numbers: Optional[List[SerialNumber]] = []
    unit_conversion: Optional[UnitConversion] = None
    status: Optional[StockStatus] = None  # Made optional
    last_count_date: Optional[datetime] = None

    @validator('available', always=True)
    def calculate_available(cls, v, values):
        if 'quantity' in values and 'reserved' in values:
            return values['quantity'] - values['reserved']
        return v

    @validator('status', always=True)
    def set_status(cls, v, values):
        if v is None:  # If status not provided, calculate it
            if 'quantity' in values:
                if values['quantity'] <= 0:
                    return StockStatus.OUT_OF_STOCK
                elif 'reorder_level' in values and values['quantity'] <= values['reorder_level']:
                    return StockStatus.LOW_STOCK
                else:
                    return StockStatus.IN_STOCK
        return v

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[Decimal] = Field(None, ge=0)
    reserved: Optional[Decimal] = Field(None, ge=0)
    min_stock: Optional[Decimal] = Field(None, ge=0)
    max_stock: Optional[Decimal] = Field(None, ge=0)
    reorder_level: Optional[Decimal] = Field(None, ge=0)
    location: Optional[str] = None
    shelf_number: Optional[str] = None
    batch_details: Optional[BatchDetails] = None
    serial_numbers: Optional[List[SerialNumber]] = []
    unit_conversion: Optional[UnitConversion] = None
    status: Optional[StockStatus] = None

class Inventory(InventoryBase, BaseSchema):
    pass