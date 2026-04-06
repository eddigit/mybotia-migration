# MEMORY.md — Mémoire long terme

## Contexte
Léa - Directrice Admin & Juridique, Coach Digital Paris. Bras droit de Gilles sur le VPS 24/7.

## 🔴 RÈGLES CRITIQUES
- **NOTION D'ABORD** : Chercher dans Notion AVANT les fichiers locaux
- **QONTO D'ABORD** : À chaque point financier, croiser Qonto avec l'admin MVP, rapprocher chaque virement
- **ANTI-FUITE** : JAMAIS de texte avant un appel outil (le gateway envoie tout en message)
- **ANTI-GRATUIT** : JAMAIS proposer de solutions gratuites/alternatives aux clients

## 📨 ENVOYER UN MESSAGE WHATSAPP — TEXTE
```bash
openclaw gateway call send \
  --token 67085f007e934ad258db36616d4797d3d3ec916cafef7d44 \
  --url ws://127.0.0.1:18789 \
  --params '{"channel":"whatsapp","to":"JID","message":"TEXTE","idempotencyKey":"clé-unique"}' \
  --json
```
- DM : `33XXXXXXXXX@s.whatsapp.net` | Groupe : `120363...@g.us`
- Champ = **"message"** (pas "text" ni "body")

## 🎤 ENVOYER UN VOCAL WHATSAPP
```bash
scripts/voice-reply-wa.sh "texte" "+33XXXXXXXXX"
```
- Ou manuellement : `OPENCLAW_GATEWAY_TOKEN=... openclaw message send --channel whatsapp --target "+33..." --media "fichier.ogg"`
- ⚠️ `gateway call send` = texte UNIQUEMENT. Médias/vocaux → `openclaw message send --media`
- ⚠️ Fichiers dans `~/.openclaw/workspace/media/` (PAS /tmp → LocalMediaAccessError)
- Voix : ElevenLabs voice_id=WeAAwKYcS06VmXw086yZ (eleven_multilingual_v2), fallback edge-tts Vivienne

## 🔗 NOTION — Bases & Accès
| Base | ID |
|------|----|
| CLIENTS | 304ddac9-bdfc-8101-b72f-df250da9f1f6 |
| PROJETS | 304ddac9-bdfc-8155-bb08-f8d2caa1439a |
| PAIEMENTS | 30cddac9-bdfc-8120-ba6c-c2f6c5ff726f |
| PORTEFEUILLE | 30cddac9-bdfc-814b-855c-cf27b2b81754 |
| AGENTS IA | 304ddac9-bdfc-81ea-addc-df57ab970a43 (lecture seule) |
| CREDENTIALS | 0893467c-c00f-4165-ac7d-b6c46d8671bc |
| PLANNING | 310ddac9-bdfc-816d-93a8-cfd2eba110f2 |

Token : `/home/gilles/.openclaw/credentials/notion`
Script client : `/home/gilles/.openclaw/scripts/notion-add-client.sh "Nom" "JID@g.us" "Type"`

## 🔴🔴 VOCABULAIRE — NE PLUS CONFONDRE (3 avril 2026)
| Terme | C'est quoi | URL | Port | BDD |
|-------|-----------|-----|------|-----|
| **CRM** | MyBotIA CRM (fork Twenty) | crm.mybotia.com | 3002 | PostgreSQL port 5433 |
| **MVP Admin** | Dashboard admin interne | admin.mybotia.com | 3001 | PostgreSQL port 5432 |

- Quand Gilles dit "CRM" → crm.mybotia.com (Twenty, GraphQL)
- Quand Gilles dit "admin" ou "MVP" → admin.mybotia.com (API REST)
- CE SONT DEUX BASES SÉPARÉES. Un ajout dans l'un N'APPARAÎT PAS dans l'autre.
- Nouveau client → L'AJOUTER DANS LES DEUX.

