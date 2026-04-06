#!/bin/bash
# Cron E — Veille version OpenClaw (toutes les 7h)
# Alerte si nouvelle version disponible

TELEGRAM_TOKEN="<TELEGRAM_BOT_TOKEN_JACQUES>"
CHAT_ID="1801835052"

send_telegram() {
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}&text=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$1'))")&parse_mode=HTML" > /dev/null 2>&1
}

CURRENT=$(openclaw --version 2>/dev/null | grep -oP '\d{4}\.\d+\.\d+[^\s]*' | head -1)
LATEST=$(npm view openclaw version 2>/dev/null)

if [ -z "$CURRENT" ] || [ -z "$LATEST" ]; then
    echo "$(date '+%Y-%m-%dT%H:%M') SKIP check-openclaw version indisponible (current=$CURRENT latest=$LATEST)"
    exit 0
fi

if [ "$CURRENT" != "$LATEST" ]; then
    send_telegram "🟡 INFO — OpenClaw update disponible : ${CURRENT} → ${LATEST}. Planifier upgrade avec Gilles."
    echo "$(date '+%Y-%m-%dT%H:%M') WARN OPENCLAW update ${CURRENT} -> ${LATEST}"
else
    echo "$(date '+%Y-%m-%dT%H:%M') OK OPENCLAW version ${CURRENT} a jour"
fi
