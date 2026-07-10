# app/schemas/settings.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class CurrencyEnum(str, Enum):
    KES = "KES"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

class TimezoneEnum(str, Enum):
    AFRICA_NAIROBI = "Africa/Nairobi"
    AFRICA_LAGOS = "Africa/Lagos"
    AFRICA_JOHANNESBURG = "Africa/Johannesburg"
    UTC = "UTC"

class OrderTypeEnum(str, Enum):
    DINE_IN = "dine-in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"
    ORDER_ONLINE = "order-online"

class PaymentMethodEnum(str, Enum):
    CASH = "cash"
    MPESA = "mpesa"
    CARD = "card"
    DEBT = "debt"

class ConnectionTypeEnum(str, Enum):
    BLUETOOTH = "bluetooth"
    USB = "usb"
    NETWORK = "network"

class BackupFrequencyEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NEVER = "never"

# Store Settings
class StoreSettings(BaseModel):
    name: str = "Babadeacon Coffee"
    email: str = "info@babadeacon.com"
    address: str = "123 Coffee Street, Nairobi, Kenya"
    phone: str = "+254-700-123456"
    currency: CurrencyEnum = CurrencyEnum.KES
    timezone: TimezoneEnum = TimezoneEnum.AFRICA_NAIROBI
    logo: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class StoreSettingsUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    currency: Optional[CurrencyEnum] = None
    timezone: Optional[TimezoneEnum] = None
    logo: Optional[str] = None

# POS Settings
class POSSettings(BaseModel):
    default_order_type: OrderTypeEnum = OrderTypeEnum.TAKEAWAY
    default_payment: PaymentMethodEnum = PaymentMethodEnum.CASH
    tax_rate: float = 10.0
    receipt_footer: str = "Thank you for your order!"
    auto_print_receipt: bool = True
    require_customer: bool = False
    allow_debt: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class POSSettingsUpdate(BaseModel):
    default_order_type: Optional[OrderTypeEnum] = None
    default_payment: Optional[PaymentMethodEnum] = None
    tax_rate: Optional[float] = Field(None, ge=0, le=100)
    receipt_footer: Optional[str] = None
    auto_print_receipt: Optional[bool] = None
    require_customer: Optional[bool] = None
    allow_debt: Optional[bool] = None

# Product Settings
class ProductSettings(BaseModel):
    default_reorder: int = 10
    low_stock_threshold: int = 5
    enable_variants: bool = True
    track_inventory: bool = True
    require_barcode: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProductSettingsUpdate(BaseModel):
    default_reorder: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    enable_variants: Optional[bool] = None
    track_inventory: Optional[bool] = None
    require_barcode: Optional[bool] = None

# Payment Settings
class PaymentMethodConfig(BaseModel):
    id: str
    name: str
    icon: str
    enabled: bool = True

class PaymentSettings(BaseModel):
    payment_methods: List[PaymentMethodConfig] = [
        PaymentMethodConfig(id="cash", name="Cash", icon="mdi-cash", enabled=True),
        PaymentMethodConfig(id="mpesa", name="M-Pesa", icon="mdi-cellphone", enabled=True),
        PaymentMethodConfig(id="card", name="Card", icon="mdi-credit-card", enabled=False),
        PaymentMethodConfig(id="debt", name="Debt", icon="mdi-account-cash", enabled=True),
    ]
    mpesa_paybill: Optional[str] = None
    mpesa_account: Optional[str] = None
    allow_partial_payment: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaymentSettingsUpdate(BaseModel):
    payment_methods: Optional[List[PaymentMethodConfig]] = None
    mpesa_paybill: Optional[str] = None
    mpesa_account: Optional[str] = None
    allow_partial_payment: Optional[bool] = None

# Receipt Settings
class ReceiptSettings(BaseModel):
    header: str = "☕ BABADEACON COFFEE\nPremium Coffee & Snacks"
    footer: str = "Thank you for your order!\nVisit us again at Babadeacon Coffee"
    paper_width: str = "80"
    font_size: str = "12"
    show_tax_breakdown: bool = True
    show_item_discounts: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ReceiptSettingsUpdate(BaseModel):
    header: Optional[str] = None
    footer: Optional[str] = None
    paper_width: Optional[str] = None
    font_size: Optional[str] = None
    show_tax_breakdown: Optional[bool] = None
    show_item_discounts: Optional[bool] = None

# Printer Settings
class PrinterSettings(BaseModel):
    connection_type: ConnectionTypeEnum = ConnectionTypeEnum.BLUETOOTH
    bluetooth_device: Optional[str] = None
    usb_device: Optional[str] = None
    ip_address: Optional[str] = None
    port: str = "9100"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PrinterSettingsUpdate(BaseModel):
    connection_type: Optional[ConnectionTypeEnum] = None
    bluetooth_device: Optional[str] = None
    usb_device: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[str] = None

# System Settings
class SystemSettings(BaseModel):
    backup_frequency: BackupFrequencyEnum = BackupFrequencyEnum.DAILY
    log_retention: int = 30
    auto_backup: bool = True
    debug_mode: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class SystemSettingsUpdate(BaseModel):
    backup_frequency: Optional[BackupFrequencyEnum] = None
    log_retention: Optional[int] = Field(None, ge=0)
    auto_backup: Optional[bool] = None
    debug_mode: Optional[bool] = None

# Main Settings Schema
class Settings(BaseModel):
    store: StoreSettings
    pos: POSSettings
    products: ProductSettings
    payments: PaymentSettings
    receipt: ReceiptSettings
    printer: PrinterSettings
    system: SystemSettings
    updated_at: Optional[datetime] = None

class SettingsUpdate(BaseModel):
    store: Optional[StoreSettingsUpdate] = None
    pos: Optional[POSSettingsUpdate] = None
    products: Optional[ProductSettingsUpdate] = None
    payments: Optional[PaymentSettingsUpdate] = None
    receipt: Optional[ReceiptSettingsUpdate] = None
    printer: Optional[PrinterSettingsUpdate] = None
    system: Optional[SystemSettingsUpdate] = None