#!/bin/bash
# daily-report.sh v2.0 SRE — Rapport quotidien + veille technique
# Cron: 0 7 * * * /home/gilles/scripts/monitoring/daily-report.sh
#
# 1. Checks de santé (gateways, WhatsApp, système, SSL, sous-domaines)
# 2. SLO compliance (lecture slo-tracker.json de la veille)
# 3. Veille technique OpenClaw (version, changelog, issues GitHub)
# 4. Envoi rapport structuré Telegram + Email

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/monitoring.conf"
source "${SCRIPT_DIR}/lib/checks.sh"
source "${SCRIPT_DIR}/lib/notify.sh"

mkdir -p "${STATE_DIR}" "${LOG_DIR}"

log_msg "========== RAPPORT SRE QUOTIDIEN DEBUT =========="

DATE_FR=$(date '+%d/%m/%Y a %Hh%M')
HOSTNAME=$(hostname)
UPTIME=$(uptime -p 2>/dev/null || uptime)

REPORT=""
ISSUES=""
ISSUE_COUNT=0
WARNING_COUNT=0

add_result() {
    local status=$1
    local msg="$2"

    if [ $status -eq 0 ]; then
        REPORT="${REPORT}✅ ${msg}\n"
    elif [ $status -eq 1 ]; then
        REPORT="${REPORT}⚠️ ${msg}\n"
        ISSUES="${ISSUES}⚠️ ${msg}\n"
        WARNING_COUNT=$((WARNING_COUNT + 1))
    else
        REPORT="${REPORT}❌ ${msg}\n"
        ISSUES="${ISSUES}❌ ${msg}\n"
        ISSUE_COUNT=$((ISSUE_COUNT + 1))
    fi
}

# === SECTION 1 : CHECKS DE SANTÉ ===

# Gateways
check_gateway_mybotia
add_result $? "$CHECK_MSG"
check_gateway_vlmedical
add_result $? "$CHECK_MSG"
check_gateway_lucy
add_result $? "$CHECK_MSG"

# WhatsApp
check_whatsapp
add_result $? "$CHECK_MSG"

# Telegram bots
check_telegram_bots
add_result $? "$CHECK_MSG"

# Ressources système
check_ram
add_result $? "$CHECK_MSG"
check_disk
add_result $? "$CHECK_MSG"

# Outils Python
check_tools_python
add_result $? "$CHECK_MSG"

# Version OpenClaw
check_openclaw_version
add_result $? "$CHECK_MSG"

# Certificats SSL
check_ssl_certs
add_result $? "$CHECK_MSG"

# Sous-domaines
check_subdomains
add_result $? "$CHECK_MSG"

# Process gateways host
check_gateway_processes
add_result $? "$CHECK_MSG"

# Doublons Docker
check_docker_doublons
add_result $? "$CHECK_MSG"

# === SECTION 2 : SLO COMPLIANCE (veille) ===

SLO_REPORT=""
TRACKER="/home/gilles/watchdog/state/slo-tracker.json"

