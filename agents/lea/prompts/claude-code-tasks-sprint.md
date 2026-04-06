# SPRINT — Tâches + Briefing Matin + Sync Notion

## Contexte

L'Agent API (`/api/agent/`) sur le MVP Admin MyBotIA (port 3001) est opérationnelle. On a déjà :
- CRUD clients, pipeline, projets, paiements
- Briefing business (`GET /briefing`)
- Alertes paiements en retard
- Sync Notion bidirectionnelle sur les clients

**Il manque la brique TÂCHES** — c'est critique pour le pilotage quotidien par Léa (agent IA principal).

## Ce qui existe dans Notion

Base **TÂCHES** — ID : `304ddac9-bdfc-8130-81de-ef1b4413acc6`

Propriétés Notion :
| Propriété | Type Notion | Valeurs |
|-----------|-------------|---------|
| Tâche | `title` | Titre de la tâche |
| Status | `select` | `À faire`, `En cours`, `Review`, `Done`, `Terminé` |
| Priorité | `select` | `Urgente`, `Haute`, `Normale`, `Basse`, `Moyenne` |
| Assigné | `rich_text` | Nom libre (ex: `Léa`, `Gilles`, `Jules`, `Claude Code`) |
| Projet | `rich_text` | Nom du projet (texte libre) |
| Deadline | `date` | Date d'échéance |
| Notes | `rich_text` | Détails / contexte |

Il y a déjà 20 tâches dedans (certaines outdated).

## À implémenter

### 1. Table SQLite `tasks`

