# Cahier des charges — Extension Chrome MyBotIA

## 1. Vision produit

Extension Chrome qui ajoute une **sidebar IA** dans le navigateur du client. Le client parle à son collaborateur IA (Lucy, Léa, etc.) directement dans son navigateur. Le collaborateur peut **voir la page** en cours et **agir dessus** (remplir, cliquer, extraire).

**Référence UX :** Extension Claude pour Chrome (sidebar) + Comet de Perplexity (navigation IA)

---

## 2. Fonctionnalités MVP

### 2.1 Sidebar chat
- Icône MyBotIA dans la barre d'extensions Chrome
- Clic → **sidebar** qui s'ouvre à droite (panel latéral Chrome Side Panel API)
- Chat en temps réel avec le collaborateur IA assigné au client
- Historique des messages (session persistante)
- Indicateur "en train d'écrire..."
- Support markdown dans les réponses

### 2.2 Contexte page
- Le collaborateur IA **voit automatiquement** la page active du client :
  - URL courante
  - Titre de la page
  - Contenu texte extrait (DOM simplifié)
  - Screenshot à la demande
- Le client peut dire "résume cette page", "remplis ce formulaire", "trouve le bouton X"

### 2.3 Actions navigateur (Phase 2)
- Le collaborateur peut **agir sur la page** avec l'accord du client :
  - Remplir des champs de formulaire
  - Cliquer sur des éléments
  - Naviguer vers une URL
  - Extraire des données structurées
- **Indicateur visuel** quand le collaborateur agit (highlight des éléments touchés)
- Le client voit en temps réel ce qui se passe

---

## 3. Architecture technique

### 3.1 Stack
```
Extension Chrome (Manifest V3)
├── popup.html          → Bouton rapide + statut connexion
├── sidepanel.html      → Interface chat principale (Side Panel API)
├── content-script.js   → Injecté dans les pages → lecture DOM + actions
├── background.js       → Service worker → connexion WebSocket gateway
└── assets/             → Logo MyBotIA, icônes, styles
```

### 3.2 Communication
```
Navigateur client
  ├── content-script.js ←→ sidepanel.html (chrome.runtime messages)
  └── background.js ←→ Gateway OpenClaw (WebSocket wss://app.mybotia.com)
                              ↓
                        Agent IA (Léa, Lucy, etc.)
```

### 3.3 Connexion à OpenClaw
- **WebSocket** vers `wss://app.mybotia.com` (gateway existante)
- **Authentification** : token client (généré lors de l'onboarding)
- **Protocole** : même protocole webchat OpenClaw existant
- L'extension est un **nouveau canal** (type: "chrome-extension") qui se comporte comme le webchat mais avec le contexte page en plus

### 3.4 Permissions Chrome requises
```json
{
  "permissions": [
    "sidePanel",
    "activeTab",
    "tabs",
    "storage"
  ],
  "host_permissions": [
    "https://app.mybotia.com/*"
  ]
}
```

---

## 4. Design / Branding

### 4.1 Identité visuelle
- **Nom extension :** MyBotIA — Collaborateur IA
- **Icône :** Logo MyBotIA (le robot bleu existant, 128x128 + 48x48 + 16x16)
- **Couleurs :** Thème sombre (#09090b fond, #3b82f6 accent bleu, #f8fafc texte)
- **Pas de mention OpenClaw** — c'est un produit MyBotIA

### 4.2 Sidebar
- Header : logo MyBotIA + nom du collaborateur connecté + pastille verte "en ligne"
- Zone chat : messages avec avatars (client à droite, collaborateur à gauche)
- Input : champ texte + bouton envoyer + bouton micro (futur)
- Footer : "Propulsé par MyBotIA" discret

### 4.3 Popup (clic sur icône quand sidebar fermée)
- Statut connexion (connecté/déconnecté)
- Bouton "Ouvrir la sidebar"
- Bouton "Se connecter" (si pas authentifié)
- Lien vers app.mybotia.com

---

## 5. Setup pré-requis (Comet / Gilles)

### 5.1 Compte Google Developer
1. Aller sur https://chrome.google.com/webstore/devconsole/
2. Se connecter avec **coachdigitalparis@gmail.com**
3. Payer les 5$ de frais d'inscription développeur
4. Accepter les conditions développeur

### 5.2 Informations à renseigner
- **Nom développeur :** Coach Digital Paris
- **Email contact :** coachdigitalparis@gmail.com
- **Site web :** https://mybotia.com
- **Politique de confidentialité :** https://mybotia.com/privacy (à créer)
- **Description :** "MyBotIA ajoute un collaborateur IA intelligent à votre navigateur. Posez des questions, faites remplir des formulaires, résumez des pages — votre assistant professionnel est toujours à portée de clic."

### 5.3 Assets à préparer
- Logo 128x128 PNG (fond transparent)
- Screenshot 1280x800 de la sidebar en action (mockup)
- Bannière promotionnelle 440x280

### 5.4 Page privacy policy
- Créer https://mybotia.com/privacy
- Contenu minimal requis : quelles données l'extension collecte (URL de page, contenu texte), où elles sont envoyées (serveurs MyBotIA), pas de revente à des tiers

---

## 6. Développement (Claude Code / Julian)

### 6.1 Phase 1 — MVP Chat (3-5 jours)
- [ ] Structure Manifest V3
- [ ] Side Panel avec chat fonctionnel
- [ ] Connexion WebSocket à la gateway OpenClaw
- [ ] Authentification par token
- [ ] Envoi/réception messages en temps réel
- [ ] Design MyBotIA (thème sombre)
- [ ] Popup avec statut connexion

### 6.2 Phase 2 — Contexte page (2-3 jours)
- [ ] Content script : extraction URL + titre + DOM simplifié
- [ ] Envoi automatique du contexte page au collaborateur
- [ ] Screenshot de la page active
- [ ] Commandes : "résume cette page", "que vois-tu ?"

### 6.3 Phase 3 — Actions navigateur (3-5 jours)
- [ ] Content script : remplissage formulaire
- [ ] Content script : clic sur élément
- [ ] Content script : navigation
- [ ] Highlight visuel des actions
- [ ] Confirmation client avant action

### 6.4 Phase 4 — Polish & publication (2 jours)
- [ ] Tests multi-sites
- [ ] Gestion erreurs/reconnexion
- [ ] Publication Chrome Web Store
- [ ] Documentation utilisateur

---

## 7. Comptes et accès

| Service | Compte | Usage |
|---------|--------|-------|
| Chrome Web Store Developer | coachdigitalparis@gmail.com | Publication extension |
| Gateway OpenClaw | wss://app.mybotia.com | Backend IA |
| GitHub | github.com/eddigit | Repo code extension |

---

## 8. Livrables

1. **Extension Chrome** fonctionnelle installable
2. **Page Chrome Web Store** avec description, screenshots, branding
3. **Page privacy policy** sur mybotia.com
4. **Documentation** : guide d'installation client + guide technique

---

## 9. Timeline estimée

| Semaine | Livrable |
|---------|----------|
| S1 | MVP chat sidebar + connexion gateway |
| S2 | Contexte page + actions basiques |
| S3 | Polish + publication Chrome Web Store |

---

*Rédigé par Léa — 1er avril 2026*
*Pour exécution : Comet (setup Google) + Claude Code (développement)*
