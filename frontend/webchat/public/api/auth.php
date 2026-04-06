<?php
// API: Hybrid authentication (email/password + token)
// POST /api/auth.php  -> login via {email, password} or {token}
// GET  /api/auth.php  -> check session -> returns client info or 401
// DELETE /api/auth.php -> logout

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

require_once dirname(dirname(dirname(__FILE__))) . '/private/config.inc.php';
require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';
require_once dirname(dirname(dirname(__FILE__))) . '/private/env.php';

ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1);
ini_set('session.cookie_samesite', 'Strict');
ini_set('session.use_strict_mode', 1);
session_name('mybotia_sid');
session_start();

$method = $_SERVER['REQUEST_METHOD'];

// --- POST: Login ---
if ($method === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);

    // --- Path A: Email + Password ---
    if (!empty($body['email']) && !empty($body['password'])) {
        $subdomain = $body['subdomain'] ?? '';

        $client = verifyClientPassword($body['email'], $body['password']);
        if (!$client) {
            http_response_code(403);
            echo json_encode(['error' => 'Email ou mot de passe incorrect']);
            exit;
        }

        $collaborateurs = getClientCollaborateurs($client['id']);
        if (empty($collaborateurs)) {
            http_response_code(403);
            echo json_encode(['error' => 'Aucun Collaborateur IA configuré pour ce compte']);
            exit;
        }

        // Pick the right collaborateur: by subdomain, or default, or first
        $active = null;
        if ($subdomain) {
            foreach ($collaborateurs as $c) {
                if ($c['subdomain'] === $subdomain) { $active = $c; break; }
            }
            // Subdomain specified but no matching collaborateur -> reject
            if (!$active) {
                http_response_code(403);
                echo json_encode(['error' => 'Acces refuse pour ce sous-domaine. Verifiez vos identifiants.']);
                exit;
            }
        } else {
            // No subdomain: use default or first
            foreach ($collaborateurs as $c) {
                if ($c['is_default']) { $active = $c; break; }
            }
            if (!$active) $active = $collaborateurs[0];
        }

        // Get usage
        $usage = getMonthlyUsage($client['id']);

        // Build session
        session_regenerate_id(true);
        $_SESSION['client_id'] = $client['id'];
        $_SESSION['client_email'] = $client['email'];
        $_SESSION['company_name'] = $client['company_name'];
        $_SESSION['contact_name'] = $client['contact_name'];
        $_SESSION['plan'] = $client['plan'];
        $_SESSION['max_tokens'] = $client['max_tokens_month'];
        $_SESSION['is_admin'] = $client['is_admin'];
        $_SESSION['active_subdomain'] = $active['subdomain'];
        $_SESSION['gateway_token'] = $active['gateway_token'];
        $_SESSION['session_key'] = $active['session_key'] ?: ('agent:' . $active['subdomain'] . ':main');
        $_SESSION['login_time'] = time();
        $_SESSION['auth_type'] = 'email';
        $csrfToken = generateCsrfToken();

        // Format collaborateurs for frontend
        $collabList = [];
        foreach ($collaborateurs as $c) {
            $collabList[] = [
                'subdomain' => $c['subdomain'],
                'name' => $c['display_name'],
                'role' => $c['display_role'],
                'is_default' => (bool)$c['is_default']
            ];
        }

        echo json_encode([
            'ok' => true,
            'auth_type' => 'email',
            'client' => [
                'id' => $client['id'],
                'company_name' => $client['company_name'],
                'contact_name' => $client['contact_name'],
                'plan' => $client['plan'],
                'max_tokens' => $client['max_tokens_month'],
                'is_admin' => (bool)$client['is_admin']
            ],
            'collaborateurs' => $collabList,
            'active_collaborateur' => $active['subdomain'],
            'session_key' => $active['session_key'] ?: ($active['subdomain'] ? 'agent:' . $active['subdomain'] . ':main' : 'main'),
            'usage' => [
                'tokens_used' => (int)$usage['tokens_used'],
                'tokens_max' => $client['max_tokens_month'],
                'messages_sent' => (int)$usage['messages_sent'],
                'messages_received' => (int)$usage['messages_received'],
                'percentage' => $client['max_tokens_month'] > 0 ? round(($usage['tokens_used'] / $client['max_tokens_month']) * 100, 1) : 0
            ],
            'csrf_token' => $csrfToken
        ]);
        exit;
    }

    // --- Path B: Token (legacy, for admin/Gilles) ---
    $token = $body['token'] ?? '';
    if (!$token) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing email/password or token']);
        exit;
    }

    $agentInfo = validateToken($token);
    if (!$agentInfo) {
        http_response_code(403);
        echo json_encode(['error' => 'Invalid token']);
        exit;
    }

    $user = getOrCreateUser($token, $agentInfo['displayName'] ?? '', $agentInfo['name'] ?? '');
    if (!$user) {
        http_response_code(500);
        echo json_encode(['error' => 'Database error']);
        exit;
    }

    session_regenerate_id(true);
    $_SESSION['user_id'] = $user['id'];
    $_SESSION['user_name'] = $user['name'];
    $_SESSION['agent'] = $user['agent'];
    $_SESSION['token_hash'] = hash('sha256', $token);
    $_SESSION['login_time'] = time();
    $_SESSION['auth_type'] = 'token';

    echo json_encode([
        'ok' => true,
        'auth_type' => 'token',
        'user' => [
            'id' => $user['id'],
            'name' => $user['name'],
            'agent' => $user['agent'],
            'avatar' => $user['avatar'] ?? null
        ],
        'session_id' => session_id()
    ]);
    exit;
}

