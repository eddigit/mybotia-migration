# MARTINE DONNETTE — Association "En Toute Franchise" (ETF)

## Groupe WhatsApp
- **Nom** : ETF
- **JID** : 120363426071294259@g.us
- **Participants** : Martine Donnette, Claude (co-associé ?), Gilles

## Statut commercial
- Phase test TERMINÉE — plus d'accompagnement gratuit
- **Exception 30/03/2026** : Gilles a accordé gratuité jusqu'à 15h pour cadrer les envois mails
- **Proposition en cours** : 190€/mois (au lieu de 980€) pour collaboratrice IA dédiée
- Martine n'a pas encore accepté l'abonnement

## Contexte client
- Association de défense des commerçants/artisans contre les grandes surfaces
- Site web : en-toutefranchise.com (React SPA, hébergé Vercel)
- Adresse mail : entoutefranchise6@gmail.com (Gmail) + assoentoutefranchise@sfr.fr (SFR, à éviter)

## Interlocuteurs
- **Martine Donnette** : Présidente/responsable, contact principal. Pas très à l'aise avec le technique. Envoie des vocaux, des messages courts. Patiente mais directe.
- **Claude** : Co-responsable. Devait fournir des listes complémentaires (commerçants spécifiques, politiques, journalistes). Pas encore actif dans les échanges récents.

## Projet : Campagne emailing (30/03/2026)

### Objectif
Envoyer un mail de mobilisation aux commerçants/artisans pour défendre le commerce de proximité et recruter des adhérents.

### Message 1ère campagne
- Objet : "Défendez votre commerce – Rejoignez-nous"
- Contenu : validé par Martine, prêt à envoyer
- Reçu par email le 30/03/2026 sur coachdigitalparis@gmail.com

### Infrastructure d'envoi
- **Expéditeur** : adresse noreply@en-toutefranchise.com (À CRÉER)
- **Serveur** : serveur d'envoi dédié, ~69€ one-shot — Gilles a validé, facture à envoyer
- **Reply-to** : entoutefranchise6@gmail.com (choix de Martine, validé)
- ❌ Gmail = limité 500/jour
- ❌ SFR = risque blacklist

### Base de contacts
- **20 000 contacts qualifiés** chez Gilles (triés, corrigés avec outil de validation)
- **Listes complémentaires** attendues de Claude : commerçants spécifiques, politiques, journalistes
- Envoi prévu : dès que l'adresse no-reply est opérationnelle

### Calendrier
- Jour d'envoi optimal : mardi/jeudi matin (9h-10h)
- Premier envoi : dès que infrastructure en place

## Historique technique

### Open Graph / Réseaux sociaux (06/03/2026)
- Problème : partage d'articles sur Facebook sans image (SPA React, crawlers ne voient pas le JS)
- Fix : serverless function Vercel `/api/og-blog` + routing crawlers + `.npmrc` (legacy-peer-deps)
- Résultat : ✅ images articles apparaissent sur Facebook/LinkedIn/X
- Bug identifié : conflit date-fns@4.1.0 vs react-day-picker@8.10.1 → résolu par .npmrc

### Flyer A5 (19/03/2026)
- Martine a demandé un flyer A5 avec QR code vers le site
- Gilles : "C'est eux qui doivent nous fournir le cahier des charges"
- Cahier des charges demandé le 20/03 → pas encore reçu

## Tarifs adhésion (validés par Martine)
- **Particuliers** : à partir de 10 € (franchisé ou particulier sensible au respect des lois)
- **Individuelle** : 50 €
- **Association de commerçants** : 153,32 €

## Chatbot — Instructions validées
- Message d'accueil : "Bonjour ! 👋 Je suis Léa, l'assistante d'En Toute Franchise. Que vous soyez commerçant, artisan, franchisé ou particulier, je suis là pour répondre à vos questions. Comment puis-je vous aider ?"
- Poser 2 questions avant d'orienter :
  1. Quel type de commerce ? (boutique, artisan, franchise…)
  2. Quelle surface ?
- Puis orienter vers la bonne adhésion SANS donner de détails supplémentaires
- Mettre en avant : 30 ans d'expérience + avocats experts en urbanisme
- JAMAIS mentionner "Les Mousquetaires" — porte préjudice à l'association
- JAMAIS divulguer d'infos sur les adhérents (risque de représailles)

## Corrections site à faire (brief Gilles)
- ✅ Supprimer "Les Mousquetaires" dans le chatbot (commit c752d2e — 02/04/2026)
- ✅ Chatbot restructuré qualification-first (plus de mur d'infos)
- ❌ Supprimer "Les Mousquetaires" sur page Contact (front-end HTML)
- ❌ Corriger tarifs d'adhésion partout
- ✅ Blog : article à la une + 3 derniers articles + bouton "Voir tous les articles"

## Actions en attente
- 🔲 Facture 69€ serveur d'envoi → envoyer à Martine/Claude
- 🔲 Recevoir paiement sur Qonto
- 🔲 Créer adresse noreply@en-toutefranchise.com
- 🔲 Récupérer liste 20 000 contacts de Gilles
- 🔲 Récupérer listes complémentaires de Claude
- 🔲 Configurer envoi + test
- 🔲 Cahier des charges flyer (en attente côté Martine/Claude)
- 🔲 **URGENT** : Appliquer toutes les corrections site + chatbot (brief prêt pour Gilles)

## ⚠️ Leçons apprises
- Ne JAMAIS écrire de notes internes dans le groupe (incident du 01/03 : "selon ma MEMORY.md", "directive de Gilles")
- Rester bref avec Martine — elle préfère les réponses courtes et directes
- Martine n'est pas technique → pas de jargon, étape par étape
