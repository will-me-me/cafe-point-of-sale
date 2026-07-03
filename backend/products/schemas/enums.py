# app/schemas/enums.py
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ProductType(str, Enum):
    STOCK = "stock"
    SERVICE = "service"
    RENTAL = "rental"
    DIGITAL = "digital"

class MovementType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    EXPIRED = "expired"
    RETURNED = "returned"
    RETURN_TO_SUPPLIER = "return_to_supplier"

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    BUY_X_GET_Y = "buy_x_get_y"

class BarcodeType(str, Enum):
    EAN13 = "ean13"
    UPC = "upc"
    CODE128 = "code128"
    QR = "qr"
    INTERNAL = "internal"

class TaxType(str, Enum):
    VAT = "vat"
    GST = "gst"
    SALES_TAX = "sales_tax"
    EXCISE = "excise"

class WarrantyProvider(str, Enum):
    MANUFACTURER = "manufacturer"
    RETAILER = "retailer"
    THIRD_PARTY = "third_party"

class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    MOBILE_MONEY = "mobile_money"
    BANK_TRANSFER = "bank_transfer"
    LOYALTY_POINTS = "loyalty_points"
    CREDIT = "credit"
    OTHER = "other"

class OrderStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class StockStatus(str, Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    LOW_STOCK = "low_stock"
    DISCONTINUED = "discontinued"

# Shared base schemas
class BaseSchema(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Contact(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: Optional[Address] = None