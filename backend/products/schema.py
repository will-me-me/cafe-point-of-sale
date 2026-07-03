# from pydantic import BaseModel, Field, HttpUrl
# from enum import Enum
# from typing import Optional
# from datetime import datetime


# # ---------- CATEGORY ENUM ----------
# class CategoryEnum(str, Enum):
#     coffee = "coffee"
#     tea = "tea"
#     snack = "snack"


# # ---------- BASE SCHEMA ----------
# class ProductBase(BaseModel):
#     name: str
#     price: float
#     category: CategoryEnum
#     image_url: Optional[HttpUrl] = Field(None, description="Link to the product image")


# # ---------- CREATE SCHEMA ----------
# class ProductCreate(ProductBase):
#     pass


# # ---------- DATABASE SCHEMA ----------
# class ProductInDB(ProductBase):
#     id: str = Field(alias="_id")
#     created_at: Optional[datetime]


# # ---------- RESPONSE SCHEMA ----------
# class Product(ProductBase):
#     id: str
#     created_at: Optional[datetime]

#     class Config:
#         from_attributes = True
