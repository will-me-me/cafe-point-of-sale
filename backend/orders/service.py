# orders/service.py
from fastapi import HTTPException
from database import db
from bson import ObjectId
from orders.schema import Order, OrderCreate, OrderUpdate, OrderStatus, PaymentStatus
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
import uuid

from products.service import ProductService
from products.services.pricing_service import PricingService



product_service = ProductService()
pricing_service = PricingService()

async def get_product_by_id_or_sku(product_identifier: str):
    """
    Get product by either ID or SKU
    """
    # Try to find by SKU first
    product = await product_service.get_product_by_sku(product_identifier)
    if product:
        return product
    
    # If not found by SKU, try by ID
    try:
        product = await product_service.get_product(product_identifier)
        if product:
            return product
    except:
        pass
    
    return None

def order_entity(order) -> dict:
    return {
        "_id": str(order["_id"]),
        "order_type": order.get("order_type"),
        "customer_id": order.get("customer_id"),
        "customer_name": order.get("customer_name"),
        "customer_phone": order.get("customer_phone"),
        "customer_email": order.get("customer_email"),
        "table_number": order.get("table_number"),
        "branch_id": order.get("branch_id"),
        "items": order.get("items", []),
        "subtotal": order.get("subtotal", 0),
        "tax": order.get("tax", 0),
        "discount_total": order.get("discount_total", 0),
        "total": order.get("total", 0),
        "receipt_number": order.get("receipt_number"),
        "payment_mode": order.get("payment_mode"),
        "payment_status": order.get("payment_status", "pending"),
        "order_status": order.get("order_status", "pending"),
        "notes": order.get("notes"),
        "created_at": order.get("created_at"),
        "updated_at": order.get("updated_at"),
        "completed_at": order.get("completed_at"),
        "total_items": order.get("total_items", 0),
        "profit": order.get("profit", 0),
        "sales_agent": order.get("sales_agent"),
        "created_by": order.get("created_by"),
    }

def order_list_entity(orders) -> list:
    return [order_entity(order) for order in orders]

async def generate_receipt_number() -> str:
    """Generate a unique receipt number"""
    today = datetime.utcnow().strftime("%Y%m%d")
    count = await db["orders"].count_documents({
        "created_at": {
            "$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        }
    })
    return f"RCP-{today}-{count + 1:04d}"

def to_float(value):
    """Convert Decimal or string to float safely"""
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, str):
        return float(value)
    return float(value)

def to_decimal(value):
    """Convert float or string to Decimal safely"""
    if value is None:
        return Decimal('0')
    if isinstance(value, Decimal):
        return value
    if isinstance(value, str):
        return Decimal(value)
    return Decimal(str(value))

async def validate_and_prepare_order(order_data: OrderCreate) -> OrderCreate:
    """Validate products and prepare order with costs"""
    validated_items = []
    total_cost = Decimal('0')
    
    for item in order_data.items:
        # Get product by ID or SKU
        product = await get_product_by_id_or_sku(item.product_id)
        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product not found: {item.product_id}"
            )
        
        # Get the actual product ID
        product_id = product.id if hasattr(product, 'id') else str(product.get('id', item.product_id))
        
        # Initialize cost price
        cost_price = Decimal('0')
        
        # Check if product has variants
        if item.variant_id and product.has_variants:
            # Find the variant - handle both dict and Pydantic model
            variant = None
            if hasattr(product, 'variants'):
                for v in product.variants:
                    # Convert to dict if it's a Pydantic model
                    if hasattr(v, 'dict'):
                        v_dict = v.dict()
                    else:
                        v_dict = v
                    
                    # Check by SKU or ID
                    if v_dict.get('sku') == item.variant_id or v_dict.get('id') == item.variant_id:
                        variant = v_dict
                        break
            
            if not variant:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Variant not found: {item.variant_id}"
                )
            
            # Get variant pricing
            variant_pricing = variant.get('pricing', {})
            
            # Use variant pricing if available
            if variant_pricing:
                # Use variant's selling price if provided in order
                if 'selling_price' in variant_pricing:
                    item.unit_price = float(variant_pricing['selling_price'])
                
                # Use variant's cost price
                if 'cost_price' in variant_pricing:
                    cost_price = to_decimal(variant_pricing['cost_price'])
                elif product.pricing:
                    cost_price = to_decimal(product.pricing.cost_price)
            else:
                # Fallback to parent pricing
                if product.pricing:
                    cost_price = to_decimal(product.pricing.cost_price)
            
            # Set product details from variant
            item.product_name = variant.get('variant_name', product.name)
            item.sku = variant.get('sku', product.sku)
            item.barcode = variant.get('barcode', product.barcode)
            
            # Check variant inventory
            variant_inventory = variant.get('inventory', {})
            available_stock = variant_inventory.get('available', 0) if variant_inventory else 0
            
            if available_stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {item.product_name}. "
                           f"Available: {available_stock}, Required: {item.quantity}"
                )
        else:
            # Simple product without variants
            if product.pricing:
                cost_price = to_decimal(product.pricing.cost_price)
            
            # Set product details
            item.product_name = product.name
            item.sku = product.sku
            item.barcode = product.barcode
            
            # Check inventory
            available_stock = product.inventory.available if product.inventory else 0
            if available_stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {item.product_name}. "
                           f"Available: {available_stock}, Required: {item.quantity}"
                )
        
        # Store cost price
        item.cost_price = float(cost_price)
        
        # Calculate total price (make sure all values are float)
        item.total_price = float(item.quantity) * float(item.unit_price)
        
        # Store the product_id for inventory deduction
        item.product_id = product_id
        item.variant_id = item.variant_id if item.variant_id else None
        
        validated_items.append(item)
        
        # Calculate total cost using Decimal for precision
        total_cost += cost_price * to_decimal(item.quantity)
    
    # Update order with validated items
    order_data.items = validated_items
    order_data.total_items = len(validated_items)
    
    # Calculate profit (total - total_cost)
    total_amount = to_decimal(order_data.total)
    profit = total_amount - total_cost
    order_data.profit = float(profit)
    
    return order_data

