# Services & Crons — VPS MyBotIA

## Crons actifs (à la date du 6 avril 2026)

| Fréquence | Script | Rôle |
|-----------|--------|------|
| */2h | healthcheck-tools.sh | Vérification APIs, Python, Skills |
| 4h | backup-dr.sh | Backup DR chiffré + GitHub |
| 7h | daily-report.sh | Rapport quotidien Telegram |
| 7h | check-model-versions.sh | Alerte si modèle LLM obsolète |
| 7h | healthcheck-tools.sh | Check complet outils |
| */6h | check-memories.sh | Vérification mémoires agents |
| 8h | lucy-morning-briefing.sh | Briefing matinal Lucy |
| */1h | lucy-hourly-research.sh | Recherche sectorielle Lucy |
| */1h | sync-pg-to-notion.js | Sync CRM PG → Notion |
| Lundi 7h15 | sre-weekly.sh | Rapport SRE hebdomadaire |

### Crons désactivés (remplacés par auto-repair.sh)
- gateway-watchdog.sh (*/2min) → auto-repair.sh
- whatsapp-creds-pruner.sh (*/10min) → auto-repair.sh
- watchdog run.sh (*/15min) → auto-repair.sh
- critical-watch.sh (*/5min) → auto-repair.sh

## Watchdog Jacques

Jacques (ce repo) fonctionne en deux modes :
1. **CLI directe** — Claude Code en session interactive avec Gilles
2. **Cron watchdog** — Remplacé par auto-repair.sh pour la surveillance basique

## Monitoring

- **auto-repair.sh** : Script unifié de réparation automatique (restart gateways, pruning WhatsApp creds, health checks)
- **Alertes** : Via Telegram bot @jacques_it_bot → chat Gilles (ID 1801835052)
