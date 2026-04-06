<?php
// Database helper for MyBotIA
define('DB_PATH', dirname(__FILE__) . '/mybotia.db');

function getDB() {
    static $db = null;
    if ($db === null) {
        $db = new SQLite3(DB_PATH);
        $db->busyTimeout(5000);
        $db->exec('PRAGMA journal_mode = WAL');
        $db->exec('PRAGMA synchronous = NORMAL');
        $db->exec('PRAGMA foreign_keys = ON');
        initDB($db);
    }
    return $db;
}

function initDB($db) {
    // --- Existing tables ---
    $db->exec("
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL UNIQUE,
            token_hash TEXT NOT NULL,
            name TEXT DEFAULT '',
            avatar TEXT DEFAULT '',
            agent TEXT DEFAULT '',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ");

    $db->exec("
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pref_key TEXT NOT NULL,
            pref_value TEXT DEFAULT '',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, pref_key)
        )
    ");

    $db->exec("CREATE INDEX IF NOT EXISTS idx_users_token_hash ON users(token_hash)");

    // --- New tables: clients, collaborateurs, usage ---
    $db->exec("
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            company_name TEXT NOT NULL,
            contact_name TEXT DEFAULT '',
            plan TEXT DEFAULT 'pro',
            max_tokens_month INTEGER DEFAULT 500000,
            is_admin INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME
        )
    ");

    $db->exec("
        CREATE TABLE IF NOT EXISTS client_collaborateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            subdomain TEXT NOT NULL,
            gateway_token TEXT NOT NULL,
            gateway_port INTEGER DEFAULT 18789,
            display_name TEXT DEFAULT '',
            display_role TEXT DEFAULT '',
            is_default INTEGER DEFAULT 0,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            UNIQUE(client_id, subdomain)
        )
    ");

    $db->exec("
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            collaborateur TEXT NOT NULL,
            direction TEXT NOT NULL,
            char_count INTEGER DEFAULT 0,
            estimated_tokens INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ");

    // --- Profile & Instructions tables ---
    $db->exec("
        CREATE TABLE IF NOT EXISTS client_instructions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            collaborateur TEXT DEFAULT '_global',
            instructions TEXT DEFAULT '',
            synced_at DATETIME DEFAULT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            UNIQUE(client_id, collaborateur)
        )
    ");

    // Migrations: add columns if they don't exist (safe to run multiple times)
    @$db->exec("ALTER TABLE clients ADD COLUMN photo_url TEXT DEFAULT ''");
    @$db->exec("ALTER TABLE client_collaborateurs ADD COLUMN workspace_path TEXT DEFAULT ''");
    @$db->exec("ALTER TABLE client_collaborateurs ADD COLUMN voice_config TEXT DEFAULT NULL");

    $db->exec("CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email)");
    $db->exec("CREATE INDEX IF NOT EXISTS idx_usage_client ON usage_log(client_id, created_at)");
}

// --- Existing user functions ---
function getUserByToken($token) {
    $db = getDB();
    $hash = hash('sha256', $token);
    $stmt = $db->prepare("SELECT * FROM users WHERE token_hash = :hash");
    $stmt->bindValue(':hash', $hash, SQLITE3_TEXT);
    $result = $stmt->execute();
    $user = $result->fetchArray(SQLITE3_ASSOC);
    if ($user) {
        $update = $db->prepare("UPDATE users SET last_seen = CURRENT_TIMESTAMP WHERE id = :id");
        $update->bindValue(':id', $user['id'], SQLITE3_INTEGER);
        $update->execute();
    }
    return $user;
}

function getOrCreateUser($token, $name = '', $agent = '') {
    $user = getUserByToken($token);
    if ($user) return $user;
    
    $db = getDB();
    $hash = hash('sha256', $token);
    $stmt = $db->prepare("INSERT INTO users (token, token_hash, name, agent) VALUES (:token, :hash, :name, :agent)");
    $stmt->bindValue(':token', $token, SQLITE3_TEXT);
    $stmt->bindValue(':hash', $hash, SQLITE3_TEXT);
    $stmt->bindValue(':name', $name, SQLITE3_TEXT);
    $stmt->bindValue(':agent', $agent, SQLITE3_TEXT);
    $stmt->execute();
    
    return getUserByToken($token);
}

function getUserPreferences($userId) {
    $db = getDB();
    $stmt = $db->prepare("SELECT pref_key, pref_value FROM user_preferences WHERE user_id = :uid");
    $stmt->bindValue(':uid', $userId, SQLITE3_INTEGER);
    $result = $stmt->execute();
    
    $prefs = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $prefs[$row['pref_key']] = json_decode($row['pref_value'], true);
        if ($prefs[$row['pref_key']] === null) {
            $prefs[$row['pref_key']] = $row['pref_value'];
        }
    }
    return $prefs;
}