async def create_order(order_data: OrderCreate, user_id: str = None) -> Order:
    """Create a new order with inventory deduction"""
    # Validate and prepare order
    validated_order = await validate_and_prepare_order(order_data)
    
    # Generate receipt number if not provided
    if not validated_order.receipt_number:
        validated_order.receipt_number = await generate_receipt_number()
    
    # Convert to dict
    order_dict = validated_order.model_dump()
    order_dict["created_at"] = datetime.utcnow()
    order_dict["updated_at"] = datetime.utcnow()
    order_dict["created_by"] = user_id
    order_dict["order_status"] = OrderStatus.COMPLETED.value
    
    # Insert order
    result = await db["orders"].insert_one(order_dict)
    
    # Deduct inventory for each item
    for item in validated_order.items:
        try:
            # Get product by ID
            product = await product_service.get_product(item.product_id)
            if not product:
                continue
            
            # Calculate quantity to deduct
            deduct_qty = float(item.quantity)
            
            # Check if this is a variant
            if item.variant_id:
                # Find the variant - handle both dict and Pydantic model
                variant = None
                if hasattr(product, 'variants'):
                    for v in product.variants:
                        # Convert to dict if it's a Pydantic model
                        if hasattr(v, 'dict'):
                            v_dict = v.dict()
                        else:
                            v_dict = v
                        
                        # Check by SKU or ID
                        if v_dict.get('sku') == item.variant_id or v_dict.get('id') == item.variant_id:
                            variant = v_dict
                            break
                
                if variant:
                    # Get variant weight for bulk products
                    variant_attributes = variant.get('attributes', {})
                    weight_kg = variant_attributes.get('weight_kg', 0)
                    weight_litre = variant_attributes.get('weight_litre', 0)
                    
                    if weight_kg > 0:
                        deduct_qty = float(item.quantity) * float(weight_kg)
                    elif weight_litre > 0:
                        deduct_qty = float(item.quantity) * float(weight_litre)
            else:
                # For simple products, use quantity as is
                pass
            
            # Deduct inventory
            await product_service.update_inventory(
                product_id=item.product_id,
                quantity_change=-deduct_qty,
                movement_type="sale",
                reason=f"Order {validated_order.receipt_number}",
                user_id=user_id,
                variant_id=item.variant_id,
                reference_id=str(result.inserted_id),
                serial_numbers=item.serial_numbers,
                batch_number=item.batch_number
            )
        except Exception as e:
            # Log error but don't fail the order
            print(f"Error deducting inventory: {e}")
    
    # Get the created order
    new_order = await db["orders"].find_one({"_id": result.inserted_id})
    return Order.model_validate(order_entity(new_order))

async def get_order(order_id: str) -> Optional[Order]:
    """Get a single order by ID"""
    order = await db["orders"].find_one({"_id": ObjectId(order_id)})
    if order:
        return Order.model_validate(order_entity(order))
    return None

async def get_order_by_receipt(receipt_number: str) -> Optional[Order]:
    """Get an order by receipt number"""
    order = await db["orders"].find_one({"receipt_number": receipt_number})
    if order:
        return Order.model_validate(order_entity(order))
    return None

