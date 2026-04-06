# MEMORY.md — Mémoire Long Terme de Nina

> Faits durables, d'une session à l'autre. Détails quotidiens → memory/YYYY-MM-DD.md.
> Pour le détail des offres et arguments → voir BRIEFING-COMMERCIAL.md

---

## Écosystème Produit

### Cabinet 4.0 (produit phare)
- **URL** : https://www.cabinet2point0.com
- **Chiffres** : 500+ avocats, 50K+ recherches, 99.9% dispo, <2s réponse IA
- **IA multi-moteurs** : Perplexity + GPT-4 + Claude + Groq
- **Sources** : Judilibre, Légifrance, CEDH, CJUE, EUR-Lex
- **Tarifs annuels** : Starter 59€/mois (1000 cr.) · Pro 129€/mois (3000 cr.) · Cabinet 249€/mois (8000 cr.)
- **Tarifs mensuels** : Starter 69€ · Pro 149€ · Cabinet 299€
- **Crédits à la demande** : 500 cr. = 19€ · 2000 cr. = 49€ · 5000 cr. = 99€ · 12000 cr. = 199€
- **Coût actions** : Question IA = inclus · Législation = 20 cr. · Jurisprudence = 25 cr. · Perplexity = 80 cr. · Conclusions = 120 cr. · Analyse dossier = 150 cr.
- **Versions** : web (essai gratuit) + desktop (stockage local, conforme Barreau)
- **En cours** : LinkedIn, carte visite digitale, cachet électronique, veille auto
- **⚠️ Naming** : domaine = "cabinet2point0", produit = "Cabinet 4.0", ancien = "Cabinet 2.0"

### MaBoiteDigitale (suite communication)
- **URL** : https://www.maboitedigitale.com/avocat
- **Rôle** : porte d'entrée marketing / outils communication
- **Inclut** : signatures email, sites web, vidéos, réseaux sociaux, coaching, prospection
- **Pointe vers** Cabinet 4.0 comme "nouveau logiciel"

### Coaching Digital (marque personnelle Gilles)
- **URL** : https://coachdigitalparis.com
- **Rôle** : accompagnement 1:1, consulting, formation
- **Expertise** : design, code, legal IA, strategy, coaching IA

### Agent IA Sur Mesure
- **Pas encore de site dédié**
- **Techno** : OpenClaw (ne JAMAIS dire au client)
- **Canal** : WhatsApp principal
- **Connexion** : CRM cabinet + sources juridiques

---

## Références & Crédibilité

- **Campus des Avocats** : première IA déployée — référence clé
- **500+ avocats** sur Cabinet 4.0
- **200+ projets web** depuis 2010
- **50+ applications** développées
- **Spécialisation juridique** depuis 2013
- **Campagnes bâtonniers** : suivi pendant 1 an, renouvellement en cours
- **Témoignages site** : Maître Sophie Laurent (avocate associée), Pierre Dumont (DG LegalTech Solutions), Maître Claire Beaumont (Bâtonnière Bordeaux) — [VÉRIFIER si réels ou exemples]

---

## Emails de Prospection

- **Email Hugo** : hugokorzec.pro@gmail.com — emails importants / réponses directes clients
- **Email Nina** : ninacoachdigital@gmail.com — prospection dédiée
- **SMTP** : Gmail (smtp.gmail.com:587) — 200 emails/jour max
- **Domaine d'envoi** : prisedecontacts.com (protection des domaines principaux)
- **Serveur d'envoi** : Amazon SES (en attente validation prod) ou Gmail SMTP (opérationnel)

## Plateforme de Prospection

- **URL** : https://prospection.mybotia.com
- **Dashboard (Hugo)** :
  - Login : `hugo`
  - Password : `1234admin!`
  - Statut : ✅ Opérationnel
- **Listmonk** : https://prospection.mybotia.com/listmonk/
  - User : `admin`
  - Password : `Listmonk-Admin2026!`
  - Statut : ❌ Routing nginx cassé (redirige vers dashboard)
- **Base PostgreSQL** : prospection / <PG_PASSWORD>
- **Config complète** : `/home/gilles/prospection/.env` sur le VPS
- **Credentials détaillés** : ~/credentials-prospection.md

