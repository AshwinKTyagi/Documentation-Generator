from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.routing import APIRoute
import markdown2

import markdown, json
from generate_markdown import generate

### ROUTES

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI Docs Generator"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.get("/generate-docs")
def generate_docs():
    """Dynamically regenerates API documentation"""
    docs = extract_routes()
    md_output = generate(docs)

    with open("API_DOCUMENTATION.md", "w") as f:
        f.write(md_output)

    html_output = markdown2.markdown(md_output)
    return HTMLResponse(content=html_output)

### HELPERS

def extract_routes():
    routes_info = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes_info.append({
                "path": route.path,
                "methods": list(route.methods),
                "description": route.endpoint.__doc__,
                "name": route.name
            })

    return routes_info

def generate(docs):
    md = '# FastAPI Documentation\n\n'
    for route in docs:
        md += f"## `{route['path']}`\n"
        md += f"**Methods** {', '.join(route['methods'])}\n\n"
        md += f"**Description** {route['description'] or 'No Description'}\n\n"
    return md
