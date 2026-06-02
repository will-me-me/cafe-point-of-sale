from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional
from auth.jwt_handler import create_access_token, hash_password, verify_password
import jwt
from pydantic import BaseModel, EmailStr, Field, validator
import bcrypt
from users.schema import TokenResponse, UserCreate, UserLogin, UserResponse

async def create_user(user_data: UserCreate) -> TokenResponse:
    from database import db
    existing_user = await db["users"].find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user_data.password)
    
    new_user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password,
        "role": user_data.role,
        "created_at": datetime.utcnow(),
    }
    
    result = await db["users"].insert_one(new_user)
    new_user["id"] = str(result.inserted_id) 

    access_token = create_access_token(data={"sub": str(result.inserted_id), "role": user_data.role})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(result.inserted_id),
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
            created_at=new_user["created_at"],
        )
    )

async def user_login(credentials: UserLogin) -> TokenResponse:
    from database import db
    user = await db["users"].find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": str(user["_id"]), "role": user["role"]})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"],
            created_at=user["created_at"],
        )
    )

    

    
    