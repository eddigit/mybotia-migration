#!/bin/bash
# Alerte si RAM > 80% ou Swap > 70%
RAM_PERCENT=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
SWAP_PERCENT=$(free | grep Swap | awk '{printf "%.0f", $3/$2 * 100}')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

if [ "$RAM_PERCENT" -gt 80 ]; then
  curl -s -X POST "https://api.telegram.org/bot8648752363:$(cat /home/gilles/.jacques-env 2>/dev/null | grep TELEGRAM_TOKEN | cut -d= -f2)/sendMessage" \
    -d chat_id=1801835052 \
    -d text="🔴 RAM CRITIQUE: ${RAM_PERCENT}% — Swap: ${SWAP_PERCENT}% — $(date)" \
    -d parse_mode=HTML > /dev/null 2>&1
fi

if [ "$SWAP_PERCENT" -gt 70 ]; then
  curl -s -X POST "https://api.telegram.org/bot8648752363:$(cat /home/gilles/.jacques-env 2>/dev/null | grep TELEGRAM_TOKEN | cut -d= -f2)/sendMessage" \
    -d chat_id=1801835052 \
    -d text="⚠️ SWAP ÉLEVÉ: ${SWAP_PERCENT}% — RAM: ${RAM_PERCENT}% — $(date)" \
    -d parse_mode=HTML > /dev/null 2>&1
fi
