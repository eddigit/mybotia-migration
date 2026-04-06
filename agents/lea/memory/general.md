# Mémoire générale — Notes non liées à un client spécifique

## Avatar Nina (17 février 2026)
URL officielle :
```
https://res.cloudinary.com/dkvhbcuaz/image/upload/v1771341557/ChatGPT_Image_17_f%C3%A9vr._2026_16_14_37_qmyjlf.png
```
À utiliser partout : WhatsApp, CRM, signatures, profils, etc.

## Accès Notion — Mémoire partagée
- Token API : `/home/gilles/.openclaw/credentials/notion`
- Script ajout client : `/home/gilles/.openclaw/scripts/notion-add-client.sh "Nom" "JID@g.us" "Type"`

### Bases de données
| Base | ID | Droits |
|------|----|--------|
| CLIENTS | 304ddac9-bdfc-8101-b72f-df250da9f1f6 | Lecture + Écriture |
| PROJETS | 304ddac9-bdfc-8155-bb08-f8d2caa1439a | Lecture + Écriture |
| SUIVI PAIEMENTS | 30cddac9-bdfc-8120-ba6c-c2f6c5ff726f | Lecture + Écriture |
| PORTEFEUILLE | 30cddac9-bdfc-814b-855c-cf27b2b81754 | Lecture + Écriture |
| AGENTS IA | 304ddac9-bdfc-81ea-addc-df57ab970a43 | Lecture SEULE |

### Commandes API Notion
```bash
# Lire une base
curl -s -H "Authorization: Bearer $(cat /home/gilles/.openclaw/credentials/notion)" -H "Notion-Version: 2022-06-28" "https://api.notion.com/v1/databases/ID_BASE/query" -X POST -H "Content-Type: application/json" -d '{}'

# Ajouter un client
bash /home/gilles/.openclaw/scripts/notion-add-client.sh "Nom du client" "JID@g.us" "Premium"
```

## Accès Credentials — Base Notion
- Base CREDENTIALS : `0893467c-c00f-4165-ac7d-b6c46d8671bc`
- Data source : `bf954795-5d39-4200-a2ed-479f774d9917`

## Planning Hebdo — Base Notion
- Base ID : `310ddac9-bdfc-816d-93a8-cfd2eba110f2`
- URL : https://www.notion.so/310ddac9bdfc816d93a8cfd2eba110f2
- Chaque lundi matin : revue avec Gilles
- Template local : templates/planning-hebdo.md

## Système Facturation PDF
- Script : `tools/generate_invoice.py`
- Template V3 — design moderne épuré, photo Gilles en avatar rond
- Règle : Bénéficiaire = "Gilles Korzec" (PAS "Coach Digital")
- Output : `factures/` dans le workspace

## MyBotIA — Interface Chat Premium & PWA
- Sous-domaines : lea/oscar/julian/nina.mybotia.com
- app.mybotia.com/v11.html → Login générique
- Interface courante : `/var/www/html/mybotia/v12-4.html`
- Mapping agents : `/var/www/html/mybotia/agents.json`
- DNS wildcard *.mybotia.com → 180.149.198.23 (Cloudflare)
- SSL wildcard Let's Encrypt via DNS-01 + Cloudflare API (expire 21 mai 2026)
- Apache VHost : `/etc/apache2/sites-available/wildcard-mybotia-le-ssl.conf`

## Plateforme Prospection — prospection.mybotia.com (MàJ 9 mars 2026)
- Dashboard : https://prospection.mybotia.com/
- Config : /home/gilles/prospection/.env + docker-compose.yml
- 35 000 contacts avocats Paris importés
- Domaine d'envoi : prisedecontacts.com (Amazon SES, sandbox 200/jour)
- Règles : pas de nom/prénom en 1er envoi, uniquement via prisedecontacts.com

## Jacques — Watchdog IT (8 mars 2026)
- Cron */15 min, 9 checks, logs rotation 7 jours
- Alertes Telegram : @jacques_it_bot + @julian_expert_bot
- Chat ID Gilles : 1801835052
- Swap vigilance >70%

## OAuth Claude Code
- Setup-token déployé 8 mars 2026, expire 8 mars 2027
- Tokens séparés VPS/WSL2

## Config OpenClaw — Leçons
- tools.profile valides : minimal, coding, messaging, full
- groupPolicy valides : open, allowlist, disabled
- dmPolicy valides : pairing, allowlist, open, disabled
