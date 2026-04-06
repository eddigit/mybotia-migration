#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# auto-repair.sh — Script unique de surveillance et auto-réparation
# ═══════════════════════════════════════════════════════════════════
# Remplace : gateway-watchdog.sh, whatsapp-creds-pruner.sh,
#            healthcheck-tools.sh, watchdog/run.sh, update-wa-contacts.py
# Cron     : */5 * * * *
# Principe : détecter → réparer → escaler → alerter
#            Zéro intervention humaine. Zéro faux positif.
#
# Sources  :
#   - Bug #56054 : corruption creds.json / boucle 499
#   - Bug #55030 : heartbeat 30min reconnect loop
#   - Bug #47142 : process zombies après restart
#   - Community  : openclaw-watchdog (LobeHub), Medium auto-recovery
#
# Créé le 04/04/2026 — Plan CTO Coach Digital Paris
# ═══════════════════════════════════════════════════════════════════

set -uo pipefail

# ── ENV SYSTEMD USER (requis pour cron) ─────────────────────────────
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"

# ── CONFIG ──────────────────────────────────────────────────────────

LOG="/tmp/auto-repair.log"
LOCKFILE="/tmp/auto-repair.lock"
STATE_FILE="/tmp/auto-repair-state.json"

# Escalade intelligente (pattern Medium "Auto-Recovery")
MAX_RESTARTS=3         # Nombre max de restarts par gateway
RESTART_WINDOW=1800    # Fenêtre en secondes (30 minutes)

# Telegram (charger depuis .jacques-env)
TELEGRAM_TOKEN=""
TELEGRAM_CHAT=""
if [ -f /home/gilles/.jacques-env ]; then
    TELEGRAM_TOKEN=$(grep -m1 'TELEGRAM_BOT_TOKEN' /home/gilles/.jacques-env 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'" || echo "")
    TELEGRAM_CHAT=$(grep -m1 'TELEGRAM_CHAT_ID' /home/gilles/.jacques-env 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'" || echo "")
fi

# Seuils credentials (agressif — basé sur expérience terrain du 03/04/2026)
CREDS_THRESHOLD=120    # Purge générale au-dessus de ce seuil
CREDS_KEEP=80          # Garder les N plus récents par type (sessions, sender-key, etc.)
PREKEY_MAX=80          # Seuil séparé pour pre-key-* (cause #1 des boucles 499)

# Seuils détection
MAX_499_COUNT=3        # Nombre de 499 dans tail-200 pour déclencher réparation
MAX_CORRUPTED=2        # Nombre de "restored corrupted" pour supprimer le .bak

# Gateways : nom|port|service_systemd|chemin_credentials
GATEWAYS=(
    "mybotia|18789|openclaw-gateway.service|/home/gilles/.openclaw/credentials/whatsapp/default"
    "vlmedical|18790|openclaw-gateway-vlmedical.service|/home/gilles/.openclaw-vlmedical/credentials/whatsapp/vlmedical-admin"
    "lucy|18795|openclaw-gateway-lucy.service|/home/gilles/.openclaw-lucy/credentials/whatsapp/lucy"
)

# Comptes WhatsApp supplémentaires (même gateway mybotia)
EXTRA_CREDS_DIRS=(
    "/home/gilles/.openclaw/credentials/whatsapp/nina"
    "/home/gilles/.openclaw/credentials/whatsapp/vlmedical-admin"
)

VOICE_SERVICE="voice-poc.service"
VOICE_PORT=3100

# État
ACTIONS_TAKEN=0
MAINTENANCE_TAKEN=0
REPORT=""

# ── FONCTIONS UTILITAIRES ──────────────────────────────────────────

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }
add_action() {
    ACTIONS_TAKEN=$((ACTIONS_TAKEN + 1))
    REPORT="${REPORT}🔧 $1\n"
    log "ACTION: $1"
}
# Maintenance de routine (purge credentials) — loggée mais pas comptée comme "action"
add_maintenance() {
    MAINTENANCE_TAKEN=$((MAINTENANCE_TAKEN + 1))
    log "MAINTENANCE: $1"
}

send_telegram() {
    [ -z "$TELEGRAM_TOKEN" ] || [ -z "$TELEGRAM_CHAT" ] && return
    local msg="🔴 AUTO-REPAIR — $(date '+%Y-%m-%d %H:%M:%S')\n\n${REPORT}\n✅ ${ACTIONS_TAKEN} action(s) effectuée(s)"
    curl -sf --max-time 10 "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT}" \
        --data-urlencode "text=$(echo -e "$msg")" \
        > /dev/null 2>&1 || true
}

send_telegram_msg() {
    [ -z "$TELEGRAM_TOKEN" ] || [ -z "$TELEGRAM_CHAT" ] && return
    curl -sf --max-time 10 "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT}" \
        --data-urlencode "text=$(echo -e "$1")" \
        > /dev/null 2>&1 || true
}

# ── GESTION ÉTAT (escalade intelligente) ───────────────────────────
# Fichier JSON : { "restarts": { "mybotia": [ts1, ts2], ... } }

init_state() {
    [ -f "$STATE_FILE" ] || echo '{"restarts":{}}' > "$STATE_FILE"
}

# Enregistre un restart et retourne le nombre dans la fenêtre
record_restart() {
    local gw_name="$1"
    local now
    now=$(date +%s)
    python3 -c "
import json, sys
now = $now
window = $RESTART_WINDOW
try:
    with open('$STATE_FILE') as f:
        state = json.load(f)
except:
    state = {'restarts': {}}
if 'restarts' not in state:
    state['restarts'] = {}
times = state['restarts'].get('$gw_name', [])
times = [t for t in times if now - t < window]
times.append(now)
state['restarts']['$gw_name'] = times
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f)
print(len(times))
" 2>/dev/null || echo "0"
}

