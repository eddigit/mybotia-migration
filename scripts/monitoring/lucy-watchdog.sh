#!/bin/bash
# Lucy gateway watchdog — relance si down
# Cron: */5 * * * *
# Corrigé 24/03/2026 : bon chemin config + --port explicite

export PATH="/home/gilles/.npm-global/bin:$PATH"

LUCY_CONFIG="/home/gilles/.openclaw-lucy/openclaw.json"
LUCY_STATE="/home/gilles/.openclaw-lucy"
LUCY_PORT=18795
LUCY_TOKEN="e581649cd03d0d2c17666f2cb82703d02c3109ab08a899de"
LOG="/tmp/lucy-watchdog.log"

HEALTH=$(curl -s --max-time 5 "http://127.0.0.1:${LUCY_PORT}/health" 2>/dev/null)

if echo "$HEALTH" | grep -q '"ok":true'; then
  exit 0
fi

# Lucy est down — log + relance
echo "[$(date -Iseconds)] Lucy gateway DOWN — relance..." >> "$LOG"

# Kill zombie sur le port
kill $(lsof -ti :${LUCY_PORT}) 2>/dev/null
sleep 2

OPENCLAW_HOME="$LUCY_STATE" \
nohup openclaw gateway --port ${LUCY_PORT} > /tmp/lucy-gateway.log 2>&1 &

sleep 8
HEALTH2=$(curl -s --max-time 5 "http://127.0.0.1:${LUCY_PORT}/health" 2>/dev/null)
if echo "$HEALTH2" | grep -q '"ok":true'; then
  echo "[$(date -Iseconds)] Lucy relancée OK (PID $!)" >> "$LOG"
else
  echo "[$(date -Iseconds)] Lucy relance ÉCHOUÉE" >> "$LOG"
fi
