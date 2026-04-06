# PROMPT 2 — JULES : Site web VL Médical (Vitrine + Portail B2B)

> Brief complet pour Jules (Tech Lead) — Création du site VL Médical.

---

## CONTEXTE

Tu dois créer le site web complet de **VL Médical**, une SAS de négoce de dispositifs médicaux (DM), d'équipements de protection individuelle (EPI) et de vêtements de luxe en gros. Dirigée par Jean-Luc Aubagnac, basée à Éguilles (13510).

Le site a **deux fonctions** :
1. **Vitrine professionnelle** — présenter l'entreprise, ses produits, ses services, inspirer confiance
2. **Portail client B2B** — espace connecté où chaque client voit SES prix, SES produits disponibles, peut demander des devis et suivre ses commandes

---

## IDENTITÉ DE L'ENTREPRISE

- **Raison sociale** : VL MÉDICAL — SAS au capital de 1 000€
- **RCS** : 853 225 100 — Aix-en-Provence
- **Siège** : 190 Rue Topaze, 13510 Éguilles
- **Président** : Jean-Luc Aubagnac
- **Activité** : Négoce de dispositifs médicaux et EPI, prestations logistiques
- **Deux pôles d'activité** :
  - **Pôle DM/EPI** (activité historique) : gants nitrile/latex/vinyle, masques, charlottes, surblouses, surchaussures, pansements
  - **Pôle Textile luxe** (activité récente) : vêtements de luxe en gros (Jacob Cohen, marques italiennes/françaises) — Showroom Marina Baie des Anges

---

## ARCHITECTURE DU SITE

### PARTIE 1 — VITRINE PUBLIQUE (sans login)