async def get_orders(
    skip: int = 0, 
    limit: int = 100,
    order_status: Optional[str] = None,
    payment_status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Order]:
    """Get orders with filters"""
    query = {}
    
    if order_status:
        query["order_status"] = order_status
    
    if payment_status:
        query["payment_status"] = payment_status
    
    if start_date or end_date:
        query["created_at"] = {}
        if start_date:
            query["created_at"]["$gte"] = start_date
        if end_date:
            query["created_at"]["$lte"] = end_date
    
    cursor = db["orders"].find(query).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    return [Order.model_validate(order_entity(order)) for order in orders]

async def update_order(order_id: str, order_data: OrderUpdate, user_id: str) -> Optional[Order]:
    """Update an order"""
    update_dict = order_data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    update_dict["updated_by"] = user_id
    
    # If order is marked as completed, set completed_at
    if order_data.order_status == OrderStatus.COMPLETED:
        update_dict["completed_at"] = datetime.utcnow()
    
    result = await db["orders"].update_one(
        {"_id": ObjectId(order_id)},
        {"$set": update_dict}
    )
    
    if result.modified_count:
        return await get_order(order_id)
    return None

async def update_payment_status(order_id: str, payment_status: str, user_id: str) -> Optional[Order]:
    """Update order payment status"""
    update_dict = {
        "payment_status": payment_status,
        "updated_at": datetime.utcnow(),
        "updated_by": user_id
    }
    
    result = await db["orders"].update_one(
        {"_id": ObjectId(order_id)},
        {"$set": update_dict}
    )
    
    if result.modified_count:
        return await get_order(order_id)
    return None

async def cancel_order(order_id: str, reason: str, user_id: str) -> Optional[Order]:
    """Cancel an order and restore inventory"""
    order = await get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order status
    update_dict = {
        "order_status": OrderStatus.CANCELLED.value,
        "updated_at": datetime.utcnow(),
        "updated_by": user_id,
        "notes": f"Cancelled: {reason}"
    }
    
    result = await db["orders"].update_one(
        {"_id": ObjectId(order_id)},
        {"$set": update_dict}
    )
    
    if result.modified_count:
        # Restore inventory for cancelled order
        for item in order.items:
            try:
                product = await product_service.get_product(item.product_id)
                if product:
                    # Calculate quantity to restore
                    restore_qty = float(item.quantity)
                    
                    await product_service.update_inventory(
                        product_id=item.product_id,
                        quantity_change=restore_qty,
                        movement_type="returned",
                        reason=f"Order {order.receipt_number} cancelled - {reason}",
                        user_id=user_id,
                        variant_id=item.variant_id,
                        reference_id=order_id,
                        serial_numbers=item.serial_numbers,
                        batch_number=item.batch_number
                    )
            except Exception as e:
                print(f"Error restoring inventory: {e}")
        
        return await get_order(order_id)
    return None

async def get_daily_sales(date: Optional[datetime] = None) -> dict:
    """Get daily sales summary"""
    if not date:
        date = datetime.utcnow()
    
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    query = {
        "created_at": {"$gte": start_of_day, "$lte": end_of_day},
        "order_status": OrderStatus.COMPLETED.value
    }
    
    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": None,
            "total_orders": {"$sum": 1},
            "total_revenue": {"$sum": "$total"},
            "total_profit": {"$sum": "$profit"},
            "total_tax": {"$sum": "$tax"},
            "total_discount": {"$sum": "$discount_total"},
            "total_items": {"$sum": "$total_items"}
        }}
    ]
    
    result = await db["orders"].aggregate(pipeline).to_list(length=1)
    
    if result:
        return {
            "date": date,
            "total_orders": result[0].get("total_orders", 0),
            "total_revenue": result[0].get("total_revenue", 0),
            "total_profit": result[0].get("total_profit", 0),
            "total_tax": result[0].get("total_tax", 0),
            "total_discount": result[0].get("total_discount", 0),
            "total_items": result[0].get("total_items", 0)
        }
    
    return {
        "date": date,
        "total_orders": 0,
        "total_revenue": 0,
        "total_profit": 0,
        "total_tax": 0,
        "total_discount": 0,
        "total_items": 0
    }

async def get_debt_orders(customer_id: Optional[str] = None) -> List[Order]:
    """Get debt orders"""
    query = {
        "payment_status": {"$in": [PaymentStatus.PENDING.value, PaymentStatus.OVERDUE.value]}
    }
    
    if customer_id:
        query["customer_id"] = customer_id
    
    cursor = db["orders"].find(query).sort("created_at", -1)
    orders = await cursor.to_list(length=1000)
    
    return [Order.model_validate(order_entity(order)) for order in orders]