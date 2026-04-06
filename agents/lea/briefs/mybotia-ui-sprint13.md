# Brief Technique — MyBotIA UI Sprint 13
## Améliorations Interface Chat

**Demandé par** : Gilles (CEO) + Léa (suivi)
**Exécuté par** : Jules (Claude Code)
**Date** : 22 mars 2026
**Priorité** : Haute

---

## Contexte

Interface actuelle : `/var/www/html/mybotia/public/`
- `index.html` — structure HTML
- `css/style.css` → compilé en `css/style.min.css`
- `js/app.js` → compilé en `js/app.min.js`
- Version actuelle : v12-15 (footer) / v12-17 (CSS) / v12-18 (JS)

---

## 3 Améliorations à implémenter

### 1. Activité temps réel dans l'indicateur typing + animation sources bar

**Actuellement** : Quand l'agent réfléchit, on affiche juste "Léa réfléchit..."
**Objectif** : Afficher ce que l'agent fait en temps réel

**Implémentation :**
- Le WebSocket envoie déjà des événements de type tool_use / thinking. Intercepter ces événements dans app.js
- Quand un outil est utilisé, mettre à jour le texte du typing indicator (#typing-name + label) :
  - Recherche Judilibre → "🔍 Recherche sur Judilibre..."
  - Recherche Légifrance → "📖 Consultation Légifrance..."
  - Lecture emails → "📧 Lecture des emails..."
  - Consultation Qonto → "💰 Consultation bancaire..."
  - Recherche web → "🌐 Recherche en cours..."
  - Notion → "📋 Consultation Notion..."
  - WhatsApp → "💬 Envoi WhatsApp..."
  - Défaut (thinking) → "💭 Réflexion en cours..."
- **Animation sources bar** : Quand un outil est utilisé, faire pulser la chip correspondante dans .sources-bar
  - Ajouter une classe `.source-chip.active-pulse` avec une animation glow/pulse de 2s
  - La retirer quand l'outil a fini

**CSS nécessaire :**
```css
.source-chip.active-pulse {
  animation: sourcePulse 1.5s ease-in-out infinite;
}
.source-chip.active-pulse .source-dot {
  box-shadow: 0 0 8px 2px currentColor;
}
@keyframes sourcePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.85; transform: scale(1.05); }
}
```

### 2. Avatar agent dans les bulles de messages + groupement messages consécutifs

**Actuellement** : Les bulles assistant n'ont pas d'avatar, juste couleur différente
**Objectif** : Afficher l'avatar miniature de l'agent à côté de ses messages (comme WhatsApp/ChatGPT)

**Implémentation :**
- Dans app.js, quand on crée un message assistant, ajouter un élément avatar avant la bulle :
```html
<div class="msg assistant">
  <div class="msg-row">
    <div class="msg-avatar"><img src="[avatar_url]" alt=""></div>
    <div class="msg-content">
      <div class="msg-bubble">...</div>
      <div class="msg-time">...</div>
    </div>
  </div>
</div>
```
- L'avatar URL est déjà disponible via la config agent (header-avatar l'utilise déjà)
- **Groupement** : Si le message précédent est du même auteur, masquer l'avatar et réduire le gap
  - Ajouter classe `.msg.grouped` quand le précédent est du même auteur
  - `.msg.grouped .msg-avatar { visibility: hidden; }` (garder l'espace pour l'alignement)
  - `.msg.grouped { margin-top: -4px; }` (rapprocher les bulles groupées)

**CSS nécessaire :**
```css
.msg-row {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}
.msg-avatar {
  width: 28px;
  min-width: 28px;
  height: 28px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}
.msg-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.msg.user .msg-row {
  flex-direction: row-reverse;
}
.msg.user .msg-avatar {
  display: none; /* pas d'avatar pour l'utilisateur */
}
.msg.grouped .msg-avatar {
  visibility: hidden;
}
.msg.grouped {
  margin-top: -4px;
}
.msg-content {
  min-width: 0;
  max-width: 100%;
}
```

### 3. Panneau Usage mensuel (Paramètres)

**Actuellement** : Le bouton "Usage mensuel" dans le menu compte existe mais n'a pas de panneau
**Objectif** : Créer un panneau overlay (comme profile-panel et settings-panel) avec les stats d'usage

**Implémentation :**
- Créer un panneau `#usage-panel` avec la même structure que `#profile-panel`
- Contenu :
  - **Barre de quota** grande et visible avec code couleur (vert > 50%, orange 20-50%, rouge < 20%)
  - **Tokens utilisés / Total** avec pourcentage
  - **Estimation** : "≈ X messages restants" (calculer moyenne tokens par message)
  - **Période** : "Mois en cours : 1er mars - 31 mars 2026"
  - **Historique** : mini graphique en barres des 7 derniers jours (CSS pur, pas de lib)
  - **Version** : Afficher "V.12-XX" en bas du panneau (pour futur déplacement du footer)
- Le bouton `#menu-usage` dans le menu compte doit ouvrir ce panneau
- Les données de tokens sont déjà dans `#credits-value` — les réutiliser

**HTML structure :**
```html
<div class="usage-overlay" id="usage-overlay"></div>
<div class="usage-panel" id="usage-panel">
  <div class="usage-panel-header">
    <h3>Usage mensuel</h3>
    <button class="usage-panel-close" id="usage-panel-close">&times;</button>
  </div>
  <div class="usage-panel-body">
    <div class="usage-quota-section">...</div>
    <div class="usage-history-section">...</div>
  </div>
  <div class="usage-panel-footer">V.12-XX</div>
</div>
```

---

## Règles techniques

1. **TOUJOURS faire un backup avant modif** : `cp file file.bak-$(date +%Y%m%d-%H%M%S)`
2. **Minifier après modif** :
   - CSS : vérifier comment style.min.css est généré (probablement simple concat/minify)
   - JS : vérifier comment app.min.js est généré
3. **Versionner** : incrémenter les `?v=v12-XX` dans les balises link/script de index.html
4. **Tester** : Vérifier que le dark mode fonctionne pour tout ce qui est ajouté
5. **Ne PAS toucher** aux fichiers .bak-*

## Ordre d'exécution

1. Backup de tous les fichiers
2. Amélioration 1 (typing + sources bar animation)
3. Amélioration 2 (avatar + groupement)
4. Amélioration 3 (panneau usage)
5. Minification
6. Test visuel (vérifier que rien n'est cassé)
