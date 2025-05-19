from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
import models, schemas
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/", response_model=list[schemas.Sale])
async def list_sales(
    date_from: datetime = Query(None),
    date_to: datetime = Query(None),
    product_id: int = Query(None),
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Sale)
    if date_from:
        query = query.filter(models.Sale.sale_date >= date_from)
    if date_to:
        query = query.filter(models.Sale.sale_date <= date_to)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)
    if category:
        query = query.join(models.Sale.product).filter(models.Product.category == category)
    return query.all()

@router.get("/revenue/", tags=["analytics"])
async def revenue_analytics(
    period: str = Query("daily", regex="^(daily|weekly|monthly|annual)$"),
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    grp = {
        'daily': [func.date(models.Sale.sale_date)],
        'weekly': [extract('year', models.Sale.sale_date), extract('week', models.Sale.sale_date)],
        'monthly': [extract('year', models.Sale.sale_date), extract('month', models.Sale.sale_date)],
        'annual': [extract('year', models.Sale.sale_date)]
    }[period]
    query = db.query(*grp, func.sum(models.Sale.total_price).label('revenue'))
    if category:
        query = query.join(models.Sale.product).filter(models.Product.category == category)
    query = query.group_by(*grp).order_by(*grp)
    return [{ 'group': row[:-1], 'revenue': float(row[-1]) } for row in query.all()]

@router.get("/compare/", tags=["analytics"])
async def compare_revenue(
    period1_start: datetime,
    period1_end: datetime,
    period2_start: datetime,
    period2_end: datetime,
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    def get_sum(start, end):
        q = db.query(func.sum(models.Sale.total_price))
        q = q.filter(models.Sale.sale_date.between(start, end))
        if category:
            q = q.join(models.Sale.product).filter(models.Product.category == category)
        return float(q.scalar() or 0)
    return {
        'period1': {'start': period1_start, 'end': period1_end, 'revenue': get_sum(period1_start, period1_end)},
        'period2': {'start': period2_start, 'end': period2_end, 'revenue': get_sum(period2_start, period2_end)},
        'difference': get_sum(period2_start, period2_end) - get_sum(period1_start, period1_end)
    }
