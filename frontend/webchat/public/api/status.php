<?php
// API: System status for authenticated users
// GET /api/status.php?t=TOKEN -> returns status of all services

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

require_once dirname(dirname(dirname(__FILE__))) . '/private/config.inc.php';
require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';

// Validate token (header preferred, GET fallback for backwards compat)
$token = $_SERVER['HTTP_X_GATEWAY_TOKEN'] ?? $_GET['t'] ?? '';
if (!$token) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing token']);
    exit;
}

$agentInfo = validateToken($token);
if (!$agentInfo) {
    http_response_code(403);
    echo json_encode(['error' => 'Invalid token']);
    exit;
}

$services = [];

// 1. Database status
try {
    $db = getDB();
    $testWrite = $db->exec("CREATE TABLE IF NOT EXISTS _health_check (id INTEGER PRIMARY KEY)");
    $testRead = $db->querySingle("SELECT COUNT(*) FROM users");
    $dbSize = file_exists(DB_PATH) ? round(filesize(DB_PATH) / 1024, 1) : 0;
    $services['database'] = [
        'status' => 'ok',
        'label' => 'Base de données',
        'detail' => $testRead . ' utilisateur(s), ' . $dbSize . ' Ko',
        'writable' => $testWrite ? true : false
    ];
} catch (Exception $e) {
    $services['database'] = [
        'status' => 'error',
        'label' => 'Base de données',
        'detail' => 'Erreur : ' . $e->getMessage(),
        'writable' => false
    ];
}

// 2. Gateway WebSocket status (check if port 18789 is listening)
$gwSocket = @fsockopen('127.0.0.1', 18789, $errno, $errstr, 2);
if ($gwSocket) {
    fclose($gwSocket);
    $services['gateway'] = [
        'status' => 'ok',
        'label' => 'Serveur temps réel',
        'detail' => 'Port 18789 actif'
    ];
} else {
    $services['gateway'] = [
        'status' => 'error',
        'label' => 'Serveur temps réel',
        'detail' => 'Injoignable'
    ];
}

// 3. PHP Runtime
$services['php'] = [
    'status' => 'ok',
    'label' => 'Moteur PHP',
    'detail' => 'PHP ' . PHP_VERSION
];

// 4. Agent config
$agentName = $agentInfo['displayName'] ?? $agentInfo['name'] ?? 'Inconnu';
$agentId = $agentInfo['agentId'] ?? '';
$services['agent'] = [
    'status' => 'ok',
    'label' => 'Agent IA',
    'detail' => $agentName . ($agentId ? ' (' . $agentId . ')' : '')
];

// 5. SSL Certificate check (for the current domain)
$host = $_SERVER['HTTP_HOST'] ?? 'mybotia.com';
$sslContext = @stream_context_create(["ssl" => ["capture_peer_cert" => true, "verify_peer" => false]]);
$sslClient = @stream_socket_client("ssl://{$host}:443", $errno, $errstr, 3, STREAM_CLIENT_CONNECT, $sslContext);
if ($sslClient) {
    $params = stream_context_get_params($sslClient);
    $cert = openssl_x509_parse($params['options']['ssl']['peer_certificate']);
    fclose($sslClient);
    if ($cert) {
        $expiresAt = $cert['validTo_time_t'] ?? 0;
        $daysLeft = max(0, round(($expiresAt - time()) / 86400));
        $services['ssl'] = [
            'status' => $daysLeft > 14 ? 'ok' : ($daysLeft > 3 ? 'warning' : 'error'),
            'label' => 'Certificat SSL',
            'detail' => $daysLeft . ' jours restants'
        ];
    } else {
        $services['ssl'] = ['status' => 'warning', 'label' => 'Certificat SSL', 'detail' => 'Non vérifiable'];
    }
} else {
    $services['ssl'] = ['status' => 'warning', 'label' => 'Certificat SSL', 'detail' => 'Non vérifiable'];
}

// 6. Disk space
$diskFree = round(disk_free_space('/') / 1024 / 1024 / 1024, 1);
$diskTotal = round(disk_total_space('/') / 1024 / 1024 / 1024, 1);
$diskPct = round(($diskTotal - $diskFree) / $diskTotal * 100);
$services['disk'] = [
    'status' => $diskPct < 85 ? 'ok' : ($diskPct < 95 ? 'warning' : 'error'),
    'label' => 'Espace disque',
    'detail' => $diskFree . ' Go libres / ' . $diskTotal . ' Go (' . $diskPct . '% utilisé)'
];

// 7. WhatsApp - check if any WA sessions exist in recent history
try {
    $db2 = getDB();
    $user = getUserByToken($token);
    if ($user) {
        $prefs = getUserPreferences($user['id']);
        $hasFolders = !empty($prefs['folders']);
        $services['preferences'] = [
            'status' => 'ok',
            'label' => 'Préférences utilisateur',
            'detail' => $hasFolders ? 'Synchronisées' : 'Par défaut'
        ];
    }
} catch (Exception $e) {
    $services['preferences'] = [
        'status' => 'warning',
        'label' => 'Préférences utilisateur',
        'detail' => 'Non disponible'
    ];
}

// Overall status
$allOk = true;
$hasWarning = false;
foreach ($services as $s) {
    if ($s['status'] === 'error') $allOk = false;
    if ($s['status'] === 'warning') $hasWarning = true;
}

echo json_encode([
    'ok' => true,
    'overall' => $allOk ? ($hasWarning ? 'warning' : 'ok') : 'error',
    'timestamp' => date('c'),
    'services' => $services
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
