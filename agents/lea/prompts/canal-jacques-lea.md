# PROMPT JACQUES — Canal de communication avec Léa

> Colle ce prompt à Jacques pour activer le canal partagé

---

Jacques, on met en place un canal de communication direct entre toi et Léa. Plus besoin de passer par Gilles pour se coordonner.

## Le canal

Dossier partagé : `/home/gilles/.openclaw/shared/`

| Fichier | Usage |
|---------|-------|
| `lea-to-jacques.md` | Messages de Léa pour toi — **lis-le à chaque check** |
| `jacques-to-lea.md` | Tes messages pour Léa — **écris ici** |
| `shared-status.md` | État infra partagé — mis à jour par les deux |
| `README.md` | Protocole complet |

## Ce que tu dois faire

### 1. Lire `lea-to-jacques.md` à chaque routine de check (toutes les 15 min)
- Si un message a Status: PENDING → le traiter
- Répondre dans `jacques-to-lea.md` avec le même format
- Marquer le message original comme ACK ou DONE

### 2. Écrire dans `jacques-to-lea.md` quand tu as besoin de Léa
Exemples :
- "Gateway mybotia redémarrée, vérifie que WhatsApp est stable de ton côté"
- "Alerte RAM — Léa, préviens Gilles"
- "Pre-keys purgées, 6975 → 1300"

### 3. Mettre à jour `shared-status.md` après chaque action infra
- Changement de status gateway
- Incident résolu
- Action effectuée

### Format des messages
```
## [YYYY-MM-DD HH:MM] PRIORITÉ — Sujet
Corps du message.
Status: PENDING | ACK | DONE
```

Priorités : 🔴 CRIT | 🟡 WARN | 🟢 INFO

### 4. Mettre à jour ton HEARTBEAT ou ta routine cron
Ajoute la lecture de `lea-to-jacques.md` dans ta routine de check toutes les 15 minutes.

## Règles

- Ce canal ne remplace PAS les alertes Telegram à Gilles pour les CRIT
- Gilles reste le décideur — ce canal c'est pour la coordination opérationnelle entre nous
- Ne pas supprimer les messages — marquer DONE et archiver en fin de journée

## Premier message

Il y a déjà un message de Léa dans `lea-to-jacques.md`. Lis-le et réponds dans `jacques-to-lea.md`.

---

**C'est simple, c'est un tableau de post-its entre collègues. GO.**
