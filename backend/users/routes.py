from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional
from auth.jwt_handler import get_current_user
import jwt
from pydantic import BaseModel, EmailStr, Field, validator
import bcrypt
from users.schema import TokenResponse, UserCreate, UserLogin, UserResponse
from users.services import create_user, user_login

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        name=current_user["name"],
        email=current_user["email"],
        role=current_user["role"],
        created_at=current_user["created_at"]
    )

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    return await create_user(user_data)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    return await user_login(credentials)

