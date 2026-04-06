# 🤖 PROTOCOLE — Création d'un Collaborateur IA Client

> **Responsable** : Léa (pilote) + Claude Code (exécution technique)
> **Durée cible** : 30 minutes max
> **Dernière MàJ** : 23 mars 2026

---

## PRÉREQUIS — Infos à collecter AVANT de commencer

| Info | Exemple | Obligatoire |
|------|---------|-------------|
| Nom du collaborateur | Lucy | ✅ |
| Nom du client / entreprise | IGH | ✅ |
| Photo avatar (URL Cloudinary) | https://res.cloudinary.com/... | ✅ |
| Numéro WhatsApp (SIM dédiée) | +33 7 58 05 46 84 | ✅ |
| Modèle IA | claude-sonnet-4-6 | ✅ |
| Port gateway (vérifier dispo) | 18795 | ✅ |
| Groupes WhatsApp autorisés (JID) | 120363407026699197@g.us | Si applicable |
| Rôle / description | Collaboratrice IA — IGH | ✅ |
| Téléphone Android dispo pour scan QR | Oui | ✅ |

**Ports utilisés :**
| Port | Agent |
|------|-------|
| 18789 | Gateway principale (Léa, Julian, Nina, Oscar) |
| 18790 | VL Medical (Max, Eva) |
| 18794 | Test (Brice) |
| 18795 | Lucy (IGH) |
| 18796+ | Prochains collaborateurs |

---

## CHECKLIST — 10 étapes dans l'ordre

### ☐ 1. Créer le profil OpenClaw dédié

**Dossier** : `~/.openclaw-{nom}/`
**Fichier** : `~/.openclaw-{nom}/openclaw.json`

⚠️ **PIÈGES À ÉVITER :**
- L'ID agent doit être `{nom}` (PAS `main` — sinon conflit avec la gateway principale)
- Le port doit être unique (vérifier avec `ss -tlnp | grep 187`)
- Générer un token gateway unique : `openssl rand -hex 24`

**Contenu obligatoire :**
- `agents.list[0].id` = `{nom}` (PAS "main")
- `agents.list[0].default` = true
- `agents.list[0].name` = nom affiché
- `agents.list[0].identity.avatar` = URL photo
- `gateway.port` = port dédié
- `gateway.auth.token` = token unique généré
- `channels.whatsapp.enabled` = true
- `channels.whatsapp.allowFrom` = ["+33652345180"] (Gilles minimum)
- `channels.whatsapp.accounts.default.name` = nom du collaborateur
- `gateway.controlUi.allowedOrigins` = inclure `https://{nom}.mybotia.com` et `https://admin.mybotia.com`

### ☐ 2. Créer le workspace

**Dossier** : `~/.openclaw/workspace-{nom}/`

**Fichiers à créer :**
- `SOUL.md` — personnalité, ton, règles
- `IDENTITY.md` — identité, rôle, rattachement, avatar URL
- `AGENTS.md` — hiérarchie, règles de conduite
- `MEMORY.md` — contexte client, organigramme, historique
- `USER.md` — contexte (client, timezone)

### ☐ 3. Copier les clés d'authentification

```bash
mkdir -p ~/.openclaw-{nom}/agents/{nom}/agent/
cp ~/.openclaw/agents/main/agent/auth-profiles.json ~/.openclaw-{nom}/agents/{nom}/agent/
```

⚠️ **PIÈGE** : Le chemin doit correspondre à l'ID agent. Si l'ID est `lucy`, le chemin est `agents/lucy/agent/`. Si c'est `main`, c'est `agents/main/agent/`. **L'ID dans le JSON et le chemin doivent matcher.**

### ☐ 4. Ajouter dans admin.mybotia.com

**4a. `gateway-config.js`** (`~/apps/admin/services/gateway-config.js`)

