-- PostgreSQL e-commerce database setup

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
