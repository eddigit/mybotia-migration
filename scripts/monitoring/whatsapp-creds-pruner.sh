#!/bin/bash
# whatsapp-creds-pruner.sh — Purge automatique credentials WhatsApp (toutes gateways)
# Basé sur PR #26625 (openclaw/openclaw) — seuil 500, garde 100
# Auto-découverte : scanne ~/.openclaw*/credentials/whatsapp/*/
# Cron: */30 * * * * /home/gilles/scripts/monitoring/whatsapp-creds-pruner.sh
#
# Références:
#   - Issue #56054: boucle 499 causée par accumulation credentials
#   - PR #26625: pruneStaleCredentials() — seuil 500, garde 100 par mtime

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/monitoring.conf" 2>/dev/null

THRESHOLD=200    # Seuil d'alerte et de purge (PR #26625)
KEEP=100         # Nombre de fichiers récents à conserver par type
WARN_THRESHOLD=150  # Alerte préventive avant le seuil critique
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')] [creds-pruner]"

PRUNABLE_PATTERNS=("pre-key-*" "sender-key-*" "session-*")

count_prunables() {
    local dir="$1"
    local count=0
    for pattern in "${PRUNABLE_PATTERNS[@]}"; do
        count=$((count + $(ls -1 "$dir"/$pattern 2>/dev/null | wc -l)))
    done
    echo "$count"
}

process_dir() {
    local creds_dir="$1"
    local profile_dir account label prunable_count

    profile_dir=$(echo "$creds_dir" | grep -oP '\.openclaw[^/]*')
    account=$(basename "$creds_dir")
    label="${profile_dir}/${account}"

    prunable_count=$(count_prunables "$creds_dir")

    if [ "$prunable_count" -ge "$THRESHOLD" ]; then
        echo "${LOG_PREFIX} 🔴 ${label}: ${prunable_count} fichiers prunables (seuil: ${THRESHOLD}) — PURGE"

        for pattern in "${PRUNABLE_PATTERNS[@]}"; do
            local count before after deleted
            count=$(ls -1 "$creds_dir"/$pattern 2>/dev/null | wc -l)
            if [ "$count" -gt "$KEEP" ]; then
                before=$count
                ls -t "$creds_dir"/$pattern 2>/dev/null | tail -n +$((KEEP + 1)) | xargs rm -f
                after=$(ls -1 "$creds_dir"/$pattern 2>/dev/null | wc -l)
                deleted=$((before - after))
                TOTAL_PURGED=$((TOTAL_PURGED + deleted))
                echo "${LOG_PREFIX}   ${pattern}: ${before} → ${after} (supprimé ${deleted})"
            fi
        done

        ALERTS="${ALERTS}🔴 ${label}: ${prunable_count} fichiers → purgé (garde ${KEEP})\n"

    elif [ "$prunable_count" -ge "$WARN_THRESHOLD" ]; then
        echo "${LOG_PREFIX} 🟡 ${label}: ${prunable_count} fichiers prunables (approche seuil ${THRESHOLD})"
        ALERTS="${ALERTS}🟡 ${label}: ${prunable_count} fichiers (seuil warn: ${WARN_THRESHOLD})\n"

    else
        echo "${LOG_PREFIX} ✅ ${label}: ${prunable_count} fichiers prunables (OK)"
    fi
}

# === MAIN ===

TOTAL_PURGED=0
ALERTS=""

# Auto-découverte de TOUS les dossiers credentials WhatsApp
for creds_dir in $(find /home/gilles/.openclaw*/credentials/whatsapp/ -mindepth 1 -maxdepth 1 -type d 2>/dev/null); do
    process_dir "$creds_dir"
done

# Alerte Telegram si purge ou warning
if [ -n "$ALERTS" ]; then
    ALERT_MSG="🧹 WhatsApp Credentials Pruner

${ALERTS}
Total purgé: ${TOTAL_PURGED} fichiers
Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')
Réf: Issue #56054, PR #26625"

    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="${TELEGRAM_CHAT_ID}" \
            --data-urlencode "text=${ALERT_MSG}" > /dev/null 2>&1
    fi
fi

echo "${LOG_PREFIX} Terminé — ${TOTAL_PURGED} fichiers purgés au total"
