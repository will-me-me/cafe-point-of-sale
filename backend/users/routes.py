from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import  List, Optional
from auth.jwt_handler import get_current_user
import jwt
from pydantic import BaseModel, EmailStr, Field, validator
import bcrypt
from users.schema import TokenResponse, UserCreate, UserLogin, UserResponse
from users.services import activate_deactivate_user, create_user, delete_user, get_activity_logs, get_all_user, user_login

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        name=current_user["name"],
        email=current_user["email"],
        role=current_user["role"],
        status=current_user.get("status"),
        created_at=current_user["created_at"]
    )

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    return await create_user(user_data)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    return await user_login(credentials)

@router.get("/users", response_model=List[UserResponse])
async def all_user(current_user: dict = Depends(get_current_user)):
    return await get_all_user()

@router.get("/activity-logs")
async def get_allactivity_logs(current_user: dict = Depends(get_current_user)):
    return await get_activity_logs()

@router.put("/users/{user_id}/status")
async def update_user_status(user_id: str, status: str, current_user: dict = Depends(get_current_user)):
    return await activate_deactivate_user(user_id, status, current_user)

@router.delete("/users/{user_id}")
async def delete_user_by_id(user_id:str, current_user: dict = Depends(get_current_user)):
    return await delete_user(user_id, current_user)

