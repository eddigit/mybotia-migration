#!/bin/bash
# Lucy Morning Briefing — Envoi quotidien à 8h00
# Cron: 0 8 * * * /home/gilles/scripts/monitoring/lucy-morning-briefing.sh

export PATH="/home/gilles/.npm-global/bin:$PATH"
export CLAUDE_CODE_OAUTH_TOKEN="<ANTHROPIC_OAUTH_TOKEN>"

LUCY_TOKEN="e581649cd03d0d2c17666f2cb82703d02c3109ab08a899de"
LUCY_URL="ws://127.0.0.1:18795"
GROUP_INITIATION="120363407877862678@g.us"

# Vérifier que Lucy est en ligne
HEALTH=$(curl -s --max-time 5 http://127.0.0.1:18795/health 2>/dev/null)
if ! echo "$HEALTH" | grep -q '"ok":true'; then
  echo "[$(date -Iseconds)] Lucy DOWN — briefing annulé" >> /tmp/lucy-briefing.log
  exit 1
fi

# Envoyer le prompt de briefing matinal à Lucy via le groupe Initiation
openclaw gateway call send \
  --token "$LUCY_TOKEN" \
  --url "$LUCY_URL" \
  --params "{\"channel\":\"whatsapp\",\"to\":\"$GROUP_INITIATION\",\"message\":\"📋 BRIEFING MATINAL — Bonjour Gilles, voici mon point du matin. Résume ce que tu as appris hier (nouveaux contacts, infos établissements, recherches web, échanges dans les groupes). Liste les points d'attention et les questions en suspens.\",\"idempotencyKey\":\"briefing-$(date +%Y%m%d)\"}" \
  --json 2>/dev/null

echo "[$(date -Iseconds)] Briefing matinal envoyé" >> /tmp/lucy-briefing.log
