# app/schemas/purchase.py
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal

from products.schemas.enums import BaseSchema, OrderStatus


class PurchaseItemBase(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    quantity: int = Field(..., ge=1)
    unit_cost: Decimal = Field(..., ge=0)
    total_cost: Decimal = Field(..., ge=0)
    discount: Decimal = Field(default=0, ge=0)
    tax_amount: Decimal = Field(default=0, ge=0)
    batch_number: Optional[str] = None
    received_quantity: int = Field(default=0, ge=0)
    notes: Optional[str] = Field(None, max_length=200)

    @field_validator('total_cost', always=True)
    def calculate_total(cls, v, values):
        if 'quantity' in values and 'unit_cost' in values:
            return values['quantity'] * values['unit_cost']
        return v

class PurchaseItemCreate(PurchaseItemBase):
    pass

class PurchaseItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    unit_cost: Optional[Decimal] = Field(None, ge=0)
    total_cost: Optional[Decimal] = Field(None, ge=0)
    discount: Optional[Decimal] = Field(None, ge=0)
    tax_amount: Optional[Decimal] = Field(None, ge=0)
    batch_number: Optional[str] = None
    received_quantity: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=200)

class PurchaseItem(PurchaseItemBase, BaseSchema):
    pass

class PurchaseBase(BaseModel):
    supplier_id: str
    purchase_order_number: str = Field(..., min_length=1, max_length=50)
    order_date: datetime = Field(default_factory=datetime.utcnow)
    expected_delivery_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    status: OrderStatus = OrderStatus.DRAFT
    subtotal: Decimal = Field(..., ge=0)
    tax_total: Decimal = Field(default=0, ge=0)
    discount_total: Decimal = Field(default=0, ge=0)
    shipping_cost: Decimal = Field(default=0, ge=0)
    total_amount: Decimal = Field(..., ge=0)
    amount_paid: Decimal = Field(default=0, ge=0)
    payment_status: str = "unpaid"  # unpaid, partial, paid
    notes: Optional[str] = Field(None, max_length=500)
    branch_id: Optional[str] = None
    created_by: str
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None

    @field_validator('total_amount', always=True)
    def calculate_total(cls, v, values):
        subtotal = values.get('subtotal', 0)
        tax = values.get('tax_total', 0)
        discount = values.get('discount_total', 0)
        shipping = values.get('shipping_cost', 0)
        return subtotal + tax - discount + shipping

class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate] = Field(..., min_items=1)

class PurchaseUpdate(BaseModel):
    supplier_id: Optional[str] = None
    purchase_order_number: Optional[str] = Field(None, min_length=1, max_length=50)
    expected_delivery_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    status: Optional[OrderStatus] = None
    subtotal: Optional[Decimal] = Field(None, ge=0)
    tax_total: Optional[Decimal] = Field(None, ge=0)
    discount_total: Optional[Decimal] = Field(None, ge=0)
    shipping_cost: Optional[Decimal] = Field(None, ge=0)
    total_amount: Optional[Decimal] = Field(None, ge=0)
    amount_paid: Optional[Decimal] = Field(None, ge=0)
    payment_status: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    branch_id: Optional[str] = None
    items: Optional[List[PurchaseItemUpdate]] = None

class Purchase(PurchaseBase, BaseSchema):
    items: List[PurchaseItem] = []
    supplier: Optional[dict] = None
    branch: Optional[dict] = None
    creator: Optional[dict] = None
    approver: Optional[dict] = None
    receipt_status: str = "pending"  # pending, partial, received