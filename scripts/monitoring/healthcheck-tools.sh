#!/bin/bash
# healthcheck-tools.sh v2.0 — Test RÉEL de chaque outil (HOST, pas Docker)
# Migré de docker exec vers exécution directe sur le host
# Usage: ./healthcheck-tools.sh [--quiet] [--json] [--fix]
# Rewrite 03/04/2026 — post-migration systemd

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/monitoring.conf" 2>/dev/null || true
set -a; source "$HOME/.jacques-env" 2>/dev/null; set +a

WORKSPACE="/home/gilles/.openclaw/workspace"
LOGFILE="/home/gilles/scripts/monitoring/logs/healthcheck-tools.log"
QUIET=false
JSON=false
FIX=false
ERRORS=0
WARNINGS=0
RESULTS=()

for arg in "$@"; do
    case $arg in
        --quiet) QUIET=true ;;
        --json) JSON=true ;;
        --fix) FIX=true ;;
    esac
done

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
    if [ "$QUIET" = false ] && [ "$JSON" = false ]; then
        echo "$1"
    fi
}

test_result() {
    local name="$1"
    local status="$2"  # OK, WARN, FAIL
    local detail="$3"
    RESULTS+=("$name|$status|$detail")
    if [ "$status" = "FAIL" ]; then
        ((ERRORS++))
        log "❌ $name: $detail"
    elif [ "$status" = "WARN" ]; then
        ((WARNINGS++))
        log "⚠️  $name: $detail"
    else
        log "✅ $name: $detail"
    fi
}

mkdir -p "$(dirname "$LOGFILE")"
log "========== HEALTHCHECK TOOLS — $(date '+%Y-%m-%d %H:%M:%S') =========="

# 1. Python3
log "--- 1. Python3 ---"
PY_VERSION=$(python3 --version 2>&1) && \
    test_result "Python3" "OK" "$PY_VERSION" || \
    test_result "Python3" "FAIL" "Python3 absent"

