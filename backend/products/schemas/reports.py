# app/schemas/reports.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal

class DateRange(BaseModel):
    start_date: date
    end_date: date

    def __init__(self, **data):
        super().__init__(**data)
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before end date")

class ReportRequest(BaseModel):
    date_range: DateRange
    branch_id: Optional[str] = None
    product_id: Optional[str] = None
    category_id: Optional[str] = None
    supplier_id: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)

class SalesReport(BaseModel):
    total_sales: Decimal
    total_items: int
    total_transactions: int
    average_transaction_value: Decimal
    total_tax: Decimal
    total_discount: Decimal
    net_sales: Decimal
    top_products: List[Dict[str, Any]]
    top_categories: List[Dict[str, Any]]
    sales_by_hour: Dict[str, Decimal]
    sales_by_day: Dict[str, Decimal]
    sales_by_payment_method: Dict[str, Decimal]
    sales_by_branch: Dict[str, Decimal]

class InventoryReport(BaseModel):
    total_products: int
    total_value: Decimal
    total_quantity: int
    out_of_stock_count: int
    low_stock_count: int
    slow_moving_items: List[Dict[str, Any]]
    fast_moving_items: List[Dict[str, Any]]
    inventory_by_category: Dict[str, Dict[str, Any]]
    inventory_by_location: Dict[str, Dict[str, Any]]
    inventory_value_by_supplier: Dict[str, Decimal]

class ProfitReport(BaseModel):
    total_revenue: Decimal
    total_cost: Decimal
    gross_profit: Decimal
    gross_profit_margin: float
    total_expenses: Decimal
    net_profit: Decimal
    net_profit_margin: float
    profit_by_product: List[Dict[str, Any]]
    profit_by_category: List[Dict[str, Any]]
    profit_by_branch: List[Dict[str, Any]]
    profit_trend: Dict[str, Decimal]

class SupplierReport(BaseModel):
    total_suppliers: int
    total_purchase_orders: int
    total_spent: Decimal
    average_lead_time: float
    top_suppliers: List[Dict[str, Any]]
    supplier_performance: List[Dict[str, Any]]
    purchases_by_supplier: Dict[str, Dict[str, Any]]

class ExpiryReport(BaseModel):
    total_expiring_soon: int
    total_expired: int
    expiring_products: List[Dict[str, Any]]
    expired_products: List[Dict[str, Any]]
    value_at_risk: Decimal
    by_category: Dict[str, Dict[str, Any]]

class DashboardStats(BaseModel):
    total_sales_today: Decimal
    total_orders_today: int
    total_customers_today: int
    low_stock_items: int
    out_of_stock_items: int
    pending_orders: int
    total_products: int
    total_value: Decimal
    top_selling_products: List[Dict[str, Any]]
    recent_orders: List[Dict[str, Any]]
    sales_trend: Dict[str, Decimal]
    inventory_status: Dict[str, int]