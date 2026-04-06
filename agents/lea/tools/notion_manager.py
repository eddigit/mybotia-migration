
import requests
import json
import os

NOTION_API_KEY = "<NOTION_API_TOKEN>"
NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1/"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_API_VERSION,
    "Content-Type": "application/json"
}

def create_notion_page(parent_info, title, properties=None, children=None):
    url = f"{NOTION_BASE_URL}pages"
    payload = {
        "parent": parent_info,
        "properties": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    }
    if properties: # Additional properties for new pages
        payload["properties"].update(properties)
    if children: # Content for the page
        payload["children"] = children

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def create_notion_database(parent_page_id, title, properties):
    url = f"{NOTION_BASE_URL}databases"
    payload = {
        "parent": {"page_id": parent_page_id},
        "title": [
            {
                "text": {
                    "content": title
                }
            }
        ],
        "properties": properties
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def add_item_to_database(database_id, properties):
    url = f"{NOTION_BASE_URL}pages"
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    # Exemple d'utilisation (à adapter pour notre cas réel)
    # Créez une page parente manuellement dans Notion et remplacez son ID ici
    # parent_id = "<ID_DE_LA_PAGE_PARENTE_NOTION>"

    # Exemple de création d'une page
    # new_page = create_notion_page(parent_id, "Ma Nouvelle Page")
    # print(f"Page créée: {new_page['url']}")

    # Exemple de création d'une base de données
    # db_properties = {
    #     "Name": {"title": {}},
    #     "Description": {"rich_text": {}},
    #     "Statut": {"select": {"options": [{"name": "En cours"}, {"name": "Terminé"}]}}
    # }
    # new_db = create_notion_database(parent_id, "Ma Nouvelle Base", db_properties)
    # print(f"Base de données créée: {new_db['url']}")

    # Exemple d'ajout d'un élément à la base de données
    # db_item_properties = {
    #     "Name": {"title": [{"text": {"content": "Tâche 1"}}]}, 
    #     "Description": {"rich_text": [{"text": {"content": "Description de la tâche 1."}}]}, 
    #     "Statut": {"select": {"name": "En cours"}}}
    # new_item = add_item_to_database(new_db['id'], db_item_properties)
    # print(f"Élément ajouté: {new_item['url']}")

    print("Script notion_manager.py créé. Il est prêt à être importé et utilisé.")
