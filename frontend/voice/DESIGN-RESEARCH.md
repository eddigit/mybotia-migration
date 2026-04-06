# Chat/Messaging UI Design Research — 2025-2026

Document de reference pour la refonte UI du Voice POC et des futures interfaces chat MyBotIA.
Recherche effectuee le 28 mars 2026.

---

## 1. LAYOUT PATTERNS

### 1.1 Structure dominante chez les grands acteurs

**ChatGPT** : Sidebar collapsible a gauche (conversations + GPTs) + zone chat centrale. Nouveau : la sidebar "hover & soft dismiss" — elle se superpose au contenu et disparait doucement quand inutilisee. Sidebar toujours en bas : settings. Navigation style Arc browser (vertical tabs).

**Claude** : Design minimaliste deux colonnes — sidebar gauche (conversations + Projects) + zone chat principale. Accents violets. Feature distinctive : "Artifacts" — panneau dedie a droite pour le contenu genere (code, sites, diagrammes), eliminant le copier-coller.

**Gemini** : Approche "portail" — s'integre en overlay dans les apps Google (Gmail, Sheets) plutot qu'interface standalone. Material Design, Google Sans, accents bleus.

**Perplexity** : Affiche des exemples de prompts immediatement a l'ouverture, zero onboarding.

### 1.2 Pattern emergent 2026 : Panneaux Glassmorphism sur base sombre

La tendance dominante pour les apps IA en 2026 est :
- Base sombre (true black ou near-black)
- Panneaux translucides givres (frosted glass) superposes pour les zones de reponse IA
- La base sombre reduit la fatigue oculaire
- Le panneau translucide cree une separation visuelle sans bord rigide

### 1.3 Recommandations layout

| Zone | Pattern |
|------|---------|
| Sidebar | Collapsible, max 15 conversations pinnees, categorisation intelligente |
| Chat area | Centree, largeur max contrainte (600-800px), scroll infini |
| Input | Fixe en bas, pleine largeur de la zone chat |
| Panneau secondaire | A droite pour artifacts/details (Claude-style) |
| Header | Minimal — nom agent + status + toggle settings |

---

## 2. TYPOGRAPHY

### 2.1 Regles generales

- **Police** : Inter (deja standard MyBotIA), Soehne (ChatGPT), Google Sans (Gemini)
- **Weights** : 300 (light/secondaire), 400 (body), 500 (emphasis), 600 (headings)
- **Unites** : REM pour font-size, padding, margins (respect zoom navigateur). PX uniquement pour borders et shadows
- **Taille body** : 1rem (16px base), messages 0.9375rem (15px)
- **Line-height** : 1.5 a 1.6 pour le body, 1.3 pour les headings
- **Letter-spacing** : 0.01em pour le texte en streaming (meilleure lisibilite caractere par caractere)

### 2.2 Dark mode specifique

