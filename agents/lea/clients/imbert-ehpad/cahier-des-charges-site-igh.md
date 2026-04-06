# CAHIER DES CHARGES — Refonte du site web du Groupe IGH
## Site institutionnel moderne pour https://www.i-g-h.fr

---

**Client :** SAS IGH — Groupe familial de 20 établissements médico-sociaux et sanitaires
**Site actuel :** https://www.i-g-h.fr
**Prestataire actuel :** Agence Rhinoferos
**Référence :** CDP-IGH-SITE-2026
**Date :** Mars 2026

---

## 1. CONTEXTE & ÉTAT DES LIEUX

### Le groupe IGH
- **SAS IGH** — Société familiale créée en 2001
- **20 établissements** : 17 EHPAD + 3 cliniques (SSR + psychiatrie)
- **9 régions** : PACA, Auvergne-Rhône-Alpes, Grand Est, Nouvelle-Aquitaine, Bourgogne, Occitanie
- **~1 400 lits**
- **Siège** : 930 Route de Berre, 13090 Aix-en-Provence
- **5 valeurs** : Accueillir, Accompagner, Soigner, Protéger, Respecter

### Analyse du site actuel (i-g-h.fr)

**Architecture technique :**
- Site sur mesure PHP/HTML (pas de CMS moderne)
- jQuery (version ancienne, 2018+)
- Hébergement 1&1 Internet SARL
- SSL actif (HTTPS)
- Google Analytics 4 (G-6GL7PE8BQE)
- Design responsive mais daté
- Bandeau cookies RGPD présent

**Palette de couleurs actuelle :**
- Bleu principal : #0a75a9
- Bleu foncé : #0e4b69
- Bleu moyen : #1079ab
- Bleu sombre : #135473
- Vert doux : #7da144
- Sarcelle : #547979 / #c0d2d2
- Rose/magenta accent : #c20e7b / #ad0b7b
- Gris texte : #656565 / #424242
- Blanc : #ffffff
- Noir : #000000