Ajouter une entrée dans le tableau `GATEWAYS` :
```javascript
{
  id: '{nom}-{client}',
  label: '{Nom} ({Client})',
  configPath: path.join(os.homedir(), '.openclaw-{nom}', 'openclaw.json'),
  stateDir: path.join(os.homedir(), '.openclaw-{nom}'),
  port: {PORT},
  mode: 'host',
  logFile: '/tmp/{nom}-gateway.log',
  restartCmd: 'pkill -f "openclaw.*gateway.*--port {PORT}" 2>/dev/null; sleep 2; OPENCLAW_CONFIG_PATH=/home/gilles/.openclaw-{nom}/openclaw.json OPENCLAW_STATE_DIR=/home/gilles/.openclaw-{nom} nohup openclaw gateway --port {PORT} > /tmp/{nom}-gateway.log 2>&1 &'
}
```

**4b. `agents.json` public** (`/var/www/html/mybotia/agents.json`)
```json
"{nom}": {
    "token": "{TOKEN_GATEWAY}",
    "session": "{nom}",
    "name": "{Nom}",
    "agentId": "{nom}",
    "port": {PORT}
}
```

**4c. `agents.json` private** (`/var/www/html/mybotia/private/agents.json`)
```json
"{nom}": {
    "token": "{TOKEN_GATEWAY}",
    "session": "agent:{nom}:{nom}",
    "name": "{Nom}",
    "agentId": "{nom}",
    "avatar": "{URL_AVATAR}",
    "role": "{Rôle}",
    "port": {PORT},
    "cards": [...]
}
```

### ☐ 5. Créer le vhost Apache

Créer `/etc/apache2/sites-available/{nom}-mybotia-le-ssl.conf` dédié qui pointe le WebSocket `/ws` vers le bon port.

Le DNS wildcard `*.mybotia.com` est déjà en place, pas besoin de toucher au DNS.

```bash
sudo a2ensite {nom}-mybotia-le-ssl.conf
sudo apachectl configtest
sudo systemctl reload apache2
```

### ☐ 6. Créer l'email sur Migadu

```bash
curl -s -X POST "https://api.migadu.com/v1/domains/collaborateur.pro/mailboxes" \
  -u "gilleskorzec@gmail.com:{MIGADU_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"local_part":"{nom}","name":"{Nom}","password":"$$Reussite888!!","password_recovery_email":"coachdigitalparis@gmail.com"}'
```

### ☐ 7. Créer le login webchat (SQLite)

```bash
HASH=$(php -r "echo password_hash('\$\$Reussite888!!', PASSWORD_BCRYPT);")
sudo sqlite3 /var/www/html/mybotia/private/mybotia.db \
  "INSERT INTO clients (email, password_hash, company_name, contact_name, plan, is_admin) VALUES ('{nom}@collaborateur.pro', '$HASH', '{Client}', '{Nom}', 'pro', 0);"
```

### ☐ 8. Lancer la gateway + scanner WhatsApp

```bash
# Lancer la gateway
OPENCLAW_CONFIG_PATH=~/.openclaw-{nom}/openclaw.json \
OPENCLAW_STATE_DIR=~/.openclaw-{nom} \
nohup /home/gilles/.npm-global/bin/openclaw gateway --port {PORT} > /tmp/{nom}-gateway.log 2>&1 &

# Vérifier
curl -s http://127.0.0.1:{PORT}/health
```

Puis scanner le QR WhatsApp via admin.mybotia.com (sélectionner la bonne gateway).

⚠️ **NE PAS restart la gateway après le scan** — le fix du 22/03/2026 a supprimé le restart post-pairing.

### ☐ 9. Créer le bot Telegram (si nécessaire)

1. Sur Telegram → @BotFather → `/newbot`
2. Nom : `{Nom} {Client}`
3. Username : `{nom}_{client}_bot`
4. Récupérer le token
5. Ajouter dans `~/.openclaw-{nom}/openclaw.json` section `channels.telegram`
6. Redémarrer la gateway

