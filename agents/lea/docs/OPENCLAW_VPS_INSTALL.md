# 📋 RÉCAP COMPLET — Réinstallation OpenClaw VPS

> **Document de référence** — Créé le 11 février 2026
> À utiliser pour toute réinstallation ou dépannage

## 🎯 OBJECTIF
Installer OpenClaw proprement sur VPS avec :
- Authentification OAuth (pas API key = pas de rate limit)
- WhatsApp fonctionnel
- Webchat accessible depuis n'importe où

---

## 🖥️ INFOS VPS

| Élément | Valeur |
|---------|--------|
| IP | 180.149.198.23 |
| User | oscar |
| Password | Oscar2026! |
| OS | Debian GNU/Linux |
| OpenClaw | v2026.2.9 |
| Home | /home/oscar/.openclaw/ |

---

## 🔑 TOKENS & CREDENTIALS

### OAuth Token Anthropic (IMPORTANT - valide 1 an)
```
<ANTHROPIC_OAUTH_TOKEN>
```

### Gateway Token
```
114dce61434a52d2bbf77f8319f831c0e761dc51fa80c1e5
```

### WhatsApp
- Numéro : +33 7 56 96 86 33
- JID : 33756968633:9@s.whatsapp.net
- Policy : Pairing (recommended)
- AllowFrom : +33652345180

---

## 🌐 ACCÈS

### Webchat
```
http://180.149.198.23:18789/#token=114dce61434a52d2bbf77f8319f831c0e761dc51fa80c1e5
```

### WhatsApp
```
+33 7 56 96 86 33
```

### SSH
```bash
ssh oscar@180.149.198.23
# Password: Oscar2026!
```

---

## 📁 CHEMINS IMPORTANTS

| Chemin | Contenu |
|--------|---------|
| ~/.openclaw/openclaw.json | Configuration principale |
| ~/.openclaw/workspace/ | Workspace agent principal |
| ~/.openclaw/agents/ | Tous les agents |
| ~/.openclaw/credentials/whatsapp/default/ | Credentials WhatsApp |
| ~/.openclaw/gateway.log | Logs du gateway |
| ~/.openclaw/agents_backup_20260211_1342/ | Backup des anciens agents |
| ~/.npm-global/bin/claude | Claude Code CLI |
| ~/.npm-global/bin/openclaw | OpenClaw CLI |

---

## 🛠️ PROCÉDURE D'INSTALLATION COMPLÈTE

### 1. Connexion VPS
```bash
ssh oscar@180.149.198.23
```

### 2. Reset (si réinstallation)
```bash
openclaw reset --yes
# Choisir : Config + credentials + sessions
```

### 3. Installer Claude Code (pour OAuth token)
```bash
npm install -g @anthropic-ai/claude-code
```

### 4. Générer OAuth Token
```bash
~/.npm-global/bin/claude setup-token
# Copier le token généré (sk-ant-oat01-...)
```

### 5. Lancer le wizard
```bash
openclaw onboard
```

### 6. Options du wizard
| Question | Réponse |
|----------|---------|
| Onboarding mode | Manual |
| Gateway type | Local gateway |
| Workspace | /home/oscar/.openclaw/workspace (défaut) |
| Model/auth provider | Anthropic |
| Anthropic auth method | Anthropic token (paste setup-token) |
| Paste token | Le token OAuth généré |
| Token name | default |
| Gateway bind | LAN (0.0.0.0) pour accès distant |
| Gateway auth | Token |
| Tailscale | Off |
| Gateway token | (laisser vide = génère auto) |
| Configure channels | Yes |
| Channel | WhatsApp |
| Link WhatsApp | Yes → Scanner QR |
| Phone setup | Separate phone just for OpenClaw |
| DM policy | Pairing |
| AllowFrom | +33652345180 |
| Autres channels | Finished |
| Skills | No (plus tard) |
| Hooks | Skip for now |
| Install Gateway service | No (systemctl --user ne marche pas) |
| Bash completion | Yes |

### 7. Lancer le gateway manuellement
```bash
nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &
```

### 8. Vérifier que ça tourne
```bash
pgrep -u oscar -f openclaw
# Doit afficher plusieurs PIDs
```

---

## ⚠️ PROBLÈMES CONNUS & SOLUTIONS

### systemctl --user ne fonctionne pas
**Erreur :** `Failed to connect to bus: Aucun médium trouvé`
**Solution :** Lancer le gateway manuellement avec nohup

### Gateway root qui bloque
**Problème :** Un gateway tourne sous root et bloque le port
**Solution :**
```bash
sudo XDG_RUNTIME_DIR=/run/user/0 systemctl --user stop openclaw-gateway
sudo XDG_RUNTIME_DIR=/run/user/0 systemctl --user disable openclaw-gateway
sudo rm -f /root/.config/systemd/user/openclaw-gateway.service
sudo pkill -9 -u root -f openclaw
```

### WhatsApp déconnecté (registered: false)
**Solution :**
```bash
openclaw channels login
# Scanner le QR code
```

### Rate limit API (429)
**Cause :** Clé API avec limites basses
**Solution :** Utiliser OAuth token à la place (quota compte Claude)

---

## 🔄 COMMANDES UTILES

### Statut
```bash
openclaw status
openclaw channels status
```

### Logs
```bash
tail -f ~/.openclaw/gateway.log
```

### Restart gateway
```bash
pkill -u oscar -f openclaw
nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &
```

### Re-login WhatsApp
```bash
openclaw channels login
```

### Vérifier config
```bash
cat ~/.openclaw/openclaw.json | grep -E "bind|token|model|whatsapp"
```

### Diagnostic
```bash
openclaw doctor
```

---

## 📱 CONFIGURATION WHATSAPP DÉTAILLÉE

Dans `~/.openclaw/openclaw.json` :
```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "dmPolicy": "pairing",
      "allowFrom": ["+33652345180"]
    }
  }
}
```

Credentials stockés dans :
```
~/.openclaw/credentials/whatsapp/default/creds.json
```

---

## 🔐 SÉCURITÉ

- Gateway bind en LAN = accessible publiquement
- Toujours utiliser le token dans l'URL
- Ne pas partager le OAuth token
- Le OAuth token expire dans 1 an (février 2027)

---

## 📅 MAINTENANCE

### Renouveler OAuth token (avant février 2027)
```bash
~/.npm-global/bin/claude setup-token
# Puis mettre à jour openclaw.json
```

### Backup régulier
```bash
cp -r ~/.openclaw/agents ~/.openclaw/agents_backup_$(date +%Y%m%d)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup_$(date +%Y%m%d)
```

---

## ✅ ÉTAT FINAL (11 février 2026)

- [x] OpenClaw v2026.2.9 installé
- [x] OAuth token configuré (pas de rate limit)
- [x] WhatsApp connecté et fonctionnel
- [x] Webchat accessible via IP publique
- [x] Gateway en mode LAN
- [x] Backup des anciens agents conservé
- [ ] Cloner Iris sur le VPS
- [ ] Créer Léa comme agent pro

---

*Dernière mise à jour : 11 février 2026, 14h36*
