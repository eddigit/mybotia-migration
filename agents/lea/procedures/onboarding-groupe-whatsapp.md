# Procédure Onboarding Nouveau Groupe WhatsApp

## PROTOCOLE AUTOMATIQUE — Quand Gilles crée un groupe et m'ajoute

### Étape 1 — Détecter le JID (IMMÉDIAT)
```bash
grep "g.us" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep "web-inbound" | tail -20
```
Chercher un JID qui n'est PAS dans la liste des groupes configurés.

### Étape 2 — Ajouter à la config
```bash
cd ~/.openclaw && python3 -c "
import json
with open('openclaw.json') as f:
    c = json.load(f)
c['channels']['whatsapp']['groups']['NOUVEAU_JID@g.us'] = {'requireMention': False}
with open('openclaw.json', 'w') as f:
    json.dump(c, f, indent=2)
"
```

### Étape 3 — Redémarrer le gateway
```bash
systemctl --user restart openclaw-gateway
```

### Étape 4 — VÉRIFIER (OBLIGATOIRE avant de confirmer)
1. `systemctl --user is-active openclaw-gateway` → doit dire "active"
2. `grep "NOUVEAU_JID" ~/.openclaw/openclaw.json` → doit exister
3. Attendre un message dans le groupe ET vérifier dans les logs qu'une réponse a été envoyée :
   ```bash
   grep "NOUVEAU_JID" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep "Auto-replied\|Sent chunk"
   ```
4. **SEULEMENT après preuve d'envoi** → confirmer à Gilles

### ⚠️ RÈGLE ABSOLUE
- **JAMAIS** dire "c'est bon" sans avoir vu la preuve dans les logs qu'un message a été envoyé dans le groupe
- Si pas de preuve d'envoi → dire "config ajoutée, en attente de test"
- Le premier "Tu es là ?" de Gilles DOIT recevoir une réponse

### Étape 5 — Enregistrer dans Notion
```bash
bash /home/gilles/.openclaw/scripts/notion-add-client.sh "NOM" "JID@g.us" "TYPE"
```

### Groupes configurés (22 février 2026)
| Groupe | JID |
|--------|-----|
| Cannes Rachel | 120363405038000558@g.us |
| Soutien Xavier | 120363406115931873@g.us |
| Soutien clemsen | 120363406481118458@g.us |
| (anciens) | 120363425931772536, 120363406232810102, 120363426071294259, 120363424693375693, 120363426451963719, 120363407026699197, 120363424470242785, 120363425162106700 |
