<?php
// API: Voice configuration for the active collaborateur
// GET /api/voice-config.php → returns voice-specific agent config
// Requires authenticated mybotia_sid session

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

require_once dirname(dirname(dirname(__FILE__))) . '/private/config.inc.php';
require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';

ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1);
ini_set('session.cookie_samesite', 'Strict');
session_name('mybotia_sid');
session_start();

// Race condition fix: if session appears empty but cookie exists,
// close and re-read to pick up data written by a concurrent request
if (empty($_SESSION['client_id']) && isset($_COOKIE['mybotia_sid'])) {
    session_write_close();
    usleep(100000); // 100ms
    session_start();
}

// Must have an authenticated email session
if (empty($_SESSION['client_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Not authenticated']);
    exit;
}

// Check session expiration (24h)
$loginTime = $_SESSION['login_time'] ?? 0;
if (time() - $loginTime > 86400) {
    session_destroy();
    http_response_code(401);
    echo json_encode(['error' => 'Session expired']);
    exit;
}

$activeSub = $_SESSION['active_subdomain'] ?? '';
if (!$activeSub) {
    http_response_code(400);
    echo json_encode(['error' => 'No active collaborateur']);
    exit;
}

// Get collaborateur from DB
$collab = getClientCollaborateurBySubdomain($_SESSION['client_id'], $activeSub);
if (!$collab) {
    http_response_code(404);
    echo json_encode(['error' => 'Collaborateur not found']);
    exit;
}

// Get agent info from agents.json (avatar, name, role)
$agentInfo = getAgentBySubdomain($activeSub);

// Parse voice_config JSON from DB (or use defaults)
$voiceConfig = [];
if (!empty($collab['voice_config'])) {
    $voiceConfig = json_decode($collab['voice_config'], true) ?: [];
}

// Build response with defaults
$defaults = [
    'voice' => 'fr-FR-VivienneMultilingualNeural',
    'voiceRate' => '-4%',
    'voicePitch' => '-2Hz',
    'wakeWord' => strtolower($agentInfo['displayName'] ?? $collab['display_name'] ?? 'assistant'),
    'systemPrompt' => ''
];

$voice = array_merge($defaults, $voiceConfig);

// Check if voice is enabled for this collaborateur
$voiceEnabled = isset($voiceConfig['enabled']) ? (bool)$voiceConfig['enabled'] : true;

if (!$voiceEnabled) {
    http_response_code(403);
    echo json_encode(['error' => 'Voice not enabled for this collaborateur']);
    exit;
}

echo json_encode([
    'ok' => true,
    'agent' => [
        'id' => $collab['subdomain'],
        'agentId' => $agentInfo['agentId'] ?? $collab['agent_id'] ?? 'main',
        'name' => $agentInfo['displayName'] ?? $collab['display_name'],
        'role' => $agentInfo['role'] ?? $collab['display_role'],
        'avatar' => $agentInfo['avatar'] ?? '',
        'voice' => $voice['voice'],
        'voiceRate' => $voice['voiceRate'],
        'voicePitch' => $voice['voicePitch'],
        'wakeWord' => $voice['wakeWord'],
        'systemPrompt' => $voice['systemPrompt']
    ],
    'gateway' => [
        'token' => $collab['gateway_token'],
        'agentId' => $agentInfo['agentId'] ?? $collab['agent_id'] ?? 'main',
        'port' => (int)($collab['gateway_port'] ?? 18789)
    ],
    'user' => [
        'name' => $_SESSION['contact_name'] ?? '',
        'email' => $_SESSION['client_email'] ?? ''
    ]
]);
