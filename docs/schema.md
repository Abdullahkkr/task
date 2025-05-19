# Database Schema Documentation

## Tables

### products
- **id** (PK): unique identifier for each product
- **name**: product name
- **description**: detailed description
- **category**: product category (e.g., Electronics)
- **price**: current unit price
- **created_at**: timestamp when added

### sales
- **id** (PK): unique sale record
- **product_id** (FK): references products.id
- **quantity**: number of units sold
- **total_price**: quantity * product.price at sale time
- **sale_date**: timestamp of sale

### inventory
- **id** (PK): unique inventory record
- **product_id** (FK, unique): references products.id
- **quantity**: current stock level
- **last_updated**: timestamp of last update

### inventory_history
- **id** (PK): unique history record
- **inventory_id** (FK): references inventory.id
- **change**: quantity change (+/-)\- **previous_quantity**: stock before change
- **new_quantity**: stock after change
- **timestamp**: when the change occurred

## Relationships
- **products** 1--* **sales**: one product can have many sales
- **products** 1--1 **inventory**: one product has one inventory record
- **inventory** 1--* **inventory_history**: each inventory record has many history entries