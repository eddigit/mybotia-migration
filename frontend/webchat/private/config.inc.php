<?php
define('AGENTS_FILE', dirname(__FILE__) . '/agents.json');

function getAgentsConfig() {
    if (!file_exists(AGENTS_FILE)) return null;
    return json_decode(file_get_contents(AGENTS_FILE), true);
}

function validateToken($token) {
    $agents = getAgentsConfig();
    if (!$agents) return null;
    foreach ($agents as $name => $config) {
        if (isset($config['token']) && $config['token'] === $token) {
            return [
                'name' => $name,
                'session' => $config['session'] ?? $name,
                'agentId' => $config['agentId'] ?? 'main',
                'displayName' => $config['name'] ?? $name
            ];
        }
    }
    return null;
}

function getAgentBySubdomain($subdomain) {
    $agents = getAgentsConfig();
    if (!$agents || !isset($agents[$subdomain])) return null;
    $a = $agents[$subdomain];
    return [
        'name' => $subdomain,
        'session' => $a['session'] ?? $subdomain,
        'agentId' => $a['agentId'] ?? 'main',
        'displayName' => $a['name'] ?? $subdomain,
        'avatar' => $a['avatar'] ?? '',
        'role' => $a['role'] ?? '',
        'cards' => $a['cards'] ?? []
    ];
}
?>
