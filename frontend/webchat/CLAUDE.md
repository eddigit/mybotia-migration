# CLAUDE.md — Règles MyBotIA pour Claude Code (CTO)

> **Dernière mise à jour : 22 mars 2026 18h30 — par Léa — V.14.0**

## 🔴 RÈGLE CSS ABSOLUE — NE JAMAIS VIOLER

L'interface MyBotIA utilise **DEUX fichiers CSS source** :
1. `public/css/style.css` — styles généraux (sidebar, chat, messages, usage-panel, streaming, animations, etc.)
2. `public/css/style-v12.css` — styles du panneau Outils (right-sidebar, rs-*, CRM, tâches, etc.)

Le fichier chargé par le navigateur est `public/css/style.min.css` qui est la **combinaison minifiée des deux**.

### Après TOUTE modification CSS :
```bash
bash public/css/rebuild-css.sh
```
Puis bumper le cache-buster dans `public/index.html` :
```
style.min.css?v=vXX-YY  →  incrémenter YY
```

### ❌ INTERDIT
- Minifier `style.css` seul (oublie style-v12.css → panneau Outils cassé)
- Écraser `style.min.css` avec seulement un des deux fichiers
- Utiliser `csso` directement sur un seul fichier source
- Créer des fichiers .bak — on a un système de backup centralisé dans `backups/`
- **Tu as déjà cassé le panneau Outils 3 FOIS en oubliant cette règle. Plus jamais.**

### Après modification JS :
```bash
npx --yes terser public/js/app.js -o public/js/app.min.js
```
Même chose pour tools-panel.js si modifié :
```bash
npx --yes terser public/js/tools-panel.js -o public/js/tools-panel.min.js
```

## Structure des fichiers (V.14.0 — nettoyée)

```
public/
├── index.html              ← HTML principal (cache-busters + version ici)
├── css/
│   ├── style.css           ← Source CSS 1 (NE PAS SUPPRIMER)
│   ├── style-v12.css       ← Source CSS 2 (NE PAS SUPPRIMER)
│   ├── style.min.css       ← COMBINAISON minifiée des 2 (auto-généré)
│   └── rebuild-css.sh      ← Script de rebuild (UTILISER APRÈS CHAQUE MODIF CSS)
├── js/
│   ├── app.js              ← Source JS principal (~222 KB)
│   ├── app.min.js          ← Minifié (~160 KB, auto-généré)
│   ├── tools-panel.js      ← Source JS panneau outils
│   └── tools-panel.min.js  ← Minifié (auto-généré)
backups/
└── pre-cleanup-2026-03-22.tar.gz  ← Archive de tous les anciens .bak
```

⚠️ **PAS de fichiers .bak** — tout est propre. Si tu veux sauvegarder avant une grosse modif :
```bash
tar czf backups/pre-DESCRIPTION-$(date +%Y%m%d).tar.gz public/css/style.css public/css/style-v12.css public/js/app.js public/js/tools-panel.js public/index.html
```

## 🎨 Fonctionnalités UX en place (V.14.0 — 22 mars 2026)

### 1. Indicateur "Réfléchit..." avec logo animé
- **Fichier** : `index.html` ligne ~269
- L'indicateur de typing utilise le **logo Collaborateur IA** (SVG Cloudinary) avec un **heartbeat lumineux violet**
- Animation CSS : `typing-logo-glow` dans `style.css`
- Se déclenche via `showTyping()` dans `app.js`

### 2. Avatar streaming pulse dans le chat
- L'avatar de l'agent **pulse dans la bulle de streaming** (pas dans le header/sidebar)
- Structure : `.streaming-row` > `.streaming-avatar` + `.streaming-content`
- Animation : `chat-avatar-pulse` (violet, scale 1→1.1)
- Déclenché par `setGenerating(true)` qui ajoute `.working` à `#streaming-avatar`

### 3. Tool steps — actions visibles dans le chat
- Chaque action s'affiche comme une étape dans le chat (style Claude)
- Dot violet qui pulse = en cours, ✓ vert = terminé
- Labels avec emojis : 📄 Lecture, ⚡ Commande, 📧 Email, 📋 Notion, etc.
- Container `.tool-steps` avec étapes `.tool-step` empilées
- Disparaît en fondu (`.fade-out`) quand la réponse finale arrive

### 4. Étapes progressives pendant le travail agent
- OpenClaw ne streame PAS les tool_use au client → étapes simulées basées sur le timing
- `lifecycle.start` déclenche un timer (3s intervals) :
  - 🧠 Analyse de la demande...
  - 🔍 Recherche d'informations...
  - ⚡ Exécution des actions...
  - 📝 Rédaction de la réponse...
