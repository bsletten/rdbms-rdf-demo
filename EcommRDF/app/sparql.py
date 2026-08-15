"""
SPARQL query handling and translation.
Supports content negotiation for different RDF formats.
"""

from typing import Dict, List, Optional, Any
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, FOAF
import json


# Define namespace
ECC = Namespace("https://example.com/ecommerce#")


class RDFMapper:
    """Maps relational data to RDF using R2RML rules."""
    
    def __init__(self, db_connector):
        self.db = db_connector
        self.graph = Graph()
        self.graph.bind("ecc", ECC)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("xsd", XSD)
    
    def map_users(self) -> None:
        """Map users table to RDF."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        
        for row in cursor.fetchall():
            user_uri = URIRef(f"https://example.com/user/{row[0]}")
            
            self.graph.add((user_uri, RDF.type, ECC.User))
            self.graph.add((user_uri, ECC.username, Literal(row[1])))
            self.graph.add((user_uri, ECC.email, Literal(row[2])))
            self.graph.add((user_uri, ECC.fullName, Literal(row[3])))
            self.graph.add((user_uri, ECC.createdAt, Literal(row[4], datatype=XSD.date)))
        
        self.db.close()
    
    def map_categories(self) -> None:
        """Map categories table to RDF."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        
        for row in cursor.fetchall():
            cat_uri = URIRef(f"https://example.com/category/{row[0]}")
            
            self.graph.add((cat_uri, RDF.type, ECC.Category))
            self.graph.add((cat_uri, ECC.name, Literal(row[1])))
            if row[2]:
                self.graph.add((cat_uri, ECC.description, Literal(row[2])))
        
        self.db.close()
    
    def map_products(self) -> None:
        """Map products table to RDF."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        
        for row in cursor.fetchall():
            prod_uri = URIRef(f"https://example.com/product/{row[0]}")
            
            self.graph.add((prod_uri, RDF.type, ECC.Product))
            self.graph.add((prod_uri, ECC.productName, Literal(row[1])))
            if row[2]:
                self.graph.add((prod_uri, ECC.productDescription, Literal(row[2])))
            self.graph.add((prod_uri, ECC.price, Literal(row[3], datatype=XSD.decimal)))
            self.graph.add((prod_uri, ECC.stockQuantity, Literal(row[5], datatype=XSD.integer)))
            self.graph.add((prod_uri, ECC.averageRating, Literal(row[6], datatype=XSD.decimal)))
            
            # Link to category
            cat_uri = URIRef(f"https://example.com/category/{row[4]}")
            self.graph.add((prod_uri, ECC.belongsToCategory, cat_uri))
        
        self.db.close()
    
    def map_orders(self) -> None:
        """Map orders table to RDF."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        
        for row in cursor.fetchall():
            order_uri = URIRef(f"https://example.com/order/{row[0]}")
            
            self.graph.add((order_uri, RDF.type, ECC.Order))
            self.graph.add((order_uri, ECC.orderDate, Literal(row[2], datatype=XSD.date)))
            if row[3]:
                self.graph.add((order_uri, ECC.shipDate, Literal(row[3], datatype=XSD.date)))
            self.graph.add((order_uri, ECC.status, Literal(row[4])))
            self.graph.add((order_uri, ECC.totalAmount, Literal(row[5], datatype=XSD.decimal)))
            
            # Link to user
            user_uri = URIRef(f"https://example.com/user/{row[1]}")
            self.graph.add((order_uri, ECC.placedByUser, user_uri))
        
        self.db.close()
    
    def map_order_items(self) -> None:
        """Map order_items table to RDF."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM order_items")
        
        for row in cursor.fetchall():
            item_uri = URIRef(f"https://example.com/orderItem/{row[0]}")
            
            self.graph.add((item_uri, RDF.type, ECC.OrderItem))
            self.graph.add((item_uri, ECC.itemNumber, Literal(row[2], datatype=XSD.integer)))
            self.graph.add((item_uri, ECC.quantity, Literal(row[4], datatype=XSD.integer)))
            self.graph.add((item_uri, ECC.unitPrice, Literal(row[5], datatype=XSD.decimal)))
            
            # Link to order
            order_uri = URIRef(f"https://example.com/order/{row[1]}")
            self.graph.add((item_uri, ECC.partOfOrder, order_uri))
            
            # Link to product
            prod_uri = URIRef(f"https://example.com/product/{row[3]}")
            self.graph.add((item_uri, ECC.referencesProduct, prod_uri))
        
        self.db.close()
    
    def map_reviews(self) -> None:
        """Map reviews table to RDF."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reviews")
        
        for row in cursor.fetchall():
            review_uri = URIRef(f"https://example.com/review/{row[0]}")
            
            self.graph.add((review_uri, RDF.type, ECC.Review))
            self.graph.add((review_uri, ECC.rating, Literal(row[3], datatype=XSD.integer)))
            if row[4]:
                self.graph.add((review_uri, ECC.comment, Literal(row[4])))
            
            # Link to user
            user_uri = URIRef(f"https://example.com/user/{row[2]}")
            self.graph.add((review_uri, ECC.reviewedBy, user_uri))
            
            # Link to product
            prod_uri = URIRef(f"https://example.com/product/{row[1]}")
            self.graph.add((review_uri, ECC.reviewsProduct, prod_uri))
        
        self.db.close()
    
    def map_all(self) -> Graph:
        """Map all tables to RDF."""
        self.map_users()
        self.map_categories()
        self.map_products()
        self.map_orders()
        self.map_order_items()
        self.map_reviews()
        return self.graph
    
    def clear(self) -> None:
        """Clear the graph."""
        self.graph = Graph()
        self.graph.bind("ecc", ECC)


class SPARQLServer:
    """Simple SPARQL endpoint server."""
    
    def __init__(self, rdf_mapper: RDFMapper):
        self.mapper = rdf_mapper
        self.graph = rdf_mapper.graph
    
    def query(self, sparql_query: str) -> Any:
        """Execute a SPARQL query."""
        try:
            results = self.graph.query(sparql_query)
            return results
        except Exception as e:
            return {"error": str(e)}
    
    def to_format(self, results, format_type: str = "json") -> str:
        """Convert results to specified format."""
        format_type = format_type.lower()
        
        if format_type == "json":
            return self._to_json(results)
        elif format_type == "xml":
            return self._to_xml(results)
        elif format_type == "json-ld":
            return self._to_jsonld(results)
        elif format_type == "nt":
            return self._to_ntriples(results)
        else:
            return self._to_turtle(results)
    
    def _to_json(self, results) -> str:
        """Convert to JSON format."""
        bindings = []
        for row in results:
            binding = {}
            for i, var in enumerate(results.vars):
                val = row[i]
                if val:
                    binding[str(var)] = {
                        "type": "uri" if isinstance(val, URIRef) else "literal",
                        "value": str(val)
                    }
            bindings.append(binding)
        
        return json.dumps({
            "head": {"vars": [str(v) for v in results.vars]},
            "results": {"bindings": bindings}
        }, indent=2)
    
    def _to_xml(self, results) -> str:
        """Convert to XML format."""
        return results.serialize(format="xml")
    
    def _to_jsonld(self, results) -> str:
        """Convert to JSON-LD format."""
        # For JSON-LD, we return the graph serialized with context
        return self.graph.serialize(format="json-ld", indent=2)
    
    def _to_turtle(self, results) -> str:
        """Convert to Turtle format."""
        return self.graph.serialize(format="turtle")
    
    def _to_ntriples(self, results) -> str:
        """Convert to N-Triples format."""
        return self.graph.serialize(format="nt")