---
name: notion
description: Gestion Notion - recherche, lecture, creation et mise a jour de pages et bases de donnees pour VL Medical.
---

# Notion - Outil de gestion

Tu disposes d un outil Python `notion_tool.py` dans ton repertoire `tools/` qui te permet d interagir avec l espace Notion de VL Medical.

## Comment utiliser

Utilise la commande `exec` pour lancer le script :

```
exec python3 tools/notion_tool.py <commande> [arguments]
```

## Commandes disponibles

### Verifier la connexion
```
exec python3 tools/notion_tool.py check
```
Verifie que la connexion a Notion fonctionne et affiche le workspace connecte.

### Rechercher
```
exec python3 tools/notion_tool.py search "mot-cle"
```
Recherche des pages et bases de donnees par mot-cle.

### Lister les bases de donnees
```
exec python3 tools/notion_tool.py databases
```
Liste toutes les bases de donnees accessibles avec leurs colonnes.

### Interroger une base de donnees
```
exec python3 tools/notion_tool.py query <database_id>
exec python3 tools/notion_tool.py query <database_id> --filter '{"property":"Status","select":{"equals":"Actif"}}'
exec python3 tools/notion_tool.py query <database_id> --sort '[{"property":"Date","direction":"descending"}]'
```
Recupere les entrees d une base. Supporte les filtres et le tri au format JSON Notion.

### Lire une page
```
exec python3 tools/notion_tool.py read <page_id>
```
Affiche les proprietes et le contenu d une page.

### Creer une entree
```
exec python3 tools/notion_tool.py create <database_id> --title "Titre"
exec python3 tools/notion_tool.py create <database_id> --title "Titre" --props '{"Status":{"select":{"name":"Actif"}}}'
```
Cree une nouvelle entree dans une base de donnees. Les proprietes additionnelles sont au format JSON Notion.

### Mettre a jour une page
```
exec python3 tools/notion_tool.py update <page_id> --props '{"Status":{"select":{"name":"Termine"}}}'
```
Modifie les proprietes d une page existante.

### Ajouter du contenu
```
exec python3 tools/notion_tool.py add_content <page_id> --text "Texte a ajouter"
exec python3 tools/notion_tool.py add_content <page_id> --text "Titre de section" --type heading_2
exec python3 tools/notion_tool.py add_content <page_id> --text "Point important" --type bulleted_list_item
```
Ajoute des blocs de contenu a une page. Types : paragraph, heading_1, heading_2, heading_3, bulleted_list_item, numbered_list_item, to_do, quote, code, divider.

## Formats de proprietes courants (pour --props)

- **Texte** : `{"Champ": {"rich_text": [{"text": {"content": "valeur"}}]}}`
- **Select** : `{"Status": {"select": {"name": "Actif"}}}`
- **Multi-select** : `{"Tags": {"multi_select": [{"name": "A"}, {"name": "B"}]}}`
- **Date** : `{"Date": {"date": {"start": "2026-03-01"}}}`
- **Checkbox** : `{"Valide": {"checkbox": true}}`
- **Nombre** : `{"Montant": {"number": 1500}}`
- **URL** : `{"Site": {"url": "https://..."}}`
- **Email** : `{"Contact": {"email": "a@b.com"}}`

## Conseils

1. Commence toujours par `check` pour verifier la connexion
2. Utilise `databases` pour decouvrir les bases disponibles et leurs IDs
3. Utilise `search` quand tu ne connais pas l ID d une page ou base
4. Les IDs Notion sont des UUID (avec ou sans tirets)
5. La propriete titre par defaut est "Name" -- si la base utilise un autre nom, adapte le --props
