<?php
// API: Message feedback (like/dislike)
// POST /api/feedback.php -> {session_key, message_index, rating, message_preview}

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';

ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1);
ini_set('session.cookie_samesite', 'Strict');
ini_set('session.use_strict_mode', 1);
session_name('mybotia_sid');
session_start();

if (!isset($_SESSION['client_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Not authenticated']);
    exit;
}

$clientId = $_SESSION['client_id'];
$collaborateur = $_SESSION['active_subdomain'] ?? '';

// Ensure table exists
$db = getDB();
$db->exec("
    CREATE TABLE IF NOT EXISTS message_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        collaborateur TEXT DEFAULT '',
        session_key TEXT NOT NULL,
        message_index INTEGER DEFAULT 0,
        rating TEXT NOT NULL,
        message_preview TEXT DEFAULT '',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
");
$db->exec("CREATE INDEX IF NOT EXISTS idx_feedback_client ON message_feedback(client_id, created_at)");

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);
    $sessionKey = $body['session_key'] ?? '';
    $msgIndex = intval($body['message_index'] ?? 0);
    $rating = $body['rating'] ?? '';
    $preview = mb_substr($body['message_preview'] ?? '', 0, 200);

    if (!in_array($rating, ['like', 'dislike', 'none'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid rating (like, dislike, or none)']);
        exit;
    }

    if ($rating === 'none') {
        // Remove existing feedback
        $stmt = $db->prepare("DELETE FROM message_feedback WHERE client_id = :cid AND session_key = :sk AND message_index = :mi");
        $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
        $stmt->bindValue(':sk', $sessionKey, SQLITE3_TEXT);
        $stmt->bindValue(':mi', $msgIndex, SQLITE3_INTEGER);
        $stmt->execute();
    } else {
        // Upsert feedback
        $stmt = $db->prepare("DELETE FROM message_feedback WHERE client_id = :cid AND session_key = :sk AND message_index = :mi");
        $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
        $stmt->bindValue(':sk', $sessionKey, SQLITE3_TEXT);
        $stmt->bindValue(':mi', $msgIndex, SQLITE3_INTEGER);
        $stmt->execute();

        $stmt = $db->prepare("INSERT INTO message_feedback (client_id, collaborateur, session_key, message_index, rating, message_preview) VALUES (:cid, :col, :sk, :mi, :rat, :prev)");
        $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
        $stmt->bindValue(':col', $collaborateur, SQLITE3_TEXT);
        $stmt->bindValue(':sk', $sessionKey, SQLITE3_TEXT);
        $stmt->bindValue(':mi', $msgIndex, SQLITE3_INTEGER);
        $stmt->bindValue(':rat', $rating, SQLITE3_TEXT);
        $stmt->bindValue(':prev', $preview, SQLITE3_TEXT);
        $stmt->execute();
    }

    echo json_encode(['ok' => true, 'rating' => $rating]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
