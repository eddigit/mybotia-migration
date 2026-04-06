# IGH — SAS IGH / EHPAD (Imbert & Cozon)

## Contacts
- **M. Imbert** : PDG
- **M. Cozon** : DG délégué
- **Intro par** : Jean-Luc Aubagnac (jeanluc@aubagnac.com)

## Groupe WhatsApp
- **Nom** : "IA GROUPE IGH"
- **JID** : 120363423979135043@g.us
- ⚠️ ANCIEN JID FAUX : 120363407026699197@g.us = c'était Team Coach Digital (INTERNE)

## Le groupe
- SAS IGH — 20 établissements (17 EHPAD + 3 cliniques), siège Aix-en-Provence

## Collaboratrice IA : Florence
- Ref Florence Nightingale
- Site présentation : https://collab-igh.vercel.app/
- **MVP Admin** : https://mvp-igh.vercel.app/

## Budget mise en place : 11 952 EUR HT (14 jours à 768 EUR/j)
- Phase 0 Cadrage : 1 200 EUR
- Phase 1 Audit terrain : 1 536 EUR (2j)
- Phase 1B Analyse + Construction : 3 072 EUR (4j)
- Phase 2 Intégration technique : 3 072 EUR (4j)
- Phase 3 Pilote + Formation : 1 536 EUR (2j)
- Phase 4 Formation plénière directeurs Nord+Sud : 1 536 EUR (2j)

## Paiement
- 40% commande / 30% Phase 2 / 30% Phase 3

## Refonte site i-g-h.fr
- 1 990 EUR HT (au lieu de 5 900 EUR) — conditionné à l'engagement offre globale

## Abonnement
- 216 EUR HT/mois/étab (20 étab = 4 320 EUR/mois = 51 840 EUR/an)
- Inclut : Florence 24/7, formation continue directeurs, maintenance, infogérance (Léa 1er niveau, Gilles escalade), assistance distancielle Gilles incluse (présentiel = frais déplacement seuls)

## Prestations complémentaires
- 90 EUR HT/h tarif préférentiel IGH

## Totaux
- Total one-shot : 13 942 EUR HT (mise en place + site)
- Coût total année 1 : 63 792 EUR (mise en place + 12 mois x 20 étab)

## MVP Admin Dashboard — https://mvp-igh.vercel.app/
- **Repo GitHub** : https://github.com/eddigit/mvp-igh
- **Stack** : Next.js (App Router), TypeScript, Tailwind CSS, Vercel
- **Créé** : 26 mars 2026
- **Dernier commit** : 26 mars 2026 — "VRAIES DONNÉES TITAN Q1 2026 - 17 EHPAD, 1063 résidents, CA 9.28M€"
- **Composants** : AnimatedCounter, LucyChat (chatbot intégré), SectionWrapper
- **Données** : mock-data.ts + titan-data.json (données réelles Q1 2026)
- **Modules actifs** : Suivi lits, Facturation, Alertes admin, Cahier du jour, Chat Lucy
- **Modules "En Option" (10)** : Juridique, Site web, Courrier, ViaTrajectoire, Relances, RH, Qualité, Formations (quiz IGH, classement, profils compétences), Secrétariat, Reporting
- **Visuels** : Logo IGH (blanc sur fond sombre), Avatar Lucy (Cloudinary)

### Sécurité MVP (30 mars 2026)
- **Mot de passe** : `igh` / `IGH-Demo2026!` (Basic Auth middleware)
- **Modal disclaimer** obligatoire à l'entrée
- **CGU 12 articles** sur /mentions-legales (RGPD, Privacy by Design, protocole démo)
- **Bandeau + footer** permanents
- **Contexte** : DPO présent lors de la démo à Cozon s'est offusqué → sécurisé dans la foulée
- Données = MOCK DATA, pas de traitement RGPD, accès privé temporaire

### Historique commits (26 mars 2026)
1. MVP Dashboard initial — suivi lits, facturation, alertes admin
2. V2 — Vrais établissements IGH, Cahier du jour, Chat Lucy, Navigation sidebar
3. Logo IGH officiel + avatar Lucy
4. 10 modules "En Option" cliquables avec contenu mock
5. Module Formations enrichi (quiz, classement, profils compétences)
6. **VRAIES DONNÉES TITAN Q1 2026** — 17 EHPAD, 1063 résidents, CA 9.28M€

## Repos GitHub IGH
| Repo | URL | Usage |
|------|-----|-------|
| **mvp-igh** | https://github.com/eddigit/mvp-igh | MVP Dashboard admin (Next.js) |
| **collab-igh** | https://github.com/eddigit/collab-igh | Site présentation collaboratrice IA |
| **site-igh-2026** | https://github.com/eddigit/site-igh-2026 | Refonte site i-g-h.fr |

## Dossier local
- `clients/imbert-ehpad/`

## Statut (MàJ 23 mars 2026)
- ✅ Commande confirmée par email de Stéphane Cozon (jeudi 19 mars)
- ✅ Facture d'acompte FA-2026-040-IGH envoyée vendredi 20 mars (4 780,80€ HT / 5 736,96€ TTC)
- ❌ Acompte non reçu sur Qonto au 23 mars
- ❌ Pas de réponse de Cozon depuis le 20 mars
- ✅ Email de confirmation/relance envoyé lundi 23 mars par Léa (coachdigitalparis@gmail.com) — copie Gilles
  - Confirme venue Gilles mercredi 25 mars 14h à Aix
  - Confirme nom Lucy (réf. film Luc Besson — accès progressif à 100% de ses capacités)
  - Rappel subtil facture + demande si élément manquant pour traitement admin
  - Frais de déplacement non facturés, pris en charge côté Coach Digital
- 📅 RDV terrain : **mercredi 25 mars 2026, 14h**, locaux IGH Aix-en-Provence
- Nom collaboratrice IA : **Lucy** (référence film Luc Besson)
- Ancien nom Florence → abandonné

## Agent Lucy — Déployé 22 mars 2026
- **Gateway dédiée** : port 18795, config `~/.openclaw-lucy/openclaw.json`
- **ID agent** : `lucy`
- **Modèle** : claude-sonnet-4-6
- **Workspace** : `/home/gilles/.openclaw/workspace-lucy/`
- **Avatar** : https://res.cloudinary.com/dniurvpzd/image/upload/v1774210075/Capture_d_e%CC%81cran_2026-03-22_a%CC%80_21.06.45_d2bygw.png
- **WhatsApp** : +33 7 80 97 30 18 (nouveau, appairé) ✅ Connecté
- **Ancien WhatsApp** : +33 7 58 05 46 84 (SIM Lyca, Android dédié) — remplacé
- **Email Gmail** : lucyighgroupe@gmail.com
- **Email pro** : lucy@collaborateur.pro (Migadu)
- **Telegram** : @lucy_igh_bot ✅ En ligne
- **WebChat** : https://lucy.mybotia.com ✅ Actif
- **Token gateway** : `e581649cd03d0d2c17666f2cb82703d02c3109ab08a899de`
- **Cron watchdog** : toutes les 5 min, relance auto si crash
- **Phase** : Apprentissage — écoute, n'intervient pas seule
