from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas
from database import SessionLocal

router = APIRouter(prefix="/inventory", tags=["inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.InventoryOut])
async def get_inventory(
    low_stock: bool = Query(False),
    threshold: int = Query(10),
    db: Session = Depends(get_db)
):
    query = db.query(models.Inventory)
    if low_stock:
        query = query.filter(models.Inventory.quantity <= threshold)
    return query.all()

class InventoryUpdate(BaseModel):
    quantity: int

@router.put("/{product_id}", response_model=schemas.InventoryOut)
async def update_inventory(
    product_id: int,
    update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    inv = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(404, "Inventory record not found")
    prev_qty = inv.quantity
    inv.quantity = update.quantity
    db.add(inv)
    db.commit()
    db.refresh(inv)
    # log history
    history = models.InventoryHistory(
        inventory_id=inv.id,
        change=update.quantity - prev_qty,
        previous_quantity=prev_qty,
        new_quantity=update.quantity
    )
    db.add(history)
    db.commit()
    return inv

@router.get("/{product_id}/history", response_model=list[schemas.InventoryHistoryOut])
async def inventory_history(
    product_id: int,
    start: datetime = Query(None),
    end: datetime = Query(None),
    db: Session = Depends(get_db)
):
    inv = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(404, "Inventory record not found")
    q = db.query(models.InventoryHistory).filter(models.InventoryHistory.inventory_id == inv.id)
    if start:
        q = q.filter(models.InventoryHistory.timestamp >= start)
    if end:
        q = q.filter(models.InventoryHistory.timestamp <= end)
    return q.all()