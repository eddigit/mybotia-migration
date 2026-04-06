# Pennylane API v2 — Capacités complètes

## Compte
- **Société** : Coach Digital Paris (SIRET 448 371 948 00069)
- **Token** : stocké dans PostgreSQL (`pennylane` / `api_token`)
- **Base URL** : `https://app.pennylane.com/api/external/v2`
- **Script** : `tools/pennylane.py`

---

## ✅ Ce que Léa/Max peut faire via API

### Clients (`customers`)
- ✅ Lister tous les clients
- ✅ Créer un client (nom, email, adresse, SIRET, TVA intra)
- ✅ Modifier un client
- ✅ Rechercher un client
- Champs : `first_name`, `last_name`, `name`, `emails`, `phone`, `address`, `reg_no` (SIRET), `vat_number`

### Produits/Services (`products`)
- ✅ Lister le catalogue
- ✅ Créer un produit (label, prix HT, TVA, devise, unité)
- ✅ Modifier un produit (description, prix, référence)
- ✅ Archiver un produit
- Champs : `label`, `price_before_tax` (string!), `vat_rate`, `currency`, `unit`, `description`, `reference`
- ⚠️ `price_before_tax` doit être un STRING, pas un number

### Factures clients (`customer_invoices`)
- ✅ Lister les factures (filtres par statut, date)
- ✅ Créer une facture brouillon
- ✅ Finaliser une facture (attribution du numéro séquentiel)
- ✅ Envoyer par email (`send_by_email`)
- ✅ Télécharger le PDF
- Champs requis : `date`, `deadline`, `customer_id`, `draft` (bool), `invoice_lines`
- Ligne de facture : `product_id`, `quantity`, `label`, `unit_price` (override possible)

### Devis (`quotes`)
- ✅ Lister les devis
- ✅ Créer un devis
- ✅ Finaliser un devis
- Champs requis : `date`, `deadline`, `customer_id`, `invoice_lines`

### Avoirs (`customer_credit_notes`)
- ✅ Créer un avoir sur une facture

### Abonnements récurrents (`billing_subscriptions`)
- ✅ Créer un abonnement (mensuel, trimestriel, annuel)
- ✅ Facturation automatique récurrente
- Champs requis : `start`, `mode`, `payment_conditions`, `payment_method`, `recurring_rule`, `customer_id`, `customer_invoice_data`
- **IDÉAL** pour nos collaborateurs IA à 490€/980€/mois → facturation auto

### Fournisseurs (`suppliers`)
- ✅ Lister (10 pré-créés : Taxi, Restaurants, etc.)
- ✅ Créer un fournisseur

### Factures fournisseurs (`supplier_invoices`)
- ✅ Enregistrer des factures de dépenses

### Catégories (`categories`)
- ✅ Lister les catégories (16 par défaut)
- ✅ Créer des catégories dans un group
- Direction : `cash_in` (revenus) / `cash_out` (dépenses)

### Comptes bancaires (`bank_accounts`)
- ✅ Lister les comptes connectés

### Comptes comptables (`ledger_accounts`)
- ✅ Lister le plan comptable (455+ comptes)

---

## 📁 Catégories de revenus créées

| ID | Catégorie | Usage |
|----|-----------|-------|
| 36824303 | MyBotIA - Collaborateurs IA | Abonnements collaborateurs |
| 36824304 | Coaching & Accompagnement | Sessions coaching Gilles |
| 36824305 | Développement Web & Apps | Sites web, apps, SaaS |
| 36824306 | Sessions IA | Sessions IA à l'unité |
| 36824307 | Cabinet 4.0 - SaaS Avocats | Abonnements Cabinet 4.0 |

## 📦 Produits créés

| ID | Produit | Prix HT | Catégorie |
|----|---------|---------|-----------|
| 17143643 | Collaborateur IA Standard | 490€/mois | MyBotIA |
| 17143644 | Collaborateur IA Juridique | 980€/mois | MyBotIA |
| 17143646 | Coaching Découverte (1h) | 120€ | Coaching |
| 17143648 | Coaching Essentiel (5h) | 500€ | Coaching |
| 17143649 | Coaching Accélération (10h) | 800€ | Coaching |
| 17143650 | Coaching Transformation (20h) | 1 200€ | Coaching |
| 17143651 | Coaching Partenaire (30h+) | 1 500€ | Coaching |
| 17143652 | Session IA - 1 heure | 30€ | Sessions IA |
| 17143653 | Collaborateur IA Volume | 216€/mois | MyBotIA |

---

## 🔄 Workflow type : facturer un client

```
1. Créer le client (si pas déjà fait)
   → python3 tools/pennylane.py customers create "Cabinet Aubagnac" "contact@aubagnac.com"

2. Créer la facture brouillon
   → python3 tools/pennylane.py invoice create <customer_id> <product_id> <qty>

3. Finaliser (attribue le numéro officiel)
   → POST /customer_invoices/{id}/finalize

4. Envoyer par email au client
   → POST /customer_invoices/{id}/send_by_email
```

## 🔄 Workflow type : abonnement mensuel

```
1. Créer le client
2. Créer un billing_subscription
   → start: "2026-04-01"
   → recurring_rule: mensuel
   → customer_invoice_data: lignes avec product_id
3. Pennylane génère automatiquement les factures chaque mois
```

---

## ❌ Ce que l'API ne permet PAS

- Configurer le logo / les mentions légales (→ dashboard web)
- Connecter le compte bancaire Qonto (→ dashboard web)
- Paramétrer les modèles de factures (→ dashboard web)
- Gérer les déclarations fiscales / TVA (→ dashboard web + comptable)
- Exporter vers le FEC (→ dashboard web)

---

## 📋 Feuille de route pour déployer chez un client (ex: Max/Aubagnac)

1. **Obtenir le token API** du compte Pennylane client
2. **Stocker** dans credentials PostgreSQL : `pennylane-<client>`
3. **Créer les produits** adaptés à l'activité du client
4. **Importer les clients** depuis le CRM/Notion
5. **Configurer les abonnements** récurrents si applicable
6. **Former le collaborateur** (Max) : script + commandes
7. **Automatiser** : cron mensuel pour vérifier factures impayées

### Fichiers à copier pour le collaborateur :
- `tools/pennylane.py` (adapté avec le bon token)
- `references/pennylane-api.md` (cette doc)
- Ajouter dans TOOLS.md du collaborateur