# Vérifie si on peut encore restart (< MAX_RESTARTS dans la fenêtre)
can_restart_gateway() {
    local gw_name="$1"
    local now
    now=$(date +%s)
    local count
    count=$(python3 -c "
import json
now = $now
window = $RESTART_WINDOW
try:
    with open('$STATE_FILE') as f:
        state = json.load(f)
    times = state.get('restarts', {}).get('$gw_name', [])
    recent = [t for t in times if now - t < window]
    print(len(recent))
except:
    print(0)
" 2>/dev/null || echo "0")
    [ "$count" -lt "$MAX_RESTARTS" ]
}

# Restart une gateway avec escalade + vérification WhatsApp post-restart
safe_restart_gateway() {
    local name="$1"
    local port="$2"
    local unit="$3"
    local reason="$4"

    if ! can_restart_gateway "$name"; then
        log "ESCALADE: ${name} a atteint ${MAX_RESTARTS} restarts en 30min — stop auto-restart"
        send_telegram_msg "🚨 CRITIQUE — ${name}\n\n${MAX_RESTARTS} restarts en 30 min, auto-repair stoppé.\nIntervention manuelle requise, possible re-link QR nécessaire.\n\nRaison dernier restart: ${reason}"
        add_action "${name}: ESCALADE — ${MAX_RESTARTS} restarts/30min, alerte envoyée"
        return 1
    fi

    systemctl --user restart "$unit" 2>/dev/null || true
    local restart_count
    restart_count=$(record_restart "$name")
    log "RESTART: ${name} (${restart_count}/${MAX_RESTARTS} dans la fenêtre) — ${reason}"

    # Test fonctionnel post-restart : attendre 15s puis vérifier
    sleep 15

    # 1. Health HTTP
    local health
    health=$(curl -sf --max-time 5 "http://127.0.0.1:${port}/health" 2>/dev/null || echo "FAIL")
    if [ "$health" = "FAIL" ]; then
        add_action "${name}: ${reason} — redémarré (${restart_count}/${MAX_RESTARTS}) mais health KO après 15s"
        return 1
    fi

    # 2. WhatsApp listening check
    local logfile="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    if [ -f "$logfile" ]; then
        local wa_ok=0
        wa_ok=$(tail -20 "$logfile" 2>/dev/null | grep -c "Listening for personal WhatsApp") || true
        if [ "$wa_ok" -eq 0 ]; then
            add_action "${name}: ${reason} — redémarré mais WhatsApp non connecté (credentials ?)"
            send_telegram_msg "⚠️ ${name} — redémarré mais WhatsApp pas listening.\nProblème de credentials probable, NE PAS re-restart.\nVérifier manuellement."
            return 1
        fi
    fi

    add_action "${name}: ${reason} — redémarré OK (${restart_count}/${MAX_RESTARTS})"
    return 0
}

# Verrou pour empêcher les exécutions concurrentes
acquire_lock() {
    if [ -f "$LOCKFILE" ]; then
        local lock_age=$(( $(date +%s) - $(stat -c %Y "$LOCKFILE" 2>/dev/null || echo "0") ))
        if [ "$lock_age" -lt 300 ]; then
            log "Lock actif (${lock_age}s), skip"
            exit 0
        fi
        rm -f "$LOCKFILE"
    fi
    echo $$ > "$LOCKFILE"
    trap "rm -f $LOCKFILE" EXIT
}

# ── 1. PROCESS ZOMBIES ─────────────────────────────────────────────
# Problème : après un restart, des vieux process openclaw-gateway
# restent et écoutent sur les mêmes ports → messages routés nulle part
# Ref : Bug #47142 — 8h de silence WhatsApp à cause de ça

repair_zombies() {
    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"

        # PID que systemd connaît
        local sys_pid
        sys_pid=$(systemctl --user show "$unit" -p MainPID --value 2>/dev/null || echo "0")
        [ "$sys_pid" = "0" ] && continue

        # PID qui écoute réellement sur le port
        local port_pids
        port_pids=$(ss -tlnp 2>/dev/null | grep ":${port} " | grep -oP 'pid=\K[0-9]+' | sort -u)

        for ppid in $port_pids; do
            # Vérifier si ce PID est un descendant du MainPID systemd
            # (openclaw fork openclaw-gateway qui écoute sur le port — c'est normal)
            if [ "$ppid" != "$sys_pid" ]; then
                local is_child=false
                if [ -f "/proc/${ppid}/status" ]; then
                    local actual_ppid
                    actual_ppid=$(awk '/^PPid:/ {print $2}' "/proc/${ppid}/status" 2>/dev/null || echo "0")
                    [ "$actual_ppid" = "$sys_pid" ] && is_child=true
                fi
                if [ "$is_child" = false ]; then
                    kill "$ppid" 2>/dev/null || true
                    add_action "${name}: orphan PID ${ppid} tué (pas enfant de systemd PID=${sys_pid})"
                fi
            fi
        done
    done
}

# ── 2. HEALTH CHECK GATEWAYS ──────────────────────────────────────
# Escalade : systemd check → HTTP health → double check → restart
# Principe : ne restart que si vraiment mort (double vérification)

repair_gateways() {
    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"

        # Étape 1 : systemd actif ?
        local state
        state=$(systemctl --user is-active "$unit" 2>/dev/null || echo "dead")

        if [ "$state" != "active" ]; then
            # Service arrêté → start (pas restart, pas d'escalade)
            systemctl --user start "$unit" 2>/dev/null || true
            sleep 5
            record_restart "$name" > /dev/null
            add_action "${name}: service ${state} → démarré"
            continue
        fi

        # Étape 2 : HTTP health check
        local health
        health=$(curl -sf --max-time 5 "http://127.0.0.1:${port}/health" 2>/dev/null || echo "FAIL")

        if [ "$health" = "FAIL" ]; then
            # Double check — attendre 10s et retester (éviter faux positifs)
            sleep 10
            health=$(curl -sf --max-time 5 "http://127.0.0.1:${port}/health" 2>/dev/null || echo "FAIL")
            if [ "$health" = "FAIL" ]; then
                safe_restart_gateway "$name" "$port" "$unit" "health KO confirmé"
            fi
        fi
    done

    # Voice-poc
    local vs
    vs=$(systemctl --user is-active "$VOICE_SERVICE" 2>/dev/null || echo "dead")
    if [ "$vs" != "active" ]; then
        systemctl --user start "$VOICE_SERVICE" 2>/dev/null || true
        add_action "voice-poc: ${vs} → démarré"
    fi
}

# ── 3. CREDENTIALS PRUNER ─────────────────────────────────────────
# Purge les pre-keys AVANT qu'elles déclenchent une boucle 499
# Plus agressif que le PR #26625 (seuil 500) — on purge à 150

purge_creds_dir() {
    local dir="$1"
    local label="$2"

    [ ! -d "$dir" ] && return

    local total purged=0
    total=$(find "$dir" -maxdepth 1 -type f 2>/dev/null | wc -l)

    # Pre-keys : seuil séparé plus agressif (cause #1 des boucles 499)
    local prekey_count
    prekey_count=$(find "$dir" -maxdepth 1 -name "pre-key-*" -type f 2>/dev/null | wc -l)
    if [ "$prekey_count" -gt "$PREKEY_MAX" ]; then
        local to_rm=$((prekey_count - PREKEY_MAX))
        ls -t "$dir"/pre-key-* 2>/dev/null | tail -n +"$((PREKEY_MAX + 1))" | xargs rm -f 2>/dev/null
        purged=$((purged + to_rm))
    fi

    # Autres types : seuil global CREDS_THRESHOLD
    if [ "$total" -ge "$CREDS_THRESHOLD" ]; then
        for pattern in "session-*" "sender-key-*" "app-state-sync-key-*" "app-state-sync-version-*"; do
            local pcount
            pcount=$(find "$dir" -maxdepth 1 -name "$pattern" -type f 2>/dev/null | wc -l)
            if [ "$pcount" -gt "$CREDS_KEEP" ]; then
                local to_rm=$((pcount - CREDS_KEEP))
                ls -t "$dir"/$pattern 2>/dev/null | tail -n +"$((CREDS_KEEP + 1))" | xargs rm -f 2>/dev/null
                purged=$((purged + to_rm))
            fi
        done
    fi

    [ "$purged" -gt 0 ] && add_maintenance "${label}: ${purged} credentials purgés (pre-keys: ${prekey_count}→${PREKEY_MAX}, total: ${total})"
}

repair_credentials() {
    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"
        purge_creds_dir "$creds" "$name"
    done

    for extra in "${EXTRA_CREDS_DIRS[@]}"; do
        [ -d "$extra" ] && purge_creds_dir "$extra" "$(basename "$extra")"
    done
}

# ── 4. BACKUP CORROMPU (creds.json.bak) ────────────────────────────
# Bug #56054 : Baileys corrompt creds.json régulièrement et restaure depuis .bak
# C'est cosmétique SAUF si ça déclenche une boucle 499.
# On ne supprime le .bak que dans repair_499_loop (section 5).
# Ici on logue seulement comme maintenance pour visibilité.

repair_corrupted_backup() {
    # No-op : la suppression du .bak est déléguée à repair_499_loop
    # Les "restored corrupted" sans 499 sont cosmétiques (bug #56054, pas de fix upstream)
    :
}

# ── 5. BOUCLE 499 ─────────────────────────────────────────────────
# Détecte une boucle 499 active et applique le fix complet :
# purge credentials + supprime .bak + restart gateway

repair_499_loop() {
    local logfile="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    [ ! -f "$logfile" ] && return

    local recent_lines
    recent_lines=$(tail -200 "$logfile" 2>/dev/null)

    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"

        # Compter les 499 spécifiques à cette gateway (par port ou nom)
        local count_499=0
        count_499=$(echo "$recent_lines" | grep -cE "status 499.*:${port}|status 499.*${name}|:${port}.*status 499" 2>/dev/null) || true

        # Fallback : si le log ne contient pas le port, chercher juste "status 499"
        # mais seulement si c'est la gateway principale (mybotia)
        if [ "$count_499" -eq 0 ] && [ "$name" = "mybotia" ]; then
            count_499=$(echo "$recent_lines" | grep -cE "status 499" 2>/dev/null) || true
        fi

        if [ "$count_499" -ge "$MAX_499_COUNT" ]; then
            # 1. Purge credentials
            purge_creds_dir "$creds" "${name}-499fix"

            # 2. Supprimer backup corrompu
            [ -f "${creds}/creds.json.bak" ] && mv "${creds}/creds.json.bak" "${creds}/creds.json.bak.purged-$(date +%s)" 2>/dev/null

            # 3. Restart avec escalade intelligente + vérification WhatsApp
            safe_restart_gateway "$name" "$port" "$unit" "boucle 499 (${count_499}x)"
        fi
    done
}

# ── 6. KEEPALIVE WHATSAPP ──────────────────────────────────────────
# Bug #55030 : le heartbeat WhatsApp de 30min a un bug qui cause
# des reconnexions en cascade quand la gateway est idle.
# Fix : toucher le health endpoint pour garder le WebSocket actif
# et empêcher le timer idle d'atteindre 30 minutes.

keepalive_whatsapp() {
    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"
        curl -sf --max-time 3 "http://127.0.0.1:${port}/health" > /dev/null 2>&1 || true
    done
}

# ── 7. UPDATE CONTACTS WHATSAPP ────────────────────────────────────

update_contacts() {
    [ -f /home/gilles/update-wa-contacts.py ] || return
    if ! python3 /home/gilles/update-wa-contacts.py >> /tmp/wa-contacts-update.log 2>&1; then
        add_action "update-wa-contacts.py a échoué (code $?)"
    fi
}

# ── 8. CHECK SYSTÈME (RAM / DISQUE) ────────────────────────────────
# Alerte si RAM libre < 500 Mo ou disque utilisé > 85%

check_system() {
    # RAM libre (MemAvailable en Mo)
    local mem_avail
    mem_avail=$(awk '/MemAvailable/ {printf "%d", $2/1024}' /proc/meminfo 2>/dev/null || echo "9999")
    if [ "$mem_avail" -lt 500 ]; then
        add_action "RAM critique : ${mem_avail} Mo disponibles (seuil 500 Mo)"
    fi

    # Disque / utilisé
    local disk_pct
    disk_pct=$(df / 2>/dev/null | awk 'NR==2 {gsub(/%/,""); print $5}' || echo "0")
    if [ "$disk_pct" -gt 85 ]; then
        add_action "Disque critique : ${disk_pct}% utilisé (seuil 85%)"
    fi
}

# ── 9. NETTOYAGE VIEUX .bak.purged ─────────────────────────────────
# Les fichiers creds.json.bak.purged-* s'accumulent à chaque suppression
# Rotation : supprimer ceux de plus de 7 jours

cleanup_old_purged() {
    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"
        [ ! -d "$creds" ] && continue
        local cleaned=0
        cleaned=$(find "$creds" -maxdepth 1 -name "creds.json.bak.purged-*" -o -name "creds.json.bak.old-*" 2>/dev/null \
            | while read -r f; do
                local age=$(( $(date +%s) - $(stat -c %Y "$f" 2>/dev/null || echo "0") ))
                if [ "$age" -gt 604800 ]; then
                    rm -f "$f" && echo "1"
                fi
            done | wc -l)
        [ "$cleaned" -gt 0 ] && add_action "${name}: ${cleaned} vieux .bak.purged supprimés (>7j)"
    done
}

# ── 10. CHECK ANTHROPIC OVERLOADED ─────────────────────────────────
# Détecte si Anthropic est surchargé (>5 "overloaded" dans les 200
# dernières lignes) → alerte pour que Gilles sache que le fallback
# Groq est actif et les réponses en mode dégradé

check_anthropic_overload() {
    local logfile="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    [ ! -f "$logfile" ] && return

    local overload_count=0
    overload_count=$(tail -200 "$logfile" 2>/dev/null | grep -ci "overloaded") || true

    if [ "$overload_count" -gt 5 ]; then
        add_action "Anthropic surchargé (${overload_count}x dans les 200 dernières lignes)"
        send_telegram_msg "⚠️ Anthropic surchargé — ${overload_count} erreurs 'overloaded' détectées.\nFallback Groq probablement actif, réponses en mode dégradé."
    fi
}

# ── 11. RAPPORT QUOTIDIEN (07:00–07:05) ───────────────────────────
# Un seul message Telegram par jour avec le résumé des dernières 24h

daily_report() {
    local hour minute
    hour=$(date +%H)
    minute=$(date +%M)

    # Ne s'exécute qu'entre 07:00 et 07:04
    [ "$hour" != "07" ] && return
    [ "$minute" -ge 5 ] && return

    # Anti-doublon : vérifier si le rapport du jour a déjà été envoyé
    local marker="/tmp/auto-repair-daily-$(date +%Y-%m-%d)"
    [ -f "$marker" ] && return
    touch "$marker"

    # Parser le log des dernières 24h
    local yesterday
    yesterday=$(date -d '1 day ago' '+%Y-%m-%d' 2>/dev/null || date -d '-1 day' '+%Y-%m-%d' 2>/dev/null || echo "")
    local today
    today=$(date '+%Y-%m-%d')

    local total_actions=0
    total_actions=$(grep -cE "ACTION:" "$LOG" 2>/dev/null | head -1) || true
    # Compter seulement les 24 dernières heures
    local actions_24h=0
    actions_24h=$(grep -E "^\[${today}|^\[${yesterday}" "$LOG" 2>/dev/null | grep -c "ACTION:") || true

    # Restarts par gateway
    local restart_summary=""
    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"
        local gw_restarts=0
        gw_restarts=$(grep -E "^\[${today}|^\[${yesterday}" "$LOG" 2>/dev/null | grep -ci "ACTION:.*${name}.*redémarré\|ACTION:.*${name}.*démarré\|RESTART:.*${name}") || true
        restart_summary="${restart_summary}  ${name}: ${gw_restarts}\n"
    done

    # Credentials purgés
    local creds_purged=0
    creds_purged=$(grep -E "^\[${today}|^\[${yesterday}" "$LOG" 2>/dev/null | grep -c "credentials purgés") || true

    # État actuel des gateways
    local status_summary=""
    local all_ok=true
    for gw in "${GATEWAYS[@]}"; do
        IFS='|' read -r name port unit creds <<< "$gw"
        local st
        st=$(systemctl --user is-active "$unit" 2>/dev/null || echo "dead")
        local ht
        ht=$(curl -sf --max-time 3 "http://127.0.0.1:${port}/health" 2>/dev/null && echo "OK" || echo "KO")
        local icon="✅"
        if [ "$st" != "active" ] || [ "$ht" = "KO" ]; then
            icon="❌"
            all_ok=false
        fi
        status_summary="${status_summary}  ${icon} ${name} (${st}, health ${ht})\n"
    done

    local header="✅ Tout OK"
    [ "$all_ok" = false ] && header="⚠️ Problèmes détectés"

    local report="📊 RAPPORT QUOTIDIEN — ${today}\n\n"
    report="${report}${header}\n\n"
    report="${report}📈 Dernières 24h :\n"
    report="${report}  Actions totales : ${actions_24h}\n"
    report="${report}  Credentials purgés : ${creds_purged}\n\n"
    report="${report}🔄 Restarts (24h) :\n${restart_summary}\n"
    report="${report}🖥️ État actuel :\n${status_summary}"

    send_telegram_msg "$report"
    log "DAILY REPORT envoyé"
}

# ── 12. ROTATION DU LOG ───────────────────────────────────────────

rotate_log() {
    [ -f "$LOG" ] || return
    local lines
    lines=$(wc -l < "$LOG" 2>/dev/null || echo "0")
    if [ "$lines" -gt 2000 ]; then
        tail -1000 "$LOG" > "${LOG}.tmp" && mv "${LOG}.tmp" "$LOG"
    fi
}

# ── MAIN ───────────────────────────────────────────────────────────

acquire_lock
init_state

log "=== Auto-repair cycle ==="

# Exécuter toutes les réparations (ordre important)
repair_zombies           # D'abord virer les fantômes
repair_gateways          # Puis vérifier que tout tourne (+ escalade + check WA)
repair_credentials       # Purger avant que ça explose
repair_corrupted_backup  # Supprimer les backups pourris
repair_499_loop          # Traiter les boucles actives (+ escalade + check WA)
keepalive_whatsapp       # Garder WhatsApp vivant
update_contacts          # Mise à jour contacts
check_system             # RAM et disque
cleanup_old_purged       # Rotation .bak.purged > 7j
check_anthropic_overload # Détecter surcharge Anthropic

# Rapport quotidien (07:00–07:05 uniquement)
daily_report

# Rapport des actions du cycle
if [ "$ACTIONS_TAKEN" -gt 0 ]; then
    log "=== ${ACTIONS_TAKEN} action(s)$([ "$MAINTENANCE_TAKEN" -gt 0 ] && echo ", ${MAINTENANCE_TAKEN} maintenance") ==="
    send_telegram
elif [ "$MAINTENANCE_TAKEN" -gt 0 ]; then
    log "=== RAS (${MAINTENANCE_TAKEN} maintenance) ==="
else
    log "=== RAS ==="
fi

rotate_log
