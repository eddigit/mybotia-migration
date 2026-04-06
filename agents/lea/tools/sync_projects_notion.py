#!/usr/bin/env python3
"""
Sync automatique Vercel/GitHub → Notion PROJETS
- Récupère tous les projets Vercel
- Récupère les URLs de production et repos GitHub
- Met à jour ou crée les projets dans Notion
- Génère les screenshots auto

Usage: python3 sync_projects_notion.py
"""

import requests
from datetime import datetime

# === CONFIG ===
NOTION_TOKEN = "<NOTION_API_TOKEN>"
VERCEL_TOKEN = "vcp_4JDvFowWX8kc99YXSUMTp55DoRYgWYlN2kfJbWNib7lZugFenR0hCIro"
GITHUB_TOKEN = "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"
PROJETS_DB_ID = "304ddac9-bdfc-8155-bb08-f8d2caa1439a"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_vercel_projects():
    """Récupère tous les projets Vercel avec leurs infos"""
    url = "https://api.vercel.com/v9/projects?limit=100"
    headers = {"Authorization": f"Bearer {VERCEL_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    projects = []
    for p in data.get('projects', []):
        # Récupérer l'URL de production
        prod_url = None
        aliases = p.get('alias', [])
        if aliases:
            prod_url = f"https://{aliases[0]['domain']}" if isinstance(aliases[0], dict) else f"https://{aliases[0]}"
        
        # URL par défaut Vercel
        vercel_url = f"https://{p['name']}.vercel.app"
        
        # Repo GitHub lié
        github_repo = None
        link = p.get('link', {})
        if link and link.get('type') == 'github':
            org = link.get('org') or link.get('repoOwner', '')
            repo = link.get('repo') or link.get('repoSlug', '')
            if org and repo:
                github_repo = f"https://github.com/{org}/{repo}"
        
        projects.append({
            'name': p['name'],
            'id': p['id'],
            'prod_url': prod_url or vercel_url,
            'vercel_url': f"https://vercel.com/{p.get('accountId', 'gilles-korzec-projects')}/{p['name']}",
            'github_repo': github_repo,
            'updated': p.get('updatedAt'),
            'framework': p.get('framework', 'unknown')
        })
    
    return projects

def get_notion_projects():
    """Récupère les projets existants dans Notion"""
    url = f"https://api.notion.com/v1/databases/{PROJETS_DB_ID}/query"
    response = requests.post(url, headers=NOTION_HEADERS, json={})
    data = response.json()
    
    projects = {}
    for page in data.get('results', []):
        props = page.get('properties', {})
        nom_prop = props.get('Nom', {}).get('title', [])
        nom = nom_prop[0]['plain_text'].lower() if nom_prop else ''
        projects[nom] = page['id']
    
    return projects

def get_screenshot_url(site_url):
    """Génère l'URL du screenshot via thum.io"""
    if not site_url:
        return None
    return f"https://image.thum.io/get/width/1200/crop/630/{site_url}"

def update_notion_project(page_id, vercel_project):
    """Met à jour un projet Notion existant"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    gouvernance = f"🔗 Vercel: {vercel_project['vercel_url']}"
    if vercel_project['github_repo']:
        gouvernance += f"\n📂 GitHub: {vercel_project['github_repo']}"
    gouvernance += f"\n🌐 URL: {vercel_project['prod_url']}"
    gouvernance += f"\n⚙️ Framework: {vercel_project['framework']}"
    
    data = {
        "properties": {
            "URL Site": {"url": vercel_project['prod_url']},
            "Gouvernance": {"rich_text": [{"text": {"content": gouvernance}}]}
        },
        "cover": {
            "type": "external",
            "external": {"url": get_screenshot_url(vercel_project['prod_url'])}
        }
    }
    
    response = requests.patch(url, headers=NOTION_HEADERS, json=data)
    return response.status_code == 200

def create_notion_project(vercel_project):
    """Crée un nouveau projet dans Notion"""
    url = "https://api.notion.com/v1/pages"
    
    gouvernance = f"🔗 Vercel: {vercel_project['vercel_url']}"
    if vercel_project['github_repo']:
        gouvernance += f"\n📂 GitHub: {vercel_project['github_repo']}"
    gouvernance += f"\n🌐 URL: {vercel_project['prod_url']}"
    gouvernance += f"\n⚙️ Framework: {vercel_project['framework']}"
    
    data = {
        "parent": {"database_id": PROJETS_DB_ID},
        "properties": {
            "Nom": {"title": [{"text": {"content": vercel_project['name']}}]},
            "URL Site": {"url": vercel_project['prod_url']},
            "Status": {"select": {"name": "Actif"}},
            "Gouvernance": {"rich_text": [{"text": {"content": gouvernance}}]}
        },
        "cover": {
            "type": "external",
            "external": {"url": get_screenshot_url(vercel_project['prod_url'])}
        }
    }
    
    response = requests.post(url, headers=NOTION_HEADERS, json=data)
    return response.status_code == 200

def main():
    print("🔄 SYNC Vercel → Notion")
    print("=" * 50)
    
    print("\n📦 Récupération projets Vercel...")
    vercel_projects = get_vercel_projects()
    print(f"   {len(vercel_projects)} projets trouvés")
    
    print("\n📋 Récupération projets Notion...")
    notion_projects = get_notion_projects()
    print(f"   {len(notion_projects)} projets existants")
    
    created = 0
    updated = 0
    
    print("\n🔄 Synchronisation...")
    for vp in vercel_projects:
        name_lower = vp['name'].lower()
        
        # Chercher si le projet existe déjà (par nom approchant)
        existing_id = None
        for notion_name, notion_id in notion_projects.items():
            if name_lower in notion_name or notion_name in name_lower:
                existing_id = notion_id
                break
        
        if existing_id:
            print(f"   📝 {vp['name']}: mise à jour...")
            if update_notion_project(existing_id, vp):
                updated += 1
                print(f"      ✅ OK")
            else:
                print(f"      ❌ Erreur")
        else:
            print(f"   ➕ {vp['name']}: création...")
            if create_notion_project(vp):
                created += 1
                print(f"      ✅ OK")
            else:
                print(f"      ❌ Erreur")
    
    print("\n" + "=" * 50)
    print(f"✅ Terminé: {created} créés, {updated} mis à jour")

if __name__ == "__main__":
    main()
