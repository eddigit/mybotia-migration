# TOOLS.md — Outils de Julian

## Outils Ops (Infrastructure)

### 1. health_check.py — Diagnostic complet de l'infrastructure
```bash
python3 tools/health_check.py          # Check complet
python3 tools/health_check.py --quick   # Check rapide (gateways + WhatsApp)
python3 tools/health_check.py --json    # Sortie JSON pour parsing
```
Vérifie : gateways HTTP, WhatsApp, Telegram bots, Python dans container, RAM, disque, Docker, systemd, SSL, sous-domaines.

### 2. auto_fix.py — Remédiation automatique des pannes connues
```bash
python3 tools/auto_fix.py --check       # Diagnostic sans action
python3 tools/auto_fix.py --fix         # Diagnostic + correction automatique
python3 tools/auto_fix.py --fix --dry   # Simulation (affiche les commandes sans exécuter)
```
Corrige : restart gateway, rebuild container, restart systemd, kill orphelins.

### 3. read_logs.py — Lecture des logs
```bash
python3 tools/read_logs.py docker 50            # 50 dernières lignes Docker mybotia-gateway
python3 tools/read_logs.py systemd 30           # 30 dernières lignes systemd VL Medical
python3 tools/read_logs.py monitoring 20        # 20 dernières lignes monitoring
python3 tools/read_logs.py autofix 20           # 20 dernières lignes autofix
python3 tools/read_logs.py apache 30            # 30 dernières lignes Apache
python3 tools/read_logs.py docker 50 --errors   # Filtrer les erreurs uniquement
```

### 4. Exec (shell)
Accès shell direct pour diagnostics avancés.
**Autorisé** : commandes de lecture (docker ps, curl, free, df, ps, cat logs, systemctl status)
**Interdit sans validation CEO** : rm, kill (processus principaux), apt install, config changes

## Outils Externes

- **Brave Search** — recherche web (doc OpenClaw, bugs GitHub, etc.)
- **Telegram** — canal de communication avec Gilles (@julian_expert_bot)

## Commandes de Diagnostic Essentielles

```bash
# Vérifier la version installée
openclaw --version

# Diagnostic complet OpenClaw
openclaw doctor
openclaw doctor --fix

# État de santé du gateway
openclaw health

# Statut actuel
openclaw status

# Journaux
openclaw logs
openclaw logs --follow

# Redémarrage gateway
openclaw gateway restart

# Docker
docker ps --filter name=mybotia-gateway
docker logs mybotia-gateway --tail 50
docker exec mybotia-gateway python3 --version

# Systemd (VL Medical)
systemctl --user status openclaw-gateway-vlmedical
journalctl --user -u openclaw-gateway-vlmedical --no-pager -n 30

# Système
free -m
df -h
ps aux --sort=-%mem | head -10
```

## Notes Environnement

### SSH
- VPS production : 180.149.198.23, user gilles

### Chemins clés
- Config MyBotIA : ~/.openclaw/openclaw.json
- Config VL Medical : ~/.openclaw-vlmedical/openclaw.json
- Dockerfile : ~/.openclaw/docker/Dockerfile.gateway
- Docker Compose : ~/.openclaw/docker/docker-compose.yml
- Monitoring : /home/gilles/scripts/monitoring/
- Apache vhosts : /etc/apache2/sites-available/
- Workspace Julian : ~/.openclaw/workspace-julian/
- Workspace Oscar : ~/.openclaw/workspace-oscar/
