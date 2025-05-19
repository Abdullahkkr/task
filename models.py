from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000))
    category = Column(String(100), index=True)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    sales = relationship('Sale', back_populates='product')
    inventory = relationship('Inventory', uselist=False, back_populates='product')

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    sale_date = Column(DateTime, server_default=func.now(), index=True)

    product = relationship('Product', back_populates='sales')

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    product = relationship('Product', back_populates='inventory')
    history = relationship('InventoryHistory', back_populates='inventory')

class InventoryHistory(Base):
    __tablename__ = 'inventory_history'
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey('inventory.id'), nullable=False, index=True)
    change = Column(Integer, nullable=False)
    previous_quantity = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), index=True)

    inventory = relationship('Inventory', back_populates='history')