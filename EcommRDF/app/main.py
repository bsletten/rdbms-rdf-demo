"""
FastAPI SPARQL endpoint application.
Provides SPARQL interface with content negotiation for RDF formats.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Optional
from pydantic import BaseModel

from database import SQLiteConnector
from sparql import RDFMapper, SPARQLServer, ECC
from rdflib import Graph


app = FastAPI(
    title="E-Commerce SPARQL Endpoint",
    description="SPARQL endpoint for e-commerce database with RDF projection",
    version="1.0.0"
)


# Initialize mapper and server
db_path = "/Users/brian/hermes/src/sqlite/ecommerce.db"
mapper = RDFMapper(SQLiteConnector(db_path))
server = SPARQLServer(mapper)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    success: bool
    data: Optional[str] = None
    error: Optional[str] = None


@app.on_event("startup")
async def load_graph():
    """Load the RDF graph on startup."""
    global mapper, server
    mapper.map_all()
    server = SPARQLServer(mapper)


@app.post("/query")
async def run_sparql(
    request: QueryRequest,
    format: str = Query(
        default="json",
        description="Output format: json, xml, json-ld, nt, turtle"
    )
):
    """
    Execute a SPARQL query.
    
    Returns results in the specified format.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")
    
    try:
        results = server.query(request.query)
        
        if 'error' in results and isinstance(results, dict):
            return QueryResponse(success=False, error=results['error'])
        
        output = server.to_format(results, format)
        
        # Set appropriate content type
        content_types = {
            'json': 'application/sparql-results+json',
            'xml': 'application/sparql-results+xml',
            'json-ld': 'application/ld+json',
            'nt': 'text/plain',
            'turtle': 'text/turtle'
        }
        
        return PlainTextResponse(
            output,
            media_type=content_types.get(format.lower(), 'text/plain')
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query.json")
async def run_sparql_json(
    request: QueryRequest,
    format: str = Query(default="json")
):
    """Execute SPARQL query and return JSON response."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")
    
    try:
        results = server.query(request.query)
        
        if 'error' in results and isinstance(results, dict):
            return {"success": False, "error": results['error']}
        
        output = server.to_format(results, format)
        
        return JSONResponse(content={
            "success": True,
            "data": output
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/graph")
async def get_graph(format: str = Query(default="turtle")):
    """
    Get the full RDF graph in the specified format.
    """
    try:
        return PlainTextResponse(
            mapper.graph.serialize(format=format),
            media_type='text/turtle'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/namespaces")
async def get_namespaces():
    """Get available namespaces and prefixes."""
    return {
        "namespaces": {
            "ecc": "https://example.com/ecommerce#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        }
    }


@app.get("/sparql")
async def sparql_endpoint(
    query: str = Query(..., description="SPARQL query string"),
    format: str = Query(default="json", description="Output format")
):
    """
    SPARQL endpoint using GET parameters.
    """
    if not query.strip():
        raise HTTPException(status_code=400, detail="Empty query")
    
    try:
        results = server.query(query)
        
        if 'error' in results and isinstance(results, dict):
            raise HTTPException(status_code=400, detail=results['error'])
        
        output = server.to_format(results, format)
        
        content_types = {
            'json': 'application/sparql-results+json',
            'xml': 'application/sparql-results+xml',
            'json-ld': 'application/ld+json',
            'nt': 'text/plain',
            'turtle': 'text/turtle'
        }
        
        return PlainTextResponse(
            output,
            media_type=content_types.get(format.lower(), 'text/plain')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "E-Commerce SPARQL Endpoint",
        "version": "1.0.0",
        "endpoints": {
            "/query": "POST - Execute SPARQL query",
            "/sparql": "GET - SPARQL endpoint with query parameter",
            "/graph": "GET - Get full RDF graph",
            "/namespaces": "GET - List available namespaces",
            "/docs": "OpenAPI/Swagger documentation"
        }
    }


@app.get("/test")
async def test_query():
    """Test endpoint with sample queries."""
    return {
        "sample_queries": [
            {
                "name": "List all users",
                "query": "SELECT ?user ?username ?email WHERE { ?user a ecc:User . ?user ecc:username ?username . ?user ecc:email ?email }"
            },
            {
                "name": "Get products by category",
                "query": "SELECT ?product ?name ?price WHERE { ?product a ecc:Product . ?product ecc:productName ?name . ?product ecc:price ?price }"
            },
            {
                "name": "Get orders with user names",
                "query": "SELECT ?order ?date ?status ?userName WHERE { ?order a ecc:Order . ?order ecc:orderDate ?date . ?order ecc:status ?status . ?order ecc:placedByUser ?user . ?user ecc:fullName ?userName }"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)