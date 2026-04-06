#!/bin/bash
# MyBotIA daily maintenance cron
# Run: 0 3 * * * /var/www/html/mybotia/private/maintenance.sh >> /var/log/mybotia-maintenance.log 2>&1

PRIVATE_DIR="/var/www/html/mybotia/private"
DB_PATH="$PRIVATE_DIR/mybotia.db"
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

echo "$LOG_PREFIX Starting maintenance..."

# 1. Cleanup expired PHP sessions (older than 24h)
SESSION_DIR=$(php -r 'echo session_save_path() ?: sys_get_temp_dir();')
if [ -d "$SESSION_DIR" ]; then
    CLEANED=$(find "$SESSION_DIR" -name 'sess_mybotia*' -mtime +1 -delete -print 2>/dev/null | wc -l)
    echo "$LOG_PREFIX Cleaned $CLEANED expired sessions"
fi

# 2. SQLite maintenance: VACUUM + integrity check
if [ -f "$DB_PATH" ]; then
    INTEGRITY=$(sqlite3 "$DB_PATH" "PRAGMA integrity_check;" 2>&1)
    echo "$LOG_PREFIX DB integrity: $INTEGRITY"
    
    SIZE_BEFORE=$(stat -c%s "$DB_PATH" 2>/dev/null || echo 0)
    sqlite3 "$DB_PATH" "VACUUM;" 2>/dev/null
    SIZE_AFTER=$(stat -c%s "$DB_PATH" 2>/dev/null || echo 0)
    echo "$LOG_PREFIX DB size: ${SIZE_BEFORE}B -> ${SIZE_AFTER}B"
fi

# 3. Rotate Apache error log if > 10MB
ERROR_LOG="/var/log/apache2/wildcard-mybotia-error.log"
if [ -f "$ERROR_LOG" ]; then
    SIZE=$(stat -c%s "$ERROR_LOG" 2>/dev/null || echo 0)
    if [ "$SIZE" -gt 10485760 ]; then
        mv "$ERROR_LOG" "${ERROR_LOG}.$(date '+%Y%m%d')"
        systemctl reload apache2 2>/dev/null
        echo "$LOG_PREFIX Rotated error log (was ${SIZE}B)"
    fi
fi

# 4. Backup database (keep last 7 days)
BACKUP_DIR="$PRIVATE_DIR/backups"
mkdir -p "$BACKUP_DIR"
if [ -f "$DB_PATH" ]; then
    cp "$DB_PATH" "$BACKUP_DIR/mybotia-$(date '+%Y%m%d').db"
    # Remove backups older than 7 days
    find "$BACKUP_DIR" -name "mybotia-*.db" -mtime +7 -delete 2>/dev/null
    echo "$LOG_PREFIX DB backup created"
fi

# 5. Quick health check
HEALTH=$(php -r '
$_SERVER["REMOTE_ADDR"] = "127.0.0.1";
$_SERVER["REQUEST_METHOD"] = "GET";
chdir("/var/www/html/mybotia/public/api");
ob_start();
include "health.php";
$out = ob_get_clean();
$data = json_decode($out, true);
echo $data["status"] ?? "error";
echo " | users=" . ($data["stats"]["users_total"] ?? "?");
echo " | prefs=" . ($data["stats"]["preferences"] ?? "?");
echo " | disk_free=" . ($data["stats"]["disk_free_gb"] ?? "?") . "GB";
' 2>/dev/null)
echo "$LOG_PREFIX Health: $HEALTH"

echo "$LOG_PREFIX Maintenance complete"
echo "---"
