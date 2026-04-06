<?php
/**
 * MyBotIA V12 — Notion Clients API
 * Endpoint : /api/notion-clients.php
 *
 * GET              → Liste les clients (filtrable par ?q=recherche, ?collaborateur=lea)
 * GET  ?id=xxx     → Detail d'un client
 * POST             → Cree un client
 * PATCH ?id=xxx    → Modifie un client
 *
 * Base Notion CLIENTS — colonnes :
 *   Nom (title), Societe (text), Email (email), Telephone (phone),
 *   Adresse (text), Type (select: Prospect/Client/Partenaire),
 *   Notes (text), Collaborateur (select), Status (select)
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-cache');

require_once dirname(dirname(dirname(__FILE__))) . '/private/env.php';
setCorsHeaders();

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

date_default_timezone_set('Europe/Paris');

/**
 * Appel generique a l'API Notion
 */
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
        CURLOPT_TIMEOUT        => 30,
        CURLOPT_CONNECTTIMEOUT => 15,
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
    $err = curl_error($ch);
    curl_close($ch);

    if ($response === false) {
        return ['error' => true, 'code' => 502, 'message' => $err];
    }

    $data = json_decode($response, true);
    if ($httpCode < 200 || $httpCode >= 300) {
        return ['error' => true, 'code' => $httpCode, 'message' => $data['message'] ?? 'Erreur Notion'];
    }

    return ['error' => false, 'code' => $httpCode, 'data' => $data];
}

/**
 * Transforme une page Notion en objet client simplifie
 */
function pageToClient($page) {
    $props = $page['properties'];

    // Helper: extract rich_text content
    $getText = function($prop) use ($props) {
        $val = '';
        if (isset($props[$prop]['rich_text'])) {
            foreach ($props[$prop]['rich_text'] as $t) {
                $val .= $t['plain_text'];
            }
        }
        return $val;
    };

    $nom = '';
    if (isset($props['Nom']['title'])) {
        foreach ($props['Nom']['title'] as $t) {
            $nom .= $t['plain_text'];
        }
    }

    $societe = $getText('Société');
    $email = $props['Email']['email'] ?? '';
    $telephone = $props['Téléphone']['phone_number'] ?? '';
    $notes = $getText('Notes');
    $jidWhatsapp = $getText('JID WhatsApp');

    $status = $props['Status']['select']['name'] ?? '';
    $agentAssigne = $props['Agent assigné']['select']['name'] ?? '';
    $abonnement = $props['Abonnement']['select']['name'] ?? '';
    $canal = $props['Canal']['select']['name'] ?? '';

    $dateCreation = '';
    if (isset($props['Date création']['date']['start'])) {
        $dateCreation = $props['Date création']['date']['start'];
    }
    $dateEssai = '';
    if (isset($props['Date début essai']['date']['start'])) {
        $dateEssai = $props['Date début essai']['date']['start'];
    }

    return [
        'id'            => $page['id'],
        'nom'           => $nom,
        'societe'       => $societe,
        'email'         => $email,
        'telephone'     => $telephone,
        'status'        => $status,
        'agentAssigne'  => $agentAssigne,
        'abonnement'    => $abonnement,
        'canal'         => $canal,
        'notes'         => $notes,
        'jidWhatsapp'   => $jidWhatsapp,
        'dateCreation'  => $dateCreation,
        'dateEssai'     => $dateEssai,
        'url'           => $page['url'] ?? '',
        'created'       => $page['created_time'] ?? '',
        'updated'       => $page['last_edited_time'] ?? ''
    ];
}

