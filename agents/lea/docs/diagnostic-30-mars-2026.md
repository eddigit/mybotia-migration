# Diagnostic OpenClaw — 30 mars 2026

## Résumé exécutif

3 problèmes actifs, tous liés à la migration Docker du 29 mars :

| # | Problème | Sévérité | Cause racine | Statut |
|---|----------|----------|-------------|--------|
| 1 | **Boucle 499 WhatsApp Léa** | 🔴 CRITIQUE | Corruption cyclique creds.json (7374 fichiers credentials) | Bug connu #56054, pas de fix upstream |
| 2 | **Lucy WhatsApp DOWN** | 🔴 CRITIQUE | Session perdue au restart Docker (0 fichier credentials) | Re-scan QR requis |
| 3 | **Multi-reply Léa** | 🟡 MOYEN | Aggravé par les reconnexions en boucle | Se résoudra avec fix #1 |

---

## 1. 🔴 Boucle de reconnexion 499 — Gateway mybotia (Léa/Nina)

### Symptômes
- Connect → 60s → disconnect status 499 → reconnect → 60s → boucle infinie
- Actif depuis 06:00 UTC (08:00 CEST) le 30 mars
- WhatsApp fonctionnel par intermittence (les messages passent pendant les 60s de connexion)

### Cause racine identifiée

**Bug OpenClaw #56054** — [WhatsApp Baileys: perpetual status 499 reconnection loop with creds.json corruption cycle](https://github.com/openclaw/openclaw/issues/56054)

Le cycle :
1. Baileys se connecte → OK
2. ~60s plus tard → déconnexion status 499
3. Module `web-reconnect` relance (retry 1/12)
4. Module `web-session` restaure `creds.json` depuis un backup STALE
5. Reconnexion → heartbeat détecte silence → force restart → goto 2

**Aggravant majeur sur notre VPS : 7 374 fichiers credentials !**

```
pre-key:    4 705 fichiers
sender-key:   193 fichiers
session:      259 fichiers
app-state:      6 fichiers
creds.json:     1 fichier
```

Le seuil de danger documenté dans le PR #26625 est **500 fichiers**. Nous sommes à **15x** ce seuil. Baileys accumule des pre-key/sender-key/session files à chaque reconnexion sans jamais les nettoyer. Après des semaines, ça corrompt la session.

### Fix disponible (non mergé)

**PR #26625** — `fix(whatsapp): add credential store pruning to prevent session corruption`
- Ajoute un `pruneStaleCredentials()` qui nettoie les fichiers > 500, garde les 100 plus récents
- Statut : **OPEN**, non mergé dans main
- Auteur a testé manuellement sur 1776 fichiers → succès

### Workaround immédiat

D'après le PR #26625 et l'issue #56054 :

```bash
# 1. Arrêter la gateway
docker stop mybotia-gateway

# 2. Purger les pre-key/sender-key/session obsolètes (garder les 100 plus récents)
cd ~/.openclaw/credentials/whatsapp/default/
ls -t pre-key-*.json | tail -n +101 | xargs rm -f
ls -t sender-key-*.json | tail -n +101 | xargs rm -f
ls -t session-*.json | tail -n +101 | xargs rm -f

# 3. NE PAS toucher à creds.json ni app-state-*

# 4. Redémarrer la gateway
docker start mybotia-gateway
```

Si la boucle persiste après purge :
```bash
# Option B : supprimer creds.json + re-scan QR
rm ~/.openclaw/credentials/whatsapp/default/creds.json
docker restart mybotia-gateway
# → Scanner le QR depuis le téléphone associé au +33 7 56 96 86 33
```

### Compte Nina (aussi concerné)
- 1 895 fichiers credentials → au-dessus du seuil de 500
- Pas encore en boucle 499, mais à risque

---

## 2. 🔴 Lucy WhatsApp DOWN — Session perdue

### Symptômes
- DOWN depuis 29/03 ~21:25 CEST (11h45+)
- `health-monitor: restarting (reason: stopped)` en boucle toutes les 10-15 min
- 0 fichiers dans le dossier credentials WhatsApp Lucy

### Cause
Le `docker restart` du 29 mars (SIGTERM à 21:25-29) a tué la gateway Lucy. Au redémarrage en Docker (`restart=unless-stopped`), la session WhatsApp n'a pas été restaurée car le dossier credentials était vide ou pas correctement monté.

### Fix
Re-scanner le QR depuis le téléphone Android Lucy (+33 7 58 05 46 84). Aucun workaround automatique possible.

---

## 3. 🟡 Multi-reply Léa (21 auto-replies ce matin)

### Symptômes
- 21 auto-replies dans le groupe 120363406232810102@g.us entre 07:12 et 08:34 CEST
- Doublons constatés

### Cause
Combinaison de :
- **Bug #54570** (fixé dans v2026.3.28) — echo loop en self-chat DM
- **Bug #54836** (OPEN) — réponses dupliquées via webchat surface
- **Bug #44467** (OPEN) — delivery-mirror déclenche des réponses dupliquées
- **Aggravé par** la boucle 499 : chaque reconnexion peut re-trigger des messages en queue

### Fix
Résoudre le problème #1 (boucle 499) devrait éliminer la majorité des multi-replies. Les bugs #54836 et #44467 restent ouverts upstream.

---

## Bugs & Fixes embarqués dans v2026.3.28 (notre version)

| Fix | Issue | Description |
|-----|-------|-------------|
| ✅ | #54570 | Echo loop WhatsApp self-chat DM — outbound ID tracking |
| ✅ | #53624 | fromMe filter en groupes WhatsApp — anti boucle infinie |
| ✅ | #56612 | Suppression NO_REPLY JSON envelopes avant delivery |
| ✅ | #53940 | Restart sentinel — wake session + preserve thread routing |
| ✅ | #54697 | Discord stale-socket drain + forced reconnect cleanup |
| ✅ | #52711 | WhatsApp mentions — quoted messages ne trigger plus mention gating |

### Bugs OUVERTS nous affectant

| Bug | Description | Impact |
|-----|-------------|--------|
| 🔴 #56054 | Boucle 499 avec corruption creds.json | Notre problème principal |
| 🟡 #54836 | Réponses dupliquées WhatsApp via webchat | Multi-reply |
| 🟡 #44467 | delivery-mirror déclenche doublons | Multi-reply |
| 🟡 #26625 | PR fix credential pruning — pas mergé | Workaround disponible |
| 🟡 #22511 | Déconnexions fréquentes sans auto-recovery | Ancien, toujours ouvert |

---

## État des credentials WhatsApp (tous comptes)

| Compte | Fichiers | Statut |
|--------|----------|--------|
| default (Léa) | **7 374** | 🔴 CRITIQUE (seuil : 500) |
| nina | **1 895** | 🟡 À PURGER |
| vlmedical-admin | 208 | ✅ OK |
| lucy | 0 | ❌ Session perdue |

---

## Recommandations

### Immédiat (GO requis)
1. **Purger les credentials Léa** (7374 → ~100 fichiers) + restart gateway
2. **Purger les credentials Nina** (1895 → ~100 fichiers) pendant qu'on y est
3. **Re-scanner QR Lucy** avec le téléphone Android

### Court terme
4. **Script cron de pruning** — ajouter un cron qui maintient les credentials < 500 fichiers (comme le PR #26625 le propose)
5. **Upgrade Max → Sonnet 4.6** + reset session (Jacques peut le faire)

### Moyen terme
6. **Monitorer** l'issue #56054 pour un fix upstream
7. **Quotas collaborateurs** (discussion en cours)
