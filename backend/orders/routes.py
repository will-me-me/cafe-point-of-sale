# orders/routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from auth.jwt_handler import get_current_user
from orders.schema import Order, OrderCreate, OrderUpdate, OrderStatus, PaymentStatus
import orders.service as order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=Order)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new order with inventory deduction"""
    try:
        new_order = await order_service.create_order(
            order_data, 
            user_id=str(current_user["_id"])
        )
        return new_order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Order])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    order_status: Optional[str] = None,
    payment_status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get orders with filters"""
    try:
        orders = await order_service.get_orders(
            skip=skip,
            limit=limit,
            order_status=order_status,
            payment_status=payment_status,
            start_date=start_date,
            end_date=end_date
        )
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a single order by ID"""
    order = await order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/receipt/{receipt_number}", response_model=Order)
async def get_order_by_receipt(
    receipt_number: str,
    current_user: dict = Depends(get_current_user)
):
    """Get an order by receipt number"""
    order = await order_service.get_order_by_receipt(receipt_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: str,
    order_data: OrderUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update an order"""
    try:
        updated_order = await order_service.update_order(
            order_id, 
            order_data, 
            str(current_user["_id"])
        )
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}/payment", response_model=Order)
async def update_payment_status(
    order_id: str,
    payment_status: PaymentStatus,
    current_user: dict = Depends(get_current_user)
):
    """Update order payment status"""
    try:
        updated_order = await order_service.update_payment_status(
            order_id, 
            payment_status.value, 
            str(current_user["_id"])
        )
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{order_id}/cancel", response_model=Order)
async def cancel_order(
    order_id: str,
    reason: str = Query(..., description="Reason for cancellation"),
    current_user: dict = Depends(get_current_user)
):
    """Cancel an order and restore inventory"""
    try:
        cancelled_order = await order_service.cancel_order(
            order_id, 
            reason, 
            str(current_user["_id"])
        )
        if not cancelled_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return cancelled_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debt/list", response_model=List[Order])
async def get_debt_orders(
    customer_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all debt orders"""
    try:
        orders = await order_service.get_debt_orders(customer_id)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/daily-sales")
async def get_daily_sales(
    date: Optional[datetime] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get daily sales summary"""
    try:
        sales = await order_service.get_daily_sales(date)
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))