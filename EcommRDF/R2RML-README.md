# RDF E-Commerce Database Project
# R2RML mapping and SPARQL interface

e-commerce-rdf/
├── r2rml/                    # R2RML mappings
│   ├── r2rml-mapping.ttl    # R2RML mapping in Turtle
│   ├── r2rml-mapping.xml    # R2RML mapping in XML
│   └── terms.ttl            # Vocabulary terms
│
├── app/                     # Python app for SPARQL endpoint
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connectors
│   ├── sparql.py            # SPARQL query handling
│   └── models.py            # RDF models
│
├── webapp/                  # HTMX-based web frontend
│   ├── templates/           # Jinja2 templates
│   ├── static/              # CSS/JS
│   └── main.py              # Web application
│
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation