#!/bin/bash
# =============================================================================
# VPS Disaster Recovery — Backup chiffré quotidien
# Créé par Jacques (Claude Code) — 2026-03-29
#
# Ce script collecte TOUT ce qui est nécessaire pour reconstruire le VPS
# from scratch, chiffre le tout avec age, et push vers GitHub.
# =============================================================================

set -uo pipefail

# --- Config ---
DR_DIR="/home/gilles/scripts/dr"
WORK_DIR="/tmp/dr-backup-$(date +%Y%m%d-%H%M%S)"
AGE_KEY="/home/gilles/.config/age/dr-key.txt"
AGE_RECIPIENT="age1qjv3zzpvrx7zdwwym85hsv54uhr7kkdr2l4rlz7l96safc7ly5tqlrephv"
REPO_DIR="/home/gilles/vps-disaster-recovery"
BACKUP_NAME="vps-backup-$(date +%Y%m%d).tar.gz"
ENCRYPTED_NAME="${BACKUP_NAME}.age"
LOG="/tmp/dr-backup.log"
MAX_BACKUPS=30  # Rotation : garder 30 jours

# Telegram alerting
TELEGRAM_BOT="<TELEGRAM_BOT_TOKEN_JACQUES>"
TELEGRAM_CHAT="1801835052"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }
alert() {
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT}/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT" \
        -d text="$1" \
        -d parse_mode="Markdown" >/dev/null 2>&1 || true
}

cleanup() {
    rm -rf "$WORK_DIR" 2>/dev/null || true
}
trap cleanup EXIT

log "=== DR Backup started ==="

# --- Vérifications ---
if [ ! -f "$AGE_KEY" ]; then
    alert "🔴 *DR Backup FAILED* — Clé age introuvable : $AGE_KEY"
    exit 1
fi

mkdir -p "$WORK_DIR"/{configs,openclaw,workspaces,credentials,apache,systemd,scripts,databases,crontabs,websites,claude}

# =============================================================================
# 1. CONFIGS OPENCLAW (4 gateways — structure + configs, PAS les logs)
# =============================================================================
log "1/11 Configs OpenClaw..."

for profile in "" "-vlmedical" "-lucy" "-test"; do
    dir="/home/gilles/.openclaw${profile}"
    name="openclaw${profile:-"-mybotia"}"
    if [ -d "$dir" ]; then
        mkdir -p "$WORK_DIR/openclaw/$name"
        # Config principale (masquer les tokens inline serait trop risqué pour DR — on chiffre le tout)
        cp "$dir/openclaw.json" "$WORK_DIR/openclaw/$name/" 2>/dev/null || true
        # Docker compose si existe
        cp "$dir/docker/docker-compose.yml" "$WORK_DIR/openclaw/$name/" 2>/dev/null || true
        # Agents configs
        if [ -d "$dir/agents" ]; then
            cp -r "$dir/agents" "$WORK_DIR/openclaw/$name/" 2>/dev/null || true
        fi
    fi
done

# =============================================================================
# 2. WORKSPACES AGENTS (SOUL, IDENTITY, MEMORY, TOOLS — le cerveau des agents)
# =============================================================================
log "2/11 Workspaces agents..."

for ws in /home/gilles/.openclaw/workspace-*/; do
    [ -d "$ws" ] || continue
    agent=$(basename "$ws")
    mkdir -p "$WORK_DIR/workspaces/$agent"
    # Fichiers identité/mémoire (pas les fichiers tmp ou cache)
    for f in SOUL.md IDENTITY.md MEMORY.md AGENTS.md USER.md TOOLS.md HEARTBEAT.md CLAUDE.md; do
        cp "$ws/$f" "$WORK_DIR/workspaces/$agent/" 2>/dev/null || true
    done
    # Sous-dossier memory si existe
    if [ -d "$ws/memory" ]; then
        cp -r "$ws/memory" "$WORK_DIR/workspaces/$agent/" 2>/dev/null || true
    fi
    # Sous-dossier skills si existe
    if [ -d "$ws/skills" ]; then
        cp -r "$ws/skills" "$WORK_DIR/workspaces/$agent/" 2>/dev/null || true
    fi
done

# Workspace principal (Léa)
mkdir -p "$WORK_DIR/workspaces/main"
for f in /home/gilles/.openclaw/workspace/{SOUL.md,IDENTITY.md,MEMORY.md,AGENTS.md,USER.md,TOOLS.md,CLAUDE.md}; do
    cp "$f" "$WORK_DIR/workspaces/main/" 2>/dev/null || true
done
[ -d /home/gilles/.openclaw/workspace/memory ] && cp -r /home/gilles/.openclaw/workspace/memory "$WORK_DIR/workspaces/main/" 2>/dev/null || true
[ -d /home/gilles/.openclaw/workspace/skills ] && cp -r /home/gilles/.openclaw/workspace/skills "$WORK_DIR/workspaces/main/" 2>/dev/null || true
[ -d /home/gilles/.openclaw/workspace/procedures ] && cp -r /home/gilles/.openclaw/workspace/procedures "$WORK_DIR/workspaces/main/" 2>/dev/null || true

# =============================================================================
# 3. CREDENTIALS (WhatsApp, Telegram, OAuth, env files)
# =============================================================================
log "3/11 Credentials..."

# WhatsApp sessions (CRITIQUE — re-pairing physique sinon)
cp -r /home/gilles/.openclaw/credentials "$WORK_DIR/credentials/openclaw-creds" 2>/dev/null || true

# Env files
cp /home/gilles/apps/admin/.env "$WORK_DIR/credentials/admin.env" 2>/dev/null || true
cp /home/gilles/prospection/.env "$WORK_DIR/credentials/prospection.env" 2>/dev/null || true

# Claude credentials
cp /home/gilles/.claude/.credentials.json "$WORK_DIR/credentials/claude-credentials.json" 2>/dev/null || true

# Cloudflare (certbot)
sudo cp /etc/letsencrypt/cloudflare.ini "$WORK_DIR/credentials/cloudflare.ini" 2>/dev/null || true

# =============================================================================
# 4. APACHE VHOSTS (tous les fichiers de config)
# =============================================================================
log "4/11 Apache vhosts..."

sudo cp /etc/apache2/sites-available/*.conf "$WORK_DIR/apache/" 2>/dev/null || true
sudo cp /etc/apache2/sites-available/*.vhost "$WORK_DIR/apache/" 2>/dev/null || true
sudo cp /etc/apache2/conf-available/security.conf "$WORK_DIR/apache/security.conf" 2>/dev/null || true

# Liste des sites enabled (symlinks)
ls -la /etc/apache2/sites-enabled/ > "$WORK_DIR/apache/sites-enabled-list.txt" 2>/dev/null || true

# =============================================================================
# 5. SYSTEMD UNITS CUSTOM
# =============================================================================
log "5/11 Systemd units..."

for unit in openclaw-mybotia openclaw-vlmedical mybotia-admin artroyal-api meshcentral; do
    sudo cp "/etc/systemd/system/${unit}.service" "$WORK_DIR/systemd/" 2>/dev/null || true
done

# User units
cp /home/gilles/.config/systemd/user/*.service "$WORK_DIR/systemd/" 2>/dev/null || true

# =============================================================================
# 6. SCRIPTS MONITORING + WATCHDOG
# =============================================================================
log "6/11 Scripts monitoring + watchdog..."

cp -r /home/gilles/scripts/monitoring "$WORK_DIR/scripts/monitoring" 2>/dev/null || true
cp -r /home/gilles/watchdog "$WORK_DIR/scripts/watchdog" 2>/dev/null || true
# Exclure les logs du watchdog (trop gros, pas utile pour DR)
rm -rf "$WORK_DIR/scripts/watchdog/logs" 2>/dev/null || true

# Collaborateur template
cp -r /home/gilles/collaborateur-template "$WORK_DIR/scripts/collaborateur-template" 2>/dev/null || true

# =============================================================================
# 7. DATABASES (PG dump frais)
# =============================================================================
log "7/11 Database dumps..."

# PostgreSQL (mybotia_crm)
PGPASSWORD="<PG_PASSWORD>" pg_dump -h 127.0.0.1 -U prospection -d mybotia_crm \
    --no-owner --no-privileges 2>/dev/null | gzip > "$WORK_DIR/databases/mybotia_crm.sql.gz" || true

# Prospection DB (contacts, segments, etc.)
PGPASSWORD="<PG_PASSWORD>" pg_dump -h 127.0.0.1 -U prospection -d prospection \
    --no-owner --no-privileges 2>/dev/null | gzip > "$WORK_DIR/databases/prospection.sql.gz" || true

# Listmonk DB
PGPASSWORD="<PG_PASSWORD>" pg_dump -h 127.0.0.1 -U prospection -d listmonk \
    --no-owner --no-privileges 2>/dev/null | gzip > "$WORK_DIR/databases/listmonk.sql.gz" || true

# SQL migrations de référence
cp /home/gilles/prospection/sql/*.sql "$WORK_DIR/databases/" 2>/dev/null || true

# =============================================================================
# 8. CRONTABS
# =============================================================================
log "8/11 Crontabs..."

crontab -l > "$WORK_DIR/crontabs/gilles.crontab" 2>/dev/null || true
sudo crontab -l > "$WORK_DIR/crontabs/root.crontab" 2>/dev/null || true

# =============================================================================
# 9. WEBSITES (webchat, bullsage, landing pages)
# =============================================================================
log "9/11 Websites..."

# Webchat mybotia (petit, critique)
cp -r /var/www/html/mybotia "$WORK_DIR/websites/mybotia" 2>/dev/null || true
# Bullsage
cp -r /var/www/html/bullsagetrader "$WORK_DIR/websites/bullsagetrader" 2>/dev/null || true

# =============================================================================
# 10. SSH + SECURITY CONFIG
# =============================================================================
log "10/11 SSH + Security..."

mkdir -p "$WORK_DIR/configs/security"
cp /home/gilles/.ssh/authorized_keys "$WORK_DIR/configs/security/authorized_keys" 2>/dev/null || true
sudo cp /etc/ssh/sshd_config.d/custom.conf "$WORK_DIR/configs/security/sshd-custom.conf" 2>/dev/null || true
sudo cp /etc/fail2ban/jail.local "$WORK_DIR/configs/security/fail2ban-jail.local" 2>/dev/null || true
sudo ufw status verbose > "$WORK_DIR/configs/security/ufw-rules.txt" 2>/dev/null || true

# Nginx
sudo cp /etc/nginx/sites-available/* "$WORK_DIR/configs/" 2>/dev/null || true

# =============================================================================
# 11. CLAUDE CODE MEMORY (Jacques)
# =============================================================================
log "11/11 Claude Code memory..."

cp -r /home/gilles/.claude/projects/-home-gilles/memory "$WORK_DIR/claude/memory" 2>/dev/null || true
cp /home/gilles/CLAUDE.md "$WORK_DIR/claude/CLAUDE.md" 2>/dev/null || true

# =============================================================================
# INVENTAIRE SYSTÈME (snapshot texte)
# =============================================================================
log "Generating system inventory..."

cat > "$WORK_DIR/INVENTORY.txt" << 'INVEOF'
# VPS Disaster Recovery — System Inventory
INVEOF

{
    echo "=== GENERATED: $(date -Iseconds) ==="
    echo ""
    echo "=== OS ==="
    cat /etc/os-release
    echo ""
    echo "=== HARDWARE ==="
    free -h
    df -h
    echo ""
    echo "=== PACKAGES (dpkg) ==="
    dpkg -l | grep '^ii' | awk '{print $2, $3}'
    echo ""
    echo "=== NPM GLOBAL ==="
    npm list -g --depth=0 2>/dev/null
    echo ""
    echo "=== PIP ==="
    pip3 list 2>/dev/null
    echo ""
    echo "=== SYSTEMD ENABLED ==="
    systemctl list-unit-files --state=enabled --no-pager
    echo ""
    echo "=== DOCKER ==="
    docker ps -a 2>/dev/null
    docker images 2>/dev/null
    echo ""
    echo "=== LISTENING PORTS ==="
    ss -tlnp
    echo ""
    echo "=== UFW ==="
    sudo ufw status verbose
} >> "$WORK_DIR/INVENTORY.txt" 2>/dev/null

# =============================================================================
# COMPRESSION + CHIFFREMENT
# =============================================================================
log "Compressing..."

cd /tmp
tar czf "$BACKUP_NAME" -C "$WORK_DIR" . 2>/dev/null

BACKUP_SIZE=$(du -sh "$BACKUP_NAME" | awk '{print $1}')
log "Archive: $BACKUP_SIZE"

log "Encrypting with age..."
age -r "$AGE_RECIPIENT" -o "$ENCRYPTED_NAME" "$BACKUP_NAME"
rm -f "$BACKUP_NAME"

ENCRYPTED_SIZE=$(du -sh "$ENCRYPTED_NAME" | awk '{print $1}')
log "Encrypted: $ENCRYPTED_SIZE"

# =============================================================================
# PUSH VERS GITHUB
# =============================================================================
log "Pushing to GitHub..."

if [ -d "$REPO_DIR/.git" ]; then
    # Rotation : supprimer les vieux backups
    find "$REPO_DIR/backups/" -name "vps-backup-*.age" -mtime +$MAX_BACKUPS -delete 2>/dev/null || true

    mkdir -p "$REPO_DIR/backups"
    mv "/tmp/$ENCRYPTED_NAME" "$REPO_DIR/backups/"

    cd "$REPO_DIR"
    git add backups/
    git commit -m "DR backup $(date +%Y-%m-%d) — ${ENCRYPTED_SIZE}" 2>/dev/null || true
    git push origin main 2>/dev/null || git push origin master 2>/dev/null || {
        log "ERROR: git push failed"
        alert "🔴 *DR Backup* — git push failed"
        exit 1
    }

    log "Pushed to GitHub OK"
    alert "✅ *DR Backup OK* — $(date +%Y-%m-%d) — $ENCRYPTED_SIZE chiffré"
else
    # Repo pas encore init — stocker localement
    mkdir -p /home/gilles/backups/dr
    mv "/tmp/$ENCRYPTED_NAME" /home/gilles/backups/dr/
    log "Stored locally (repo not initialized yet): /home/gilles/backups/dr/$ENCRYPTED_NAME"
    alert "⚠️ *DR Backup* — Sauvé localement ($ENCRYPTED_SIZE). Repo GitHub pas encore configuré."
fi

log "=== DR Backup completed ==="
