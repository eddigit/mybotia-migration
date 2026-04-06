# OpenClaw Agents — Doc à jour 14/02/2026 13h50

## Version actuelle
- **Local** : 2026.2.13
- **VPS** : 2026.2.9 (à mettre à jour)

---

## COMMANDES OFFICIELLES (pas de manipulation manuelle !)

### Lister les agents
```bash
openclaw agents list
openclaw agents list --bindings   # avec le routage
```

### Ajouter un agent
```bash
openclaw agents add <nom> --workspace ~/.openclaw/workspace-<nom>
```

### Supprimer un agent
```bash
openclaw agents delete <nom>
```

### Modifier l'identité
```bash
openclaw agents set-identity --agent <nom> --name "Nom" --emoji "🎯"
```

---

## STRUCTURE DES FICHIERS

```
~/.openclaw/
├── openclaw.json          # Config principale (agents, bindings, channels)
├── workspace/             # Workspace agent principal (main)
├── agents/
│   ├── main/
│   │   ├── agent/         # Auth profiles, state
│   │   └── sessions/      # Historique conversations
│   ├── lea/
│   │   ├── agent/
│   │   └── sessions/
│   └── nina/
│       ├── agent/
│       └── sessions/
└── credentials/
    └── whatsapp/          # Credentials WhatsApp par compte
```

---

## CONFIGURATION MULTI-AGENT (openclaw.json)

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "Léa",
        workspace: "~/.openclaw/workspace",
        agentDir: "~/.openclaw/agents/main/agent",
      },
      {
        id: "nina",
        name: "Nina",
        workspace: "~/.openclaw/agents/nina/workspace",
        agentDir: "~/.openclaw/agents/nina/agent",
      },
    ],
  },
  bindings: [
    // Routage par défaut vers main (Léa)
    { agentId: "main", match: { channel: "whatsapp" } },
    // Routage spécifique pour Nina si besoin
    // { agentId: "nina", match: { channel: "whatsapp", peer: { kind: "direct", id: "+33..." } } },
  ],
}
```

---

## PROCÉDURE NETTOYAGE VPS (avec commandes officielles)

### 1. Backup
```bash
cd ~/.openclaw
tar -czf agents_backup_$(date +%Y%m%d_%H%M).tar.gz agents/
```

### 2. Lister les agents actuels
```bash
openclaw agents list
```

### 3. Supprimer les agents inutiles
```bash
openclaw agents delete iris
openclaw agents delete jules
openclaw agents delete nessy
openclaw agents delete oscar
openclaw agents delete nina   # on recrée proprement après
```

### 4. Vérifier que "main" = Léa
Si main n'est pas Léa, modifier la config :
```bash
openclaw config set agents.list[0].name "Léa"
```

### 5. Recréer Nina proprement
```bash
openclaw agents add nina --workspace ~/.openclaw/agents/nina/workspace
openclaw agents set-identity --agent nina --name "Nina" --emoji "🎯"
```

### 6. Restart gateway
```bash
openclaw gateway restart
```

---

## VÉRIFICATIONS POST-NETTOYAGE

```bash
openclaw agents list --bindings
openclaw health
openclaw status
```

---

## RÈGLES IMPORTANTES

1. **TOUJOURS utiliser les commandes `openclaw agents`** — pas de rm -rf manuel
2. **Backup AVANT toute suppression**
3. **L'agent "main" est le défaut** — tous les messages non-routés vont vers main
4. **Chaque agent a son workspace isolé** — pas de partage de fichiers
5. **Les sessions sont par agent** — supprimer un agent = perdre son historique

---

*Généré le 14/02/2026 à 13h52*
