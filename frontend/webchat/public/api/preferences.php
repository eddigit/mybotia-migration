<?php
// API: User preferences (folders, theme, settings)
// GET /api/preferences.php?t=TOKEN  -> get all preferences
// POST /api/preferences.php?t=TOKEN -> save preferences (JSON body: {key: value, ...})

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin && preg_match('/^https:\/\/([a-z0-9-]+\.)?mybotia\.com$/', $origin)) {
    header('Access-Control-Allow-Origin: ' . $origin);
} else {
    header('Access-Control-Allow-Origin: https://app.mybotia.com');
}
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Gateway-Token');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

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

// Get or create user
$user = getOrCreateUser($token, $agentInfo['displayName'] ?? '', $agentInfo['name'] ?? '');
if (!$user) {
    http_response_code(500);
    echo json_encode(['error' => 'Database error']);
    exit;
}

// GET: return all preferences
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $prefs = getUserPreferences($user['id']);
    echo json_encode([
        'ok' => true,
        'user' => [
            'name' => $user['name'],
            'agent' => $user['agent'],
            'created_at' => $user['created_at']
        ],
        'preferences' => $prefs
    ]);
    exit;
}

// POST: save preferences
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);
    if (!$body || !is_array($body)) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON body']);
        exit;
    }
    
    $saved = [];
    foreach ($body as $key => $value) {
        // Whitelist allowed preference keys
        $allowedKeys = ['folders', 'theme', 'sidebar_width', 'font_size', 'notifications', 'notes', 'session_renames', 'pinned'];
        if (!in_array($key, $allowedKeys)) continue;
        
        setUserPreference($user['id'], $key, $value);
        $saved[] = $key;
    }
    
    echo json_encode(['ok' => true, 'saved' => $saved]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
?>
