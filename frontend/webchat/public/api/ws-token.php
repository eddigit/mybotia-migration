<?php
// API: Serve gateway token only to authenticated PHP sessions
// GET /api/ws-token.php → {token, role, scope, agent_id, expires}
// The real gateway token never leaves server-side except through this endpoint,
// which requires a valid mybotia_sid session cookie.

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1);
ini_set('session.cookie_samesite', 'Strict');
session_name('mybotia_sid');
session_start();

// Must have an authenticated email session with a gateway token
if (empty($_SESSION['client_id']) || empty($_SESSION['gateway_token'])) {
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

// Determine role and scope
$isAdmin = !empty($_SESSION['is_admin']);
$role = $isAdmin ? 'admin' : 'collaborator';
$activeSub = $_SESSION['active_subdomain'] ?? 'main';
$scope = $isAdmin ? '*' : ('agent:' . $activeSub);

echo json_encode([
    'token' => $_SESSION['gateway_token'],
    'role' => $role,
    'scope' => $scope,
    'agent_id' => $activeSub,
    'expires' => $loginTime + 86400
]);
