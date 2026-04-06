# Prompts Emergent — Projet EmiRise
## Site Web Premium Location Courte Durée — Aix-en-Provence & Provence

> **Référence design principale : highstay.com**
> **Stack suggérée : Next.js + Tailwind CSS + TypeScript**
> **Chaque prompt est autonome et séquentiel. Envoyer dans l'ordre.**

---

## PROMPT 1 — Architecture globale & Layout principal

```
Crée un site web premium pour EmiRise, une entreprise de location courte durée haut de gamme à Aix-en-Provence et en Provence.

DESIGN & POSITIONNEMENT :
- Inspiration principale : highstay.com (copier fidèlement l'esprit, le layout et l'UX)
- Univers : luxe, élégance, exclusivité, art de vivre provençal
- Palette : tons neutres/chauds (beige, crème, blanc cassé, accents dorés ou terre)
- Typo : serif élégante pour les titres (type Playfair Display), sans-serif clean pour le body
- Photos plein écran, grande respiration visuelle, espaces blancs généreux

STRUCTURE DES PAGES :
1. Page d'accueil (hero + sections)
2. Page "Nos Appartements" (liste des biens)
3. Page détail logement (fiche individuelle)
4. Page "Nos Villas" (liste des villas)
5. Page "Services & Expériences"
6. Page "Explorer nos quartiers" (guides Aix-en-Provence)
7. Page "Journal" (blog SEO)
8. Page "À propos"
9. Page "Rejoindre notre portfolio" (formulaire propriétaires)
10. Page "Besoin d'aide" / Contact

RESPONSIVE : Mobile-first, design parfait sur mobile et desktop.

Pour ce premier prompt, mets en place l'architecture du projet, le layout global (header, footer, navigation), les routes et la structure des composants. Pas de contenu encore — juste le squelette.
```

---

## PROMPT 2 — Header & Navigation

```
Implémente le header et la navigation du site EmiRise, fidèlement inspiré de highstay.com :

HEADER :
- Image de fond immersive plein écran en arrière-plan (hero image)
- Logo EmiRise centré dans le header
- Menu burger (☰) en haut à gauche
- En haut à droite : bouton "Nous contacter" + sélecteur de langue (FR/EN)
- PAS de bouton "Compte" / "Connexion" — on ne veut pas de système de compte utilisateur

MENU BURGER (encart latéral gauche) :
À l'ouverture, le menu apparaît comme un panneau latéral gauche, fond blanc/crème, sans image de fond.

Sections du menu :
- Nos Appartements
- Nos Villas
- Nos Services et Expériences
- Rejoindre notre portfolio

Sous-sections :
- Les incontournables
- Journal
- À propos
- Besoin d'aide

En bas du menu : inscription newsletter (champ email + bouton)

COMPORTEMENT :
- Le header doit devenir sticky/transparent au scroll (comme highstay.com)
- Animation douce à l'ouverture/fermeture du menu
- Transition fluide entre les pages
```

---

## PROMPT 3 — Hero Section & Bandeau de recherche

```
Crée la section hero de la page d'accueil EmiRise, inspirée de highstay.com :

HERO :
- Image de fond plein écran, haute qualité (placeholder pour l'instant)
- Titre principal centré en overlay : "Séjours d'exception en Provence" (ou similaire)
- Sous-titre : "Appartements & villas de luxe à Aix-en-Provence"

BANDEAU DE RECHERCHE (above the fold, visible sans scroller) :
- Design horizontal élégant, fond blanc semi-transparent ou card avec ombre
- 4 champs + 1 bouton :
  1. "Tous les quartiers" — Select/dropdown
  2. "Arrivée" — Date picker
  3. "Départ" — Date picker
  4. "Nombre d'invités" — Compteur (+/-)
  5. Bouton CTA : "Trouver un logement" (style accent, bien visible)

BLOCS AVANTAGES (juste sous le bandeau) :
3 blocs horizontaux avec icônes et textes courts :
- Icône 1 : "Réservation directe — Sans frais de plateforme"
- Icône 2 : "Conciergerie dédiée — Service personnalisé 24/7"
- Icône 3 : "Biens sélectionnés — Qualité vérifiée et premium"

Style épuré, icônes fines (type Lucide/Phosphor), texte court.
```

---

## PROMPT 4 — Section "Nos Appartements" (fiches logements)

