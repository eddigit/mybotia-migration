# Stack Technique — MyBotIA

## Serveur

| Composant | Version |
|-----------|---------|
| OS | Debian 12 (Bookworm) |
| Kernel | Linux 6.12.43+deb13-amd64 |
| Node.js | 22.22.0 |
| Python | 3.11 |
| OpenClaw | 2026.4.2 |
| Apache | 2.4 |
| Nginx | 1.22 |
| Docker | CE |
| Redis | 6+ |
| MySQL | 8+ |
| PostgreSQL | 15+ (Docker) |

## Frontend Webchat (mybotia.com)

- **Langage :** PHP + HTML/CSS/JS vanilla
- **Pas de framework SPA** (pas React, pas Vue, pas Angular)
- **CSS :** Style custom (style.css, style-v12.css, voice.css)
- **JS :** app.js, tools-panel.js, voice-client.js
- **Auth :** Token-based (agents.json) + email/password
- **WebSocket :** Connexion directe vers gateway OpenClaw via Apache reverse proxy
- **PWA :** manifest.json + service worker (sw.js)
- **Base locale :** SQLite (sessions, clients)

## Admin Dashboard (admin.mybotia.com)

- **Framework :** Express.js (Node)
- **Port :** 3001
- **Architecture :** Modulaire (21 modules) — server.js + routes/ + services/ + middleware/
- **Features :** CRUD agents, wizard déploiement, CRM PostgreSQL, OAuth management, Notion sync
- **Base :** PostgreSQL (mybotia_crm) + Notion API

## Voice POC V2 (voice.mybotia.com)

- **Backend :** Express.js (Node)
- **TTS :** Python + ElevenLabs API
- **Frontend :** HTML/CSS/JS (PWA)
- **Port :** 3100

## Gateways OpenClaw

- **Runtime :** Node.js (CLI openclaw)
- **WhatsApp :** Baileys (WebSocket, pas l'API Business officielle)
- **Telegram :** grammy
- **WebSocket :** intégré (clients webchat)
- **Sandbox :** Docker containers pour isolation outils agents
- **Auth LLM :** OAuth tokens Anthropic (sk-ant-oat01-*)
- **Config :** JSON (openclaw.json par gateway)

## Intégrations

| Service | Usage | Protocole |
|---------|-------|-----------|
| Anthropic Claude | LLM principal | OAuth API |
| ElevenLabs | Text-to-Speech | REST API |
| Brave Search | Recherche web agents | REST API |
| Notion | CRM, bases de données, sync | REST API |
| Cloudinary | Upload/stockage images | REST API |
| Google Gmail | Envoi emails | OAuth2 + REST |
| Google Calendar | Agenda | OAuth2 + REST |
| Pennylane | Facturation | REST API |
| Qonto | Banque / transactions | REST API |
| Migadu | Email agents | SMTP |
| Telegram | Messaging bots | Bot API |
| WhatsApp | Messaging (Baileys) | WebSocket |
