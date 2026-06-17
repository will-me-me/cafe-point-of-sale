from fastapi import APIRouter, Depends, HTTPException
from typing import List
from auth.jwt_handler import get_current_user
from orders.schema import Order, OrderCreate, OrderItem
from datetime import datetime
from bson import ObjectId
import orders.service as order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=Order)
async def create_order_route(order_data: OrderCreate):
    try:
        new_order = await order_service.create_order(order_data)
        return new_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Order])
async def get_orders_route():
    try:
        orders = await order_service.get_orders()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{order_id}/debt", response_model=Order)
async def update_debt_order_route(order_id: str, payment_status: str,current_user: dict = Depends(get_current_user)):
    try:
        updated_order = await order_service.update_debt_order(order_id, payment_status,current_user)
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))