# VPS Oscar — Serveur Équipe IA

## 🎉 STATUS: OPÉRATIONNEL

OpenClaw gateway tourne sur le VPS depuis le 04-02-2026 10:50 CET !

## Infos serveur

| Champ | Valeur |
|-------|--------|
| **Hébergeur** | LWS |
| **Référence** | VPS-116827 |
| **Formule** | VPS LC3 |
| **IP** | 180.149.198.23 |
| **Hostname** | vps116827.serveur-vps.net |
| **OS** | Debian 12 (Bookworm) + ISPConfig 3 |
| **RAM** | 8 Go |
| **Disque** | 80 Go |
| **Expiration** | 09-02-2026 ⚠️ |

## Accès SSH

- **Host** : 180.149.198.23
- **Port** : 22
- **User root** : `Oscar2026VPS!`
- **User oscar** : `Oscar2026!`

## OpenClaw Gateway

### Accès
- **URL Dashboard** : http://180.149.198.23:18789
- **WebSocket** : ws://180.149.198.23:18789
- **Token** : `OscarVPS2026SecureToken!`

### Service systemd
```bash
# En tant qu'utilisateur oscar
systemctl --user status openclaw-gateway
systemctl --user restart openclaw-gateway
systemctl --user stop openclaw-gateway
journalctl --user -u openclaw-gateway -f  # Voir les logs
```

### Fichiers config
- Config : `/home/oscar/.openclaw/openclaw.json`
- Auth profiles : `/home/oscar/.openclaw/agents/main/agent/auth-profiles.json`
- Workspace : `/home/oscar/.openclaw/workspace`

### Clé API Anthropic
Configurée dans auth-profiles.json (même clé que le PC de Gilles)

## Panel ISPConfig

- **URL** : https://vps116827.serveur-vps.net:8080
- **User** : admin
- **Password** : `[À récupérer via LWS]`

## Mission

Héberger l'équipe d'agents IA "Oscar & Associés" :
- **Oscar** — Agent principal, bras droit de Gilles
- **Agent Commercial** — Prospection LinkedIn/Email
- **Agents Clients** — Un par cabinet d'avocat (futur)

## Stack installée

- [x] Node.js 22.22.0 LTS
- [x] npm
- [x] OpenClaw 2026.2.2-3 (global)
- [x] Service systemd avec linger (auto-restart)
- [x] Port 18789 ouvert dans firewall LWS
- [x] Chromium 144.0.7559.109 headless
- [x] Fichiers workspace synchronisés (SOUL.md, MEMORY.md, clients, etc.)
- [ ] Certificat SSL (Let's Encrypt) — optionnel pour HTTPS

## Avantages vs PC local

- ✅ 24/7 autonome (pas de dépendance au PC de Gilles)
- ✅ IP fixe pour webhooks
- ✅ Service systemd avec auto-restart
- ✅ Accessible depuis Internet
- ⏳ Chrome headless à installer pour browser automation

## ⚠️ URGENT

**Le VPS expire le 09-02-2026** (dans 5 jours)
→ Penser à renouveler !

## Prochaines étapes

1. [ ] Configurer les workspace files (SOUL.md, AGENTS.md, etc.)
2. [ ] Connecter WhatsApp (nouveau numéro dédié Oscar VPS)
3. [ ] Installer Chrome headless
4. [ ] Configurer HTTPS (optionnel)
5. [ ] **RENOUVELER LE VPS AVANT LE 09/02 !**

---
*Créé le 04-02-2026*
*Mis à jour le 04-02-2026 10:50 — Gateway opérationnel !*
