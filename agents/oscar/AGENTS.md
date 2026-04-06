# AGENTS.md — Protocoles Opérationnels d'Oscar

> Dernière mise à jour : 26 février 2026
> Lis ce fichier en entier à chaque session.

---

## Protocole de Démarrage

1. Lis SOUL.md, IDENTITY.md, USER.md, MEMORY.md
2. Exécute un health check complet : `python3 tools/health_check.py`
3. Si des problèmes sont détectés, agis selon le runbook ci-dessous
4. Reporte le statut à Gilles si un problème est trouvé

---

## Architecture de Production

### Dual-Gateway

| | Gateway MyBotIA | Gateway VL Medical |
|--|----------------|-------------------|
| Port | 18789 | 18790 |
| Mode | Docker container (mybotia-gateway) | Systemd user service |
| Config | ~/.openclaw/openclaw.json | ~/.openclaw-vlmedical/openclaw.json |
| State dir | ~/.openclaw/ | ~/.openclaw-vlmedical/ |
| Agents | Léa, Julian, Nina, Oscar | Max, Eva |

### Réseau

```
Internet → *.mybotia.com (Apache vhost + SSL)
                ↓ ProxyPass
           127.0.0.1:18789 (MyBotIA — Docker)
           127.0.0.1:18790 (VL Medical — systemd)
```

---

## RUNBOOK — Pannes Connues et Remédiation

### PANNE 1 : Gateway MyBotIA DOWN (HTTP ≠ 200 sur port 18789)

**Diagnostic :**
```bash
docker ps --filter name=mybotia-gateway
docker logs mybotia-gateway --tail 30
```
**Fix :**
```bash
docker restart mybotia-gateway
# Attendre 30 secondes
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/health
```
**Vérification :** HTTP 200 sur /health
**Escalade si :** le restart ne résout pas après 2 tentatives

### PANNE 2 : Gateway VL Medical DOWN (HTTP ≠ 200 sur port 18790)

**Diagnostic :**
```bash
systemctl --user status openclaw-gateway-vlmedical
journalctl --user -u openclaw-gateway-vlmedical --no-pager -n 30
```
**Fix :**
```bash
systemctl --user restart openclaw-gateway-vlmedical
# Attendre 30 secondes
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18790/health
```
**Vérification :** HTTP 200 + systemctl active

### PANNE 3 : Python3 absent du container Docker

**Diagnostic :**
```bash
docker exec mybotia-gateway python3 --version
docker exec mybotia-gateway python3 -c "import requests, google.auth, reportlab"
```
**Fix :**
```bash
cd ~/.openclaw/docker && docker compose build --no-cache && docker compose up -d
```
**Vérification :** python3 --version + imports OK dans le container
**Note :** ce rebuild prend ~2 minutes. Léa sera indisponible pendant ce temps.
**Cause racine :** le Dockerfile doit TOUJOURS inclure python3 + pip + dépendances

### PANNE 4 : WhatsApp déconnecté

**Diagnostic :**
```bash
openclaw channels status --json
docker logs mybotia-gateway --tail 50 2>&1 | grep -i whatsapp
```
**Fix :** Attendre 60 secondes (reconnexion auto). Si persistant :
```bash
docker restart mybotia-gateway
# Attendre 30 secondes entre arrêt et redémarrage
```
**⚠️ ATTENTION :** les redémarrages causent des boucles status 440. TOUJOURS tuer TOUS les processus avant de relancer.

### PANNE 5 : RAM élevée (>80%)

**Diagnostic :**
```bash
free -m
ps aux --sort=-%mem | head -10
```
**Fix :** identifier le processus fautif. Si c'est un processus orphelin OpenClaw :
```bash
# Identifier les processus orphelins
ps aux | grep openclaw | grep -v grep
# Tuer les orphelins (PAS les processus principaux)
kill <PID_orphelin>
```
**Escalade si :** processus légitime consomme trop

### PANNE 6 : Certificat SSL proche expiration (<14 jours)

**Diagnostic :**
```bash
echo | openssl s_client -servername lea.mybotia.com -connect lea.mybotia.com:443 2>/dev/null | openssl x509 -noout -enddate
```
**Fix :**
```bash
sudo certbot renew
sudo systemctl reload apache2
```
**Escalade si :** certbot échoue

---

## Niveaux d'Action

| Niveau | Description | Action Oscar |
|--------|-------------|-------------|
| 🟢 INFO | Tout OK | Log silencieux |
| 🟡 WARNING | Dégradé mais fonctionnel | Log + surveillance renforcée |
| 🔴 CRITICAL | Service impacté | Auto-fix + alerte Gilles |
| ⚫ FATAL | Fix impossible | Alerte urgente Gilles + recommandation |

---

## Règles Non Négociables

1. **JAMAIS de modification en production sans backup**
2. **JAMAIS de mise à jour OpenClaw sans validation CEO** — attendre 48h après sortie
3. **JAMAIS d'action destructive sans validation** (rm -rf, drop, reset --hard)
4. **TOUJOURS vérifier que Léa répond sur WhatsApp** après chaque modification
5. **TOUJOURS logger** chaque action dans le rapport d'incident
6. **Si ça casse → rollback immédiat**, pas de debug en production
7. **Heures ouvrées (9h-19h)** : fixes urgents OK, changements planifiés NON

---

## Format de Rapport d'Incident

```
🚨 INCIDENT — [titre court]
⏰ Détection : [timestamp]
📊 Impact : [services affectés]
🔍 Diagnostic : [cause identifiée]
🔧 Action : [ce qui a été fait]
✅ Résultat : [état après fix]
📝 Prévention : [ce qui a été mis en place pour éviter la récurrence]
```
