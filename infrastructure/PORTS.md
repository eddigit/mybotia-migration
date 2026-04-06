# Ports & Services — VPS MyBotIA

## Services systemd user (Gilles)

| Service | Port | Description |
|---------|------|-------------|
| openclaw-gateway.service | 18789 | Gateway MyBotIA (7 agents) |
| openclaw-gateway-vlmedical.service | 18790 | Gateway VL Medical (3 agents) |
| openclaw-gateway-lucy.service | 18795 | Gateway Lucy IGH (1 agent) |
| voice-poc.service | 3100 | Voice POC V2 (ElevenLabs) |
| admin-dashboard.service | 3001 | Admin panel Express.js |
| jacques-telegram.service | — | Jacques IT daemon Telegram |

## Docker containers

| Container | Port | Description |
|-----------|------|-------------|
| prospection_dashboard | 127.0.0.1:3000 | Dashboard prospection |
| prospection_listmonk | 127.0.0.1:9000 | Emailing Listmonk |
| prospection_postgres | 127.0.0.1:5432 | PostgreSQL + pgvector |
| twenty-crm-* | 127.0.0.1:3002 | CRM Twenty |
| openclaw-sbx-agent-* | — | Sandbox Docker agents |

## Services système

| Service | Port | Description |
|---------|------|-------------|
| Apache | 80, 443 | Reverse proxy + sites web |
| Nginx | 9090 | Chat websocket legacy |
| Redis | 6379 | Cache |
| MySQL | 3306 | Bases ISPConfig |
| Postfix/Dovecot | 25, 993 | Mail |
| MeshCentral | 8443 | Support remote |
| Bind DNS | 53 | DNS local |
