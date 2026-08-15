# PostgreSQL E-Commerce Database

A complete e-commerce database schema and setup scripts for PostgreSQL.

## Files

- `setup_postgres.sql` - SQL script to create tables and insert sample data
- `setup_postgres_db.py` - Python script to programmatically set up the database
- `ecommerce_queries.sql` - Sample queries demonstrating JOIN operations

## Prerequisites

- PostgreSQL installed and running
- A PostgreSQL user with privileges to create databases
- Python with `pg8000` package (or `psycopg2`)

Install Python dependency:
```bash
pip install pg8000
```

## Quick Start

### Option 1: Using SQL script

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Create the database and tables
CREATE DATABASE ecommerce;
\c ecommerce
\i setup_postgres.sql
```

### Option 2: Using Python script

```bash
# Set environment variables if needed
export PG_USER=your_postgres_user
export PG_HOST=localhost
export PG_PORT=5432

# Run the setup script
python3 setup_postgres_db.py
```

## Database Schema

The database contains 6 tables:

### users
- `user_id` (SERIAL PK) - Unique identifier
- `username` (VARCHAR) - Unique login name
- `email` (VARCHAR) - Unique email address
- `full_name` (VARCHAR) - Customer name
- `created_at` (DATE) - Account creation date

### categories
- `category_id` (SERIAL PK) - Unique identifier
- `name` (VARCHAR) - Category name
- `description` (TEXT) - Category description

### products
- `product_id` (SERIAL PK) - Unique identifier
- `name` (VARCHAR) - Product name
- `description` (TEXT) - Product description
- `price` (DECIMAL) - Selling price
- `category_id` (FK) - Links to categories
- `stock_quantity` (INTEGER) - Inventory count
- `average_rating` (DECIMAL) - Average rating 1-5

### orders
- `order_id` (SERIAL PK) - Unique identifier
- `user_id` (FK) - Links to users
- `order_date` (DATE) - Order creation date
- `ship_date` (DATE) - Shipping date (NULL if pending)
- `status` (VARCHAR) - Order status
- `total_amount` (DECIMAL) - Order total

### order_items
- `item_id` (SERIAL PK) - Unique identifier
- `order_id` (FK) - Links to orders
- `order_item_number` (INTEGER) - Item sequence
- `product_id` (FK) - Links to products
- `quantity` (INTEGER) - Ordered quantity
- `unit_price` (DECIMAL) - Price at order time

### reviews
- `review_id` (SERIAL PK) - Unique identifier
- `product_id` (FK) - Links to products
- `user_id` (FK) - Links to users
- `rating` (INTEGER) - Rating 1-5
- `comment` (TEXT) - Review text

## Sample Queries

See `ecommerce_queries.sql` for a collection of example queries:

1. Orders with user details
2. Order details with products
3. Product catalog with categories
4. User purchase history analytics
5. Top-selling products
6. Pending order management

## Sample Data

After setup, you'll have:
- 5 users
- 5 categories
- 14 products
- 6 orders
- 10 order items
- 10 reviews

## Connection Example

```python
import pg8000

conn = pg8000.connect(
    host='localhost',
    port=5432,
    user='your_user',
    password='your_password',
    database='ecommerce'
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM products LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()
```

## Verification

```sql
-- Check all tables exist and have data
SELECT table_name, table_rows 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```