function setUserPreference($userId, $key, $value) {
    $db = getDB();
    $jsonValue = is_string($value) ? $value : json_encode($value);
    $stmt = $db->prepare("
        INSERT INTO user_preferences (user_id, pref_key, pref_value, updated_at) 
        VALUES (:uid, :key, :val, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, pref_key) 
        DO UPDATE SET pref_value = :val, updated_at = CURRENT_TIMESTAMP
    ");
    $stmt->bindValue(':uid', $userId, SQLITE3_INTEGER);
    $stmt->bindValue(':key', $key, SQLITE3_TEXT);
    $stmt->bindValue(':val', $jsonValue, SQLITE3_TEXT);
    return $stmt->execute();
}

// --- Client functions ---
function getClientByEmail($email) {
    $db = getDB();
    $stmt = $db->prepare("SELECT * FROM clients WHERE email = :email");
    $stmt->bindValue(':email', strtolower(trim($email)), SQLITE3_TEXT);
    $result = $stmt->execute();
    return $result->fetchArray(SQLITE3_ASSOC);
}

function verifyClientPassword($email, $password) {
    $client = getClientByEmail($email);
    if (!$client) return false;
    if (!password_verify($password, $client['password_hash'])) return false;
    // Update last_login
    $db = getDB();
    $stmt = $db->prepare("UPDATE clients SET last_login = CURRENT_TIMESTAMP WHERE id = :id");
    $stmt->bindValue(':id', $client['id'], SQLITE3_INTEGER);
    $stmt->execute();
    return $client;
}

function getClientById($id) {
    $db = getDB();
    $stmt = $db->prepare("SELECT * FROM clients WHERE id = :id");
    $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    $result = $stmt->execute();
    return $result->fetchArray(SQLITE3_ASSOC);
}

function getClientCollaborateurs($clientId) {
    $db = getDB();
    $stmt = $db->prepare("SELECT * FROM client_collaborateurs WHERE client_id = :cid ORDER BY is_default DESC, display_name ASC");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $result = $stmt->execute();
    $list = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $list[] = $row;
    }
    return $list;
}

function getClientCollaborateurBySubdomain($clientId, $subdomain) {
    $db = getDB();
    $stmt = $db->prepare("SELECT * FROM client_collaborateurs WHERE client_id = :cid AND subdomain = :sub");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $stmt->bindValue(':sub', $subdomain, SQLITE3_TEXT);
    $result = $stmt->execute();
    return $result->fetchArray(SQLITE3_ASSOC);
}

// --- Usage functions ---
function logUsage($clientId, $collaborateur, $direction, $charCount) {
    $db = getDB();
    $tokens = intval(ceil($charCount / 4));
    $stmt = $db->prepare("INSERT INTO usage_log (client_id, collaborateur, direction, char_count, estimated_tokens) VALUES (:cid, :col, :dir, :chars, :tokens)");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $stmt->bindValue(':col', $collaborateur, SQLITE3_TEXT);
    $stmt->bindValue(':dir', $direction, SQLITE3_TEXT);
    $stmt->bindValue(':chars', $charCount, SQLITE3_INTEGER);
    $stmt->bindValue(':tokens', $tokens, SQLITE3_INTEGER);
    return $stmt->execute();
}

