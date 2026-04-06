# TOOLS.md — Outils Opérationnels d'Oscar

## Outils Disponibles

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
python3 tools/read_logs.py docker 50 --errors   # Filtrer les erreurs uniquement
```

### 4. Exec (shell)
Accès shell direct pour diagnostics avancés. Utiliser avec prudence.
Autorisé : commandes de lecture (docker ps, curl, free, df, ps, cat logs)
Interdit sans validation CEO : rm, kill (processus principaux), apt install, config changes

## Outils Externes
- Brave Search (recherche web)
- Telegram (canal de communication avec Gilles)
