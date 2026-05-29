import mimetypes
import uuid
import datetime
from supabase import create_client, Client
from typing import List
from fastapi import UploadFile
import os
from dotenv import load_dotenv
from database import db


from products.schema import Product

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "product-images")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def upload_to_supabase(file: UploadFile):
    file_bytes = await file.read()

    extension = file.filename.split(".")[-1]
    unique_id = uuid.uuid4().hex
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{timestamp}_{unique_id}.{extension}"
    file_path = f"uploads/{unique_filename}"

    content_type, _ = mimetypes.guess_type(file.filename)
    if not content_type:
        content_type = "application/octet-stream"

    result = supabase.storage.from_(SUPABASE_BUCKET).upload(
        file_path,
        file_bytes,
        {"content-type": content_type},
    )

    print({"results": file_path})

    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_path)
    if public_url.endswith("?"):
        public_url = public_url[:-1]
    return public_url


def product_entity(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "image_url": product.get("image_url"),
        "created_at": product.get("created_at"),
    }
def order_list_entity(products) -> list:
    return [product_entity(product) for product in products]

async def get_products() -> List[Product]:
    products_cursor = db["products"].find().sort("created_at", -1)
    products = await products_cursor.to_list(length=100)
    formatted_products = order_list_entity(products)
    return [Product(**p) for p in formatted_products]


