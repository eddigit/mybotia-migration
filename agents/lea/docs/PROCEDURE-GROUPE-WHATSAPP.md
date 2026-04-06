# PROCÉDURE — Créer un groupe WhatsApp client avec Léa

**Auteur :** Iris  
**Date :** 12 février 2026  
**Validé par :** Gilles (groupe Hugo fonctionnel)

---

## Prérequis

1. **Gateway VPS opérationnel** — vérifier avec :
   ```bash
   ssh oscar@180.149.198.23 'lsof -ti:18789 && curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/health'
   ```
   Résultat attendu : PID + "200"

2. **WhatsApp connecté** — vérifier dans les logs :
   ```bash
   ssh oscar@180.149.198.23 'tail -20 ~/.openclaw/gateway.log | grep -i whatsapp'
   ```
   Doit montrer "Listening for personal WhatsApp inbound messages"

3. **Config groupes activée** dans `~/.openclaw/openclaw.json` :
   ```json
   "channels": {
     "whatsapp": {
       "groupPolicy": "allowlist",
       "groupAllowFrom": ["+33652345180"],
       "groups": {
         "*": { "requireMention": false }
       },
       "ackReaction": {
         "emoji": "👀",
         "direct": true,
         "group": "always"
       }
     }
   }
   ```

---

## Étapes (5 minutes)

### Étape 1 — Créer le groupe (téléphone Gilles)

1. Ouvrir WhatsApp sur le téléphone (+33 6 52 34 51 80)
2. Créer un nouveau groupe
3. Ajouter le bot : **+33 7 56 96 86 33**
4. Nommer le groupe (ex: "Accompagnement [Nom Client]")
5. **NE PAS ajouter le client encore**

### Étape 2 — Tester (téléphone Gilles)

1. Envoyer "Test" dans le groupe
2. Attendre :
   - Réaction 👀 sur le message (confirmation visuelle)
   - Réponse de Léa

**Si Léa ne répond pas :**
```bash
ssh oscar@180.149.198.23 'tail -20 ~/.openclaw/gateway.log | grep -i "group\|inbound"'
```

### Étape 3 — Récupérer le JID (optionnel)

```bash
ssh oscar@180.149.198.23 'tail -50 ~/.openclaw/gateway.log | grep "g.us" | tail -5'
```
Le JID est au format `XXXXXXXXXXXXXXXXXX@g.us`

### Étape 4 — Ajouter le client

1. Ouvrir le groupe
2. Ajouter le numéro du client
3. Le client reçoit l'invitation
4. Quand le client envoie un message, Léa répond automatiquement

---

## Troubleshooting

### WhatsApp déconnecté

**Symptôme :** Pas de réaction 👀, pas de réponse

**Diagnostic :**
```bash
ssh oscar@180.149.198.23 'tail -50 ~/.openclaw/gateway.log | grep -iE "whatsapp|error|timeout"'
```

**Si timeout/déconnexion :**
```bash
ssh oscar@180.149.198.23 'pkill -9 openclaw; sleep 3; nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &'
```
Attendre 30 secondes, puis retester.

### Gateway down

**Diagnostic :**
```bash
ssh oscar@180.149.198.23 'lsof -ti:18789 || echo "Gateway DOWN"'
```

**Relance :**
```bash
ssh oscar@180.149.198.23 'rm -f ~/.openclaw/*.lock; nohup openclaw gateway > ~/.openclaw/gateway.log 2>&1 &'
```

### Config invalide

**Vérifier :**
```bash
ssh oscar@180.149.198.23 'tail -20 ~/.openclaw/gateway.log | grep -i "invalid config"'
```

**Si erreur ackReaction.group :** Doit être "always", "mentions", ou "never" (PAS "all")

---

## Groupes actifs

| Nom | JID | Client | Date création |
|-----|-----|--------|---------------|
| Accompagnement Hugo | 120363406361914483@g.us | Hugo (fils) | 12/02/2026 |

---

## Ce qui a fait marcher le groupe Hugo

1. **Gateway déjà UP** (PID 439390)
2. **WhatsApp connecté** depuis 14:21
3. **Config correcte** : `groups: { "*": { requireMention: false } }`
4. **ackReaction.group: "always"** (corrigé de "all")
5. **Gilles dans groupAllowFrom** : `["+33652345180"]`

**Temps entre création groupe et première réponse Léa : ~30 secondes**

---

*Dernière mise à jour : 12 février 2026, 15:24*