if [ -f "$TRACKER" ]; then
    SLO_REPORT=$(python3 -c "
import json

with open('$TRACKER') as f:
    data = json.load(f)

day = data.get('current_day', {})
services = day.get('services', {})
system = day.get('system', {})

lines = []
lines.append('SLO Compliance (dernières 24h):')

for name, svc in services.items():
    target = svc.get('slo_target', 0)
    actual = svc.get('uptime_pct', 100)
    checks = svc.get('checks_total', 0)
    budget = svc.get('error_budget_remaining_sec', 0)
    budget_total = svc.get('error_budget_total_sec', 0)
    status = svc.get('status', 'OK')

    icon = '✅' if status == 'OK' else '⚠️' if 'WARN' in status else '🔴'
    lines.append(f'  {icon} {name}: {actual}% (SLO {target}%) — budget {budget}s/{budget_total}s — {checks} checks')

lines.append('')
lines.append('Système:')
for name, res in system.items():
    pct = res.get('last_pct', '?')
    status = res.get('status', 'OK')
    icon = '✅' if status == 'OK' else '⚠️' if status == 'WARN' else '🔴'
    lines.append(f'  {icon} {name}: {pct}%')

print('\n'.join(lines))
" 2>/dev/null)
fi

# === SECTION 3 : VEILLE TECHNIQUE ===

VEILLE_REPORT=""

# Version installée
INSTALLED_VERSION=$("${OPENCLAW_BIN}" --version 2>/dev/null | head -1)

# Dernière version npm
LATEST_NPM=$(npm view openclaw version 2>/dev/null)

# Dernière release GitHub
LATEST_GITHUB=$(curl -s --max-time 10 "https://api.github.com/repos/${GITHUB_REPO}/releases/latest" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('tag_name','inconnu').lstrip('v'))" 2>/dev/null)

# Changelog résumé (si nouvelle version)
CHANGELOG_SUMMARY=""
if [ -n "$LATEST_GITHUB" ] && [ "$LATEST_GITHUB" != "inconnu" ] && [ "$INSTALLED_VERSION" != "$LATEST_GITHUB" ]; then
    CHANGELOG_BODY=$(curl -s --max-time 10 "https://api.github.com/repos/${GITHUB_REPO}/releases/latest" 2>/dev/null | python3 -c "
import sys, json, re
body = json.load(sys.stdin).get('body', '')
# Chercher les mots-clés critiques
keywords = ['BREAKING', 'WhatsApp', 'Baileys', 'heartbeat', 'OAuth', 'auth', 'Telegram', 'cron', 'security', 'sandbox', 'memory', 'stale-socket']
lines = body.split('\n')
relevant = []
for line in lines:
    for kw in keywords:
        if kw.lower() in line.lower():
            relevant.append(line.strip()[:120])
            break
if relevant:
    print('\n'.join(relevant[:8]))
else:
    print('Pas de changement critique détecté')
" 2>/dev/null)
    CHANGELOG_SUMMARY="⚡ NOUVELLE VERSION DISPONIBLE
  Installée: ${INSTALLED_VERSION}
  Disponible: ${LATEST_GITHUB} (npm: ${LATEST_NPM})
  Changements pertinents:
${CHANGELOG_BODY}"
else
    CHANGELOG_SUMMARY="OpenClaw: ${INSTALLED_VERSION} (à jour)"
fi

# Issues GitHub pertinentes (whatsapp, baileys, stale-socket, memory)
GITHUB_ISSUES=""
for keyword in whatsapp baileys stale-socket memory; do
    issue_count=$(curl -s --max-time 10 "https://api.github.com/search/issues?q=${keyword}+repo:${GITHUB_REPO}+is:open&per_page=1" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('total_count',0))" 2>/dev/null)
    if [ "${issue_count:-0}" -gt 0 ]; then
        GITHUB_ISSUES="${GITHUB_ISSUES}  ${keyword}: ${issue_count} issue(s) ouverte(s)\n"
    fi
done

VEILLE_REPORT="Veille technique:
  ${CHANGELOG_SUMMARY}
  Node.js: $(node --version 2>/dev/null)
  Claude Code: $(claude --version 2>/dev/null | head -1)
Issues GitHub ouvertes (nos problèmes):
$(echo -e "${GITHUB_ISSUES:-  Aucune issue pertinente}")"

# Sauvegarder la veille du jour
VEILLE_FILE="/home/gilles/watchdog/memory/veille-$(date '+%Y-%m-%d').md"
cat > "$VEILLE_FILE" <<VEILLE_EOF
# Veille technique — $(date '+%Y-%m-%d')

## Versions
- OpenClaw installé: ${INSTALLED_VERSION}
- OpenClaw disponible (npm): ${LATEST_NPM}
- OpenClaw disponible (GitHub): ${LATEST_GITHUB}
- Node.js: $(node --version 2>/dev/null)
- Claude Code: $(claude --version 2>/dev/null | head -1)

## Changelog
${CHANGELOG_SUMMARY}

## Issues GitHub
$(echo -e "${GITHUB_ISSUES:-Aucune issue pertinente}")
VEILLE_EOF

# === COMPILATION DU RAPPORT ===

if [ $ISSUE_COUNT -eq 0 ] && [ $WARNING_COUNT -eq 0 ]; then
    HEADER="✅ Rapport SRE ${DATE_FR} — Tout OK"
else
    HEADER="🔴 Rapport SRE ${DATE_FR} — ${ISSUE_COUNT} problème(s), ${WARNING_COUNT} avertissement(s)"
fi

FULL_REPORT="${HEADER}
Serveur: ${HOSTNAME} | Uptime: ${UPTIME}

--- CHECKS ---
$(echo -e "${REPORT}")
--- SLO ---
${SLO_REPORT}

--- VEILLE ---
${VEILLE_REPORT}

--- Monitoring SRE MaBoiteIA v2.0 ---"

# Résumé des problèmes s'il y en a
if [ $ISSUE_COUNT -gt 0 ] || [ $WARNING_COUNT -gt 0 ]; then
    FULL_REPORT="${FULL_REPORT}

PROBLÈMES:
$(echo -e "${ISSUES}")"
fi

# === ENVOI ===

log_msg "Rapport SRE compilé: ${ISSUE_COUNT} erreurs, ${WARNING_COUNT} warnings"
echo -e "${FULL_REPORT}" >> "${LOG_FILE}"

# Telegram (rapport complet)
send_telegram "${FULL_REPORT}"

# Email (backup)
send_email "[SRE MyBotIA] Rapport $(date '+%d/%m/%Y')" "${FULL_REPORT}"

log_msg "========== RAPPORT SRE QUOTIDIEN FIN =========="
