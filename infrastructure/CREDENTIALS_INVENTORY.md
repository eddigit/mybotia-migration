# Coffre-Fort Credentials — Inventaire pour migration Emergent

> **Les VALEURS ne sont PAS dans ce repo.** Elles seront transmises via canal sécurisé.

## Tokens LLM

| Service | Type | Utilisé par | Localisation actuelle |
|---------|------|-------------|----------------------|
| Anthropic (gilleskorzec@gmail.com) | OAuth Token | Tous agents (priorité 1) | ~/.openclaw-tokens-vault.json |
| Anthropic (coachdigitalparis@gmail.com) | OAuth Token | Tous agents (fallback) | ~/.openclaw-tokens-vault.json |
| Groq | API Key | Fallback LLM (Llama 3.3 70B) | ~/.openclaw-tokens-vault.json |

## Telegram Bot Tokens

| Bot | Utilisé par | Config |
|-----|-------------|--------|
| @lea_admin_bot | Léa | openclaw-mybotia.json |
| @julian_expert_bot | Julian | openclaw-mybotia.json |
| @nina_coachdigital_bot | Nina | openclaw-mybotia.json |
| @oscar_coachdigital_bot | Oscar | openclaw-mybotia.json |
| @jacques_it_bot | Jacques | openclaw-mybotia.json + scripts monitoring |
| Bot VL Medical | Max | openclaw-vlmedical.json |
| Bot Lucy | Lucy | openclaw-lucy.json |

## APIs & Services

| Service | Type | Utilisé par | Fichier .env |
|---------|------|-------------|-------------|
| Notion API | Integration Token | Léa, Max, Admin dashboard, Sync scripts | apps/admin/.env, agents tools |
| ElevenLabs | API Key | Voice POC V2 | apps/voice-poc/.env |
| Brave Search | API Key | Agents avec web_search | openclaw.json (tools config) |
| Cloudinary | Cloud credentials | Upload images (Léa, Lucy) | Agents tools (get_credential.py) |
| Google Gmail | OAuth Client + Tokens | Léa (envoi emails) | workspace/tools/gmail-*.json |
| Google Calendar | OAuth Token | Léa | Même credentials Gmail |
| Pennylane | API Token | Léa (facturation) | Via get_credential.py |
| Qonto | API Token | Léa (banque) | Via get_credential.py |

## Base de données

| Service | Type | Utilisé par | Localisation |
|---------|------|-------------|-------------|
| PostgreSQL (mybotia_crm) | User/Password | Admin dashboard, CRM, Sync | apps/admin/.env, webchat/private/env.php |
| SQLite (mybotia.db) | Fichier | Webchat auth/sessions | /var/www/html/mybotia/private/ |

## WhatsApp

| Élément | Notes |
|---------|-------|
| Session credentials (creds.json) | Non transférable — QR code requis à chaque nouveau device |
| Numéros : +33756968633, +33780956160, +33756928403, +33780973018 | À transférer vers Twilio Business API |

## Fichiers .env sur le VPS

| Fichier | Contenu principal |
|---------|------------------|
| ~/.openclaw/.env | Variables gateway mybotia |
| apps/admin/.env | PG, Notion, credentials admin |
| apps/voice-poc/.env | ElevenLabs API key |
| prospection/.env | Stack prospection (PG, Listmonk) |
| artroyal-api/.env | API ArtRoyal |

## Actions pour Emergent

1. Les credentials Anthropic seront remplacées par la clé universelle Emergent
2. Les tokens Telegram doivent être transférés tels quels
3. Les sessions WhatsApp Baileys sont NON transférables → re-pairing via Twilio
4. Les credentials Google (Gmail/Calendar) nécessitent un re-consentement OAuth
5. Notion, ElevenLabs, Brave, Cloudinary → transfert direct des API keys
