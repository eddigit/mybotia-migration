#!/bin/bash
# Lucy Hourly Research — Recherches continues toutes les heures
# Cron: 0 * * * * /home/gilles/scripts/monitoring/lucy-hourly-research.sh

export PATH="/home/gilles/.npm-global/bin:$PATH"
export CLAUDE_CODE_OAUTH_TOKEN="<ANTHROPIC_OAUTH_TOKEN>"

LUCY_TOKEN="e581649cd03d0d2c17666f2cb82703d02c3109ab08a899de"
LUCY_URL="ws://127.0.0.1:18795"
LUCY_DM="33652345180@s.whatsapp.net"

# Vérifier que Lucy est en ligne
HEALTH=$(curl -s --max-time 5 http://127.0.0.1:18795/health 2>/dev/null)
if ! echo "$HEALTH" | grep -q '"ok":true'; then
  echo "[$(date -Iseconds)] Lucy DOWN — recherche annulée" >> /tmp/lucy-research.log
  exit 1
fi

# Pas de recherche entre 23h et 7h (pas besoin de spammer la nuit)
HOUR=$(date +%H)
if [ "$HOUR" -ge 23 ] || [ "$HOUR" -lt 7 ]; then
  exit 0
fi

# Envoyer un prompt de recherche silencieux à Lucy en DM (pas dans le groupe)
openclaw gateway call send \
  --token "$LUCY_TOKEN" \
  --url "$LUCY_URL" \
  --params "{\"channel\":\"whatsapp\",\"to\":\"$LUCY_DM\",\"message\":\"🔍 RECHERCHE CONTINUE — Continue tes recherches sur IGH. Cherche de nouvelles infos sur : les directeurs d'établissements, les profils LinkedIn/web de M. Imbert et M. Cozon, les actualités récentes du groupe, les établissements individuels, les avis en ligne, les meilleures pratiques EHPAD. Mets à jour ta mémoire MEMORY.md avec ce que tu trouves. Ne réponds pas dans le groupe, travaille en silence.\",\"idempotencyKey\":\"research-$(date +%Y%m%d-%H)\"}" \
  --json 2>/dev/null

echo "[$(date -Iseconds)] Recherche horaire lancée" >> /tmp/lucy-research.log
