# Architecture MyBotIA — État actuel VPS

## Vue d'ensemble

```
Internet
    │
    ├── Apache (80/443) ─── SSL Wildcard Let's Encrypt
    │   ├── mybotia.com / *.mybotia.com → /var/www/html/mybotia/public (webchat PHP)
    │   ├── app.mybotia.com             → /var/www/html/mybotia/public (webchat)
    │   ├── client.mybotia.com          → localhost:3001 (admin Express)
    │   ├── admin.mybotia.com           → localhost:3001 (admin Express)
    │   ├── lucy.mybotia.com            → localhost:18795 (gateway Lucy, auth Basic)
    │   ├── voice.mybotia.com           → localhost:3100 (Voice POC)
    │   ├── prospection.mybotia.com     → localhost:3000 (Docker)
    │   ├── listmonk.mybotia.com        → localhost:9000 (Docker)
    │   ├── crm.mybotia.com             → CRM Twenty
    │   └── WebSocket /ws              → localhost:18789 (gateway mybotia)
    │
    ├── Nginx (9090) ── Chat legacy
    │   └── /var/www/chat-maboitedigitale/index.html → ws://localhost:18789
    │
    └── Gateways OpenClaw (loopback 127.0.0.1)
        ├── :18789 — mybotia (7 agents, WhatsApp + Telegram + WebSocket)
        ├── :18790 — vlmedical (3 agents, WhatsApp + Telegram + WebSocket)
        ├── :18795 — lucy (1 agent, WhatsApp + Telegram + WebSocket)
        └── :3100  — voice-poc (ElevenLabs TTS)
```

## Gateways OpenClaw

Toutes les gateways sont des **services systemd user** (JAMAIS Docker, JAMAIS nohup).

### Gateway MyBotIA (port 18789)
- **Config :** `~/.openclaw/openclaw.json`
- **Agents :** Léa (main), Oscar, Nina, Jacques, Julian, BullSage, Agent-RH
- **WhatsApp :** Baileys (numéro +33756968633 pour Léa, +33780956160 pour Nina)
- **Telegram :** 5 bots (@lea_admin_bot, @julian_expert_bot, @nina_coachdigital_bot, @oscar_coachdigital_bot, @jacques_it_bot)
- **WebSocket :** accepte connexions webchat via Apache reverse proxy
- **dmScope :** per-channel-peer (isolation sessions DM)
- **groupPolicy :** allowlist (23 groupes WhatsApp configurés)

### Gateway VL Medical (port 18790)
- **Config :** `~/.openclaw-vlmedical/openclaw.json`
- **Agents :** vlmedical-main (dispatch), vlmedical-admin (Max), vlmedical-commercial (Eva)
- **WhatsApp :** +33756928403 (Max)
- **Telegram :** 1 bot
- **sandbox :** mode all (Docker isolation)

### Gateway Lucy IGH (port 18795)
- **Config :** `~/.openclaw-lucy/openclaw.json`
- **Agents :** lucy
- **WhatsApp :** +33780973018
- **Phase :** Apprentissage (écoute, enregistre, n'intervient pas seule)

## Routing canal → agent

Les agents répondent selon le canal d'arrivée :
- **WhatsApp DM** → Agent lié au numéro
- **WhatsApp Groupe** → Agent configuré dans groupPolicy avec requireMention
- **Telegram** → Agent lié au bot token
- **WebSocket/Webchat** → Agent sélectionné par le token de session dans agents.json

## Frontend

### Webchat (mybotia.com)
- **Stack :** PHP + HTML/CSS/JS vanilla
- **Auth :** Token-based (agents.json) + email/password (SQLite DB)
- **Features :** Chat WebSocket, upload fichiers, voice client, CRM Notion, onboarding
- **Sous-domaines webchat :** *.mybotia.com (wildcard Apache) — chaque agent accessible via [prenom].mybotia.com

### Admin Dashboard (client.mybotia.com / admin.mybotia.com)
- **Stack :** Express.js (Node), port 3001
- **Features :** CRUD agents, wizard déploiement, CRM PostgreSQL, OAuth management, Notion sync

### Voice POC V2 (voice.mybotia.com)
- **Stack :** Express.js (Node) + Python (ElevenLabs TTS), port 3100
- **Features :** PWA, reconnaissance vocale, synthèse vocale ElevenLabs, WebSocket

## Sécurité

- Gateways bind sur loopback uniquement (127.0.0.1)
- Sandbox Docker pour les outils agents (mode non-main mybotia/lucy, mode all vlmedical)
- dmPolicy : allowlist sur tous les profils
- Elevated : uniquement +33652345180 (Gilles)
- SSL wildcard Let's Encrypt via Cloudflare DNS-01
- Apache trusted proxies configuré pour WebSocket
