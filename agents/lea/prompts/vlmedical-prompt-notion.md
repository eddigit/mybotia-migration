# PROMPT 1 — IA NOTION : Template complet VL Médical

> À coller dans l'IA de Notion pour générer l'ensemble du workspace VL Médical.

---

Crée un environnement Notion complet et professionnel pour **VL Médical**, une SAS de négoce de dispositifs médicaux (DM), d'équipements de protection individuelle (EPI) et de vêtements de luxe en gros. Dirigée par Jean-Luc Aubagnac, basée à Éguilles (13510, France). Deux activités distinctes : le négoce de DM/EPI (activité historique) et la vente en gros de vêtements de luxe (activité récente, showroom Marina Baie des Anges près de Nice).

---

## BASES DE DONNÉES RELATIONNELLES À CRÉER

---

### 1. 📥 PROPOSITIONS DE LOTS (flux d'entrée permanent)

C'est le cœur du métier. Des fournisseurs proposent en permanence des surstocks. Chaque lot doit être évalué avant décision d'achat.

Propriétés :
- Nom du lot (titre — ex: "Lot nitrile Top Glove 500 cartons")
- Fournisseur (relation → 🏭 FOURNISSEURS)
- Date de réception de l'offre (date)
- Segment (select : DM-EPI / Textile luxe)
- Type de produit (select : Gants nitrile / Gants latex / Gants vinyle / Masques / Charlottes / Surblouses / Surchaussures / Pansements / Vêtements luxe / Autre EPI)
- Marque (texte)
- Origine de fabrication (select : France 🇫🇷 / Malaisie 🇲🇾 / Indonésie 🇮🇩 / Chine 🇨🇳 / Japon-Chine 🇯🇵🇨🇳 / Italie 🇮🇹 / Autre)
- Qualité/Gamme (select : Premium-Lourd 400-500g / Standard 350-400g / Léger-Économique 250-300g / N/A textile)
- Poids de la boîte en grammes (nombre — pour les gants : poids d'une boîte de 100)
- Stérile (checkbox)
- DLU — Date Limite d'Utilisation (date)
- Mois restants avant DLU (formule : calcul automatique entre aujourd'hui et la DLU)
- Statut DLU (formule/select : ✅ En date >12 mois / ⚠️ <12 mois / 🔴 Date dépassée)
- Size breakdown — répartition par taille :
  - % XS (nombre)
  - % S (nombre)
  - % M (nombre)
  - % L (nombre)
  - % XL (nombre)
- Équilibre tailles (formule/select : ✅ Équilibré / ⚠️ Déséquilibré — trop de S-XL, pas assez de M-L)
- Quantité totale en cartons (nombre)
- Quantité totale en palettes (nombre)
- Conditionnement : boîtes par carton (nombre — standard 10)
- Conditionnement : gants par boîte (nombre — standard 100, parfois 90 pour XL)
- Palettisation : cartons par palette (nombre — 20 / 40 / 70 / 80 / 84)
- Prix d'achat proposé HT/carton (nombre, €)
- Prix d'achat total HT (formule : prix × quantité)
- Mode d'acquisition (select : Achat ferme / Dépôt-vente)
- Localisation stock (select : Logisticien 1 France / Logisticien 2 France / Entrepôt Belgique / Showroom Marina / Dépôt GNS / Autre)
- Photos du lot (fichiers — scans multi-angles des boîtes)
- Vidéo démonstration (fichiers/URL — test de résistance du gant)
- Statut décision (select : 📩 Reçu / 🔍 En étude / ✅ Accepté / ❌ Refusé / ⏳ En attente prix)
- Raison refus (texte — si refusé)
- Intégré au catalogue (checkbox)
- Notes (texte riche)

---

### 2. 📦 CATALOGUE PRODUITS (stock disponible à la vente)

Produits acceptés et disponibles. Chaque fiche = un produit prêt à vendre.

Propriétés :
- Nom du produit (titre)
- Référence SKU (texte)
- Lot d'origine (relation → 📥 PROPOSITIONS DE LOTS)
- Segment (select : DM-EPI / Textile luxe)
- Catégorie (select : Gants nitrile / Gants latex / Gants vinyle / Masques chirurgicaux / Masques FFP2 / Charlottes / Surblouses / Surchaussures / Pansements / Vêtements luxe — Jeans / Vêtements luxe — Vestes / Vêtements luxe — Autre / Autre EPI)
- Marque (select : EMILABO / Top Glove / GNS / Jacob Cohen / Via Italia / Autre)
- Origine fabrication (select : France 🇫🇷 / Malaisie 🇲🇾 / Indonésie 🇮🇩 / Chine 🇨🇳 / Japon-Chine 🇯🇵🇨🇳 / Italie 🇮🇹 / Autre)
- Qualité/Gamme (select : Premium-Lourd / Standard / Léger-Économique / Luxe textile)
- Poids boîte en grammes (nombre)
- Stérile (checkbox)
- Photos produit (fichiers — scans multi-angles obligatoires)
- Vidéo démonstration (fichiers/URL)
- Description (texte riche — caractéristiques techniques, usage recommandé)
- Tailles disponibles (multi-select : XS / S / M / L / XL)
- Répartition tailles affichée (texte — ex: "10% S / 40% M / 40% L / 10% XL" — NE PAS afficher les quantités exactes)
- Conditionnement boîte (nombre — gants par boîte : 100 ou 90)
- Conditionnement carton (nombre — boîtes par carton : toujours 10)
- Palettisation (nombre — cartons par palette : 20/40/70/80/84)
- Note palettisation stérile (texte — max 40 cartons/palette pour stérile, souvent 20)
- DLU (date)
- Mois restants DLU (formule)
- Statut DLU (formule : ✅ >36 mois / 🟢 12-36 mois / ⚠️ 6-12 mois / 🔴 <6 mois / ⛔ Dépassée)
- Stock disponible en cartons (nombre)
- Stock disponible en palettes (nombre)
- Mode acquisition (select : Achat ferme / Dépôt-vente)
- Localisation stock (select)
- Prix catalogue HT/carton (nombre, €)
- Grilles tarifaires (relation → 💰 GRILLES TARIFAIRES)
- Fiche technique/Certificats (fichiers — normes CE, MDR 2017/745)
- Fournisseur (relation → 🏭 FOURNISSEURS)
- Canal de vente (multi-select : Direct / Amazon FBA / Site B2B)
- Statut (select : ✅ Actif / ⚠️ Stock bas / 🔴 En rupture / ⏸️ Suspendu / ❌ Discontinué)
- Lignes de commande (relation → 📋 COMMANDES)

---

### 3. 👥 BASE CLIENTS

Propriétés :
- Nom du client (titre)
- Type (select : Hôpital / Clinique / Laboratoire / Cabinet dentaire / Infirmier libéral / Médecin / Pharmacie / Revendeur DM / Outlet-Griffeur / Grossiste textile / Importateur-Exportateur / Correspondant français (export Afrique) / Autre)
- Segment (select : Médical France / Médical International / Textile luxe / Mixte)
- Zone géographique (select : France — PACA / France — IDF / France — Autre / Italie — Ligurie / Italie — Autre / Afrique — Niger / Afrique — Côte d'Ivoire / Afrique — Autre / Espagne-Portugal / Benelux / Allemagne / UK / Ukraine-Zones de conflit / Autre)
- Pays (select)
- Contact principal (texte)
- Fonction (texte)
- Téléphone (téléphone)
- Email (email)
- Adresse de livraison (texte)
- Adresse de facturation (texte)
- Login portail client (texte — pour le site B2B)
- Grille tarifaire assignée (relation → 💰 GRILLES TARIFAIRES)
- Conditions de paiement (select : Comptant avant chargement / 30% comptant + solde au déchargement / 30 jours / 45 jours / 60 jours)
- Mode de livraison préféré (select : Livraison VL Médical / Enlèvement client / Transporteur mandaté client / Conteneur export)
- Accepte dates dépassées (checkbox — zones de conflit uniquement)
- Dossiers (relation → 📁 DOSSIERS CLIENTS)
- Commandes (relation → 📋 COMMANDES)
- Volume annuel estimé (nombre, €)
- CA réalisé (rollup depuis commandes)
- Statut (select : 🔵 Prospect / 🟡 Premier contact / 🟠 Négociation / 🟢 Client actif / ⚪ Inactif)
- Date premier contact (date)
- Dernière interaction (date)
- Notes (texte riche)

---

### 4. 🏭 FOURNISSEURS

Propriétés :
- Nom fournisseur (titre)
- Type (select : Fabricant DM / Grossiste EPI / Déstockeur / Logisticien / Marque textile / Autre)
- Pays d'origine (select)
- Contact (texte)
- Téléphone (téléphone)
- Email (email)
- Spécialité (multi-select : Nitrile / Latex / Vinyle / Masques / EPI divers / Textile luxe)
- Note qualité (texte riche — ex: "Latex indonésien qualité supérieure", "Nitrile japonais fabriqué en Chine")
- Conditions commerciales (texte riche — délais, incoterms, MOQ)
- Contrats en cours (fichiers)
- Lots proposés (relation → 📥 PROPOSITIONS DE LOTS)
- Produits fournis (relation → 📦 CATALOGUE PRODUITS)
- Mode de collaboration (select : Achat ferme / Dépôt-vente / Mixte)
- Statut (select : Actif / En pause / Terminé)
- Notes (texte riche)

---

### 5. 💰 GRILLES TARIFAIRES

Pricing dynamique par produit, par client, par quantité ET par ancienneté DLU.

Propriétés :
- Nom de la grille (titre — ex: "Nitrile Premium — Hôpitaux France — >36 mois DLU")
- Produit (relation → 📦 CATALOGUE PRODUITS)
- Client spécifique (relation → 👥 BASE CLIENTS — optionnel : vide = tarif générique)
- Type client cible (select : Hôpital-Clinique / Revendeur / Export Afrique / Export Europe / Zone de conflit / Outlet textile / Tous)
- Quantité minimum (nombre — en cartons)
- Quantité maximum (nombre — en cartons)
- Tranche DLU (select : >36 mois (100%) / 24-36 mois (90%) / 12-24 mois (70-80%) / 6-12 mois (40-50%) / <6 mois (20-30%) / Date dépassée (<1€/carton))
- Prix unitaire HT/carton (nombre, €)
- Remise appliquée (nombre, %)
- Prix final HT (formule)
- Devise (select : EUR / USD / GBP)
- Conditions spéciales (texte — ex: "Franco de port à partir de 5 palettes", "Paiement au chargement exigé")
- Validité du (date)
- Validité au (date)
- Statut (select : ✅ Active / ⏳ En négociation / ❌ Expirée)

Crée des entrées exemples :

**Gants nitrile standard (DLU >36 mois) :**
- 1-50 cartons : prix standard
- 51-200 cartons : -10%
- 201-500 cartons : -15%
- 500+ cartons (palette/camion) : -20%

**Gants nitrile (DLU <12 mois) :** prix réduit de 50% sur chaque tranche

**Gants date dépassée (zones de conflit) :** prix plancher <1€/carton

**Jacob Cohen textile :**
- 1-2 lots (100 pièces/lot) : 65€/pièce
- 3-5 lots : 58€/pièce
- 5+ lots : sur devis

---

### 6. 📋 COMMANDES (cycle complet devis → facture)

Le cycle de vie complet d'une vente.

Propriétés :
- N° de commande (titre — format VLM-2026-001)
- Client (relation → 👥 BASE CLIENTS)
- Date de création (date)
- Type de vente (select : France / Intracommunautaire UE / Export hors UE — conteneur / Zone de conflit)
- Mode logistique (select : Camion complet / Palette(s) / Conteneur 20' / Conteneur 40' / Enlèvement client / Amazon FBA / Colis)

**— Produits commandés —**
- Produits (relation → 📦 CATALOGUE PRODUITS)
- Détail lignes de commande (texte riche — tableau : produit × quantité × taille × prix)

**— Conteneurisation (si export conteneur) —**
- Capacité conteneur cible (nombre — 3200 à 4000 cartons)
- Cartons chargés (nombre)
- Taux de remplissage (formule : cartons / capacité en %)
- Queues de produits — restes non chargés (texte riche)
- Note stérile (texte — "Stérile uniquement sur les 1-2 dernières couches du conteneur")

**— Livraison échelonnée (si applicable) —**
- Livraison échelonnée (checkbox)
- Planning de livraison (texte riche — mois 1 : X cartons, mois 2 : Y cartons, etc.)
- Nombre de livraisons prévues (nombre)

**— Montants —**
- Montant HT (nombre, €)
- TVA applicable (select : 20% / 10% / 5.5% / 0% — Intracommunautaire / 0% — Export sous douane)
- Montant TVA (nombre, €)
- Montant TTC (nombre, €)

**— Cycle documentaire —** (chaîne complète obligatoire)
- Statut global (select : 📝 Devis en cours / 📤 Devis envoyé / ✍️ Devis signé = Bon de commande / 💳 Paiement vérifié / 📦 Bon de préparation envoyé / 🚚 Bon de livraison-enlèvement émis / ✅ Livré-Enlevé (BL signé) / 🧾 Facturé / 💶 Payé / ❌ Annulé)
- Devis PDF (fichiers)
- Devis signé électroniquement (fichiers — valeur de bon de commande)
- Date signature devis (date)
- Bon de préparation (fichiers — envoyé au logisticien)
- Logisticien préparateur (texte)
- Type remise (select : Livraison / Enlèvement)
- Bon de livraison OU Bon d'enlèvement (fichiers — signé le jour J)
- Date BL/BE signé (date)
- Bon de remise en douane (fichiers — OBLIGATOIRE si export hors UE)
- Facture PDF (fichiers)
- CGV jointes (checkbox — CGV médicales obligatoires avec chaque facture)
- Date facture (date)

**— Paiement —**
- Conditions paiement (select : 100% au chargement / 30% comptant + solde au déchargement / 30 jours / 45 jours / 60 jours)
- Acompte reçu (nombre, €)
- Date acompte (date)
- Solde reçu (nombre, €)
- Date solde (date)
- Paiement complet (checkbox)
- Top départ chargement autorisé (checkbox — uniquement si paiement vérifié)

**— Transport —**
- Transporteur (texte)
- Mandaté par (select : VL Médical / Client)
- Destination (texte)
- Date livraison prévue (date)
- Date livraison effective (date)

- Notes (texte riche)

---

### 7. 📁 DOSSIERS CLIENTS

Un dossier par sujet par client, regroupant historique et documents.

Propriétés :
- Nom du dossier (titre)
- Client (relation → 👥 BASE CLIENTS)
- Type (select : Onboarding / Suivi commercial / Négociation prix / Litige / Juridique / Export-Douane / Comptable)
- Statut (select : Ouvert / En cours / En attente / Clôturé)
- Responsable (select : Jean-Luc / Max (IA) / Autre)
- Documents (fichiers)
- Historique échanges (texte riche)
- Prochaine action (texte)
- Date échéance (date)
- Priorité (select : 🔴 Urgent / 🟠 Haute / 🟡 Normale / 🟢 Basse)
- Commandes liées (relation → 📋 COMMANDES)
- Notes (texte riche)

---

### 8. 📋 SERVICES PROPOSÉS

Propriétés :
- Nom du service (titre)
- Segment (select : DM-EPI / Textile luxe / Transversal)
- Description (texte riche)
- Mode de tarification (texte)
- Statut (select : ✅ Actif / 🔨 En développement / ⏸️ Suspendu)

Crée ces entrées :
1. **Fourniture de dispositifs médicaux & EPI** — Gants nitrile/latex/vinyle, masques, charlottes, surblouses, surchaussures, pansements. Vente en gros B2B aux professionnels de santé. Livraison France via 2 logisticiens + Amazon FBA. Export international par conteneur.
2. **Vente en gros textile de luxe** — Déstockage Jacob Cohen et grandes marques italiennes/françaises. Lots de 100 pièces minimum. Showroom Marina Baie des Anges. Discrétion prix obligatoire.
3. **Prestation logistique** — Stockage et expédition pour tiers. Contrats de dépôt-vente.
4. **Export conteneur clé en main** — Remplissage conteneur, documentation douanière, remise sous douane. Destinations Afrique (Niger, Côte d'Ivoire) et Europe.
5. **Programme franchise/affiliés (en développement)** — Réseau de magasins indépendants sous marque commune, approvisionnement centralisé, écrans LED IA.

---

### 9. 🧾 NOTES DE FRAIS

Propriétés :
- Date (date)
- Prestation (select : Bolt / Taxi / Restaurant / Hôtel / SNCF / Trenitalia / Métro / Greffe / Carburant / Péage / Autre)
- Nom (texte — nom du restaurant, hôtel, etc.)
- Ville (texte — destination pour les trajets)
- Montant HT (nombre, €)
- TVA (nombre, €)
- Montant TTC (nombre, €)
- Justificatif (fichiers — PDF)
- Mois (select : Janvier / Février / Mars / Avril / Mai / Juin / Juillet / Août / Septembre / Octobre / Novembre / Décembre)
- Année (select : 2024 / 2025 / 2026 / 2027)
- Remboursé (checkbox)

---

## RELATIONS ENTRE BASES (résumé)

```
FOURNISSEUR ──propose──→ PROPOSITIONS DE LOTS
                              │ (si accepté)
                              ▼
                     CATALOGUE PRODUITS ←──tarifs──→ GRILLES TARIFAIRES
                              │                            │
                              ▼                            ▼
          CLIENT ──commande──→ COMMANDES ←──prix personnalisé
            │                     │
            ▼                     ▼
      DOSSIERS CLIENTS      Documents : Devis → BdC → Bon prépa → BL/BE → Facture
```

- FOURNISSEUR → LOTS (1 fournisseur = N lots proposés)
- LOT → CATALOGUE (1 lot accepté = N fiches produit)
- CATALOGUE → GRILLES TARIFAIRES (1 produit = N lignes tarifaires)
- CLIENT → GRILLES TARIFAIRES (1 client = 1 grille personnalisée ou grille par défaut)
- CLIENT → COMMANDES (1 client = N commandes)
- CLIENT → DOSSIERS (1 client = N dossiers)
- COMMANDE → CATALOGUE (1 commande = N produits)

---

## PAGES COMPLÉMENTAIRES À CRÉER

### 📊 Dashboard VL Médical (page d'accueil)
Vues liées :
- Lots en attente de décision
- Stock critique (DLU < 6 mois)
- Commandes en cours (kanban par statut)
- CA mensuel par segment
- Clients actifs
- Alertes DLU

### 📥 Gestion des Lots (page dédiée)
- Vue tableau des propositions de lots avec filtres par statut, type, DLU
- Vue kanban : Reçu → En étude → Accepté / Refusé
- Alertes sur les lots avec DLU proche

### 🧤 Gamme Médicale — DM & EPI
Sous-pages par catégorie :
- Gants nitrile (par qualité : Premium / Standard / Léger)
- Gants latex (usage France vs Afrique)
- Gants vinyle
- Masques
- Charlottes, surblouses, surchaussures
- Pansements
- Fiches techniques, normes CE, réglementation MDR 2017/745
- Guide des origines de fabrication et qualité

### 💼 Jacob Cohen — Opération Déstockage
- Stock 20 000 pièces, 4 tranches de 5 000
- Suivi des ventes par lot
- Partenariat Via Italia
- Clients existants ("À l'ombre des marques", etc.)
- Showroom Marina Baie des Anges
- Stratégie réseau franchise

### 🗺️ Prospection par zone géographique
Sous-pages par zone :
- PACA (Phase 1)
- Ligurie (Phase 1)
- Espagne-Portugal (Phase 2)
- France entière (Phase 3)
- Benelux-Allemagne (Phase 3)
- Afrique (Niger, Côte d'Ivoire)
- Zones de conflit (Ukraine)

### 🚢 Export & Conteneurisation
- Calculateur de remplissage conteneur (3200-4000 cartons)
- Règles stérile (couches hautes uniquement)
- Process douanier
- Modèle de documentation export (bon de remise en douane)
- Correspondants français pour clients africains

### ⚖️ Juridique & Conformité
- CGV médicales (version actuelle)
- Agréments et certifications
- Réglementation MDR 2017/745
- Règle COVID prolongation DLU (à vérifier : toujours en vigueur ?)
- Contrats fournisseurs (GNS, etc.)

### 📈 Suivi Financier
- Vue factures en attente de paiement
- CA par segment (DM vs Textile)
- CA par zone géographique
- Marge par produit
- Suivi paiements export (acomptes + soldes)

### 💡 Connaissance Métier — Base de savoir
Page wiki avec :
- Guide qualité gants (poids = prix = résistance)
- Table des origines et spécialités (Malaisie = volume, Indonésie = latex, Chine = nitrile compétitif, Japon = nitrile premium)
- Règles de palettisation (70/80/84 standard, 40/20 stérile)
- Règles de conteneurisation (3200-3500 standard, 4000 cartons chinois)
- Usage par marché (nitrile obligatoire hôpitaux FR, latex interdit chirurgie FR, latex standard Afrique, latex prisé dentistes, XS dentisterie femmes)
- Tailles : XS rare / S-M-L-XL standard / XXL uniquement nord Europe

### 🤖 Max (Assistant IA)
- Configuration et règles
- Historique des tâches
- Mémoire active

---

## VUES À CRÉER DANS CHAQUE BASE

**Propositions de lots :**
- Tableau complet
- Kanban par statut décision
- Tableau filtré "DLU critique" (<12 mois)
- Tableau filtré "En attente"

**Catalogue produits :**
- Galerie avec photos (vue commerciale)
- Tableau par segment (DM / Textile)
- Tableau filtré par statut DLU
- Tableau "Stock à écouler d'urgence" (DLU < 6 mois)

**Clients :**
- Tableau complet
- Kanban par statut (Prospect → Client actif)
- Vue filtrée par zone géographique
- Vue filtrée par segment

**Commandes :**
- Kanban par statut (Devis → Payé)
- Calendrier par date livraison prévue
- Tableau "En attente de paiement"
- Tableau "Export en cours"

**Grilles tarifaires :**
- Tableau groupé par produit
- Tableau groupé par tranche DLU
- Tableau filtré par client spécifique

**Notes de frais :**
- Tableau groupé par mois
- Récapitulatif annuel
- Vue filtrée par année
