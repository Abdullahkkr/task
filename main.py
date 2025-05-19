from fastapi import FastAPI
from routers import products, sales, inventory

app = FastAPI(
    title="E-commerce Admin API",
    description="API for sales analytics and inventory management",
    version="1.0.0"
)

app.include_router(products.router)
app.include_router(sales.router)
app.include_router(inventory.router)

@app.get("/")
def health_check():
    return {"status": "OK"}