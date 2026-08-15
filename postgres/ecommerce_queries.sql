-- Sample queries for the e-commerce database

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
