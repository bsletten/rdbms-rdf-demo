# RDBMS-to-RDF Demo - Session Notes

## Key Lessons Learned

### 1. Database Path Resolution
**Problem**: Hardcoded absolute paths like `/Users/brian/hermes/src/sqlite/ecommerce.db` don't work when code is run from different directories or machines.

**Solution**: Use relative paths based on script location:
```python
from pathlib import Path
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent.parent / "sqlite" / "ecommerce.db"
```

### 2. Cross-Directory Module Imports
**Problem**: `webapp/main.py` tried to import from `database` but couldn't find it.

**Solution**: Add parent directories to `sys.path`:
```python
import sys
from pathlib import Path
app_dir = Path(__file__).parent.parent / "app"
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))
```

### 3. GitHub Repository Structure
- Put `LICENSE` at repository root (GitHub detects automatically)
- Database file separate from code (SQLite is a file)
- Include `main.py` and `requirements.txt`
- Use relative paths for portability

### 4. Error Troubleshooting Order
1. Check dependencies installed
2. Check path exists
3. Check import correct
4. Check file in git

### 5. HTMX Web Interface Notes
- Requires `jinja2` in requirements.txt
- Templates directory must match FastAPI expectations

## Working Directory Structure
```
repo/
├── EcommRDF/app/
├── EcommRDF/r2rml/
├── EcommRDF/webapp/
├── sqlite/ecommerce.db
└── postgres/
```