# orders/schema.py
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class PaymentMode(str, Enum):
    CASH = "cash"
    MPESA = "mpesa"
    DEBT = "debt"
    CARD = "card"
    MOBILE_MONEY = "mobile_money"
    BANK_TRANSFER = "bank_transfer"

class PaymentStatus(str, Enum):
    PAID = "paid"
    PENDING = "pending"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class OrderStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

# Each item in the cart - Now integrated with products
class OrderItem(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    product_name: str
    sku: str
    barcode: Optional[str] = None
    quantity: float
    unit_price: float
    total_price: float
    cost_price: Optional[float] = None
    discount: float = 0
    tax_amount: float = 0
    weight: Optional[float] = None
    weight_litre: Optional[float] = None
    batch_number: Optional[str] = None
    serial_numbers: Optional[List[str]] = None
    
    @validator('total_price')
    def calculate_total(cls, v, values):
        if 'quantity' in values and 'unit_price' in values:
            return values['quantity'] * values['unit_price']
        return v

# Order Create Schema
class OrderCreate(BaseModel):
    order_type: str = "takeaway"
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    table_number: Optional[str] = None
    branch_id: Optional[str] = None
    items: List[OrderItem]
    subtotal: float
    tax: float
    discount_total: float = 0
    total: float
    receipt_number: Optional[str] = None  # Made optional
    payment_mode: Optional[PaymentMode] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING
    order_status: OrderStatus = OrderStatus.PENDING
    notes: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    sales_agent: Optional[str] = None
    total_items: Optional[int] = 0
    profit: Optional[float] = None

# Order Response Schema
class Order(OrderCreate):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_items: int = 0
    profit: Optional[float] = None

    class Config:
        from_attributes = True
        populate_by_name = True

# Order Update Schema
class OrderUpdate(BaseModel):
    order_status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    payment_mode: Optional[PaymentMode] = None
    notes: Optional[str] = None
    items: Optional[List[OrderItem]] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    discount_total: Optional[float] = None
    total: Optional[float] = None