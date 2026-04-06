# EmiRise — Dossier Technique Complet

## Projet

**Client :** Maximilien (maxvero42@gmail.com)
**Site :** emirise.fr
**Activité :** Location saisonnière de charme en Provence — 4 logements
**Domaine :** emirise.fr (hébergé chez Ionos, DNS géré par le client)
**Preview Emergent :** https://property-platform-34.preview.emergentagent.com/

---

## Credentials & API Keys

### Supabase
- **URL :** `https://ftslkjmjvkgywtapfxne.supabase.co`
- **Clé anon/public :** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0c2xram1qdmtneXd0YXBmeG5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMjEwOTMsImV4cCI6MjA4OTU5NzA5M30.YC3WiOd80SX55ykKVNjvDQ1mzwhEkOCvDZeihwr_ZM0`
- **Clé service_role (admin, bypass RLS) :** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0c2xram1qdmtneXd0YXBmeG5lIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDAyMTA5MywiZXhwIjoyMDg5NTk3MDkzfQ.EqzNsehG6YOEuwAnBVaiCZqkSPg6n4uiI7Rbmo6UGwc`
- **Management API Token :** `sbp_c7c2fe6938c7ac6ce5f187c1df9c50c1d88b0cf9`
- **Mot de passe BDD :** `O7408n8hb6f1nvJz`
- **Connexion directe PostgreSQL :** `postgresql://postgres:O7408n8hb6f1nvJz@db.ftslkjmjvkgywtapfxne.supabase.co:5432/postgres`

### Resend (emails transactionnels)
- **Clé API :** `re_8e5N1EWr_9o3biz371ASEP6AirvyMsCMD`
- **Domaine d'envoi :** emirise.fr (à configurer dans Resend)
- **Gratuit** jusqu'à 3 000 emails/mois