- Poids legerement plus lourd qu'en light mode (400 au lieu de 300 pour le body)
- Espacement legerement augmente pour meilleure lisibilite sur fond sombre
- Texte off-white (#E8E8F0 ou #D4D4E8) — jamais blanc pur sur fond sombre
- Tester le rendu sur differents ecrans (anti-aliasing varie)

### 2.3 Code et contenu structure

- Blocs monospaces avec coloration syntaxique
- Bouton copier sur chaque bloc code
- Panneaux expandables pour contenu long (style Artifacts Claude)

---

## 3. COULEURS ET DARK MODE

### 3.1 Dark mode = standard en 2026

82% des utilisateurs ont le dark mode active. Ce n'est plus une feature request — c'est le defaut.

### 3.2 Palette de reference (compatible charte MyBotIA)

| Role | Valeur | Notes |
|------|--------|-------|
| Base background | #0A0A1A | Charte MyBotIA existante |
| Surface / cards | #12122A | Charte MyBotIA existante |
| Surface elevated | #1A1A2E | Standard industrie 2026 |
| Accent primaire | #8B5CF6 | Violet MyBotIA |
| Accent indigo IA | #6366F1 | Tendance 2026 pour identite IA |
| Texte primaire | #F1F5F9 | Off-white, pas blanc pur |
| Texte secondaire | #94A3B8 | Gris clair |
| Texte tertiaire | #475569 | Gris moyen |
| Bordures subtiles | rgba(255,255,255,0.1) | 1px, quasi invisible |
| Erreur | Rouge high-contrast | Bold, jamais couleur seule |
| Succes/confiance | Vert | Pour indicateurs de confiance IA |

### 3.3 Glassmorphism 2.0 (tendance 2026)

```css
/* Pattern recommande pour panneaux IA */
backdrop-filter: blur(12px) to blur(20px);
background: rgba(255, 255, 255, 0.08) to rgba(255, 255, 255, 0.15);
border: 1px solid rgba(255, 255, 255, 0.1);
```

- Apple a adopte ce style ("Liquid Glass") pour tous ses OS a WWDC 2025
- Ideal pour : modals, panneaux de reponse IA, sidebars, overlays
- A utiliser selectivement — c'est un outil, pas un style global

### 3.4 Contraste et accessibilite

- WCAG minimum : 4.5:1 pour texte normal, 3:1 pour texte large
- Dark grey (#121212) au lieu de noir pur — economie 67% batterie OLED
- Ombres douces, pas de drop shadows traditionnels
- Ne jamais s'appuyer uniquement sur la couleur pour les alertes

---

## 4. MICRO-INTERACTIONS ET ANIMATIONS

### 4.1 Animations d'etat IA (pattern 2026)

| Etat | Animation | Duree |
|------|-----------|-------|
| Processing/thinking | Pulse subtil sur le panneau reponse | 100-300ms |
| Streaming texte | Typewriter effet + curseur clignotant 2px | 500ms blink |
| Generation contenu | Expansion hauteur progressive | smooth |
| Confiance update | Transition couleur (ambre → vert) | 200ms |
| Dismiss/fermeture | Fade-out doux | 150-200ms |
| Chargement | Skeleton loading (3-5 lignes, largeurs decroissantes) | shimmer continu |

### 4.2 Impact mesure

- Typewriter effect : reduit le temps d'attente percu de 55-70%
- Skeleton loading : reduit le temps de charge percu de 40% vs spinners
- Streaming SSE/WebSocket : le texte apparait caractere par caractere

### 4.3 Animations vocales

- Waveform audio : 100 points de donnees pour un affichage optimal
- 3 etats visuels : enregistrement, pause, arret
- Feedback en temps reel pendant l'enregistrement
- Transitions d'etat fluides entre les modes

---

## 5. MESSAGE BUBBLES ET CONVERSATION

### 5.1 Design des bulles

| Propriete | Valeur recommandee |
|-----------|--------------------|
| Padding | 20px top, 10px sides, 15px bottom |
| Coins arrondis | 8-16px (preference utilisateurs vs angles droits) |
| Largeur min | 180px |
| Largeur max | 70-80% de la zone chat |
| Espacement entre bulles | 8-12px meme auteur, 16-20px auteurs differents |
| Alignement | Gauche = IA/bot, Droite = utilisateur |

### 5.2 Couleurs des bulles

- **Bulles utilisateur** : accent color (violet #8B5CF6 ou indigo #6366F1) avec texte blanc
- **Bulles IA** : surface elevated (#1A1A2E) avec texte off-white
- Bulles bleu fonce + texte blanc = 90% meilleure lisibilite que combinaisons claires

### 5.3 Groupement et horodatage

- Regrouper les messages consecutifs du meme auteur (pas de repetition avatar/nom)
- Timestamp discret (texte tertiaire, petite taille) — au survol ou toutes les 5 minutes
- Indicateur de frappe : animation toutes les 2 secondes
- Etats de livraison : icones distinctes pour envoye, recu, lu

### 5.4 Avatars

- Position : a gauche de la bulle pour l'IA, a droite ou absent pour l'utilisateur
- Taille : 32-40px, coins arrondis complets (cercle)
- Afficher uniquement sur le premier message d'un groupe
- Avatar IA avec identite visuelle forte (couleur d'accent, icone ou photo)

---

## 6. INPUT AREA

### 6.1 Patterns d'entree

- **Position fixe en bas** : standard, 40% de temps de reponse plus rapide
- **Zone extensible** : s'agrandit avec le contenu (textarea auto-resize)
- **Texte predictif** : reduit le temps de frappe de 33%
- **Bouton micro** : persistent dans la barre d'action (voice-first growing 65%/an)
- **Boutons suggestion** : 5 max, texte 20 caracteres max, jusqu'a 13 quick replies visibles

### 6.2 Composition de la zone input

```
[Attachments/+] [Zone de texte extensible] [Micro] [Envoyer]
```

- Bouton d'envoi : accent color, apparait quand texte non vide
- Bouton micro : icone claire, feedback visuel pendant enregistrement
- Zone texte : placeholder descriptif ("Posez votre question a Lea...")
- Raccourci clavier : Enter pour envoyer, Shift+Enter pour nouvelle ligne

### 6.3 Suggestions et chips

- Afficher des suggestion chips au-dessus de l'input quand la conversation est vide
- Chips cliquables avec formulation naturelle
- Disparaissent apres le premier message
- Slash commands (style Slack/Discord) pour les utilisateurs avances

---

## 7. EMPTY STATES ET ONBOARDING

### 7.1 Principes cles 2026

- **Zero onboarding** : le produit s'enseigne lui-meme par l'usage
- **Exemples larges > exemples niches** : "Aide-moi a rediger un email" > "Genere un haiku sur les chats"
- **Valeur en secondes** : Perplexity montre des prompts immediatement, zero guide
- **Try-before-signup** : 40% des outils IA permettent d'essayer sans inscription

### 7.2 Design de l'empty state

| Element | Implementation |
|---------|----------------|
| Message d'accueil | Court, personnalise ("Bonjour Gilles, comment puis-je vous aider ?") |
| Avatar agent | Centre, grande taille (80-120px), avec nom et role |
| Exemples de prompts | 3-4 cartes cliquables, formulations concretes |
| Capacites | Liste courte de ce que l'agent sait faire (3-5 items) |
| Ton | Conversationnel, chaleureux, pas technique |

### 7.3 Anti-patterns

- Popups tutoriels (confondus avec des pubs, dismiss immediat)
- Longues listes de features (surcharge cognitive)
- Onboarding generique non lie au contexte
- Assistant "universel" sans perimetre clair defini

### 7.4 Pattern ChatGPT

ChatGPT affiche "des exemples generaux perspicaces qui demontrent ses capacites, avec une phrase detaillee servant d'inspiration."

### 7.5 Pattern Claude

Claude introduit le pricing tot avec un ton de "discussion amicale" plutot que du gatekeeping. Signup en 3-5 questions personnalisees (use case, role, objectifs).

---

## 8. VOICE-FIRST PATTERNS

### 8.1 Croissance

Usage voice dans les apps IA : +65% par an. Sur mobile, la voix devient le mode d'entree principal pour un segment croissant et significatif.

### 8.2 Elements UI obligatoires

- Bouton micro persistent dans la barre d'action principale
- Animation waveform visuelle pendant l'ecoute
- Transcription instantanee dans le champ texte pendant que l'utilisateur parle
- Reponses audio IA distinctes visuellement
- Gestion gracieuse des interruptions

### 8.3 Feedback etats vocaux

| Etat | Feedback visuel |
|------|-----------------|
| Idle | Icone micro statique |
| Listening | Waveform animee + indicateur couleur |
| Processing STT | Animation de transcription |
| AI thinking | Pulse/breathing animation ou son ambiance |
| AI speaking | Waveform lecture + controles playback |
| Error | Icone erreur + message court |

---

## 9. MOBILE-FIRST

### 9.1 Patterns dominants

- **Sidebar cachee** : accessible par swipe ou hamburger, pas visible par defaut
- **Bottom navigation** : Home, Feed, Saved, etc.
- **Touch targets** : minimum 44x44px (Apple HIG) / 48x48px (Material Design)
- **Chat-centric** : tout l'ecran est conversation, elements secondaires caches
- **Scroll vertical** : methode principale de navigation contenu

### 9.2 Adaptation responsive

- ChatGPT : menu collapsible, gros boutons micro/image optimises tactile
- Claude : sidebar masquable, acces offline aux conversations recentes
- Gemini : overlays contextuels, integration Android intents, partage ecran voice mode

### 9.3 Contraintes MyBotIA

- Max-width widget : 420px (charte existante)
- Espacements multiples de 4px
- Arrondis : 8px, 16px, 9999px (pills)
- Icones Phosphor Thin exclusivement

---

## 10. ACCESSIBILITE

### 10.1 Standards obligatoires

- **ARIA live regions** : `aria-live="polite"` sur les containers de reponse IA
- **role="status"** sur les indicateurs de chargement
- **Focus keyboard** : gestion du focus vers la reponse IA quand complete
- **Alt text** : descriptif sur icones de confiance et images generees par IA
- **Tester avec** : VoiceOver (iOS/macOS), NVDA (Windows)

### 10.2 Dark mode accessible

- Support niveaux de luminosite ajustables
- Etats de focus clavier visibles
- Navigation clavier complete
- Ne pas s'appuyer uniquement sur la couleur pour differencier les alertes
- Respecter les preferences systeme (prefers-color-scheme)

### 10.3 Contraste et lisibilite

- WCAG 2.1 AA minimum : 4.5:1 texte normal, 3:1 texte large
- Indicateurs de statut : couleur + forme + texte (triple codage)
- Labels corrects pour les lecteurs d'ecran (Claude cite en exemple)
- Taille texte minimum 14px, idealement 16px

---

## 11. TENDANCES VISUELLES 2026

### 11.1 Glassmorphism 2.0

- Evolue de tendance a outil de design
- Apple "Liquid Glass" (WWDC 2025) — adoption mainstream
- Ideal pour panneaux IA, modals, overlays
- Necessite un fond colore/image pour fonctionner visuellement
- A utiliser selectivement et avec intention

### 11.2 Neumorphism

- Ombres douces + highlights pour un aspect "extrude du fond"
- Mieux adapte aux boutons et controles interactifs
- Problemes d'accessibilite significatifs — contraste difficile
- Necessite beaucoup plus de soin que le glassmorphism
- Usage recommande : boutons d'action sur panneaux glassmorphiques

### 11.3 Dark mode comme baseline

- 82% des utilisateurs l'activent
- Defaut pour toutes les apps IA
- "Low light aesthetic" — evolution du dark mode classique
- System-aware switching (respecter les prefs OS)
- Toggle manuel toujours accessible

### 11.4 Intelligence ambiante

- L'app adapte layout, suggestions, emphase sans config utilisateur
- Widget rearrangement dynamique, ajustement de ton
- Pattern : changements visibles, reversibles, explicables
- Label "Personnalise pour vous" + bouton "Retour aux defauts"

### 11.5 Indicateurs de confiance IA

- Signaux visuels montrant la certitude de l'IA
- Badges pourcentage, citations sources, bordures color-coded
- Vert = confiance haute, ambre = moyenne
- Usage selectif la ou les enjeux de precision sont reels

---

## 12. CONFIANCE ET UX CONVERSATIONNELLE

### 12.1 Principes fondamentaux

- L'adoption depend de la confiance et de la clarte, pas juste de la tech
- Toujours informer l'utilisateur qu'il interagit avec une IA
- Acces clair a l'assistance humaine (bouton ou phrase declencheur)
- Les utilisateurs pardonnent les reponses imparfaites si l'interface reconnait les limites

### 12.2 Gestion du contexte

- Conversations multi-tours avec retention de contexte
- "Combien j'ai depense le mois dernier ?" suivi de "Et en restaurants ?" — le systeme doit retenir le timeframe
- Memoire persistante des preferences (Gemini, ChatGPT, Claude Projects)

### 12.3 Reponses naturelles

- Court et direct — personne ne veut lire un roman dans un chat bot
- Ton aligne avec la marque (pro, casual, formel selon le contexte)
- Aller droit au but rapidement

### 12.4 Escalade humaine

- Bouton ou phrase pour transfert vers humain, visible avant que l'utilisateur abandonne
- Systeme de fallback en 3 tentatives pour les incomprehensions

---

## 13. SYNTHESE — PATTERNS PRIORITAIRES POUR MYBOTIA

En croisant les tendances 2025-2026 avec la charte MyBotIA existante :

### Must-have
1. **Dark mode par defaut** avec palette MyBotIA (#0A0A1A / #12122A / #8B5CF6)
2. **Glassmorphism selectif** pour panneaux IA (backdrop-filter blur 12-20px)
3. **Streaming typewriter** avec curseur clignotant (SSE/WebSocket deja en place)
4. **Skeleton loading** a la place des spinners
5. **Empty state actionnable** avec 3-4 prompts cliquables
6. **Input fixe en bas** avec micro persistent (voice-first)
7. **Accessibilite ARIA** sur tous les conteneurs de reponse IA
8. **Inter font** avec weights 300-600 (deja en place)
9. **Phosphor Icons Thin** (deja standard)
10. **Mobile-first** max-width 420px widgets

### Nice-to-have
1. Indicateurs de confiance IA (badge ou bordure coloree)
2. Intelligence ambiante (suggestions adaptatives)
3. Panneau Artifacts lateral (style Claude)
4. Neumorphism sur boutons d'action selectifs
5. Animations micro-etat (pulse, fade, color transitions 100-300ms)

### A eviter
1. Popups tutoriels / onboarding long
2. Blanc pur sur fond sombre (off-white seulement)
3. Noir pur comme fond (#000000)
4. Spinners classiques (utiliser skeletons)
5. Drop shadows lourds en dark mode
6. SVG inline ou emojis pour icones (Phosphor uniquement)
7. Surcharge de features sans hierarchie claire

---

## SOURCES

- [Comparing Conversational AI Tool User Interfaces 2025 | IntuitionLabs](https://intuitionlabs.ai/articles/conversational-ai-ui-comparison-2025)
- [Top 20 Chatbot UI Examples In 2025 | Kaily.ai](https://www.kaily.ai/blog/chatbot-ui-examples)
- [Innovative Chat UI Design Trends 2025 | MultitaskAI](https://multitaskai.com/blog/chat-ui-design/)
- [The 20 best looking chatbot UIs in 2026 | Jotform](https://www.jotform.com/ai/agents/best-chatbot-ui/)
- [UI/UX Design Trends for AI-First Apps in 2026 | GroovyWeb](https://www.groovyweb.co/blog/ui-ux-design-trends-ai-apps-2026)
- [SaaS Design Trends 2026 | JetBase](https://jetbase.io/blog/saas-design-trends-best-practices)
- [Dark Mode Design Best Practices 2026 | Tech-RZ](https://www.tech-rz.com/blog/dark-mode-design-best-practices-in-2026/)
- [60+ Best Chat UI Design Ideas 2026 | Muzli](https://muz.li/inspiration/chat-ui/)
- [16 Chat UI Design Patterns That Work in 2025 | BricxLabs](https://bricxlabs.com/blogs/message-screen-ui-deisgn)
- [New Users Need Support with Generative-AI Tools | NN/g](https://www.nngroup.com/articles/new-AI-users-onboarding/)
- [How Top AI Tools Onboard New Users 2026 | UserGuiding](https://userguiding.com/blog/how-top-ai-tools-onboard-new-users)
- [Conversational UI: 6 Best Practices 2026 | AIMultiple](https://research.aimultiple.com/conversational-ui/)
- [Designing UX for AI Chatbots | ParallelHQ](https://www.parallelhq.com/blog/ux-ai-chatbots)
- [7 New Rules of AI in UX Design 2026 | Millipixels](https://millipixels.com/blog/ai-in-ux-design)
- [Glassmorphism 2025 | Medium/Bootcamp](https://medium.com/design-bootcamp/glassmorphism-the-2015-design-trend-9d1f60d68ba2)
- [Neumorphism vs Glassmorphism | Zignuts](https://www.zignuts.com/blog/neumorphism-vs-glassmorphism)
- [What Is Neumorphism in UI Design 2026 | BigHuman](https://www.bighuman.com/blog/neumorphism)
- [ChatGPT Sidebar Redesign | AI-Toolbox](https://www.ai-toolbox.co/chatgpt-management-and-productivity/chatgpt-sidebar-redesign-guide)
- [AI Onboarding: Activate Users in Under 60 Seconds | ProductLed](https://productled.com/blog/ai-onboarding)
- [Chatbot Design Challenges 2026 | Jotform](https://www.jotform.com/ai/agents/chatbot-design/)
