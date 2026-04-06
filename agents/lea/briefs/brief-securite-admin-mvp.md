# Brief Claude Code — Section Sécurité dans Admin MVP

## Contexte

L'admin MVP MyBotIA tourne sur `http://127.0.0.1:3001` (Express.js) avec un frontend en `/var/www/html/mybotia/`.
L'API agent existe déjà : `/api/agent/briefing`, `/clients`, `/pipeline`, `/paiements`, `/tasks`, `/alerts`, `/search`.
Base de données : PostgreSQL `mybotia_crm`.

On veut ajouter une **section Sécurité** complète au dashboard admin.

## Ce qu'il faut créer

### 1. Nouvel endpoint API : `GET /api/agent/security`

Retourne un JSON avec 4 blocs :

#### A. Audit OpenClaw
- Exécuter `python3 /home/gilles/.openclaw/workspace/skills/oc-security-hardener/scripts/hardener.py audit -f json`
- Retourner le score, le label, et la liste des checks (passed/failed)
- Config auditée : `~/.openclaw/openclaw.json`

#### B. État des backups
- Lister les archives dans `/home/gilles/backups/config-backup-*.tar.gz`
- Pour chaque : date, taille
- Dernier backup : date, taille, âge (heures depuis)
- Nombre total de backups stockés
- Statut du cron backup : vérifier que la ligne existe dans `crontab -l`

#### C. Santé serveur
- RAM : totale, utilisée, disponible (lire `/proc/meminfo`)
- Swap : total, utilisé, pourcentage
- Disque : espace total, utilisé, disponible, pourcentage (df /)
- Uptime serveur
- Load average

#### D. Statut collaborateurs
- Lire le health check gateway : appeler `openclaw gateway call health` via WebSocket local `ws://127.0.0.1:18789` avec le token gateway depuis la config
- Extraire le statut de chaque agent (main/julian/nina/oscar/bullsage/agent-rh) : running, dernière session, dernière activité
- Extraire le statut de chaque channel (whatsapp, telegram) : connected, linked, dernière activité

### 2. Nouvel endpoint API : `POST /api/agent/backup/trigger`

- Exécute le script de backup existant : `/home/gilles/scripts/monitoring/backup-config.sh`
- Retourne le résultat (succès/erreur + nom de l'archive)
- Protection : ne pas permettre plus d'un backup par heure (anti-spam)

### 3. Nouvel endpoint API : `POST /api/agent/security/audit`

- Relance l'audit de sécurité à la demande
- Retourne le JSON de l'audit frais

### 4. Frontend — Nouvelle page/section dans le dashboard

Ajouter une section "🔒 Sécurité" accessible depuis la navigation du dashboard.

#### Layout de la page :

**Ligne 1 — Score sécu + Santé serveur (2 cartes)**
- Carte gauche : Score de sécurité (gros chiffre /100 avec couleur : vert >80, orange 50-80, rouge <50), label (Excellent/Good/Fair/Poor), bouton "Relancer l'audit"
- Carte droite : RAM, Swap, Disque en barres de progression avec pourcentages, Uptime, Load

**Ligne 2 — Détail de l'audit (1 carte large)**
- Tableau des checks : nom, sévérité (badge coloré CRITICAL/HIGH/MEDIUM/LOW), statut PASS/FAIL, description, fix recommandé si FAIL

**Ligne 3 — Backups (1 carte large)**
- Dernier backup : date, taille, âge
- Tableau des 10 derniers backups (date, taille)
- Bouton "Lancer un backup maintenant"
- Indicateur cron actif/inactif

**Ligne 4 — Collaborateurs (1 carte large)**
- Tableau : nom agent, emoji, statut (pastille verte/rouge), dernière activité, nombre de sessions
- Tableau : channels (WhatsApp, Telegram), statut connexion, dernier message

#### Style
- Même style que le reste du dashboard (CSS existant)
- Responsive
- Pas de framework JS externe (vanilla JS comme le reste de l'app)

### 5. Backup PostgreSQL (nouveau script)

Créer `/home/gilles/scripts/monitoring/backup-postgres.sh` :
- Dump de la base `mybotia_crm` avec `pg_dump`
- Compression gzip
- Stockage dans `/home/gilles/backups/postgres/`
- Rétention 30 jours
- Ajouter au cron : tous les jours à 2h30 (avant le backup config de 3h)
- Intégrer le statut de ce backup dans l'endpoint `/api/agent/security` (bloc B)

## Fichiers existants à consulter

- Backend admin : chercher le serveur Express dans `/var/www/html/mybotia/` ou dans les process Node qui écoutent sur le port 3001
- Frontend : `/var/www/html/mybotia/v12-4.html` (interface actuelle)
- Script backup existant : `/home/gilles/scripts/monitoring/backup-config.sh`
- Hardener : `/home/gilles/.openclaw/workspace/skills/oc-security-hardener/scripts/hardener.py`
- Config OpenClaw : `~/.openclaw/openclaw.json`
- Gateway token : dans `~/.openclaw/openclaw.json` → `gateway.auth.token`

## Contraintes

- Pas de dépendances npm supplémentaires sauf si absolument nécessaire
- Vanilla JS côté frontend (pas de React/Vue)
- Les endpoints doivent être protégés par le même système d'auth que les endpoints existants (header X-API-Key)
- Ne pas modifier les endpoints existants
- Ne pas toucher à la config OpenClaw
- Ne pas redémarrer la gateway
- Tester que tout fonctionne avant de valider

## Résultat attendu

Une section Sécurité fonctionnelle dans l'admin MVP qui permet à Gilles de voir en un coup d'œil :
- Le niveau de sécurité de l'infra
- L'état des backups
- La santé du serveur
- Le statut de chaque collaborateur IA
- Et de déclencher manuellement un backup ou un audit
