# 🦞 RÉFÉRENCE COMPLÈTE OPENCLAW VPS
## Document d'urgence pour reprise par Claude ou autre IA

> **Document critique** — Créé le 11 février 2026
> À utiliser si Iris locale n'est pas disponible et qu'il faut intervenir sur le VPS

---

# 📌 INFORMATIONS CRITIQUES

## Accès VPS

| Élément | Valeur |
|---------|--------|
| **IP** | `180.149.198.23` |
| **User** | `oscar` |
| **Password** | `Oscar2026!` |
| **OS** | Debian GNU/Linux |
| **OpenClaw Version** | v2026.2.9 |

```bash
ssh oscar@180.149.198.23
# Password: Oscar2026!
```

## Tokens & Credentials

### OAuth Token Anthropic (valide jusqu'à février 2027)
```
<ANTHROPIC_OAUTH_TOKEN>
```

### Gateway Token
```
114dce61434a52d2bbf77f8319f831c0e761dc51fa80c1e5
```

### WhatsApp
| Élément | Valeur |
|---------|--------|
| Numéro | +33 7 56 96 86 33 |
| JID | 33756968633:9@s.whatsapp.net |
| Policy | Pairing (recommended) |
| AllowFrom | +33652345180 (Gilles) |
| Groupe autorisé | 120363427866204061@g.us |

## URLs d'accès

### Webchat (navigateur)
```
http://180.149.198.23:18789/#token=114dce61434a52d2bbf77f8319f831c0e761dc51fa80c1e5
```

### WhatsApp
```
+33 7 56 96 86 33
```

---

# 📁 CHEMINS CRITIQUES

| Chemin | Description |
|--------|-------------|
| `~/.openclaw/openclaw.json` | Configuration principale |
| `~/.openclaw/workspace/` | Workspace agent principal |
| `~/.openclaw/agents/` | Tous les agents |
| `~/.openclaw/credentials/whatsapp/default/` | Credentials WhatsApp |
| `~/.openclaw/credentials/whatsapp/default/creds.json` | Session WhatsApp active |
| `~/.openclaw/credentials/whatsapp/default/creds.json.bak` | Backup session WhatsApp |
| `~/.openclaw/gateway.log` | Logs du gateway |
| `~/.openclaw/agents_backup_20260211_1342/` | Backup des anciens agents |
| `~/.npm-global/bin/claude` | Claude Code CLI |
| `~/.npm-global/bin/openclaw` | OpenClaw CLI |
| `~/.openclaw/.env` | Variables d'environnement |

---

# ⚠️ RÈGLES CRITIQUES

## ❌ COMMANDES INTERDITES

```bash
# NE JAMAIS FAIRE - casse les credentials WhatsApp
pkill -f openclaw
pkill -9 openclaw
kill -9 <pid>
```

## ✅ COMMANDES AUTORISÉES

```bash
# Arrêt propre (graceful shutdown)
openclaw gateway stop

# Attendre que tout soit flush
sleep 5

# Redémarrage
nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &
```

## Pourquoi ?
Le `pkill` ne laisse pas le temps au gateway de sauvegarder les credentials WhatsApp (flush). Résultat : `registered: false` dans creds.json → WhatsApp déconnecté.

---

# 🔧 PROCÉDURES D'URGENCE

## 1. Vérifier si le gateway tourne

```bash
ssh oscar@180.149.198.23
pgrep -u oscar -f openclaw
# Doit afficher plusieurs PIDs
```

## 2. Vérifier l'état WhatsApp

```bash
cat ~/.openclaw/credentials/whatsapp/default/creds.json | grep registered
# Doit afficher "registered":true
```

**Si `registered: false`** → WhatsApp déconnecté, voir procédure de reconnexion.

## 3. Redémarrer le gateway (PROPREMENT)

```bash
# 1. Arrêt graceful
openclaw gateway stop

# 2. Attendre
sleep 5

# 3. Vérifier qu'il est bien arrêté
pgrep -u oscar -f openclaw
# Ne doit rien afficher

# 4. Redémarrer
nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &

# 5. Vérifier
sleep 5
pgrep -u oscar -f openclaw
# Doit afficher plusieurs PIDs
```

## 4. Reconnecter WhatsApp (si déconnecté)

```bash
# 1. Lancer le login
openclaw channels login

# 2. Un QR code s'affiche
# 3. Scanner avec le téléphone +33756968633
# 4. Attendre "Linked after restart; web session ready."
```

## 5. Restaurer credentials WhatsApp depuis backup

```bash
# Si creds.json est corrompu
cp ~/.openclaw/credentials/whatsapp/default/creds.json.bak \
   ~/.openclaw/credentials/whatsapp/default/creds.json

# Redémarrer le gateway
openclaw gateway stop
sleep 5
nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &
```

## 6. Vérifier les logs

```bash
# Logs temps réel
tail -f ~/.openclaw/gateway.log

# Dernières lignes
tail -50 ~/.openclaw/gateway.log

# Chercher des erreurs
grep -i error ~/.openclaw/gateway.log | tail -20
```

## 7. Diagnostic complet

```bash
openclaw doctor
```

## 8. Statut des channels

```bash
openclaw status
openclaw channels status
```

---

# 🔄 RÉINSTALLATION COMPLÈTE

Si tout est cassé, voici la procédure de réinstallation from scratch.

## Étape 1 : Backup

```bash
cp -r ~/.openclaw/agents ~/.openclaw/agents_backup_$(date +%Y%m%d_%H%M)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup_$(date +%Y%m%d_%H%M)
```

## Étape 2 : Reset

```bash
openclaw reset --yes
# Choisir : Config + credentials + sessions
```

## Étape 3 : Installer Claude Code (si pas installé)

```bash
npm install -g @anthropic-ai/claude-code
```

