<?php
/**
 * MyBotIA — Centralized secrets & environment config
 * All API files should require_once this instead of hardcoding credentials.
 *
 * Priority: environment variable > fallback value
 * In production, set env vars in Apache vhost or /etc/environment.
 */

// PostgreSQL (mybotia_crm)
define('PG_DSN',  getenv('MYBOTIA_PG_DSN')  ?: 'pgsql:host=127.0.0.1;port=5432;dbname=mybotia_crm');
define('PG_USER', getenv('MYBOTIA_PG_USER') ?: 'prospection');
define('PG_PASS', getenv('MYBOTIA_PG_PASS') ?: '<PG_PASSWORD>');

// Notion API
define('NOTION_TOKEN',      getenv('MYBOTIA_NOTION_TOKEN')      ?: '<NOTION_API_TOKEN>');
define('NOTION_DB_TASKS',   getenv('MYBOTIA_NOTION_DB_TASKS')   ?: '304ddac9bdfc813081deef1b4413acc6');
define('NOTION_DB_CLIENTS', getenv('MYBOTIA_NOTION_DB_CLIENTS') ?: '304ddac9bdfc8101b72fdf250da9f1f6');
define('NOTION_API',        'https://api.notion.com/v1');
define('NOTION_VER',        '2022-06-28');

// CORS — allowed origins
define('ALLOWED_ORIGINS', [
    'https://app.mybotia.com',
    'https://admin.mybotia.com',
    'https://lea.mybotia.com',
    'https://julian.mybotia.com',
    'https://nina.mybotia.com',
    'https://oscar.mybotia.com',
    'https://max.mybotia.com',
    'https://eva.mybotia.com',
    'https://brice.mybotia.com',
    'https://lucy.mybotia.com',
    'https://client.mybotia.com',
    'https://voice.mybotia.com',
]);

/**
 * Set CORS headers based on request Origin.
 * Replaces hardcoded Access-Control-Allow-Origin: *
 */
function setCorsHeaders() {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    // Allow any *.mybotia.com subdomain
    if ($origin && preg_match('#^https://[a-z0-9-]+\.mybotia\.com$#', $origin)) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Vary: Origin');
    }
    header('Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, X-CSRF-Token');
    header('Access-Control-Allow-Credentials: true');
}

/**
 * CSRF token management.
 * Generate on login, verify on state-changing requests.
 */
function generateCsrfToken() {
    if (session_status() !== PHP_SESSION_ACTIVE) return '';
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function verifyCsrfToken() {
    if ($_SERVER['REQUEST_METHOD'] === 'GET' || $_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        return true;
    }
    $token = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    if (empty($token) || empty($_SESSION['csrf_token'])) {
        return false;
    }
    return hash_equals($_SESSION['csrf_token'], $token);
}

// Admin-only subdomains — these can access CRM, tasks, internal tools
define('ADMIN_SUBDOMAINS', ['app', 'admin', 'lea', 'julian', 'nina', 'oscar']);

/**
 * Guard: block access to admin-only APIs from client subdomains.
 * Call this at the top of any API that exposes internal data (CRM, tasks, etc.)
 * Returns the current subdomain if allowed, or exits with 403.
 */
function requireAdminSubdomain() {
    $host = $_SERVER['HTTP_HOST'] ?? '';
    $sub = explode('.', $host)[0] ?? '';
    if (!in_array($sub, ADMIN_SUBDOMAINS, true)) {
        http_response_code(403);
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Access denied']);
        exit;
    }
    return $sub;
}

/**
 * Get the current subdomain from the request host.
 */
function getCurrentSubdomain() {
    $host = $_SERVER['HTTP_HOST'] ?? '';
    return explode('.', $host)[0] ?? '';
}

/**
 * Shared PostgreSQL connection.
 */
function getPgDb() {
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO(PG_DSN, PG_USER, PG_PASS, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]);
    }
    return $pdo;
}
