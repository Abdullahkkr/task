# E-commerce Admin API
Provides endpoints for sales retrieval and analytics (daily, weekly, monthly, annual revenue), revenue comparisons across periods and categories, inventory management with low-stock alerts and history tracking, and product registration.

## Setup Instructions
### 1. Clone the repository
git clone https://github.com/Abdullahkkr/task.git

cd task

### 2. Create a virtual environment and install dependencies
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

### 3. Configure the database
Copy .env.example to .env and update with your MySQL credentials

Ensure .env.example is committed and add .env to .gitignore

Run SQL: CREATE DATABASE ecommerce_db;

### 4. Populate demo data
python populate_demo_data.py

### 5. Run the API server
uvicorn main:app --reload

## Endpoints
### Health Check
GET / → { status: OK }

### Products
POST /products/ → Register a new product

### Sales
GET /sales/ → List sales (optional query params: date_from, date_to, product_id, category)

GET /sales/revenue/ → Revenue analytics (period: daily|weekly|monthly|annual, optional category)

GET /sales/compare/ → Compare revenue between periods (period1_start, period1_end, period2_start, period2_end, optional category)

### Inventory
GET /inventory/ → View current inventory (optional low_stock, threshold)

PUT /inventory/{product_id} → Update stock level

GET /inventory/{product_id}/history → Inventory change history (optional start, end filters)

## Database Schema
See docs/schema.md for table and relationship details.