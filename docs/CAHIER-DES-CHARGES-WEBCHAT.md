# Cahier des Charges — Webchat MyBotIA

**Version :** V.16.0 (état au 6 avril 2026)
**Objectif :** Documenter le fonctionnement complet du webchat pour reproduction chez Emergent

---

## 1. Vue d'ensemble

Le webchat MyBotIA est une **application web mono-page (SPA-like)** qui permet aux clients de converser avec leur(s) collaborateur(s) IA en temps réel via WebSocket. C'est l'interface principale de l'offre MaBoiteIA.

**URL actuelle :** `https://mybotia.com` et `https://app.mybotia.com`
**Stack :** PHP (backend API) + HTML/CSS/JS vanilla (frontend) — **aucun framework SPA**
**Connexion temps réel :** WebSocket vers les gateways OpenClaw

---

## 2. Architecture multi-collaborateurs

### Le principe fondamental

Chaque client MyBotIA a accès à **un ou plusieurs collaborateurs IA**. Le webchat s'adapte dynamiquement au collaborateur sélectionné :

- **Sous-domaine dédié** : Chaque agent a son propre sous-domaine → `lea.mybotia.com`, `max.mybotia.com`, `lucy.mybotia.com`, etc.
- **Wildcard Apache** : Un seul vhost `*.mybotia.com` sert tout le monde — le JS détecte le sous-domaine et charge le bon agent
- **Sélecteur de collaborateur** : Si un client a plusieurs collaborateurs, un dropdown en sidebar permet de basculer

### Détection du sous-domaine (app.js)

```javascript
var _hostParts = window.location.hostname.split('.');
if (_hostParts.length >= 3 && _hostParts[_hostParts.length - 2] === 'mybotia') {
  _subdomain = _hostParts[0].toLowerCase();
  if (_subdomain === 'app' || _subdomain === 'www') _subdomain = ''; // pas un agent
}
```

Le sous-domaine est ensuite utilisé pour :
1. Charger la config de l'agent (nom, avatar, rôle, cartes d'action)
2. Sélectionner la bonne session WebSocket (`agent:<agentId>:main`)
3. Se connecter au bon port gateway si l'agent est sur une gateway différente

### Configuration agents (private/agents.json)

Chaque agent est défini dans `private/agents.json` avec :

```json
{
  "lea": {
    "token": "<token_session>",
    "session": "agent:main:main",
    "name": "Léa",
    "agentId": "main",
    "avatar": "https://...",
    "role": "Directrice Admin & Juridique",
    "cards": [
      {
        "icon": "calendar",
        "title": "Mon planning du jour",
        "desc": "Rendez-vous, tâches et priorités",
        "prompt": "Quel est mon planning du jour ?"
      }
    ]
  },
  "lucy": {
    "token": "<token_session>",
    "session": "agent:lucy:lucy",
    "name": "Lucy",
    "agentId": "lucy",
    "port": 18795,
    "avatar": "https://...",
    "role": "Collaboratrice IA — IGH",
    "cards": [...]
  }
}
```

**Champs importants :**
- `token` : Token de session WebSocket (authentifie la connexion vers la gateway)
- `session` : Identifiant de session OpenClaw (format `agent:<agentId>:<scope>`)
- `agentId` : Identifiant de l'agent dans la gateway
- `port` : Si l'agent est sur une gateway différente (ex: Lucy sur 18795 au lieu de 18789)
- `cards` : Actions rapides affichées sur le dashboard d'accueil (voir section 4)
- `avatar` : URL Cloudinary de la photo de l'agent

### Agents actuels configurés

| Sous-domaine | Nom | Session | Gateway | Rôle |
|---|---|---|---|---|
| lea | Léa | agent:main:main | mybotia (18789) | Admin & Juridique |
| julian | Julian | agent:julian:main | mybotia (18789) | Expert technique |
| nina | Nina | agent:nina:main | mybotia (18789) | Commerciale |
| oscar | Oscar | agent:oscar:main | mybotia (18789) | Directeur opérations |
| eva | Eva | agent:vlmedical-commercial:main | vlmedical (18790) | Commerciale VL Medical |
| max | Max | agent:vlmedical-admin:main | vlmedical (18790) | Admin VL Medical |
| brice | Brice | agent:brice:main | test (18794) | Démo avocats |
| lucy | Lucy | agent:lucy:lucy | lucy (18795) | IGH (EHPAD) |

