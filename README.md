# MyBotIA — Migration vers Emergent

**Organisation :** Coach Digital Paris (MaBoiteIA)
**Date :** Avril 2026
**Objectif :** Migration complète de l'infrastructure MyBotIA depuis le VPS vers la plateforme Emergent (emergent.sh)

## Qu'est-ce que MyBotIA ?

MyBotIA est une plateforme SaaS de **collaborateurs IA** (agents conversationnels) déployés sur WhatsApp, Telegram et webchat. Chaque agent possède un "cerveau" (SOUL.md), des outils, une mémoire et des canaux de communication.

## Stack technique actuelle

- **OS :** Debian 12 (Bookworm) — VPS LWS
- **Runtime :** Node.js 22.22.0
- **Gateway :** OpenClaw 2026.4.2 (gateways WhatsApp/Telegram via Baileys + grammy)
- **LLM :** Claude Opus 4.6 / Sonnet 4.6 (via tokens OAuth Anthropic)
- **Frontend webchat :** PHP + HTML/CSS/JS (vanilla, pas de framework SPA)
- **Admin panel :** Express.js (Node)
- **Voice :** Express + ElevenLabs (Python TTS)
- **Reverse proxy :** Apache 2 + Nginx (chat websocket)
- **Base de données :** SQLite (webchat), PostgreSQL (CRM)
- **SSL :** Let's Encrypt wildcard via Cloudflare DNS-01

## Les 11 agents

| Agent | Modèle | Rôle | Canaux |
|-------|--------|------|--------|
| **Léa** (main) | Opus 4.6 | Admin, juridique, orchestration | WhatsApp, Telegram, Webchat |
| **Oscar** | Opus 4.6 | Prospection commerciale | WhatsApp, Telegram, Webchat |
| **Nina** | Sonnet 4.5 | Communication, social media | WhatsApp, Telegram, Webchat |
| **Jacques** | Sonnet 4.5 | IT monitoring | Telegram |
| **Julian** | Opus 4.6 | Expert IT & technique | Telegram, Webchat |
| **BullSage** | Sonnet 4.5 | Finance, crypto | Webchat |
| **Agent-RH** | Sonnet 4.5 | Ressources humaines | Webchat |
| **Max** (VL Medical Admin) | Opus 4.6 | Agent principal VL Medical | WhatsApp, Telegram, Webchat |
| **Eva** (VL Medical Commercial) | Sonnet 4.5 | Commercial VL Medical | WhatsApp, Webchat |
| **Lucy** (IGH) | Sonnet 4.6 | Collaboratrice dédiée IGH (20 EHPAD) | WhatsApp, Telegram, Webchat |
| **VL Medical Main** | — | Routeur / agent de dispatch VL Medical | — |

## Architecture des gateways

| Gateway | Port | Agents | Config |
|---------|------|--------|--------|
| mybotia | 18789 | Léa, Oscar, Nina, Jacques, Julian, BullSage, Agent-RH | `gateways/mybotia/` |
| vlmedical | 18790 | VL Medical Main, Max, Eva | `gateways/vlmedical/` |
| lucy | 18795 | Lucy IGH | `gateways/lucy/` |
| voice-poc | 3100 | Voice POC V2 (ElevenLabs) | `frontend/voice/` |

## Structure du repo

```
agents/           → Cerveaux, outils, mémoire des 11 agents
gateways/         → Configs OpenClaw (sanitisées — pas de credentials)
frontend/
  webchat/        → Site mybotia.com (PHP + HTML/JS)
  admin/          → Dashboard admin Express.js (:3001)
  voice/          → Voice POC V2 (ElevenLabs)
scripts/          → Scripts monitoring/maintenance
infrastructure/   → Documentation DNS, ports, services, credentials
```

## Credentials

Les valeurs des credentials ne sont PAS dans ce repo. Voir `infrastructure/CREDENTIALS_INVENTORY.md` pour l'inventaire complet. Les valeurs seront transmises séparément via un canal sécurisé.

## Pourquoi migrer vers Emergent ?

1. **Fin tokens OAuth Anthropic** → passage API payante, Emergent propose des tarifs LLM plus compétitifs
2. **Maintenance infra insoutenable** → bugs Baileys, reconnexion WhatsApp, auto-repair, crons = temps perdu
3. **Emergent gère tout** → hébergement, LLM multi-provider, gateways (Twilio Business API), monitoring
4. **Objectif** → VPS allégé (ne garde que sites hébergés), tout le reste chez Emergent