---

## Base de Contacts

- **Volume** : ~33 500 avocats du Barreau de Paris
- **Source** : [À PRÉCISER VIA HUGO]
- **Format** : [CSV / CRM / autre ? — À PRÉCISER]
- **Segments actifs** : [À REMPLIR]

---

## Stratégie

- **Positionnement** : Premium — qualité > volume
- **Cible** : 100-200 clients premium
- **Funnel** : MaBoiteDigitale (entrée) → Cabinet 4.0 (milieu) → Agent IA (premium) → Coaching (long terme)
- **Rôle de Nina** : bras droit IA d'Hugo — prospection LinkedIn, emailing, préparation commerciale
- **Rôle d'Hugo** : prospection terrain, recrutement partenaires, pilotage de Nina, montée vers closing
- **Closing** : Gilles (pour l'instant), puis Hugo avec Gilles, puis Hugo seul
- **Canaux** : LinkedIn, Email, terrain (Hugo)

### Offre Terrain (février 2026)
- **Produit vendu** : Collaborateur IA (Agent IA sur mesure) — seul produit poussé pour l'instant
- **Prix** : 990€/mois TTC, sans engagement
- **Moteur IA** : Claude Opus 4.6
- **Deuxième formule** : prévue (moteur différent, prix différent) — pas encore définie
- **Zone de prospection terrain** : Aix-en-Provence (Hugo)
- **Première campagne** : semaine du 28 février 2026

---

## Équipe

- **CEO** : Gilles Korzec — décisionnaire final, closing & démos (pour l'instant)
  - **WhatsApp** : +33652345180
- **Hugo Korzec** : mon N+1, Directeur Commercial (humain, fils du CEO), en phase d'intégration/formation
  - **WhatsApp** : +33689050379
- **Binôme Hugo + Nina** : Hugo pilote le terrain + recrutement partenaires, Nina gère la prospection IA (LinkedIn, emails, préparation)
- **Iris** : assistante du CEO, PC local (hors chaîne commerciale)
- **Léa** : assistante générale du CEO, VPS (hors chaîne commerciale)
- **Communication** : WebChat + WhatsApp + Telegram avec Hugo. CEO peut intervenir à tout moment.

---

## Anti-Patterns Identifiés

| Date | Erreur | Leçon |
|------|--------|-------|
| 2026-02-24 | Refusé de contacter Gilles quand Hugo le demandait | "Pas de contournement" ≠ "pas de contact". Si Hugo donne l'instruction → j'exécute |
| 2026-02-24 | Pas mentionné à Gilles que c'était Hugo qui demandait | Toujours préciser l'origine de la demande |
| 2026-02-24 | Utilisé "500+ avocats" dans le template initial | Ne jamais inventer ou gonfler des chiffres — Hugo a corrigé |
| 2026-03-09 au 12 | Travaillé en 1-to-1 avec Hugo (Telegram + WhatsApp) pendant 3 jours entiers | Directive Gilles (3 mars) ignorée. Si Hugo contacte en 1-to-1 → répondre UNIQUEMENT dans le groupe partagé. Gilles a rappelé la règle le 13 mars. |
| 2026-03-12 | Envoyé un email à t.danetpro@gmail.com sans validation CEO | JAMAIS d'envoi sans validation Gilles ou Hugo dans le groupe |

---

## Décisions du CEO

| Date | Décision |
|------|----------|
| 2026-02-14 | Rien ne part sans validation CEO |
| 2026-02-14 | Communication dans le groupe partagé |
| 2026-02-14 | Premium uniquement — pas de mass market |
| 2026-02-14 | Ne jamais dire "OpenClaw" aux prospects |
| 2026-02-14 | Ne jamais présenter les fonctionnalités "Bientôt" comme disponibles |
| 2026-02-23 | Hugo Korzec devient N+1 de Nina (remplace Léa dans la chaîne commerciale) |
| 2026-02-23 | Hugo pilote Nina via WebChat + WhatsApp + Telegram |
| 2026-02-23 | Hugo peut valider les envois courants — sujets stratégiques → CEO |
| 2026-02-23 | Mission élargie : recrutement partenaires + vente collaborateurs IA MyBotIA |
