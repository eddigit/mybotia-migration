<?php
/**
 * MyBotIA V12 — CRM API (PostgreSQL)
 * Endpoint : /api/crm.php
 *
 * GET ?action=clients[&search=xxx&status=xxx]     → Liste clients
 * GET ?action=client&id=X                         → Fiche client (+ projets + paiements)
 * GET ?action=projets[&client_id=X]               → Liste projets
 * GET ?action=paiements[&client_id=X]             → Liste paiements
 * GET ?action=stats                               → Compteurs globaux
 * POST ?action=client                             → Créer client
 * POST ?action=projet                             → Créer projet
 * POST ?action=paiement                           → Créer paiement
 * PATCH ?action=client&id=X                       → Modifier client
 * PATCH ?action=projet&id=X                       → Modifier projet
 * PATCH ?action=paiement&id=X                     → Modifier paiement
 * DELETE ?action=client&id=X                      → Supprimer client
 * DELETE ?action=projet&id=X                      → Supprimer projet
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-cache');

require_once dirname(dirname(dirname(__FILE__))) . '/private/env.php';
setCorsHeaders();

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// CRM data is admin-only — block access from client subdomains
requireAdminSubdomain();

date_default_timezone_set('Europe/Paris');

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

function jsonOut($data, $code = 200) {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

function jsonErr($msg, $code = 400) {
    jsonOut(['error' => $msg], $code);
}

function getInput() {
    return json_decode(file_get_contents('php://input'), true) ?: [];
}

function sanitizeInt($v) {
    return $v !== null && $v !== '' && is_numeric($v) ? (int)$v : null;
}

// ==================== ROUTING ====================
try {
    $db = getDb();
} catch (PDOException $e) {
    jsonErr('Connexion PostgreSQL impossible', 500);
}

$method = $_SERVER['REQUEST_METHOD'];
$action = trim($_GET['action'] ?? '');
$id = sanitizeInt($_GET['id'] ?? null);

// ==================== GET ====================
if ($method === 'GET') {
    switch ($action) {

    // ---------- STATS ----------
    case 'stats':
        $stats = [];
        $stats['clients'] = (int)$db->query("SELECT COUNT(*) FROM clients")->fetchColumn();
        $stats['clients_actifs'] = (int)$db->query("SELECT COUNT(*) FROM clients WHERE status = 'Actif'")->fetchColumn();
        $stats['prospects'] = (int)$db->query("SELECT COUNT(*) FROM clients WHERE status = 'Prospect'")->fetchColumn();
        $stats['projets'] = (int)$db->query("SELECT COUNT(*) FROM projets WHERE status NOT IN ('Terminé')")->fetchColumn();
        $stats['projets_en_cours'] = (int)$db->query("SELECT COUNT(*) FROM projets WHERE status IN ('En cours', 'Actif')")->fetchColumn();
        $stats['paiements_attente'] = (int)$db->query("SELECT COUNT(*) FROM paiements WHERE statut IN ('En attente', 'En retard', 'Partiel')")->fetchColumn();
        $r = $db->query("SELECT COALESCE(SUM(montant_attendu),0) as attendu, COALESCE(SUM(montant_recu),0) as recu FROM paiements WHERE statut != 'Annulé'");
        $row = $r->fetch();
        $stats['ca_attendu'] = round((float)$row['attendu'], 2);
        $stats['ca_recu'] = round((float)$row['recu'], 2);
        jsonOut($stats);

    // ---------- CLIENTS LIST ----------
    case 'clients':
        $search = trim($_GET['search'] ?? '');
        $status = trim($_GET['status'] ?? '');
        $where = [];
        $params = [];

        if ($search !== '') {
            $where[] = "(LOWER(nom) LIKE :s OR LOWER(societe) LIKE :s OR LOWER(email) LIKE :s)";
            $params[':s'] = '%' . mb_strtolower($search) . '%';
        }
        if ($status !== '') {
            $where[] = "status = :status";
            $params[':status'] = $status;
        }

        $sql = "SELECT id, nom, email, telephone, societe, status, abonnement, canal, agent_assigne, date_creation, notes FROM clients";
        if ($where) $sql .= " WHERE " . implode(' AND ', $where);
        $sql .= " ORDER BY CASE status WHEN 'Actif' THEN 1 WHEN 'En essai' THEN 2 WHEN 'Prospect' THEN 3 WHEN 'Liste d''attente' THEN 4 ELSE 5 END, nom ASC";
        $sql .= " LIMIT 200";

        $stmt = $db->prepare($sql);
        $stmt->execute($params);
        $clients = $stmt->fetchAll();

        // Count by status
        $counts = [];
        $cq = $db->query("SELECT status, COUNT(*) as c FROM clients GROUP BY status ORDER BY status");
        while ($r = $cq->fetch()) { $counts[$r['status']] = (int)$r['c']; }

        jsonOut(['clients' => $clients, 'counts' => $counts, 'total' => count($clients)]);

    // ---------- CLIENT DETAIL ----------
    case 'client':
        if (!$id) jsonErr('ID client manquant');
        $stmt = $db->prepare("SELECT * FROM clients WHERE id = ?");
        $stmt->execute([$id]);
        $client = $stmt->fetch();
        if (!$client) jsonErr('Client non trouvé', 404);

        // Projets liés
        $pStmt = $db->prepare("SELECT id, nom, status, priorite, budget, deadline, url_site FROM projets WHERE client_id = ? ORDER BY created_at DESC");
        $pStmt->execute([$id]);
        $projets = $pStmt->fetchAll();

        // Paiements liés
        $payStmt = $db->prepare("SELECT id, label, statut, montant_attendu, montant_recu, facture_no, date_echeance, date_paiement FROM paiements WHERE client_id = ? ORDER BY date_echeance DESC NULLS LAST");
        $payStmt->execute([$id]);
        $paiements = $payStmt->fetchAll();

        jsonOut(['client' => $client, 'projets' => $projets, 'paiements' => $paiements]);

    // ---------- PROJETS LIST ----------
    case 'projets':
        $clientId = sanitizeInt($_GET['client_id'] ?? null);
        $sql = "SELECT p.id, p.nom, p.status, p.priorite, p.budget, p.deadline, p.url_site, p.assigne, p.notes, c.nom as client_nom FROM projets p LEFT JOIN clients c ON p.client_id = c.id";
        $params = [];
        if ($clientId) {
            $sql .= " WHERE p.client_id = :cid";
            $params[':cid'] = $clientId;
        }
        $sql .= " ORDER BY CASE p.status WHEN 'En cours' THEN 1 WHEN 'Actif' THEN 2 WHEN 'À démarrer' THEN 3 WHEN 'Bloqué' THEN 4 WHEN 'En attente' THEN 5 ELSE 6 END, p.nom ASC LIMIT 200";
        $stmt = $db->prepare($sql);
        $stmt->execute($params);
        jsonOut(['projets' => $stmt->fetchAll()]);

    // ---------- PAIEMENTS LIST ----------
    case 'paiements':
        $clientId = sanitizeInt($_GET['client_id'] ?? null);
        $sql = "SELECT pa.*, c.nom as client_nom, pr.nom as projet_nom FROM paiements pa LEFT JOIN clients c ON pa.client_id = c.id LEFT JOIN projets pr ON pa.projet_id = pr.id";
        $params = [];
        if ($clientId) {
            $sql .= " WHERE pa.client_id = :cid";
            $params[':cid'] = $clientId;
        }
        $sql .= " ORDER BY CASE pa.statut WHEN 'En retard' THEN 1 WHEN 'En attente' THEN 2 WHEN 'Partiel' THEN 3 ELSE 4 END, pa.date_echeance ASC NULLS LAST LIMIT 200";
        $stmt = $db->prepare($sql);
        $stmt->execute($params);
        jsonOut(['paiements' => $stmt->fetchAll()]);

    default:
        jsonErr('Action GET inconnue: ' . $action);
    }
}

// ==================== POST (Create) ====================
if ($method === 'POST') {
    $input = getInput();

    switch ($action) {

    case 'client':
        if (empty($input['nom'])) jsonErr('Le nom est obligatoire');
        $stmt = $db->prepare("INSERT INTO clients (nom, email, telephone, societe, status, abonnement, canal, agent_assigne, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *");
        $stmt->execute([
            trim($input['nom']),
            $input['email'] ?? null,
            $input['telephone'] ?? null,
            $input['societe'] ?? null,
            $input['status'] ?? 'Prospect',
            $input['abonnement'] ?? null,
            $input['canal'] ?? null,
            $input['agent_assigne'] ?? null,
            $input['notes'] ?? null
        ]);
        jsonOut(['success' => true, 'client' => $stmt->fetch(), 'message' => 'Client créé']);

    case 'projet':
        if (empty($input['nom'])) jsonErr('Le nom est obligatoire');
        $stmt = $db->prepare("INSERT INTO projets (nom, client_id, status, priorite, budget, deadline, url_site, assigne, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *");
        $stmt->execute([
            trim($input['nom']),
            sanitizeInt($input['client_id'] ?? null),
            $input['status'] ?? 'À démarrer',
            $input['priorite'] ?? null,
            $input['budget'] ?? null,
            $input['deadline'] ?? null,
            $input['url_site'] ?? null,
            $input['assigne'] ?? null,
            $input['notes'] ?? null
        ]);
        jsonOut(['success' => true, 'projet' => $stmt->fetch(), 'message' => 'Projet créé']);

    case 'paiement':
        if (empty($input['label'])) jsonErr('Le label est obligatoire');
        $stmt = $db->prepare("INSERT INTO paiements (label, client_id, projet_id, statut, montant_attendu, montant_recu, facture_no, mode_paiement, date_echeance, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *");
        $stmt->execute([
            trim($input['label']),
            sanitizeInt($input['client_id'] ?? null),
            sanitizeInt($input['projet_id'] ?? null),
            $input['statut'] ?? 'En attente',
            $input['montant_attendu'] ?? null,
            $input['montant_recu'] ?? 0,
            $input['facture_no'] ?? null,
            $input['mode_paiement'] ?? null,
            $input['date_echeance'] ?? null,
            $input['notes'] ?? null
        ]);
        jsonOut(['success' => true, 'paiement' => $stmt->fetch(), 'message' => 'Paiement créé']);

    default:
        jsonErr('Action POST inconnue: ' . $action);
    }
}

// ==================== PATCH (Update) ====================
if ($method === 'PATCH') {
    if (!$id) jsonErr('ID manquant');
    $input = getInput();

    switch ($action) {

    case 'client':
        $fields = [];
        $vals = [];
        $allowed = ['nom', 'email', 'telephone', 'societe', 'status', 'abonnement', 'canal', 'agent_assigne', 'notes'];
        foreach ($allowed as $f) {
            if (array_key_exists($f, $input)) {
                $fields[] = "$f = ?";
                $vals[] = $input[$f];
            }
        }
        if (empty($fields)) jsonErr('Aucun champ à modifier');
        $vals[] = $id;
        $stmt = $db->prepare("UPDATE clients SET " . implode(', ', $fields) . ", updated_at = NOW() WHERE id = ? RETURNING *");
        $stmt->execute($vals);
        $row = $stmt->fetch();
        if (!$row) jsonErr('Client non trouvé', 404);
        jsonOut(['success' => true, 'client' => $row, 'message' => 'Client modifié']);

    case 'projet':
        $fields = [];
        $vals = [];
        $allowed = ['nom', 'client_id', 'status', 'priorite', 'budget', 'deadline', 'url_site', 'assigne', 'notes'];
        foreach ($allowed as $f) {
            if (array_key_exists($f, $input)) {
                $fields[] = "$f = ?";
                $vals[] = $f === 'client_id' ? sanitizeInt($input[$f]) : $input[$f];
            }
        }
        if (empty($fields)) jsonErr('Aucun champ à modifier');
        $vals[] = $id;
        $stmt = $db->prepare("UPDATE projets SET " . implode(', ', $fields) . ", updated_at = NOW() WHERE id = ? RETURNING *");
        $stmt->execute($vals);
        $row = $stmt->fetch();
        if (!$row) jsonErr('Projet non trouvé', 404);
        jsonOut(['success' => true, 'projet' => $row, 'message' => 'Projet modifié']);

    case 'paiement':
        $fields = [];
        $vals = [];
        $allowed = ['label', 'client_id', 'projet_id', 'statut', 'montant_attendu', 'montant_recu', 'facture_no', 'mode_paiement', 'date_echeance', 'date_paiement', 'notes'];
        foreach ($allowed as $f) {
            if (array_key_exists($f, $input)) {
                $fields[] = "$f = ?";
                $vals[] = in_array($f, ['client_id', 'projet_id']) ? sanitizeInt($input[$f]) : $input[$f];
            }
        }
        if (empty($fields)) jsonErr('Aucun champ à modifier');
        $vals[] = $id;
        $stmt = $db->prepare("UPDATE paiements SET " . implode(', ', $fields) . ", updated_at = NOW() WHERE id = ? RETURNING *");
        $stmt->execute($vals);
        $row = $stmt->fetch();
        if (!$row) jsonErr('Paiement non trouvé', 404);
        jsonOut(['success' => true, 'paiement' => $row, 'message' => 'Paiement modifié']);

    default:
        jsonErr('Action PATCH inconnue: ' . $action);
    }
}

// ==================== DELETE ====================
if ($method === 'DELETE') {
    if (!$id) jsonErr('ID manquant');

    switch ($action) {
    case 'client':
        $stmt = $db->prepare("DELETE FROM clients WHERE id = ?");
        $stmt->execute([$id]);
        if ($stmt->rowCount() === 0) jsonErr('Client non trouvé', 404);
        jsonOut(['success' => true, 'message' => 'Client supprimé']);

    case 'projet':
        $stmt = $db->prepare("DELETE FROM projets WHERE id = ?");
        $stmt->execute([$id]);
        if ($stmt->rowCount() === 0) jsonErr('Projet non trouvé', 404);
        jsonOut(['success' => true, 'message' => 'Projet supprimé']);

    default:
        jsonErr('Action DELETE inconnue: ' . $action);
    }
}

jsonErr('Méthode non supportée', 405);
