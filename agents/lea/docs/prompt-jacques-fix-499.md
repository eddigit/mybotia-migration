# Prompt pour Jacques — Fix boucle 499 + maintenance WhatsApp

> Ce prompt est à donner directement à Jacques (Claude Code / SRE VPS)

---

## Contexte

La gateway mybotia (Léa/Nina WhatsApp) est en boucle de reconnexion status 499 depuis ~06:00 UTC. Diagnostic complet : le dossier credentials WhatsApp est hyper-gonflé (7374 fichiers pour le compte `default`, 1895 pour `nina`). C'est un bug connu OpenClaw (#56054) : Baileys accumule des pre-key/sender-key/session files à chaque reconnexion sans jamais les nettoyer. Au-delà de ~500 fichiers, ça corrompt la session et provoque une boucle 499 auto-entretenue.

Un PR de fix existe (#26625, `pruneStaleCredentials()`) mais n'est pas encore mergé upstream.

## Mission

### Étape 1 — Purger les credentials WhatsApp (PRIORITÉ ABSOLUE)

```bash
# 1. Arrêter la gateway mybotia proprement
docker stop mybotia-gateway

# 2. Backup de sécurité du creds.json (ne pas toucher aux app-state-*)
cp ~/.openclaw/credentials/whatsapp/default/creds.json /tmp/creds-default-backup-$(date +%Y%m%d%H%M).json
cp ~/.openclaw/credentials/whatsapp/nina/creds.json /tmp/creds-nina-backup-$(date +%Y%m%d%H%M).json

# 3. Purger les pre-key, sender-key, session obsolètes
# Compte default (Léa) — 7374 fichiers → garder les 100 plus récents
cd ~/.openclaw/credentials/whatsapp/default/
ls -t pre-key-*.json 2>/dev/null | tail -n +101 | xargs rm -f
ls -t sender-key-*.json 2>/dev/null | tail -n +101 | xargs rm -f
ls -t session-*.json 2>/dev/null | tail -n +101 | xargs rm -f

# Compte nina — 1895 fichiers → même traitement
cd ~/.openclaw/credentials/whatsapp/nina/
ls -t pre-key-*.json 2>/dev/null | tail -n +101 | xargs rm -f
ls -t sender-key-*.json 2>/dev/null | tail -n +101 | xargs rm -f
ls -t session-*.json 2>/dev/null | tail -n +101 | xargs rm -f

# 4. Vérifier le résultat
echo "default: $(find ~/.openclaw/credentials/whatsapp/default/ -type f | wc -l) fichiers"
echo "nina: $(find ~/.openclaw/credentials/whatsapp/nina/ -type f | wc -l) fichiers"
# Attendu : ~100-150 chacun

# 5. Redémarrer la gateway
docker start mybotia-gateway

# 6. Vérifier que la boucle 499 s'est arrêtée (attendre 2-3 min)
sleep 180
docker logs mybotia-gateway --tail 30 2>&1 | grep -i "499\|connected\|disconnect"
```

**Si la boucle 499 persiste après purge** (peu probable mais possible) :
```bash
# Option B : supprimer creds.json et forcer re-pairing
docker stop mybotia-gateway
rm ~/.openclaw/credentials/whatsapp/default/creds.json
docker start mybotia-gateway
# → Récupérer le QR code dans les logs et le faire scanner par Gilles
# docker logs mybotia-gateway 2>&1 | grep -i "qr\|scan\|pair"
```

### Étape 2 — Script de maintenance automatique (cron)

Créer un script de pruning automatique pour éviter que ça se reproduise :

```bash
#!/bin/bash
# /home/gilles/watchdog/scripts/wa-creds-prune.sh
# Purge les credentials WhatsApp quand ils dépassent 500 fichiers
# À exécuter via cron toutes les 6h

THRESHOLD=500
KEEP=100
LOG="/home/gilles/watchdog/logs/wa-creds-prune.log"

for ACCOUNT_DIR in ~/.openclaw/credentials/whatsapp/*/; do
    ACCOUNT=$(basename "$ACCOUNT_DIR")
    COUNT=$(find "$ACCOUNT_DIR" -name "pre-key-*.json" -o -name "sender-key-*.json" -o -name "session-*.json" | wc -l)
    
    if [ "$COUNT" -gt "$THRESHOLD" ]; then
        echo "[$(date -Iseconds)] $ACCOUNT: $COUNT fichiers (seuil: $THRESHOLD) — purge..." >> "$LOG"
        
        cd "$ACCOUNT_DIR"
        for PATTERN in "pre-key-*.json" "sender-key-*.json" "session-*.json"; do
            ls -t $PATTERN 2>/dev/null | tail -n +$((KEEP + 1)) | xargs rm -f 2>/dev/null
        done
        
        NEW_COUNT=$(find "$ACCOUNT_DIR" -name "pre-key-*.json" -o -name "sender-key-*.json" -o -name "session-*.json" | wc -l)
        echo "[$(date -Iseconds)] $ACCOUNT: purgé → $NEW_COUNT fichiers" >> "$LOG"
    fi
done
```

Cron :
```
0 */6 * * * /home/gilles/watchdog/scripts/wa-creds-prune.sh
```

### Étape 3 — Upgrade Max vers Sonnet 4.6

Dans la config VL Medical (`~/.openclaw-vlmedical/openclaw.json` ou équivalent Docker) :
- Remplacer `claude-sonnet-4-5-20250929` par `claude-sonnet-4-6`
- Redémarrer la gateway VL Medical
- Vérifier que le modèle est bien actif

### Étape 4 — Préparer le re-pairing Lucy

Comme tu l'as déjà identifié :
- Purger les creds Lucy si besoin
- Relancer la gateway pour générer le QR
- Attendre que Gilles scanne avec le téléphone Android Lucy

### Étape 5 — Rapport

Après chaque étape, reporter le résultat dans `/home/gilles/.openclaw/shared/jacques-to-lea.md` :
- Nombre de fichiers avant/après purge
- Est-ce que la boucle 499 s'est arrêtée ?
- Modèle Max confirmé en Sonnet 4.6 ?
- QR Lucy prêt à scanner ?

## Contraintes

- **NE PAS supprimer** `creds.json` ni `app-state-sync-*` sauf si Option B nécessaire
- **NE PAS toucher** au compte `vlmedical-admin` (208 fichiers, sous le seuil)
- **Backup avant toute suppression**
- **Documenter** chaque action dans le rapport

## Références

- Issue #56054 : https://github.com/openclaw/openclaw/issues/56054
- PR #26625 : https://github.com/openclaw/openclaw/pulls/26625
- Issue #22511 : https://github.com/openclaw/openclaw/issues/22511
- Notre diagnostic : `~/.openclaw/workspace/docs/diagnostic-30-mars-2026.md`
