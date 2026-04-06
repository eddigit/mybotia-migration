<?php
// API: Link Preview — fetch Open Graph meta tags from a URL
// GET /api/link-preview.php?url=https://example.com

header('Content-Type: application/json');
header('Cache-Control: public, max-age=86400'); // Cache 24h

$url = $_GET['url'] ?? '';

if (!$url || !filter_var($url, FILTER_VALIDATE_URL)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid URL']);
    exit;
}

// Only allow http/https
$scheme = parse_url($url, PHP_URL_SCHEME);
if (!in_array($scheme, ['http', 'https'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Only http/https allowed']);
    exit;
}

// Block private IPs
$host = parse_url($url, PHP_URL_HOST);
$ip = gethostbyname($host);
if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) === false) {
    http_response_code(403);
    echo json_encode(['error' => 'Private IPs not allowed']);
    exit;
}

$ctx = stream_context_create([
    'http' => [
        'timeout' => 5,
        'max_redirects' => 3,
        'user_agent' => 'Mozilla/5.0 (compatible; MyBotIA/1.0)',
        'header' => "Accept: text/html\r\n"
    ],
    'ssl' => ['verify_peer' => false]
]);

$html = @file_get_contents($url, false, $ctx, 0, 50000); // Max 50KB
if (!$html) {
    http_response_code(502);
    echo json_encode(['error' => 'Could not fetch URL']);
    exit;
}

$result = ['url' => $url, 'title' => '', 'description' => '', 'image' => '', 'site_name' => ''];

// Parse OG tags
if (preg_match('/<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']/si', $html, $m)) {
    $result['title'] = html_entity_decode($m[1], ENT_QUOTES, 'UTF-8');
}
if (preg_match('/<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']/si', $html, $m)) {
    $result['description'] = html_entity_decode($m[1], ENT_QUOTES, 'UTF-8');
}
if (preg_match('/<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']/si', $html, $m)) {
    $result['image'] = $m[1];
}
if (preg_match('/<meta\s+property=["\']og:site_name["\']\s+content=["\'](.*?)["\']/si', $html, $m)) {
    $result['site_name'] = html_entity_decode($m[1], ENT_QUOTES, 'UTF-8');
}

// Fallback to <title>
if (!$result['title'] && preg_match('/<title>(.*?)<\/title>/si', $html, $m)) {
    $result['title'] = html_entity_decode(trim($m[1]), ENT_QUOTES, 'UTF-8');
}
// Fallback to meta description
if (!$result['description'] && preg_match('/<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']/si', $html, $m)) {
    $result['description'] = html_entity_decode($m[1], ENT_QUOTES, 'UTF-8');
}

// Truncate
$result['title'] = mb_substr($result['title'], 0, 150);
$result['description'] = mb_substr($result['description'], 0, 300);

echo json_encode($result);