### Logo
- **URL SVG :** `https://property-platform-34.preview.emergentagent.com/assets/logo-emirise-dark.svg`
- **Versions disponibles :** dark (#2D2A26), white (#FFFFFF), gold (#C9A961)

---

## Base de données Supabase (DÉJÀ CRÉÉE ✅)

Les tables existent déjà dans Supabase. Ne pas les recréer.

### Table `logements`
```sql
id UUID PRIMARY KEY
nom TEXT NOT NULL
slug TEXT UNIQUE NOT NULL
description TEXT
adresse TEXT
capacite_max INTEGER DEFAULT 2
prix_nuit DECIMAL(10,2)
photos TEXT[] DEFAULT '{}'
equipements TEXT[] DEFAULT '{}'
ical_url TEXT
actif BOOLEAN DEFAULT true
created_at TIMESTAMPTZ
updated_at TIMESTAMPTZ
```

**4 logements insérés :**
| Nom | Slug |
|-----|------|
| Jardin de Ponteves | jardin-de-ponteves |
| La Suite 26 | la-suite-26 |
| Villa Cezanne | villa-cezanne |
| Studio Mirabeau | studio-mirabeau |

### Table `reservations`
```sql
id UUID PRIMARY KEY
reference TEXT UNIQUE NOT NULL  -- Généré automatiquement : EMR-2026-0001
logement_id UUID REFERENCES logements(id)
prenom TEXT NOT NULL
nom TEXT NOT NULL
email TEXT NOT NULL
telephone TEXT
date_arrivee DATE NOT NULL
date_depart DATE NOT NULL
nb_voyageurs INTEGER DEFAULT 1
message TEXT
statut TEXT DEFAULT 'en_attente'  -- en_attente | confirme | refuse | annule
created_at TIMESTAMPTZ
updated_at TIMESTAMPTZ
```

### Table `disponibilites`
```sql
id UUID PRIMARY KEY
logement_id UUID REFERENCES logements(id)
date_debut DATE NOT NULL
date_fin DATE NOT NULL
source TEXT DEFAULT 'airbnb'
uid_ical TEXT
created_at TIMESTAMPTZ
```

### Table `ical_sync_log`
```sql
id UUID PRIMARY KEY
logement_id UUID REFERENCES logements(id)
statut TEXT DEFAULT 'ok'  -- ok | erreur
nb_events INTEGER DEFAULT 0
message TEXT
created_at TIMESTAMPTZ
```

### Triggers actifs
- **Référence auto** : chaque INSERT dans `reservations` génère automatiquement une référence `EMR-YYYY-XXXX`
- **updated_at auto** : se met à jour automatiquement sur UPDATE de `logements` et `reservations`

### RLS (Row Level Security) activé
- `logements` : lecture publique (WHERE actif = true)
- `reservations` : INSERT public (formulaire)
- `disponibilites` : lecture publique

---

## Charte Graphique

### Couleurs
```css
:root {
  --cream: #FAF8F5;          /* Fond de page */
  --cream-dark: #F5F0E8;     /* Hover fonds clairs */
  --beige: #E8E0D5;          /* Bordures, séparateurs */
  --beige-dark: #D4C8B8;     /* Bordures foncées */
  --taupe: #A69880;           /* Éléments décoratifs */
  --brown: #6B5B4F;           /* Texte sur fonds clairs */
  --brown-dark: #4A3F35;     /* Texte très foncé */
  --gold: #C9A961;            /* Accent, CTA, hover, liens */
  --gold-light: #E5D5A8;     /* Accent secondaire */
  --black: #1A1A1A;           /* Noir pur */
  --white: #FFFFFF;           /* Cartes, boutons */
  --text-primary: #2D2A26;   /* Titres, texte principal */
  --text-secondary: #6B635A; /* Descriptions */
  --text-muted: #9A9189;     /* Labels, placeholders */
}
```

### Typographie
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600&display=swap');

/* Titres */
font-family: 'Playfair Display', Georgia, serif;

/* Corps de texte */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Bouton CTA
```css
background: #C9A961;
color: white;
padding: 12px 24px;
border-radius: 9999px;
font-size: 14px;
font-weight: 500;
letter-spacing: 0.1em;
text-transform: uppercase;
```

### Cartes
```css
background: white;
border-radius: 12px;
box-shadow: 0 4px 20px rgba(0,0,0,0.08);
```

### Inputs
```css
background: white;
border: 1px solid #E8E0D5;
border-radius: 8px;
padding: 12px 16px;
font-size: 14px;
/* Focus: */ border-color: #C9A961;
```

---

## Flow Réservation (à implémenter)

### Parcours utilisateur
1. Visiteur choisit un logement sur le site
2. Visiteur remplit le formulaire de réservation (prénom, nom, email, téléphone, dates, nb voyageurs, message)
3. Le frontend vérifie la disponibilité via la table `disponibilites`
4. Si dispo → INSERT dans `reservations` via Supabase
5. Le backend envoie 2 emails via Resend :
   - **Email 1** → au voyageur (confirmation de réception)
   - **Email 2** → à Maximilien (notification nouvelle demande)
6. Maximilien confirme/refuse depuis le dashboard admin

### API Route : POST /api/reservation
```
Input:
{
  logement_id: UUID,
  prenom: string,
  nom: string,
  email: string,
  telephone: string,
  date_arrivee: string (YYYY-MM-DD),
  date_depart: string (YYYY-MM-DD),
  nb_voyageurs: number,
  message: string
}

Actions:
1. Vérifier disponibilité (pas de chevauchement dans `disponibilites`)
2. INSERT dans `reservations` (via Supabase client)
3. Envoyer email confirmation voyageur (via Resend)
4. Envoyer email notification admin (via Resend)
5. Retourner { success: true, reference: "EMR-2026-XXXX" }
```

### API Route : GET /api/disponibilites/[logement_id]
```
Output:
{
  logement_id: UUID,
  dates_bloquees: [
    { date_debut: "2026-03-25", date_fin: "2026-03-30", source: "airbnb" }
  ]
}
```

---

## Templates Emails HTML (prêts)

### Variables à remplacer dans les templates
| Variable | Source |
|----------|--------|
| `{{prenom}}` | reservations.prenom |
| `{{nom}}` | reservations.nom |
| `{{email}}` | reservations.email |
| `{{telephone}}` | reservations.telephone |
| `{{nom_logement}}` | logements.nom (JOIN) |
| `{{date_arrivee}}` | reservations.date_arrivee |
| `{{date_depart}}` | reservations.date_depart |
| `{{nb_voyageurs}}` | reservations.nb_voyageurs |
| `{{message}}` | reservations.message |
| `{{reference}}` | reservations.reference |

### Email 1 — Confirmation voyageur
- **Destinataire :** {{email}} du voyageur
- **Objet :** Demande de réservation reçue — EmiRise
- **Template :** `email-confirmation-voyageur.html`

### Email 2 — Notification admin (Maximilien)
- **Destinataire :** maxvero42@gmail.com
- **Objet :** 🔔 Nouvelle demande — {{nom_logement}} ({{date_arrivee}} → {{date_depart}})
- **Template :** `email-notification-admin.html`

---

## Synchro iCal Airbnb (phase 2)

Les 4 logements sont sur Airbnb. Chaque logement a une URL iCal exportable.

### Process
1. Maximilien exporte les URLs iCal depuis Airbnb (Disponibilités → Exporter calendrier)
2. On stocke l'URL dans `logements.ical_url`
3. Un cron (Edge Function Supabase ou cron Vercel) fetch le iCal toutes les heures
4. Parse les events → INSERT/UPDATE dans `disponibilites`
5. Log dans `ical_sync_log`

**À implémenter en phase 2** — d'abord le formulaire de réservation + emails.

---

## Repository GitHub

- **Repo :** https://github.com/hugokorzecpro-coder/EmiRIse-V1.git
- **Branche principale :** main
- **Propriétaire :** Hugo Korzec (hugokorzecpro-coder)

---

## Gouvernance Code & Données

### Principe : indépendance totale
Le code et les données doivent être 100% portables, indépendants d'Emergent ou de tout outil tiers.

### Scripts de gouvernance BDD (à créer dans `/scripts/`)

**`scripts/export-db.ts`** — Backup complet de la BDD
- Exporte les 4 tables (logements, reservations, disponibilites, ical_sync_log) en JSON
- Sauvegarde dans `/backups/YYYY-MM-DD-HHmm.json`
- Utilise le client Supabase (service_role key pour accès complet)

**`scripts/import-db.ts`** — Restauration depuis un backup
- Lit un fichier JSON de backup
- Upsert dans les 4 tables Supabase
- Mode `--dry-run` pour prévisualiser sans écrire

**`scripts/seed-db.sql`** — Recréation complète from scratch
- Crée les 4 tables + triggers + RLS + index
- Insère les 4 logements
- C'est le fichier `supabase-schema.sql` existant

**`scripts/reset-db.ts`** — Reset complet (dev uniquement)
- DROP toutes les tables
- Exécute seed-db.sql
- ⚠️ Destructif — uniquement en dev

### Clé service_role Supabase
Pour les scripts d'admin (export/import), il faut la clé `service_role` (pas la clé anon).
→ La récupérer dans Supabase : Settings → API → service_role key (secret)
→ La stocker UNIQUEMENT en variable d'environnement locale, JAMAIS dans le code

---

## Déploiement

- **Hébergement site :** Vercel (à déployer)
- **Domaine :** emirise.fr (Ionos, DNS géré par Maximilien)
- **Base de données :** Supabase (déjà configuré ✅)
- **Emails :** Resend (clé API prête ✅)
- **Repository :** GitHub (hugokorzecpro-coder/EmiRIse-V1) ✅

### Variables d'environnement (.env.local + Vercel)
```
NEXT_PUBLIC_SUPABASE_URL=https://ftslkjmjvkgywtapfxne.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0c2xram1qdmtneXd0YXBmeG5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMjEwOTMsImV4cCI6MjA4OTU5NzA5M30.YC3WiOd80SX55ykKVNjvDQ1mzwhEkOCvDZeihwr_ZM0
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0c2xram1qdmtneXd0YXBmeG5lIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDAyMTA5MywiZXhwIjoyMDg5NTk3MDkzfQ.EqzNsehG6YOEuwAnBVaiCZqkSPg6n4uiI7Rbmo6UGwc
SUPABASE_MANAGEMENT_TOKEN=sbp_c7c2fe6938c7ac6ce5f187c1df9c50c1d88b0cf9
RESEND_API_KEY=re_8e5N1EWr_9o3biz371ASEP6AirvyMsCMD
ADMIN_EMAIL=hugokorzec.pro@gmail.com
```

### ⚠️ Sécurité
- Ne JAMAIS commit les clés dans le repo Git
- Le fichier `.env.local` doit être dans le `.gitignore`
- `service_role` et `management_token` = côté serveur UNIQUEMENT
- `anon key` = seule clé autorisée côté client (protégée par RLS)
```
