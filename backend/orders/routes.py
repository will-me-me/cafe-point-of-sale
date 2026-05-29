from fastapi import APIRouter, HTTPException
from typing import List
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
