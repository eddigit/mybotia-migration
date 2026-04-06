#!/usr/bin/env python3
"""
Auto-génère les covers Notion à partir des URLs de projets.
Utilise thum.io pour les screenshots (gratuit, pas de clé API).

Usage: python3 notion_screenshot_covers.py
"""

import requests
import sys

NOTION_TOKEN = "<NOTION_API_TOKEN>"
PROJETS_DB_ID = "304ddac9-bdfc-8155-bb08-f8d2caa1439a"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_screenshot_url(site_url):
    """Génère l'URL du screenshot via thum.io"""
    if not site_url:
        return None
    # Nettoyer l'URL
    site_url = site_url.strip()
    if not site_url.startswith('http'):
        site_url = f"https://{site_url}"
    return f"https://image.thum.io/get/width/1200/crop/630/{site_url}"

def get_projects_with_urls():
    """Récupère tous les projets avec une URL Site"""
    url = f"https://api.notion.com/v1/databases/{PROJETS_DB_ID}/query"
    response = requests.post(url, headers=HEADERS, json={})
    data = response.json()
    
    projects = []
    for page in data.get('results', []):
        page_id = page['id']
        props = page.get('properties', {})
        
        # Récupérer le nom
        nom_prop = props.get('Nom', {}).get('title', [])
        nom = nom_prop[0]['plain_text'] if nom_prop else 'Sans nom'
        
        # Récupérer l'URL Site
        url_site = props.get('URL Site', {}).get('url')
        
        # Récupérer la cover actuelle
        cover = page.get('cover')
        
        projects.append({
            'id': page_id,
            'nom': nom,
            'url_site': url_site,
            'has_cover': cover is not None
        })
    
    return projects

def update_cover(page_id, screenshot_url):
    """Met à jour la cover d'une page Notion"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = {
        "cover": {
            "type": "external",
            "external": {
                "url": screenshot_url
            }
        }
    }
    response = requests.patch(url, headers=HEADERS, json=data)
    return response.status_code == 200

def main():
    print("🔍 Récupération des projets Notion...")
    projects = get_projects_with_urls()
    
    updated = 0
    skipped = 0
    
    for p in projects:
        if p['url_site']:
            screenshot_url = get_screenshot_url(p['url_site'])
            print(f"📸 {p['nom']}: {p['url_site']}")
            
            if update_cover(p['id'], screenshot_url):
                print(f"   ✅ Cover mise à jour")
                updated += 1
            else:
                print(f"   ❌ Erreur mise à jour")
        else:
            print(f"⏭️  {p['nom']}: pas d'URL Site")
            skipped += 1
    
    print(f"\n✅ {updated} covers mises à jour, {skipped} projets sans URL")

if __name__ == "__main__":
    main()