// ==================== ROUTING ====================
$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {

// ========== GET : Lister ou Detail ==========
case 'GET':
    // Detail d'un client
    if (!empty($_GET['id'])) {
        $result = notionRequest(NOTION_API . '/pages/' . $_GET['id']);
        if ($result['error']) {
            http_response_code($result['code']);
            echo json_encode(['error' => $result['message']]);
            exit;
        }
        echo json_encode([
            'client' => pageToClient($result['data'])
        ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        exit;
    }

    // Liste avec recherche optionnelle
    $query = trim($_GET['q'] ?? '');
    $agent = trim($_GET['agent'] ?? '');

    $filters = [];

    if ($query !== '') {
        $filters[] = [
            'or' => [
                ['property' => 'Nom', 'title' => ['contains' => $query]],
                ['property' => 'Société', 'rich_text' => ['contains' => $query]],
                ['property' => 'Email', 'email' => ['contains' => $query]]
            ]
        ];
    }

    if ($agent !== '') {
        $filters[] = [
            'property' => 'Agent assigné',
            'select' => ['equals' => $agent]
        ];
    }

    $body = [
        'sorts' => [['property' => 'Nom', 'direction' => 'ascending']],
        'page_size' => 50
    ];

    if (count($filters) === 1) {
        $body['filter'] = $filters[0];
    } elseif (count($filters) > 1) {
        $body['filter'] = ['and' => $filters];
    }

    $result = notionRequest(
        NOTION_API . '/databases/' . NOTION_DB_CLIENTS . '/query',
        'POST',
        $body
    );

    if ($result['error']) {
        http_response_code($result['code']);
        echo json_encode(['error' => $result['message'], 'clients' => []]);
        exit;
    }

    $clients = [];
    foreach ($result['data']['results'] as $page) {
        $clients[] = pageToClient($page);
    }

    echo json_encode([
        'clients' => $clients,
        'count'   => count($clients)
    ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    break;

// ========== POST : Creer un client ==========
case 'POST':
    $input = json_decode(file_get_contents('php://input'), true);

    if (empty($input['nom'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Le nom est obligatoire']);
        exit;
    }

    $properties = [
        'Nom' => [
            'title' => [['text' => ['content' => $input['nom']]]]
        ]
    ];

    if (!empty($input['societe'])) {
        $properties['Société'] = ['rich_text' => [['text' => ['content' => $input['societe']]]]];
    }
    if (!empty($input['email'])) {
        $properties['Email'] = ['email' => $input['email']];
    }
    if (!empty($input['telephone'])) {
        $properties['Téléphone'] = ['phone_number' => $input['telephone']];
    }
    if (!empty($input['status'])) {
        $properties['Status'] = ['select' => ['name' => $input['status']]];
    }
    if (!empty($input['agentAssigne'])) {
        $properties['Agent assigné'] = ['select' => ['name' => $input['agentAssigne']]];
    }
    if (!empty($input['abonnement'])) {
        $properties['Abonnement'] = ['select' => ['name' => $input['abonnement']]];
    }
    if (!empty($input['canal'])) {
        $properties['Canal'] = ['select' => ['name' => $input['canal']]];
    }
    if (!empty($input['notes'])) {
        $properties['Notes'] = ['rich_text' => [['text' => ['content' => $input['notes']]]]];
    }

    $result = notionRequest(NOTION_API . '/pages', 'POST', [
        'parent' => ['database_id' => NOTION_DB_CLIENTS],
        'properties' => $properties
    ]);

    if ($result['error']) {
        http_response_code($result['code']);
        echo json_encode(['error' => $result['message']]);
        exit;
    }

    echo json_encode([
        'success' => true,
        'client' => pageToClient($result['data']),
        'message' => 'Client cree'
    ], JSON_UNESCAPED_UNICODE);
    break;

// ========== PATCH : Modifier un client ==========
case 'PATCH':
    $pageId = $_GET['id'] ?? '';
    if (empty($pageId)) {
        http_response_code(400);
        echo json_encode(['error' => 'ID client manquant']);
        exit;
    }

    $input = json_decode(file_get_contents('php://input'), true);
    $properties = [];

    if (isset($input['nom'])) {
        $properties['Nom'] = ['title' => [['text' => ['content' => $input['nom']]]]];
    }
    if (isset($input['societe'])) {
        $properties['Société'] = ['rich_text' => [['text' => ['content' => $input['societe']]]]];
    }
    if (isset($input['email'])) {
        $properties['Email'] = ['email' => $input['email'] ?: null];
    }
    if (isset($input['telephone'])) {
        $properties['Téléphone'] = ['phone_number' => $input['telephone'] ?: null];
    }
    if (isset($input['status'])) {
        $properties['Status'] = ['select' => ['name' => $input['status']]];
    }
    if (isset($input['agentAssigne'])) {
        $properties['Agent assigné'] = ['select' => ['name' => $input['agentAssigne']]];
    }
    if (isset($input['abonnement'])) {
        $properties['Abonnement'] = ['select' => ['name' => $input['abonnement']]];
    }
    if (isset($input['canal'])) {
        $properties['Canal'] = ['select' => ['name' => $input['canal']]];
    }
    if (isset($input['notes'])) {
        $properties['Notes'] = ['rich_text' => [['text' => ['content' => $input['notes']]]]];
    }

    if (empty($properties)) {
        http_response_code(400);
        echo json_encode(['error' => 'Aucune propriete a modifier']);
        exit;
    }

    $result = notionRequest(NOTION_API . '/pages/' . $pageId, 'PATCH', ['properties' => $properties]);

    if ($result['error']) {
        http_response_code($result['code']);
        echo json_encode(['error' => $result['message']]);
        exit;
    }

    echo json_encode([
        'success' => true,
        'client'  => pageToClient($result['data']),
        'message' => 'Client modifie'
    ], JSON_UNESCAPED_UNICODE);
    break;

default:
    http_response_code(405);
    echo json_encode(['error' => 'Methode non supportee']);
}
