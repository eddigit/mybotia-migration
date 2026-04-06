# Clarification Architecture & Données — Pour Emergent

**Date :** 6 avril 2026
**Contexte :** Ce document clarifie la distinction entre les différents composants MyBotIA et documente précisément où sont stockées les données.

---

## 1. Deux interfaces distinctes — NE PAS CONFONDRE

### Le Webchat (mybotia.com / *.mybotia.com) — Interface CLIENT

C'est l'interface que les **clients finaux** utilisent au quotidien. Chaque client se connecte avec son email/mot de passe et accède à **son ou ses collaborateurs IA**.

- **URL** : `lea.mybotia.com`, `max.mybotia.com`, `lucy.mybotia.com`, etc.
- **Auth** : Email + mot de passe (par client)
- **Fonctionnalités** : Chat temps réel, historique conversations, pièces jointes, mode vocal, profil, instructions personnalisées
- **Multi-collaborateurs** : Un client peut avoir accès à plusieurs agents. Il bascule entre eux via un sélecteur en sidebar ou en changeant de sous-domaine.
- **C'est LE produit** que les clients paient (490 ou 980 €/mois)

### Le Dashboard Admin (admin.mybotia.com / client.mybotia.com) — Interface ADMIN

C'est l'interface de **gestion interne** pour Gilles (et potentiellement les admins). Elle sert à administrer les agents, les clients, les déploiements.

- **URL** : `admin.mybotia.com` ou `client.mybotia.com`
- **Stack** : Express.js (Node), port 3001
- **Fonctionnalités** : CRUD agents, wizard déploiement, CRM PostgreSQL, OAuth management, Notion sync
- **Ce n'est PAS ce que les clients voient**

### Résumé

| | Webchat | Admin Dashboard |
|---|---|---|
| **Pour qui** | Clients finaux | Gilles / admins |
| **URL** | *.mybotia.com | admin.mybotia.com |
| **Stack** | PHP + HTML/JS | Express.js (Node) |
| **Auth** | Email/password client | Token admin |
| **Priorité migration** | HAUTE | Moyenne |

---

## 2. Stockage des données — Où trouver quoi

### 2.1 Historiques de conversation (CRITIQUE)

Les conversations sont stockées par **OpenClaw** dans des fichiers JSONL, PAS dans une base de données SQL.

```
~/.openclaw/agents/<agentId>/sessions/<uuid>.jsonl
```

**Chaque fichier JSONL** = une session de conversation complète (tous les messages user + assistant + metadata).

#### Localisation par gateway :

| Gateway | Chemin | Agents | Nb sessions |
|---|---|---|---|
| **mybotia** | `~/.openclaw/agents/main/sessions/` | Léa | **408 sessions (138 Mo)** |
| mybotia | `~/.openclaw/agents/julian/sessions/` | Julian | 8 sessions |
| mybotia | `~/.openclaw/agents/nina/sessions/` | Nina | 22 sessions |
| mybotia | `~/.openclaw/agents/oscar/sessions/` | Oscar | 7 sessions |
| mybotia | `~/.openclaw/agents/bullsage/sessions/` | BullSage | 24 sessions |
| mybotia | `~/.openclaw/agents/jacques/sessions/` | Jacques | 3 sessions |
| **vlmedical** | `~/.openclaw-vlmedical/agents/vlmedical-admin/sessions/` | Max | 31 sessions |
| vlmedical | `~/.openclaw-vlmedical/agents/vlmedical-commercial/sessions/` | Eva | 2 sessions |
| **lucy** | `~/.openclaw-lucy/agents/lucy/sessions/` | Lucy | 4 sessions |

#### Format d'un fichier session (.jsonl) :

Chaque fichier contient un objet JSON par ligne. La première ligne est le header de session :

```json
{
  "agent:main:main": {
    "sessionId": "dc06e2a0-...",
    "updatedAt": 1775208134848,
    "chatType": "direct",
    "deliveryContext": {
      "channel": "whatsapp",
      "to": "+33652345180",
      "accountId": "default"
    },
    "origin": {
      "label": "+33652345180"
    }
  }
}
```

Les lignes suivantes sont les messages (user, assistant, tool_use, etc.).

**Important :** Les sessions contiennent les conversations de TOUS les canaux (WhatsApp, Telegram ET webchat). Le champ `deliveryContext.channel` indique le canal d'origine.

### 2.2 Mémoire des agents (SQLite + fichiers .md)

Chaque agent a deux types de mémoire :

#### Mémoire vectorielle (SQLite + embeddings)
```
~/.openclaw/memory/<agentId>.sqlite
```
- Contient des chunks de texte avec embeddings pour la recherche sémantique
- Tables : `chunks`, `chunks_fts`, `chunks_vec`, `embedding_cache`, `files`
- Utilisé pour le RAG (Retrieval-Augmented Generation)
- Tailles : main.sqlite (20 Mo), bullsage.sqlite (27 Mo), nina.sqlite (16 Mo)

