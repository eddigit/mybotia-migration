# PROMPT CLAUDE CODE — Site de présentation Collaborateur IA pour IGH

## Contexte

Tu es un développeur front-end expert. Tu dois créer un site web de présentation ONE-PAGE, moderne et professionnel, destiné au groupe IGH (SAS IGH — 17 EHPAD + 3 cliniques en France). Ce site présente leur futur collaborateur IA sur mesure.

Ce site est **privé** (pas de login pour l'instant, mais pas référencé, pas de SEO). Il sera partagé uniquement avec M. Imbert (PDG) et M. Cozon (DG délégué) du groupe IGH.

## Stack technique

- **Next.js 14** (App Router)
- **Tailwind CSS** + animations fluides (framer-motion ou CSS natif)
- **TypeScript**
- **Responsive** mobile-first (M. Imbert lira depuis son téléphone)
- **Dark mode** élégant — thème sombre avec accents bleus/verts
- **Pas de backend** — tout est statique
- **Déploiement** : Vercel

## Structure du site (sections dans l'ordre)

### 1. HERO — Accroche
- Titre : "Votre collaborateur IA dédié au groupe IGH"
- Sous-titre : "20 établissements. 1 collaborateur. 0 surprise."
- Animation subtile (particules ou gradient animé)
- CTA : "Découvrir" (scroll vers section suivante)

### 2. LE CONTEXTE — Qui est le groupe IGH
- 20 établissements (17 EHPAD, 3 cliniques)
- Répartis sur tout le territoire (carte interactive ou visuel)
- SAS IGH, société familiale créée en 2001
- Siège : 930 Route de Berre, 13090 Aix-en-Provence
- Visualisation : icônes/chiffres animés (20 établissements, ~1 400 lits, 6 régions)

### 3. LES PROBLÈMES — Ce que vous nous avez dit
Présenter les 6 problèmes identifiés, chacun dans une carte avec icône + description :

**Problème 1 — Pas de visibilité sur la facturation**
80 lits par EHPAD, 80 factures chaque fin de mois, émises le 20, payables avant le 5 du mois suivant. Quand vous appelez un directeur pour savoir combien il a encaissé, la réponse c'est : "Ah, je ne sais pas."

**Problème 2 — Les obligations administratives ne sont pas respectées**
Documents à remplir, deadlines à tenir, signalements à faire. Les directeurs ne le font pas — ou pas à temps. Résultat : l'inspection du travail débarque, comme à La Rochelle, "la rage entre les dents". Des PV, des amendes, des problèmes évitables.

**Problème 3 — Le courrier est maltraité**
Des courriers physiques arrivent dans les établissements — ARS, CPAM, préfecture, inspection du travail. Ils sont oubliés sur un bureau, pas ouverts, pas traités. Quand vous le découvrez, c'est souvent trop tard.

**Problème 4 — Les emails des établissements ne sont pas suivis**
Les boîtes mail des EHPAD reçoivent des messages importants — convocations, demandes d'information, relances administratives. Personne ne les surveille de manière systématique. Des emails critiques restent sans réponse pendant des jours, voire des semaines.

**Problème 5 — Des admissions sont perdues**
Les demandes de placement arrivent via ViaTrajectoire. C'est le plus réactif qui emporte le morceau. Certains directeurs ne traitent pas les dossiers à temps. Chaque admission perdue, c'est ~2 500€/mois de séjour en moins.

**Problème 6 — Les impayés ne sont pas suivis**
Pas de visibilité claire sur qui a payé et qui n'a pas payé. Pas de relances systématiques. L'argent traîne.

Animation : chaque carte apparaît au scroll (fade-in staggeré)

### 4. CE QUE VOUS ATTENDEZ — Les mots de M. Imbert
Section épurée, citations en grand :
> "Tous les matins à 10h, un rapport d'où est-ce qu'on en est."
> "La condition, c'est que ce soit simple pour moi."
> "Cadrer les directeurs et les directrices, gentiment."

Design : fond différent, typographie grande, style citation élégant

### 5. LA RÉPONSE — Votre collaborateur IA
Transition : "Vous n'avez pas besoin d'un logiciel de plus. Vous avez besoin de quelqu'un qui est là tous les jours, qui connaît vos 20 établissements, et qui ne lâche rien."

Présenter les 6 axes avec des blocs visuels (accordéon ou tabs) :

**🔒 Plus jamais de mauvaise surprise**
- Inspection du travail → Alerte 5 jours avant, relance 2 jours avant, escalade si pas fait
- Courrier préfecture → Photo par le directeur, analysé en secondes (expéditeur, objet, deadline, urgence)
- Emails critiques ARS/CPAM → Surveillance 24/7 de chaque boîte mail, alerte si pas traité sous 3 jours
- RGPD → Aucun accès données médicales, hébergement France, effacement 30 jours (sauf facturation 3 ans)
- **Preuve** : La Rochelle n'aurait jamais eu lieu. Traçabilité complète.

**🏆 Le groupe EHPAD le mieux piloté de France**
- Tableau de bord consolidé 20 établissements, mis à jour chaque jour, sur votre téléphone
- Chaque action, deadline, document tracé. Données objectives, pas des "je crois que…"
- **Preuve** : Aucun autre groupe EHPAD familial de cette taille n'a ça.

**✨ Une longueur d'avance sur vos concurrents**
- Le collaborateur comprend un document, pose les bonnes questions, relance au bon moment
- ViaTrajectoire : détection temps réel, alerte directeur, réactivité maximale
- **Preuve** : Le plus réactif emporte l'admission. Avec ce collaborateur, c'est toujours vous.

**🛋️ Vous pilotez, il exécute**
- 1 rapport à 10h, automatique. Zéro appel.
- Il relance, escalade, trace. Vous gérez les exceptions.
- WhatsApp. Zéro formation. Le directeur sait déjà l'utiliser.

**💰 Chaque euro compte — voici les chiffres**
Présenter avec des compteurs animés :
- Amende inspection évitée : 5 000 à 50 000€ économisés par incident
- 1 admission récupérée : ~2 500€/mois
- 5 admissions/an sur le groupe : ~150 000€/an de CA supplémentaire
- Impayés : relances systématiques, trésorerie améliorée
- Temps DG : libéré pour tâches à valeur ajoutée

**🤝 Un collaborateur, pas un logiciel**
- Il a un prénom (que vous choisissez). Il apprend votre vocabulaire, vos habitudes.
- Il ne remplace pas les directeurs, il les aide. Allié, pas contrôleur.
- "Cadrer les directeurs, gentiment" — c'est exactement ce qu'il fait.
- Équipe dédiée : Gilles sur le terrain, Léa dans le groupe.

### 6. CONCRÈTEMENT, À QUOI ÇA SERT ?
Section immersive avec scénario avant/après :

**AVANT — Le lundi matin, 10h :**
(côté gauche, style sombre/rouge)
Vous décrochez le téléphone. Vous appelez La Rochelle. Pas de réponse. Vous appelez Aix. Le directeur cherche ses chiffres. Vous rappelez La Rochelle. On vous dit "je crois que c'est bon". Vous raccrochez sans savoir si c'est vrai. 45 minutes. 2 établissements sur 17. Pour les 15 autres, vous espérez.

**APRÈS — Le lundi matin, 10h :**
(côté droit, style lumineux/vert)
Vous ouvrez WhatsApp. Le rapport est là. Les 17 EHPAD :
- Taux d'occupation : 92%, 87%, 78%…
- Facturation : émise / en attente / en retard
- Impayés : 3 familles en retard >30 jours (noms, montants, relances envoyées)
- Obligations admin : 2 documents cette semaine — directeurs alertés
- Admissions : 4 ViaTrajectoire hier, 3 traitées, 1 en attente — directeur relancé
- Courrier : recommandé ARS Béziers, scanné, analysé — conformité, deadline 15 jours

3 minutes. Zéro appel. Vous savez tout.

**ALERTES TEMPS RÉEL :**
Animation de notifications qui apparaissent :
- "L'EHPAD de Grenoble n'a pas soumis le document CPAM dû demain. Voulez-vous que M. Cozon l'appelle ?"
- "Nouvelle admission ViaTrajectoire pour Marseille. Directeur pas consulté depuis 24h. Je relance."
- "12 factures non encaissées >45 jours sur Aix. Montant : 34 200€. Relances envoyées."

**TABLEAU COMPARATIF :**
Slider ou tableau interactif avant/après :
| Sans le collaborateur | Avec le collaborateur |
|---|---|
| Vous appelez, personne ne sait | Vous ouvrez WhatsApp, tout est là |
| Documents en retard → amende | Alerte 5j avant, relance, escalade |
| Courrier ARS dort 3 semaines | Scanné, analysé, deadline le jour même |
| Admissions inaperçues | Détectées temps réel, directeur relancé |
| Impayés traînent des mois | Relances systématiques, suivi au centime |
| M. Cozon au téléphone toute la journée | Il gère uniquement les exceptions |
| Vous espérez que ça tourne | **Vous savez que ça tourne** |

### 7. COMMENT ÇA SE PASSE — Timeline visuelle

**Jour 0 — L'équipe de démarrage**
Timeline verticale animée :

Étape 0 : Constitution de l'équipe
- M. Imbert — Direction, validation, orientations stratégiques
- M. Cozon — Opérationnel, connaissance terrain, priorités
- Gilles Korzec — Architecte de la solution, audit, formation
- Léa — Admin, juridique, suivi projet, recherches API
- Votre collaborateur IGH — Le nouveau (vous choisissez son prénom)

Groupe WhatsApp créé. Le collaborateur se présente, fait connaissance. Il écoute, retient, commence à comprendre.

**Jours 1-4 — Audit terrain (le collaborateur est dedans, pas derrière)**

Jour 1 — Siège Aix avec M. Imbert + M. Cozon
→ Cycle facturation, obligations admin, relations siège-établissements
→ Le soir : synthèse structurée dans le groupe. Vous corrigez, il apprend.

Jour 2 — DSI / Responsable informatique
→ Cartographie Titan, emails, ViaTrajectoire, réseau
→ Le soir : raisonnement sur connexions possibles, points de blocage, pistes.

Jour 3 — Un EHPAD terrain
→ Quotidien directeur : Titan, courrier, emails, admissions
→ Le soir : alertes et contrôles adaptés à CET établissement.

Jour 4 — Second établissement
→ Comparaison, ajustement
→ Vue consolidée siège + adaptation par établissement.

**+8 jours atelier**
Pour chaque jour terrain :
- 1 jour d'analyse — structurer ce qui a été capté
- 1 jour de construction — alimenter le cerveau, créer la mémoire, configurer les connaissances

**Résultat : 12 jours → un collaborateur opérationnel**
Pas un prototype. Un collaborateur qui connaît votre groupe, qui a raisonné sur vos problèmes, prêt à travailler.

### 8. CONNEXION AUX OUTILS — Phase 2
Visuels avec icônes/logos :
- **Titan/TitanLink** → Facturation, lits, encaissements
- **Boîtes emails 17 EHPAD** → Surveillance, détection, alertes
- **ViaTrajectoire** → Demandes d'admission temps réel
- **Rapport du matin** → Consolidation automatique chaque jour à 10h

### 9. DÉPLOIEMENT — Phase 3
- Démo avec vrais établissements, vrais chiffres
- 2-3 EHPAD pilotes
- Puis les 20

### 10. FOOTER
- "Coach Digital Paris — Gilles Korzec — 06 52 34 51 80"
- Note discrète : "Qu'est-ce qu'une API ? Une API est simplement un pont entre deux logiciels. C'est ce qui permet à votre collaborateur de lire les données de Titan sans se connecter manuellement — comme un assistant qui consulte un dossier dans une armoire, sauf que l'armoire est un logiciel."
- Pas de mentions légales (site privé)

## Design & UX

### Palette de couleurs
- **Fond principal** : #0a0a1a (noir profond)
- **Fond sections alternées** : #111827 (gris très sombre)
- **Accent principal** : #3b82f6 (bleu)
- **Accent secondaire** : #10b981 (vert émeraude — pour le "après", les solutions)
- **Accent danger** : #ef4444 (rouge — pour les problèmes, le "avant")
- **Texte** : #f3f4f6 (blanc cassé)
- **Texte secondaire** : #9ca3af (gris)

### Typographie
- Titres : Inter ou Sora (bold, tracking serré)
- Corps : Inter (regular, 16px min)

### Animations
- Scroll reveal (fade-in + slide-up) pour chaque section
- Compteurs animés pour les chiffres (ROI, admissions, etc.)
- Avant/Après : slider interactif ou split-screen
- Notifications : animation type pop-in pour les alertes temps réel
- Timeline : progression verticale au scroll

### Responsive
- Mobile first (M. Imbert lira sur son iPhone)
- Les tableaux deviennent des cartes empilées sur mobile
- Navigation : menu hamburger ou dots de scroll

## Fichiers de données

Créer un fichier `data/igh.ts` qui contient toutes les données structurées :
- Les 6 problèmes
- Les 6 axes argumentaire (avec problème/solution/preuve pour chaque)
- Le scénario avant/après
- Les alertes temps réel
- Le tableau comparatif
- La timeline
- Les chiffres ROI
- Les citations d'Imbert

## Instructions de déploiement

```bash
npx create-next-app@latest igh-presentation --typescript --tailwind --app --src-dir
cd igh-presentation
# Installer dépendances
npm install framer-motion lucide-react
# Développer
npm run dev
```

## IMPORTANT

- Ce site est PRIVÉ. Pas de référencement, pas de sitemap, pas de robots.txt permissif.
- Ajouter `<meta name="robots" content="noindex, nofollow">` sur toutes les pages.
- Le ton est professionnel mais direct. Pas de bullshit corporate. Pas de "synergies" ou "transformation digitale". On parle comme des humains.
- Les données sont RÉELLES — issues de la réunion du 9 mars 2026 avec M. Imbert et M. Cozon.
- Le site doit être IMPRESSIONNANT visuellement tout en restant lisible et clair.
- M. Imbert a 60+ ans — pas de police trop petite, pas de design trop abstrait. Clair, lisible, impactant.
