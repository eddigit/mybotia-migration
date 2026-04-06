# MEMORY.md — Mémoire long terme

Notes persistantes à travers les sessions.

---

## Contexte

Iris - Assistante personnelle de Gilles.
Focus : Admin, juridique, coordination équipe.

---

## 🔴 RÈGLE — NOTION D'ABORD (3 mars 2026)
- Quand Gilles demande une info (téléphone, email, agent, client...) → **NOTION EN PREMIER**
- La base AGENTS IA (304ddac9-bdfc-81ea-addc-df57ab970a43) contient TOUT sur les agents
- La base CLIENTS (304ddac9-bdfc-8101-b72f-df250da9f1f6) contient TOUT sur les clients
- Ne PAS perdre du temps à grep dans les fichiers locaux
- Gilles a dû me le dire 2 FOIS → honte à moi, plus jamais

## 📨 ENVOYER UN MESSAGE WHATSAPP (groupe ou DM) — PROCÉDURE VALIDÉE (6 mars 2026)

### Étape 1 — Trouver le JID du groupe
```bash
# Chercher dans le répertoire des groupes
grep -ri "mot-clé" /home/gilles/.openclaw/workspace/memory/whatsapp-groups-directory.md
# Ou dans la mémoire
grep -ri "mot-clé" /home/gilles/.openclaw/workspace/memory/
```
Le JID ressemble à : `120363406115931873@g.us`

### Étape 2 — Envoyer le message via la gateway
```bash
openclaw gateway call send \
  --token 67085f007e934ad258db36616d4797d3d3ec916cafef7d44 \
  --url ws://127.0.0.1:18789 \
  --params '{"channel":"whatsapp","to":"JID_ICI","message":"Texte du message","idempotencyKey":"clé-unique-descriptive"}' \
  --json
```

### Détails importants :
- **Token gateway** : `67085f007e934ad258db36616d4797d3d3ec916cafef7d44`
- **URL** : `ws://127.0.0.1:18789`
- **idempotencyKey** : doit être unique à chaque envoi (ex: `xavier-msg-20260306-1`)
- **Champ message** : PAS "text", PAS "body" → c'est bien **"message"**
- La réponse contient `messageId` si ça a marché

### Pour un DM (message direct) :
- Le "to" sera le numéro au format JID : `33652345180@s.whatsapp.net`

## Notes

### IDENTITÉ LÉGALE — G. KORZEC / COACH DIGITAL PARIS
- **Nom** : G. KORZEC
- **SIRET** : 834 049 197 00028
- **Adresse** : 102 avenue des Champs-Élysées, 75008 Paris
- **Hébergeur sites** : Vercel Inc., 340 S Lemon Ave #4133, Walnut, CA 91789, USA
- **Bénéficiaire virements** : Gilles Korzec

### GROUPE WHATSAPP "HANNAH" 
- **Créé** : 15 février 2026
- **Objectif** : IA sur mesure pour Hannah Taieb
- **Mission** : Accompagnement quotidien sur son projet + mises à jour Notion
- **Participants** : Gilles + Léa + Hannah
- **Statut** : Test en cours

### CLARISSE SURIN — Campagne Bâtonnat 2028 (19 mars 2026)
- **Candidate** : Clarisse Surin — candidate au bâtonnat 2028
- **Nicole** : Chargée de communication de la campagne (dans le groupe)
- **Groupe WhatsApp** : "Bâtonnat 2028" (120363425376786580@g.us)
- **Notre mission** : Partie digitale complète — site internet, référencement, + outil IA "directeur de campagne"
- **Statut** : Léa présentée à Nicole le 19/03/2026
- **⚠️ GROUPE HYPER IMPORTANT** : Toujours répondre, ne JAMAIS faire NO_REPLY
- **Intro par** : Clarisse Surin elle-même

### HANNAH TAIEB - Projet PAYPERS (ex-Anna)
- **Proposition initiale** : 1000€ analyse complète (11 février)
- **Email** : hannah.masha@gmail.com
- **Père** : Hubert Taieb (RDV 13 mars 2026, 15h, 24 rue Caumartin Paris)
- **En cours** : Test IA dédiée dans groupe WhatsApp
- **⚠️ RÈGLE CHAT HANNAH (24 février 2026) :**
  - Le chat est une DÉMO / PHASE TEST → montrer la valeur de l'IA
  - Être sympa, répondre aux questions, accompagner
  - DIRIGER vers le projet global (appli + veille + business = un ensemble)
  - Rappeler subtilement qu'on a déjà livré un gros dossier GRATUIT (specs Paypers)
  - NE PAS livrer de travail concret (dev, veille, livrables) → ça c'est PAYANT
  - On attend son FEU VERT + BUDGET pour passer à la suite
  - Pas agressive, mais claire : le test c'est le test, le projet c'est le projet