### ☐ 10. Watchdog + Enregistrements

**Cron watchdog :**
```bash
# Ajouter dans crontab
*/5 * * * * /home/gilles/scripts/monitoring/{nom}-watchdog.sh
```

**Enregistrer dans Notion** (base Credentials `0893467c-c00f-4165-ac7d-b6c46d8671bc`) :
- Email Migadu ({nom}@collaborateur.pro)
- Bot Telegram
- Token gateway

**Mettre à jour CLAUDE.md** pour que Claude Code connaisse le nouveau collaborateur.

**Mettre à jour la mémoire Léa** (MEMORY-CORE.md, fichier client).

---

## VÉRIFICATION FINALE

| Check | Commande / Action |
|-------|-------------------|
| Gateway health | `curl http://127.0.0.1:{PORT}/health` |
| WhatsApp connecté | Vérifier dans admin.mybotia.com |
| Telegram actif | Envoyer /start au bot |
| Webchat fonctionne | Aller sur https://{nom}.mybotia.com |
| Login webchat | {nom}@collaborateur.pro / $$Reussite888!! |
| Admin affiche bien | Vérifier fiche dans admin.mybotia.com |
| Watchdog cron | `crontab -l | grep {nom}` |
| Notion à jour | Credentials enregistrés |
| CLAUDE.md à jour | Claude Code connaît l'agent |

---

## ERREURS CONNUES — NE PAS REPRODUIRE

| Erreur | Conséquence | Solution |
|--------|-------------|----------|
| ID agent = `main` | Conflit avec Léa, l'admin ouvre le mauvais profil | Toujours utiliser un ID unique = nom du collaborateur |
| Mettre l'agent dans la gateway principale | Pas isolé, si un plante tout plante | Toujours une gateway dédiée par client |
| Restart gateway après scan QR | WhatsApp se déconnecte après quelques heures | Ne JAMAIS restart après le scan |
| Oublier auth-profiles.json | "No API key found" | Copier depuis la gateway principale |
| Email @collaborateur.ia.pro | Domaine inexistant | Le bon domaine = collaborateur.pro |
| Pas de watchdog cron | Si la gateway crash la nuit, personne ne relance | Toujours créer le script + cron |
| Token gateway = même que principale | Risque de conflit | Toujours générer un token unique |
| Pas mettre à jour CLAUDE.md | Si Léa tombe, Claude Code ne connaît pas l'agent | Toujours mettre à jour |

---

## VERSION RAPIDE — PROMPTS CLAUDE CODE

### Prompt 1 : Infrastructure
```
Créer un nouveau collaborateur IA :
- Nom : {NOM}
- Client : {CLIENT}
- Port : {PORT}
- Avatar : {URL}
- WhatsApp : {NUMÉRO}
- Groupes WA : {JID}

Suivre le protocole dans /home/gilles/.openclaw/workspace/procedures/creation-collaborateur.md
Étapes 1 à 5 uniquement. Ne PAS toucher à la gateway principale (18789).
```

### Prompt 2 : Email + Login
```
Créer l'email et le login webchat pour le collaborateur {NOM} :
- Étapes 6 et 7 du protocole dans procedures/creation-collaborateur.md
- Email : {nom}@collaborateur.pro
- Mot de passe : $$Reussite888!!
- Client : {CLIENT}
```

### Prompt 3 : Lancement + Scan
```
Lancer la gateway {NOM} et préparer le scan WhatsApp :
- Étape 8 du protocole
- Port : {PORT}
- NE PAS restart après le scan
```

### Prompt 4 : Telegram + Finalisation
```
Ajouter le bot Telegram au collaborateur {NOM} :
- Token bot : {TOKEN}
- Étapes 9 et 10 du protocole
- Créer le watchdog cron
- Enregistrer dans Notion
- Mettre à jour CLAUDE.md
```
