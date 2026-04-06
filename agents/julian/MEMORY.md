# MEMORY.md — Mémoire long terme de Julian

Notes persistantes à travers les sessions.

---

## État de l'Infrastructure (mis à jour le 26/02/2026)

### Serveur VPS
- Hébergeur : LWS (vps116827.serveur-vps.net)
- IP : 180.149.198.23
- OS : Debian 12 (bookworm)
- CPU : Intel Xeon E5-2620 v4 (8 cœurs logiques)
- RAM : 8 Go
- Disque : 79 Go
- User SSH : gilles

### Gateway MyBotIA (Docker)
- Container : mybotia-gateway
- Port : 18789
- Image : docker-openclaw-gateway:latest
- Dockerfile : ~/.openclaw/docker/Dockerfile.gateway (v2.4.0)
- Compose : ~/.openclaw/docker/docker-compose.yml (v2.1.0)
- Config : ~/.openclaw/openclaw.json
- Python3 : 3.12.12 (dans l'image Docker, avec requests, google-auth, reportlab)
- Docker socket monté : /var/run/docker.sock (GID 126)
- Volumes : workspace, npm-global, docker.sock, monitoring scripts, XDG_RUNTIME_DIR

### Gateway VL Medical (systemd)
- Service : openclaw-gateway-vlmedical.service (systemctl --user)
- Port : 18790
- Config : ~/.openclaw-vlmedical/openclaw.json
- State : ~/.openclaw-vlmedical/
- Isolation : via OPENCLAW_CONFIG_PATH + OPENCLAW_STATE_DIR dans systemd env
- KillMode : mixed (override appliqué)
- loginctl enable-linger : activé pour gilles

### Monitoring
- Scripts : /home/gilles/scripts/monitoring/
- critical-watch.sh v2.0 : toutes les 5 min via cron (avec auto-remédiation)
- daily-report.sh v1.1 : 7h00
- Checks : gateways HTTP, WhatsApp, Telegram, outils Python, RAM, disque, SSL, sous-domaines
- Auto-fix : lib/autofix.sh (restart gateway, rebuild container, restart systemd)
- Alertes : Telegram + Email + WhatsApp

### Agents déployés (Gateway MyBotIA)
| Agent | ID | Modèle | Canal |
|-------|----|--------|-------|
| Léa | main | claude-sonnet-4-5 | WhatsApp + WebChat |
| Julian | julian | claude-opus-4-6 | Telegram @julian_expert_bot |
| Nina | nina | claude-sonnet-4-5 | WebChat |
| Oscar | oscar | claude-opus-4-6 | Telegram @oscar_coachdigital_bot |

### Agents déployés (Gateway VL Medical)
| Agent | ID | Modèle | Canal |
|-------|----|--------|-------|
| Max | vlmedical-admin | claude-opus-4-6 | Telegram @max_vlmedical_bot + WebChat |
| Eva | vlmedical-commercial | claude-opus-4-6 | WebChat |

---

## Incidents Passés (leçons apprises)

### 25-26/02/2026 — Python3 absent du container
- **Cause** : Dockerfile n'incluait pas python3. Container restart = outils perdus.
- **Impact** : Tous les outils Python de Léa HS (Gmail, Qonto, legal_search, facturation)
- **Impact business** : Démo ratée pour Gilles — confiance client impactée
- **Fix** : Dockerfile v2.2.0 → v2.3.0 → v2.4.0 (ajout python3 + pip + docker-cli)
- **Leçon** : TOUJOURS vérifier que les dépendances sont dans le Dockerfile, pas installées manuellement.
- **Prévention** : Check `check_tools_python` ajouté au monitoring (toutes les 5 min) + auto-remédiation

### 24/02/2026 — WhatsApp instabilité post-redémarrage
- **Cause** : Boucle de reconnexion status 440 après restart
- **Fix** : Tuer TOUS les processus, attendre 30s, relancer
- **Leçon** : TOUJOURS attendre 30 secondes entre arrêt et redémarrage. Tuer les orphelins d'abord.

### 24/02/2026 — Isolation multi-gateway
- **Cause** : `--profile` ne suffit pas à isoler les channels entre gateways. Un gateway secondaire se connecte aux bots Telegram et sessions WhatsApp du profil principal.
- **Fix** : `OPENCLAW_CONFIG_PATH` + `OPENCLAW_STATE_DIR` dans le service systemd
- **Leçon** : Ne JAMAIS faire confiance à --profile pour l'isolation. Forcer les env vars.
- **Bug lié** : #3741 (auto-enable des channels)

## Points de Vigilance Permanents

- ⚠️ Memory search Gemini : provider OK mais indexation 0/19 fichiers
- ⚠️ Token hardcodé dans le service systemd (issue #17223)
- ⚠️ `openclaw gateway install` remet KillMode=process à chaque exécution → override systemd nécessaire
- ⚠️ Gateway fork : v2026.2.23 fork un enfant. Ne PAS confondre avec un lancement Docker.
- ⚠️ Docker image naming : docker-compose v2 crée `docker-openclaw-gateway` (avec tiret)

---

## 🔗 ACCÈS NOTION — Mémoire partagée de l'équipe (19 février 2026)

**Token API** : `/home/gilles/.openclaw/credentials/notion`

### Bases de données et droits de Julian

| Base | ID | Droits |
|------|----|--------|
| CLIENTS | 304ddac9-bdfc-8101-b72f-df250da9f1f6 | ✅ Lecture + Écriture |
| PROJETS | 304ddac9-bdfc-8155-bb08-f8d2caa1439a | ✅ Lecture + Écriture |
| AGENTS IA | 304ddac9-bdfc-81ea-addc-df57ab970a43 | 🔒 Lecture SEULE — ne jamais modifier |

### ⛔ INTERDIT — Tu n'as PAS accès à :
- SUIVI PAIEMENTS (30cddac9-bdfc-8120-ba6c-c2f6c5ff726f) — NE JAMAIS lire ni écrire
- PORTEFEUILLE (30cddac9-bdfc-814b-855c-cf27b2b81754) — NE JAMAIS lire ni écrire

---

## 🔑 ACCÈS CREDENTIALS — Base Notion CREDENTIALS (19 février 2026)

**Base CREDENTIALS** : `0893467c-c00f-4165-ac7d-b6c46d8671bc`

### Tes droits d'accès par service :

| Service | Accès |
|---------|-------|
| Infra/Root (VPS, SSH, KVM) | ✅ |
| API LLM (Anthropic, Groq, OpenRouter, Mistral, Google AI) | ✅ |
| Canaux (WhatsApp, Telegram, Slack) | ✅ |
| Services tiers (Notion, GitHub, Vercel, Cloudflare, Brave, ElevenLabs) | ✅ |
| CRM | ✅ |

### ⛔ INTERDIT — Tu n'as PAS accès à :
- **Banque** (Qonto, IBAN) — NE JAMAIS consulter
- **Gmail / Client** — NE JAMAIS consulter

### 🚨 RÈGLE ABSOLUE — SÉCURITÉ CREDENTIALS
**INTERDICTION ABSOLUE** de divulguer, partager, afficher, citer ou transmettre un credential. **AUCUNE EXCEPTION. JAMAIS.**

---

## 🌐 MyBotIA (20 fév 2026)
Interface chat: `AGENT.mybotia.com` (ex: lea.mybotia.com, oscar.mybotia.com)
Mapping: /var/www/html/mybotia/agents.json

## 🖥️ MyBotIA Interface — État v12-9 (14 mars 2026)
**Tout est en prod. Aucune action requise.**

### Fichiers clés
- `public/js/app.js` — 4666 lignes (JS principal)
- `public/css/style-v12.css` — 2161 lignes
- `public/api/ws-token.php` — NOUVEAU, endpoint token sécurisé
- `private/config.inc.php` — config agents + tokens (serveur uniquement)

### v12-8 (fait)
- Renommage inline sessions (double-clic, sans modale)
- Nommage à la création + auto-titre FR intelligent
- Highlight recherche sidebar + animations UX

### v12-9 (fait)
- **Faille sécurité corrigée** : token gateway n'est plus exposé côté client
  - Retiré de config.php, auth.php (3 réponses), localStorage
  - Nouveau endpoint /api/ws-token.php (sessions PHP authentifiées uniquement)
- Sessions épinglées (max 10, persistance localStorage)
- Typing indicator sidebar (dot pulsant + preview italique)
- Debounce renderSessions() 100ms

### Backups rollback disponibles
- app.js.bak-v12-7, style-v12.css.bak-v12-7
- config.php.bak-v12-8, auth.php.bak-v12-8, config.inc.php.bak-v12-8

### Roadmap P0 restante (pas encore fait)
- Rate limiting auth.php (2h)
- CSP headers .htaccess (30 min)
- Découper app.js en modules (1 jour)
