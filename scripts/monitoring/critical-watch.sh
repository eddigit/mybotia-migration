#!/bin/bash
# critical-watch.sh v2.0 — Alertes + Auto-remediation MyBotIA
# Cron: */5 * * * * /home/gilles/scripts/monitoring/critical-watch.sh
#
# WORKFLOW:
# 1. Detecte un probleme connu
# 2. Tente un auto-fix IMMEDIATEMENT
# 3. Si fix OK → alerte "corrige automatiquement" (info)
# 4. Si fix ECHOUE → alerte critique "intervention requise"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/monitoring.conf"
source "${SCRIPT_DIR}/lib/checks.sh"
source "${SCRIPT_DIR}/lib/notify.sh"
source "${SCRIPT_DIR}/lib/autofix.sh"

mkdir -p "${STATE_DIR}" "${LOG_DIR}"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
ALERTS_SENT=0

# --- CHECK 1 : Gateway MyBotIA ---
check_gateway_mybotia
gw1_status=$?
if [ $gw1_status -ne 0 ]; then
    # AUTO-FIX: restart systemd
    fix_gateway_mybotia
    fix_result=$?
    if [ $fix_result -eq 0 ]; then
        send_critical_alert "gateway-mybotia-fixed" "Gateway MyBotIA etait DOWN — AUTO-CORRIGE par restart systemd.
Tout est rentre dans l'ordre. Aucune action requise."
        clear_alert "gateway-mybotia"
        gw1_status=0  # corrige
    else
        send_critical_alert "gateway-mybotia" "Gateway MyBotIA DOWN — auto-fix ECHOUE !
Le restart systemd n'a pas fonctionne.
Action manuelle requise: tail /tmp/mybotia-gateway.log && systemctl status openclaw-mybotia"
    fi
    ALERTS_SENT=$((ALERTS_SENT + 1))
else
    clear_alert "gateway-mybotia"
    clear_alert "gateway-mybotia-fixed"
fi

# --- CHECK 2 : Gateway VL Medical ---
check_gateway_vlmedical
gw2_status=$?
if [ $gw2_status -ne 0 ]; then
    fix_gateway_vlmedical
    fix_result=$?
    if [ $fix_result -eq 0 ]; then
        send_critical_alert "gateway-vlmedical-fixed" "Gateway VL Medical etait DOWN — AUTO-CORRIGE par restart service.
Tout est rentre dans l'ordre."
        clear_alert "gateway-vlmedical"
    else
        send_critical_alert "gateway-vlmedical" "Gateway VL Medical DOWN — auto-fix ECHOUE !
Action: tail /tmp/vlmedical-gateway.log && systemctl status openclaw-vlmedical"
    fi
    ALERTS_SENT=$((ALERTS_SENT + 1))
else
    clear_alert "gateway-vlmedical"
    clear_alert "gateway-vlmedical-fixed"
fi

# --- CHECK : Gateway Lucy (IGH) ---
check_gateway_lucy
gw_lucy_status=$?
if [ $gw_lucy_status -ne 0 ]; then
    fix_gateway_lucy
    fix_result=$?
    if [ $fix_result -eq 0 ]; then
        send_critical_alert "gateway-lucy-fixed" "Gateway Lucy (IGH) etait DOWN — AUTO-CORRIGE par restart.
Tout est rentre dans l'ordre."
        clear_alert "gateway-lucy"
    else
        send_critical_alert "gateway-lucy" "🚨 Gateway Lucy (IGH) DOWN — auto-fix ECHOUE !
Action: tail /tmp/lucy-gateway.log
Config: /home/gilles/.openclaw-lucy/openclaw.json"
    fi
    ALERTS_SENT=$((ALERTS_SENT + 1))
else
    clear_alert "gateway-lucy"
    clear_alert "gateway-lucy-fixed"
fi

# --- CHECK 3 : WhatsApp ---
if [ $gw1_status -eq 0 ]; then
    check_whatsapp
    wa_status=$?
    if [ $wa_status -eq 2 ]; then
        send_critical_alert "whatsapp-disconnect" "WhatsApp DECONNECTE !
${CHECK_MSG}
Pas d'auto-fix dispo pour WhatsApp — verification manuelle requise."
        ALERTS_SENT=$((ALERTS_SENT + 1))
    elif [ $wa_status -eq 1 ]; then
        log_msg "WARNING: ${CHECK_MSG}"
    else
        clear_alert "whatsapp-disconnect"
    fi
fi

# --- CHECK 4 : RAM ---
check_ram
ram_status=$?
if [ $ram_status -ne 0 ]; then
    send_critical_alert "ram-high" "RAM elevee !
${CHECK_MSG}
Top processus:
$(ps aux --sort=-%mem | head -5)"
    ALERTS_SENT=$((ALERTS_SENT + 1))
else
    clear_alert "ram-high"
fi

# --- CHECK 5 : Outils Python sur le host ---
if [ $gw1_status -eq 0 ]; then
    check_tools_python
    tools_status=$?
    if [ $tools_status -eq 2 ]; then
        send_critical_alert "tools-python" "OUTILS LEA HORS SERVICE !
${CHECK_MSG}
Intervention manuelle requise (python3 ou modules manquants sur le host)."
        ALERTS_SENT=$((ALERTS_SENT + 1))
    elif [ $tools_status -eq 1 ]; then
        send_critical_alert "tools-python-warn" "Outils Lea partiellement KO
${CHECK_MSG}"
        ALERTS_SENT=$((ALERTS_SENT + 1))
    else
        clear_alert "tools-python"
        clear_alert "tools-python-fixed"
        clear_alert "tools-python-warn"
    fi
fi

# --- LOG ---
if [ $ALERTS_SENT -gt 0 ]; then
    log_msg "CRITICAL-WATCH: ${ALERTS_SENT} alerte(s) envoyee(s) (avec auto-fix)"
else
    MINUTE=$(date '+%M')
    if [ "$MINUTE" = "00" ]; then
        log_msg "CRITICAL-WATCH: tous les checks OK"
    fi
fi
