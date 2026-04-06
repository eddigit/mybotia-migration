<?php
// Health check endpoint — restricted to localhost and private IPs
header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

// Restrict access to localhost / private networks
$remoteIp = $_SERVER['REMOTE_ADDR'] ?? '';
$allowed = in_array($remoteIp, ['127.0.0.1', '::1']) || 
           filter_var($remoteIp, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) === false;

if (!$allowed) {
    http_response_code(403);
    echo json_encode(['error' => 'Access denied']);
    exit;
}

require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';

$db = getDB();

// Gather stats
$usersCount = $db->querySingle("SELECT COUNT(*) FROM users");
$prefsCount = $db->querySingle("SELECT COUNT(*) FROM user_preferences");
$lastSeen = $db->querySingle("SELECT MAX(last_seen) FROM users");
$activeToday = $db->querySingle("SELECT COUNT(*) FROM users WHERE last_seen >= date('now', '-1 day')");
$dbSize = file_exists(DB_PATH) ? round(filesize(DB_PATH) / 1024, 1) : 0;

// Check PHP sessions directory
$sessPath = session_save_path() ?: sys_get_temp_dir();
$sessCount = 0;
if (is_dir($sessPath)) {
    $sessCount = count(glob($sessPath . '/sess_*'));
}

// Disk usage
$diskFree = round(disk_free_space('/') / 1024 / 1024 / 1024, 2);
$diskTotal = round(disk_total_space('/') / 1024 / 1024 / 1024, 2);

// Error log tail
$errorLog = '/var/log/apache2/wildcard-mybotia-error.log';
$recentErrors = [];
if (file_exists($errorLog) && is_readable($errorLog)) {
    $lines = array_slice(file($errorLog, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES), -5);
    $recentErrors = $lines;
}

echo json_encode([
    'status' => 'ok',
    'timestamp' => date('c'),
    'stats' => [
        'users_total' => (int)$usersCount,
        'users_active_24h' => (int)$activeToday,
        'preferences' => (int)$prefsCount,
        'last_activity' => $lastSeen,
        'php_sessions' => $sessCount,
        'db_size_kb' => $dbSize,
        'disk_free_gb' => $diskFree,
        'disk_total_gb' => $diskTotal
    ],
    'php_version' => PHP_VERSION,
    'sqlite_version' => SQLite3::version()['versionString'],
    'recent_errors' => $recentErrors
], JSON_PRETTY_PRINT);