// --- GET: Check session ---
if ($method === 'GET') {
    // Client session (email auth)
    if (isset($_SESSION['client_id'])) {
        $client = getClientById($_SESSION['client_id']);
        if (!$client) {
            session_destroy();
            http_response_code(401);
            echo json_encode(['error' => 'Client not found']);
            exit;
        }
        $collaborateurs = getClientCollaborateurs($client['id']);
        $usage = getMonthlyUsage($client['id']);

        $collabList = [];
        foreach ($collaborateurs as $c) {
            $collabList[] = [
                'subdomain' => $c['subdomain'],
                'name' => $c['display_name'],
                'role' => $c['display_role'],
                'is_default' => (bool)$c['is_default']
            ];
        }

        // Find active collaborateur's token
        $activeToken = $_SESSION['gateway_token'] ?? '';
        $activeSub = $_SESSION['active_subdomain'] ?? '';

        echo json_encode([
            'ok' => true,
            'auth_type' => 'email',
            'client' => [
                'id' => $client['id'],
                'company_name' => $client['company_name'],
                'contact_name' => $client['contact_name'],
                'plan' => $client['plan'],
                'max_tokens' => $client['max_tokens_month'],
                'is_admin' => (bool)$client['is_admin']
            ],
            'collaborateurs' => $collabList,
            'active_collaborateur' => $activeSub,
            'session_key' => $_SESSION['session_key'] ?? ($activeSub ? 'agent:' . $activeSub . ':main' : 'main'),
            'usage' => [
                'tokens_used' => (int)$usage['tokens_used'],
                'tokens_max' => $client['max_tokens_month'],
                'messages_sent' => (int)$usage['messages_sent'],
                'messages_received' => (int)$usage['messages_received'],
                'percentage' => $client['max_tokens_month'] > 0 ? round(($usage['tokens_used'] / $client['max_tokens_month']) * 100, 1) : 0
            ],
            'csrf_token' => generateCsrfToken()
        ]);
        exit;
    }

    // Legacy user session (token auth)
    if (isset($_SESSION['user_id'])) {
        $db = getDB();
        $stmt = $db->prepare("SELECT id, name, agent, avatar FROM users WHERE id = :id");
        $stmt->bindValue(':id', $_SESSION['user_id'], SQLITE3_INTEGER);
        $result = $stmt->execute();
        $user = $result->fetchArray(SQLITE3_ASSOC);

        if (!$user) {
            session_destroy();
            http_response_code(401);
            echo json_encode(['error' => 'User not found']);
            exit;
        }

        echo json_encode([
            'ok' => true,
            'auth_type' => 'token',
            'user' => [
                'id' => $user['id'],
                'name' => $user['name'],
                'agent' => $user['agent'],
                'avatar' => $user['avatar']
            ],
            'token_hash' => $_SESSION['token_hash'] ?? null
        ]);
        exit;
    }

    http_response_code(401);
    echo json_encode(['error' => 'Not authenticated']);
    exit;
}

// --- PATCH: Switch collaborateur ---
if ($method === 'PATCH') {
    if (!isset($_SESSION['client_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Not authenticated']);
        exit;
    }
    $body = json_decode(file_get_contents('php://input'), true);
    $newSub = $body['subdomain'] ?? '';
    if (!$newSub) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing subdomain']);
        exit;
    }
    $collab = getClientCollaborateurBySubdomain($_SESSION['client_id'], $newSub);
    if (!$collab) {
        http_response_code(404);
        echo json_encode(['error' => 'Collaborateur non trouvé']);
        exit;
    }
    $_SESSION['active_subdomain'] = $collab['subdomain'];
    $_SESSION['gateway_token'] = $collab['gateway_token'];
    $_SESSION['session_key'] = $collab['session_key'] ?: ('agent:' . $collab['subdomain'] . ':main');

    echo json_encode([
        'ok' => true,
        'active_collaborateur' => $collab['subdomain'],
        'session_key' => $collab['session_key'] ?: ('agent:' . $collab['subdomain'] . ':main'),
        'name' => $collab['display_name'],
        'role' => $collab['display_role']
    ]);
    exit;
}

// --- DELETE: Logout ---
if ($method === 'DELETE') {
    $_SESSION = [];
    if (ini_get("session.use_cookies")) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000,
            $params["path"], $params["domain"],
            $params["secure"], $params["httponly"]
        );
    }
    session_destroy();
    echo json_encode(['ok' => true, 'message' => 'Logged out']);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
