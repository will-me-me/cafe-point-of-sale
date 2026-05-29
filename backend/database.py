from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
try:
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["shop_db"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    database = None
