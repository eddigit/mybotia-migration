#!/usr/bin/env python3
"""
Créer une page dans Notion via l'API
"""
import requests
import json
import sys

NOTION_API_KEY = "<NOTION_API_TOKEN>"
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

def search_databases():
    """Recherche les bases de données disponibles"""
    response = requests.post(
        "https://api.notion.com/v1/search",
        headers=headers,
        json={"filter": {"property": "object", "value": "database"}}
    )
    return response.json()

def search_pages(query=""):
    """Recherche les pages disponibles"""
    response = requests.post(
        "https://api.notion.com/v1/search",
        headers=headers,
        json={"query": query, "filter": {"property": "object", "value": "page"}}
    )
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "databases":
        result = search_databases()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        result = search_pages(sys.argv[1] if len(sys.argv) > 1 else "")
        print(json.dumps(result, indent=2, ensure_ascii=False))
