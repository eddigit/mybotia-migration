<?php
/**
 * MyBotIA V12 — Tasks CRUD API (PostgreSQL + Notion sync)
 * Endpoint : /api/notion-tasks.php
 *
 * GET ?filter=today|overdue|upcoming  → Liste les tâches filtrées
 * POST                                → Crée une tâche
 * PATCH ?id=xxx                       → Complete/archive une tâche
 * DELETE ?id=xxx                      → Supprime une tâche
 *
 * Source de vérité : PostgreSQL (mybotia_crm.tasks)
 * Sync background : Notion TÂCHES (304ddac9bdfc813081deef1b4413acc6)
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-cache');

require_once dirname(dirname(dirname(__FILE__))) . '/private/env.php';
setCorsHeaders();

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// Tasks are admin-only — block access from client subdomains
requireAdminSubdomain();

// Alias for backward compatibility with existing code
define('NOTION_DB_ID', NOTION_DB_TASKS);

date_default_timezone_set('Europe/Paris');

// --- PostgreSQL connection ---
function getDb() {
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO(PG_DSN, PG_USER, PG_PASS, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]);
    }
    return $pdo;
}

// --- Format task row for API response ---
function formatTask($row) {
    $dueFormatted = '';
    if (!empty($row['deadline'])) {
        $d = DateTime::createFromFormat('Y-m-d', $row['deadline']);
        $dueFormatted = $d ? $d->format('d/m') : $row['deadline'];
    }

    $done = in_array($row['status'], ['Done', 'Terminé']);

    return [
        'id'       => (int)$row['id'],
        'title'    => $row['titre'],
        'due'      => $dueFormatted,
        'dueRaw'   => $row['deadline'] ?? '',
        'status'   => $row['status'] ?? 'À faire',
        'priority' => $row['priorite'] ?? 'Normale',
        'projet'   => $row['projet_nom'] ?? '',
        'assignee' => $row['assignee'] ?? '',
        'notes'    => $row['notes'] ?? '',
        'done'     => $done
    ];
}

// --- Notion sync (background, non-blocking) ---
function notionRequest($url, $method = 'GET', $body = null) {
    $ch = curl_init($url);
    $headers = [
        'Authorization: Bearer ' . NOTION_TOKEN,
        'Content-Type: application/json',
        'Notion-Version: ' . NOTION_VER
    ];
    $opts = [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => $headers,
        CURLOPT_TIMEOUT        => 10,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_SSL_VERIFYPEER => true
    ];
    if ($method === 'POST') {
        $opts[CURLOPT_POST] = true;
        if ($body) $opts[CURLOPT_POSTFIELDS] = json_encode($body);
    } elseif ($method === 'PATCH') {
        $opts[CURLOPT_CUSTOMREQUEST] = 'PATCH';
        if ($body) $opts[CURLOPT_POSTFIELDS] = json_encode($body);
    }
    curl_setopt_array($ch, $opts);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($response === false || $httpCode < 200 || $httpCode >= 300) return null;
    return json_decode($response, true);
}

function syncTaskToNotion($task) {
    // Fire and forget — don't block the response
    $notionId = $task['notion_id'] ?? null;
    $props = [
        'Tâche'    => ['title' => [['text' => ['content' => $task['titre']]]]],
        'Status'   => ['select' => ['name' => $task['status'] ?? 'À faire']],
    ];
    if (!empty($task['priorite'])) {
        $props['Priorité'] = ['select' => ['name' => $task['priorite']]];
    }
    if (!empty($task['deadline'])) {
        $props['Deadline'] = ['date' => ['start' => $task['deadline']]];
    }
    if (!empty($task['projet_nom'])) {
        $props['Projet'] = ['rich_text' => [['text' => ['content' => $task['projet_nom']]]]];
    }
    if (!empty($task['notes'])) {
        $props['Notes'] = ['rich_text' => [['text' => ['content' => $task['notes']]]]];
    }
    if (!empty($task['assignee'])) {
        $props['Assigné'] = ['rich_text' => [['text' => ['content' => $task['assignee']]]]];
    }

    if ($notionId) {
        notionRequest(NOTION_API . '/pages/' . $notionId, 'PATCH', ['properties' => $props]);
    } else {
        $result = notionRequest(NOTION_API . '/pages', 'POST', [
            'parent' => ['database_id' => NOTION_DB_ID],
            'properties' => $props
        ]);
        if ($result && isset($result['id'])) {
            // Save notion_id back to PG
            try {
                $db = getDb();
                $stmt = $db->prepare('UPDATE tasks SET notion_id = ? WHERE id = ?');
                $stmt->execute([$result['id'], $task['id']]);
            } catch (Exception $e) {}
        }
    }
}

// ==================== ROUTING ====================
$method = $_SERVER['REQUEST_METHOD'];

try {
    $db = getDb();
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Connexion PostgreSQL impossible']);
    exit;
}

switch ($method) {

// ========== GET : Lister les tâches filtrées ==========
case 'GET':
    $filter = trim($_GET['filter'] ?? 'today');
    $today = date('Y-m-d');

    $baseWhere = "status NOT IN ('Done', 'Terminé')";

    switch ($filter) {
        case 'today':
            // Uniquement les tâches dont la deadline est aujourd'hui
            $where = "$baseWhere AND deadline = :today";
            $params = [':today' => $today];
            break;
        case 'overdue':
            // En retard = deadline passée
            $where = "$baseWhere AND deadline < :today AND deadline IS NOT NULL";
            $params = [':today' => $today];
            break;
        case 'upcoming':
            // A venir = deadline future
            $where = "$baseWhere AND deadline > :today";
            $params = [':today' => $today];
            break;
        case 'unplanned':
            // Tâches sans date
            $where = "$baseWhere AND deadline IS NULL";
            $params = [];
            break;
        case 'all':
            // Toutes les tâches non terminées
            $where = $baseWhere;
            $params = [];
            break;
        default:
            $where = "$baseWhere AND deadline = :today";
            $params = [':today' => $today];
    }

    // Compteurs pour les badges
    $counts = [];
    $cToday = $db->prepare("SELECT COUNT(*) FROM tasks WHERE status NOT IN ('Done', 'Terminé') AND deadline = :d");
    $cToday->execute([':d' => $today]);
    $counts['today'] = (int)$cToday->fetchColumn();

    $cOverdue = $db->prepare("SELECT COUNT(*) FROM tasks WHERE status NOT IN ('Done', 'Terminé') AND deadline < :d AND deadline IS NOT NULL");
    $cOverdue->execute([':d' => $today]);
    $counts['overdue'] = (int)$cOverdue->fetchColumn();

    $cUpcoming = $db->prepare("SELECT COUNT(*) FROM tasks WHERE status NOT IN ('Done', 'Terminé') AND deadline > :d");
    $cUpcoming->execute([':d' => $today]);
    $counts['upcoming'] = (int)$cUpcoming->fetchColumn();

    $cUnplanned = $db->prepare("SELECT COUNT(*) FROM tasks WHERE status NOT IN ('Done', 'Terminé') AND deadline IS NULL");
    $cUnplanned->execute();
    $counts['unplanned'] = (int)$cUnplanned->fetchColumn();

    // Requête principale
    $order = "ORDER BY
        CASE priorite WHEN 'Urgente' THEN 1 WHEN 'Haute' THEN 2 WHEN 'Normale' THEN 3 WHEN 'Basse' THEN 4 ELSE 5 END,
        deadline ASC NULLS LAST";
    $stmt = $db->prepare("SELECT * FROM tasks WHERE $where $order LIMIT 100");
    $stmt->execute($params);

    $tasks = [];
    while ($row = $stmt->fetch()) {
        $tasks[] = formatTask($row);
    }

    echo json_encode([
        'tasks'  => $tasks,
        'date'   => $today,
        'filter' => $filter,
        'counts' => $counts,
        'count'  => count($tasks)
    ], JSON_UNESCAPED_UNICODE);
    break;

// ========== POST : Créer une tâche ==========
case 'POST':
    $input = json_decode(file_get_contents('php://input'), true);

    if (empty($input['title'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Le titre est obligatoire']);
        exit;
    }

    $titre    = trim($input['title']);
    $priorite = $input['priority'] ?? 'Normale';
    $deadline = !empty($input['deadline']) ? $input['deadline'] : null;
    $status   = $input['status'] ?? 'À faire';
    $notes    = $input['notes'] ?? null;
    $projet   = $input['projet'] ?? null;
    $assignee = $input['assignee'] ?? null;

    $stmt = $db->prepare("INSERT INTO tasks (titre, status, priorite, deadline, notes, projet_nom, assignee, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, 'webchat') RETURNING *");
    $stmt->execute([$titre, $status, $priorite, $deadline, $notes, $projet, $assignee]);
    $row = $stmt->fetch();

    // Sync to Notion in background
    syncTaskToNotion($row);

    echo json_encode([
        'success' => true,
        'task'    => formatTask($row),
        'message' => 'Tâche créée'
    ], JSON_UNESCAPED_UNICODE);
    break;

// ========== PATCH : Compléter/archiver une tâche ==========
case 'PATCH':
    $taskId = $_GET['id'] ?? '';
    if (empty($taskId) || !is_numeric($taskId)) {
        http_response_code(400);
        echo json_encode(['error' => 'ID de tâche manquant']);
        exit;
    }

    $input = json_decode(file_get_contents('php://input'), true);

    // Support deadline update
    if (isset($input['deadline'])) {
        $newDeadline = $input['deadline'] ?: null;
        $stmt = $db->prepare("UPDATE tasks SET deadline = ?, updated_at = NOW() WHERE id = ? RETURNING *");
        $stmt->execute([$newDeadline, (int)$taskId]);
        $row = $stmt->fetch();
        if (!$row) {
            http_response_code(404);
            echo json_encode(['error' => 'Tâche non trouvée']);
            exit;
        }
        syncTaskToNotion($row);
        echo json_encode(['success' => true, 'task' => formatTask($row), 'message' => 'Date mise à jour'], JSON_UNESCAPED_UNICODE);
        break;
    }

    // Support priority update
    if (isset($input['priority'])) {
        $stmt = $db->prepare("UPDATE tasks SET priorite = ?, updated_at = NOW() WHERE id = ? RETURNING *");
        $stmt->execute([$input['priority'], (int)$taskId]);
        $row = $stmt->fetch();
        if (!$row) {
            http_response_code(404);
            echo json_encode(['error' => 'Tâche non trouvée']);
            exit;
        }
        syncTaskToNotion($row);
        echo json_encode(['success' => true, 'task' => formatTask($row), 'message' => 'Priorité mise à jour'], JSON_UNESCAPED_UNICODE);
        break;
    }

    $newStatus = $input['status'] ?? 'Terminé';

    $stmt = $db->prepare("UPDATE tasks SET status = ?, completed_at = CASE WHEN ? IN ('Done', 'Terminé') THEN NOW() ELSE completed_at END, updated_at = NOW() WHERE id = ? RETURNING *");
    $stmt->execute([$newStatus, $newStatus, (int)$taskId]);
    $row = $stmt->fetch();

    if (!$row) {
        http_response_code(404);
        echo json_encode(['error' => 'Tâche non trouvée']);
        exit;
    }

    // Sync to Notion
    syncTaskToNotion($row);

    echo json_encode([
        'success' => true,
        'task'    => formatTask($row),
        'message' => 'Tâche archivée'
    ], JSON_UNESCAPED_UNICODE);
    break;

// ========== DELETE : Supprimer une tâche ==========
case 'DELETE':
    $taskId = $_GET['id'] ?? '';
    if (empty($taskId) || !is_numeric($taskId)) {
        http_response_code(400);
        echo json_encode(['error' => 'ID de tâche manquant']);
        exit;
    }

    // Récupérer notion_id avant suppression pour sync
    $stmt = $db->prepare("SELECT notion_id FROM tasks WHERE id = ?");
    $stmt->execute([(int)$taskId]);
    $row = $stmt->fetch();

    if (!$row) {
        http_response_code(404);
        echo json_encode(['error' => 'Tâche non trouvée']);
        exit;
    }

    // Supprimer de PG
    $stmt = $db->prepare("DELETE FROM tasks WHERE id = ?");
    $stmt->execute([(int)$taskId]);

    // Archiver dans Notion si notion_id existe
    if (!empty($row['notion_id'])) {
        notionRequest(NOTION_API . '/pages/' . $row['notion_id'], 'PATCH', ['archived' => true]);
    }

    echo json_encode(['success' => true, 'message' => 'Tâche supprimée'], JSON_UNESCAPED_UNICODE);
    break;

default:
    http_response_code(405);
    echo json_encode(['error' => 'Méthode non supportée']);
}
