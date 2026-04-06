#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# openclaw-veille.sh — Veille automatique OpenClaw (releases + bugs)
# ═══════════════════════════════════════════════════════════════════
# Cron     : 0 6 * * * (1x/jour à 6h)
# Principe : surveiller les nouvelles versions et bugs WhatsApp
#            upstream pour anticiper les problèmes avant qu'ils
#            arrivent sur notre infra.
#
# Bash + curl + jq uniquement. Zéro token Anthropic consommé.
#
# Créé le 04/04/2026 — Jacques, collaborateur IA Coach Digital Paris
# ═══════════════════════════════════════════════════════════════════

set -uo pipefail

# ── CONFIG ──────────────────────────────────────────────────────────

LOG="/home/gilles/scripts/monitoring/logs/veille-openclaw.log"
STATE_FILE="/tmp/openclaw-veille-state.json"
GITHUB_REPO="openclaw/openclaw"
GITHUB_API="https://api.github.com"

# Telegram (charger depuis .jacques-env)
TELEGRAM_TOKEN=""
TELEGRAM_CHAT=""
if [ -f /home/gilles/.jacques-env ]; then
    TELEGRAM_TOKEN=$(grep -m1 'TELEGRAM_BOT_TOKEN' /home/gilles/.jacques-env 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'" || echo "")
    TELEGRAM_CHAT=$(grep -m1 'TELEGRAM_CHAT_ID' /home/gilles/.jacques-env 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'" || echo "")
fi

TS=$(date '+%Y-%m-%d %H:%M:%S')

# ── FONCTIONS ──────────────────────────────────────────────────────

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

send_telegram() {
    [ -z "$TELEGRAM_TOKEN" ] || [ -z "$TELEGRAM_CHAT" ] && return
    curl -sf --max-time 10 "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT}" \
        -d parse_mode="Markdown" \
        --data-urlencode "text=$1" \
        > /dev/null 2>&1 || true
}

init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        echo '{"last_known_version":"","last_alerted_version":"","last_alerted_issues":[]}' > "$STATE_FILE"
    fi
}

get_state_value() {
    jq -r ".$1 // \"\"" "$STATE_FILE" 2>/dev/null || echo ""
}

set_state_value() {
    local tmp
    tmp=$(jq ".$1 = $2" "$STATE_FILE" 2>/dev/null) || return
    echo "$tmp" > "$STATE_FILE"
}

# ── 1. CHECK VERSION ──────────────────────────────────────────────

check_releases() {
    log "Vérification releases..."

    # Version installée
    local installed
    installed=$(openclaw --version 2>/dev/null | grep -oP '[\d]+\.[\d]+\.[\d]+' | head -1 || echo "unknown")
    log "Version installée: ${installed}"

    # Dernières releases GitHub
    local releases_json
    releases_json=$(curl -sf --max-time 15 "${GITHUB_API}/repos/${GITHUB_REPO}/releases?per_page=3" 2>/dev/null)
    if [ -z "$releases_json" ] || [ "$releases_json" = "null" ]; then
        log "ERREUR: impossible de récupérer les releases GitHub"
        return
    fi

    # Dernière version stable (pas pre-release)
    local latest_tag latest_name latest_url
    latest_tag=$(echo "$releases_json" | jq -r '[.[] | select(.prerelease == false)][0].tag_name // ""' 2>/dev/null)
    latest_name=$(echo "$releases_json" | jq -r '[.[] | select(.prerelease == false)][0].name // ""' 2>/dev/null)
    latest_url=$(echo "$releases_json" | jq -r '[.[] | select(.prerelease == false)][0].html_url // ""' 2>/dev/null)

    if [ -z "$latest_tag" ]; then
        log "Aucune release stable trouvée"
        return
    fi

    # Extraire le numéro de version du tag (supprimer le 'v' initial si présent)
    local latest_version
    latest_version=$(echo "$latest_tag" | sed 's/^v//')
    log "Dernière version stable: ${latest_version} (${latest_tag})"

    # Comparer avec la version installée
    if [ "$latest_version" != "$installed" ]; then
        local already_alerted
        already_alerted=$(get_state_value "last_alerted_version")

        if [ "$latest_version" != "$already_alerted" ]; then
            log "NOUVELLE VERSION disponible: ${latest_version} (installé: ${installed})"

            # Extraire le changelog (premiers 500 chars)
            local changelog
            changelog=$(echo "$releases_json" | jq -r '[.[] | select(.prerelease == false)][0].body // "Pas de changelog"' 2>/dev/null | head -20 | cut -c1-500)

            # Chercher si le changelog mentionne des fixes WhatsApp
            local wa_fixes=""
            if echo "$changelog" | grep -qi "whatsapp\|baileys\|credentials\|499\|reconnect"; then
                wa_fixes="\n\n*Contient des fixes WhatsApp !*"
            fi

            send_telegram "🆕 *OpenClaw ${latest_version}* disponible (installé: ${installed})

${latest_name}
${latest_url}${wa_fixes}

Changelog (extrait):
\`\`\`
$(echo "$changelog" | head -10)
\`\`\`"

            set_state_value "last_alerted_version" "\"${latest_version}\""
            log "Alerte Telegram envoyée pour version ${latest_version}"
        else
            log "Version ${latest_version} déjà signalée"
        fi
    else
        log "Version à jour (${installed})"
    fi

    set_state_value "last_known_version" "\"${latest_version}\""
}

# ── 2. CHECK BUGS WHATSAPP ────────────────────────────────────────

check_whatsapp_bugs() {
    log "Vérification bugs WhatsApp..."

    # Issues ouvertes taguées "bug" créées dans les dernières 48h
    local since
    since=$(date -u -d '2 days ago' '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u -v-2d '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo "")
    if [ -z "$since" ]; then
        log "ERREUR: impossible de calculer la date since"
        return
    fi

    local issues_json
    issues_json=$(curl -sf --max-time 15 "${GITHUB_API}/repos/${GITHUB_REPO}/issues?labels=bug&state=open&since=${since}&per_page=20" 2>/dev/null)
    if [ -z "$issues_json" ] || [ "$issues_json" = "null" ]; then
        log "ERREUR: impossible de récupérer les issues GitHub"
        return
    fi

    local total_bugs=0
    total_bugs=$(echo "$issues_json" | jq 'length' 2>/dev/null) || true
    log "Bugs ouverts (48h): ${total_bugs}"

    if [ "$total_bugs" -eq 0 ]; then
        log "Aucun nouveau bug dans les 48 dernières heures"
        return
    fi

    # Filtrer les issues liées à WhatsApp/Baileys/credentials
    local wa_bugs
    wa_bugs=$(echo "$issues_json" | jq -r '[.[] | select(
        (.title | test("(?i)whatsapp|baileys|credential|499|reconnect|disconnect")) or
        (.labels[]?.name | test("(?i)whatsapp"))
    )] | length' 2>/dev/null) || true

    log "Bugs WhatsApp (48h): ${wa_bugs}"

    if [ "$wa_bugs" -gt 0 ]; then
        # Lister les bugs WhatsApp
        local bug_list
        bug_list=$(echo "$issues_json" | jq -r '.[] | select(
            (.title | test("(?i)whatsapp|baileys|credential|499|reconnect|disconnect")) or
            (.labels[]?.name | test("(?i)whatsapp"))
        ) | "• #\(.number): \(.title)"' 2>/dev/null | head -5)

        # Vérifier si on a déjà alerté pour ces issues
        local new_issue_numbers
        new_issue_numbers=$(echo "$issues_json" | jq -r '.[] | select(
            (.title | test("(?i)whatsapp|baileys|credential|499|reconnect|disconnect")) or
            (.labels[]?.name | test("(?i)whatsapp"))
        ) | .number' 2>/dev/null)

        local already_alerted
        already_alerted=$(jq -r '.last_alerted_issues | join(",")' "$STATE_FILE" 2>/dev/null || echo "")

        local new_bugs=""
        local new_ids=()
        while IFS= read -r issue_num; do
            [ -z "$issue_num" ] && continue
            if ! echo ",$already_alerted," | grep -q ",${issue_num},"; then
                new_bugs="1"
                new_ids+=("$issue_num")
            fi
        done <<< "$new_issue_numbers"

        if [ -n "$new_bugs" ]; then
            send_telegram "🐛 *${wa_bugs} nouveau(x) bug(s) WhatsApp* sur OpenClaw (48h)

${bug_list}

Vérifier si notre infra est impactée.
https://github.com/${GITHUB_REPO}/issues?q=is%3Aissue+is%3Aopen+label%3Abug"

            # Mettre à jour les issues déjà alertées
            local all_ids
            all_ids=$(echo "$issues_json" | jq '[.[] | select(
                (.title | test("(?i)whatsapp|baileys|credential|499|reconnect|disconnect")) or
                (.labels[]?.name | test("(?i)whatsapp"))
            ) | .number]' 2>/dev/null)
            set_state_value "last_alerted_issues" "$all_ids"

            log "Alerte Telegram envoyée: ${wa_bugs} bugs WhatsApp"
        else
            log "Bugs WhatsApp déjà signalés"
        fi
    fi

    # Log tous les bugs récents (même non-WhatsApp) pour référence
    if [ "$total_bugs" -gt 0 ]; then
        log "--- Tous les bugs (48h) ---"
        echo "$issues_json" | jq -r '.[] | "[#\(.number)] \(.title) (\(.labels | map(.name) | join(", ")))"' 2>/dev/null \
            | while IFS= read -r line; do log "  $line"; done
        log "--- Fin bugs ---"
    fi
}

# ── 3. CHECK FIXES PERTINENTS ─────────────────────────────────────
# Vérifie si des PRs récemment mergées concernent nos bugs connus

check_relevant_fixes() {
    log "Vérification fixes pertinents..."

    # Nos bugs connus (référencés dans CLAUDE.md)
    local known_bugs=("56054" "55030" "47142")

    local closed_json
    closed_json=$(curl -sf --max-time 15 "${GITHUB_API}/repos/${GITHUB_REPO}/issues?state=closed&labels=bug&per_page=10&sort=updated&direction=desc" 2>/dev/null)
    if [ -z "$closed_json" ] || [ "$closed_json" = "null" ]; then
        log "Impossible de récupérer les issues fermées"
        return
    fi

    local fixes_found=""
    for bug_id in "${known_bugs[@]}"; do
        local is_closed
        is_closed=$(echo "$closed_json" | jq -r ".[] | select(.number == ${bug_id}) | .state" 2>/dev/null)
        if [ "$is_closed" = "closed" ]; then
            local closed_at
            closed_at=$(echo "$closed_json" | jq -r ".[] | select(.number == ${bug_id}) | .closed_at" 2>/dev/null)
            # Vérifier si fermé dans les dernières 48h
            local closed_ts
            closed_ts=$(date -d "$closed_at" +%s 2>/dev/null || echo "0")
            local now_ts
            now_ts=$(date +%s)
            if [ $((now_ts - closed_ts)) -lt 172800 ]; then
                local title
                title=$(echo "$closed_json" | jq -r ".[] | select(.number == ${bug_id}) | .title" 2>/dev/null)
                fixes_found="${fixes_found}• #${bug_id}: ${title}\n"
                log "FIX DETECTE: #${bug_id} fermé le ${closed_at}"
            fi
        fi
    done

    if [ -n "$fixes_found" ]; then
        send_telegram "✅ *Fix upstream détecté* pour nos bugs connus !

${fixes_found}
Envisager une mise à jour OpenClaw."
        log "Alerte fix upstream envoyée"
    else
        log "Aucun fix récent pour nos bugs connus"
    fi
}

# ── 4. ROTATION LOG ───────────────────────────────────────────────

rotate_log() {
    [ -f "$LOG" ] || return
    local lines
    lines=$(wc -l < "$LOG" 2>/dev/null || echo "0")
    if [ "$lines" -gt 5000 ]; then
        tail -2000 "$LOG" > "${LOG}.tmp" && mv "${LOG}.tmp" "$LOG"
    fi
}

# ── MAIN ───────────────────────────────────────────────────────────

init_state

log "=== Veille OpenClaw ==="

check_releases
check_whatsapp_bugs
check_relevant_fixes

log "=== Fin veille ==="

rotate_log
