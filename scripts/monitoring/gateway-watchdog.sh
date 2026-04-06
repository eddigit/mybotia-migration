#!/bin/bash
# gateway-watchdog.sh — Watchdog SRE MaBoiteIA
# Cron: */2 * * * * /home/gilles/scripts/monitoring/gateway-watchdog.sh >> /tmp/gateway-watchdog.log 2>&1
# Créé suite à incident reboot 16/03/2026
# Refactorisé 29/03/2026 — Programme SRE (SLO tracker + format alertes + consolidation checks)

set -a; source "$HOME/.jacques-env" 2>/dev/null; set +a

LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')] [sre-watchdog]"
TRACKER="/home/gilles/watchdog/state/slo-tracker.json"
STATE_DIR="/home/gilles/scripts/monitoring/state"
mkdir -p "$STATE_DIR"

# === ALERTES SRE ===

send_alert() {
    local level="$1"    # CRIT, WARN, INFO
    local service="$2"
    local agent="$3"
    local problem="$4"
    local since="$5"
    local impact="$6"
    local action="$7"
    local budget_info="$8"

    # INFO = log only
    if [ "$level" = "INFO" ]; then
        echo "${LOG_PREFIX} INFO: ${service} — ${problem}"
        return 0
    fi

    local icon="🟡 WARNING"
    [ "$level" = "CRIT" ] && icon="🔴 CRITIQUE"

    local msg="${icon}

Service : ${service}
Agent : ${agent}
Problème : ${problem}
Depuis : ${since}
Impact : ${impact}
Action : ${action}"

    [ -n "$budget_info" ] && msg="${msg}
Error Budget : ${budget_info}"

    # Debounce : WARN = 1h (3600s), CRIT = 10 min (600s)
    local alert_key
    alert_key=$(echo "${service}-${problem}" | md5sum | cut -c1-12)
    local state_file="${STATE_DIR}/sre-alert-${alert_key}"
    local now
    now=$(date +%s)
    local debounce_secs=600
    [ "$level" = "WARN" ] && debounce_secs=3600

    if [ -f "$state_file" ]; then
        local last_alert
        last_alert=$(cat "$state_file" 2>/dev/null)
        local elapsed=$(( now - last_alert ))
        if [ "$elapsed" -lt "$debounce_secs" ]; then
            echo "${LOG_PREFIX} DEBOUNCE: ${service} — alerte envoyée il y a ${elapsed}s (debounce=${debounce_secs}s), ignorée"
            return 0
        fi
    fi
    echo "$now" > "$state_file"

    # WARN → canal partagé uniquement (PAS Telegram à Gilles)
    # CRIT → Telegram Gilles + canal partagé
    if [ "$level" = "CRIT" ]; then
        curl -sf "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="${TELEGRAM_CHAT_ID}" \
            --data-urlencode "text=${msg}" \
            > /dev/null 2>&1
    fi

    # Écrire dans le canal partagé (WARN + CRIT)
    local shared_file="/home/gilles/.openclaw/shared/jacques-to-lea.md"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local priority_icon="🟡"
    [ "$level" = "CRIT" ] && priority_icon="🔴"
    echo "" >> "$shared_file"
    echo "## [${timestamp}] ${priority_icon} ${level} — ${service}: ${problem}" >> "$shared_file"
    echo "${msg}" >> "$shared_file"
    echo "Status: PENDING" >> "$shared_file"

    echo "${LOG_PREFIX} ALERT ${level}: ${service} — ${problem}"
}

clear_sre_alert() {
    local service="$1"
    local problem="$2"
    local alert_key
    alert_key=$(echo "${service}-${problem}" | md5sum | cut -c1-12)
    rm -f "${STATE_DIR}/sre-alert-${alert_key}" 2>/dev/null
}

# === SLO TRACKER ===

update_tracker() {
    local service_key="$1"
    local is_ok="$2"  # 1=ok, 0=fail

    [ ! -f "$TRACKER" ] && return

    python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=1))
now = datetime.now(tz)
today = now.strftime('%Y-%m-%d')

with open('$TRACKER') as f:
    data = json.load(f)

