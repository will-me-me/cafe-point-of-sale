# mpesa/routes.py
from fastapi import APIRouter, Request, Depends, HTTPException, status
from datetime import datetime
import logging
from typing import Optional

from mpesa.models import (
    MpesaCallback, PaymentRequest, STKPushResponse, 
    TransactionStatus, TransactionRecord
)
from mpesa.services import (
    CALLBACK_URL, SHORTCODE, get_access_token, initiate_stk_push, 
    query_stk_status, save_transaction
)

router = APIRouter(tags=["M-Pesa"])
logger = logging.getLogger(__name__)


@router.post("/stk-push", response_model=STKPushResponse)
async def lipa_na_mpesa(req: PaymentRequest):
    """
    Initiate STK Push payment using Till Number
    
    This endpoint triggers an STK Push to the customer's phone.
    
    Args:
        req: Payment request with phone, amount, and order details
    
    Returns:
        STKPushResponse with checkout request ID
    """
    try:
        # Validate amount range
        if req.amount < 1 or req.amount > 150000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be between 1 and 150,000"
            )
        
        # Initiate STK Push
        response = initiate_stk_push(
            phone_number=req.phone_number,
            amount=req.amount,
            account_reference=req.account_reference or f"ORDER-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            transaction_desc=req.transaction_desc or "Coffee POS Payment",
            till_number=req.till_number or SHORTCODE
        )
        
        # Log the request
        logger.info(f"STK Push initiated: {response}")
        
        # Save initial transaction record
        transaction_data = {
            "checkout_request_id": response.get("CheckoutRequestID", ""),
            "merchant_request_id": response.get("MerchantRequestID", ""),
            "amount": req.amount,
            "phone_number": req.phone_number,
            "account_reference": req.account_reference,
            "status": TransactionStatus.PENDING,
            "created_at": datetime.now()
        }
        save_transaction(transaction_data)
        
        # Parse and return standardized response
        return STKPushResponse(
            merchant_request_id=response.get("MerchantRequestID", ""),
            checkout_request_id=response.get("CheckoutRequestID", ""),
            response_code=response.get("ResponseCode", ""),
            response_description=response.get("ResponseDescription", ""),
            customer_message=response.get("CustomerMessage", "")
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"STK Push failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate payment: {str(e)}"
        )


@router.post("/callback")
async def mpesa_callback(request: Request):
    """
    Handle M-Pesa STK Push callback
    
    This endpoint receives payment confirmation from Daraja API.
    """
    try:
        # Parse callback data
        callback_data = await request.json()
        logger.info(f"M-Pesa callback received: {callback_data}")
        
        try:
            # Validate and parse using Pydantic model
            callback = MpesaCallback(**callback_data)
        except Exception as validation_error:
            logger.error(f"Pydantic validation failed: {validation_error}")
            # Return success to M-Pesa anyway
            return {"ResultCode": 0, "ResultDesc": "Success"}
        
        stk_callback = callback.Body.stkCallback
        
        # Check transaction result
        if stk_callback.ResultCode == 0:
            # Payment successful
            logger.info(f"Payment successful: {stk_callback.CheckoutRequestID}")
            
            # Extract transaction details
            if stk_callback.CallbackMetadata:
                metadata = {}
                for item in stk_callback.CallbackMetadata['Item']:
                    metadata[item['Name']] = item.get('Value')
                
                # Prepare transaction data
                transaction_data = {
                    "checkout_request_id": stk_callback.CheckoutRequestID,
                    "merchant_request_id": stk_callback.MerchantRequestID,
                    "amount": metadata.get("Amount"),
                    "mpesa_receipt_number": metadata.get("MpesaReceiptNumber"),
                    "transaction_date": datetime.strptime(
                        str(metadata.get("TransactionDate", "")), 
                        "%Y%m%d%H%M%S"
                    ) if metadata.get("TransactionDate") else datetime.now(),
                    "phone_number": metadata.get("PhoneNumber"),
                    "status": TransactionStatus.SUCCESS,
                    "updated_at": datetime.now()
                }
                
                # Save to database
                save_transaction(transaction_data)
                
                # TODO: Update order status in your orders collection
                # await update_order_status(stk_callback.CheckoutRequestID, "completed")
                
                logger.info(f"Transaction completed: {transaction_data}")
                
        else:
            # Payment failed
            logger.warning(
                f"Payment failed: {stk_callback.ResultDesc} "
                f"(Code: {stk_callback.ResultCode})"
            )
            
            # Update transaction status in database
            failed_data = {
                "checkout_request_id": stk_callback.CheckoutRequestID,
                "merchant_request_id": stk_callback.MerchantRequestID,
                "status": TransactionStatus.FAILED,
                "failure_reason": stk_callback.ResultDesc,
                "result_code": stk_callback.ResultCode,
                "updated_at": datetime.now()
            }
            save_transaction(failed_data)
        
        # Always return success to Daraja
        return {
            "ResultCode": 0,
            "ResultDesc": "Success"
        }
        
    except Exception as e:
        logger.error(f"Error processing callback: {str(e)}")
        # Still return success to Daraja to avoid retries
        return {
            "ResultCode": 0,
            "ResultDesc": "Success"
        }


@router.get("/transaction-status/{checkout_request_id}")
async def get_transaction_status(checkout_request_id: str):
    """
    Check status of an STK Push transaction
    """
    try:
        result = query_stk_status(checkout_request_id)
        
        # Interpret result code
        result_code = result.get("ResultCode")
        status_messages = {
            "0": "Transaction completed successfully",
            "1": "Transaction failed",
            "1037": "Transaction timeout - customer didn't respond",
            "1032": "Transaction cancelled by user"
        }
        
        status_msg = status_messages.get(result_code, result.get("ResultDesc", "Unknown status"))
        
        return {
            "checkout_request_id": checkout_request_id,
            "result_code": result_code,
            "result_description": result.get("ResultDesc"),
            "status": status_msg,
            "raw_response": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query transaction status: {str(e)}"
        )


@router.get("/test")
async def test_mpesa():
    """Test endpoint to verify M-Pesa configuration"""
    try:
        token = get_access_token()
        
        return {
            "status": "success",
            "message": "M-Pesa API is configured correctly",
            "shortcode": SHORTCODE,
            "callback_url": CALLBACK_URL,
            "token_available": bool(token)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"M-Pesa configuration error: {str(e)}"
        }