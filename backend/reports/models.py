
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel

class DailyFinancialReport(BaseModel):
    # Date
    date: str
    
    # Revenue Section
    total_orders: int
    total_revenue: float
    cash_revenue: float
    mpesa_revenue: float
    debt_revenue: float
    
    # Debt Section
    total_debt_outstanding: float
    debts_cleared_today: List[DebtPaymentRecord]
    new_debts_today: List[str]  # Receipt numbers
    
    # Expenses Section
    total_expenses: float
    expenses_by_category: Dict[str, float]
    expense_transactions: List[Dict]  # List of expense records
    
    # Summary
    net_profit: float  # Revenue - Expenses
    cash_flow: float  # Cash revenue + debt cleared - cash expenses
    profit_margin: float  # (Net Profit / Revenue) * 100
    
    # Notes
    notes: Optional[str] = None

class DebtPaymentRecord(BaseModel):
    receipt_number: str
    customer_name: str
    amount: float
    payment_date: datetime
    payment_method: str