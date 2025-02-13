import markdown
import json

def generate(docs):
    md = '# FastAPI Documentation\n\n'
    for route in docs:
        md += f"## `{route['path']}`\n"
        md += f"**Methods** {', '.join(route['methods'])}\n\n"
        md += f"**Description** {route['description'] or 'No Description'}\n\n"
    return md

