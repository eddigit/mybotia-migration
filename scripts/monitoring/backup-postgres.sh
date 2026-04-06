#!/bin/bash
# ============================================
# Backup quotidien — PostgreSQL mybotia_crm
# Cron: 30 2 * * * (tous les jours à 2h30)
# Rétention: 30 jours
# ============================================

BACKUP_DIR="/home/gilles/backups/postgres"
DATE=$(date +%Y-%m-%d_%H%M)
BACKUP_NAME="mybotia_crm-${DATE}.sql.gz"
RETENTION_DAYS=30
LOG="/home/gilles/scripts/monitoring/logs/backup-postgres.log"

mkdir -p "$BACKUP_DIR" "$(dirname "$LOG")"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

log "=== DEBUT BACKUP PostgreSQL ==="

# Dump via docker exec
if docker exec prospection_postgres pg_dump -U prospection mybotia_crm 2>/dev/null | gzip > "${BACKUP_DIR}/${BACKUP_NAME}"; then
    SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}" | cut -f1)
    # Vérifier que le fichier n'est pas vide
    BYTES=$(stat -c%s "${BACKUP_DIR}/${BACKUP_NAME}" 2>/dev/null || echo 0)
    if [ "$BYTES" -lt 100 ]; then
        log "❌ Dump vide ou trop petit (${BYTES} octets)"
        rm -f "${BACKUP_DIR}/${BACKUP_NAME}"
        echo "❌ Backup PostgreSQL échoué — dump vide"
        exit 1
    fi
    log "✅ Dump: ${BACKUP_NAME} (${SIZE})"
else
    log "❌ pg_dump échoué"
    rm -f "${BACKUP_DIR}/${BACKUP_NAME}"
    echo "❌ Backup PostgreSQL échoué"
    exit 1
fi

# Rétention — supprimer les backups > 30 jours
DELETED=$(find "$BACKUP_DIR" -name "mybotia_crm-*.sql.gz" -mtime +${RETENTION_DAYS} -delete -print | wc -l)
if [ "$DELETED" -gt 0 ]; then
    log "🗑️ ${DELETED} ancien(s) backup(s) supprimé(s) (>${RETENTION_DAYS}j)"
fi

TOTAL=$(ls "$BACKUP_DIR"/mybotia_crm-*.sql.gz 2>/dev/null | wc -l)
log "=== FIN BACKUP PostgreSQL — ${TOTAL} backups stockés ==="
echo "✅ Backup PostgreSQL OK — ${BACKUP_NAME} (${SIZE}) — ${TOTAL} backups stockés"