#### Page d'accueil
- Hero section professionnelle — positionnement : fournisseur de confiance DM/EPI
- Chiffres clés (années d'expérience, nombre de clients, zones couvertes)
- Les deux pôles d'activité présentés visuellement
- CTA principal : "Demander un devis" / "Accéder à mon espace"
- Certifications et conformité (MDR 2017/745, normes CE)

#### Page "Nos Produits — DM & EPI"
Présentation par catégorie :
- **Gants nitrile** — description, usages (hôpitaux, cliniques — obligatoire en France, latex interdit en chirurgie)
- **Gants latex** — description, usages (dentisterie en France pour le toucher précis, standard en Afrique)
- **Gants vinyle** — description, usages légers
- **Masques** (chirurgicaux, FFP2)
- **Charlottes, surblouses, surchaussures**
- **Pansements**

Pour chaque catégorie :
- Photos professionnelles
- Gammes qualité : Premium (400-500g/boîte), Standard (350-400g), Économique (250-300g) — le poids fait la qualité et le prix
- Origines disponibles : France 🇫🇷, Malaisie 🇲🇾 (Top Glove), Indonésie 🇮🇩 (latex premium), Chine 🇨🇳 (nitrile compétitif), Japon-Chine 🇯🇵 (nitrile haut de gamme)
- Conditionnement : 100 gants/boîte (90 pour XL lourd), 10 boîtes/carton, 70-84 cartons/palette
- Tailles : XS, S, M, L, XL (pas de XXL)
- ⚠️ **PAS DE PRIX AFFICHÉS** sur la partie publique — "Contactez-nous pour un devis"
- Mention stérile/non stérile quand applicable

#### Page "Nos Produits — Textile de Luxe"
- Présentation sobre et haut de gamme
- **Positionnement : "Outlets de goût et de prix doux"** — PAS de communication "braderie" ou "déstockage"
- Photos lifestyle, ambiance élégante
- Marques disponibles (sans mentionner les prix cassés)
- Showroom Marina Baie des Anges — sur rendez-vous
- ⚠️ **RÈGLE ABSOLUE** : ne JAMAIS afficher de prix publiquement pour le textile. Protéger les marques fournisseurs. Communication axée sur le BEAU, le goût, l'assortiment.
- CTA : "Prendre rendez-vous au showroom" / "Demander notre catalogue privé"

#### Page "Services"
1. **Fourniture DM & EPI** — Gros volumes, livraison rapide France (2 logisticiens + Amazon), export international
2. **Export clé en main** — Conteneurisation, documentation douanière, remise sous douane. Destinations Afrique et Europe.
3. **Déstockage textile de luxe** — Lots de 100 pièces min, marques premium, showroom privatif
4. **Prestation logistique** — Stockage, préparation, expédition pour tiers
5. **Programme partenaires (bientôt)** — Réseau de magasins indépendants

#### Page "Zones de livraison"
Carte interactive ou visuelle :
- 🇫🇷 France entière (2 logisticiens, Amazon FBA)
- 🇮🇹 Italie (camion complet, spécialité Ligurie)
- 🇪🇸🇵🇹 Espagne & Portugal
- 🇧🇪🇳🇱🇩🇪 Benelux & Allemagne
- 🇬🇧 UK
- 🌍 Afrique (Niger, Côte d'Ivoire — conteneurs)
- Zones de conflit (sur demande spéciale)

#### Page "À propos"
- Histoire de VL Médical (fondée 2019)
- Jean-Luc Aubagnac — expertise et parcours
- Valeurs : qualité, réactivité, confiance
- Showroom Marina Baie des Anges

#### Page "Contact / Demande de devis"
- Formulaire de contact structuré :
  - Nom / Entreprise / Email / Téléphone
  - Type de demande (Devis DM-EPI / Devis Textile / Partenariat / Autre)
  - Produits d'intérêt (multi-select)
  - Volume estimé
  - Zone de livraison
  - Message libre
- Coordonnées directes (email, téléphone)
- Plan d'accès showroom (si textile)

#### Pages légales
- Mentions légales (RCS, siège, hébergeur)
- CGV médicales (15 articles, conforme MDR 2017/745)
- Politique de confidentialité

---

### PARTIE 2 — PORTAIL CLIENT B2B (avec login)

#### Système d'authentification
- Login par email + mot de passe
- Chaque client a un compte créé par VL Médical (pas d'inscription libre)
- Onboarding : VL Médical crée le compte, le client reçoit ses identifiants par email
- Rôles : Client / Admin (Jean-Luc + Max)

#### Dashboard client personnalisé
À la connexion, le client arrive sur SON environnement avec :

**Ses informations**
- Profil client (raison sociale, adresses, contacts)
- Conditions de paiement négociées
- Grille tarifaire qui lui est assignée

**Son catalogue personnalisé**
- Seuls les produits disponibles pour LUI (selon son segment : médical France, médical export, textile, etc.)
- **SES prix** (pas les prix standard — prix personnalisés selon sa grille tarifaire, ses quantités habituelles, et la DLU des produits)
- Stock disponible en temps réel
- Photos + fiches produits
- DLU affichée pour chaque produit
- Filtres : par type, par marque, par taille, par gamme qualité, par DLU

**Demande de devis en ligne**
- Le client sélectionne des produits, choisit les quantités et les tailles
- Calcul automatique du prix selon sa grille tarifaire et les quantités
- Si export conteneur : calculateur de remplissage (3200-4000 cartons selon origine)
- Soumission de la demande → VL Médical reçoit et génère le devis officiel
- Option livraison échelonnée (sélectionner le nombre de mois)

**Suivi de commandes**
- Historique des commandes avec statut en temps réel :
  - 📝 Devis envoyé
  - ✍️ Devis signé (bon de commande)
  - 💳 Paiement vérifié
  - 📦 En préparation
  - 🚚 Expédié / En attente d'enlèvement
  - ✅ Livré
  - 🧾 Facturé
  - 💶 Payé
- Documents téléchargeables : devis, bon de commande signé, bon de livraison/enlèvement, facture
- Suivi des paiements (acompte versé, solde dû)

**Signature électronique des devis**
- Le devis est présenté en ligne
- Le client peut le signer électroniquement (signature reconnue juridiquement)
- Le devis signé = bon de commande → déclenche le process de préparation
- Intégration avec un service de signature électronique (DocuSign, Yousign ou équivalent)

**Documents**
- Accès aux CGV
- Certificats produits (CE, MDR)
- Fiches techniques téléchargeables

---

### PARTIE 3 — BACK-OFFICE ADMIN (Jean-Luc + Max)

#### Gestion des clients
- Créer/modifier/désactiver des comptes clients
- Assigner une grille tarifaire à chaque client
- Définir les produits visibles par client
- Conditions de paiement par client

#### Gestion du catalogue
- Ajouter/modifier des produits
- Upload photos multi-angles + vidéos de démonstration
- Définir le size breakdown affiché (en pourcentages, pas en quantités exactes)
- Gérer les stocks par localisation (logisticien 1, logisticien 2, showroom, etc.)
- Alertes automatiques : DLU < 12 mois, DLU < 6 mois, stock bas

#### Gestion des grilles tarifaires
- Créer des grilles par type de client, par produit, par quantité
- Pricing dynamique selon la DLU :
  - >36 mois : prix fort (100%)
  - 24-36 mois : ~90%
  - 12-24 mois : ~70-80%
  - 6-12 mois : ~40-50%
  - <6 mois : ~20-30%
  - Date dépassée : prix plancher (zones de conflit uniquement)
- Grilles personnalisées par client spécifique

#### Gestion des commandes
- Générer les documents de la chaîne :
  1. Devis PDF (à partir du panier client ou manuellement)
  2. Bon de préparation (envoyé au logisticien par email)
  3. Bon de livraison / Bon d'enlèvement
  4. Facture (avec ou sans TVA selon destination)
- Règles TVA automatiques :
  - France → TVA 20%
  - Intracommunautaire UE → 0% TVA (mention autoliquidation)
  - Export hors UE → 0% TVA + bon de remise en douane obligatoire
  - Cas spécial : correspondant français pour export Afrique → 0% TVA si remise sous douane documentée
- CGV médicales automatiquement jointes à chaque facture
- Suivi des paiements : acompte reçu, solde dû, top départ chargement

#### Calculateur de conteneur
- Outil intégré pour calculer le remplissage d'un conteneur :
  - Saisir les produits, quantités, taille des cartons, origine (impact taille carton)
  - Capacité : 3200-3500 cartons standard, jusqu'à 4000 pour cartons chinois compacts
  - Alerte stérile : les produits stériles ne vont que sur les 1-2 dernières couches du haut
  - Calcul automatique du prix total du conteneur
  - Identification des "queues de produits" (restes qui ne rentrent pas)

#### Notifications
- Email automatique au client quand : devis prêt, commande expédiée, facture émise
- Email au logisticien quand : bon de préparation généré
- Alerte interne quand : DLU critique, paiement en retard, stock bas

---

## CONTRAINTES TECHNIQUES

### Stack recommandée
- **Frontend** : Next.js (React) — SSR pour le SEO de la vitrine
- **Backend/API** : Next.js API routes ou backend dédié (Node.js)
- **Base de données** : PostgreSQL (Supabase) ou MongoDB
- **Auth** : NextAuth.js ou Supabase Auth
- **Signature électronique** : Yousign API (français, conforme eIDAS) ou DocuSign
- **Génération PDF** : pour devis, bons de préparation, BL/BE, factures
- **Hébergement** : Vercel (frontend) + API backend
- **Stockage fichiers** : Cloudinary ou S3 (photos produits, documents)

### Responsive
- Mobile-first pour le portail client (Jean-Luc travaille beaucoup depuis son téléphone)
- Desktop optimisé pour le back-office admin

### SEO
- Pages vitrine optimisées pour le référencement
- Meta descriptions, schema.org pour produits B2B
- Blog/actualités (optionnel, phase 2)

### Sécurité
- HTTPS obligatoire
- Données clients confidentielles (RGPD)
- Pas de prix publics (ni dans le code source, ni en cache)
- Accès portail uniquement par compte validé

### Synchronisation Notion (phase 2)
- API Notion pour synchroniser :
  - Catalogue produits ↔ base Notion
  - Clients ↔ base Notion
  - Commandes ↔ base Notion
- Notion = back-office de gestion, Site = interface client

### Amazon (module séparé — phase ultérieure)
- Connexion API Amazon Seller Central
- Synchronisation du catalogue DM/EPI vers Amazon
- Gestion FBA (Fulfillment by Amazon)
- Suivi des ventes Amazon dans le dashboard
- *Ce module sera spécifié séparément*

---

## DESIGN & IDENTITÉ VISUELLE

### Ton & positionnement
- **Professionnel et sobre** — on s'adresse à des hôpitaux, cliniques, laboratoires
- **Confiance et fiabilité** — certifications mises en avant
- **Pas de communication "discount"** — surtout pas pour le textile
- Bilingue FR/EN (clients internationaux)

### Couleurs suggérées
- Bleu médical (confiance, santé) — couleur principale
- Blanc (propreté, médical)
- Gris foncé (texte, élégance)
- Vert d'accent (validation, CTA)
- Section textile : tons plus chauds, élégants (doré, noir, blanc cassé)

### Éléments visuels
- Photos produits de haute qualité (scans multi-angles des boîtes, gants)
- Vidéos de démonstration (résistance des gants)
- Icônes certification (CE, MDR)
- Carte des zones de livraison

---

## LIVRABLES ATTENDUS

### Phase 1 — MVP (4-6 semaines)
1. Site vitrine complet (toutes les pages publiques)
2. Formulaire de contact/devis fonctionnel
3. Portail client : login + dashboard + catalogue personnalisé + demande de devis
4. Back-office admin : gestion clients, produits, grilles tarifaires
5. Génération PDF : devis, factures

### Phase 2 — Fonctionnalités avancées (6-10 semaines)
6. Signature électronique des devis
7. Chaîne documentaire complète (bon prépa → BL/BE → facture)
8. Calculateur de conteneur
9. Notifications email automatiques
10. Synchronisation Notion

### Phase 3 — Extensions
11. Module Amazon (API Seller Central)
12. Blog / actualités
13. App mobile PWA
14. Programme franchise (portail partenaires)
