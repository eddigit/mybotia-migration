# MEMORY.md — Mémoire Opérationnelle d'Oscar

## État de l'Infrastructure (mis à jour le 26/02/2026)

### Serveur VPS
- Hébergeur : LWS (vps116827.serveur-vps.net)
- IP : 180.149.198.23
- OS : Debian 12
- CPU : 8 cœurs logiques
- RAM : 8 Go
- Disque : 79 Go

### Gateway MyBotIA (Docker)
- Container : mybotia-gateway
- Port : 18789
- Image : docker-openclaw-gateway:latest (380MB, rebuild 26/02 avec Python3)
- Dockerfile : ~/.openclaw/docker/Dockerfile.gateway (v2.3.0)
- Compose : ~/.openclaw/docker/docker-compose.yml
- Config : ~/.openclaw/openclaw.json
- Python3 : 3.12.12 (installé dans l'image Docker)

### Gateway VL Medical (systemd)
- Service : openclaw-gateway-vlmedical.service
- Port : 18790
- Config : ~/.openclaw-vlmedical/openclaw.json
- State : ~/.openclaw-vlmedical/

### Monitoring
- Scripts : /home/gilles/scripts/monitoring/
- Cron critical-watch : toutes les 5 minutes
- Cron daily-report : 7h00
- Alertes : Telegram + Email + WhatsApp
- Checks : gateways HTTP, WhatsApp, Telegram, RAM, disque, SSL, sous-domaines, outils Python

## Incidents Passés (leçons apprises)

### 25-26/02/2026 — Python3 absent du container
- **Cause** : Dockerfile n'incluait pas python3. Container restart = outils perdus.
- **Impact** : Tous les outils Python de Léa HS (Gmail, Qonto, legal_search, facturation)
- **Fix** : Dockerfile v2.2.0 → v2.3.0 (ajout python3 + pip + dépendances)
- **Leçon** : TOUJOURS vérifier que les dépendances sont dans le Dockerfile, pas installées manuellement.
- **Prévention** : Check `check_tools_python` ajouté au monitoring (toutes les 5 min)

### 24/02/2026 — WhatsApp instabilité post-redémarrage
- **Cause** : Boucle de reconnexion status 440 après restart
- **Fix** : Tuer TOUS les processus, attendre 30s, relancer
- **Leçon** : TOUJOURS attendre 30 secondes entre arrêt et redémarrage

### 24/02/2026 — Isolation multi-gateway
- **Cause** : `--profile` ne suffit pas à isoler les channels entre gateways
- **Fix** : `OPENCLAW_CONFIG_PATH` + `OPENCLAW_STATE_DIR` dans le service systemd
- **Leçon** : Ne JAMAIS faire confiance à --profile pour l'isolation

## Points de Vigilance Permanents

- ⚠️ Memory search Gemini : provider OK mais indexation 0/19 fichiers
- ⚠️ Token hardcodé dans le service systemd (issue #17223)
- ⚠️ `openclaw gateway install` remet KillMode=process à chaque exécution
- ⚠️ Gateway fork : le v2026.2.23 fork un enfant. Ne PAS confondre avec un lancement Docker.
