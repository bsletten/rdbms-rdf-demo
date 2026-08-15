"""
Web frontend for SPARQL endpoint using HTMX.
Provides an interactive query interface.
"""

import sys
import os
from pathlib import Path

# Debug: print paths
_webapp_dir = Path(__file__).parent.resolve()
_base_dir = _webapp_dir.parent
_app_dir = _base_dir / "app"
_db_path = _webapp_dir.parent.parent / "sqlite" / "ecommerce.db"

print(f"DEBUG: __file__ = {__file__}")
print(f"DEBUG: _webapp_dir = {_webapp_dir}")
print(f"DEBUG: templates dir = {_webapp_dir / 'templates'}")
print(f"DEBUG: templates exists = {(_webapp_dir / 'templates').exists()}")

# Add app directory to path for imports
if str(_app_dir) not in sys.path:
    sys.path.insert(0, str(_app_dir))

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import SQLiteConnector
from sparql import RDFMapper

app = FastAPI(title="E-Commerce RDF Web Interface")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(_webapp_dir / "static")), name="static")
templates = Jinja2Templates(directory=str(_webapp_dir / "templates"))

# Initialize mapper
mapper = None


class QueryRequest(BaseModel):
    query: str
    format: str = "json"


@app.on_event("startup")
async def load_graph():
    """Load the RDF graph on startup."""
    global mapper
    mapper = RDFMapper(SQLiteConnector(str(_db_path)))
    mapper.map_all()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/query")
async def query_endpoint(
    request: Request,
    query: str = Form(...),
    format: str = Form("json")
):
    """Handle SPARQL query requests."""
    global mapper
    
    if not mapper:
        return {"error": "Graph not loaded"}
    
    try:
        results = mapper.query(query)
        
        if 'error' in results and isinstance(results, dict):
            return {"error": results['error']}
        
        output = mapper.to_format(results, format)
        
        content_type = {
            'json': 'application/sparql-results+json',
            'json-ld': 'application/ld+json',
            'turtle': 'text/turtle',
            'xml': 'application/sparql-results+xml'
        }.get(format, 'text/plain')
        
        return HTMLResponse(content=output, media_type=content_type)
    
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/query")
async def api_query(query: str, format: str = "json"):
    """API endpoint for programmatic access."""
    global mapper
    
    if not mapper:
        return {"error": "Graph not loaded"}
    
    try:
        results = mapper.query(query)
        
        if 'error' in results and isinstance(results, dict):
            return {"error": results['error']}
        
        output = mapper.to_format(results, format)
        
        content_type = {
            'json': 'application/sparql-results+json',
            'json-ld': 'application/ld+json',
            'turtle': 'text/turtle',
            'xml': 'application/sparql-results+xml'
        }.get(format, 'application/json')
        
        return HTMLResponse(content=output, media_type=content_type)
    
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/sparql")
async def sparql_endpoint(query: str, format: str = "json"):
    """SPARQL endpoint URL."""
    return await api_query(query, format)


@app.get("/graph")
async def get_graph(format: str = "turtle"):
    """Get the full RDF graph."""
    global mapper
    if not mapper:
        return {"error": "Graph not loaded"}
    return PlainTextResponse(mapper.graph.serialize(format=format))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)