# 2. Imports Python critiques
log "--- 2. Imports Python ---"
IMPORTS=$(python3 -c "
import requests; import google.auth; import reportlab
print('requests+google.auth+reportlab OK')
" 2>&1) && \
    test_result "Python-imports" "OK" "$IMPORTS" || \
    test_result "Python-imports" "FAIL" "Import échoué: $IMPORTS"

# 3. Gmail lecture (vrai appel)
log "--- 3. Gmail ---"
GMAIL=$(python3 "$WORKSPACE/tools/read_emails.py" 1 2>&1 | head -3)
if echo "$GMAIL" | grep -qi "email\|trouv"; then
    test_result "Gmail-read" "OK" "Lecture OK"
elif echo "$GMAIL" | grep -qi "error\|token\|expired\|invalid"; then
    test_result "Gmail-read" "FAIL" "Erreur: $(echo "$GMAIL" | head -1)"
else
    test_result "Gmail-read" "WARN" "Réponse inattendue: $(echo "$GMAIL" | head -1)"
fi

# 4. Qonto (vrai appel — solde)
log "--- 4. Qonto ---"
QONTO=$(python3 "$WORKSPACE/tools/qonto.py" balance 2>&1 | head -5)
if echo "$QONTO" | grep -qi "solde\|balance\|iban\|EUR\|nom"; then
    test_result "Qonto" "OK" "API répond"
elif echo "$QONTO" | grep -qi "error\|unauthorized\|401\|403"; then
    test_result "Qonto" "FAIL" "Erreur API: $(echo "$QONTO" | head -1)"
else
    test_result "Qonto" "WARN" "Réponse: $(echo "$QONTO" | head -1)"
fi

# 5. Judilibre (vrai appel API PISTE)
log "--- 5. Judilibre ---"
JUDI=$(python3 "$WORKSPACE/tools/legal_search.py" judilibre "test" 2>&1 | head -5)
if echo "$JUDI" | grep -qi "résultat"; then
    test_result "Judilibre" "OK" "$(echo "$JUDI" | grep -i 'résultat' | head -1)"
elif echo "$JUDI" | grep -qi "error\|token\|401\|403"; then
    test_result "Judilibre" "FAIL" "Erreur API: $(echo "$JUDI" | head -1)"
else
    test_result "Judilibre" "WARN" "$(echo "$JUDI" | head -1)"
fi

# 6. Légifrance (vrai appel API PISTE)
log "--- 6. Légifrance ---"
LEGI=$(python3 "$WORKSPACE/tools/legal_search.py" legifrance "code civil" 2>&1 | head -5)
if echo "$LEGI" | grep -qi "résultat" && ! echo "$LEGI" | grep -q "0 résultat"; then
    test_result "Legifrance" "OK" "$(echo "$LEGI" | grep -i 'résultat' | head -1)"
elif echo "$LEGI" | grep -q "0 résultat"; then
    test_result "Legifrance" "WARN" "0 résultats retournés — API potentiellement dégradée"
else
    test_result "Legifrance" "FAIL" "$(echo "$LEGI" | head -1)"
fi

# 7. Facturation (test dry-run / import)
log "--- 7. Facturation ---"
INVOICE=$(python3 -c "
import sys; sys.path.insert(0, '$WORKSPACE/tools')
from reportlab.lib.pagesizes import A4
print('reportlab import + A4 OK')
" 2>&1) && \
    test_result "Facturation" "OK" "$INVOICE" || \
    test_result "Facturation" "FAIL" "reportlab cassé: $INVOICE"

# 8. Notion API
log "--- 8. Notion ---"
NOTION_TOKEN=$(cat /home/gilles/.openclaw/credentials/notion 2>/dev/null || echo "")
if [ -n "$NOTION_TOKEN" ]; then
    NOTION=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" "https://api.notion.com/v1/users/me" 2>&1)
    NOTION_CODE=$(echo "$NOTION" | tail -1)
    if [ "$NOTION_CODE" = "200" ]; then
        test_result "Notion" "OK" "API répond (HTTP 200)"
    else
        test_result "Notion" "FAIL" "HTTP $NOTION_CODE"
    fi
else
    test_result "Notion" "WARN" "Token non trouvé dans credentials/notion"
fi

# 9. Brave Search
log "--- 9. Brave Search ---"
BRAVE_KEY="${BRAVE_API_KEY:-<BRAVE_SEARCH_API_KEY>}"
BRAVE=$(curl -s -w "\n%{http_code}" -H "X-Subscription-Token: $BRAVE_KEY" "https://api.search.brave.com/res/v1/web/search?q=test&count=1" 2>&1)
BRAVE_CODE=$(echo "$BRAVE" | tail -1)
if [ "$BRAVE_CODE" = "200" ]; then
    test_result "BraveSearch" "OK" "API répond (HTTP 200)"
else
    test_result "BraveSearch" "FAIL" "HTTP $BRAVE_CODE"
fi

# 10. Skills discovery
log "--- 10. Skills ---"
SKILLS_COUNT=$(find "$WORKSPACE/skills" -name "SKILL.md" 2>/dev/null | wc -l)
if [ "$SKILLS_COUNT" -ge 4 ]; then
    test_result "Skills" "OK" "$SKILLS_COUNT skills découverts"
elif [ "$SKILLS_COUNT" -gt 0 ]; then
    test_result "Skills" "WARN" "Seulement $SKILLS_COUNT skills (attendu: 4+)"
else
    test_result "Skills" "FAIL" "Aucun skill trouvé"
fi

# 11. Gateways health (via systemd + HTTP)
log "--- 11. Gateways ---"
for gw in "mybotia:18789:openclaw-gateway.service" "vlmedical:18790:openclaw-gateway-vlmedical.service" "lucy:18795:openclaw-gateway-lucy.service"; do
    IFS=':' read -r gw_name gw_port gw_unit <<< "$gw"
    gw_state=$(systemctl --user is-active "$gw_unit" 2>/dev/null)
    if [ "$gw_state" = "active" ] && curl -sf --max-time 5 "http://127.0.0.1:${gw_port}/health" > /dev/null 2>&1; then
        test_result "Gateway-${gw_name}" "OK" "systemd active + health OK"
    elif [ "$gw_state" = "active" ]; then
        test_result "Gateway-${gw_name}" "WARN" "systemd active mais health check échoué"
    else
        test_result "Gateway-${gw_name}" "FAIL" "systemd: ${gw_state}"
    fi
done

# === RÉSUMÉ ===
log "=================================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    log "🟢 TOUT OK — ${#RESULTS[@]} tests passés"
elif [ $ERRORS -eq 0 ]; then
    log "🟡 $WARNINGS WARNING(S) — $ERRORS erreur(s) sur ${#RESULTS[@]} tests"
else
    log "🔴 $ERRORS ERREUR(S) CRITIQUE(S) — $WARNINGS warning(s) sur ${#RESULTS[@]} tests"
fi
log "=================================================="

# JSON output
if [ "$JSON" = true ]; then
    echo "{"
    echo "  \"timestamp\": \"$(date -Iseconds)\","
    echo "  \"errors\": $ERRORS,"
    echo "  \"warnings\": $WARNINGS,"
    echo "  \"total\": ${#RESULTS[@]},"
    echo "  \"results\": ["
    first=true
    for r in "${RESULTS[@]}"; do
        IFS='|' read -r name status detail <<< "$r"
        if [ "$first" = true ]; then first=false; else echo ","; fi
        echo -n "    {\"name\": \"$name\", \"status\": \"$status\", \"detail\": \"$(echo "$detail" | sed 's/"/\\"/g')\"}"
    done
    echo ""
    echo "  ]"
    echo "}"
fi

# Alerte si erreurs — via Jacques bot (canal unifié)
if [ $ERRORS -gt 0 ]; then
    ALERT_MSG="🔴 HEALTHCHECK TOOLS — $ERRORS ERREUR(S) sur ${#RESULTS[@]} tests"
    for r in "${RESULTS[@]}"; do
        IFS='|' read -r name status detail <<< "$r"
        if [ "$status" = "FAIL" ]; then
            ALERT_MSG="$ALERT_MSG
❌ $name: $detail"
        fi
    done

    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        curl -sf "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="${TELEGRAM_CHAT_ID}" \
            --data-urlencode "text=${ALERT_MSG}" \
            > /dev/null 2>&1
    fi

    exit 1
fi

exit 0
