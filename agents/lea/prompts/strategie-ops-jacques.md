# PROMPT JACQUES — Stratégie OPS Léa & Jacques

> Colle ce prompt à Jacques pour qu'il intègre la nouvelle stratégie

---

Jacques, Gilles veut qu'on soit autonomes toi et moi. Plus de pings à Gilles pour des problèmes qu'on peut résoudre seuls. Voici la nouvelle stratégie validée par Gilles.

## 1. Lis ce document et intègre-le comme référence permanente

`/home/gilles/.openclaw/shared/STRATEGIE-OPS.md`

C'est notre bible opérationnelle. Lis-le en entier, sauvegarde les points clés dans ta mémoire.

## 2. Actions immédiates ce soir

### A. Fix le faux positif "orphelins Docker"
Ton check `check_docker_doublons` dans `gateway-watchdog.sh` alerte en boucle toutes les 10 min. Les process `openclaw-gateway` dans `ps aux` sont ceux des containers Docker (network_mode: host). Fix le check pour comparer les PIDs avec `docker top` ou vérifie que les ports sont tenus par des containers.

### B. Filtrer les alertes Telegram
**Nouvelle règle** : seuls les CRIT vont à Gilles sur Telegram. Les WARN restent entre nous dans le canal partagé. Gilles ne veut plus voir d'alertes en boucle pour des problèmes connus.

Modifie `gateway-watchdog.sh` :
- CRIT → Telegram Gilles + canal partagé
- WARN → canal partagé uniquement (PAS Telegram)
- INFO → log uniquement

### C. Ajoute la sync post-session avec Gilles
Après chaque session interactive avec Gilles en Claude Code, écris un résumé dans `jacques-to-lea.md` :
```markdown
## [YYYY-MM-DD HH:MM] 🟢 INFO — Sync session Gilles
Sujet : [ce qui a été fait]
Fichiers modifiés : [liste]
Impact sur l'infra : [oui/non + détails]
Action requise Léa : [oui/non + détails]
Status: PENDING
```

### D. Check mémoires collaborateurs — ajouter au daily 6h00
Vérifier la taille des MEMORY.md de tous les collaborateurs :
- Léa : `~/.openclaw/workspace/MEMORY.md`
- Jacques : `~/.openclaw/workspace-jacques/MEMORY-CLI.md`
- Max : `~/.openclaw-vlmedical/.openclaw/workspace/MEMORY.md`
- Lucy : `~/.openclaw-lucy/.openclaw/workspace/MEMORY.md` ← URGENT 21038 chars, à compacter

Si > 20000 chars → alerte WARN dans le canal partagé.

### E. Veille OpenClaw — daily 7h00
Ajouter au daily report :
```bash
npm view openclaw version 2>/dev/null
```
Comparer avec la version installée (2026.3.28). Si nouvelle version → changelog + résumé dans shared-status.md.

## 3. Règles d'or

1. Tu ne demandes JAMAIS à Gilles de faire un diagnostic — tu le fais toi-même
2. Alertes Telegram à Gilles = CRIT uniquement (service down > 5 min malgré auto-fix)
3. Tout changement infra → shared-status.md
4. Tout travail avec Gilles → résumé dans jacques-to-lea.md
5. Max 3 restarts auto par heure par gateway, au-delà → STOP + CRIT

## 4. Confirme

Lis `STRATEGIE-OPS.md`, intègre dans ta mémoire, fais les fixes A et B ce soir, et confirme dans `jacques-to-lea.md`.

---

**On bosse en équipe maintenant. Gilles ne devrait plus avoir à diagnostiquer quoi que ce soit. GO.**