## Étape 4 : Générer OAuth Token

```bash
~/.npm-global/bin/claude setup-token
# Sauvegarder le token généré (sk-ant-oat01-...)
```

## Étape 5 : Onboarding

```bash
openclaw onboard
```

### Options du wizard :

| Question | Réponse |
|----------|---------|
| Onboarding mode | **Manual** |
| Gateway type | **Local gateway** |
| Workspace | `/home/oscar/.openclaw/workspace` (défaut) |
| Model/auth provider | **Anthropic** |
| Auth method | **Anthropic token (paste setup-token)** |
| Token | Le token OAuth généré |
| Token name | `default` |
| Gateway bind | **LAN (0.0.0.0)** |
| Gateway auth | **Token** |
| Tailscale | **Off** |
| Gateway token | (laisser vide = génère auto) |
| Configure channels | **Yes** |
| Channel | **WhatsApp** |
| Link WhatsApp | **Yes** → Scanner QR |
| Phone setup | **Separate phone just for OpenClaw** |
| DM policy | **Pairing** |
| AllowFrom | `+33652345180` |
| Autres channels | **Finished** |
| Skills | **No** |
| Hooks | **Skip for now** |
| Install Gateway service | **No** (systemctl --user ne marche pas) |
| Bash completion | **Yes** |

## Étape 6 : Lancer le gateway

```bash
nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &
```

## Étape 7 : Configurer les groupes WhatsApp

Ajouter les groupes dans la config :

```bash
# Éditer openclaw.json
nano ~/.openclaw/openclaw.json

# Ajouter dans channels.whatsapp :
# "groupPolicy": "allowlist",
# "allowFrom": ["120363427866204061@g.us", "+33652345180"]
```

---

# 🐛 PROBLÈMES CONNUS

## systemctl --user ne fonctionne pas

**Erreur :** `Failed to connect to bus: Aucun médium trouvé`

**Cause :** Le VPS n'a pas de session D-Bus pour l'utilisateur oscar.

**Solution :** Ne pas utiliser `openclaw gateway install`. Lancer manuellement avec `nohup`.

## Gateway root qui bloque

**Symptôme :** Deux process gateway (un root, un oscar)

**Solution :**
```bash
# Désactiver le service root
sudo XDG_RUNTIME_DIR=/run/user/0 systemctl --user stop openclaw-gateway
sudo XDG_RUNTIME_DIR=/run/user/0 systemctl --user disable openclaw-gateway
sudo rm -f /root/.config/systemd/user/openclaw-gateway.service

# Tuer les process root
sudo pkill -9 -u root -f openclaw

# Vérifier
ps aux | grep openclaw | grep -v grep
# Doit montrer SEULEMENT oscar
```

## WhatsApp "registered: false"

**Cause :** Gateway arrêté brutalement (pkill), credentials non sauvegardés.

**Solution :**
```bash
# Option 1 : Restaurer backup
cp ~/.openclaw/credentials/whatsapp/default/creds.json.bak \
   ~/.openclaw/credentials/whatsapp/default/creds.json
openclaw gateway stop && sleep 5 && nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &

# Option 2 : Re-scanner QR
openclaw channels login
```

## Rate limit 429 (si clé API utilisée)

**Cause :** Clé API avec limites basses au lieu du token OAuth.

**Vérification :**
```bash
grep -i anthropic ~/.openclaw/openclaw.json
grep -i anthropic ~/.openclaw/.env
```

**Solution :** Utiliser le token OAuth (sk-ant-oat01-...) qui utilise le quota du compte Claude.

## Port 18789 déjà utilisé

```bash
# Trouver le process
lsof -i :18789

# Tuer si nécessaire
kill -9 <PID>

# Ou forcer le démarrage
openclaw gateway --force
```

---

# 📊 CONFIGURATION ACTUELLE

## openclaw.json (extraits importants)

```json
{
  "auth": {
    "profiles": {
      "anthropic:default": {
        "provider": "anthropic",
        "mode": "token"
      }
    }
  },
  "gateway": {
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token"
    }
  },
  "channels": {
    "whatsapp": {
      "enabled": true,
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "allowFrom": [
        "120363427866204061@g.us",
        "+33652345180"
      ]
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5"
      }
    }
  }
}
```

## .env

```bash
BRAVE_API_KEY=<BRAVE_SEARCH_API_KEY>
```

---

# 📅 MAINTENANCE

## Vérification quotidienne

```bash
ssh oscar@180.149.198.23
pgrep -u oscar -f openclaw && echo "Gateway OK" || echo "Gateway DOWN"
cat ~/.openclaw/credentials/whatsapp/default/creds.json | grep -o '"registered":[^,]*'
```

## Renouvellement OAuth token (avant février 2027)

```bash
~/.npm-global/bin/claude setup-token
# Copier le nouveau token dans openclaw.json
```

## Backup régulier

```bash
cp -r ~/.openclaw/agents ~/.openclaw/agents_backup_$(date +%Y%m%d)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup_$(date +%Y%m%d)
```

---

# 📞 CONTACTS

| Qui | Numéro | Rôle |
|-----|--------|------|
| Gilles Korzec | +33 6 52 34 51 80 | CEO / Propriétaire |
| Iris (VPS) | +33 7 56 96 86 33 | IA Assistant (WhatsApp) |

---

# 🔐 SÉCURITÉ

- Gateway bind en LAN = accessible publiquement sur l'IP
- **Toujours utiliser le token dans l'URL webchat**
- **Ne jamais partager le OAuth token publiquement**
- OAuth token expire dans 1 an (février 2027)
- Credentials WhatsApp = session active, ne pas supprimer

---

*Dernière mise à jour : 11 février 2026, 14h59*
*Document créé par Iris pour continuité opérationnelle*