## 🏢 CRM MyBotIA — crm.mybotia.com (fork Twenty)
- **API GraphQL** : `http://127.0.0.1:3002/graphql`
- **Token API** : `python3 tools/get_credential.py twenty-crm api_key`
- **Workspace ID** : `16fc94e7-130b-41eb-ac7d-f7f682897ac0`
- **Workspace schema** : `workspace_1czoiv1m6luu6pvhlwdcix8e8`
- **Docker** : `/home/gilles/twenty-crm/docker-compose.yml` (image: `twentycrm/twenty:latest`)
- **Branding** : script `/home/gilles/twenty-crm/brand-patch.sh`
- **Schéma complet** : `projects/mybotia-crm/CRM-SCHEMA.md`
- **Objets** : Company, Person, Opportunity, Note, Task
- **Champs custom** : statutClient, agentAssigne, jidWhatsapp, siret, iban, forfaitMensuel, gatewayPort, urlWebchat
- **Adresse** : `address: { addressCity, addressPostcode, addressCountry, addressStreet1 }`
- **Nom personne** : `name: { firstName, lastName }`
- **Téléphone** : `phones: { primaryPhoneNumber }`
- **Pipeline** : NEW → SCREENING → MEETING → PROPOSAL → CUSTOMER
- **Montants** : en micros (÷ 1 000 000)

## 🏦 MVP ADMIN — admin.mybotia.com
- URL : `http://127.0.0.1:3001/api/agent/`
- Key : `0d4ebb779ab550255e1f39f3384d22816bdd58e3b7d6a92780ceded81688c5d3`
- Endpoints : /briefing, /morning, /tasks, /tasks/today, /clients, /pipeline, /paiements, /alerts, /search

## 💰 FACTURATION
- Script : `tools/generate_invoice.py`
- Template V3 validé
- Bénéficiaire = "Gilles Korzec" (PAS "Coach Digital")
- Output : `factures/`

## 🌐 MyBotIA
- DNS wildcard `*.mybotia.com` → 180.149.198.23
- SSL wildcard Let's Encrypt (expire 21 mai 2026)
- Interface : `/var/www/html/mybotia/v12-4.html`
- Config critique : `gateway.trustedProxies`, `allowedOrigins`, `dangerouslyDisableDeviceAuth: true`

## 📧 PROSPECTION
- Dashboard : https://prospection.mybotia.com/ (gilles/Gilles-Prosp2026!)
- Listmonk : https://listmonk.mybotia.com/admin/ (admin/Listmonk-Admin2026!)
- 35 000 contacts avocats | Domaine : prisedecontacts.com | SES sandbox 200/jour

## 🤖 JACQUES — SRE VPS (programme SRE depuis 29/03/2026)
- **Mode proactif** : anticiper → prévenir → documenter
- Crontab consolidée :
  - `gateway-watchdog.sh` */2 min (SLO tracker + health + WhatsApp + système + SSL)
  - `watchdog/run.sh` */15 min (analyse intelligente Claude Code)
  - `daily-report.sh` 7h (checks + SLO compliance + veille OpenClaw)
  - `sre-weekly.sh` lundi 7h15 (rapport hebdo SRE)
  - `ram-alert.sh` et `critical-watch.sh` → DÉSACTIVÉS (consolidés dans gateway-watchdog)
- SLO : MyBotIA 99.9%, VL Medical 99.5%, Lucy/IGH 99%, Léa/Nina WA 99%
- Alertes Telegram : @jacques_it_bot + @julian_expert_bot
- Chat ID Gilles : 1801835052
- Fichiers SRE clés : `~/watchdog/SLO.md`, `~/watchdog/state/slo-tracker.json`, `~/watchdog/.claude/skills/sre-mybotia/SKILL.md`

## 🤖 ABONNEMENTS CLAUDE MAX
| Compte | Plan | Usage |
|--------|------|-------|
| coachdigitalparis@gmail.com | Max $200/mois | VPS OpenClaw (usage intensif) |
| gilleskorzec@gmail.com | Max $90/mois | Usage perso Gilles |

