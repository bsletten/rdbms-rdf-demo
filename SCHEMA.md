# E-Commerce Database Schema

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
