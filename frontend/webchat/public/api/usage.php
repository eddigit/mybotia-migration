<?php
// API: Usage tracking (token estimation)
// POST /api/usage.php  -> log usage {collaborateur, direction, char_count}
// GET  /api/usage.php  -> get monthly usage for current client

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';

ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1);
ini_set('session.cookie_samesite', 'Strict');
ini_set('session.use_strict_mode', 1);
session_name('mybotia_sid');
session_start();

// Must be logged in as client (email auth)
if (!isset($_SESSION['client_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Not authenticated']);
    exit;
}

$clientId = $_SESSION['client_id'];
$method = $_SERVER['REQUEST_METHOD'];

// --- POST: Log usage ---
if ($method === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);
    $collaborateur = $body['collaborateur'] ?? ($_SESSION['active_subdomain'] ?? '');
    $direction = $body['direction'] ?? '';
    $charCount = intval($body['char_count'] ?? 0);

    if (!in_array($direction, ['sent', 'received'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid direction (sent or received)']);
        exit;
    }
    if ($charCount <= 0) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid char_count']);
        exit;
    }

    logUsage($clientId, $collaborateur, $direction, $charCount);

    // Return updated usage
    $usage = getMonthlyUsage($clientId);
    $maxTokens = $_SESSION['max_tokens'] ?? 500000;

    echo json_encode([
        'ok' => true,
        'usage' => [
            'tokens_used' => (int)$usage['tokens_used'],
            'tokens_max' => $maxTokens,
            'messages_sent' => (int)$usage['messages_sent'],
            'messages_received' => (int)$usage['messages_received'],
            'percentage' => $maxTokens > 0 ? round(($usage['tokens_used'] / $maxTokens) * 100, 1) : 0
        ]
    ]);
    exit;
}

// --- GET: Get monthly usage ---
if ($method === 'GET') {
    $usage = getMonthlyUsage($clientId);
    $maxTokens = $_SESSION['max_tokens'] ?? 500000;

    echo json_encode([
        'ok' => true,
        'usage' => [
            'tokens_used' => (int)$usage['tokens_used'],
            'tokens_max' => $maxTokens,
            'messages_sent' => (int)$usage['messages_sent'],
            'messages_received' => (int)$usage['messages_received'],
            'percentage' => $maxTokens > 0 ? round(($usage['tokens_used'] / $maxTokens) * 100, 1) : 0
        ]
    ]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