```
Crée la section "Nos Appartements" pour la page d'accueil et la page listing, fidèlement inspirée de highstay.com :

FICHES LOGEMENTS :
Chaque fiche contient :
- Carousel d'images (swipe horizontal, avec dots/indicateurs)
- Nom du logement (ex: "Casavo — Le Tholonet")
- Quartier / Localisation
- Informations clés avec icônes : superficie (m²), chambres (lit), invités max (personne)
- Prix : "À partir de XXX€ / nuit"
- Les icônes doivent être fines et élégantes (lit, personne, surface)

LAYOUT :
- Grille 2 ou 3 colonnes sur desktop, 1 colonne sur mobile
- Espacement généreux entre les cards
- Hover effect subtil (légère élévation ou zoom image)

En bas de la section : bouton "Découvrir tous nos appartements" → lien vers page listing complète

DONNÉES PLACEHOLDER (5 logements) :
1. Casavo — Le Tholonet | 120m² | 3 chambres | 6 invités | à partir de 250€/nuit
2. Villa Provence — Aix-Centre | 200m² | 4 chambres | 8 invités | à partir de 400€/nuit
3. L'Atelier — Cours Mirabeau | 75m² | 2 chambres | 4 invités | à partir de 180€/nuit
4. Bastide du Soleil — Puyricard | 300m² | 5 chambres | 10 invités | à partir de 550€/nuit
5. Le Mazet — Éguilles | 90m² | 2 chambres | 4 invités | à partir de 200€/nuit
```

---

## PROMPT 5 — Page détail logement

```
Crée la page de détail d'un logement EmiRise, inspirée de highstay.com :

STRUCTURE :
1. GALERIE PHOTOS en haut — Grande image principale + grille de 4-5 photos secondaires, cliquable pour ouvrir un carousel plein écran

2. INFOS PRINCIPALES :
   - Nom du logement
   - Localisation / quartier
   - Icônes : m², chambres, salles de bain, invités max
   - Description longue du bien (2-3 paragraphes)

3. ÉQUIPEMENTS :
   - Grille d'icônes + labels : WiFi, Climatisation, Cuisine équipée, Machine à laver, Parking, Terrasse, Piscine, etc.

4. CARTE DE LOCALISATION :
   - Intégration Google Maps ou Mapbox — pin sur l'emplacement du logement

5. CALENDRIER DE DISPONIBILITÉ :
   - Calendrier visuel avec dates disponibles/indisponibles (placeholder pour l'intégration iCal future)

6. BLOC RÉSERVATION (sidebar droite sur desktop) :
   - Arrivée / Départ (date pickers)
   - Nombre d'invités
   - Récapitulatif prix (nuits × tarif + frais ménage + total)
   - Bouton "Réserver" ou "Demander une réservation"

7. AVIS CLIENTS :
   - Section en bas avec témoignages (nom, date, note étoiles, commentaire)

8. LOGEMENTS SIMILAIRES :
   - Carousel horizontal de 3-4 logements recommandés
```

---

## PROMPT 6 — Section "Explorer nos quartiers"

```
Crée la section "Explorer nos quartiers" pour EmiRise :

CONCEPT : Articles/guides sur les quartiers d'Aix-en-Provence et ses environs pour le SEO et l'immersion.

LAYOUT PAGE D'ACCUEIL :
- 3-4 cards en grille horizontale
- Chaque card : image de fond du quartier + nom en overlay + courte description
- Hover : légère animation (zoom ou overlay plus sombre)
- CTA : "Explorer tous les quartiers"

PAGE LISTING QUARTIERS :
- Grille de cards plus large
- Chaque quartier mène vers un article dédié

PAGE ARTICLE QUARTIER :
- Image hero du quartier
- Titre H1 : "Découvrir [Quartier]"
- Contenu éditorial riche : histoire, ambiance, restaurants, activités
- Sidebar : logements disponibles dans ce quartier
- CTA en bas : "Voir nos logements à [Quartier]"

QUARTIERS PLACEHOLDER :
1. Aix-Centre / Cours Mirabeau
2. Le Tholonet
3. Puyricard
4. Éguilles
5. Pays d'Aix (alentours)
```

---

## PROMPT 7 — Section "Service exceptionnel" + "À propos"

