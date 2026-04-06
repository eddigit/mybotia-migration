<?php
// API: Client profile management (email-authenticated)
// GET    /api/profile.php         -> get full profile + instructions
// POST   /api/profile.php         -> upload photo (multipart/form-data)
// PUT    /api/profile.php         -> save profile fields + instructions + sync workspace

header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

require_once dirname(dirname(dirname(__FILE__))) . '/private/db.php';

// Session check
session_name('mybotia_sid');
session_start();

if (empty($_SESSION['client_id']) || empty($_SESSION['auth_type']) || $_SESSION['auth_type'] !== 'email') {
    http_response_code(401);
    echo json_encode(['error' => 'Non authentifié (login email requis)']);
    exit;
}

$clientId = $_SESSION['client_id'];
$client = getClientById($clientId);
if (!$client) {
    http_response_code(404);
    echo json_encode(['error' => 'Client introuvable']);
    exit;
}

// ========== GET: Full profile + instructions ==========
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $collaborateurs = getClientCollaborateurs($clientId);
    $instructions = getClientInstructions($clientId);

    // Format instructions as key->text map
    $instructionsMap = [];
    foreach ($instructions as $key => $data) {
        $instructionsMap[$key] = $data['text'];
    }

    // Format collaborateurs
    $collabList = [];
    foreach ($collaborateurs as $c) {
        $collabList[] = [
            'subdomain' => $c['subdomain'],
            'name' => $c['display_name'],
            'role' => $c['display_role']
        ];
    }

    echo json_encode([
        'ok' => true,
        'profile' => [
            'company_name' => $client['company_name'],
            'contact_name' => $client['contact_name'],
            'email' => $client['email'],
            'plan' => $client['plan'],
            'max_tokens' => $client['max_tokens_month'],
            'photo_url' => $client['photo_url'] ?? '',
            'is_admin' => (bool)$client['is_admin']
        ],
        'instructions' => $instructionsMap,
        'collaborateurs' => $collabList
    ]);
    exit;
}

// ========== POST: Upload photo (multipart/form-data) ==========
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Check if this is a photo upload
    if (!isset($_FILES['photo'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Aucun fichier photo envoyé']);
        exit;
    }

    $file = $_FILES['photo'];

    // Validate upload
    if ($file['error'] !== UPLOAD_ERR_OK) {
        $errors = [
            UPLOAD_ERR_INI_SIZE => 'Fichier trop volumineux (limite serveur)',
            UPLOAD_ERR_FORM_SIZE => 'Fichier trop volumineux',
            UPLOAD_ERR_PARTIAL => 'Upload interrompu',
            UPLOAD_ERR_NO_FILE => 'Aucun fichier',
        ];
        http_response_code(400);
        echo json_encode(['error' => $errors[$file['error']] ?? 'Erreur upload']);
        exit;
    }

    // Validate size (max 2 MB)
    if ($file['size'] > 2 * 1024 * 1024) {
        http_response_code(400);
        echo json_encode(['error' => 'Photo trop volumineuse (max 2 Mo)']);
        exit;
    }

    // Validate MIME type
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mimeType = finfo_file($finfo, $file['tmp_name']);
    finfo_close($finfo);

    $allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!in_array($mimeType, $allowedTypes)) {
        http_response_code(400);
        echo json_encode(['error' => 'Format non supporté (JPEG, PNG ou WebP)']);
        exit;
    }

    // Process image with GD: resize to 256x256 max, convert to JPEG
    $srcImage = null;
    switch ($mimeType) {
        case 'image/jpeg': $srcImage = imagecreatefromjpeg($file['tmp_name']); break;
        case 'image/png':  $srcImage = imagecreatefrompng($file['tmp_name']); break;
        case 'image/webp': $srcImage = imagecreatefromwebp($file['tmp_name']); break;
    }

    if (!$srcImage) {
        http_response_code(500);
        echo json_encode(['error' => 'Impossible de traiter l\'image']);
        exit;
    }

    $srcW = imagesx($srcImage);
    $srcH = imagesy($srcImage);

    // Crop to square (center) then resize to 256x256
    $cropSize = min($srcW, $srcH);
    $cropX = ($srcW - $cropSize) / 2;
    $cropY = ($srcH - $cropSize) / 2;

    $destImage = imagecreatetruecolor(256, 256);
    imagecopyresampled($destImage, $srcImage, 0, 0, $cropX, $cropY, 256, 256, $cropSize, $cropSize);

    // Save as JPEG
    $filename = 'client_' . $clientId . '_' . time() . '.jpg';
    $uploadDir = dirname(dirname(__FILE__)) . '/uploads/profile/';
    $filepath = $uploadDir . $filename;

    if (!imagejpeg($destImage, $filepath, 85)) {
        http_response_code(500);
        echo json_encode(['error' => 'Erreur lors de la sauvegarde']);
        exit;
    }

    imagedestroy($srcImage);
    imagedestroy($destImage);

    // Delete old photo if exists
    $oldPhoto = $client['photo_url'] ?? '';
    if ($oldPhoto && strpos($oldPhoto, '/uploads/profile/') !== false) {
        $oldPath = dirname(dirname(__FILE__)) . $oldPhoto;
        if (file_exists($oldPath)) @unlink($oldPath);
    }

    // Update DB
    $photoUrl = '/uploads/profile/' . $filename;
    updateClientPhoto($clientId, $photoUrl);

    echo json_encode([
        'ok' => true,
        'photo_url' => $photoUrl
    ]);
    exit;
}

