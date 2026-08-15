"""
Web frontend for SPARQL endpoint using HTMX.
Provides an interactive query interface.
"""

import sys
import os
from pathlib import Path

# Add the app directory to the path for imports
app_dir = Path(__file__).parent.parent / "app"
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import SQLiteConnector
from sparql import RDFMapper

app = FastAPI(title="E-Commerce RDF Web Interface")

# Get paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
webapp_dir = os.path.join(base_dir, "webapp")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=os.path.join(webapp_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(webapp_dir, "templates"))

# Initialize mapper - resolve database relative to webapp location
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent.parent / "sqlite" / "ecommerce.db"
mapper = None


class QueryRequest(BaseModel):
    query: str
    format: str = "json"


@app.on_event("startup")
async def load_graph():
    """Load the RDF graph on startup."""
    global mapper
    mapper = RDFMapper(SQLiteConnector(str(DB_PATH)))
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
        
        # Get the output in the requested format
        output = mapper.to_format(results, format)
        
        # Return as HTML response for browser rendering
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)