```
Crée deux sections pour EmiRise :

SECTION "UN SERVICE EXCEPTIONNEL" (page d'accueil) :
- Image de fond grande et immersive (intérieur luxueux ou paysage provençal)
- Titre fort centré en overlay : "Un service exceptionnel et une équipe dédiée"
- Sous-titre court
- 4 blocs avantages en dessous :
  1. "Accueil personnalisé" — Remise des clés en personne, guide du séjour
  2. "Conciergerie sur mesure" — Restaurants, activités, transferts
  3. "Qualité garantie" — Chaque bien est inspecté et préparé avec soin
  4. "Support 24/7" — Une équipe disponible à tout moment

PAGE "À PROPOS" :
- Hero image + titre "Notre histoire"
- Section texte : présentation EmiRise, fondateurs (Emilio Arias & Maximilien Veronico)
- Vision : "Révéler l'art de vivre provençal à travers des séjours d'exception"
- Section équipe avec photos (placeholder)
- Nos valeurs : Excellence, Authenticité, Hospitalité, Sélection rigoureuse
- CTA : "Découvrir nos logements" + "Rejoindre notre portfolio"
```

---

## PROMPT 8 — Blog / Journal

```
Crée la section "Journal" (blog) pour EmiRise, inspirée de highstay.com :

PAGE D'ACCUEIL — Section blog :
- 3 articles en preview (image + titre + extrait + date)
- Bouton "Lire notre journal"

PAGE LISTING BLOG :
- Articles en grille (2 colonnes desktop, 1 mobile)
- Filtres par catégorie : Quartiers, Culture, Gastronomie, Activités, Actualités EmiRise
- Pagination

PAGE ARTICLE :
- Image hero plein largeur
- Titre H1 + date + catégorie + temps de lecture
- Contenu riche avec images intégrées
- Sidebar : articles similaires + CTA réservation
- Partage réseaux sociaux
- Section "Articles similaires" en bas

Objectif SEO : chaque article cible des requêtes type "que faire à Aix-en-Provence", "meilleur restaurant Aix", "location vacances Le Tholonet"
```

---

## PROMPT 9 — Formulaire "Rejoindre notre portfolio" + Avis clients

```
Crée deux éléments pour EmiRise :

PAGE "REJOINDRE NOTRE PORTFOLIO" (pour les propriétaires) :
Inspiré du formulaire Le Collectionist.

Formulaire avec les champs :
- Nom complet
- Email
- Téléphone
- Type de bien : Appartement / Villa / Maison / Autre
- Localisation du bien
- Superficie (m²)
- Nombre de chambres
- Description courte du bien
- Photos (upload multiple)
- Message complémentaire
- Bouton "Soumettre votre bien"

Texte d'intro au-dessus du formulaire :
"Vous êtes propriétaire d'un bien d'exception en Provence ? Rejoignez notre collection de logements soigneusement sélectionnés et bénéficiez de notre expertise en gestion locative haut de gamme."

WIDGET AVIS CLIENTS (page d'accueil) :
- Carousel horizontal auto-défilant
- Chaque avis : note étoiles, prénom, date du séjour, commentaire, logement
- Design élégant, fond légèrement teinté
- Contrôles gauche/droite + dots
- 5 avis placeholder
```

---

## PROMPT 10 — Footer + SMTP + Finitions

```
Crée le footer et les finitions du site EmiRise, inspiré de highstay.com :

FOOTER :
Structure en colonnes :
- Col 1 : Logo EmiRise + courte description + réseaux sociaux (Instagram, Facebook, LinkedIn)
- Col 2 : Navigation — Nos Appartements, Nos Villas, Services, Journal
- Col 3 : Informations — À propos, Rejoindre notre portfolio, Besoin d'aide, CGV
- Col 4 : Newsletter — champ email + bouton "S'inscrire"
- Barre basse : © 2026 EmiRise — Tous droits réservés | Mentions légales | Politique de confidentialité

FINITIONS GLOBALES :
- Smooth scroll sur toutes les ancres
- Animations d'entrée subtiles au scroll (fade-in)
- Loading states élégants sur les images
- Meta tags SEO sur chaque page (title, description, og:image)
- Favicon EmiRise
- Responsive parfait (tester 375px, 768px, 1024px, 1440px)

SMTP (placeholder) :
- Formulaire contact → envoi email via API route (placeholder, prêt pour intégration SMTP)
- Formulaire newsletter → stockage email (placeholder)
- Formulaire portfolio → envoi email avec pièces jointes (placeholder)
```

---

## Notes pour Hugo

- **Ordre d'envoi** : Prompt 1 → 10 dans l'ordre
- **Après chaque prompt** : vérifier le rendu avant d'envoyer le suivant
- **Photos** : remplacer les placeholders par les vraies photos Google Drive une fois l'accès obtenu
- **Intégrations futures** (pas dans ces prompts) : iCal, synchro Airbnb, système de réservation réel, SMTP réel, Google Maps API
- **Référence absolue** : highstay.com pour chaque détail de design et d'UX
