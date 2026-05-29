from database import db
from bson import ObjectId
from orders.schema import Order
from datetime import datetime
from typing import List
from orders.schema import OrderCreate


def order_entity(order) -> dict:
    return {
        "_id": str(order["_id"]),
        "orderType": order["orderType"],
        "customerName": order.get("customerName"),
        "tableNumber": order.get("tableNumber"),
        "items": order["items"],
        "subtotal": order["subtotal"],
        "tax": order["tax"],
        "total": order["total"],
        "receiptNumber": order["receiptNumber"],
        "created_at": order["created_at"],
    }


def order_list_entity(orders) -> list:
    return [order_entity(order) for order in orders]


async def create_order(order_data: OrderCreate) -> Order:
    order_dict = order_data.model_dump()
    order_dict["created_at"] = datetime.utcnow()
    result = await db["orders"].insert_one(order_dict)
    new_order = await db["orders"].find_one({"_id": result.inserted_id})
    return Order.model_validate(order_entity(new_order))


async def get_orders() -> List[Order]:
    orders_cursor = db["orders"].find().sort("created_at", -1)
    orders = await orders_cursor.to_list(length=100)
    # Convert all MongoDB documents to dicts
    formatted_orders = order_list_entity(orders)
    # Validate and return as Pydantic models
    return [Order(**o) for o in formatted_orders]
