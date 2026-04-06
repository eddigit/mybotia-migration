<?php
/**
 * MyBotIA V12 — File Upload API
 * Endpoint : /api/upload.php
 *
 * POST (multipart/form-data) → Upload un fichier
 *   - Sauve dans ~/.openclaw/uploads/ (accessible depuis le container Docker)
 *   - Retourne le chemin serveur pour injection dans le message agent
 *
 * Types acceptés : PDF, Word, Excel, CSV, TXT, ZIP
 * Taille max : 25 Mo
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-cache');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Preflight CORS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Méthode non supportée']);
    exit;
}

// ==================== CONFIGURATION ====================
// Répertoire d'upload — monté dans le container Docker via ~/.openclaw (rw)
$uploadDir = '/home/gilles/.openclaw/uploads';
$maxSize = 25 * 1024 * 1024; // 25 Mo

$allowedTypes = [
    'application/pdf' => 'pdf',
    'application/msword' => 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document' => 'docx',
    'application/vnd.ms-excel' => 'xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' => 'xlsx',
    'text/plain' => 'txt',
    'text/csv' => 'csv',
    'application/zip' => 'zip',
    'application/json' => 'json',
    'text/markdown' => 'md',
];
// =======================================================

// Créer le répertoire si nécessaire
if (!is_dir($uploadDir)) {
    if (!mkdir($uploadDir, 0755, true)) {
        http_response_code(500);
        echo json_encode(['error' => 'Impossible de créer le répertoire upload']);
        exit;
    }
}

// Vérifier qu'un fichier a été envoyé
if (empty($_FILES['file'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Aucun fichier reçu. Utilisez le champ "file"']);
    exit;
}

$file = $_FILES['file'];

// Vérifier les erreurs d'upload PHP
if ($file['error'] !== UPLOAD_ERR_OK) {
    $errors = [
        UPLOAD_ERR_INI_SIZE => 'Fichier trop volumineux (limite PHP)',
        UPLOAD_ERR_FORM_SIZE => 'Fichier trop volumineux (limite formulaire)',
        UPLOAD_ERR_PARTIAL => 'Upload incomplet',
        UPLOAD_ERR_NO_FILE => 'Aucun fichier',
        UPLOAD_ERR_NO_TMP_DIR => 'Répertoire temporaire manquant',
        UPLOAD_ERR_CANT_WRITE => 'Écriture impossible',
    ];
    $msg = $errors[$file['error']] ?? 'Erreur upload #' . $file['error'];
    http_response_code(400);
    echo json_encode(['error' => $msg]);
    exit;
}

// Vérifier la taille
if ($file['size'] > $maxSize) {
    http_response_code(413);
    echo json_encode(['error' => 'Fichier trop volumineux (max 25 Mo)', 'size' => $file['size']]);
    exit;
}

// Vérifier le type MIME
$mimeType = $file['type'];
// Fallback: détection par extension si le MIME est générique
if ($mimeType === 'application/octet-stream') {
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    $extToMime = array_flip($allowedTypes);
    if (isset($extToMime[$ext])) {
        $mimeType = $extToMime[$ext];
    }
}

if (!isset($allowedTypes[$mimeType])) {
    http_response_code(415);
    echo json_encode([
        'error' => 'Type non supporté: ' . $mimeType,
        'allowed' => array_keys($allowedTypes)
    ]);
    exit;
}

// Générer un nom de fichier sécurisé (UUID + extension originale)
$ext = $allowedTypes[$mimeType];
$originalName = preg_replace('/[^a-zA-Z0-9._\-]/', '_', basename($file['name']));
$uuid = bin2hex(random_bytes(8)); // 16 chars hex
$timestamp = date('Ymd_His');
$safeFilename = $timestamp . '_' . $uuid . '.' . $ext;

$destPath = $uploadDir . '/' . $safeFilename;

// Déplacer le fichier
if (!move_uploaded_file($file['tmp_name'], $destPath)) {
    http_response_code(500);
    echo json_encode(['error' => 'Impossible de sauvegarder le fichier']);
    exit;
}

// Rendre lisible par le container Docker (user gilles UID 5010)
chmod($destPath, 0644);

// Retourner les infos
echo json_encode([
    'success' => true,
    'file' => [
        'name' => $file['name'],
        'safeName' => $safeFilename,
        'path' => $destPath,
        'size' => $file['size'],
        'sizeHuman' => round($file['size'] / 1024) . ' Ko',
        'mimeType' => $mimeType,
        'ext' => $ext
    ]
], JSON_UNESCAPED_UNICODE);
