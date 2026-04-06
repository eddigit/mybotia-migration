#!/bin/bash
# Cron D — Vérification taille des MEMORY.md agents (toutes les 6h)
# Alerte si approche la limite de 20000 chars

set -a; source "$HOME/.jacques-env" 2>/dev/null; set +a

WARN_THRESHOLD=18000
CRIT_THRESHOLD=19500

send_telegram() {
    local msg="$1"
    curl -sf "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        --data-urlencode "text=${msg}" \
        > /dev/null 2>&1
}

check_memory() {
    local name="$1"
    local path="$2"

    if [ ! -f "$path" ]; then
        echo "$(date '+%Y-%m-%dT%H:%M') SKIP MEMORY ${name} — fichier inexistant: ${path}"
        return
    fi

    local size
    size=$(wc -c < "$path" 2>/dev/null || echo 0)

    if [ "$size" -ge "$CRIT_THRESHOLD" ]; then
        send_telegram "🔴 CRITIQUE — MEMORY.md ${name} : ${size} chars (limite 20000 — TRUNCATION ACTIVE)"
        echo "$(date '+%Y-%m-%dT%H:%M') CRIT MEMORY ${name} ${size}c"
    elif [ "$size" -ge "$WARN_THRESHOLD" ]; then
        send_telegram "🟡 WARNING — MEMORY.md ${name} : ${size} chars (seuil 18000 — compactage recommandé)"
        echo "$(date '+%Y-%m-%dT%H:%M') WARN MEMORY ${name} ${size}c"
    else
        echo "$(date '+%Y-%m-%dT%H:%M') OK MEMORY ${name} ${size}c"
    fi
}

check_memory "Léa"     "/home/gilles/.openclaw/workspace/MEMORY.md"
check_memory "Julian"  "/home/gilles/.openclaw/workspace-julian/MEMORY.md"
check_memory "Nina"    "/home/gilles/.openclaw/workspace-nina/MEMORY.md"
check_memory "Oscar"   "/home/gilles/.openclaw/workspace-oscar/MEMORY.md"
check_memory "Max"     "/home/gilles/.openclaw-vlmedical/workspace-vlmedical-admin/MEMORY.md"
check_memory "Lucy"    "/home/gilles/.openclaw/workspace-lucy/MEMORY.md"
