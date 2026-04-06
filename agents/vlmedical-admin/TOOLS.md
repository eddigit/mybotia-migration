# TOOLS.md — Max — Outils disponibles

## 🔍 Auto-diagnostic — self_diagnostic.py

**Script** : `python3 tools/self_diagnostic.py`

### Tu DOIS lancer cet outil :
1. **Au début de chaque session** (mode quick) — avant de répondre à quoi que ce soit
2. **Quand un outil ne marche pas** — pour identifier la cause exacte
3. **Quand on te demande ce qui va/ne va pas** — c'est la réponse factuelle, pas du blabla
4. **Quand tu sens que tu ne peux pas exécuter une commande** — avant de dire "je ne peux pas"

### Commandes
| Commande | Usage | Description |
|----------|-------|-------------|
| `self_diagnostic.py` | Audit complet | Vérifie TOUT : exec, email, Notion, juridique, fichiers, gateway, WhatsApp, disque |
| `self_diagnostic.py quick` | Check rapide | Vérifie exec + email + Notion + gateway (10 sec) |
| `self_diagnostic.py fix` | Audit + auto-fix | Corrige ce qui est corrigeable automatiquement |
| `self_diagnostic.py report` | Rapport markdown | Génère diagnostic_report.md avec tout le détail |

### Codes retour
- `0` = tout OK — tu peux travailler normalement
- `1` = warnings — tu peux travailler mais signale les problèmes
- `2` = critiques — tu NE PEUX PAS travailler, appelle Jacques

### 🔴 RÈGLE ABSOLUE
Si le diagnostic détecte un problème critique : **DIS-LE IMMÉDIATEMENT AU CLIENT.** Ne masque JAMAIS un dysfonctionnement. Le message doit être :
> "J'ai un problème technique : [description exacte]. Je ne peux pas [action bloquée]. Jacques doit intervenir."

---

## ⚖️ Recherche juridique unifiée

**Script** : `python3 tools/legal_search.py`

### Commandes disponibles

| Commande | Source | Contenu |
|----------|--------|---------|
| `legal_search.py judilibre "requête"` | Cour de cassation | Jurisprudence (157 000+ décisions) |
| `legal_search.py legifrance "requête"` | Légifrance | Codes, lois, décrets en vigueur |
| `legal_search.py cedh "requête"` | HUDOC / CEDH | Arrêts Cour Européenne des Droits de l'Homme (7 200+) |
| `legal_search.py eurlex "requête"` | EUR-Lex | Droit de l'Union Européenne |
| `legal_search.py all "requête"` | Toutes | Recherche multi-sources |
| `legal_search.py codes` | Légifrance | Liste tous les codes disponibles |
| `legal_search.py status` | Toutes | Vérifie la connectivité de toutes les APIs |

### Options
- Nombre de résultats : `legal_search.py judilibre "requête" 10` (défaut: 5)

### Exemples pertinents VL Medical
```bash
# Jurisprudence dispositifs médicaux
python3 tools/legal_search.py judilibre "dispositif médical responsabilité" 5

# Règlement MDR dans le droit UE
python3 tools/legal_search.py eurlex "règlement 2017/745 dispositifs médicaux"

# Code de commerce — CGV
python3 tools/legal_search.py legifrance "conditions générales de vente"

# Dépôt-vente — jurisprudence
python3 tools/legal_search.py judilibre "contrat dépôt-vente responsabilité"
```

### Authentification
- **PISTE.gouv.fr** (sandbox) — credentials intégrés au script
- Auth OAuth2 automatique (client_credentials)

### ⚠️ Limitations
- PISTE est en mode **sandbox** (données réelles mais accès non garanti en prod)
- Pas d'accès aux décisions des Cours d'appel (pas d'API publique)
- Pas d'accès au registre du Barreau (pas d'API publique)
- EUR-Lex n'a pas d'API JSON simple — résultats limités

### 💡 Pour passer en production PISTE
Contacter : api@dila.gouv.fr pour demander l'activation production

---

## 📧 Email — email_tool.py

Ta boîte mail professionnelle : **max.vlmedical@collaborateur.pro**

### Commandes
| Commande | Usage | Description |
|----------|-------|-------------|
| check | `python3 tools/email_tool.py check` | Vérifie les nouveaux mails non lus |
| list | `python3 tools/email_tool.py list 20` | Liste les N derniers mails |
| read | `python3 tools/email_tool.py read 42` | Lit le contenu complet d'un mail |
| draft | `python3 tools/email_tool.py draft "dest@email.com" "Objet" "Corps" --attach fichier.pdf` | Brouillon (TOUJOURS avant envoi) |
| send | `python3 tools/email_tool.py send "dest@email.com" "Objet" "Corps" --attach fichier.pdf` | Envoie (⚠️ après GO du client) |
| reply | `python3 tools/email_tool.py reply 42 "Réponse"` | Réponse (⚠️ après GO du client) |
| search | `python3 tools/email_tool.py search "facture"` | Recherche dans les mails |

