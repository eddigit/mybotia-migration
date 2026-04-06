#!/bin/bash
# daily-maintenance.sh — Maintenance quotidienne agents & WhatsApp
# Cron: 0 4 * * * (avant le daily-cleanup.sh de 6h)
# Actions :
#   1. Purge WhatsApp sessions/pre-keys stale (préventif, seuil bas)
#   2. Rotation logs gateways (garder 50K lignes)
#   3. Vérification auth-profiles OAuth (fichiers existent + tokens valides)
#   4. Vérification santé systemd services
#   5. Rapport Telegram résumé

set -a; source "$HOME/.jacques-env" 2>/dev/null; set +a

LOG="/tmp/daily-maintenance.log"
REPORT=""
ISSUES=0

log() { echo "[$(date '+%H:%M:%S')] $1" >> "$LOG"; }
add_report() { REPORT="${REPORT}${1}\n"; }
add_issue() { ISSUES=$((ISSUES + 1)); add_report "⚠️ $1"; }

echo "=== Maintenance quotidienne — $(date '+%Y-%m-%d %H:%M') ===" > "$LOG"
add_report "📋 Maintenance quotidienne — $(date '+%d/%m/%Y')"
add_report ""

# ── 1. Purge préventive WhatsApp credentials ─────────────────────────
log "1. Purge préventive WhatsApp credentials"
add_report "🔑 WhatsApp Credentials"

KEEP=80  # Seuil préventif (vs 100 du pruner réactif)
TOTAL_PRUNED=0

for creds_dir in $(find /home/gilles/.openclaw*/credentials/whatsapp/ -mindepth 1 -maxdepth 1 -type d 2>/dev/null); do
    account=$(basename "$creds_dir")
    profile=$(echo "$creds_dir" | grep -oP '\.openclaw[^/]*')
    label="${profile}/${account}"

    for pattern in pre-key- sender-key- session-; do
        count=$(ls -1 "${creds_dir}/${pattern}"* 2>/dev/null | wc -l)
        if [ "$count" -gt "$KEEP" ]; then
            to_prune=$((count - KEEP))
            # Supprimer les plus anciens (par mtime)
            ls -1t "${creds_dir}/${pattern}"* 2>/dev/null | tail -n "$to_prune" | xargs rm -f 2>/dev/null
            TOTAL_PRUNED=$((TOTAL_PRUNED + to_prune))
            log "  ${label}: purgé ${to_prune} ${pattern}* (gardé ${KEEP})"
        fi
    done
done

if [ "$TOTAL_PRUNED" -gt 0 ]; then
    add_report "  Purgé : ${TOTAL_PRUNED} fichiers stale"
else
    add_report "  ✅ Propre (< ${KEEP} par type)"
fi

# ── 2. Rotation logs gateways ────────────────────────────────────────
log "2. Rotation logs gateways"
add_report ""
add_report "📝 Logs"

MAX_LINES=50000
LOGS_ROTATED=0

for logfile in /tmp/mybotia-gateway.log /tmp/vlmedical-gateway.log /tmp/lucy-gateway.log /tmp/voice-v2.log /tmp/gateway-watchdog.log; do
    if [ -f "$logfile" ]; then
        lines=$(wc -l < "$logfile" 2>/dev/null)
        if [ "${lines:-0}" -gt "$MAX_LINES" ]; then
            tail -n "$MAX_LINES" "$logfile" > "${logfile}.tmp" && mv "${logfile}.tmp" "$logfile"
            LOGS_ROTATED=$((LOGS_ROTATED + 1))
            log "  Tronqué ${logfile}: ${lines} → ${MAX_LINES} lignes"
        fi
    fi
done

if [ "$LOGS_ROTATED" -gt 0 ]; then
    add_report "  Tronqué : ${LOGS_ROTATED} fichiers (> ${MAX_LINES} lignes)"
else
    add_report "  ✅ OK"
fi

# ── 3. Vérification auth-profiles OAuth ──────────────────────────────
log "3. Vérification auth-profiles"
add_report ""
add_report "🔐 OAuth"

AUTH_OK=0
AUTH_FAIL=0