day = data.get('current_day', {})

# Reset si nouveau jour
if day.get('date') != today:
    # Archiver le jour précédent dans week_summary avant reset
    week_num = now.strftime('%Y-W%W')
    ws = data.setdefault('week_summary', {})
    ws['week'] = week_num
    ws_services = ws.setdefault('services', {})
    for svc_key, svc_data in day.get('services', {}).items():
        ws_svc = ws_services.setdefault(svc_key, {
            'budget_used_pct': 0, 'total_downtime_sec': 0, 'incidents': 0
        })
        budget_total = svc_data.get('error_budget_total_sec', 0)
        budget_remain = svc_data.get('error_budget_remaining_sec', budget_total)
        consumed = budget_total - budget_remain
        ws_svc['total_downtime_sec'] = ws_svc.get('total_downtime_sec', 0) + max(0, consumed)
        if budget_total > 0:
            ws_svc['budget_used_pct'] = round(ws_svc['total_downtime_sec'] / (budget_total * 7) * 100, 1)

    # Reset day
    for svc_key, svc_data in day.get('services', {}).items():
        svc_data['checks_total'] = 0
        svc_data['checks_ok'] = 0
        svc_data['uptime_pct'] = 100.0
        svc_data['error_budget_remaining_sec'] = svc_data.get('error_budget_total_sec', 0)
        svc_data['error_budget_used_pct'] = 0
        svc_data['status'] = 'OK'
        svc_data['last_failure'] = None
        svc_data['consecutive_failures'] = 0
    day['date'] = today
    day['started_at'] = now.isoformat()

svc = day.get('services', {}).get('$service_key')
if svc is None:
    sys.exit(0)

svc['checks_total'] = svc.get('checks_total', 0) + 1
svc['last_check'] = now.isoformat()

if $is_ok:
    svc['checks_ok'] = svc.get('checks_ok', 0) + 1
    svc['consecutive_failures'] = 0
else:
    svc['consecutive_failures'] = svc.get('consecutive_failures', 0) + 1
    svc['last_failure'] = now.isoformat()
    # Consume error budget (120s per failed check at 2-min interval)
    svc['error_budget_remaining_sec'] = svc.get('error_budget_remaining_sec', 0) - 120

total = svc['checks_total']
ok = svc['checks_ok']
svc['uptime_pct'] = round(ok / total * 100, 2) if total > 0 else 100.0

budget_total = svc.get('error_budget_total_sec', 0)
budget_remain = svc.get('error_budget_remaining_sec', 0)
if budget_total > 0:
    svc['error_budget_used_pct'] = round((budget_total - budget_remain) / budget_total * 100, 1)
else:
    svc['error_budget_used_pct'] = 0

# Status
if budget_remain <= 0:
    svc['status'] = 'BUDGET_EXCEEDED'
elif svc['error_budget_used_pct'] >= 75:
    svc['status'] = 'BUDGET_LOW'
elif svc['error_budget_used_pct'] >= 50:
    svc['status'] = 'BUDGET_WARN'
else:
    svc['status'] = 'OK'

data['current_day'] = day
data['last_updated'] = now.isoformat()

with open('$TRACKER', 'w') as f:
    json.dump(data, f, indent=2)

# Output for caller: status,budget_remaining,budget_used_pct,consecutive_failures
print(f'{svc[\"status\"]},{budget_remain},{svc[\"error_budget_used_pct\"]},{svc[\"consecutive_failures\"]}')
" 2>/dev/null
}