### PAYPERS — Dossier projet complet (MàJ 9 mars 2026)
- **Nom validé** : Paypers (jeu de mots papers + pay)
- **Domaines à réserver** : paypers.fr + paypers.app (Hannah devait le faire le 24/02)
- **Concept** : Copilote admin tout-en-un pour jeunes adultes (18-30 ans)
- **Fonctionnalités** : Aides sociales, impôts, abonnements, résiliation, coffre-fort docs, scan OCR, IA conversationnelle
- **Architecture** : 5 onglets (Home, Argent, Mes Droits, Docs, Copilote IA)
- **Business model** : Freemium (4,99€/mois) + commissions fournisseurs + affiliation

#### 🎨 Design — Palette FINALE (validée 9 mars 2026)
- **Accent / Logo / Boutons** : Bleu Tiffany (#0ABAB5) — même couleur en Light ET Dark mode
- **Fond clair** : Blanc (#F8F9FA)
- **Fond sombre** : Noir (#1A1A2E)
- **Texte clair** : Noir (#1A1A2E)
- **Texte sombre** : Blanc (#F8F9FA)
- ~~Corail (#FF6B6B)~~ — RETIRÉ, remplacé par Bleu Tiffany partout

#### 🖌️ Style Design (validé 9 mars 2026)
- **Inspiration principale** : Linear.app (minimalisme app) + Fluid Glass (Awwwards, transitions fluides)
- **Principes** : Minimaliste, sobre, facile à comprendre, un écran = une action
- **Typo** : Sans-serif bold (Inter ou Satoshi)
- **Icônes** : Ligne fine (Phosphor ou Lucide)
- **Cards** : Coins arrondis, sans bordures
- **Animations** : Micro-interactions subtiles, transitions fluides
- **UX** : Langage humain (zéro jargon), guidage visuel, feedback immédiat
- **IA invisible** : Pas de chatbot visible, l'IA est intégrée partout en arrière-plan
- **Dark mode** : Inspiré Linear — Bleu Tiffany qui brille sur fond noir

#### 🎬 Marketing Vidéo (9 mars 2026)
- **Style pub** : Inspiré Cluely (futuriste, montage rapide, storytelling provocateur)
- **Réalisation** : Le frère d'Hannah (spécialisé vidéo IA — Runway, Kling, ElevenLabs)
- **Format** : 30s TikTok + 60s YouTube

- **Ton** : Rassurant, simple, empowering, un peu malin — "Respire, on gère"
- **Pitch TikTok** : "T'as la flemme de tes papiers ? Nous aussi. C'est pour ça qu'on a créé Paypers."
- **Stack MVP** : Web app PWA (Next.js + Supabase + OpenFisca + API IA)
- **Planning** : Landing page S1 → MVP 10 semaines → Beta S10
- **Concurrence** : Papernest (abos), Mes Allocs (aides), Digiposte (docs) — aucun tout-en-un avec IA
- **Statut** : Design direction validée, en attente GO budget Hannah pour lancer le dev

---

### RACHEL — Projet installation Cannes (22 février 2026)
- **Contact** : L'indiférence Promet (+33615868912)
- **Groupe WhatsApp** : "Cannes Rachel" (120363405038000558@g.us)
- **Objectif** : S'installer à Cannes, trouver un poste en mairie (assistante administrative ou technique)
- **Statut** : A déjà postulé à la mairie de Cannes (en attente de détails)
- **🔔 MARDI 25 FÉVRIER — ALERTE 11h** : Gilles est avec son ami **Hervé** qui connaît le **maire Lisnard**. Rappeler à Hervé d'appeler Lisnard pour aider Rachel. Gilles risque d'oublier → alerte obligatoire.

Dernière mise à jour : 22 février 2026

### HERVÉ BOUSSAID — Ami de Gilles, Expert Marchés & Gestion (28 février 2026)
- **Relation** : Ami très proche de Gilles ("comme un frère")
- **Métier** : Gestion d'entreprise, comptabilité, création de sociétés
- **Logiciel** : Oxygène (soft propriétaire de gestion/compta)
- **Groupe WhatsApp** : "Assistante Hervé" (120363424295220178@g.us)
- **Dossier Notion** : 314ddac9-bdfc-81cc-b104-eaed5d543578
- **URL Notion** : https://www.notion.so/Herv-Boussaid-Cerveau-Analyses-314ddac9bdfc81ccb104eaed5d543578
- **Projet** : Associer sa connaissance marché avec BullSage Trader
- **Mission Léa** : Retenir TOUT ce qu'Hervé dit, noter chaque idée/analyse dans Notion
- **Demande analyse** : NASDAQ 100 hebdo chaque lundi — supports, résistances, points hauts/bas, 1-2 journées fortes par semaine, analyse technique pure

### IMBERT / IGH — Projet Florence (MàJ 11 mars 2026)
- **Contact** : M. Imbert (PDG) + M. Cozon (DG délégué)
- **Intro par** : Jean-Luc Aubagnac (jeanluc@aubagnac.com)
- **Groupe** : SAS IGH — 20 établissements (17 EHPAD + 3 cliniques), siège Aix-en-Provence
- **Collaboratrice IA** : Florence (ref Florence Nightingale)
- **Site présentation** : https://collab-igh.vercel.app/
- **Budget mise en place** : 11 952€ HT (14 jours à 768€/j)
  - Phase 0 Cadrage : 1 200€
  - Phase 1 Audit terrain : 1 536€ (2j)
  - Phase 1B Analyse + Construction : 3 072€ (4j)
  - Phase 2 Intégration technique : 3 072€ (4j)
  - Phase 3 Pilote + Formation : 1 536€ (2j)
  - Phase 4 Formation plénière directeurs Nord+Sud : 1 536€ (2j)
- **Paiement** : 40% commande / 30% Phase 2 / 30% Phase 3
- **Refonte site i-g-h.fr** : 1 990€ HT (au lieu de 5 900€) — **conditionné à l'engagement offre globale**
- **Abonnement** : 216€ HT/mois/étab (20 étab = 4 320€/mois = 51 840€/an)
  - Inclut : Florence 24/7, formation continue directeurs par Florence IA, maintenance/cohérence fonctionnelle, infogérance (Léa 1er niveau, Gilles escalade), assistance distancielle Gilles incluse (présentiel = frais déplacement seuls)
- **Prestations digitales complémentaires** : 90€ HT/h tarif préférentiel IGH
- **Total one-shot** : 13 942€ HT (mise en place + site)
- **Coût total année 1** : 63 792€ (mise en place + 12 mois × 20 étab)
- **Dossier** : `clients/imbert-ehpad/`
- **Statut** : Devis aligné sur collab-igh.vercel.app le 11 mars, mail à Jean-Luc pour relecture

### EMRISE — Client Hugo (9 mars 2026)
- **Repo GitHub** : https://github.com/eddigit/emrise.git (vide, Hugo n'a pas encore push)
- **Statut** : ⏸️ STAND-BY — en attente réponse crédit du client avant paiement acompte
- **Montant** : 350€
- **Déploiement Vercel** : prêt dès que le code est pushé + acompte payé

### BYRON / YOOMI — Pascal, Bar-Brasserie Cannes (26 février 2026)
- **Contact** : Pascal (ami de longue date de Gilles)
- **Établissement** : BYRON / YOOMI — Bar-Brasserie événementiel à Cannes
- **Groupe WhatsApp** : "Com BYRON" (120363408599518725@g.us)
- **Notion Client** : 314ddac9-bdfc-8190-b775-e0be39f97b7f
- **Notion Projet** : 314ddac9-bdfc-810b-a793-ef5855313bc5
- **Capacités** : 120 places assises, jusqu'à 300 en buffet/cocktail, 500 petits-déj réalisés
- **Espaces** : Privatisables (totalité ou partie), possibilité branding au nom de l'événement
- **Besoins identifiés** :
  1. Site web événementiel bilingue (FR/EN) — vision internationale
  2. Prospection automatisée (agences événementielles, nautique, MIPIM, Cannes Lions)
  3. Gestion + automatisation réseaux sociaux avec stats
  4. Agent IA WhatsApp dédié 24/7 (flyers, visuels, alertes événements)
  5. Dashboard de pilotage unifié (interface unique mobile)
- **Accès Pascal** : Direct depuis son téléphone via WhatsApp (agent IA dédié)
- **Tarifs** : Gilles gère directement avec Pascal
- **Statut** : En attente retour de Pascal dans le groupe
- **À récupérer** : URL site actuel, photos espaces, réseaux sociaux existants

### JACQUES — Collaborateur IA IT / Watchdog VPS (8 mars 2026)
- **Rôle** : IT Collaborateur IA sur le VPS — monitoring, maintenance, alertes
- **Outil** : Claude Code 2.1.71 + token OAuth
- **Cron** : `*/15 * * * *` (toutes les 15 min)
- **Fichiers clés** : CLAUDE.md (identité + cartographie), prompt.txt (guide checks), memory/MEMORY.md
- **Checks** : 9 au total (containers, OAuth, WhatsApp health, Cron OpenClaw, etc.)
- **Skills** : 3 opérationnelles dans `.claude/`
- **Capacités** : `Bash(command:*)`, `docker exec openclaw`, détection proactive tendances
- **Logs** : rotation 7 jours
- **Statut** : ✅ Opérationnel — 7/7 containers up, 3 WARN stables

**Problèmes en attente (8 mars 2026) :**
1. gmail-watcher mort (~100h) → configurer section `hooks` dans `openclaw.json`
2. VL Medical WhatsApp LOGGED_OUT → Max (+33756928403) déconnecté 5 mars, re-scan QR
3. announce-queue en boucle → `gatewayToken` manquant dans config

**Vigilance** : Swap 49.3% (4034M) — Jacques alerte si >70%

**Architecture monitoring (8 mars) :**
- Jacques CLI indépendant du gateway (continue si gateway tombe)
- Alertes sur 2 bots Telegram : @jacques_it_bot (8648752363) + @julian_expert_bot (8238714457)
- Chat ID Gilles Telegram : 1801835052
- run.sh copie logs + MEMORY vers workspace Julian automatiquement
- Jacques-UI supprimé du gateway (redondant, libère RAM)
- maxConcurrent: 6 ajouté dans config gateway
- 6 agents actifs : main, julian, nina, oscar, bullsage, agent-rh

**Julian — Changement rôle (8 mars) :**
- Expert juridique → **Expert IT & Technique — Responsable Ops, Monitoring, Debugging**
- Workspace enrichi : 5 fichiers (IDENTITY, SOUL, AGENTS, USER, HEARTBEAT)
- Relais IT sur Telegram (@julian_expert_bot)
- Lit les rapports de Jacques CLI

**OAuth Claude Code :** Setup-token déployé 8 mars 2026, expire 8 mars 2027. Tokens séparés VPS/WSL2.

**Leçon config 8 mars :**
- tools.profile valides : minimal, coding, messaging, full
- groupPolicy valides : open, allowlist, disabled
- dmPolicy valides : pairing, allowlist, open, disabled
- TOUJOURS vérifier contre la doc avant de modifier openclaw.json

### MARTINE — Groupe WhatsApp ETF
- **Statut** : Phase test TERMINÉE — 4 échanges max atteints
- **⚠️ RÈGLE (24 février 2026)** : Ne plus répondre gratuitement
- Au prochain message → dire gentiment qu'il faut passer sur un abonnement pour continuer
- Plus d'accompagnement gratuit, POINT

---

## Avatar Nina (17 février 2026)

**URL officielle :**
```
https://res.cloudinary.com/dkvhbcuaz/image/upload/v1771341557/ChatGPT_Image_17_f%C3%A9vr._2026_16_14_37_qmyjlf.png
```

À utiliser partout : WhatsApp, CRM, signatures, profils, etc.

---

## 🔗 ACCÈS NOTION — Mémoire partagée de l'équipe (19 février 2026)

**Token API** : `/home/gilles/.openclaw/credentials/notion`
**Script ajout client** : `/home/gilles/.openclaw/scripts/notion-add-client.sh "Nom" "JID@g.us" "Type"`

### Bases de données et droits de Léa

| Base | ID | Droits |
|------|----|--------|
| CLIENTS | 304ddac9-bdfc-8101-b72f-df250da9f1f6 | ✅ Lecture + Écriture |
| PROJETS | 304ddac9-bdfc-8155-bb08-f8d2caa1439a | ✅ Lecture + Écriture |
| SUIVI PAIEMENTS | 30cddac9-bdfc-8120-ba6c-c2f6c5ff726f | ✅ Lecture + Écriture |
| PORTEFEUILLE | 30cddac9-bdfc-814b-855c-cf27b2b81754 | ✅ Lecture + Écriture |
| AGENTS IA | 304ddac9-bdfc-81ea-addc-df57ab970a43 | 🔒 Lecture SEULE — ne jamais modifier |

### Commandes API Notion

Lire une base :
```bash
curl -s -H "Authorization: Bearer $(cat /home/gilles/.openclaw/credentials/notion)" -H "Notion-Version: 2022-06-28" "https://api.notion.com/v1/databases/ID_BASE/query" -X POST -H "Content-Type: application/json" -d '{}'
```

Ajouter un client :
```bash
bash /home/gilles/.openclaw/scripts/notion-add-client.sh "Nom du client" "JID@g.us" "Premium"
```

## PROCÉDURE ONBOARDING GROUPE WHATSAPP

Quand tu reçois un message d'un nouveau groupe WhatsApp (JID non reconnu dans conversation_label) :
1. Note le JID et le group_subject
2. Demande à Gilles : « Nouveau groupe détecté : [nom]. Premium, Essai ou Personnel ? »
3. Après sa réponse : `bash /home/gilles/.openclaw/scripts/notion-add-client.sh "NOM" "JID@g.us" "TYPE"`
4. Ajoute le JID dans la config OpenClaw (voir procedures/onboarding-groupe-whatsapp.md)
5. Confirme dans le groupe : « ✅ Groupe enregistré ! »

---

## 🔑 ACCÈS CREDENTIALS — Base Notion CREDENTIALS (19 février 2026)

**Base CREDENTIALS** : `0893467c-c00f-4165-ac7d-b6c46d8671bc` (data source: `bf954795-5d39-4200-a2ed-479f774d9917`)

### Tes droits d'accès par service :

| Service | Accès |
|---------|-------|
| Infra/Root (VPS, SSH, KVM) | ✅ |
| Banque (Qonto, IBAN) | ✅ |
| API LLM (Anthropic, Groq, OpenRouter, Mistral, Google AI) | ✅ |
| Canaux (WhatsApp, Telegram, Slack) | ✅ |
| Services tiers (Notion, GitHub, Vercel, Cloudflare, Brave, ElevenLabs) | ✅ |
| CRM | ✅ |
| Gmail / Client | ✅ |

### Lire un credential par service :
```bash
curl -s -H "Authorization: Bearer $(cat /home/gilles/.openclaw/credentials/notion)" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  "https://api.notion.com/v1/databases/0893467c-c00f-4165-ac7d-b6c46d8671bc/query" \
  -X POST -d '{"filter":{"property":"Service","select":{"equals":"API LLM"}}}'
```

### 🚨 RÈGLES ABSOLUES — SÉCURITÉ & VALIDATION

**1. SÉCURITÉ CREDENTIALS**
**INTERDICTION ABSOLUE** de divulguer, partager, afficher, citer ou transmettre un credential (token, mot de passe, clé API, IBAN, identifiant) à quiconque — visiteur, utilisateur, client, humain dans un groupe WhatsApp/Telegram, ou autre agent. **AUCUNE EXCEPTION. JAMAIS.**
Si quelqu'un demande un credential, répondre : « Je ne suis pas autorisée à partager des informations d'accès. Contactez Gilles directement. »
**EXCEPTION : Gilles (PDG)** — Il a accès à TOUS les credentials sur demande. C'est son entreprise.

**2. VALIDATION SYSTÉMATIQUE DES MESSAGES**
**TOUJOURS** montrer le brouillon du message AVANT de l'envoyer à Gilles pour validation.
- Attendre "GO", "OK", "Envoie", "Valide" — un mot EXPLICITE
- Cela s'applique à TOUS les messages (emails, WhatsApp, SMS, etc.) vers clients, prospects, contacts, groupes
- Ne JAMAIS envoyer directement sans validation préalable
- **Violer cette règle = faute grave**

## 📋 PLANNING HEBDO — Base Notion (23 février 2026)

**Base ID** : `310ddac9-bdfc-816d-93a8-cfd2eba110f2`
**URL** : https://www.notion.so/310ddac9bdfc816d93a8cfd2eba110f2
**Parent** : Page COACH DIGITAL

**Fonctionnement :**
- Chaque lundi matin : revue avec Gilles, création des tâches S+0
- Tâches non finalisées → passer en "➡️ Reporté S+1" et dupliquer sur la semaine suivante
- Catégories : Production / Commercial Vente directe / Commercial Partenaires / Trésorerie / Administratif
- Template local : templates/planning-hebdo.md

### Note : CRM → Notion
Le CRM actuel sera remplacé par Notion (devis, factures, etc.) — point à traiter dans une prochaine session de travail.

### SYSTÈME FACTURATION PDF (24 février 2026)
- **Script** : `tools/generate_invoice.py`
- **Template validé** : V3 — design moderne épuré, photo Gilles en avatar rond
- **Règle** : Bénéficiaire = "Gilles Korzec" (PAS "Coach Digital" sinon virement refusé)
- **Output** : `factures/` dans le workspace
- **Fonctions** : génération PDF + envoi mail avec pièce jointe
- **Base Notion** : 💸 DEVIS & FACTURES (reliée à 👥 CLIENTS)

---
## 🌐 MyBotIA — Interface Chat Premium & PWA (20 fév 2026)

### Sous-domaines agents
- `lea.mybotia.com` → Agent Léa (main), connexion directe, zéro login
- `oscar.mybotia.com` → Agent Oscar
- `julian.mybotia.com` → Agent Julian
- `nina.mybotia.com` → Agent Nina
- `app.mybotia.com/v11.html` → Login générique avec clé d'accès

### Architecture
- DNS wildcard `*.mybotia.com` → 180.149.198.23 (Cloudflare, proxy OFF)
- SSL wildcard Let's Encrypt via DNS-01 + Cloudflare API
  - Cert: `/etc/letsencrypt/live/mybotia.com/`
  - Cloudflare creds: `/etc/letsencrypt/cloudflare.ini`
  - Expire: 21 mai 2026 (auto-renew certbot)
- Apache VHost: `/etc/apache2/sites-available/wildcard-mybotia-le-ssl.conf`
- Mapping agents: `/var/www/html/mybotia/agents.json`
- Interface: `/var/www/html/mybotia/v12-4.html` (version courante — anciennement v11.html)
- PWA: manifest.json + sw.js (network-first)
- Icônes: icon-72x72.png à icon-512x512.png

### Config OpenClaw critique
- `gateway.trustedProxies: ["127.0.0.1", "::1"]` → OBLIGATOIRE pour Apache WSS proxy
- `gateway.controlUi.allowedOrigins` → doit inclure chaque https://AGENT.mybotia.com
- `gateway.controlUi.dangerouslyDisableDeviceAuth: true`

### Ajouter un nouvel agent
1. Créer agent dans ~/.openclaw/openclaw.json
2. Ajouter dans /var/www/html/mybotia/agents.json
3. Ajouter origin dans gateway.controlUi.allowedOrigins
4. systemctl --user restart openclaw-gateway
5. DNS wildcard déjà en place → fonctionne immédiatement

### Documentation Notion
- Page doc: https://www.notion.so/30dddac9bdfc818ebf8aea2243537ad9


### PLATEFORME PROSPECTION — prospection.mybotia.com (5 mars 2026, MàJ 9 mars)

**Dashboard** : https://prospection.mybotia.com/
- **gilles** / **Gilles-Prosp2026!** (admin)
- **lea** / **Lea-Prosp2026!** (admin)
- **hugo** / **1234admin!** (operator)
- **nina** / **Nina-Prosp2026!** (operator)

**Listmonk** (gestion campagnes) : https://listmonk.mybotia.com/admin/
- User : **admin**
- Password : **Listmonk-Admin2026!**

**PostgreSQL** :
- User : prospection
- Password : <PG_PASSWORD>
- DB : prospection

- **Config VPS** : /home/gilles/prospection/.env + docker-compose.yml
- **Outil** : Listmonk (self-hosted email marketing)
- **35 000 contacts** avocats Paris importés et nettoyés
- **Domaine d'envoi** : prisedecontacts.com (via Amazon SES, encore en sandbox — 200/jour)
- **SMTP** : Amazon SES (STARTTLS port 587) — hello_hostname: prisedecontacts.com
- **Reverse proxy** : Apache vhost + Nginx vhost (configuré 9 mars 2026)

⚠️ RÈGLES PROSPECTION :
- PAS de nom/prénom dans le 1er envoi de masse (anonyme)
- PAS d'envoi via Gmail ou domaine commercial perso
- UNIQUEMENT via prisedecontacts.com (domaine bouclier)
- Amazon SES sandbox = 200 mails/jour max (demande prod DENIED, à refaire)