#### Mémoire contextuelle (fichiers .md dans workspace)
```
~/.openclaw/workspace-<agent>/memory/*.md
~/.openclaw/workspace-<agent>/MEMORY.md
```
- Fichiers Markdown lisibles par l'agent au démarrage de chaque session
- Contient l'historique des interactions, les décisions, les apprentissages

### 2.3 Base SQLite Webchat (auth + config clients)

```
/var/www/html/mybotia/private/mybotia.db
```

| Table | Contenu |
|---|---|
| `clients` | Comptes clients (email, password_hash, company_name, plan, max_tokens) |
| `client_collaborateurs` | Association client ↔ collaborateurs (subdomain, gateway_port, agent_id, session_key) |
| `client_instructions` | Instructions personnalisées par client (globales + par collaborateur) |
| `client_notes` | Notes prises par le client dans le webchat |
| `usage_log` | Compteur de tokens par client/collaborateur/mois |
| `user_preferences` | Préférences UI (avatar, voice settings, etc.) |

#### Clients actuels :

| ID | Email | Entreprise | Plan | Tokens/mois | Admin |
|---|---|---|---|---|---|
| 2 | coachdigitalparis@gmail.com | Coach Digital | enterprise | 2M | Oui |
| 3-6 | lea/julian/nina/oscar@collaborateur.pro | Coach Digital | enterprise | 2M | Oui |
| 7 | max.vlmedical@collaborateur.pro | VL Medical | pro | 500K | Non |
| 8 | eva.vlmedical@collaborateur.pro | VL Medical | pro | 500K | Non |
| 9 | lucy@collaborateur.pro | IGH | pro | 500K | Non |

#### Associations client → collaborateurs :

| Client (email) | Collaborateurs autorisés |
|---|---|
| coachdigitalparis@gmail.com (Gilles) | Léa, Julian, Nina, Oscar, Brice, Lucy (6 agents) |
| lea@collaborateur.pro | Léa (1 agent, accès direct) |
| max.vlmedical@collaborateur.pro | Max (gateway VL Medical, port 18790) |
| eva.vlmedical@collaborateur.pro | Eva (gateway VL Medical, port 18790) |
| lucy@collaborateur.pro | Lucy (gateway Lucy, port 18795) |

### 2.4 CRM PostgreSQL

```
Host: 127.0.0.1:5432
Database: mybotia_crm
User: prospection
```

Contient : clients (46), projets (74), paiements (10), portefeuille.
Source de vérité pour les données business → sync one-way vers Notion.

### 2.5 Registre des flows (OpenClaw)

```
~/.openclaw/flows/registry.sqlite
```
Table `flow_runs` — traces d'exécution des workflows agents.

---

## 3. Comment le webchat charge les historiques

Quand un client se connecte au webchat :

1. **Login** → `POST /api/auth.php` → SQLite `clients` + `client_collaborateurs`
2. **Token gateway** → `GET /api/ws-token.php` → retourne le token pour la connexion WebSocket
3. **WebSocket** → connexion à la gateway OpenClaw (`wss://mybotia.com/ws`)
4. **Sessions** → la gateway OpenClaw envoie la liste des sessions existantes pour cet agent/scope
5. **Historique** → quand le client clique sur une session dans la sidebar, la gateway renvoie les messages de cette session (depuis le fichier JSONL)

**La sidebar du webchat affiche les sessions qui viennent d'OpenClaw**, pas d'une base SQL.

Le webchat JS reçoit les sessions via un event WebSocket au moment de la connexion, et les affiche dans la sidebar avec :
- Le titre (premier message ou titre auto-généré)
- La date de dernière activité
- Groupement par "Dossiers" et "30 derniers jours"

---

## 4. Ce qu'Emergent doit gérer pour reproduire le webchat

### Données à migrer :
1. **Comptes clients** (SQLite `clients`) → recréer chez Emergent
2. **Associations client ↔ collaborateurs** (SQLite `client_collaborateurs`) → reconfigurer
3. **Instructions personnalisées** (SQLite `client_instructions`) → transférer
4. **Historiques de conversation** (fichiers JSONL dans `agents/*/sessions/`) → importer si possible, ou repartir de zéro

### APIs à exposer :
1. **Auth** : login email/password → retourne client + collaborateurs autorisés
2. **Sessions** : liste des conversations passées pour un client/agent
3. **Chat WebSocket** : envoi/réception de messages en temps réel avec streaming
4. **Profil** : instructions personnalisées, préférences, avatar
5. **Usage** : compteur tokens mensuel

### Stockage requis :
- Conversations (équivalent des JSONL OpenClaw)
- Comptes clients (équivalent du SQLite mybotia.db)
- Mémoire agents (équivalent des SQLite + fichiers .md)

---

*Document rédigé le 6 avril 2026 par Jacques (Claude Code)*
