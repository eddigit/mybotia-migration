#!/bin/bash
# ============================================
# Backup quotidien — Configs critiques MyBotIA
# Version: 1.0.0
# Date: 26/02/2026
# Cron: 0 3 * * * (tous les jours à 3h)
# Rétention: 30 jours
# ============================================

BACKUP_DIR="/home/gilles/backups"
DATE=$(date +%Y-%m-%d_%H%M)
BACKUP_NAME="config-backup-${DATE}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"
RETENTION_DAYS=30
LOG="/home/gilles/scripts/monitoring/logs/backup.log"

mkdir -p "$BACKUP_PATH" "$(dirname "$LOG")"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

log "=== DEBUT BACKUP ${BACKUP_NAME} ==="

ERRORS=0

# 1. openclaw.json (gateway principale)
if cp ~/.openclaw/openclaw.json "$BACKUP_PATH/" 2>/dev/null; then
    log "✅ openclaw.json"
else
    log "❌ openclaw.json MANQUANT"; ((ERRORS++))
fi

# 2. openclaw.json (gateway VL Medical)
if cp ~/.openclaw-vlmedical/openclaw.json "$BACKUP_PATH/openclaw-vlmedical.json" 2>/dev/null; then
    log "✅ openclaw-vlmedical.json"
else
    log "❌ openclaw-vlmedical.json MANQUANT"; ((ERRORS++))
fi

# 3. Dockerfile + requirements.txt + docker-compose.yml
mkdir -p "$BACKUP_PATH/docker"
for f in Dockerfile.gateway requirements.txt docker-compose.yml; do
    if cp ~/.openclaw/docker/$f "$BACKUP_PATH/docker/" 2>/dev/null; then
        log "✅ docker/$f"
    else
        log "⚠️ docker/$f non trouvé"
    fi
done

# 4. Tools Python (workspace principal — Léa)
mkdir -p "$BACKUP_PATH/tools-lea"
cp ~/.openclaw/workspace/tools/*.py "$BACKUP_PATH/tools-lea/" 2>/dev/null && \
    log "✅ tools Léa ($(ls "$BACKUP_PATH/tools-lea/" | wc -l) fichiers)" || \
    log "⚠️ tools Léa — aucun fichier"

# 5. Skills (workspace principal)
if [ -d ~/.openclaw/workspace/skills ]; then
    cp -r ~/.openclaw/workspace/skills "$BACKUP_PATH/skills-lea" 2>/dev/null
    log "✅ skills Léa"
fi

# 6. Tools Oscar
mkdir -p "$BACKUP_PATH/tools-oscar"
cp ~/.openclaw/workspace-oscar/tools/*.py "$BACKUP_PATH/tools-oscar/" 2>/dev/null && \
    log "✅ tools Oscar ($(ls "$BACKUP_PATH/tools-oscar/" | wc -l) fichiers)" || \
    log "⚠️ tools Oscar — aucun fichier"

# 7. Tools Julian
mkdir -p "$BACKUP_PATH/tools-julian"
cp ~/.openclaw/workspace-julian/tools/*.py "$BACKUP_PATH/tools-julian/" 2>/dev/null && \
    log "✅ tools Julian ($(ls "$BACKUP_PATH/tools-julian/" | wc -l) fichiers)" || \
    log "⚠️ tools Julian — aucun fichier"

# 8. Tools Max (VL Medical)
mkdir -p "$BACKUP_PATH/tools-max"
cp ~/.openclaw-vlmedical/workspace-vlmedical-admin/tools/*.py "$BACKUP_PATH/tools-max/" 2>/dev/null && \
    log "✅ tools Max" || log "⚠️ tools Max — aucun fichier"

# 9. Scripts monitoring
mkdir -p "$BACKUP_PATH/monitoring"
cp /home/gilles/scripts/monitoring/*.sh "$BACKUP_PATH/monitoring/" 2>/dev/null
cp /home/gilles/scripts/monitoring/monitoring.conf "$BACKUP_PATH/monitoring/" 2>/dev/null
cp /home/gilles/scripts/monitoring/lib/*.sh "$BACKUP_PATH/monitoring/" 2>/dev/null
log "✅ scripts monitoring"

# 10. Apache vhosts
mkdir -p "$BACKUP_PATH/apache"
cp /etc/apache2/sites-available/*mybotia* "$BACKUP_PATH/apache/" 2>/dev/null
log "✅ apache vhosts"

# 11. Systemd service VL Medical
cp ~/.config/systemd/user/openclaw-gateway-vlmedical.service "$BACKUP_PATH/" 2>/dev/null && \
    log "✅ systemd VL Medical" || log "⚠️ service VL Medical non trouvé"

# Compression
cd "$BACKUP_DIR" && tar czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME" && rm -rf "$BACKUP_NAME"
SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)
log "✅ Archive: ${BACKUP_NAME}.tar.gz (${SIZE})"

# Rétention — supprimer les backups > 30 jours
DELETED=$(find "$BACKUP_DIR" -name "config-backup-*.tar.gz" -mtime +${RETENTION_DAYS} -delete -print | wc -l)
if [ "$DELETED" -gt 0 ]; then
    log "🗑️ ${DELETED} ancien(s) backup(s) supprimé(s) (>${RETENTION_DAYS}j)"
fi

# Résumé
TOTAL=$(ls "$BACKUP_DIR"/config-backup-*.tar.gz 2>/dev/null | wc -l)
log "=== FIN BACKUP — ${ERRORS} erreur(s) — ${TOTAL} backups stockés ==="

if [ "$ERRORS" -gt 0 ]; then
    echo "❌ Backup terminé avec ${ERRORS} erreur(s)"
    exit 1
else
    echo "✅ Backup OK — ${BACKUP_NAME}.tar.gz (${SIZE}) — ${TOTAL} backups stockés"
fi
