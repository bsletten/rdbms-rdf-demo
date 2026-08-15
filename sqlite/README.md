# SQLite E-Commerce Database

A complete e-commerce database for SQLite with sample data and query examples.

## Files

- `ecommerce.db` - SQLite database file (ready to use)
- `db_setup.py` - Python script to create the database from scratch
- `ecommerce_queries.sql` - Sample queries demonstrating JOIN operations

## Quick Start

### Using the existing database

```bash
# Query the database
sqlite3 ecommerce.db

# Run queries
sqlite3 ecommerce.db < ecommerce_queries.sql

# Or interactive mode
sqlite3 ecommerce.db
```

### Creating the database from scratch

```bash
python3 db_setup.py
```

## Database Schema

The database contains 6 tables representing a complete e-commerce system:

- **users** - Customer accounts (5 users)
- **categories** - Product categories (5 categories)
- **products** - Items for sale (14 products)
- **orders** - Customer orders (6 orders)
- **order_items** - Order line items (10 items)
- **reviews** - Product reviews (10 reviews)

## Sample Queries

### List all orders with customer names

```sql
SELECT o.order_id, u.full_name, o.order_date, o.status, o.total_amount
FROM orders o
JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_date DESC;
```

### Get order details with products

```sql
SELECT 
    o.order_id,
    u.full_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN users u ON o.user_id = u.user_id
JOIN products p ON oi.product_id = p.product_id;
```

### Top-selling products

```sql
SELECT 
    p.name AS product_name,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status IN ('delivered', 'shipped')
GROUP BY p.product_id
ORDER BY total_sold DESC;
```

## Data Summary

- 5 users with sample email addresses
- 5 categories: Electronics, Clothing, Books, Home & Garden, Sports
- 14 products spanning all categories with prices from $9.99 to $129.99
- 6 orders with statuses: pending, shipped, delivered
- 10 product reviews with ratings 1-5

## Running Tests

```bash
# Verify database integrity
sqlite3 ecommerce.db "PRAGMA integrity_check;"

# Count rows in each table
sqlite3 ecommerce.db "SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'categories', COUNT(*) FROM categories
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'reviews', COUNT(*) FROM reviews;"
```