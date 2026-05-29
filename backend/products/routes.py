from fastapi import APIRouter, Form, HTTPException
from typing import List
from datetime import datetime
from bson import ObjectId
from fastapi import FastAPI, UploadFile, File
from products.schema import CategoryEnum, Product
import products.service as product_service
from database import db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    image_url = await product_service.upload_to_supabase(file)
    return {"image_url": image_url}


@router.post("/", response_model=Product)
async def create_product(
    name: str = Form(...),
    price: float = Form(...),
    category: CategoryEnum = Form(...),
    image: UploadFile = File(...),
):
    try:
        image_url = await product_service.upload_to_supabase(image)

        product_data = {
            "name": name,
            "price": price,
            "category": category,
            "image_url": image_url,
            "created_at": datetime.utcnow(),
        }
        print("Product data to insert:", product_data)  # Debugging statement
        result = await db["products"].insert_one(product_data)

        product_data["_id"] = str(result.inserted_id)
        return Product(**product_service.product_entity(product_data))
        # return Product(**product_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/", response_model=List[Product])
async def get_all_products():
    try:
        products = await product_service.get_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
