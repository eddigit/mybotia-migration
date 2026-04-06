#!/usr/bin/env python3
"""
notion_tool.py - Outil Notion pour Max (VL Medical)
Commandes : check, search, databases, query, read, create, update, add_content
Version : 1.0.0
"""

import sys
import json
import argparse
import requests
from datetime import datetime

NOTION_TOKEN = "<NOTION_API_TOKEN>"
NOTION_VERSION = "2022-06-28"
NOTION_BASE = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

def api_request(method, endpoint, payload=None):
    url = f"{NOTION_BASE}/{endpoint}"
    try:
        if method == "GET":
            resp = requests.get(url, headers=HEADERS, timeout=15)
        elif method == "POST":
            resp = requests.post(url, headers=HEADERS, json=payload or {}, timeout=15)
        elif method == "PATCH":
            resp = requests.patch(url, headers=HEADERS, json=payload or {}, timeout=15)
        else:
            return {"error": f"Unknown HTTP method: {method}"}
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"HTTP {resp.status_code}", "message": resp.json().get("message", resp.text[:500])}
    except requests.exceptions.Timeout:
        return {"error": "Timeout (15s)"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot reach Notion API"}
    except Exception as e:
        return {"error": str(e)}

def format_rich_text(rich_text_array):
    if not rich_text_array:
        return ""
    return "".join(item.get("plain_text", "") for item in rich_text_array)

def format_property_value(prop):
    ptype = prop.get("type", "")
    if ptype == "title":
        return format_rich_text(prop.get("title", []))
    elif ptype == "rich_text":
        return format_rich_text(prop.get("rich_text", []))
    elif ptype == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    elif ptype == "multi_select":
        return ", ".join(s.get("name", "") for s in prop.get("multi_select", []))
    elif ptype == "date":
        d = prop.get("date")
        if not d: return ""
        start = d.get("start", "")
        end = d.get("end", "")
        return f"{start} -> {end}" if end else start
    elif ptype == "checkbox":
        return "[x]" if prop.get("checkbox") else "[ ]"
    elif ptype == "number":
        val = prop.get("number")
        return str(val) if val is not None else ""
    elif ptype == "url":
        return prop.get("url", "")
    elif ptype == "email":
        return prop.get("email", "")
    elif ptype == "phone_number":
        return prop.get("phone_number", "")
    elif ptype == "status":
        st = prop.get("status")
        return st.get("name", "") if st else ""
    elif ptype == "relation":
        return ", ".join(r.get("id", "") for r in prop.get("relation", []))
    elif ptype == "formula":
        formula = prop.get("formula", {})
        ftype = formula.get("type", "")
        return str(formula.get(ftype, ""))
    elif ptype == "rollup":
        rollup = prop.get("rollup", {})
        rtype = rollup.get("type", "")
        return str(rollup.get(rtype, ""))
    elif ptype == "people":
        return ", ".join(p.get("name", p.get("id", "")) for p in prop.get("people", []))
    elif ptype == "created_time":
        return prop.get("created_time", "")
    elif ptype == "last_edited_time":
        return prop.get("last_edited_time", "")
    elif ptype == "created_by":
        return prop.get("created_by", {}).get("name", "")
    elif ptype == "last_edited_by":
        return prop.get("last_edited_by", {}).get("name", "")
    elif ptype == "files":
        return ", ".join(f.get("name", "") for f in prop.get("files", []))
    else:
        return f"[{ptype}]"

def format_page_row(page):
    props = page.get("properties", {})
    row = {"id": page.get("id", ""), "url": page.get("url", "")}
    for name, prop in props.items():
        row[name] = format_property_value(prop)
    return row

def format_block(block):
    btype = block.get("type", "")
    content = block.get(btype, {})
    if "rich_text" in content:
        text = format_rich_text(content["rich_text"])
    elif "text" in content:
        text = format_rich_text(content["text"])
    elif btype == "child_database":
        text = "[DB: " + content.get("title", "Sans titre") + "]"
    elif btype == "child_page":
        text = "[Page: " + content.get("title", "Sans titre") + "]"
    elif btype == "image":
        src = content.get("file", content.get("external", {}))
        text = "[Image: " + src.get("url", "?") + "]"
    elif btype == "divider":
        text = "---"
    else:
        text = f"[{btype}]"
    prefix = ""
    if btype == "heading_1": prefix = "# "
    elif btype == "heading_2": prefix = "## "
    elif btype == "heading_3": prefix = "### "
    elif btype == "bulleted_list_item": prefix = "- "
    elif btype == "numbered_list_item": prefix = "1. "
    elif btype == "to_do":
        checked = content.get("checked", False)
        prefix = "[x] " if checked else "[ ] "
    elif btype == "toggle": prefix = "> "
    elif btype == "quote": prefix = "> "
    elif btype == "callout":
        icon = block.get("callout", {}).get("icon", {})
        emoji = icon.get("emoji", "!") if icon else "!"
        prefix = f"{emoji} "
    elif btype == "code":
        lang = content.get("language", "")
        return "```" + lang + "\n" + text + "\n```"
    return f"{prefix}{text}"

def cmd_check():
    print("Test de connexion Notion...")
    result = api_request("GET", "users/me")
    if "error" in result:
        print("ERREUR : " + result["error"])
        if "message" in result: print("   Detail : " + result["message"])
        return 1
    bot = result.get("bot", {})
    workspace = bot.get("workspace_name", "?")
    print("Connexion OK")
    print("   Bot : " + result.get("name", "?"))
    print("   Type : " + result.get("type", "?"))
    print("   Workspace : " + workspace)
    search_result = api_request("POST", "search", {"page_size": 1})
    if "error" not in search_result:
        total = len(search_result.get("results", []))
        msg = "au moins 1 page accessible" if total > 0 else "aucune page accessible"
        print("   Acces : " + msg)
    else:
        print("   Impossible de verifier acces : " + search_result["error"])
    return 0

def cmd_search(query):
    payload = {"query": query, "page_size": 20}
    result = api_request("POST", "search", payload)
    if "error" in result:
        print("ERREUR : " + result["error"])
        return 1
    items = result.get("results", [])
    if not items:
        print("Aucun resultat pour : " + query)
        return 0
    print(str(len(items)) + " resultat(s) pour : " + query + "\n")
    for item in items:
        obj_type = item.get("object", "?")
        item_id = item.get("id", "?")
        url = item.get("url", "")
        if obj_type == "page":
            props = item.get("properties", {})
            title = ""
            for pname, pval in props.items():
                if pval.get("type") == "title":
                    title = format_rich_text(pval.get("title", []))
                    break
            title = title or "(Sans titre)"
            parent = item.get("parent", {})
            parent_type = parent.get("type", "")
            print("  PAGE : " + title)
            print("     ID : " + item_id)
            print("     Parent : " + parent_type)
            if url: print("     URL : " + url)
        elif obj_type == "database":
            title_arr = item.get("title", [])
            title = format_rich_text(title_arr) or "(Sans titre)"
            db_props = item.get("properties", {})
            columns = list(db_props.keys())
            print("  BASE : " + title)
            print("     ID : " + item_id)
            print("     Colonnes : " + ", ".join(columns[:10]))
            if len(columns) > 10: print("     ... et " + str(len(columns) - 10) + " de plus")
            if url: print("     URL : " + url)
        print()
    return 0

def cmd_databases():
    payload = {"filter": {"property": "object", "value": "database"}, "page_size": 100}
    result = api_request("POST", "search", payload)
    if "error" in result:
        print("ERREUR : " + result["error"])
        return 1
    dbs = result.get("results", [])
    if not dbs:
        print("Aucune base de donnees accessible.")
        print("Verifiez que les bases sont partagees avec l integration Notion.")
        return 0
    print(str(len(dbs)) + " base(s) de donnees accessible(s) :\n")
    for db in dbs:
        title_arr = db.get("title", [])
        title = format_rich_text(title_arr) or "(Sans titre)"
        db_id = db.get("id", "?")
        db_props = db.get("properties", {})
        columns = list(db_props.keys())
        print("  " + title)
        print("     ID : " + db_id)
        print("     Colonnes : " + ", ".join(columns))
        print("     URL : " + db.get("url", "?"))
        print()
    return 0

def cmd_query(database_id, filter_json=None, sort_json=None, page_size=50):
    payload = {"page_size": min(page_size, 100)}
    if filter_json:
        try:
            payload["filter"] = json.loads(filter_json)
        except json.JSONDecodeError as e:
            print("Filtre JSON invalide : " + str(e))
            return 1
    if sort_json:
        try:
            payload["sorts"] = json.loads(sort_json)
        except json.JSONDecodeError as e:
            print("Tri JSON invalide : " + str(e))
            return 1
    result = api_request("POST", f"databases/{database_id}/query", payload)
    if "error" in result:
        print("ERREUR : " + result["error"])
        if "message" in result: print("   Detail : " + result["message"])
        return 1
    pages = result.get("results", [])
    if not pages:
        print("Aucun resultat dans cette base.")
        return 0
    print(str(len(pages)) + " entree(s) :\n")
    for page in pages:
        row = format_page_row(page)
        page_id = row.pop("id", "?")
        url = row.pop("url", "")
        title = ""
        for key, val in row.items():
            if val and not title:
                title = val
                break
        title = title or "(Sans titre)"
        print("  " + title)
        print("     ID : " + page_id)
        for key, val in row.items():
            if val: print("     " + key + " : " + str(val))
        if url: print("     URL : " + url)
        print()
    has_more = result.get("has_more", False)
    if has_more:
        cursor = result.get("next_cursor", "")
        print("  Il y a plus de resultats (next_cursor: " + cursor + ")")
    return 0

def cmd_read(page_id):
    page_result = api_request("GET", f"pages/{page_id}")
    if "error" in page_result:
        print("ERREUR page : " + page_result["error"])
        return 1
    props = page_result.get("properties", {})
    url = page_result.get("url", "")
    title = ""
    for pname, pval in props.items():
        if pval.get("type") == "title":
            title = format_rich_text(pval.get("title", []))
            break
    title = title or "(Sans titre)"
    print("PAGE: " + title)
    print("   ID : " + page_id)
    if url: print("   URL : " + url)
    print("   Cree : " + page_result.get("created_time", "?"))
    print("   Modifie : " + page_result.get("last_edited_time", "?"))
    print()
    print("-- Proprietes --")
    for pname, pval in props.items():
        val = format_property_value(pval)
        if val: print("  " + pname + " : " + str(val))
    print()
    blocks_result = api_request("GET", f"blocks/{page_id}/children?page_size=100")
    if "error" in blocks_result:
        print("Impossible de lire le contenu : " + blocks_result["error"])
        return 0
    blocks = blocks_result.get("results", [])
    if blocks:
        print("-- Contenu --")
        for block in blocks:
            text = format_block(block)
            if text: print("  " + text)
    else:
        print("(Page vide -- aucun contenu)")
    return 0

def cmd_create(database_id, title, extra_props_json=None):
    properties = {"Name": {"title": [{"text": {"content": title}}]}}
    if extra_props_json:
        try:
            extra = json.loads(extra_props_json)
            properties.update(extra)
        except json.JSONDecodeError as e:
            print("Props JSON invalides : " + str(e))
            return 1
    payload = {"parent": {"database_id": database_id}, "properties": properties}
    result = api_request("POST", "pages", payload)
    if "error" in result:
        print("ERREUR : " + result["error"])
        if "message" in result: print("   Detail : " + result["message"])
        return 1
    print("Entree creee")
    print("   Titre : " + title)
    print("   ID : " + result.get("id", "?"))
    print("   URL : " + result.get("url", "?"))
    return 0

def cmd_update(page_id, props_json):
    try:
        properties = json.loads(props_json)
    except json.JSONDecodeError as e:
        print("Props JSON invalides : " + str(e))
        return 1
    payload = {"properties": properties}
    result = api_request("PATCH", f"pages/{page_id}", payload)
    if "error" in result:
        print("ERREUR : " + result["error"])
        if "message" in result: print("   Detail : " + result["message"])
        return 1
    print("Page mise a jour")
    print("   ID : " + page_id)
    print("   URL : " + result.get("url", "?"))
    return 0

def cmd_add_content(page_id, text, block_type="paragraph"):
    valid_types = ["paragraph", "heading_1", "heading_2", "heading_3",
                   "bulleted_list_item", "numbered_list_item", "to_do",
                   "toggle", "quote", "callout", "divider", "code"]
    if block_type == "divider":
        children = [{"object": "block", "type": "divider", "divider": {}}]
    elif block_type == "code":
        children = [{"object": "block", "type": "code", "code": {"rich_text": [{"text": {"content": text}}], "language": "plain text"}}]
    elif block_type in valid_types:
        children = [{"object": "block", "type": block_type, block_type: {"rich_text": [{"text": {"content": text}}]}}]
    else:
        print("Type de bloc invalide : " + block_type)
        print("   Types valides : " + ", ".join(valid_types))
        return 1
    payload = {"children": children}
    result = api_request("PATCH", f"blocks/{page_id}/children", payload)
    if "error" in result:
        print("ERREUR : " + result["error"])
        if "message" in result: print("   Detail : " + result["message"])
        return 1
    print("Contenu ajoute a la page")
    print("   Type : " + block_type)
    txt_preview = text[:100]
    if len(text) > 100:
        txt_preview = txt_preview + "..."
    print("   Texte : " + txt_preview)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Outil Notion pour Max (VL Medical)", formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", help="Commande a executer")
    subparsers.add_parser("check", help="Verifie la connexion a Notion")
    p_search = subparsers.add_parser("search", help="Recherche des pages et bases")
    p_search.add_argument("query", help="Terme de recherche")
    subparsers.add_parser("databases", help="Liste les bases de donnees accessibles")
    p_query = subparsers.add_parser("query", help="Interroge une base de donnees")
    p_query.add_argument("database_id", help="ID de la base de donnees")
    p_query.add_argument("--filter", help="Filtre JSON Notion")
    p_query.add_argument("--sort", help="Tri JSON Notion")
    p_query.add_argument("--limit", type=int, default=50, help="Nombre max de resultats")
    p_read = subparsers.add_parser("read", help="Lit le contenu d une page")
    p_read.add_argument("page_id", help="ID de la page")
    p_create = subparsers.add_parser("create", help="Cree une entree dans une base")
    p_create.add_argument("database_id", help="ID de la base de donnees")
    p_create.add_argument("--title", required=True, help="Titre de l entree")
    p_create.add_argument("--props", help="Proprietes additionnelles (JSON)")
    p_update = subparsers.add_parser("update", help="Met a jour une page")
    p_update.add_argument("page_id", help="ID de la page")
    p_update.add_argument("--props", required=True, help="Proprietes a modifier (JSON)")
    p_content = subparsers.add_parser("add_content", help="Ajoute du contenu a une page")
    p_content.add_argument("page_id", help="ID de la page")
    p_content.add_argument("--text", required=True, help="Texte a ajouter")
    p_content.add_argument("--type", default="paragraph", help="Type de bloc")
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    if args.command == "check": return cmd_check()
    elif args.command == "search": return cmd_search(args.query)
    elif args.command == "databases": return cmd_databases()
    elif args.command == "query": return cmd_query(args.database_id, args.filter, args.sort, args.limit)
    elif args.command == "read": return cmd_read(args.page_id)
    elif args.command == "create": return cmd_create(args.database_id, args.title, args.props)
    elif args.command == "update": return cmd_update(args.page_id, args.props)
    elif args.command == "add_content": return cmd_add_content(args.page_id, args.text, getattr(args, "type", "paragraph"))
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
