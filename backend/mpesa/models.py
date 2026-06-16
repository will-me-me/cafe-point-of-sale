# mpesa/models.py
import base64
import re
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Union
from pydantic import BaseModel, field_validator, Field
from dotenv import load_dotenv
import os

load_dotenv()

# ENV VARS
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
PASSKEY = os.getenv("PASSKEY")
SHORTCODE = os.getenv("SHORTCODE", "174379")  # Your Till Number/Paybill
ACCOUNT = os.getenv("DEFAULT_ACCOUNT", "COFFEE_POS")
CALLBACK_URL = os.getenv("CALLBACK_URL", "https://your-domain.com/mpesa/callback")


class PaymentRequest(BaseModel):
    phone_number: str
    amount: int = Field(gt=0, le=150000, description="Amount must be between 1 and 150,000")
    account_reference: Optional[str] = "COFFEE_POS"
    transaction_desc: Optional[str] = "Coffee POS Payment"
    payment_method: Optional[str] = "mpesa"
    till_number: Optional[str] = "174379"  # Your Till Number
    
    @field_validator('phone_number')
    def validate_phone(cls, v):
        v = re.sub(r'\D', '', v)
        if v.startswith('0'):
            v = '254' + v[1:]
        elif v.startswith('+'):
            v = v[1:]
        elif len(v) == 9 and v.startswith('7'):
            v = '254' + v
        if not (v.startswith('254') and len(v) == 12 and v[3:].isdigit()):
            raise ValueError('Phone number must be in format: 2547XXXXXXXX')
        return v


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class STKPushResponse(BaseModel):
    merchant_request_id: str
    checkout_request_id: str
    response_code: str
    response_description: str
    customer_message: str


class CallbackMetadataItem(BaseModel):
    Name: str
    Value: Optional[Union[str, int, float]] = None


class CallbackMetadata(BaseModel):
    Item: List[CallbackMetadataItem]


class STKCallback(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
    CallbackMetadata: Optional[Union[CallbackMetadata, dict]] = None

    class Config:
        arbitrary_types_allowed = True


class CallbackBody(BaseModel):
    stkCallback: STKCallback


class MpesaCallback(BaseModel):
    Body: CallbackBody


class TransactionRecord(BaseModel):
    checkout_request_id: str
    merchant_request_id: str
    amount: float
    mpesa_receipt_number: str
    transaction_date: datetime
    phone_number: str
    status: TransactionStatus
    account_reference: str
    order_id: Optional[str] = None
    customer_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)