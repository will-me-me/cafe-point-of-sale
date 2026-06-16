# mpesa/services.py
import base64
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Configuration
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
SHORTCODE = os.getenv("SHORTCODE", "174379")  # Your Till Number
PASSKEY = os.getenv("PASSKEY")
CALLBACK_URL = os.getenv("CALLBACK_URL", "https://your-domain.com/mpesa/callback")
ACCOUNT = os.getenv("DEFAULT_ACCOUNT", "COFFEE_POS")

# API URLs (Sandbox)
TOKEN_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
STK_QUERY_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"

logger = logging.getLogger(__name__)


def formatted_phone_number(phone: str) -> str:
    """Format phone number to 2547XXXXXXXX format"""
    import re
    phone = re.sub(r'\D', '', phone)
    
    if phone.startswith('0'):
        return '254' + phone[1:]
    elif phone.startswith('+254'):
        return phone[1:]
    elif phone.startswith('254'):
        return phone
    elif len(phone) == 9:
        return '254' + phone
    else:
        raise ValueError(f"Invalid phone number format: {phone}")


def get_access_token() -> str:
    """Get OAuth access token from Daraja API"""
    try:
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        params = {"grant_type": "client_credentials"}
        
        auth_str = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode('utf-8')
        
        headers = {
            "Authorization": f"Basic {encoded_auth}"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        token_data = response.json()
        
        if "access_token" not in token_data:
            raise Exception(f"Access token not found in response: {token_data}")
            
        return token_data["access_token"]
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP {e.response.status_code} Error"
        if e.response.text:
            error_msg += f": {e.response.text}"
        raise Exception(f"Failed to get access token: {error_msg}")
    except Exception as e:
        raise Exception(f"Failed to get access token: {str(e)}")


def generate_stk_password(timestamp: str) -> str:
    """Generate password for STK Push"""
    data_to_encode = f"{SHORTCODE}{PASSKEY}{timestamp}"
    password_stk = base64.b64encode(data_to_encode.encode()).decode()
    return password_stk


def initiate_stk_push(
    phone_number: str,
    amount: int,
    account_reference: str = ACCOUNT,
    transaction_desc: str = "Coffee POS Payment",
    till_number: str = SHORTCODE,
) -> Dict[str, Any]:
    """
    Initiate STK Push payment using Till Number
    
    Args:
        phone_number: Customer phone number (2547XXXXXXXX)
        amount: Amount to charge (1-150,000)
        account_reference: Account reference (e.g., Order ID)
        transaction_desc: Transaction description
        till_number: Your Till Number (default from env)
    
    Returns:
        STK Push response from Daraja API
    """
    try:
        token = get_access_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = generate_stk_password(timestamp)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # For Till Number (Paybill), use CustomerPayBillOnline
        payload = {
            "BusinessShortCode": till_number,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": formatted_phone_number(phone_number),  # Customer phone
            "PartyB": till_number,  # Your Till Number
            "PhoneNumber": formatted_phone_number(phone_number),  # Customer phone
            "CallBackURL": CALLBACK_URL,
            "AccountReference": account_reference,  # Order ID or receipt number
            "TransactionDesc": transaction_desc
        }
        
        logger.info(f"STK Push Payload: {payload}")
        
        response = requests.post(STK_PUSH_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        logger.error(f"STK Push failed: {str(e)}")
        raise Exception(f"STK Push failed: {str(e)}")


def query_stk_status(checkout_request_id: str) -> Dict[str, Any]:
    """Query status of an STK Push transaction"""
    try:
        token = get_access_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = generate_stk_password(timestamp)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        response = requests.post(STK_QUERY_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        raise Exception(f"STK Query failed: {str(e)}")


def save_transaction(transaction_data: dict) -> bool:
    """Save transaction to database"""
    # TODO: Implement your database save logic here
    # This should save to your MongoDB orders collection
    try:
        # Example MongoDB save
        # from database import get_database
        # db = get_database()
        # result = db.transactions.insert_one(transaction_data)
        # return True
        
        logger.info(f"Transaction saved: {transaction_data}")
        return True
    except Exception as e:
        logger.error(f"Failed to save transaction: {str(e)}")
        return False