---

## 3. Authentification — Double système

### Mode 1 : Connexion email/mot de passe (clients)

C'est le mode principal pour les clients finaux :

1. L'utilisateur arrive sur `lea.mybotia.com` → écran de login
2. Il saisit email + mot de passe
3. `POST /api/auth.php` → vérifie dans SQLite, retourne :
   - `client` : infos client (id, company_name, contact_name, plan, max_tokens, is_admin)
   - `collaborateurs[]` : liste des collaborateurs autorisés pour ce client
   - `active_collaborateur` : sous-domaine du collaborateur actif
   - `session_key` : clé de session WebSocket
   - `csrf_token` : token CSRF pour les requêtes suivantes
4. Le JS appelle ensuite `GET /api/ws-token.php` pour obtenir le token gateway
5. Connexion WebSocket avec ce token

**Persistance :** Session PHP + option "Se souvenir de moi" (localStorage). Au rechargement, `GET /api/auth.php` récupère la session existante.

### Mode 2 : Token URL (admin/Gilles)

Pour l'accès rapide sans login :
- URL : `https://mybotia.com/?t=<token>&session=<session_key>&name=<nom>`
- Le token est directement utilisé pour la connexion WebSocket
- Pas d'écran de login

### Flux de connexion WebSocket

```
Client → fetchGatewayToken() → /api/ws-token.php → TOKEN
Client → new WebSocket(wss://mybotia.com/ws) avec TOKEN
        → Apache ProxyPass → localhost:18789 (gateway OpenClaw)
        → Authentification par token → Session établie
```

Si l'agent est sur un port différent (ex: Lucy sur 18795), le WebSocket se connecte au bon endpoint via le routing Apache.

### Déconnexion

- Bouton "Déconnexion" en sidebar
- `DELETE /api/auth.php` détruit la session PHP
- Nettoyage localStorage
- Fermeture WebSocket
- Retour à l'écran de login

---

## 4. Interface — Layout complet

### Structure 3 colonnes

```
┌─────────────────────────────────────────────────────────┐
│                     HEADER                              │
│  [☰] [◀] [Avatar] Nom / Rôle    [●status] [↻] [☽]    │
├──────────┬──────────────────────────┬───────────────────┤
│          │                          │                   │
│ SIDEBAR  │      ZONE CHAT           │  PANNEAU OUTILS   │
│          │                          │  (right-sidebar)  │
│ Sessions │  [Dashboard / Messages]  │                   │
│ Dossiers │                          │  CRM, Tâches,     │
│ Recherche│  [Streaming + Typing]    │  Clients, Notes   │
│          │                          │                   │
│ Compte   │  ─────────────────────── │                   │
│ Crédits  │  [📎] [🎤] [Message...] [▶] │                   │
│ Collab.  │                          │                   │
├──────────┴──────────────────────────┴───────────────────┤
│                     FOOTER                              │
│         CONÇU ET DÉVELOPPÉ PAR G.KORZEC — V.16.0       │
└─────────────────────────────────────────────────────────┘
```

### Header

| Élément | Description |
|---|---|
| Bouton burger (☰) | Ouvre/ferme la sidebar sur mobile |
| Bouton sidebar toggle (◀) | Masque/affiche la sidebar sur desktop |
| Avatar agent | Photo Cloudinary ou initiale |
| Nom + Rôle | Nom du collaborateur + son rôle |
| Status dot (●) | Vert = connecté, orange = connexion, rouge = déconnecté. Cliquable → panneau "Santé système" |
| Bouton refresh (↻) | Recharge la page |
| Bouton thème (☽/☀) | Bascule dark/light mode |

### Sidebar gauche

