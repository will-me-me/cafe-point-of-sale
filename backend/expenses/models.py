from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class ExpenseCategory(str, Enum):
    INVENTORY = "inventory"          # Coffee beans, milk, syrups
    SUPPLIES = "supplies"            # Cups, lids, napkins
    UTILITIES = "utilities"          # Electricity, water, internet
    RENT = "rent"                    # Shop rent
    SALARIES = "salaries"            # Staff wages
    MAINTENANCE = "maintenance"      # Equipment repairs
    MARKETING = "marketing"          # Advertising, promotions
    MISCELLANEOUS = "miscellaneous"  # Other expenses

class Expense(BaseModel):
    id: Optional[str] = None
    description: str
    amount: float = Field(gt=0)
    category: ExpenseCategory
    payment_method: str  # cash, mpesa, bank
    date: datetime = Field(default_factory=datetime.now)
    receipt_url: Optional[str] = None  # For storing receipt images
    notes: Optional[str] = None
    approved_by: Optional[str] = None  # Admin/Manager who approved
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str  # Cashier who recorded it
    store_location: str = "main"

class DailyExpenseSummary(BaseModel):
    date: str
    total_expenses: float
    by_category: dict[str, float]
    expenses_count: int
    cash_expenses: float
    mpesa_expenses: float