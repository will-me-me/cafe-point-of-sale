# backend/reports/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from typing import List, Optional
from bson import ObjectId

from auth.jwt_handler import get_current_user
from database import db


router = APIRouter()

@router.get("/daily/{date}")
async def get_daily_financial_report(
    date: str,
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive daily financial report"""
    try:
      
        
        # Parse date range
        start_date = datetime.fromisoformat(date)
        end_date = start_date + timedelta(days=1)
        
        # ===== GET ORDERS FOR THE DAY =====
        orders = await db["orders"].find({
            "created_at": {"$gte": start_date, "$lt": end_date}
        }).to_list(1000)

        
        # ===== CALCULATE REVENUE =====
        total_revenue = sum(o.get("total", 0) for o in orders)
        cash_revenue = sum(o.get("total", 0) for o in orders if o.get("paymentMode") == "cash")
        mpesa_revenue = sum(o.get("total", 0) for o in orders if o.get("paymentMode") == "mpesa")
        
        # Debt revenue (pending debts)
        debt_orders = [o for o in orders if o.get("paymentMode") == "debt" and o.get("paymentStatus") == "pending"]
        debt_revenue = sum(o.get("total", 0) for o in debt_orders)
        
        # Debt cleared today
        cleared_debts = [o for o in orders if o.get("paymentMode") == "debt" and o.get("paymentStatus") == "completed"]
        debts_cleared_today = sum(o.get("total", 0) for o in cleared_debts)
        
        # ===== GET EXPENSES FOR THE DAY =====
        expenses = await db["expenses"].find({
            "date": {"$gte": start_date, "$lt": end_date}
        }).to_list(1000)
        
        
        total_expenses = sum(e.get("amount", 0) for e in expenses)
        expenses_by_category = {}
        
        for expense in expenses:
            category = expense.get("category", "miscellaneous")
            expenses_by_category[category] = expenses_by_category.get(category, 0) + expense["amount"]
        
        # ===== GET OUTSTANDING DEBTS =====
        all_debts = await db["orders"].find({
            "paymentMode": "debt",
            "paymentStatus": "pending"
        }).to_list(1000)
        
        total_debt_outstanding = sum(o.get("total", 0) for o in all_debts)
        unique_debt_customers = len(set(o.get("customerName", "") for o in all_debts))
        
        # ===== CALCULATE PROFIT =====
        net_profit = total_revenue - total_expenses
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Cash flow (actual cash received - cash expenses)
        cash_expenses = sum(e.get("amount", 0) for e in expenses if e.get("payment_method") == "cash")
        cash_flow = cash_revenue + mpesa_revenue + debts_cleared_today - cash_expenses
        
        return {
            "date": date,
            "totalRevenue": total_revenue,
            "cashRevenue": cash_revenue,
            "mpesaRevenue": mpesa_revenue,
            "debtRevenue": debt_revenue,
            "debtsClearedToday": debts_cleared_today,
            "totalExpenses": total_expenses,
            "expensesByCategory": expenses_by_category,
            "expenseCount": len(expenses),
            "netProfit": net_profit,
            "profitMargin": profit_margin,
            "cashFlow": cash_flow,
            "totalOrders": len(orders),
            "totalDebtOutstanding": total_debt_outstanding,
            "newDebtsToday": len(debt_orders),
            "debtCustomers": unique_debt_customers,
            "debtOrders": [
                {
                    "id": str(o["_id"]),
                    "receiptNumber": o.get("receiptNumber"),
                    "customerName": o.get("customerName"),
                    "total": o.get("total"),
                    "created_at": o.get("created_at")
                }
                for o in debt_orders[:10]  # Last 10 debts
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get financial report: {str(e)}"
        )

@router.get("/debt/overview")
async def get_debt_overview(
    current_user: dict = Depends(get_current_user)
):
    """Get overview of all outstanding debts"""
    try:
        
        # Get all pending debts
        debts = await db["orders"].find({
            "paymentMode": "debt",
            "paymentStatus": "pending"
        }).to_list(1000)

        
        # Calculate debt aging
        now = datetime.now()
        debt_summary = {
            "total_debt": 0,
            "total_customers": 0,
            "average_age": 0,
            "by_age": {
                "0-7_days": 0,
                "8-14_days": 0,
                "15-30_days": 0,
                "30+_days": 0
            },
            "debts": []
        }
        
        total_age = 0
        customers = set()
        
        for debt in debts:
            amount = debt.get("total", 0)
            debt_summary["total_debt"] += amount
            
            customer = debt.get("customerName", "")
            customers.add(customer)
            
            # Calculate age
            age_days = (now - debt.get("created_at", now)).days
            total_age += age_days
            
            # Categorize by age
            if age_days <= 7:
                debt_summary["by_age"]["0-7_days"] += amount
            elif age_days <= 14:
                debt_summary["by_age"]["8-14_days"] += amount
            elif age_days <= 30:
                debt_summary["by_age"]["15-30_days"] += amount
            else:
                debt_summary["by_age"]["30+_days"] += amount
            
            debt_summary["debts"].append({
                "id": str(debt["_id"]),
                "receiptNumber": debt.get("receiptNumber"),
                "customerName": customer,
                "total": amount,
                "age_days": age_days,
                "created_at": debt.get("created_at")
            })
        
        debt_summary["total_customers"] = len(customers)
        debt_summary["average_age"] = total_age / len(debts) if debts else 0
        
        return debt_summary
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get debt overview: {str(e)}"
        )

@router.put("/debt/{order_id}/pay")
async def mark_debt_as_paid(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark a debt order as paid"""
    try:
        
        # Find the order
        order = await db["orders"].find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Update order status
        result = await db["orders"].update_one(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "paymentStatus": "completed",
                    "paymentMode": "debt",
                    "updated_at": datetime.now(),
                    "cleared_at": datetime.now(),
                    "cleared_by": current_user["name"]
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update order status"
            )
        
        return {
            "status": "success",
            "message": "Debt marked as paid successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark debt as paid: {str(e)}"
        )