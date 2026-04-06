# HEARTBEAT.md — Checklist Opérationnelle d'Oscar

## À chaque activation (heartbeat toutes les 30 min)

### Checks automatiques (via health_check.py)
- [ ] Gateway MyBotIA (port 18789) répond HTTP 200
- [ ] Gateway VL Medical (port 18790) répond HTTP 200
- [ ] WhatsApp linked et connecté
- [ ] Python3 + modules OK dans le container Docker
- [ ] RAM < 80%
- [ ] Disque < 85%

### Si un check échoue
1. Exécuter `python3 tools/auto_fix.py --fix`
2. Vérifier que le fix a fonctionné
3. Reporter à Gilles le diagnostic et le résultat

### Checks manuels (si sollicité par Gilles)
- Bots Telegram actifs (getMe API)
- Certificats SSL > 14 jours
- Sous-domaines accessibles (HTTP 200)
- Logs Docker récents (erreurs)
- Logs monitoring (dernières alertes)
- Version OpenClaw installée vs disponible

## Fréquence des rapports
- **Automatique** : alerte immédiate si panne critique détectée
- **Sur demande** : rapport complet quand Gilles demande le statut
- **Proactif** : si je détecte un warning, je préviens même sans demande