// ========== PUT: Save profile fields + instructions + sync workspace ==========
if ($_SERVER['REQUEST_METHOD'] === 'PUT') {
    $body = json_decode(file_get_contents('php://input'), true);
    if (!$body) {
        http_response_code(400);
        echo json_encode(['error' => 'JSON invalide']);
        exit;
    }

    $updated = [];
    $synced = [];

    // Update contact_name
    if (isset($body['contact_name']) && is_string($body['contact_name'])) {
        $name = trim(substr($body['contact_name'], 0, 100));
        if ($name !== '') {
            updateClientField($clientId, 'contact_name', $name);
            $updated[] = 'contact_name';
        }
    }

    // Save instructions
    if (isset($body['instructions']) && is_array($body['instructions'])) {
        $globalText = '';

        foreach ($body['instructions'] as $collab => $text) {
            if (!is_string($text)) continue;
            $text = trim(substr($text, 0, 5000)); // Max 5000 chars per instruction
            $safeCollab = preg_replace('/[^a-z0-9_-]/', '', strtolower($collab));
            if ($safeCollab === '' && $collab === '_global') $safeCollab = '_global';
            if ($safeCollab === '') continue;

            saveClientInstruction($clientId, $safeCollab, $text);
            $updated[] = 'instructions.' . $safeCollab;

            if ($safeCollab === '_global') {
                $globalText = $text;
            }
        }

        // Sync to workspace for each collaborateur with instructions
        $collaborateurs = getClientCollaborateurs($clientId);
        $allInstructions = getClientInstructions($clientId);
        $globalInstr = isset($allInstructions['_global']) ? $allInstructions['_global']['text'] : '';

        foreach ($collaborateurs as $c) {
            $sub = $c['subdomain'];
            $workspacePath = $c['workspace_path'];
            if (!$workspacePath) continue;

            // Build CLIENT_INSTRUCTIONS.md content
            $collabInstr = isset($allInstructions[$sub]) ? $allInstructions[$sub]['text'] : '';

            // Only write if there are actual instructions
            if ($globalInstr === '' && $collabInstr === '') continue;

            $content = "# Instructions Client — " . $client['company_name'] . "\n";
            $content .= "> Synchronisé le " . date('d/m/Y à H:i') . "\n\n";

            if ($globalInstr !== '') {
                $content .= "## Instructions Générales\n\n";
                $content .= $globalInstr . "\n\n";
            }

            if ($collabInstr !== '') {
                $content .= "## Instructions Spécifiques (" . $c['display_name'] . ")\n\n";
                $content .= $collabInstr . "\n";
            }

            // Ensure workspace directory exists
            if (!is_dir($workspacePath)) {
                @mkdir($workspacePath, 0755, true);
            }

            $filePath = rtrim($workspacePath, '/') . '/CLIENT_INSTRUCTIONS.md';
            if (file_put_contents($filePath, $content) !== false) {
                markInstructionSynced($clientId, '_global');
                if ($collabInstr !== '') markInstructionSynced($clientId, $sub);
                $synced[] = $sub;
            }
        }
    }

    echo json_encode([
        'ok' => true,
        'updated' => $updated,
        'synced' => $synced
    ]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Méthode non supportée']);