- Le timer s'arrête dès que le premier texte arrive

### 5. Indicateur d'activité pendant les tool calls
- Quand le streaming est en cours mais qu'aucun nouveau texte n'arrive pendant **3 secondes**, une barre de progression animée + label "En cours..." apparaît
- La classe `.working` est ajoutée à `.streaming-bubble`
- **NE PAS SUPPRIMER**

### 6. Streaming fluide (anti-saccade)
- Le texte streaming est **bufferisé 350ms** avant rendu
- Animation CSS `stream-text-in` : fondu 0.25s sur les nouveaux éléments
- Résultat : des phrases complètes apparaissent fluidement

### 7. Escape stoppe la génération
- `document.addEventListener('keydown')` — Escape appelle `abortChat()` si `_isGenerating === true`

### 8. Reconnexion WS restaure l'indicateur
- Variable `_isGenerating` track l'état de génération
- Sur reconnexion WebSocket, si `_isGenerating` est true → `showTyping()` est rappelé

### 9. Session active — surbrillance visible
- Barre violette à gauche (`border-left: 3px solid #6366f1` + pseudo `::before`)
- Titre en blanc + gras
- Auto-expand : si la session active est dans un dossier/section fermée, ça s'ouvre automatiquement
- Auto-scroll vers la session active au chargement

### 10. Section Dossiers collapsible
- Header "DOSSIERS" avec chevron cliquable
- Couleur titre : `#88D4FD`
- État persisté en localStorage

### 11. Titres sidebar en #88D4FD
- "DOSSIERS" et "30 DERNIERS JOURS" en `#88D4FD` (bleu clair)
- Séparation subtile (`border-bottom: 1px solid rgba(136, 212, 253, 0.2)`)

### 12. Events OpenClaw — format réel
Le WebSocket envoie des events `agent` (PAS `chat` pour le streaming) :
- `stream: "lifecycle"` → `data.phase: "start"` / `"end"`
- `stream: "assistant"` → `data.text` (accumulé) + `data.delta` (nouveau)
- **Les tool_use ne sont PAS streamées au client** — c'est pour ça qu'on utilise les étapes simulées

## ⚠️ Variables JS critiques (app.js)

| Variable | Usage |
|----------|-------|
| `_isGenerating` | true quand l'agent travaille — utilisé partout |
| `_streamLastDelta` | Timestamp du dernier delta reçu — détection tool calls |
| `_streamActivityTimer` | Timer pour afficher "En cours..." après 3s sans delta |
| `_agentWorkingTimer` | Timer pour les étapes progressives (🧠→🔍→⚡→📝) |
| `_agentWorkingSteps` | Compteur d'étapes affichées |
| `_streamRawText` | Texte brut accumulé du streaming |
| `_toolStepsEl` | Container DOM des tool steps |

**NE PAS renommer ou supprimer ces variables.**

## Checklist OBLIGATOIRE avant de dire "c'est déployé"

- [ ] `bash public/css/rebuild-css.sh` exécuté
- [ ] `npx --yes terser public/js/app.js -o public/js/app.min.js` exécuté
- [ ] Cache-buster incrémenté dans `index.html` (CSS + JS)
- [ ] Version V.XX.X mise à jour dans `index.html` (footer + usage-panel-footer)
- [ ] Hard refresh (Ctrl+Shift+R) fait par toi-même
- [ ] Panneau Outils s'ouvre correctement
- [ ] Sidebar fonctionne (dossiers, sessions, WhatsApp)
- [ ] Usage panel se ferme/ouvre correctement
- [ ] Indicateur "réfléchit" visible quand l'agent travaille
- [ ] Étapes progressives apparaissent pendant le travail
- [ ] Streaming fluide (pas de saccade lettre par lettre)
- [ ] Bouton Stop et Escape fonctionnent
- [ ] Session active visible avec barre violette

## 🚫 NE PAS TOUCHER sans raison

- L'indicateur typing (logo pulse + "réfléchit...")
- Le système de streaming bufferisé (350ms)
- Les timers `_streamActivityTimer` et `_agentWorkingTimer`
- La reconnexion WS + restauration typing
- Les animations CSS (`typing-logo-glow`, `stream-text-in`, `activity-slide`, `chat-avatar-pulse`)
- La structure `.streaming-row` > `.streaming-avatar` + `.streaming-content`

Si tu dois modifier un de ces éléments, **explique pourquoi** et **vérifie que tout fonctionne après**.

## Source de vérité

- **PostgreSQL** (via admin.mybotia.com API) est la source de vérité pour les données business
- **Notion** est synchronisé depuis PostgreSQL, pas l'inverse
- Pour créer/modifier projets, tâches, clients → utiliser l'API admin.mybotia.com