→ Pour le setup-token VPS : utiliser **coachdigitalparis@gmail.com** (plan $200)
→ Sur le Mac, vérifier quel compte est actif : `claude auth status`

## 🔑 VPS SSH — DÉFINITIF
- User : gilles
- Password : fPS9AH48olixmBey
- ⚠️ NE JAMAIS CHANGER SANS ORDRE EXPLICITE DE GILLES
- ⚠️ NE JAMAIS REMETTRE 557577 (ancien, non sécurisé)

## 🌐 OpenClaw — Version & Infra (29 mars 2026)
- **Version** : 2026.3.28 (latest stable, mode HOST)
- **Node.js** : v22.22.0
- **Gateways** : MyBotIA (18789) ✅, VL Medical (18790) ✅, Lucy/IGH (18795) ✅
- **Fixes importants embarqués** : #54570 (multi-reply Léa), #56612 (NO_REPLY), #53624 (groups echo dedup), #53940 (restart sentinel)
- voice-poc : DÉSACTIVÉ (crash loop, zéro trafic prod)

## 🔐 SSH VPS (29 mars 2026)
- Clé SSH ED25519 "vps-gilles" opérationnelle (Mac via Termius)
- Password auth SSH : **actif temporairement** (en attente clé iPhone — sync Termius impossible sur plan Starter)
- Bitwarden : 4 clés SSH documentées

## 🔐 TOKENS ANTHROPIC — NE JAMAIS TOUCHER (3 avril 2026)
- **INTERDIT** de modifier `~/.claude/.credentials.json`
- **INTERDIT** de restaurer des backups de credentials
- **INTERDIT** de toucher aux tokens OAuth Anthropic
- Le token qui marche passe via `CLAUDE_CODE_OAUTH_TOKEN` en variable d'env
- Pour lancer Claude Code : `CLAUDE_CODE_OAUTH_TOKEN="<ANTHROPIC_OAUTH_TOKEN_TRUNCATED>" claude --permission-mode bypassPermissions --print "prompt"`
- IL Y A 2 TOKENS, 2 COMPTES. ILS SONT BONS. ON LES TOUCHE PLUS. POINT FINAL.

## ⚠️ PROBLÈMES CONNUS (29 mars 2026)
- MEMORY.md tronqué si >20 000 chars → infos perdues en fin de fichier
- Webchat : erreurs "missing scope: operator.read" en boucle toutes les 60s
- Max WhatsApp : LOGGED_OUT depuis 5 mars (attente re-pairing Jean-Luc)
- Password auth SSH actif temporairement
- Bug #44467 delivery-mirror toujours ouvert upstream
- ✅ RÉSOLU : 3 gateways zombies nettoyées (upgrade 29/03)
- ✅ RÉSOLU : Swap 49.3% → maintenant 0%
- ✅ RÉSOLU : Faux positifs monitoring WhatsApp (patterns corrigés)

## 🔧 GIT & VERCEL — RÈGLE DÉPLOIEMENT (30 mars 2026)
- **Vercel Hobby** = 1 seul seat → l'auteur git DOIT être le propriétaire Vercel
- **Tous les repos eddigit** déployés sur Vercel :
  - `user.name` = `Gilles KORZEC`
  - `user.email` = `gilleskorzec@gmail.com`
- ❌ NE PLUS UTILISER : `Coach Digital Paris` / `coachdigitalparis@gmail.com` / `Co-Authored-By`
- **Process prod** : Claude Code = dev/brouillon → Léa = push en production
- Commit via API GitHub : `POST /repos/eddigit/{repo}/git/commits` + `PATCH /git/refs/heads/main`

## 📝 INFOS CLIENTS → voir memory/clients/*.md
Tous les détails clients sont dans les fichiers dédiés, pas ici.