### 🔴 PIÈCES JOINTES — OBLIGATOIRE
- **Pour joindre un fichier** : ajouter `--attach /chemin/complet/fichier.pdf` à la fin de la commande `send` ou `draft`
- **Plusieurs fichiers** : `--attach fichier1.pdf fichier2.xlsx fichier3.docx`
- **TOUJOURS utiliser le chemin COMPLET** du fichier (ex: `/home/gilles/.openclaw-vlmedical/workspace-vlmedical-admin/dossiers/emilabo-marseille/offre.pdf`)
- **Si tu génères un document et que le client demande un envoi par email → tu DOIS l'attacher avec `--attach`**
- **JAMAIS écrire "PDF en pièce jointe" sans réellement joindre le fichier avec `--attach`**
- **Alternative** : `python3 tools/send_email_attachments.py "dest" "Objet" "Corps" fichier1.pdf fichier2.pdf`

### Règles
- TOUJOURS montrer le brouillon (draft) avec `--attach` si un fichier doit être joint
- ATTENDRE le "GO" explicite du client avant tout envoi
- Résumer chaque nouveau mail reçu (expéditeur, objet, urgence)
- VÉRIFIER que le fichier existe (`ls -la fichier`) AVANT d'envoyer

---

## 3. notion_tool.py — Gestion Notion (VL Medical)

**Fichier** : `tools/notion_tool.py`
**Token** : Intégration Notion dédiée "Max" — Workspace "Espace de Jean-Luc Aubagnac"
**Date déploiement** : 1 mars 2026

### Commandes

| Commande | Usage | Description |
|----------|-------|-------------|
| `check` | `python3 tools/notion_tool.py check` | Vérifie la connexion à Notion |
| `search` | `python3 tools/notion_tool.py search "mot-clé"` | Recherche pages et bases |
| `databases` | `python3 tools/notion_tool.py databases` | Liste les bases accessibles |
| `query` | `python3 tools/notion_tool.py query <db_id> [--filter JSON]` | Interroge une base |
| `read` | `python3 tools/notion_tool.py read <page_id>` | Lit une page (propriétés + contenu) |
| `create` | `python3 tools/notion_tool.py create <db_id> --title "X" [--props JSON]` | Crée une entrée |
| `update` | `python3 tools/notion_tool.py update <page_id> --props JSON` | Modifie une page |
| `add_content` | `python3 tools/notion_tool.py add_content <page_id> --text "X" [--type heading_2]` | Ajoute du contenu |

### Exemples pour VL Medical

```bash
# Vérifier la connexion
python3 tools/notion_tool.py check

# Lister toutes les bases de données
python3 tools/notion_tool.py databases

# Chercher un dossier
python3 tools/notion_tool.py search "appel d'offres"

# Interroger une base avec filtre
python3 tools/notion_tool.py query <db_id> --filter '{"property":"Status","select":{"equals":"En cours"}}'

# Créer une entrée
python3 tools/notion_tool.py create <db_id> --title "Dossier CH Toulouse" --props '{"Status":{"select":{"name":"En cours"}},"Client":{"rich_text":[{"text":{"content":"CH Toulouse"}}]}}'

# Mettre à jour un statut
python3 tools/notion_tool.py update <page_id> --props '{"Status":{"select":{"name":"Terminé"}}}'
```

### Prérequis

- Les pages et bases Notion doivent être **partagées avec l'intégration "Max"** dans le workspace de Jean-Luc Aubagnac
- Sans partage, les commandes `databases`, `search` et `query` ne retourneront rien

---

## 4. Génération de documents — Scripts workspace

### Proformas / Devis
| Script | Usage |
|--------|-------|
| `python3 tools/create_proforma_lch_pdf.py` | Génère une proforma PDF (format LCH) |
| `python3 tools/create_proforma_lch.py` | Génère une proforma Excel (format LCH) |

### Contrats GNS
| Script | Usage |
|--------|-------|
| `python3 gen_contrat_gns_pdf_v2.py` | Génère un contrat GNS en PDF (version courante) |
| `python3 gen_contrat_docx.py` | Génère un contrat en format Word (.docx) |

### Reconnaissances de dette
| Script | Usage |
|--------|-------|
| `python3 gen_reconnaissance_consult_v2.py` | Reconnaissance de dette Consult (version courante) |
| `python3 gen_reconnaissances_pdf.py` | Reconnaissances de dette en PDF |
| `python3 gen_reconnaissances_docx.py` | Reconnaissances de dette en Word |

### Protocoles
| Script | Usage |
|--------|-------|
| `python3 protocole_compensation.py` | Protocole de compensation GNS/VL |

### Envoi de documents
| Script | Usage |
|--------|-------|
| `python3 send_contrat_gns_v3.py` | Envoie un contrat GNS par email (version courante) |
| `python3 send_consult_v2.py` | Envoie une reconnaissance Consult par email |
| `python3 send_reconnaissances.py` | Envoie les reconnaissances par email |

### ⚠️ Règles pour TOUS les scripts de génération
- Vérifier que le fichier généré existe APRÈS exécution (`ls -la fichier`)
- Pour envoyer par email → utiliser `--attach` avec `email_tool.py` OU le script `send_*` dédié
- TOUJOURS montrer le résultat au client AVANT envoi
