# RDBMS-to-RDF Demo: E-Commerce Database

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project demonstrates how to map a relational database to RDF using R2RML (RDF to RDB Mapping Language) and exposes it through a SPARQL endpoint with HTMX-based web interface.

## Overview

- **Schema**: E-commerce database with 6 tables (users, categories, products, orders, order_items, reviews)
- **Mapping**: W3C R2RML-compliant mappings in Turtle and XML formats
- **Endpoint**: FastAPI-based SPARQL server with content negotiation
- **Frontend**: HTMX-powered web interface for interactive querying

## Features

- ✨ R2RML mappings for both SQLite and PostgreSQL
- 🔍 SPARQL endpoint at `/sparql`
- 📊 Content negotiation (JSON, JSON-LD, Turtle, N-Triples, XML)
- 🌐 HTMX web interface for building queries
- 🎨 Bootstrap-styled HTML presentation

## Quick Start

### Prerequisites

- Python 3.8+
- pip install rdflib fastapi uvicorn pydantic

### Running the SPARQL Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
cd EcommRDF/app
uvicorn main:app --port 8000

# Server available at http://localhost:8000
```

### Running the Web Interface

```bash
# Run the web frontend
cd EcommRDF/webapp
uvicorn main:app --port 8080

# Open in browser: http://localhost:8080
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/sparql?query=...` | SPARQL endpoint (GET) |
| `/query` | SPARQL execution (POST) |
| `/graph` | Get full RDF graph |
| `/namespaces` | List available prefixes |

## Sample Queries

### List all users
```sparql
PREFIX ecc: <https://example.com/ecommerce#>

SELECT ?user ?username ?email ?fullName
WHERE {
    ?user a ecc:User ;
          ecc:username ?username ;
          ecc:email ?email ;
          ecc:fullName ?fullName .
}
```

### Get products with categories
```sparql
PREFIX ecc: <https://example.com/ecommerce#>

SELECT ?product ?name ?price ?category
WHERE {
    ?product a ecc:Product ;
             ecc:productName ?name ;
             ecc:price ?price ;
             ecc:belongsToCategory ?cat .
    ?cat ecc:name ?category .
}
ORDER BY ?price
```

## Database Schema

The database contains 6 related tables modeling an e-commerce system:

```
users → orders → order_items → products → reviews
       ↓         ↑            ↓
   reviews ←──────┘      categories
```

## RDF Vocabulary

All RDF terms are defined in the `ecc:` namespace: `https://example.com/ecommerce#`

| Class | Description |
|-------|-------------|
| `ecc:User` | Customer account |
| `ecc:Product` | Item for sale |
| `ecc:Order` | Customer order |
| `ecc:OrderItem` | Order line item |
| `ecc:Review` | Product review |
| `ecc:Category` | Product category |

## Files Structure

```
.
├── EcommRDF/           # RDF/SPARQL application
│   ├── r2rml/         # R2RML mappings
│   ├── app/           # FastAPI server
│   └── webapp/        # HTMX frontend
│
├── sqlite/            # SQLite database
│   └── ecommerce.db
│
├── postgres/          # PostgreSQL setup
│   ├── setup_postgres.sql
│   └── setup_postgres_db.py
│
└── README.md          # This file
```

## License

MIT License - see [LICENSE](LICENSE) file for details.