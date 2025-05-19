from database import SessionLocal, engine, Base
import models
from datetime import datetime, timedelta
import random

# Create tables
Base.metadata.create_all(bind=engine)

# Demo entries
demo_products = [
    {"name": "Amazon Echo Dot", "description": "Smart speaker with Alexa.", "category": "Electronics", "price": 49.99},
    {"name": "Walmart USB-C Charger", "description": "Fast charging USB-C adapter.", "category": "Electronics", "price": 19.99}
]

session = SessionLocal()
# Insert products
products = []
for p in demo_products:
    prod = models.Product(**p)
    session.add(prod)
    session.commit()
    session.refresh(prod)
    products.append(prod)

# Initialize inventory and sales
for prod in products:
    inv = models.Inventory(product_id=prod.id, quantity=random.randint(20, 100))
    session.add(inv)
    session.commit()
    # generate sales over past 30 days
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        qty = random.randint(1, 5)
        sale = models.Sale(
            product_id=prod.id,
            quantity=qty,
            total_price=round(qty * float(prod.price), 2),
            sale_date=date
        )
        session.add(sale)
    session.commit()

# Log initial inventory history
for inv in session.query(models.Inventory).all():
    hist = models.InventoryHistory(
        inventory_id=inv.id,
        change=0,
        previous_quantity=inv.quantity,
        new_quantity=inv.quantity
    )
    session.add(hist)
session.commit()
session.close()
print("Demo data populated successfully.")