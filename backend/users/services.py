from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional
from auth.jwt_handler import create_access_token, get_current_user, hash_password, verify_password
import jwt
from pydantic import BaseModel, EmailStr, Field, validator
import bcrypt
from users.schema import ActivityLog, TokenResponse, UserCreate, UserLogin, UserResponse
from database import db


async def create_log(
    activity: ActivityLog,
    current_user: dict
) -> None:
    log_entry = {
        "user_id": str(current_user["_id"]),
        "user_name": current_user.get("name"),
        "user_email": current_user.get("email"),
        "action": activity.action,
        "message": activity.message,
        "created_at": datetime.utcnow(),
    }

    await db["activity_logs"].insert_one(log_entry)

async def get_activity_logs():
    logs_cursor = db["activity_logs"].find().sort("created_at", -1)
    logs = []
    async for log in logs_cursor:
        log["id"] = str(log["_id"])
        del log["_id"]
        logs.append(log)
    return logs

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
    await create_log( 
        ActivityLog(
            user_id=str(result.inserted_id),
            action="user_registered",
            message=f"User {user_data.email} registered successfully.",
            user_email=user_data.email,
            user_name=user_data.name,


        ),
        current_user=new_user
    )

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

    await create_log(
        ActivityLog(
            user_id=str(user["_id"]),
            user_email=user["email"],
            user_name=user["name"],
            action="user_logged_in",
            message=f"User {credentials.email} logged in successfully."
        ),
        current_user=user
    )


    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"],
            status=user["status"] if "status" in user else None,
            created_at=user["created_at"],
        )
    )

async def get_all_user():
    users_cursor = db["users"].find().sort("created_at", -1)
    users = []
    async for user in users_cursor:
        user["id"] = str(user["_id"])
        del user["_id"]
        del user["password"]
        users.append(user)
    return users

async def activate_deactivate_user(user_id: str, status: str, current_user: dict):
    current_user_role = current_user["role"]
    if current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can perform this action")
    
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"status": status}})
    
    await create_log(
        ActivityLog(
            user_id=str(current_user["_id"]),
            user_email=current_user["email"],
            user_name=current_user["name"],
            action="user_status_changed",
            message=f"User {user['email']} status changed to {status}."
        ),
        current_user=current_user
    )

    return {"message": f"User {user['email']} status changed to {status}."}
    
async def delete_user(user_id: str, current_user: dict):
    current_user_role = current_user["role"]
    if current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can perform this action")
    
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db["users"].delete_one({"_id": ObjectId(user_id)})
    
    await create_log(
        ActivityLog(
            user_id=str(current_user["_id"]),
            user_email=current_user["email"],
            user_name=current_user["name"],
            action="user_deleted",
            message=f"User {user['email']} deleted."
        ),
        current_user=current_user
    )

    return {"message": f"User {user['email']} deleted."}

    

    
    