# Scan tous les auth-profiles.json par agent (pas à la racine du profil)
for auth_file in $(find /home/gilles/.openclaw*/agents/*/agent/auth-profiles.json /home/gilles/.openclaw*/.openclaw/agents/*/agent/auth-profiles.json 2>/dev/null | sort -u); do
    # Extraire le label : profil/agent
    agent_name=$(echo "$auth_file" | grep -oP 'agents/\K[^/]+')
    profile_name=$(echo "$auth_file" | grep -oP '\.openclaw[^/]*')
    label="${profile_name}/${agent_name}"

    # Vérifier que le JSON est valide
    if ! python3 -c "import json; json.load(open('$auth_file'))" 2>/dev/null; then
        add_issue "${label}: auth-profiles.json JSON INVALIDE"
        AUTH_FAIL=$((AUTH_FAIL + 1))
        continue
    fi

    # Vérifier qu'il y a au moins un token OAuth anthropic
    token_count=$(python3 -c "
import json
with open('$auth_file') as f:
    data = json.load(f)
profiles = data.get('profiles', {})
if isinstance(profiles, dict):
    count = len([k for k, v in profiles.items() if v.get('key', '').startswith('sk-ant-')])
elif isinstance(profiles, list):
    count = len([p for p in profiles if p.get('key', '').startswith('sk-ant-')])
else:
    count = 0
print(count)
" 2>/dev/null)

    if [ "${token_count:-0}" -eq 0 ]; then
        add_issue "${label}: aucun token OAuth"
        AUTH_FAIL=$((AUTH_FAIL + 1))
    else
        AUTH_OK=$((AUTH_OK + 1))
    fi
done

if [ "$AUTH_FAIL" -eq 0 ]; then
    add_report "  ✅ ${AUTH_OK} profils OK"
fi

# ── 4. Santé services systemd ────────────────────────────────────────
log "4. Vérification services systemd"
add_report ""
add_report "⚙️ Services"

SVC_OK=0
SVC_FAIL=0

for unit in openclaw-gateway.service openclaw-gateway-vlmedical.service openclaw-gateway-lucy.service voice-poc.service; do
    state=$(systemctl --user is-active "$unit" 2>/dev/null)
    if [ "$state" = "active" ]; then
        SVC_OK=$((SVC_OK + 1))
    else
        add_issue "${unit}: état ${state}"
        SVC_FAIL=$((SVC_FAIL + 1))
    fi
done

if [ "$SVC_FAIL" -eq 0 ]; then
    add_report "  ✅ ${SVC_OK}/4 actifs"
fi

# ── 5. Health check gateways ─────────────────────────────────────────
log "5. Health check gateways"
add_report ""
add_report "🏥 Health"

for gw in "mybotia:18789" "vlmedical:18790" "lucy:18795"; do
    name="${gw%%:*}"
    port="${gw##*:}"
    if curl -sf --max-time 5 "http://127.0.0.1:${port}/health" > /dev/null 2>&1; then
        log "  ${name}: healthy"
    else
        add_issue "${name} (port ${port}): health check FAIL"
    fi
done

# Résumé health
GW_OK=$((3 - $(echo "$REPORT" | grep -c "health check FAIL")))
if [ "$GW_OK" -eq 3 ]; then
    add_report "  ✅ 3/3 healthy"
fi

# ── 6. Métriques système ─────────────────────────────────────────────
RAM_PCT=$(free | awk '/Mem:/{printf "%.0f", $3/$2*100}')
SWAP_PCT=$(free | awk '/Swap:/{if($2>0) printf "%.0f", $3/$2*100; else print "0"}')
DISK_PCT=$(df / | awk 'NR==2{gsub(/%/,""); print $5}')

add_report ""
add_report "💻 Système: RAM ${RAM_PCT}% | Swap ${SWAP_PCT}% | Disque ${DISK_PCT}%"

[ "${RAM_PCT:-0}" -ge 80 ] && add_issue "RAM élevée: ${RAM_PCT}%"
[ "${SWAP_PCT:-0}" -ge 50 ] && add_issue "Swap élevé: ${SWAP_PCT}%"
[ "${DISK_PCT:-0}" -ge 85 ] && add_issue "Disque élevé: ${DISK_PCT}%"

# ── Rapport final ────────────────────────────────────────────────────
add_report ""
if [ "$ISSUES" -eq 0 ]; then
    add_report "✅ Tout est OK — ${ISSUES} problème"
else
    add_report "⚠️ ${ISSUES} problème(s) détecté(s)"
fi

# Envoi Telegram
FINAL_MSG=$(echo -e "$REPORT")
log "Envoi rapport Telegram (${ISSUES} issues)"

curl -sf "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" \
    --data-urlencode "text=${FINAL_MSG}" \
    > /dev/null 2>&1

log "=== Terminé ==="
cat "$LOG"
