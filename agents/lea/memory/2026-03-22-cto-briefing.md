# Briefing CTO IA — 22 mars 2026

## Travaux réalisés aujourd'hui par le CTO (Claude Code Opus 4.6)

### 1. Upgrade serveur LC4 confirmé
Le VPS a été upgradé par LWS :
- RAM : 8 Go → **12 Go** (+12 Go swap)
- CPU : 2 → **3 vCPUs** online (16 total)
- Disque : 79 Go → **98 Go** SSD
- CLAUDE.md mis à jour avec les nouvelles specs

### 2. Fix WhatsApp Pairing — Bug Baileys RC9
**Problème** : L'appairage WhatsApp via admin.mybotia.com fonctionnait (QR scanné) mais la session se déconnectait après quelques heures.

**Cause racine** : Bug Baileys 7.0.0-rc.9 (utilisé par OpenClaw 2026.3.13) — après un scan QR réussi, le flag `registered` dans `creds.json` reste à `false`. WhatsApp finit par rejeter la session (erreur 401). De plus, une erreur 515 ("Unknown Stream Errored") crash le stream juste après le scan.

**Fix déployé dans admin.mybotia.com (v4.1.0)** :
- **Nouveau bouton "Forcer un nouveau lien"** : purge automatiquement les anciens credentials + restart gateway + génère un QR frais
- **Auto-patch `registered: true`** : après détection de connexion réussie, le backend patche automatiquement le creds.json
- **Détection 515 intelligente** : si le RPC crash (erreur 515) mais que les credentials montrent un `me.id` valide, le système déclare quand même la connexion réussie
- **Auto-restart gateway** : après le patch, la gateway est redémarrée automatiquement pour une connexion propre

**Fichiers modifiés** :
- `~/apps/admin/routes/agents.js` — nouvelles fonctions `patchWhatsAppRegistered()`, `purgeWhatsAppCreds()`, `restartGatewayAndWait()`, `checkCredsLinked()`
- `~/apps/admin/public/js/agents.js` — UX améliorée du modal QR (force re-link, gestion timeout, feedback utilisateur)

### 3. Gateway test Brice — État actuel
- Port 18794 : **UP**
- WhatsApp (+33780956222) : **connecté** (Brice MyBotIA)
- Telegram (@brice_test_mybotia_bot) : **actif**
- Vhost Apache brice.mybotia.com : pas encore configuré (webchat uniquement)
- Credentials patchés avec `registered: true`

### Impact pour les autres agents
Ce fix WhatsApp s'applique à **toutes les gateways** gérées par le dashboard admin. Si un agent WhatsApp (Léa, Nina, Max) se déconnecte, le bouton "Forcer un nouveau lien" dans admin.mybotia.com fera automatiquement : purge → restart → QR → patch → reconnexion.

### Surveillance
- Brice sous surveillance 24h pour confirmer la stabilité du fix
- Si la session retombe, le prochain fix envisagé : cron de vérification `registered: true` ou upgrade OpenClaw

---
*Rédigé par le CTO IA (Claude Code) — session du 22/03/2026*