update_system_tracker() {
    local resource="$1"  # ram, swap, disk
    local value="$2"     # percentage
    local status="$3"    # OK, WARN, CRIT

    [ ! -f "$TRACKER" ] && return

    python3 -c "
import json
from datetime import datetime, timezone, timedelta
tz = timezone(timedelta(hours=1))
now = datetime.now(tz)
with open('$TRACKER') as f:
    data = json.load(f)
sys_data = data.get('current_day', {}).get('system', {}).get('$resource', {})
sys_data['last_pct'] = $value
sys_data['status'] = '$status'
sys_data['last_check'] = now.isoformat()
data['last_updated'] = now.isoformat()
with open('$TRACKER', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null
}

get_budget_info() {
    local service_key="$1"
    [ ! -f "$TRACKER" ] && echo "" && return

    python3 -c "
import json
with open('$TRACKER') as f:
    data = json.load(f)
svc = data.get('current_day', {}).get('services', {}).get('$service_key', {})
remain = svc.get('error_budget_remaining_sec', 0)
used_pct = svc.get('error_budget_used_pct', 0)
total = svc.get('error_budget_total_sec', 0)
if remain <= 0:
    print(f'{total}s total, ÉPUISÉ (dépassé de {abs(remain)}s)')
elif used_pct >= 75:
    print(f'{remain}s restant sur {total}s ({used_pct}% consommé) — BAS')
else:
    print(f'{remain}s restant sur {total}s ({used_pct}% consommé)')
" 2>/dev/null
}

# === CHECKS GATEWAY ===

check_and_restart() {
    local name="$1"
    local port="$2"
    local compose_dir="$3"
    local tracker_key="$4"

    local is_ok=1
    if ! curl -sf --max-time 5 "http://127.0.0.1:${port}/health" > /dev/null 2>&1; then
        is_ok=0
    fi

    # Update SLO tracker
    local tracker_result
    tracker_result=$(update_tracker "$tracker_key" "$is_ok")
    local slo_status budget_remain budget_used_pct consecutive_failures
    IFS=',' read -r slo_status budget_remain budget_used_pct consecutive_failures <<< "$tracker_result"

    if [ "$is_ok" -eq 1 ]; then
        # Service OK — clear alerts
        clear_sre_alert "$name" "Health check failed"

        # Alert si budget exceeded (même si le service est up maintenant)
        # Debounce : 1 seule alerte par jour (86400s) — WARN seulement (pas Telegram)
        if [ "$slo_status" = "BUDGET_EXCEEDED" ]; then
            local budget_exceeded_state="${STATE_DIR}/budget-exceeded-$(echo "$name" | md5sum | cut -c1-8)"
            local now_ts
            now_ts=$(date +%s)
            local should_alert_budget=1
            if [ -f "$budget_exceeded_state" ]; then
                local last_budget_alert
                last_budget_alert=$(cat "$budget_exceeded_state" 2>/dev/null)
                local budget_elapsed=$(( now_ts - last_budget_alert ))
                if [ "$budget_elapsed" -lt 86400 ]; then
                    should_alert_budget=0
                fi
            fi
            if [ "$should_alert_budget" -eq 1 ]; then
                echo "$now_ts" > "$budget_exceeded_state"
                local budget_info
                budget_info=$(get_budget_info "$tracker_key")
                send_alert "WARN" "$name" "-" \
                    "Error Budget épuisé" \
                    "aujourd'hui" \
                    "SLO violé — trop de downtime cumulé" \
                    "Gel des changements recommandé — info seulement" \
                    "$budget_info"
            fi
        fi
        return 0
    fi

    echo "${LOG_PREFIX} ALERTE: ${name} ne répond pas sur le port ${port}"

    # Anti-faux-positif : ne restart que si 2+ échecs consécutifs (= 4 min de down)
    if [ "${consecutive_failures:-0}" -lt 2 ]; then
        echo "${LOG_PREFIX} ${name}: premier échec, attente confirmation au prochain check"
        return 1
    fi

    # Restart via systemd (tous les services sont maintenant des units systemd user)
    local systemd_unit="$compose_dir"  # compose_dir réutilisé comme nom de l'unit systemd
    echo "${LOG_PREFIX} ${name}: restart via systemctl --user restart ${systemd_unit}"
    systemctl --user restart "$systemd_unit" 2>&1
    echo "${LOG_PREFIX} ${name} restart lancé"

    local budget_info
    budget_info=$(get_budget_info "$tracker_key")

    # Vérifier si le restart a fonctionné (attendre 20s pour laisser le service démarrer)
    sleep 20
    if curl -sf --max-time 5 "http://127.0.0.1:${port}/health" > /dev/null 2>&1; then
        send_alert "WARN" "$name" "-" \
            "Health check failed — AUTO-CORRIGÉ" \
            "$(date '+%H:%M') (${consecutive_failures} checks ratés)" \
            "Service était down, restart auto OK" \
            "restart effectué (${name})" \
            "$budget_info"
    else
        send_alert "CRIT" "$name" "-" \
            "Health check failed — auto-fix ÉCHOUÉ" \
            "$(date '+%H:%M') (${consecutive_failures} checks ratés)" \
            "Service DOWN, restart n'a pas fonctionné" \
            "Intervention manuelle requise — journalctl --user -u openclaw-gateway / docker logs ${name}" \
            "$budget_info"
    fi
}

# === CHECK WHATSAPP ===

check_whatsapp_creds() {
    local name="$1"
    local creds_path="$2"
    local compose_dir="$3"
    local tracker_key="$4"

    [ ! -f "$creds_path" ] && return 0

    local registered
    registered=$(python3 -c "import json; print(json.load(open('$creds_path')).get('registered', True))" 2>/dev/null)

    local is_ok=1
    if [ "$registered" = "False" ]; then
        is_ok=0
    fi

    # Check heartbeat loop via logs (tous les gateways écrivent dans /tmp/)
    local last30
    local log_file="/tmp/${name}.log"
    last30=$(tail -30 "$log_file" 2>/dev/null)
    local heartbeat_count
    heartbeat_count=$(echo "$last30" | grep -c "No messages received in")
    heartbeat_count=${heartbeat_count:-0}
    local listening_count
    listening_count=$(echo "$last30" | grep -c "Listening for personal WhatsApp")
    listening_count=${listening_count:-0}
    if [ "$heartbeat_count" -gt 15 ] && [ "$listening_count" -eq 0 ]; then
        is_ok=0
    fi

    # Check logout events (exclude "Inbound/Sending/Sent message" lines to avoid false positives on "401 chars")
    local logout_count
    logout_count=$(echo "$last30" | grep -vE "\[whatsapp\] (Inbound|Sending|Sent) message" | grep -ciE "LOGGED_OUT|logged out|session error|status[: ]*401")
    logout_count=${logout_count:-0}
    if [ "$logout_count" -gt 0 ]; then
        is_ok=0
    fi

    # Update SLO tracker
    update_tracker "$tracker_key" "$is_ok" > /dev/null

    if [ "$registered" = "False" ]; then
        echo "${LOG_PREFIX} CRIT: ${name} WhatsApp registered=false. Auto-fix..."

        # Patch registered=true
        python3 -c "
import json
with open('$creds_path') as f: c=json.load(f)
c['registered']=True
with open('$creds_path','w') as f: json.dump(c,f,indent=2)
"
        # Restart via systemd (compose_dir = systemd unit name)
        local systemd_unit="$compose_dir"
        systemctl --user restart "$systemd_unit" 2>&1
        echo "${LOG_PREFIX} FIX: ${name} WhatsApp patched registered=true + systemctl restart ${systemd_unit}"

        local budget_info
        budget_info=$(get_budget_info "$tracker_key")
        send_alert "WARN" "$name" "WhatsApp" \
            "registered=false — AUTO-CORRIGÉ" \
            "$(date '+%H:%M')" \
            "Messages WhatsApp interrompus pendant le fix" \
            "Patch registered=true + systemctl restart ${systemd_unit}" \
            "$budget_info"
        return
    fi

    if [ "$heartbeat_count" -gt 10 ]; then
        local budget_info
        budget_info=$(get_budget_info "$tracker_key")
        send_alert "WARN" "$name" "WhatsApp" \
            "Boucle heartbeat (${heartbeat_count}x)" \
            "$(date '+%H:%M')" \
            "Connexion WhatsApp probablement morte" \
            "Vérifier manuellement — restart gateway si persistant" \
            "$budget_info"
    fi

    if [ "$logout_count" -gt 0 ]; then
        local budget_info
        budget_info=$(get_budget_info "$tracker_key")
        send_alert "WARN" "$name" "WhatsApp" \
            "Événements logout détectés (${logout_count}x)" \
            "$(date '+%H:%M')" \
            "Session WhatsApp instable" \
            "Surveiller — re-scan QR si persistant" \
            "$budget_info"
    fi

    if [ "$is_ok" -eq 1 ]; then
        clear_sre_alert "$name" "registered=false — AUTO-CORRIGÉ"
        clear_sre_alert "$name" "Boucle heartbeat"
        clear_sre_alert "$name" "Événements logout détectés"
    fi
}

# === CHECK SYSTÈME (RAM/Swap/Disque) ===

check_system() {
    local ram_total ram_used ram_pct
    ram_total=$(free -m | awk '/Mem:/{print $2}')
    ram_used=$(free -m | awk '/Mem:/{print $3}')
    ram_pct=$(( (ram_used * 100) / ram_total ))

    local swap_total swap_used swap_pct
    swap_total=$(free -m | awk '/Swap:/{print $2}')
    swap_used=$(free -m | awk '/Swap:/{print $3}')
    if [ "${swap_total:-0}" -gt 0 ]; then
        swap_pct=$(( (swap_used * 100) / swap_total ))
    else
        swap_pct=0
    fi

    local disk_pct
    disk_pct=$(df / | awk 'NR==2{gsub(/%/,""); print $5}')

    # RAM
    local ram_status="OK"
    if [ "$ram_pct" -ge 85 ]; then
        ram_status="CRIT"
        send_alert "CRIT" "VPS Système" "-" \
            "RAM critique: ${ram_pct}%" \
            "$(date '+%H:%M')" \
            "Risque OOM — services dégradés" \
            "Vérifier top processus, purge caches si nécessaire" \
            ""
    elif [ "$ram_pct" -ge 75 ]; then
        ram_status="WARN"
        send_alert "WARN" "VPS Système" "-" \
            "RAM élevée: ${ram_pct}%" \
            "$(date '+%H:%M')" \
            "Approche du seuil critique (85%)" \
            "Surveiller tendance" \
            ""
    fi
    update_system_tracker "ram" "$ram_pct" "$ram_status"

    # Swap
    local swap_status="OK"
    if [ "$swap_pct" -ge 60 ]; then
        swap_status="CRIT"
        send_alert "CRIT" "VPS Système" "-" \
            "Swap critique: ${swap_pct}%" \
            "$(date '+%H:%M')" \
            "Pression mémoire forte" \
            "Identifier process en swap, restart si fuite mémoire" \
            ""
    elif [ "$swap_pct" -ge 40 ]; then
        swap_status="WARN"
        send_alert "WARN" "VPS Système" "-" \
            "Swap élevé: ${swap_pct}%" \
            "$(date '+%H:%M')" \
            "Approche du seuil critique (60%)" \
            "Surveiller tendance" \
            ""
    fi
    update_system_tracker "swap" "$swap_pct" "$swap_status"

    # Disque
    local disk_status="OK"
    if [ "$disk_pct" -ge 90 ]; then
        disk_status="CRIT"
        send_alert "CRIT" "VPS Système" "-" \
            "Disque critique: ${disk_pct}%" \
            "$(date '+%H:%M')" \
            "Risque de saturation" \
            "Purge logs + docker prune requis" \
            ""
    elif [ "$disk_pct" -ge 80 ]; then
        disk_status="WARN"
        send_alert "WARN" "VPS Système" "-" \
            "Disque élevé: ${disk_pct}%" \
            "$(date '+%H:%M')" \
            "Approche du seuil critique (90%)" \
            "Vérifier du -sh /home/gilles/* /tmp/*" \
            ""
    fi
    update_system_tracker "disk" "$disk_pct" "$disk_status"

    echo "${LOG_PREFIX} SYSTEM: RAM=${ram_pct}% Swap=${swap_pct}% Disk=${disk_pct}%"
}

# === CHECK SYSTEMD SERVICES (vérifier que les units sont actives) ===

check_systemd_services() {
    for unit in openclaw-gateway.service openclaw-gateway-vlmedical.service openclaw-gateway-lucy.service voice-poc.service; do
        local state
        state=$(systemctl --user is-active "$unit" 2>/dev/null)
        if [ "$state" != "active" ]; then
            send_alert "WARN" "systemd" "$unit" \
                "Unit ${unit} état: ${state}" \
                "$(date '+%H:%M')" \
                "Service pas en état active — possible crash sans restart" \
                "systemctl --user status ${unit} pour diagnostic" \
                ""
        fi
    done
}

# === CHECK BOUCLE 499 WHATSAPP (toutes les gateways Docker) ===

check_whatsapp_499_loop() {
    # 1. Mybotia-gateway (host, pas Docker) — scanner le fichier log
    local count_499_host
    count_499_host=$(tail -100 /tmp/mybotia-gateway.log 2>/dev/null | grep -c "status 499" 2>/dev/null)
    count_499_host=${count_499_host:-0}

    if [ "$count_499_host" -ge 3 ]; then
        send_alert "CRIT" "mybotia-gateway" "WhatsApp" \
            "Boucle 499 détectée (${count_499_host}x récemment)" \
            "$(date '+%H:%M')" \
            "WhatsApp en reconnexion permanente — messages intermittents" \
            "Restart gateway recommandé" \
            ""
    fi

    # 2. Autres gateways (systemd, logs dans /tmp/)
    for gw_entry in "vlmedical-gateway:/tmp/vlmedical-gateway.log:openclaw-gateway-vlmedical.service" \
                    "lucy-gateway:/tmp/lucy-gateway.log:openclaw-gateway-lucy.service"; do
        local gw_name gw_log gw_unit
        IFS=':' read -r gw_name gw_log gw_unit <<< "$gw_entry"

        local count_499
        count_499=$(tail -100 "$gw_log" 2>/dev/null | grep -c "status 499" 2>/dev/null)
        count_499=${count_499:-0}

        if [ "$count_499" -ge 3 ]; then
            send_alert "CRIT" "$gw_name" "WhatsApp" \
                "Boucle 499 détectée (${count_499}x récemment)" \
                "$(date '+%H:%M')" \
                "WhatsApp en reconnexion permanente — messages intermittents" \
                "Purger credentials puis restart ${gw_unit}" \
                ""

            bash "${SCRIPT_DIR}/whatsapp-creds-pruner.sh" 2>/dev/null
            echo "${LOG_PREFIX} AUTO-FIX: pruner lancé pour $gw_name suite à boucle 499"
        fi
    done
}

# === CHECK BLOAT CREDENTIALS WHATSAPP ===

check_whatsapp_creds_bloat() {
    # Auto-découverte de tous les dossiers credentials
    local THRESHOLD=500
    local WARN=350

    for creds_dir in $(find /home/gilles/.openclaw*/credentials/whatsapp/ -mindepth 1 -maxdepth 1 -type d 2>/dev/null); do
        local account=$(basename "$creds_dir")
        local profile=$(echo "$creds_dir" | grep -oP '\.openclaw[^/]*')
        local label="${profile}/${account}"

        local prunable=0
        for pattern in pre-key- sender-key- session-; do
            prunable=$((prunable + $(ls -1 "${creds_dir}/${pattern}"* 2>/dev/null | wc -l)))
        done

        if [ "$prunable" -ge "$THRESHOLD" ]; then
            send_alert "CRIT" "WhatsApp Credentials" "$label" \
                "Bloat credentials: ${prunable} fichiers (seuil: ${THRESHOLD})" \
                "$(date '+%H:%M')" \
                "Risque boucle 499 — session WhatsApp instable" \
                "Purge auto en cours (whatsapp-creds-pruner.sh)" \
                ""
            bash "${SCRIPT_DIR}/whatsapp-creds-pruner.sh" 2>/dev/null
        elif [ "$prunable" -ge "$WARN" ]; then
            send_alert "WARN" "WhatsApp Credentials" "$label" \
                "Credentials en hausse: ${prunable} fichiers (warn: ${WARN})" \
                "$(date '+%H:%M')" \
                "Approche du seuil critique (${THRESHOLD})" \
                "Surveillance renforcée" \
                ""
        fi
    done
}

# === CHECK SSL & SOUS-DOMAINES (toutes les heures seulement) ===

check_ssl_and_subdomains() {
    local minute
    minute=$(date '+%M')
    # Ne lancer qu'au passage de l'heure (minute 00 ou 02)
    [ "$minute" != "00" ] && [ "$minute" != "02" ] && return

    local now_epoch
    now_epoch=$(date +%s)

    for domain in app.mybotia.com admin.mybotia.com prospection.mybotia.com listmonk.mybotia.com; do
        # SSL
        local expiry_str
        expiry_str=$(echo | openssl s_client -servername "$domain" -connect "${domain}:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
        if [ -n "$expiry_str" ]; then
            local expiry_epoch
            expiry_epoch=$(date -d "$expiry_str" +%s 2>/dev/null)
            local days_left=$(( (expiry_epoch - now_epoch) / 86400 ))
            if [ "$days_left" -lt 14 ]; then
                send_alert "WARN" "SSL ${domain}" "-" \
                    "Certificat expire dans ${days_left} jours" \
                    "maintenant" \
                    "HTTPS sera cassé à l'expiration" \
                    "Vérifier certbot renew" \
                    ""
            fi
        fi

        # HTTP check
        local http_code
        http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "https://${domain}" 2>/dev/null)
        if [ "$http_code" != "200" ] && [ "$http_code" != "301" ] && [ "$http_code" != "302" ]; then
            send_alert "WARN" "Sous-domaine ${domain}" "-" \
                "HTTP ${http_code}" \
                "$(date '+%H:%M')" \
                "Site inaccessible" \
                "Vérifier Apache/Nginx config" \
                ""
        fi
    done
}

# === MAIN ===

# Gateways
check_and_restart "mybotia-gateway" "18789" \
    "openclaw-gateway.service" \
    "mybotia-gateway"

check_and_restart "vlmedical-gateway" "18790" \
    "openclaw-gateway-vlmedical.service" \
    "vlmedical-gateway"

check_and_restart "lucy-gateway" "18795" \
    "openclaw-gateway-lucy.service" \
    "lucy-gateway"

# WhatsApp
check_whatsapp_creds "mybotia-gateway" \
    "/home/gilles/.openclaw/credentials/whatsapp/default/creds.json" \
    "openclaw-gateway.service" \
    "lea-whatsapp"

# Lucy WA (IGH) — compte "lucy" (pas "default")
check_whatsapp_creds "lucy-gateway" \
    "/home/gilles/.openclaw-lucy/.openclaw/credentials/whatsapp/lucy/creds.json" \
    "openclaw-gateway-lucy.service" \
    "lucy-whatsapp"

# Nina WhatsApp — compte séparé sur mybotia-gateway
check_whatsapp_creds "mybotia-gateway" \
    "/home/gilles/.openclaw/credentials/whatsapp/nina/creds.json" \
    "openclaw-gateway.service" \
    "nina-whatsapp"

# VL Medical = Max, mais LOGGED_OUT — on track quand meme pour le jour ou il revient
# On ne consomme PAS d'error budget pour Max (SLO = N/A)
# check_whatsapp_creds "vlmedical-gateway" \
#     "/home/gilles/.openclaw-vlmedical/credentials/whatsapp/default/creds.json" \
#     "18790" \
#     "openclaw --profile vlmedical gateway --port 18790" \
#     "max-whatsapp"

# WhatsApp 499 loop + credentials bloat
check_whatsapp_499_loop
check_whatsapp_creds_bloat

# Système
check_system

# Vérification units systemd
check_systemd_services

# SSL & sous-domaines (1x/heure)
check_ssl_and_subdomains

# Voice-poc — systemd service (port 3100)
if ! curl -sf --max-time 3 "http://127.0.0.1:3100/" > /dev/null 2>&1; then
    echo "${LOG_PREFIX} ALERTE: voice-poc ne répond pas. Restart via systemd..."
    systemctl --user restart voice-poc.service 2>&1
    echo "${LOG_PREFIX} voice-poc restart lancé via systemctl"
fi
