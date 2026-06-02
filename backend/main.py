from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orders.routes import router as orders_router
from products.routes import router as products_router
from users.routes import router as users_router
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(products_router)


@app.get("/")
def root():
    return {"message": "Backend API is running 🚀"}
