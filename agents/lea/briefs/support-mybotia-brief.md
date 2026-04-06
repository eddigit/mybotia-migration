# Brief — Système Support MaBoiteIA

## Contexte

MaBoiteIA (mybotia.com) est un SaaS de collaborateurs IA pour entreprises (principalement cabinets d'avocats). Chaque client a un collaborateur IA dédié qui communique avec lui via WhatsApp, Telegram ou email.

Aujourd'hui, le support est fait manuellement par Gilles (CEO) et Léa (Directrice Admin). Ça ne scale pas. On a besoin d'un système de support intégré, professionnel et traçable.

## Vision

Le support MaBoiteIA est **innovant** : le premier niveau de support, c'est le collaborateur IA lui-même. Il s'autocorrige quand il peut. Quand il ne peut pas, il escalade à l'équipe MaBoiteIA de manière transparente pour le client. Le client ne parle qu'à son collaborateur — jamais besoin d'ouvrir un ticket, d'envoyer un email ou d'attendre au téléphone.

## Architecture générale

```
Client signale un problème à son collaborateur IA
        │
        ▼
NIVEAU 0 — Auto-diagnostic & auto-correction
Le collaborateur tente de diagnostiquer et corriger lui-même
        │
        ├── Résolu → informe le client, ticket auto-clos
        │
        ▼ (non résolu)
NIVEAU 1 — Escalade
Le collaborateur crée un ticket via API interne
Il dit au client : "Maintenance en cours, je reviens vers vous"
        │
        ▼
NIVEAU 2 — Traitement par l'équipe MaBoiteIA
Léa (ou Julian pour les sujets infra) traite le ticket
Met à jour le ticket avec les actions effectuées
        │
        ▼
RETOUR
Le collaborateur reçoit la résolution
Il informe le client : "C'est réglé, voilà ce qui a été fait"
Ticket clos avec traçabilité complète
```

## Ce qu'il faut construire

### 1. Base de données — PostgreSQL (base existante `mybotia_crm`)

**Table `support_tickets`**

| Champ | Type | Description |
|-------|------|-------------|
| id | serial PK | |
| ticket_number | varchar | Format TK-2026-0001 (auto-incrémenté, unique) |
| client_id | int | Référence au client dans le CRM |
| client_name | varchar | Nom du client (dénormalisé pour affichage rapide) |
| collaborator_id | varchar | Identifiant du collaborateur qui a créé le ticket |
| collaborator_name | varchar | Nom du collaborateur (ex: Max, Lucy) |
| category | varchar | bug, question, maintenance, feature_request, behavioral |
| priority | varchar | critical, high, normal, low |
| status | varchar | open, self_diagnosed, escalated, in_progress, waiting_client, resolved, closed |
| subject | varchar | Titre court du problème |
| description | text | Description détaillée |
| self_diagnosis_log | text | Ce que le collaborateur a tenté avant d'escalader (tests effectués, résultats) |
| assigned_to | varchar | Qui traite (léa, julian, gilles) — nullable |
| resolution_summary | text | Résumé de la résolution — nullable |
| created_at | timestamp | Création (immutable) |
| updated_at | timestamp | Dernière mise à jour |
| resolved_at | timestamp | Date de résolution — nullable |
| closed_at | timestamp | Date de clôture — nullable |

Contrainte : **rien n'est jamais supprimé**. Soft delete uniquement si nécessaire. Les timestamps sont immutables une fois écrits. C'est une exigence juridique — en cas de litige avec un client, on doit pouvoir retracer l'intégralité des échanges.

**Table `support_messages`**

| Champ | Type | Description |
|-------|------|-------------|
| id | serial PK | |
| ticket_id | int FK | Référence au ticket |
| sender | varchar | Qui a écrit (nom du collaborateur, "léa", "julian", "gilles", "system") |
| sender_role | varchar | collaborator, support_team, system |
| message | text | Contenu du message |
| attachments | jsonb | Pièces jointes éventuelles (logs, screenshots) — nullable |
| created_at | timestamp | Immutable |

Chaque échange sur un ticket est un message horodaté. C'est le fil de discussion complet.

### 2. API REST — Endpoints dans l'admin Next.js existant

L'admin est dans `/var/www/html/apps/admin/`. C'est une app Next.js avec API routes dans `app/api/`. L'authentification agent existante utilise les headers `X-API-Key` et `X-Agent-Id`.

**Endpoints nécessaires :**

`POST /api/support/tickets` — Créer un ticket
- Body : client_name, collaborator_name, category, priority, subject, description, self_diagnosis_log
- Retourne : ticket_number, id
- Utilisé par les collaborateurs pour escalader

`GET /api/support/tickets` — Lister les tickets
- Filtres query params : status, priority, client_name, collaborator_name, assigned_to, date_from, date_to
- Pagination : page, limit
- Tri : sort_by (created_at, priority, updated_at), sort_order
- Utilisé par le dashboard

`GET /api/support/tickets/:id` — Détail d'un ticket avec tous ses messages
- Retourne le ticket + tableau de messages ordonné chronologiquement
- Utilisé par le dashboard et par les collaborateurs pour vérifier la résolution

`PATCH /api/support/tickets/:id` — Mettre à jour un ticket
- Champs modifiables : status, priority, assigned_to, resolution_summary
- Chaque changement de statut ajoute automatiquement un message system dans support_messages

`POST /api/support/tickets/:id/messages` — Ajouter un message à un ticket
- Body : sender, sender_role, message, attachments
- Utilisé par Léa/Julian pour répondre, par le collaborateur pour ajouter du contexte

`GET /api/support/tickets/collaborator/:collaborator_name` — Tickets d'un collaborateur
- Filtre par collaborateur, optionnellement par status
- Permet au collaborateur de vérifier ses tickets résolus pour informer le client

`GET /api/support/stats` — Métriques
- Tickets par période (jour/semaine/mois)
- Temps moyen de résolution
- Taux d'auto-correction (tickets résolus en self_diagnosed vs escalated)
- Répartition par catégorie et priorité
- Tickets par client et par collaborateur

`GET /api/support/tickets/:id/export` — Export PDF d'un ticket
- Génère un PDF avec l'intégralité du fil (ticket + tous les messages)
- Usage juridique : preuve de traçabilité en cas de litige

### 3. Dashboard Support — Page dans l'admin

Ajouter une section "Support" dans la navigation de l'admin existant.

**Vue liste :**
- Tableau des tickets avec colonnes : #ticket, client, collaborateur, sujet, priorité, statut, assigné à, date création, dernière mise à jour
- Filtres rapides : Tous / Ouverts / En cours / Résolus / Critiques
- Recherche texte (sujet, description, client)
- Badges de couleur sur les priorités et statuts
- Clic sur une ligne → vue détail

**Vue détail d'un ticket :**
- En-tête : infos du ticket (client, collaborateur, catégorie, priorité, statut, assigné)
- Section "Auto-diagnostic" : ce que le collaborateur a tenté (affiché proprement)
- Fil de messages : style conversation (comme un chat), chaque message avec auteur + timestamp
- Zone de réponse : champ texte pour ajouter un message
- Actions : changer statut, changer priorité, assigner, résoudre (avec résumé), exporter PDF

**Vue métriques :**
- Cartes en haut : tickets ouverts, temps moyen résolution, taux auto-correction
- Graphique tickets/semaine
- Top clients par nombre de tickets
- Top catégories

### 4. Landing page — support.mybotia.com

Une page publique, marketing, qui présente notre approche innovante du support.

**Structure de la page :**

**Hero section :**
- Titre : "Votre support, c'est votre collaborateur"
- Sous-titre : "Pas de ticket à ouvrir. Pas d'attente. Votre collaborateur IA détecte, corrige et vous tient informé. En temps réel."
- Illustration ou animation simple montrant le flux (client parle → collaborateur résout)

**Section "Comment ça marche" — 3 étapes visuelles :**

1. **Vous parlez à votre collaborateur** — "Comme d'habitude. Dans votre WhatsApp, votre Telegram, votre email. Vous lui dites ce qui ne va pas."

2. **Il s'autocorrige** — "Votre collaborateur analyse le problème et corrige lui-même quand il peut. La plupart des problèmes sont résolus en quelques secondes, sans intervention humaine."

3. **L'équipe MaBoiteIA intervient quand nécessaire** — "Pour les problèmes complexes, votre collaborateur contacte directement notre équipe technique. Vous êtes tenu informé à chaque étape. Zéro friction."

**Section exemples — 3 conversations réelles (simulées) :**

**Exemple 1 — Auto-correction (comportement)**
```
👤 Client : "Je trouve que tes réponses sont trop longues, j'aimerais quelque chose de plus concis"
🤖 Collaborateur : "Bien noté. J'ajuste immédiatement. Mes réponses seront désormais plus synthétiques. N'hésitez pas à me le signaler si c'est encore trop long."
✅ Résolu en 10 secondes
```

**Exemple 2 — Escalade transparente (technique)**
```
👤 Client : "Les emails que tu envoies n'arrivent pas chez mes clients"
🤖 Collaborateur : "Je vérifie immédiatement... Je constate un problème sur le service d'envoi qui nécessite une intervention technique. L'équipe est dessus, je reviens vers vous dès que c'est réglé."
⏳ 45 minutes plus tard
🤖 Collaborateur : "C'est réglé ! Le service d'envoi a été rétabli. J'ai renvoyé les 3 emails qui étaient en attente."
✅ Résolu en 45 min — le client n'a parlé qu'à son collaborateur
```

**Exemple 3 — Amélioration continue (feature)**
```
👤 Client : "Tu pourrais me préparer un récap hebdomadaire de mes dossiers ?"
🤖 Collaborateur : "Très bonne idée. Ce n'est pas encore dans mes fonctionnalités, je remonte la demande à l'équipe produit."
⏳ Quelques jours plus tard
🤖 Collaborateur : "Bonne nouvelle ! Le récap hebdomadaire est maintenant actif. Chaque lundi matin, vous recevrez un résumé de vos dossiers en cours."
✅ Le collaborateur apprend et évolue
```

**Section réassurance :**
- "Et si j'ai besoin de parler à un humain ?" → "C'est toujours possible. Mais honnêtement, vous n'en aurez probablement pas besoin."
- "Mes données sont-elles sécurisées ?" → "Absolument. Tous les échanges sont chiffrés et hébergés en France."
- "Mon collaborateur va-t-il s'améliorer avec le temps ?" → "Oui. Chaque problème résolu le rend plus performant. C'est l'avantage d'un collaborateur IA : il apprend en continu."

**Footer :** Lien vers mybotia.com, contact, mentions légales

**Design :** Cohérent avec le site mybotia.com existant. Moderne, professionnel, sobre. Couleurs MaBoiteIA.

### 5. Configuration DNS

Sous-domaine `support.mybotia.com` à pointer vers le VPS (180.149.198.23). Le wildcard DNS est déjà en place, et le SSL wildcard Let's Encrypt couvre `*.mybotia.com`.

Il faudra configurer un virtual host Nginx pour servir la page statique ou la route Next.js.

## Stack technique

- **Backend :** Next.js API routes (dans l'admin existant `/var/www/html/apps/admin/`)
- **Base de données :** PostgreSQL `mybotia_crm` (existante, connexion déjà configurée dans l'admin)
- **Frontend dashboard :** React/Next.js (dans l'admin existant, ajouter des pages)
- **Landing page :** Peut être une page dans l'admin (route publique) ou une page statique séparée dans `/var/www/html/support/`
- **Export PDF :** Librairie au choix (puppeteer, jspdf, ou autre)

## Contraintes

1. **Traçabilité juridique** — Rien n'est jamais supprimé. Tous les timestamps sont immutables. L'export PDF d'un ticket doit être complet et exploitable comme preuve.
2. **Sécurité** — Les endpoints API sont protégés par authentification agent (X-API-Key + X-Agent-Id). La landing page est publique. Le dashboard nécessite une authentification admin.
3. **Performance** — Le système doit supporter une montée en charge (aujourd'hui 5-6 clients, demain 20+ collaborateurs).

## Livraison

Une fois terminé, partager le résultat complet à Léa :
- Structure des fichiers créés/modifiés
- Migration SQL à exécuter
- Configuration Nginx si nécessaire
- Instructions de déploiement
- Ce qui a été testé / ce qui reste à tester

## Contact

Pour toute question pendant le développement, contacter Léa directement (canal interne VPS).
