# Credentials Index — Carte rapide

> Source : PostgreSQL `mybotia_crm` table `credentials`
> Commande : `python3 tools/get_credential.py <service> [clé]`
> Dernière mise à jour : 25 mars 2026

## IA & LLM

| Service | Clés | Usage |
|---------|------|-------|
| anthropic-api | api_key | Claude (principal) |
| anthropic-bullsage | api_key | Claude (Bullsage dédié) |
| deepseek | api_key | DeepSeek |
| google-ai | api_key | Google AI / Gemini |
| groq | api_key | Groq (Whisper STT, LLama) |
| groq-v2 | api_key | Groq v2 |
| manus | api_key | Manus AI |
| mistral | api_key | Mistral |
| openrouter | api_key | OpenRouter |
| openrouter-v2 | api_key | OpenRouter v2 |
| perplexity | api_key | Perplexity |
| xai-grok | api_key | xAI Grok |

## Infra & DevOps

| Service | Clés | Usage |
|---------|------|-------|
| openclaw-vps | gateway_token, oauth_token | OpenClaw gateway + OAuth |
| vps-ssh | password | SSH user gilles |
| aws | access_key_id, secret_access_key, account_id, root_password | AWS (SES, etc.) |
| cloudflare | api_token | DNS management |
| vercel | token | Déploiement sites |
| lws | api_key, client_id | Hébergeur VPS |
| github-admin | token | GitHub full access (no expiry) |
| github-team | token | GitHub repo+workflow |

## Communication

| Service | Clés | Usage |
|---------|------|-------|
| gmail-coachdigital | account, credentials_path, token_path | Email pro CDP |
| gmail-gilles | account, credentials_path, token_path | Email perso Gilles |
| gmail-lea | account, password, credentials_path, token_path | Email Léa |
| gmail-loolyyb | account, password | Email loolyyb |
| telegram-user | api_id, api_hash, 2fa_password | Telegram user API |
| slack | app_token, bot_token | Slack workspace |

## Business & Finance

| Service | Clés | Usage |
|---------|------|-------|
| qonto | iban, slug | Banque Qonto |
| notion | api_key | CRM, bases clients |
| crm-coachdigital | url, password | CRM Vercel |
| godaddy | api_key, api_secret | Domaines clients |
| mybotia-admin | api_key | Admin MVP API |

## Outils & APIs

| Service | Clés | Usage |
|---------|------|-------|
| brave-search | api_key | Recherche web |
| elevenlabs | api_key, voice_id | TTS (backup, on utilise edge-tts) |
| piste | api_key, client_id, client_secret | Légifrance, Judilibre, BOAMP |

## Bullsage (crypto/finance)

| Service | Clés |
|---------|------|
| bullsage | mongo_url, password |
| bullsage-alphavantage | api_key |
| bullsage-cron | api_key |
| bullsage-deribit | client_id, client_secret |
| bullsage-finnhub | api_key |
| bullsage-fred | api_key |
| bullsage-jwt | secret |
| bullsage-marketaux | api_key |
