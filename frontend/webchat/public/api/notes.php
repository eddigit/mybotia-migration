<?php
/**
 * MyBotIA — Notes API (session-based, for email-auth clients)
 * GET  /api/notes.php              → Get all notes for current client
 * POST /api/notes.php              → Save notes {session_key: "...", content: "..."}
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-cache');

require_once dirname(dirname(dirname(__FILE__))) . '/private/config.inc.php';
require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';
require_once dirname(dirname(dirname(__FILE__))) . '/private/env.php';
setCorsHeaders();

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1);
ini_set('session.cookie_samesite', 'Strict');
session_name('mybotia_sid');
session_start();

$clientId = $_SESSION['client_id'] ?? null;
if (!$clientId) {
    http_response_code(401);
    echo json_encode(['error' => 'Not authenticated']);
    exit;
}

$db = getDB();

// Ensure table exists
$db->exec("
    CREATE TABLE IF NOT EXISTS client_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        session_key TEXT NOT NULL DEFAULT 'main',
        content TEXT DEFAULT '',
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(client_id, session_key)
    )
");

// GET: return all notes for this client
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $stmt = $db->prepare("SELECT session_key, content FROM client_notes WHERE client_id = :cid");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $result = $stmt->execute();

    $notes = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $notes[$row['session_key']] = $row['content'];
    }

    echo json_encode(['ok' => true, 'notes' => $notes]);
    exit;
}

// POST: save a note
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);
    $sessionKey = $body['session_key'] ?? 'main';
    $content = $body['content'] ?? '';

    $stmt = $db->prepare("
        INSERT INTO client_notes (client_id, session_key, content, updated_at)
        VALUES (:cid, :sk, :content, datetime('now'))
        ON CONFLICT(client_id, session_key)
        DO UPDATE SET content = :content, updated_at = datetime('now')
    ");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $stmt->bindValue(':sk', $sessionKey, SQLITE3_TEXT);
    $stmt->bindValue(':content', $content, SQLITE3_TEXT);
    $stmt->execute();

    echo json_encode(['ok' => true, 'saved' => $sessionKey]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