```sql
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  notionId TEXT UNIQUE,
  titre TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'À faire',    -- À faire, En cours, Review, Done, Terminé
  priorite TEXT DEFAULT 'Normale',   -- Urgente, Haute, Normale, Basse
  assignee TEXT,                     -- Léa, Gilles, Jules, Nina, Claude Code, etc.
  projetId INTEGER REFERENCES projets(id),
  projetNom TEXT,                    -- Dénormalisé pour affichage rapide
  clientId INTEGER REFERENCES clients(id),
  clientNom TEXT,                    -- Dénormalisé
  deadline DATE,
  completedAt DATETIME,
  createdBy TEXT DEFAULT 'system',
  notes TEXT,
  createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Endpoints Agent API

```
GET    /api/agent/tasks                → Liste tâches
         ?status=À faire
         ?assignee=lea
         ?projetId=74
         ?clientId=22
         ?deadline=today          (deadline ≤ aujourd'hui)
         ?deadline=week           (deadline ≤ 7 jours)
         ?priorite=Urgente

GET    /api/agent/tasks/:id            → Détail tâche

POST   /api/agent/tasks                → Créer tâche
         Body: { titre, description?, status?, priorite?, assignee?,
                 projetId?, clientId?, deadline?, notes? }
         → Sync Notion (créer page dans base TÂCHES)

PUT    /api/agent/tasks/:id            → Modifier tâche
         → Sync Notion (update page)

DELETE /api/agent/tasks/:id            → Archiver (status → Terminé)
         → Sync Notion

GET    /api/agent/tasks/today          → Tâches actionnables MAINTENANT
         Retourne :
         - overdue: tâches avec deadline passée et status ≠ Done/Terminé
         - today: tâches avec deadline = aujourd'hui
         - urgent: tâches priorité Urgente/Haute sans deadline
         - inProgress: tâches status "En cours"
```

### 3. Endpoint `/api/agent/morning` — Briefing Matin

Un seul appel qui agrège TOUT ce dont Léa a besoin le matin :

```json
GET /api/agent/morning

Response:
{
  "date": "2026-03-20",
  "bonjour": "Bonjour Gilles, voici ton briefing du jeudi 20 mars 2026.",

  "urgences": [
    // Tâches en retard (deadline dépassée)
    // Paiements en retard
  ],

  "aujourdhui": {
    "taches": [
      // Tâches deadline = aujourd'hui
    ],
    "rdv": []  // Placeholder pour calendrier futur
  },

  "enCours": [
    // Tâches status "En cours" toutes assignees confondues
  ],

  "business": {
    "mrr": 7840,
    "encaisse": 3453,
    "attendu": 6743,
    "paiementsRetard": 3,
    "pipelineValeur": 26600
  },

  "aFaire": [
    // Top 10 tâches "À faire" triées par priorité puis deadline
  ],

  "resume": "3 urgences. 2 tâches aujourd'hui. MRR 7 840€. 3 paiements en retard (total ~2 926€)."
}
```

### 4. Sync Notion bidirectionnelle

**MVP → Notion :**
- POST /tasks → créer page Notion dans base `304ddac9-bdfc-8130-81de-ef1b4413acc6`
- PUT /tasks/:id → update propriétés page Notion
- DELETE /tasks/:id → update status "Terminé" dans Notion

**Notion → MVP (import initial) :**
- Ajouter une route `POST /api/agent/tasks/sync-notion` qui :
  1. Query la base Notion TÂCHES
  2. Pour chaque tâche Notion non présente en local (par notionId) → INSERT
  3. Pour chaque tâche existante → UPDATE si Notion plus récent
  4. Retourne le nombre de tâches synchro

**Mapping Notion ↔ SQLite :**
| Notion | SQLite |
|--------|--------|
| Tâche (title) | titre |
| Status (select) | status |
| Priorité (select) | priorite |
| Assigné (rich_text) | assignee |
| Projet (rich_text) | projetNom |
| Deadline (date) | deadline |
| Notes (rich_text) | notes |
| page.id | notionId |

### 5. Vue Dashboard (optionnel mais utile)

Si le temps le permet, ajouter un onglet **Tâches** dans le dashboard admin (`admin.mybotia.com`) :
- Vue kanban (À faire → En cours → Review → Done)
- Filtre par assignee, projet, priorité
- Création rapide de tâche
- Drag & drop pour changer le status

### 6. Mise à jour du endpoint `/api/agent/` (doc)

Ajouter les nouveaux endpoints dans la doc auto-générée.

## Credentials Notion

- API Key : lire depuis `/home/gilles/.openclaw/credentials/notion`
- Base TÂCHES : `304ddac9-bdfc-8130-81de-ef1b4413acc6`
- Notion-Version : `2022-06-28`

## Priorité d'implémentation

1. **Table SQLite + CRUD endpoints** (30 min)
2. **`/tasks/today`** (15 min)
3. **`/morning` briefing** (30 min)
4. **Sync Notion** — import initial + sync sur write (45 min)
5. **Vue dashboard** (si temps)

## Tests attendus

```bash
# Créer une tâche
curl -s -X POST -H "X-API-Key: 0d4ebb779ab550255e1f39f3384d22816bdd58e3b7d6a92780ceded81688c5d3" \
  -H "Content-Type: application/json" \
  -d '{"titre":"Relancer Valérie solde 1700€","priorite":"Haute","assignee":"Léa","deadline":"2026-03-20","clientId":22}' \
  http://127.0.0.1:3001/api/agent/tasks

# Tâches du jour
curl -s -H "X-API-Key: 0d4ebb779ab550255e1f39f3384d22816bdd58e3b7d6a92780ceded81688c5d3" \
  http://127.0.0.1:3001/api/agent/tasks/today

# Briefing matin
curl -s -H "X-API-Key: 0d4ebb779ab550255e1f39f3384d22816bdd58e3b7d6a92780ceded81688c5d3" \
  http://127.0.0.1:3001/api/agent/morning

# Sync Notion
curl -s -X POST -H "X-API-Key: 0d4ebb779ab550255e1f39f3384d22816bdd58e3b7d6a92780ceded81688c5d3" \
  http://127.0.0.1:3001/api/agent/tasks/sync-notion
```
