# E-Commerce Database

A multi-database e-commerce schema implementation with sample data.

## Overview

This project demonstrates how to create identical database schemas across different database engines (SQLite and PostgreSQL) for a complete e-commerce system.

## Structure

```
hermes/src/
├── README.md           # This file
├── SCHEMA.md           # Schema documentation
├── ecommerce_queries.sql   # Sample SQL queries
│
├── sqlite/            # SQLite implementation
│   ├── README.md
│   ├── ecommerce.db   # SQLite database file
│   └── db_setup.py    # Setup script
│
└── postgres/          # PostgreSQL implementation
    ├── README.md
    ├── setup_postgres.sql   # SQL setup script
    ├── setup_postgres_db.py # Python setup script
    └── ecommerce_queries.sql
```

## Database Schema

The schema models a complete e-commerce system with 6 tables:

| Table | Description | Records |
|-------|-------------|---------|
| users | Customer accounts | 5 |
| categories | Product categories | 5 |
| products | Items for sale | 14 |
| orders | Customer orders | 6 |
| order_items | Order line items | 10 |
| reviews | Product reviews | 10 |

**Relationships:**
- users → orders (1:N)
- users → reviews (1:N)
- categories → products (1:N)
- products → reviews (1:N)
- products → order_items (1:N)
- orders → order_items (1:N)

## Quick Start

### SQLite (simplest to start)

```bash
cd sqlite
sqlite3 ecommerce.db
# Or run queries
sqlite3 ecommerce.db "SELECT * FROM users;"
```

### PostgreSQL

```bash
cd postgres
# Option 1: SQL script
psql -U postgres -f setup_postgres.sql

# Option 2: Python script
python3 setup_postgres_db.py
```

## Sample Queries

See `ecommerce_queries.sql` for:
- Join operations across multiple tables
- Aggregations and grouping
- Filtering and sorting
- Order management queries

## Data Domain

The database models an e-commerce system with:
- Electronics (headphones, fitness tracker, cables)
- Clothing (jeans, jacket, shoes, basketball)
- Books (Python guide, Art of War, Data Science)
- Home & Garden (plant pot, cookware set)
- Sports (yoga mat, dumbbells, basketball)

Sample customers, orders, and reviews are included to demonstrate real-world usage patterns.