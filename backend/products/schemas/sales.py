# app/schemas/sales.py
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal
from .enums import BaseSchema, OrderStatus, PaymentMethod

class SaleItemBase(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., ge=0)
    discount: Decimal = Field(default=0, ge=0)
    tax_amount: Decimal = Field(default=0, ge=0)
    total_price: Decimal = Field(..., ge=0)
    batch_number: Optional[str] = None
    serial_numbers: Optional[List[str]] = []

    @field_validator('total_price')
    def calculate_total(cls, v, values):
        quantity = values.get('quantity', 0)
        unit_price = values.get('unit_price', 0)
        discount = values.get('discount', 0)
        tax = values.get('tax_amount', 0)
        return (quantity * unit_price) - discount + tax

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    unit_price: Optional[Decimal] = Field(None, ge=0)
    discount: Optional[Decimal] = Field(None, ge=0)
    tax_amount: Optional[Decimal] = Field(None, ge=0)
    total_price: Optional[Decimal] = Field(None, ge=0)
    batch_number: Optional[str] = None
    serial_numbers: Optional[List[str]] = None

class SaleItem(SaleItemBase, BaseSchema):
    pass

class PaymentBase(BaseModel):
    method: PaymentMethod
    amount: Decimal = Field(..., ge=0)
    reference_number: Optional[str] = None
    payment_date: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(None, max_length=200)

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase, BaseSchema):
    pass

class SaleBase(BaseModel):
    order_number: str = Field(..., min_length=1, max_length=50)
    customer_id: Optional[str] = None
    branch_id: str
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: OrderStatus = OrderStatus.DRAFT
    subtotal: Decimal = Field(..., ge=0)
    tax_total: Decimal = Field(default=0, ge=0)
    discount_total: Decimal = Field(default=0, ge=0)
    shipping_cost: Decimal = Field(default=0, ge=0)
    total_amount: Decimal = Field(..., ge=0)
    amount_paid: Decimal = Field(default=0, ge=0)
    change_due: Decimal = Field(default=0, ge=0)
    notes: Optional[str] = Field(None, max_length=500)
    sales_agent: str
    is_printed: bool = False
    is_void: bool = False
    void_reason: Optional[str] = Field(None, max_length=200)

    @field_validator('total_amount')
    def calculate_total(cls, v, values):
        subtotal = values.get('subtotal', 0)
        tax = values.get('tax_total', 0)
        discount = values.get('discount_total', 0)
        shipping = values.get('shipping_cost', 0)
        return subtotal + tax - discount + shipping

class SaleCreate(SaleBase):
    items: List[SaleItemCreate] = Field(..., min_items=1)
    payments: Optional[List[PaymentCreate]] = []

class SaleUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    subtotal: Optional[Decimal] = Field(None, ge=0)
    tax_total: Optional[Decimal] = Field(None, ge=0)
    discount_total: Optional[Decimal] = Field(None, ge=0)
    shipping_cost: Optional[Decimal] = Field(None, ge=0)
    total_amount: Optional[Decimal] = Field(None, ge=0)
    amount_paid: Optional[Decimal] = Field(None, ge=0)
    change_due: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=500)
    is_printed: Optional[bool] = None
    is_void: Optional[bool] = None
    void_reason: Optional[str] = Field(None, max_length=200)
    items: Optional[List[SaleItemUpdate]] = None
    payments: Optional[List[PaymentCreate]] = None

class Sale(SaleBase, BaseSchema):
    items: List[SaleItem] = []
    payments: List[Payment] = []
    customer: Optional[dict] = None
    branch: Optional[dict] = None
    agent: Optional[dict] = None
    promotion_ids: Optional[List[str]] = []