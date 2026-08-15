#!/usr/bin/env python3
"""
E-commerce database setup script for PostgreSQL and SQLite.
Creates identical schema and sample data for both databases.
"""

import sqlite3
import os
from datetime import datetime

# Sample data - tuples match table column order
USERS = [
    (1, 'john_doe', 'john@example.com', 'John Doe', '2024-01-15'),
    (2, 'jane_smith', 'jane@example.com', 'Jane Smith', '2024-01-20'),
    (3, 'bob_wilson', 'bob@example.com', 'Bob Wilson', '2024-02-01'),
    (4, 'alice_jones', 'alice@example.com', 'Alice Jones', '2024-02-10'),
    (5, 'charlie_brown', 'charlie@example.com', 'Charlie Brown', '2024-02-15'),
]

CATEGORIES = [
    (1, 'Electronics', 'Electronic devices and accessories'),
    (2, 'Clothing', 'Apparel and fashion items'),
    (3, 'Books', 'Books and publications'),
    (4, 'Home & Garden', 'Home decor and garden supplies'),
    (5, 'Sports', 'Sports and fitness equipment'),
]

PRODUCTS = [
    # Electronics
    (1, 'Wireless Bluetooth Headphones', 'Premium wireless headphones with noise cancellation', 79.99, 1, 150, 4.8),
    (2, 'Smart Fitness Tracker', 'Track steps, heart rate, and sleep patterns', 59.99, 1, 200, 4.6),
    (3, 'USB-C Charging Cable', 'Fast charging USB-C to USB-C cable, 6ft length', 12.99, 1, 500, 4.7),
    # Clothing
    (4, 'Denim Jeans', 'Classic fit denim jeans for men', 49.99, 2, 89, 4.3),
    (5, 'Womens Winter Jacket', 'Waterproof insulated winter jacket', 89.99, 2, 45, 4.5),
    (6, 'Running Shoes', 'Lightweight running shoes with cushioned sole', 64.99, 2, 120, 4.4),
    # Books
    (7, 'Python Programming Guide', 'Comprehensive guide to Python development', 34.99, 3, 75, 4.6),
    (8, 'The Art of War', 'Classic military strategy text by Sun Tzu', 9.99, 3, 300, 4.4),
    (9, 'Data Science Handbook', 'Essential techniques for data scientists', 44.99, 3, 60, 4.7),
    # Home & Garden
    (10, 'Ceramic Plant Pot', 'Decorative planter with drainage hole', 14.99, 4, 180, 4.5),
    (11, 'Stainless Steel Cookware Set', '8-piece stainless steel cookware set', 129.99, 4, 35, 4.8),
    # Sports
    (12, 'Yoga Mat', 'Non-slip eco-friendly yoga mat', 24.99, 5, 200, 4.6),
    (13, 'Dumbbell Set (5-25lbs)', 'Adjustable dumbbell weight set', 89.99, 5, 55, 4.7),
    (14, 'Basketball', 'Official size mens basketball', 19.99, 5, 110, 4.3),
]

ORDERS = [
    (1, 1, '2024-03-01', '2024-03-03', 'delivered', 102.98),
    (2, 2, '2024-03-05', '2024-03-07', 'delivered', 59.99),
    (3, 1, '2024-03-10', '2024-03-12', 'shipped', 149.98),
    (4, 3, '2024-03-12', None, 'pending', 24.99),
    (5, 4, '2024-03-15', None, 'pending', 89.99),
    (6, 2, '2024-03-16', None, 'pending', 109.98),
]

ORDER_ITEMS = [
    (1, 1, 1, 1, 1, 79.99),
    (2, 1, 3, 1, 1, 12.99),
    (3, 2, 2, 1, 1, 59.99),
    (4, 3, 4, 1, 1, 49.99),
    (5, 3, 5, 1, 1, 39.99),
    (6, 3, 11, 1, 1, 89.99),
    (7, 4, 12, 1, 1, 24.99),
    (8, 5, 11, 1, 1, 89.99),
    (9, 6, 6, 1, 1, 64.99),
    (10, 6, 14, 1, 1, 19.99),
]

REVIEWS = [
    (1, 1, 1, 5, 'Amazing sound quality!'),
    (2, 1, 2, 4, 'Great headphones but a bit heavy.'),
    (3, 2, 2, 5, 'Accurate tracking, great battery.'),
    (4, 2, 3, 4, 'Good tracker app needs work.'),
    (5, 4, 3, 4, 'Perfect jeans fit.'),
    (6, 4, 4, 5, 'Best jeans I have owned.'),
    (7, 7, 1, 5, 'Incredible Python resource.'),
    (8, 7, 2, 4, 'Well structured content.'),
    (9, 12, 1, 5, 'Super grippy yoga mat.'),
    (10, 12, 2, 4, 'Good quality but could be longer.'),
]