function getMonthlyUsage($clientId) {
    $db = getDB();
    $firstOfMonth = date('Y-m-01 00:00:00');
    $stmt = $db->prepare("
        SELECT 
            COALESCE(SUM(estimated_tokens), 0) as tokens_used,
            COALESCE(SUM(CASE WHEN direction='sent' THEN 1 ELSE 0 END), 0) as messages_sent,
            COALESCE(SUM(CASE WHEN direction='received' THEN 1 ELSE 0 END), 0) as messages_received
        FROM usage_log 
        WHERE client_id = :cid AND created_at >= :month
    ");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $stmt->bindValue(':month', $firstOfMonth, SQLITE3_TEXT);
    $result = $stmt->execute();
    return $result->fetchArray(SQLITE3_ASSOC);
}
// --- Profile functions ---
function getClientInstructions($clientId) {
    $db = getDB();
    $stmt = $db->prepare("SELECT collaborateur, instructions, synced_at, updated_at FROM client_instructions WHERE client_id = :cid");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $result = $stmt->execute();
    $instructions = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $instructions[$row['collaborateur']] = [
            'text' => $row['instructions'],
            'synced_at' => $row['synced_at'],
            'updated_at' => $row['updated_at']
        ];
    }
    return $instructions;
}

function saveClientInstruction($clientId, $collaborateur, $text) {
    $db = getDB();
    $stmt = $db->prepare("
        INSERT INTO client_instructions (client_id, collaborateur, instructions, updated_at, synced_at)
        VALUES (:cid, :col, :text, CURRENT_TIMESTAMP, NULL)
        ON CONFLICT(client_id, collaborateur)
        DO UPDATE SET instructions = :text, updated_at = CURRENT_TIMESTAMP, synced_at = NULL
    ");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $stmt->bindValue(':col', $collaborateur, SQLITE3_TEXT);
    $stmt->bindValue(':text', $text, SQLITE3_TEXT);
    return $stmt->execute();
}

function markInstructionSynced($clientId, $collaborateur) {
    $db = getDB();
    $stmt = $db->prepare("UPDATE client_instructions SET synced_at = CURRENT_TIMESTAMP WHERE client_id = :cid AND collaborateur = :col");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $stmt->bindValue(':col', $collaborateur, SQLITE3_TEXT);
    return $stmt->execute();
}

function updateClientPhoto($clientId, $photoUrl) {
    $db = getDB();
    $stmt = $db->prepare("UPDATE clients SET photo_url = :url WHERE id = :id");
    $stmt->bindValue(':url', $photoUrl, SQLITE3_TEXT);
    $stmt->bindValue(':id', $clientId, SQLITE3_INTEGER);
    return $stmt->execute();
}

function updateClientField($clientId, $field, $value) {
    $allowed = ['contact_name', 'company_name'];
    if (!in_array($field, $allowed)) return false;
    $db = getDB();
    $stmt = $db->prepare("UPDATE clients SET $field = :val WHERE id = :id");
    $stmt->bindValue(':val', $value, SQLITE3_TEXT);
    $stmt->bindValue(':id', $clientId, SQLITE3_INTEGER);
    return $stmt->execute();
}

function getCollaborateurWorkspacePath($clientId, $subdomain) {
    $db = getDB();
    $stmt = $db->prepare("SELECT workspace_path FROM client_collaborateurs WHERE client_id = :cid AND subdomain = :sub");
    $stmt->bindValue(':cid', $clientId, SQLITE3_INTEGER);
    $stmt->bindValue(':sub', $subdomain, SQLITE3_TEXT);
    $result = $stmt->execute();
    $row = $result->fetchArray(SQLITE3_ASSOC);
    return $row ? $row['workspace_path'] : '';
}
?>
