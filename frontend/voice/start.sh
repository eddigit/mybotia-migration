#!/bin/bash
cd /home/gilles/apps/voice-poc
set -a; source .env; set +a
while true; do
  node server.js 2>&1 | tee -a /tmp/voice-v2.log
  echo "[$(date)] Voice V2 crashed, restarting in 2s..." >> /tmp/voice-v2.log
  sleep 2
done