def setup_sqlite(db_path='ecommerce.db'):
    """Create SQLite database with e-commerce schema and sample data."""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            created_at DATE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        );
        
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category_id INTEGER NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            average_rating REAL DEFAULT 0.0
        );
        
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            ship_date DATE,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            order_item_number INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit_price REAL
        );
        
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at DATE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
        CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
        CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
        CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);
    ''')
    
    cursor.executemany(
        'INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)',
        USERS
    )
    
    cursor.executemany(
        'INSERT OR REPLACE INTO categories VALUES (?, ?, ?)',
        CATEGORIES
    )
    
    cursor.executemany(
        'INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?, ?)',
        PRODUCTS
    )
    
    cursor.executemany(
        'INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?, ?)',
        ORDERS
    )
    
    cursor.executemany(
        'INSERT OR REPLACE INTO order_items VALUES (?, ?, ?, ?, ?, ?)',
        ORDER_ITEMS
    )
    
    # Reviews has 5 columns, and 'created_at' is auto-generated
    cursor.executemany(
        'INSERT OR REPLACE INTO reviews (review_id, product_id, user_id, rating, comment) VALUES (?, ?, ?, ?, ?)',
        REVIEWS
    )
    
    conn.commit()
    conn.close()
    print(f"SQLite database created: {db_path}")


def generate_postgres_script():
    """Generate PostgreSQL setup SQL script."""
    
    script = """-- PostgreSQL e-commerce database setup

CREATE DATABASE ecommerce;

-- Connect to database with: \c ecommerce

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    stock_quantity INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    order_date DATE NOT NULL,
    ship_date DATE,
    status VARCHAR(20) NOT NULL CHECK(status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10,2) NOT NULL
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    order_item_number INTEGER NOT NULL,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2)
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_reviews_product ON reviews(product_id);

-- Insert users
INSERT INTO users (username, email, full_name, created_at) VALUES
('john_doe', 'john@example.com', 'John Doe', '2024-01-15'),
('jane_smith', 'jane@example.com', 'Jane Smith', '2024-01-20'),
('bob_wilson', 'bob@example.com', 'Bob Wilson', '2024-02-01'),
('alice_jones', 'alice@example.com', 'Alice Jones', '2024-02-10'),
('charlie_brown', 'charlie@example.com', 'Charlie Brown', '2024-02-15');

-- Insert categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Books and publications'),
('Home & Garden', 'Home decor and garden supplies'),
('Sports', 'Sports and fitness equipment');

-- Insert products
INSERT INTO products (name, description, price, category_id, stock_quantity, average_rating) VALUES
('Wireless Bluetooth Headphones', 'Premium wireless headphones with noise cancellation', 79.99, 1, 150, 4.8),
('Smart Fitness Tracker', 'Track steps, heart rate, and sleep patterns', 59.99, 1, 200, 4.6),
('USB-C Charging Cable', 'Fast charging USB-C to USB-C cable, 6ft length', 12.99, 1, 500, 4.7),
('Denim Jeans', 'Classic fit denim jeans for men', 49.99, 2, 89, 4.3),
('Womens Winter Jacket', 'Waterproof insulated winter jacket', 89.99, 2, 45, 4.5),
('Running Shoes', 'Lightweight running shoes with cushioned sole', 64.99, 2, 120, 4.4),
('Python Programming Guide', 'Comprehensive guide to Python development', 34.99, 3, 75, 4.6),
('The Art of War', 'Classic military strategy text by Sun Tzu', 9.99, 3, 300, 4.4),
('Data Science Handbook', 'Essential techniques for data scientists', 44.99, 3, 60, 4.7),
('Ceramic Plant Pot', 'Decorative planter with drainage hole', 14.99, 4, 180, 4.5),
('Stainless Steel Cookware Set', '8-piece stainless steel cookware set', 129.99, 4, 35, 4.8),
('Yoga Mat', 'Non-slip eco-friendly yoga mat', 24.99, 5, 200, 4.6),
('Dumbbell Set (5-25lbs)', 'Adjustable dumbbell weight set', 89.99, 5, 55, 4.7),
('Basketball', 'Official size mens basketball', 19.99, 5, 110, 4.3);

-- Insert orders
INSERT INTO orders (user_id, order_date, ship_date, status, total_amount) VALUES
(1, '2024-03-01', '2024-03-03', 'delivered', 102.98),
(2, '2024-03-05', '2024-03-07', 'delivered', 59.99),
(1, '2024-03-10', '2024-03-12', 'shipped', 149.98),
(3, '2024-03-12', NULL, 'pending', 24.99),
(4, '2024-03-15', NULL, 'pending', 89.99),
(2, '2024-03-16', NULL, 'pending', 109.98);

-- Insert order items
INSERT INTO order_items (order_id, order_item_number, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 79.99),
(1, 2, 3, 1, 12.99),
(2, 3, 2, 1, 59.99),
(3, 4, 4, 1, 49.99),
(3, 5, 5, 1, 39.99),
(3, 6, 11, 1, 89.99),
(4, 7, 12, 1, 24.99),
(5, 8, 11, 1, 89.99),
(6, 9, 6, 1, 64.99),
(6, 10, 14, 1, 19.99);

-- Insert reviews
INSERT INTO reviews (product_id, user_id, rating, comment) VALUES
(1, 1, 5, 'Amazing sound quality!'),
(1, 2, 4, 'Great headphones but a bit heavy.'),
(2, 2, 5, 'Accurate tracking, great battery.'),
(2, 3, 4, 'Good tracker app needs work.'),
(4, 3, 4, 'Perfect jeans fit.'),
(4, 4, 5, 'Best jeans I have owned.'),
(7, 1, 5, 'Incredible Python resource.'),
(7, 2, 4, 'Well structured content.'),
(12, 1, 5, 'Super grippy yoga mat.'),
(12, 2, 4, 'Good quality but could be longer.');
"""
    
    return script


def generate_sample_queries():
    """Generate sample SQL queries demonstrating multi-table relationships."""
    
    queries = """-- Sample queries for the e-commerce database

-- 1. Get all orders with user details
SELECT 
    o.order_id,
    u.full_name,
    u.email,
    o.order_date,
    o.status,
    o.total_amount
FROM orders o
JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_date DESC;

-- 2. Get order details with products
SELECT 
    o.order_id,
    u.full_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN users u ON o.user_id = u.user_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id, oi.order_item_number;

-- 3. Get product catalog with category and rating
SELECT 
    p.name AS product_name,
    p.description,
    p.price,
    c.name AS category,
    p.stock_quantity,
    p.average_rating,
    COUNT(r.review_id) AS review_count
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, c.category_id
ORDER BY p.average_rating DESC NULLS LAST
LIMIT 10;

-- 4. Get user purchase history with total spent
SELECT 
    u.username,
    u.full_name,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username, u.full_name
ORDER BY total_spent DESC;

-- 5. Get top-selling products
SELECT 
    p.name AS product_name,
    c.name AS category,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue,
    p.average_rating
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status IN ('delivered', 'shipped')
GROUP BY p.product_id, c.category_id
ORDER BY total_sold DESC
LIMIT 10;

-- 6. Get pending orders with items
SELECT 
    o.order_id,
    u.full_name,
    o.order_date,
    p.name AS product,
    oi.quantity
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'pending'
ORDER BY o.order_date;
"""
    
    return queries


def generate_schema_info():
    """Generate schema documentation."""
    
    info = """# E-Commerce Database Schema

## Tables Overview

### 1. users
Core user/customer information.
- `user_id` (PK) - Unique identifier
- `username` - Unique login name
- `email` - Unique email address
- `full_name` - Customer full name
- `created_at` - Account creation date

### 2. categories
Product categorization system.
- `category_id` (PK) - Unique identifier
- `name` - Category name
- `description` - Category description

### 3. products
Items available for purchase.
- `product_id` (PK) - Unique identifier
- `name` - Product name
- `description` - Product description
- `price` - Current selling price
- `category_id` (FK) - Link to categories
- `stock_quantity` - Available inventory
- `average_rating` - Average customer rating (1-5)

### 4. orders
Customer purchase orders.
- `order_id` (PK) - Unique identifier
- `user_id` (FK) - Link to users
- `order_date` - When order was placed
- `ship_date` - When order will ship (NULL if not shipped)
- `status` - Current order status
- `total_amount` - Order total

### 5. order_items
Line items within orders.
- `item_id` (PK) - Unique identifier
- `order_id` (FK) - Link to orders
- `order_item_number` - Item sequence in order
- `product_id` (FK) - Link to products
- `quantity` - Number of units ordered
- `unit_price` - Price at time of order

### 6. reviews
Customer product reviews.
- `review_id` (PK) - Unique identifier
- `product_id` (FK) - Link to products
- `user_id` (FK) - Link to users
- `rating` - Star rating (1-5)
- `comment` - Review text

## Relationships

```
users ───┐
         ├──> orders ───> order_items ───> products
         ├──> reviews
categories ───────────────────────────────> products
```

## Sample Data Summary

- 5 users
- 5 categories  
- 14 products
- 6 orders
- 10 order items
- 10 reviews

## Sample Queries

See `ecommerce_queries.sql` for example JOIN queries demonstrating:
1. Orders with user details
2. Order details with products
3. Product catalog with categories
4. User purchase history analytics
5. Top-selling products
6. Pending order management
"""
    
    return info


if __name__ == '__main__':
    # Create SQLite database
    print("Setting up SQLite database...")
    setup_sqlite('ecommerce.db')
    
    # Generate PostgreSQL script
    print("Generating PostgreSQL setup script...")
    pg_script = generate_postgres_script()
    with open('setup_postgres.sql', 'w') as f:
        f.write(pg_script)
    print("Created: setup_postgres.sql")
    
    # Generate sample queries
    print("Generating sample queries...")
    queries = generate_sample_queries()
    with open('ecommerce_queries.sql', 'w') as f:
        f.write(queries)
    print("Created: ecommerce_queries.sql")
    
    # Generate schema documentation
    print("Generating schema documentation...")
    docs = generate_schema_info()
    with open('SCHEMA.md', 'w') as f:
        f.write(docs)
    print("Created: SCHEMA.md")
    
    print("\nSetup complete!")
    
    # Verify SQLite database
    print("\nVerifying SQLite database contents:")
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    for table in ['users', 'categories', 'products', 'orders', 'order_items', 'reviews']:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} rows")
    
    conn.close()