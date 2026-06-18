from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orders.routes import router as orders_router
from products.routes import router as products_router
from users.routes import router as users_router
from mpesa.routes import router as mpesa_router
from expenses.routes import router as expenses_router
from reports.routes import router as reports_router
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
app.include_router(expenses_router, prefix="/expenses", tags=["Expenses"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
app.include_router(mpesa_router,  prefix="/mpesa", tags=["M-Pesa"])


@app.get("/")
def root():
    return {"message": "Backend API is running 🚀"}
