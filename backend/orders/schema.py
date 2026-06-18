from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PaymentMode(str, Enum):
    CASH = "cash"
    MPESA = "mpesa"
    DEBT = "debt"
    CARD = "card"  # For future expansion

class PaymentStatus(str, Enum):
    PAID = "completed"
    PENDING = "pending"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


# Each item in the cart
class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int
    
    


# Data received from frontend
class OrderCreate(BaseModel):
    orderType: str  # e.g., "Dine-In" or "Takeaway"
    customerName: Optional[str] = None
    tableNumber: Optional[str] = None
    items: List[OrderItem]
    subtotal: float
    tax: float
    total: float
    receiptNumber: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    paymentMode: Optional[str] = None  # e.g., "Cash", "Card", "Online", "mpesa"
    paymentStatus: Optional[str] = None  # e.g., "Paid", "Pending", "Failed"
    


# Database representation
class Order(OrderCreate):
    id: str = Field(alias="_id")
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
