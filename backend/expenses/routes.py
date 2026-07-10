# backend/expenses/routes.py
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from datetime import datetime, timedelta
from typing import List, Optional
from bson import ObjectId
import os
import shutil

from fastapi.encoders import jsonable_encoder

from auth.jwt_handler import get_current_user

from database import db


router = APIRouter()

@router.post("/")
async def create_expense(
    description: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    payment_method: str = Form(...),
    notes: Optional[str] = Form(None),
    receipt: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """Create a new expense record"""
    try:

        # Upload receipt if provided
        receipt_url = None
        if receipt:
            # Create uploads directory if not exists
            os.makedirs("uploads/expenses", exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{receipt.filename}"
            filepath = f"uploads/expenses/{filename}"
            
            # Save file
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(receipt.file, buffer)
            
            receipt_url = f"/uploads/expenses/{filename}"
        
        expense_data = {
            "description": description,
            "amount": amount,
            "category": category,
            "payment_method": payment_method,
            "notes": notes,
            "receipt_url": receipt_url,
            "date": datetime.now(),
            "created_at": datetime.now(),
            "created_by": current_user["name"],
            "approved_by": current_user["name"] if current_user["role"] == "admin" else None,
            "store_location": "main"
        }
        
        result = await db["expenses"].insert_one(expense_data)
        expense_data["_id"] = str(result.inserted_id)
        
        return {
            "status": "success",
            "message": "Expense recorded successfully",
            "data": {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in expense_data.items()}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record expense: {str(e)}"
        )

@router.get("/")
async def get_expenses(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get expenses with date filtering"""
    try:
        
        # Build query
        query = {}
        
        if start_date or end_date:
            query["date"] = {}
            if start_date:
                query["date"]["$gte"] = datetime.fromisoformat(start_date)
            if end_date:
                query["date"]["$lte"] = datetime.fromisoformat(end_date) + timedelta(days=1)
        
        if category:
            query["category"] = category
        
        expenses = await db["expenses"].find(query).sort("date", -1).to_list(100)
        
        # Convert ObjectId to string
        for expense in expenses:
            expense["id"] = str(expense["_id"])
            del expense["_id"]
        
        return jsonable_encoder(expenses)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch expenses: {str(e)}"
        )

@router.get("/summary/{date}")
async def get_daily_expense_summary(
    date: str,
    current_user: dict = Depends(get_current_user)
):
    """Get daily expense summary for a specific date"""
    try:
        # db = get_database()
        
        # Parse date
        start_date = datetime.fromisoformat(date)
        end_date = start_date + timedelta(days=1)
        
        # Get all expenses for the date
        expenses = await db["expenses"].find({
            "date": {
                "$gte": start_date,
                "$lt": end_date
            }
        }).to_list(100)
        
        for expense in expenses:
            expense["_id"] = str(expense["_id"])

        
        # Calculate summary
        total_expenses = sum(e["amount"] for e in expenses)
        expenses_by_category = {}
        cash_expenses = 0
        mpesa_expenses = 0
        
        for expense in expenses:
            category = expense.get("category", "miscellaneous")
            expenses_by_category[category] = expenses_by_category.get(category, 0) + expense["amount"]
            
            if expense.get("payment_method") == "cash":
                cash_expenses += expense["amount"]
            elif expense.get("payment_method") == "mpesa":
                mpesa_expenses += expense["amount"]
        
        return {
            "date": date,
            "total_expenses": total_expenses,
            "by_category": expenses_by_category,
            "expenses_count": len(expenses),
            "cash_expenses": cash_expenses,
            "mpesa_expenses": mpesa_expenses,
            "expenses": expenses
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get expense summary: {str(e)}"
        )