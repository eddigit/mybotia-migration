<?php
header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');
// Allow all *.mybotia.com subdomains
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin && preg_match('/^https:\/\/([a-z0-9-]+\.)?mybotia\.com$/', $origin)) {
    header('Access-Control-Allow-Origin: ' . $origin);
} else {
    header('Access-Control-Allow-Origin: https://app.mybotia.com');
}

require_once dirname(dirname(__FILE__)) . '/private/config.inc.php';

$method = $_SERVER['REQUEST_METHOD'];

// Mode 1: validate token
$token = $_GET['t'] ?? '';
if ($token) {
    $info = validateToken($token);
    if (!$info) {
        http_response_code(403);
        echo json_encode(['error' => 'Invalid token']);
        exit;
    }
    echo json_encode($info);
    exit;
}

// Mode 2: get subdomain agent config (for auto-connect)
$sub = $_GET['sub'] ?? '';
if ($sub) {
    $agent = getAgentBySubdomain($sub);
    if (!$agent) {
        http_response_code(404);
        echo json_encode(['error' => 'Agent not found']);
        exit;
    }
    echo json_encode($agent);
    exit;
}

http_response_code(400);
echo json_encode(['error' => 'Missing parameters']);
?>