**Pages existantes :**
- Accueil (diaporama d'images)
- IGH (présentation du groupe)
- Nos Résidences — 17 fiches EHPAD
- Nos Cliniques — 3 fiches
- Actualités
- Témoignages
- Partenaires
- Recrutement (candidatures spontanées)
- FAQ
- Contact
- Mentions légales

**Points faibles identifiés :**
1. Design daté — esthétique 2018, pas aux standards actuels
2. Pas de stratégie de contenu (aucun blog, aucun article)
3. SEO faible — peu de contenu textuel optimisé
4. Réseaux sociaux absents (pas d'Instagram, pas de LinkedIn visible)
5. 20 établissements = chacun a son propre site indépendant → pas de cohérence
6. Pas de chatbot / pas d'IA / pas d'interactivité
7. Communication familles limitée (seul Utrillo a "FAMILYPOST")
8. Recrutement basique — simple formulaire
9. Pas d'application mobile
10. Pas de visite virtuelle des établissements
11. Témoignages familles en texte brut, pas mis en valeur
12. Carte des établissements peu interactive

---

## 2. OBJECTIFS DE LA REFONTE

### Objectifs stratégiques
1. **Moderniser l'image du groupe** — un site à la hauteur d'un groupe de 20 établissements
2. **Rassurer les familles** — le choix d'un EHPAD est un moment difficile, le site doit inspirer confiance
3. **Faciliter le recrutement** — attirer des soignants dans un secteur en tension
4. **Unifier la marque** — un site groupe cohérent avec les sites individuels des établissements
5. **Améliorer le référencement** — être trouvable sur "EHPAD + ville" pour chaque établissement

### Objectifs opérationnels
- Site responsive mobile-first (les familles cherchent sur leur téléphone)
- Temps de chargement < 3 secondes
- Score Lighthouse > 90 (Performance, Accessibilité, SEO)
- Administration simple (CMS) pour que le groupe puisse mettre à jour le contenu
- Formulaire de contact / demande d'information par établissement
- Intégration réseaux sociaux

---

## 3. ARBORESCENCE DU NOUVEAU SITE

```
🏠 ACCUEIL
├── 🏥 LE GROUPE IGH
│   ├── Notre histoire
│   ├── Nos valeurs (Accueillir, Accompagner, Soigner, Protéger, Respecter)
│   ├── Notre démarche qualité
│   └── Notre équipe dirigeante
│
├── 🏡 NOS ÉTABLISSEMENTS
│   ├── Vue d'ensemble (carte interactive)
│   ├── EHPAD (17 fiches individuelles)
│   │   └── Chaque fiche : photos, description, services, capacité, contact, localisation, visite virtuelle
│   └── Cliniques (3 fiches individuelles)
│       └── Chaque fiche : spécialité, équipe, services, contact
│
├── 👨‍👩‍👧‍👦 FAMILLES
│   ├── Comment choisir un EHPAD ?
│   ├── Les étapes de l'admission
│   ├── ViaTrajectoire — comment ça marche ?
│   ├── Tarifs et aides financières (APA, ASH, APL)
│   ├── Témoignages (carrousel moderne avec photos)
│   └── FAQ
│
├── 💼 NOUS REJOINDRE
│   ├── Pourquoi rejoindre IGH ?
│   ├── Nos métiers (infirmier, aide-soignant, directeur, animateur, cuisinier...)
│   ├── Offres d'emploi (par établissement, par métier, par région)
│   └── Candidature spontanée (formulaire moderne + upload CV)
│
├── 📰 ACTUALITÉS
│   ├── Blog / Articles (vie des établissements, événements, formations)
│   └── Newsletter (inscription)
│
├── 📞 CONTACT
│   ├── Siège (formulaire + carte)
│   ├── Par établissement (sélection → formulaire dédié)
│   └── Demande de renseignements / visite
│
└── ⚖️ MENTIONS LÉGALES / POLITIQUE DE CONFIDENTIALITÉ / COOKIES
```

---

## 4. CAHIER DES CHARGES PAR PAGE

### 4.1 ACCUEIL

**Objectif :** Inspirer confiance dès la première seconde. Rassurer les familles.

**Contenu :**
- Hero plein écran avec vidéo ou image de qualité (personnes âgées souriantes, personnel bienveillant, établissement lumineux)
- Titre : "20 établissements. Une famille." ou "Prendre soin, c'est notre raison d'être"
- Les 5 valeurs en icônes animées
- Chiffres clés animés au scroll :
  - 20 établissements
  - ~1 400 résidents accompagnés
  - 9 régions
  - Depuis 2001
  - Société familiale
- Carte interactive de France avec les 20 établissements (clic → fiche)
- Carrousel de témoignages familles
- Bloc "Vous cherchez un EHPAD ?" avec moteur de recherche (par ville, par région, par département)
- Bloc recrutement : "Rejoignez-nous" avec chiffre d'offres ouvertes
- Bloc actualités : 3 derniers articles

**Design :**
- Couleurs chaudes et rassurantes
- Photos réelles (PAS de stock photos génériques)
- Typographie grande, lisible, accessible
- Animations douces au scroll (fade-in, parallax léger)

---

### 4.2 LE GROUPE IGH

**Objectif :** Montrer la solidité et l'humanité du groupe

**Contenu :**
- Notre histoire : timeline depuis 2001 (création → développement → 20 établissements aujourd'hui)
- Nos valeurs : 5 blocs visuels (Accueillir, Accompagner, Soigner, Protéger, Respecter) avec illustrations
- Démarche qualité : certification, engagements, formation continue
- L'équipe dirigeante : photos + bio (si validé par le client)
- Services supports fournis aux établissements (RH, juridique, qualité, achats groupés, veille)

---

### 4.3 NOS ÉTABLISSEMENTS

**Objectif :** Permettre aux familles de trouver et comparer les établissements facilement

**Vue d'ensemble :**
- Carte interactive de France (style Google Maps intégré)
- Filtres : par type (EHPAD / Clinique), par région, par département, par services (Alzheimer, PASA, SSR)
- Liste avec vignettes photos + infos clés

**Fiche individuelle par établissement :**
- Galerie photos / visite virtuelle 360° (si disponible)
- Description détaillée
- Services proposés (unité Alzheimer, PASA, jardin thérapeutique, animations, restauration)
- Capacité (nombre de lits / chambres)
- L'équipe (directeur, médecin coordinateur)
- Localisation (carte + accès)
- Contact direct (téléphone, email, formulaire)
- Bouton "Demander une visite"
- Bouton "Faire une demande d'admission"
- Lien vers le site individuel de l'établissement (si existant)
- Témoignages liés à cet établissement

**Les 17 EHPAD :**

| N° | Établissement | Ville | Région | Tél |
|----|---------------|-------|--------|-----|
| 1 | Lac de Calot | Cadaujac (33) | Nouvelle-Aquitaine | 05 57 83 84 00 |
| 2 | Centre des Carmes | Aiglun (04) | PACA | 04 92 30 34 00 |
| 3 | L'Aube | Saint-Cyr-du-Doret (17) | Nouvelle-Aquitaine | 05 46 00 76 70 |
| 4 | Margaux | Lyon 9ème (69) | Auvergne-Rhône-Alpes | 04 72 20 09 89 |
| 5 | Utrillo | Saint-Bernard (01) | Auvergne-Rhône-Alpes | 04 74 00 17 17 |
| 6 | Marie Madeleine | Saint-Maximin (83) | PACA | 04 94 78 01 94 |
| 7 | Le Parc | Nancy (54) | Grand Est | 03 83 32 97 12 |
| 8 | Les Hibiscus | Mexy (54) | Grand Est | 03 82 25 85 67 |
| 9 | Les Jardins de la Vire | Ville-Houdlemont (54) | Grand Est | 03 82 25 20 50 |
| 10 | Les Verts Monts | Charly (69) | Auvergne-Rhône-Alpes | 04 78 46 09 82 |
| 11 | Saint-Laurent | Lentilly (69) | Auvergne-Rhône-Alpes | 04 74 01 67 00 |
| 12 | L'Âge d'Or | Saint-Dié-des-Vosges (88) | Grand Est | 03 29 56 00 01 |
| 13 | Résidence Antoine | Saint-Maurice-sur-Moselle (88) | Grand Est | 03 29 25 82 11 |
| 14 | Résidence Jeanne | Dijon (21) | Bourgogne-Franche-Comté | 03 80 65 34 75 |
| 15 | Les Jardins des Cuvières | Thaon-les-Vosges (88) | Grand Est | 03 29 38 50 00 |
| 16 | La Résidence | Lisle-sur-Tarn (81) | Occitanie | 05 63 33 32 00 |
| 17 | Les Tamaris | Aytré (17) | Nouvelle-Aquitaine | 05 46 45 42 50 |

**Les 3 Cliniques :**

| N° | Clinique | Ville | Type | Tél |
|----|----------|-------|------|-----|
| 1 | La Chenaie | Bouc-Bel-Air (13) | SSR | 04 42 94 98 98 |
| 2 | La Jauberte | Aix-en-Provence (13) | Psychiatrie | 08 26 02 60 02 |
| 3 | Centre des Carmes | Aiglun (04) | SSR + EHPAD + USLD | 04 92 30 34 00 |

---

### 4.4 FAMILLES

**Objectif :** Accompagner les familles dans leur démarche (moment émotionnel difficile)

**Contenu :**
- Guide "Comment choisir un EHPAD ?" — article de fond, critères, check-list
- Les étapes de l'admission — processus clair, pas à pas visuel
- ViaTrajectoire — qu'est-ce que c'est, comment ça marche, comment déposer un dossier
- Tarifs et aides — explication APA, ASH, APL, aide au calcul du reste à charge
- Témoignages — carrousel moderne avec photos, prénoms, établissements, citations
- FAQ — accordéon avec les questions fréquentes

**Ton :** Bienveillant, rassurant, clair. Pas administratif, pas froid.

---

### 4.5 NOUS REJOINDRE (Recrutement)

**Objectif :** Attirer des talents dans un secteur en pénurie

**Contenu :**
- "Pourquoi rejoindre IGH ?" — valeurs, groupe familial, développement professionnel, ambiance
- Nos métiers — fiches métiers illustrées (infirmier, aide-soignant, médecin coordinateur, animateur, cuisinier, agent de service, directeur d'établissement)
- Offres d'emploi — moteur de recherche (par métier, par établissement, par région)
- Candidature spontanée — formulaire moderne (upload CV, lettre de motivation, choix de région)
- Témoignages collaborateurs — vidéos ou citations de salariés

**Fonctionnalités :**
- Alerte emploi par email (inscription)
- Partage offre sur réseaux sociaux
- Candidature en 1 clic (mobile)

---

### 4.6 ACTUALITÉS / BLOG

**Objectif :** Montrer la vie des établissements, améliorer le SEO

**Contenu :**
- Articles sur la vie des résidents (fêtes, animations, sorties)
- Événements du groupe (formations, séminaires, certifications)
- Articles de fond (bien vieillir, maladie d'Alzheimer, alimentation des seniors)
- Newsletter : inscription en bas de page

---

### 4.7 CONTACT

**Objectif :** Faciliter la prise de contact

**Contenu :**
- Formulaire contact siège
- Sélecteur d'établissement → formulaire dédié (directement au bon EHPAD)
- Demande de visite (choix de date, de créneau)
- Demande d'information / admission
- Carte interactive siège + établissements
- Téléphone siège : 04 28 38 05 10

---

## 5. SPÉCIFICATIONS TECHNIQUES

### Stack recommandée
- **Framework** : Next.js 14 (App Router) ou Astro (pour un site statique ultra-rapide)
- **Styling** : Tailwind CSS
- **CMS headless** : Sanity, Strapi ou Notion API (pour que le groupe puisse éditer le contenu)
- **Hébergement** : Vercel ou Netlify
- **Carte** : Mapbox ou Leaflet (carte interactive des établissements)
- **Formulaires** : React Hook Form + envoi email (SendGrid ou Resend)
- **Analytics** : Google Analytics 4 (conservation GA4 actuel) + Plausible (alternative privacy-first)
- **SEO** : Sitemap XML, robots.txt, meta OpenGraph, Schema.org (LocalBusiness pour chaque EHPAD)

### Performance
- Score Lighthouse > 90 sur les 4 critères
- Temps de chargement < 3 secondes (mobile 4G)
- Images optimisées (WebP, lazy loading)
- Core Web Vitals conformes

### Accessibilité
- WCAG 2.1 niveau AA minimum (personnes âgées = publics avec handicaps potentiels)
- Contraste texte/fond élevé
- Navigation au clavier
- Textes alternatifs sur toutes les images
- Taille de police minimum 16px corps

### Responsive
- Mobile first (>60% du trafic)
- Breakpoints : mobile (< 768px), tablette (768-1024px), desktop (> 1024px)

### SEO
- URL propres : /etablissements/ehpad-margaux-lyon
- Balises title et meta description uniques par page
- Schema.org LocalBusiness pour chaque établissement (nom, adresse, téléphone, coordonnées GPS)
- Contenu textuel riche sur chaque fiche établissement (>300 mots)
- Blog avec articles optimisés SEO

### Sécurité
- HTTPS obligatoire
- RGPD : bandeau cookies avec consentement granulaire
- Formulaires avec reCAPTCHA ou honeypot
- Mentions légales à jour

---

## 6. CHARTE GRAPHIQUE

### Palette de couleurs (évolution de l'identité IGH existante)

| Usage | Couleur | Hex |
|-------|---------|-----|
| Bleu principal (confiance, santé) | Bleu IGH | #0a75a9 |
| Bleu foncé (profondeur, sérieux) | Bleu nuit IGH | #0e4b69 |
| Vert (nature, sérénité, vie) | Vert IGH | #7da144 |
| Sarcelle clair (douceur, apaisement) | Sarcelle | #c0d2d2 |
| Blanc (clarté, pureté) | Blanc | #ffffff |
| Gris texte (lisibilité) | Gris | #424242 |
| Accent (CTAs, boutons) | Magenta IGH | #c20e7b |
| Fond clair (arrière-plans) | Gris très clair | #f5f7fa |
| Alerte/urgence | Rouge doux | #e12625 |

### Typographie
- Titres : **Inter Bold** ou **Sora Bold** — grandes tailles, tracking serré
- Corps : **Inter Regular** — 16px minimum, interligne 1.6
- Citations : **Serif (Georgia ou Playfair Display)** — italique, élégant

### Iconographie
- Icônes ligne fine (Lucide, Phosphor ou Heroicons)
- Illustrations douces (style flat ou isométrique) pour les guides familles

### Photographie
- Photos réelles des établissements et des résidents (PAS de stock photos)
- Lumière naturelle, tons chauds
- Personnes souriantes, interactions humaines
- Bannir : images froides, hôpital, solitude

---

## 7. FONCTIONNALITÉS AVANCÉES (PHASE 2)

Ces fonctionnalités peuvent être ajoutées après le lancement initial :

| Fonctionnalité | Description | Priorité |
|----------------|-------------|----------|
| **Chatbot IA** | Agent conversationnel pour répondre aux questions des familles 24/7 | Haute |
| **Espace familles** | Portail privé (type FAMILYPOST) : photos, activités, menu de la semaine, messages | Haute |
| **Visite virtuelle 360°** | Pour chaque établissement, visite immersive des locaux | Moyenne |
| **Simulateur de coût** | Calcul du reste à charge (APA + ASH + APL) | Moyenne |
| **Système de réservation de visite** | Prise de RDV en ligne avec calendrier | Haute |
| **Alertes emploi** | Notification par email quand une offre correspond au profil | Moyenne |
| **Multi-langue** | Anglais (pour les familles étrangères) | Basse |
| **Application mobile** | PWA ou app native pour les familles | Basse |

---

## 8. CONTENUS À FOURNIR PAR LE CLIENT

| Contenu | Responsable | Format |
|---------|-------------|--------|
| Photos des 20 établissements (haute résolution) | Directeurs d'établissement | JPEG/PNG min 2000px |
| Descriptions mises à jour de chaque établissement | Directeurs + siège | Texte |
| Témoignages familles (avec accord écrit) | Siège | Texte + photo si possible |
| Témoignages collaborateurs | RH | Texte ou vidéo |
| Offres d'emploi actuelles | RH | Texte |
| Organigramme direction | Direction | Document |
| Logo IGH (vectoriel) | Siège | SVG ou AI |
| Charte graphique existante (si elle existe) | Siège | PDF |
| Tarifs de référence par établissement | Direction | Document |

---

## 9. PLANNING PRÉVISIONNEL

```
Semaine 1-2    ████████  Design & Maquettes (wireframes + UI)
Semaine 3-4    ████████  Développement structure + pages principales
Semaine 5      ████      Intégration contenu (textes, photos, fiches établissements)
Semaine 6      ████      Tests + Corrections + Optimisation SEO
Semaine 7      ██        Mise en ligne + Formation CMS
```

**Durée estimée : 6-7 semaines**

---

## 10. LIVRABLES

| Livrable | Format |
|----------|--------|
| Maquettes UI/UX (mobile + desktop) | Figma |
| Site web complet déployé | URL de production |
| Accès CMS (back-office) | Identifiants admin |
| Documentation CMS | PDF / Notion |
| Formation utilisation CMS | Visio 1h |
| Optimisation SEO technique | Inclus |
| Sitemap XML + robots.txt | Inclus |
| Configuration Analytics | Inclus |

---

*Cahier des charges préparé par Coach Digital Paris — Gilles Korzec*
*Mars 2026 — Confidentiel*