#### Section haute : Conversations
- **Bouton "Nouvelle conversation"** (icône crayon)
- **Barre de recherche** avec auto-complétion dans les sessions
- **Section "DOSSIERS"** (collapsible, titre en #88D4FD)
  - Sessions groupées par dossier
- **Section "30 DERNIERS JOURS"** (titre en #88D4FD)
  - Sessions récentes, triées par date
- **Session active** : Barre violette à gauche, titre en blanc + gras
- **Auto-expand** : Si la session active est dans un dossier fermé, il s'ouvre

#### Section basse : Compte utilisateur
- **Profil** : Avatar + nom + badge plan (Standard/Premium/Admin)
- **Menu compte** (···) : Mon profil, Usage mensuel, Paramètres, Déconnexion
- **Jauge de tokens** : Barre de progression (tokens utilisés / max)
- **Sélecteur de collaborateur** : Dropdown si le client a plusieurs agents

### Zone chat principale

#### Dashboard d'accueil (welcome)
Quand aucune conversation n'est active :
- **Avatar** : Logo Collaborateur IA ou avatar de l'agent
- **Message d'accueil** : "Bonjour, comment puis-je vous aider ?"
- **Cartes d'action rapide** (4-6 cartes selon l'agent) :
  - Chaque carte a une icône SVG, un titre, une description
  - Clic → envoie automatiquement le prompt associé
  - Les cartes sont **dynamiques** : configurées dans `agents.json` par agent

#### Zone de messages
- **Bulles utilisateur** : Alignées à droite, fond violet/accent
- **Bulles agent** : Alignées à gauche, avec avatar
- **Support Markdown** : Rendu via Prism.js pour le code
- **Pièces jointes** : Preview inline (images, documents)
- **Drag & drop** : Glisser un fichier sur la zone de chat

#### Indicateur de travail de l'agent

Séquence quand l'agent "réfléchit" :

1. **Indicateur "réfléchit..."** : Logo Collaborateur IA avec pulse lumineux violet + "Votre collaborateur réfléchit..."
2. **Étapes progressives** (simulées, car OpenClaw ne streame pas les tool_use) :
   - 🧠 Analyse de la demande... (3s)
   - 🔍 Recherche d'informations... (6s)
   - ⚡ Exécution des actions... (9s)
   - 📝 Rédaction de la réponse... (12s)
3. **Streaming** : Le texte arrive de façon fluide (bufferisé 350ms pour éviter les saccades lettre par lettre)
4. **Indicateur d'activité** : Si aucun nouveau texte pendant 3s pendant le streaming, une barre "En cours..." apparaît

#### Barre de sources
Sous le header, bandeau horizontal scrollable montrant les sources connectées :
- Légifrance, Judilibre, EUR-Lex, CEDH (juridique)
- Gmail, Banque (Qonto), WhatsApp, Telegram, Notion, Web, CRM
- Chaque chip a un dot vert "actif"
- **Les sources affichées dépendent de l'agent** (à configurer par agent chez Emergent)

### Zone de saisie (input-area)

| Élément | Fonctionnalité |
|---|---|
| 📎 Bouton pièce jointe | Ouvre le sélecteur de fichier (images, PDF, Word, Excel, CSV, TXT, ZIP) |
| 🎤 Bouton micro | Dictée vocale (Speech-to-Text navigateur) |
| Textarea | Auto-expand, placeholder "Tapez votre message...", Enter = envoyer, Shift+Enter = nouvelle ligne |
| ▶ Bouton envoyer | Envoie le message + pièces jointes |
| ■ Bouton stop | Arrête la génération en cours (aussi via Escape) |
| 🎵 Bouton mode vocal | Ouvre le panneau Voice (voir section 7) |

### Preview pièces jointes
- Les fichiers joints apparaissent dans une barre de preview au-dessus de l'input
- Images : thumbnail
- Documents : icône + nom de fichier
- Bouton X pour retirer

---

## 5. Panneau Outils (right-sidebar)

Le panneau de droite (tools-panel.js, style-v12.css) affiche des outils métier :

- **CRM** : Fiche client, projets, suivi
- **Tâches** : Liste de tâches Notion
- **Clients** : Annuaire clients
- **Notes** : Prise de notes
- **WhatsApp** : Contacts et messages récents

Ce panneau est **masquable** et s'ouvre via des boutons dans le header ou via des actions dans le chat.

---

## 6. Panneaux secondaires (overlays)

### Panneau "Mon profil"
- Photo de profil (upload)
- Nom du contact (modifiable)
- Entreprise, email, plan (lecture seule)
- **Instructions globales** : Texte libre transmis à TOUS les collaborateurs (ex: "Vouvoyez-moi")
- **Instructions par collaborateur** : Un textarea par collaborateur autorisé
- Bouton "Sauvegarder et synchroniser"

### Panneau "Usage mensuel"
- Pourcentage de tokens utilisés (barre de progression)
- Détail tokens utilisés / max
- Estimation de fin de mois
- Graphique d'activité des 7 derniers jours (barres)

### Panneau "Paramètres"
- **Avatar du collaborateur** : Changement via URL
- **Infos agent** : Nom, rôle, sous-domaine (lecture seule)
- **Mode vocal** : Microphone, vitesse de parole, mode par défaut, email comptes-rendus
- **Santé système** : Status des services (gateway, agent, DB, PHP, SSL, disque, préférences)

### Panneau "Fiche client" (CRM)
- Avatar + nom de l'entreprise
- Contact (email, téléphone)
- Status, agent assigné, abonnement, canal
- Notes
- Lien vers Notion

---

## 7. Mode vocal (Voice)

Le webchat intègre un **mode vocal** (panneau latéral droit) :

### 3 modes
1. **Libre** : Conversation naturelle (appuyer pour parler, relâcher pour envoyer)
2. **Sur appel** : Activation par mot-clé (dit le nom de l'agent)
3. **Réunion** : Transcription continue avec timer + sauvegarde

### Composants
- **Orbe** : Cercle animé central (micro, spinner, états visuels)
- **Pipeline** : Label d'état (Écoute, Transcription, Réflexion, Synthèse vocale)
- **Transcript** : Historique de la conversation vocale
- **TTS** : Synthèse vocale via ElevenLabs (server-side Python → audio renvoyé au client)

### Fin de session vocale
- **Conserver** dans le fil de conversation
- **Résumer** par l'IA (remplace les échanges vocaux par une synthèse)
- **Supprimer** du fil

### Fin de réunion
- **Pause** (reprendre plus tard)
- **Terminer + email** (CR envoyé par email)
- **Terminer sans email** (CR dans la conversation uniquement)

---

## 8. Communication WebSocket — Protocole OpenClaw

### Événements reçus

Le WebSocket envoie des événements de type `agent` :

| Event | Champ | Description |
|---|---|---|
| `stream: "lifecycle"` | `data.phase: "start"` | L'agent commence à travailler |
| `stream: "lifecycle"` | `data.phase: "end"` | L'agent a fini |
| `stream: "assistant"` | `data.text` | Texte accumulé complet |
| `stream: "assistant"` | `data.delta` | Nouveau texte incrémental |

**Important :** Les `tool_use` ne sont PAS streamées au client. C'est pourquoi les étapes progressives (🧠→🔍→⚡→📝) sont simulées côté JS.

### Messages envoyés

```json
{
  "type": "chat",
  "text": "Le message de l'utilisateur",
  "session": "agent:main:main",
  "attachments": [
    {
      "type": "image",
      "data": "base64...",
      "mimeType": "image/jpeg",
      "fileName": "photo.jpg"
    }
  ]
}
```

### Reconnexion automatique

- Backoff exponentiel (800ms → 1.6s → 3.2s → ... max 30s)
- Bannière "Reconnexion..." avec bouton "Reconnecter maintenant"
- Restauration de l'état de génération si `_isGenerating` était true

---

## 9. Thème et design

### Charte graphique
- **Couleur accent** : Violet (#6366f1 / #a78bfa)
- **Background** : Dark mode par défaut (#0b101c)
- **Light mode** : Disponible via toggle
- **Font** : Inter (400/500/600/700) + Marck Script (branding)
- **Icons** : Phosphor Icons (thin) + SVG inline

### PWA
- `manifest.json` configuré
- Service Worker (`sw.js`) pour le cache
- Installable sur mobile (Add to Home Screen)
- `viewport-fit=cover` pour les safe areas iPhone

### Responsive
- **Desktop** : 3 colonnes (sidebar + chat + tools panel)
- **Mobile** : Sidebar en overlay (burger menu), tools panel masqué
- **Tablette** : Layout adaptatif

---

## 10. APIs PHP backend

| Endpoint | Méthode | Rôle |
|---|---|---|
| `/api/auth.php` | GET | Récupérer session existante |
| `/api/auth.php` | POST | Login (email/password ou token) |
| `/api/auth.php` | PATCH | Changer le collaborateur actif |
| `/api/auth.php` | DELETE | Logout |
| `/api/ws-token.php` | GET | Obtenir le token gateway WebSocket |
| `/api/profile.php` | GET/PUT | Profil utilisateur (nom, photo, instructions) |
| `/api/preferences.php` | GET/PUT | Préférences (avatar, voice settings) |
| `/api/upload.php` | POST | Upload fichier (profil photo) |
| `/api/status.php` | GET | Santé système (gateway, DB, SSL, etc.) |
| `/api/usage.php` | GET | Usage tokens du mois |
| `/api/feedback.php` | POST | Feedback utilisateur (👍/👎) |
| `/api/notes.php` | GET/POST | Notes persistantes |
| `/api/crm.php` | GET | Données CRM (clients, projets) |
| `/api/notion-clients.php` | GET | Clients depuis Notion |
| `/api/notion-tasks.php` | GET/POST/PUT | Tâches Notion |
| `/api/link-preview.php` | GET | Aperçu de liens (OG metadata) |
| `/api/voice-config.php` | GET | Config ElevenLabs pour le mode vocal |
| `/api/health.php` | GET | Health check simple |

### Base de données
- **SQLite** (`private/mybotia.db`) : Clients, sessions, notes, feedback, préférences
- **PostgreSQL** (mybotia_crm via env.php) : CRM complet (clients, projets, paiements)
- **Notion** : Sync one-way depuis PostgreSQL (tâches, clients)

---

## 11. Configuration côté Emergent — Ce qu'il faut reproduire

### Pour chaque client MyBotIA, il faut :

1. **Un compte** avec email/mot de passe
2. **Un ou plusieurs collaborateurs** assignés (avec leurs SOUL.md)
3. **Un sous-domaine** par collaborateur (`prenom.mybotia.com`)
4. **Des cartes d'action** personnalisées par agent
5. **Un quota de tokens** mensuel (selon le plan Standard/Premium)
6. **Des instructions personnalisées** (globales + par collaborateur)

### Pour le webchat, il faut :

1. **Login email/password** → retourne la liste des collaborateurs autorisés
2. **Connexion WebSocket** vers le bon agent
3. **Streaming texte** avec indicateur de travail
4. **Upload fichiers** (images, PDF, documents)
5. **Historique conversations** (sidebar avec sessions, dossiers, recherche)
6. **Panneau profil** avec instructions personnalisées
7. **Usage mensuel** (compteur tokens)
8. **Mode vocal** (ElevenLabs TTS)
9. **PWA** (installable, offline-capable)
10. **Dark/Light mode**

### Ce qui peut être simplifié chez Emergent :

- Le double système auth (email + token URL) → probablement juste email
- Le routing multi-ports (18789/18790/18795) → Emergent gère les gateways
- Les APIs PHP → remplacées par l'API REST Emergent
- Le panneau outils (CRM, Notion, tâches) → à voir si Emergent a un équivalent

---

## 12. Fichiers sources

| Fichier | Lignes | Rôle |
|---|---|---|
| `public/index.html` | 743 | Structure HTML complète (tous les panneaux) |
| `public/js/app.js` | 6040 | Logique principale (auth, WebSocket, chat, streaming, sidebar, panneaux) |
| `public/js/tools-panel.js` | 1286 | Panneau outils (CRM, tâches, clients, notes) |
| `public/js/voice-client.js` | 655 | Mode vocal (STT, TTS, modes, orbe) |
| `public/css/style.css` | 3158 | Styles principaux (sidebar, chat, messages, animations) |
| `public/css/style-v12.css` | — | Styles panneau outils (right-sidebar, rs-*) |
| `public/css/voice.css` | 486 | Styles mode vocal |
| `private/agents.json` | 300 | Config de tous les agents (tokens, sessions, cartes) |
| `private/config.inc.php` | — | Routing agents par sous-domaine/token |
| `private/env.php` | — | Credentials centralisées (PG, Notion) |
| `private/db.php` | — | Helpers SQLite + PostgreSQL |
| `public/api/*.php` | ~15 fichiers | Endpoints REST |

---

*Document rédigé le 6 avril 2026 par Jacques (Claude Code) — Coach Digital Paris*
