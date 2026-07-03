# app/schemas/movement.py
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from .enums import BaseSchema, MovementType

class InventoryMovementBase(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    quantity: int = Field(..., ge=0)
    movement_type: MovementType
    reason: str = Field(..., min_length=1, max_length=200)
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None  # e.g., 'purchase', 'sale', 'transfer'
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    batch_number: Optional[str] = None
    serial_numbers: List[str] = Field(default_factory=list) 
    unit_cost: Optional[Decimal] = Field(None, ge=0)
    total_cost: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=500)
    created_by: str

    class Config:
        from_attributes = True

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovementUpdate(BaseModel):
    reason: Optional[str] = Field(None, min_length=1, max_length=200)
    notes: Optional[str] = Field(None, max_length=500)
    batch_number: Optional[str] = None
    serial_numbers: List[str] = Field(default_factory=list) 

class InventoryMovement(InventoryMovementBase, BaseSchema):
    movement_date: datetime = Field(default_factory=datetime.utcnow)
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None

class StockTransfer(BaseModel):
    from_branch_id: str
    to_branch_id: str
    product_id: str
    variant_id: Optional[str] = None
    quantity: int = Field(..., gt=0)
    batch_number: Optional[str] = None
    serial_numbers: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    transfer_date: datetime = Field(default_factory=datetime.utcnow)
    received_date: Optional[datetime] = None
    status: str = "pending"  # pending, in_transit, received, cancelled
    created_by: str
    received_by: Optional[str] = None