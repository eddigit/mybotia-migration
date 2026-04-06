# AGENTS.md -- Cartographie Infrastructure & Procedures IT

## VPS -- Informations systeme
- Hostname : vps116827.serveur-vps.net
- IP : 180.149.198.23
- OS : Debian 13 (Trixie), Kernel 6.12.43
- RAM : 8 Go (swap 8 Go)
- Disque : 79 Go (/dev/zd112)
- User principal : gilles
- Hebergeur : LWS (identifiant client LWS-783705, panel sur panel.lws.fr)

## Versions en cours
- OpenClaw : 2026.3.2 (containers Docker, mis a jour 3 mars 2026)
- Node.js : 22.x
- Auth : OAuth uniquement (tokens sk-ant-oat01-), zero cle API sk-ant-api03-
- Claude Code (Jacques CLI) : 2.1.71

## Docker Containers
| Container | Image | Role | Ports |
|-----------|-------|------|-------|
| mybotia-gateway | docker-openclaw-gateway | Gateway principale (Lea, Julian, Nina, Oscar, Bullsage, Agent-RH) | 18789, 18791, 18792 |
| vlmedical-gateway | docker-openclaw-gateway-vlmedical | Gateway VL Medical (Max, Eva) | 18790, 18793 |
| prospection_dashboard | prospection-dashboard | Dashboard prospection | 127.0.0.1:3000 |
| prospection_listmonk | listmonk/listmonk:latest | Emailing prospection | 127.0.0.1:9000 |
| prospection_postgres | pgvector/pgvector:pg16 | BDD prospection + vectoriel | 127.0.0.1:5432 |

## Agents IA -- MyBotIA Gateway
| Agent | Modele | Role | Telegram |
|-------|--------|------|----------|
| main (Lea) | claude-opus-4-6 | Assistante principale | @lea_admin_bot |
| julian (TOI) | claude-opus-4-6 | IT & Technique | @julian_expert_bot |
| nina | claude-sonnet-4-5 | Communication | @nina_coachdigital_bot |
| oscar | claude-opus-4-6 | Prospection | @oscar_coachdigital_bot |
| bullsage | claude-sonnet-4-5 | Finance/crypto | - |
| agent-rh | claude-sonnet-4-5 | RH | - |

## Agents IA -- VL Medical Gateway
| Agent | Modele | Role |
|-------|--------|------|
| main (Max) | claude-opus-4-6 | Agent principal VL Medical |
| eva | claude-sonnet-4-5 | (workspace a finaliser) |

## Config critique des gateways
- MyBotIA : config dans ~/.openclaw/openclaw.json
- VL Medical : config dans ~/.openclaw-vlmedical/openclaw.json
- IMPORTANT pour VL Medical : les commandes OpenClaw necessitent les env vars :
  OPENCLAW_CONFIG_PATH=/home/gilles/.openclaw-vlmedical/openclaw.json
  OPENCLAW_STATE_DIR=/home/gilles/.openclaw-vlmedical
- heartbeat.directPolicy: "block" dans les deux gateways (breaking change 2026.3.2)

## Canaux de communication
- WhatsApp Lea : +33756968633
- WhatsApp Nina : +33780956160
- WhatsApp Max : +33756928403 -- LOGGED_OUT depuis 5 mars, QR re-scan requis
- Gmail : hook natif gmail-pubsub (s'arrete car pas de section hooks dans openclaw.json)

## Services annexes
- Admin Dashboard : port 3001 (Node.js, ~/apps/admin/server.js)
- Nginx : port 9090 (chat web), 80/443 (web)
- Redis : port 6379
- MySQL : port 3306
- Postfix/Dovecot : ports 25/465/587/993/995
- MeshCentral : port 8443/4433/4434
- DNS : port 53 (Bind)
- gog CLI v0.11.0 : Google services (coachdigitalparis@gmail.com, projet GCP: openclaw-gmail)

## Commandes de diagnostic (a executer dans les containers Docker)
```bash
# Health gateway
docker exec mybotia-gateway openclaw health
docker exec vlmedical-gateway openclaw health

# Health endpoint rapide
docker exec mybotia-gateway curl -s http://127.0.0.1:18789/healthz
docker exec vlmedical-gateway curl -s http://127.0.0.1:18790/healthz

# Etat OAuth
docker exec mybotia-gateway openclaw models status --check
docker exec vlmedical-gateway openclaw models status --check

# Cron jobs
docker exec mybotia-gateway openclaw cron status
docker exec mybotia-gateway openclaw cron list

# Logs internes gateway
docker exec mybotia-gateway openclaw logs --follow
docker exec vlmedical-gateway openclaw logs --follow

# Etat containers Docker
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# RAM + Swap
free -m
cat /proc/meminfo | grep -E "Mem|Swap"

# Disque
df -h /

# Logs Docker recents
docker logs mybotia-gateway --tail 30 --since 10m 2>&1
docker logs vlmedical-gateway --tail 30 --since 10m 2>&1
```

## Arborescence cle
```
/home/gilles/
|-- .openclaw/              # Config mybotia-gateway
|   |-- openclaw.json       # Config principale (NE PAS MODIFIER)
|   |-- docker/             # Docker compose gateway
|   |-- workspace/          # Workspace Lea
|   |-- workspace-julian/   # TON workspace (+ rapports Jacques)
|   |-- workspace-nina/
|   |-- workspace-oscar/
|   |-- workspace-bullsage/
|   |-- workspace-agent-rh/
|   +-- memory/
|-- .openclaw-vlmedical/    # Config VL Medical gateway
|-- watchdog/               # Jacques CLI (cron */15 min)
|   |-- CLAUDE.md
|   |-- prompt.txt
|   |-- run.sh
|   |-- .claude/skills/     # 3 skills monitoring
|   |-- logs/               # Logs quotidiens Jacques
|   +-- memory/MEMORY.md    # Memoire Jacques
|-- scripts/monitoring/     # Scripts monitoring bash
|-- apps/admin/             # Dashboard admin
+-- prospection/            # Stack prospection
```

## Cron existants sur le host
- */5 min : update-wa-contacts.py, critical-watch.sh
- Toutes les heures : healthcheck-tools.sh
- 3h : backup-config.sh
- 7h : daily-report.sh
- */15 min : Jacques CLI (analyse intelligente Claude Code)

## Actions autorisees en autonomie
- docker restart mybotia-gateway ou vlmedical-gateway (si unresponsive)
- docker system prune -f (si disque > 85%)
- kill process zombie
- Nettoyer logs > 100MB
- Redemarrer nginx si down

## Actions INTERDITES
- Modifier openclaw.json ou toute config applicative
- docker rm / docker stop definitif
- Modifier code source, credentials, nginx config
- Supprimer donnees utilisateur
- apt install/remove
- Mettre a jour OpenClaw (signaler a Gilles uniquement)

## Alertes Telegram
- Chat ID Gilles : 1801835052
- WhatsApp Gilles : +33652345180

## Bugs connus a ne PAS alerter
- gmail-watcher mort dans les logs = normal (pas de section hooks dans openclaw.json)
- stale-socket warnings = normal (reconnexion Telegram periodique)
- Brave 429 (rate limit) = normal si occasionnel
- announce-queue drain failed = bug gatewayToken connu, non bloquant
- OAuth "unknown expires unknown" = normal pour setup-token, pas une alerte