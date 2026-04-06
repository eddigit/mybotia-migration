# PROMPT JULES — Optimisation Gestion des Sessions v12-7

## CONTEXTE — NE PAS CHERCHER, TOUT EST LÀ

L'interface Collaborateur IA (MyBotIA) est servie sur `*.mybotia.com` (ex: lea.mybotia.com, max.mybotia.com).

### Architecture des fichiers (sur le VPS hôte, PAS dans le container OpenClaw) :

```
/var/www/html/mybotia/           ← Dossier racine servi par Apache
├── index.html                   ← HTML principal (568 lignes)
├── css/
│   ├── style.css                ← CSS base
│   └── style-v12.css            ← CSS v12 (2062 lignes) — versionné ?v=v12-7
├── js/
│   ├── app.js                   ← JS principal (4441 lignes) — versionné ?v=v12-7
│   └── tools-panel.js           ← Panel outils (chargé séparément)
├── api/
│   ├── auth.php                 ← Authentification email/password + sessions PHP
│   └── preferences.php          ← Sync préférences (thème, dossiers) côté serveur
├── config.php                   ← Config agent par sous-domaine (avatar, cards, rôle)
├── wa-contacts.json             ← Noms contacts WhatsApp
├── manifest.json                ← PWA manifest
├── sw.js                        ← Service Worker
└── icon-*.png                   ← Icônes PWA
```

L'interface communique avec le **gateway OpenClaw** (port 18789, bind loopback) via **WebSocket JSON-RPC**.

### APIs WebSocket utilisées pour les sessions :
- `sessions.list` → liste toutes les sessions (params: `limit`, `includeDerivedTitles`, `includeLastMessage`)
- `sessions.update` → met à jour une session (params: `sessionKey`, `title`)
- `chat.history` → charge l'historique d'une session (params: `sessionKey`, `limit`)
- `agent.identity.get` → identité de l'agent (params: `sessionKey`)

### Comment les sessions sont identifiées :
- Chaque session a un `sessionKey` de format `agent:<agentId>:<simpleKey>`
- Le `simpleKey` est la partie après le dernier `:` (ex: `main`, `chat-20260313-191743`, `120363407026699197@g.us`)
- Les sessions webchat auto-créées suivent le pattern : `chat-YYYYMMDD-HHMMSS`
- Les sessions WhatsApp contiennent `@s.whatsapp.net` (DM) ou `@g.us` (groupe)
- La session spéciale `main` est la session principale

### Comment les noms de session fonctionnent ACTUELLEMENT (app.js) :

1. **Renommage local** : stocké dans `localStorage` sous `mybotia-renames` (objet `{simpleKey: "nom"}`)
2. **Auto-titre** : fonction `autoGenerateTitle()` (ligne ~2044) — génère un titre IA pour les sessions `chat-XXXXXXXX-XXXXXX` au 1er message, via `sessions.update` côté gateway + stockage local
3. **Résolution WhatsApp** : `resolveSessionName()` utilise `wa-contacts.json` pour les noms WA
4. **Affichage** : priorité = renommage local > titre serveur > nom WA > label > simpleKey

### Sidebar existante (app.js ligne ~2185-2700) :

- **Dossiers** : système complet avec CRUD, collapsible, types (projet/client/général), couleurs, drag & drop
- **Groupement par date** : Aujourd'hui / Hier / 7 jours / 30 jours / Plus ancien
- **Section WhatsApp** : collapsible séparément
- **Recherche** : barre de recherche avec clear button (HTML existe, vérifier JS)
- **Menu contextuel** : clic droit ou bouton "..." sur chaque session → renommer, déplacer, supprimer, épingler
- **Badges non-lus** : `unreadCounts` par sessionKey
- **Préférences sync** : dossiers + thème synchronisés via `/api/preferences.php`

### Fonctions clés dans app.js :
- `loadSessions()` — ligne ~2233 : charge via `sessions.list` API
- `renderSessions()` — ligne ~2280 : rendu complet sidebar
- `createSessionItem()` — ligne ~2565 : crée un élément DOM session
- `switchSession()` — rechercher dans le fichier : change de session active
- `autoGenerateTitle()` — ligne ~2044 : auto-nommage IA
- `getSessionRenames()` / `saveSessionRenames()` — stockage local des noms
- `getHiddenSessions()` — sessions cachées (supprimées côté client)
- `showSessionContextMenu()` — menu contextuel clic droit
- `updateSidebarActiveItem()` — mise à jour en temps réel de l'item actif
- `relativeTime()` — formatage temps relatif (À l'instant, Il y a 5 min, etc.)
- `escapeHtml()` — échappement HTML
- `resolveSessionName()` — résolution noms WhatsApp
- `getSessionIcon()` — icône WhatsApp pour les sessions WA

### Nouveau chat (bouton "+") :
Rechercher `btn-new-chat` dans app.js pour voir comment une nouvelle session est créée. Le pattern est :
```js
var now = new Date();
var key = 'chat-' + now.toISOString().slice(0,10).replace(/-/g,'') + '-' + now.toTimeString().slice(0,8).replace(/:/g,'');
SESSION_KEY = key;
```

---

## OBJECTIF — Optimiser la gestion des sessions

### 1. Nommer une session dès sa création
- Quand l'utilisateur clique "+", afficher un **champ inline éditable** en haut de la sidebar (pas de popup)
- Pré-remplir avec "Nouvelle conversation"
- Si l'utilisateur tape un nom → utiliser ce nom comme sessionKey display
- Si l'utilisateur ne tape rien et envoie un message → `autoGenerateTitle()` prend le relais

### 2. Renommer une session existante
- **Double-clic** sur le titre d'une session → édition inline (le titre devient un input)
- **Menu contextuel** (clic droit) → option "Renommer" (DÉJÀ EXISTANT, vérifier que ça marche)
- Sauvegarder via `sessions.update` API + localStorage

### 3. Auto-nommage intelligent
- `autoGenerateTitle()` existe déjà — vérifier qu'elle fonctionne bien
- Le titre doit être court (max 40 chars), descriptif du sujet de conversation
- Ne pas re-générer si un titre custom existe déjà

### 4. Recherche dans les sessions
- La barre HTML existe (`#sidebar-search`)
- Vérifier que le JS de filtrage fonctionne (filtre sur titre + preview)
- Ajouter highlight du terme recherché dans les résultats

### 5. UX inspirée Claude.ai / ChatGPT
- Transitions fluides lors de l'ajout/suppression de sessions
- Animation subtile quand une session remonte en haut (nouveau message)
- Feedback visuel lors du renommage (bordure, icône check)
- Le bouton "+" doit être bien visible et réactif

---

## RÈGLES

1. **NE MODIFIE RIEN** sans avoir d'abord montré ta proposition à Gilles
2. Présente d'abord : quels fichiers tu vas modifier, quelles fonctions, quel impact
3. Le code est en **vanilla JS** (pas de React/Vue/framework) — reste en vanilla
4. Teste que tes modifs ne cassent pas : login, WebSocket, dossiers, WhatsApp sessions
5. Versionne en **v12-8** (update le footer + les query params CSS/JS)
