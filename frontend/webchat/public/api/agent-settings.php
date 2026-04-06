<?php
/**
 * API Agent Settings — Collaborateur Pro
 * GET  /api/agent-settings.php?sub=lea       → Retourne la config de l'agent
 * POST /api/agent-settings.php               → Met a jour les settings (avatar, role, etc.)
 *   Body JSON: { "subdomain": "lea", "avatar": "https://..." }
 *
 * Securite : seuls les admins (auth par token) ou les sessions email auth peuvent modifier.
 */

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

require_once dirname(dirname(dirname(__FILE__))) . '/private/config.inc.php';

// Charger les agents
$agentsFile = dirname(dirname(dirname(__FILE__))) . '/private/agents.json';

function loadAgents() {
    global $agentsFile;
    if (!file_exists($agentsFile)) {
        return null;
    }
    $content = file_get_contents($agentsFile);
    return json_decode($content, true);
}

function saveAgents($agents) {
    global $agentsFile;
    // Backup avant ecriture
    $backupFile = $agentsFile . '.bak-' . date('Ymd-His');
    copy($agentsFile, $backupFile);

    $json = json_encode($agents, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    return file_put_contents($agentsFile, $json) !== false;
}

$method = $_SERVER['REQUEST_METHOD'];

// --- GET : Retourner la config d'un agent ---
if ($method === 'GET') {
    $sub = $_GET['sub'] ?? '';
    if (!$sub) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'Parametre "sub" requis']);
        exit;
    }

    $agents = loadAgents();
    if (!$agents || !isset($agents[$sub])) {
        http_response_code(404);
        echo json_encode(['ok' => false, 'error' => 'Agent non trouve']);
        exit;
    }

    $agent = $agents[$sub];
    echo json_encode([
        'ok' => true,
        'agent' => [
            'subdomain' => $sub,
            'name' => $agent['name'] ?? $sub,
            'role' => $agent['role'] ?? '',
            'avatar' => $agent['avatar'] ?? '',
            'cards' => $agent['cards'] ?? []
        ]
    ]);
    exit;
}

// --- POST : Mettre a jour la config d'un agent ---
if ($method === 'POST') {
    // Verifier l'authentification (session PHP ou token admin)
    session_start();
    $isAuth = false;

    // 1. Session email (client connecte)
    if (isset($_SESSION['client_id']) && isset($_SESSION['is_admin']) && $_SESSION['is_admin']) {
        $isAuth = true;
    }

    // 2. Token admin dans le header Authorization
    $authHeader = $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['HTTP_X_AUTH_TOKEN'] ?? '';
    if (!$isAuth && $authHeader) {
        $token = str_replace('Bearer ', '', $authHeader);
        // Verifier si c'est un token admin connu
        $agents = loadAgents();
        if ($agents) {
            foreach ($agents as $agentData) {
                if (isset($agentData['token']) && $agentData['token'] === $token) {
                    $isAuth = true;
                    break;
                }
            }
        }
    }

    // 3. Token dans le body
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$isAuth && $input && isset($input['admin_token'])) {
        $agents = loadAgents();
        if ($agents) {
            foreach ($agents as $agentData) {
                if (isset($agentData['token']) && $agentData['token'] === $input['admin_token']) {
                    $isAuth = true;
                    break;
                }
            }
        }
    }

    if (!$isAuth) {
        http_response_code(403);
        echo json_encode(['ok' => false, 'error' => 'Non autorise']);
        exit;
    }

    if (!$input || !isset($input['subdomain'])) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'Champs requis: subdomain']);
        exit;
    }

    $sub = $input['subdomain'];
    $agents = loadAgents();

    if (!$agents || !isset($agents[$sub])) {
        http_response_code(404);
        echo json_encode(['ok' => false, 'error' => 'Agent non trouve: ' . $sub]);
        exit;
    }

    // Mettre a jour les champs autorises
    $updated = [];

    if (isset($input['avatar'])) {
        $avatarUrl = trim($input['avatar']);
        // Validation basique de l'URL
        if ($avatarUrl !== '' && !filter_var($avatarUrl, FILTER_VALIDATE_URL)) {
            http_response_code(400);
            echo json_encode(['ok' => false, 'error' => 'URL avatar invalide']);
            exit;
        }
        $agents[$sub]['avatar'] = $avatarUrl;
        $updated[] = 'avatar';
    }

    if (isset($input['role'])) {
        $agents[$sub]['role'] = trim($input['role']);
        $updated[] = 'role';
    }

    if (isset($input['name'])) {
        $agents[$sub]['name'] = trim($input['name']);
        $updated[] = 'name';
    }

    if (empty($updated)) {
        echo json_encode(['ok' => true, 'message' => 'Rien a modifier']);
        exit;
    }

    // Sauvegarder
    if (saveAgents($agents)) {
        echo json_encode([
            'ok' => true,
            'message' => 'Mis a jour: ' . implode(', ', $updated),
            'agent' => [
                'subdomain' => $sub,
                'name' => $agents[$sub]['name'] ?? $sub,
                'role' => $agents[$sub]['role'] ?? '',
                'avatar' => $agents[$sub]['avatar'] ?? ''
            ]
        ]);
    } else {
        http_response_code(500);
        echo json_encode(['ok' => false, 'error' => 'Erreur ecriture fichier']);
    }
    exit;
}

// --- OPTIONS (CORS) ---
if ($method === 'OPTIONS') {
    header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Auth-Token');
    http_response_code(200);
    exit;
}

http_response_code(405);
echo json_encode(['ok' => false, 'error' => 'Methode non supportee']);
?>
