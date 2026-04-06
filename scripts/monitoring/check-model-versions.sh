#!/bin/bash
# check-model-versions.sh — Vérifie les versions de modèles sur toutes les gateways
# Cron: intégré au daily-report.sh (7h) + appelable standalone
# Alerte Telegram CRIT si modèle obsolète détecté

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/monitoring.conf"

# Modèles actuels valides
VALID_MODELS=(
    "anthropic/claude-opus-4-6"
    "claude-opus-4-6"
    "anthropic/claude-sonnet-4-6"
    "claude-sonnet-4-6"
    "groq/llama-3.3-70b-versatile"
)

# Modèles obsolètes connus (alerte immédiate)
OBSOLETE_MODELS=(
    "anthropic/claude-sonnet-4-5-20250929"
    "claude-sonnet-4-5-20250929"
    "anthropic/claude-sonnet-4-5"
    "claude-sonnet-4-5"
    "anthropic/claude-3-5-sonnet"
    "claude-3-5-sonnet"
    "anthropic/claude-3-opus"
    "claude-3-opus"
)

# Gateways à vérifier
declare -A GATEWAYS
GATEWAYS[mybotia-gateway]="/home/gilles/.openclaw/openclaw.json"
GATEWAYS[vlmedical-gateway]="/home/gilles/.openclaw-vlmedical/openclaw.json"
GATEWAYS[lucy-gateway]="/home/gilles/.openclaw-lucy/openclaw.json"

ISSUES=""
ISSUE_COUNT=0

is_valid_model() {
    local model="$1"
    for valid in "${VALID_MODELS[@]}"; do
        [[ "$model" == "$valid" ]] && return 0
    done
    return 1
}

is_obsolete_model() {
    local model="$1"
    for obs in "${OBSOLETE_MODELS[@]}"; do
        [[ "$model" == "$obs" ]] && return 0
    done
    return 1
}

check_gateway() {
    local gw_name="$1"
    local config_file="$2"

    if [[ ! -f "$config_file" ]]; then
        echo "⚠️ Config introuvable: $config_file ($gw_name)"
        return
    fi

    # Extraire tous les modèles configurés
    local models
    models=$(python3 -c "
import json, sys
with open('$config_file') as f:
    c = json.load(f)

models = []
agents = c.get('agents', {})

# defaults.model.primary
dp = agents.get('defaults', {}).get('model', {}).get('primary', '')
if dp: models.append(('defaults.model.primary', dp))

# defaults.pdfModel
pm = agents.get('defaults', {}).get('pdfModel', '')
if pm: models.append(('defaults.pdfModel', pm))

# defaults.model.fallbacks
for fb in agents.get('defaults', {}).get('model', {}).get('fallbacks', []):
    models.append(('defaults.model.fallbacks', fb))

# agents.list[*].model.primary
for agent in agents.get('list', []):
    aid = agent.get('id', 'unknown')
    ap = agent.get('model', {}).get('primary', '')
    if ap: models.append((f'agent:{aid}.model.primary', ap))
    for fb in agent.get('model', {}).get('fallbacks', []):
        models.append((f'agent:{aid}.model.fallbacks', fb))

# tools.media.image.models
for im in c.get('tools', {}).get('media', {}).get('image', {}).get('models', []):
    m = im.get('model', '')
    if m: models.append(('tools.media.image.model', m))

for loc, model in models:
    print(f'{loc}|{model}')
" 2>/dev/null)

    while IFS='|' read -r location model; do
        [[ -z "$model" ]] && continue
        if is_obsolete_model "$model"; then
            ISSUES="${ISSUES}🚨 MODÈLE OBSOLÈTE détecté\nGateway: ${gw_name}\nConfig: ${location}\nModèle: ${model}\nAction: Mettre à jour openclaw.json\n\n"
            ISSUE_COUNT=$((ISSUE_COUNT + 1))
        elif ! is_valid_model "$model"; then
            # Modèle inconnu — pas forcément obsolète, mais à surveiller
            ISSUES="${ISSUES}⚠️ Modèle non référencé\nGateway: ${gw_name}\nConfig: ${location}\nModèle: ${model}\nAction: Vérifier si ce modèle est valide\n\n"
        fi
    done <<< "$models"
}

# === EXÉCUTION ===

for gw_name in "${!GATEWAYS[@]}"; do
    check_gateway "$gw_name" "${GATEWAYS[$gw_name]}"
done

# Résultat
if [[ $ISSUE_COUNT -gt 0 ]]; then
    ALERT_MSG="🚨 ALERTE MODÈLES — ${ISSUE_COUNT} problème(s) détecté(s)

${ISSUES}Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"

    # Alerte Telegram
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        -d text="${ALERT_MSG}" \
        -d parse_mode="Markdown" > /dev/null 2>&1

    echo "❌ ${ISSUE_COUNT} modèle(s) obsolète(s) détecté(s) — alerte envoyée"
    echo -e "$ISSUES"
    exit 1
else
    echo "✅ Tous les modèles sont à jour sur les 3 gateways"
    exit 0
fi
