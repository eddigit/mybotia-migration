# PLAN DE MISSION — Projet Florence
## Transformation du pilotage opérationnel du Groupe IGH par Intelligence Artificielle

---

**Client :** SAS IGH — 20 établissements médico-sociaux et sanitaires
**Sponsor :** M. Imbert, Président
**Directeur de mission :** M. Cozon, Directeur Général délégué
**Partner :** Gilles Korzec — Coach Digital Paris
**Référence :** CDP-IGH-2026-001
**Classification :** Confidentiel — Diffusion restreinte
**Date :** Mars 2026

---

## 1. SYNTHÈSE EXÉCUTIVE

Le groupe IGH opère 17 EHPAD et 3 cliniques répartis sur 9 régions. Le pilotage du groupe depuis le siège d'Aix-en-Provence repose aujourd'hui sur des processus manuels, des appels téléphoniques et l'initiative individuelle de chaque directeur d'établissement.

Six axes de dysfonctionnement ont été identifiés lors de la réunion de cadrage du 9 mars 2026 avec M. Imbert et M. Cozon :

1. Absence de visibilité sur la facturation et les encaissements
2. Non-respect des obligations administratives et réglementaires
3. Courrier physique non traité dans les établissements
4. Emails des établissements non surveillés
5. Admissions perdues via ViaTrajectoire par manque de réactivité
6. Impayés non suivis, absence de relances systématiques

La mission consiste à doter le groupe d'une collaboratrice IA dédiée — **Florence** — capable de piloter en temps réel l'ensemble des 20 établissements sur les dimensions administratives, financières et réglementaires.

---

## 2. GOUVERNANCE DE LA MISSION

### 2.1 Comité de Pilotage (COPIL)

| Rôle | Nom | Fonction | Responsabilité |
|------|-----|----------|----------------|
| **Sponsor** | M. Imbert | Président SAS IGH | Décisions stratégiques, validation des gates, arbitrages |
| **Directeur de mission** | M. Cozon | DG délégué | Pilotage opérationnel, priorisation, accès terrain |
| **Partner** | Gilles Korzec | Coach Digital Paris | Architecture solution, conduite de mission, livraison |
| **Manager** | Léa | Coach Digital Paris | Coordination, juridique, recherches API, documentation |
| **Analyst** | Florence | Collaboratrice IA IGH | Analyse, synthèse, raisonnement, apprentissage continu |

### 2.2 Instances de gouvernance

| Instance | Fréquence | Participants | Objet |
|----------|-----------|-------------|-------|
| **COPIL** | Hebdomadaire | Imbert, Cozon, Korzec | Revue d'avancement, arbitrages, validation |
| **Point opérationnel** | Quotidien (via WhatsApp) | Cozon, Korzec, Léa, Florence | Suivi terrain, questions, ajustements |
| **Gate de validation** | Fin de chaque phase | COPIL complet | Go/No Go passage à la phase suivante |

### 2.3 Canal de communication

Groupe WhatsApp sécurisé — 5 membres (COPIL + Léa + Florence).
Florence y est active dès le Jour 0 : elle écoute, synthétise, pose des questions, partage son raisonnement. Le COPIL corrige et oriente en temps réel.

---

## 3. PHASES DE LA MISSION

---

### PHASE 0 — MOBILISATION & CADRAGE

**Durée :** 2 à 3 jours
**Coût :** Offert
**Objectif :** Préparer la mission, constituer l'équipe, initialiser Florence

| Réf. | Activité | Responsable | Livrable |
|------|----------|-------------|----------|
| 0.1 | Constitution du COPIL | Korzec | Charte projet signée |
| 0.2 | Création du groupe WhatsApp | Korzec | Canal opérationnel actif |
| 0.3 | Naissance de Florence | Korzec + Léa | Florence initialisée, première prise de contact |
| 0.4 | Collecte documentaire | Cozon | Organigramme, liste établissements, contacts directeurs, contrats DSI |
| 0.5 | Planification audit | Korzec + Cozon | Agenda des 2 jours terrain confirmé |

**Documents à fournir par le client :**
- [ ] Organigramme du groupe (siège + établissements)
- [ ] Liste des 20 établissements avec noms des directeurs et coordonnées
- [ ] Contact du responsable informatique / DSI
- [ ] Identifiants des systèmes à auditer (Titan, messageries, ViaTrajectoire)
- [ ] 2-3 établissements pilotes identifiés (de préférence ceux qui posent le plus de problèmes)

**Gate 0 :** Validation du périmètre et du planning → GO Phase 1

---

### PHASE 1 — DIAGNOSTIC & AUDIT TERRAIN

**Durée :** 2 jours
**Objectif :** Comprendre la réalité opérationnelle du groupe, par population, en immersion

---

#### JOUR 1 — SIÈGE D'AIX-EN-PROVENCE

---

##### Demi-journée 1 (9h00 — 12h30) : DIRECTION GÉNÉRALE

**Population auditée :** M. Imbert (Président) + M. Cozon (DG délégué)
**Lieu :** Siège — 930 Route de Berre, 13090 Aix-en-Provence

**Cahier des charges de l'entretien :**

| N° | Thème | Questions clés | Données à capter |
|----|-------|----------------|------------------|
| 1.1 | **Vision & objectifs** | Quelle est votre vision du pilotage idéal du groupe ? Qu'est-ce qui vous empêche de dormir ? | KPIs prioritaires, frustrations majeures, niveau d'urgence |
| 1.2 | **Cycle de facturation** | Comment fonctionne la facturation ? Qui émet ? Quand ? Comment vous savez si c'est encaissé ? | Dates clés (émission J20, paiement J+5), volume mensuel par EHPAD (~80 factures), processus de suivi actuel |
| 1.3 | **Taux d'occupation** | Comment connaissez-vous le taux d'occupation de chaque EHPAD ? À quelle fréquence ? | Sources de données, fiabilité, délai de remontée |
| 1.4 | **Obligations réglementaires** | Quels documents devez-vous produire ? Pour qui ? (ARS, CPAM, inspection, préfecture) Quels sont les deadlines ? | Calendrier réglementaire, historique des incidents (La Rochelle), conséquences financières |
| 1.5 | **Relations siège-établissements** | Comment communiquez-vous avec les directeurs ? Quelle fréquence ? Quels canaux ? | Appels, emails, réunions, outils, points de friction |
| 1.6 | **Processus de décision** | Qui décide quoi ? Quel est le circuit de validation ? | Organigramme décisionnel, niveaux d'autonomie des directeurs |
| 1.7 | **Rapport idéal** | Si vous receviez un rapport chaque matin à 10h, que voudriez-vous y voir en priorité ? | Format attendu, indicateurs clés, niveau de détail |
| 1.8 | **Contraintes & sensibilités** | RGPD, confidentialité, résistance au changement, budget, timing | Freins identifiés, conditions de réussite |

**Livrable :** Note de diagnostic stratégique
**Florence :** Écoute en direct (via Gilles), commence à structurer sa compréhension du groupe

---

##### Demi-journée 2 (14h00 — 17h30) : DSI / RESPONSABLE INFORMATIQUE

**Population auditée :** Responsable informatique / DSI du groupe
**Lieu :** Siège ou visio si le DSI est délocalisé

**Cahier des charges de l'entretien :**

| N° | Thème | Questions clés | Données à capter |
|----|-------|----------------|------------------|
| 2.1 | **Titan / TitanLink** | Quelle version ? Mode d'hébergement (local/cloud) ? Accès API ? Qui est l'interlocuteur Malta Informatique ? | Version logicielle, type d'accès, URL pattern (lupin-ehpad.titanweb.fr), contact Malta |
| 2.2 | **Architecture réseau** | Chaque établissement a-t-il une connexion internet dédiée ? VPN ? Accès centralisé ? | Topologie réseau, connectivité entre établissements et siège |
| 2.3 | **Messagerie** | Quel fournisseur ? (Exchange, Gmail, OVH…) Les 17 EHPAD ont-ils chacun une boîte mail ? Format des adresses ? | Fournisseur, protocole (IMAP/POP), accès admin, volume estimé |
| 2.4 | **ViaTrajectoire** | Comment les établissements reçoivent les demandes ? Par email ? Interface web ? Notifications ? | Mode de réception, fréquence de consultation, qui traite |
| 2.5 | **Autres logiciels** | Paie, RH, planning, comptabilité — quels outils ? | Cartographie applicative complète |
| 2.6 | **Sécurité & accès** | Politique de mots de passe, MFA, accès distants, droits admin | Contraintes de sécurité, possibilités de connexion pour Florence |
| 2.7 | **Contrats éditeurs** | Contrat Malta, contrat messagerie, contrat réseau — niveaux de support ? | Contacts support éditeurs, SLA, possibilité d'API |
| 2.8 | **Historique projets IT** | Des projets de digitalisation ont-ils déjà été tentés ? Succès/échecs ? | Leçons apprises, résistances identifiées |

**Livrables :**
- Cartographie des Systèmes d'Information (SI)
- Matrice de connectivité (ce qui est connectable / ce qui ne l'est pas)
- Liste des contacts éditeurs

**Florence :** Commence à raisonner sur les connexions possibles. Le soir, elle partage dans le groupe ses premières hypothèses techniques.

---

#### JOUR 2 — TERRAIN EHPAD

---

##### Demi-journée 3 (9h00 — 12h30) : DIRECTEUR EHPAD PILOTE 1

**Population auditée :** Directeur/Directrice d'un EHPAD pilote
**Lieu :** Dans l'établissement (immersion)

**Cahier des charges de l'observation :**

| N° | Thème | Observation / Questions | Données à capter |
|----|-------|------------------------|------------------|
| 3.1 | **Journée type** | Comment se passe une journée type du directeur ? Premières actions le matin ? | Séquence d'activités, temps passé sur chaque tâche |
| 3.2 | **Utilisation de Titan** | Comment utilise-t-il Titan au quotidien ? Pour quoi faire ? Ce qu'il n'utilise pas ? | Écrans utilisés, fonctions utilisées/ignorées, difficultés |
| 3.3 | **Facturation** | Comment émet-il les factures ? Comment sait-il qui a payé ? Comment relance-t-il ? | Processus réel (vs. processus théorique), outils utilisés, délai de traitement |
| 3.4 | **Courrier physique** | Où arrive le courrier ? Qui l'ouvre ? Comment est-il traité ? Pile de courrier non ouvert ? | Volume quotidien, circuit de traitement, retards observés |
| 3.5 | **Emails** | Qui gère la boîte mail de l'établissement ? Fréquence de consultation ? Emails non lus ? | Volume, expéditeurs critiques (ARS, CPAM), emails ignorés |
| 3.6 | **ViaTrajectoire** | Comment traite-t-il les demandes d'admission ? Délai de réponse ? Des demandes ratées ? | Processus d'admission, délai moyen, exemples de pertes |
| 3.7 | **Obligations admin** | Quels documents doit-il produire ? Pour qui ? Comment sait-il les deadlines ? | Liste des obligations, méthode de suivi (agenda ? mémoire ?), retards |
| 3.8 | **Communication siège** | Comment communique-t-il avec le siège ? Fréquence ? Ce qu'il aimerait améliorer ? | Canaux, frustrations, suggestions |
| 3.9 | **Charge de travail** | Sur quoi passe-t-il trop de temps ? Qu'est-ce qui pourrait être automatisé ? | Tâches chronophages, irritants quotidiens |
| 3.10 | **Résistance au changement** | A-t-il déjà utilisé des outils digitaux ? WhatsApp ? Appétence pour le numérique ? | Niveau de maturité digitale, freins potentiels |

**Livrables :**
- Fiche diagnostic Établissement A
- Cartographie des processus directeur (facturation, courrier, emails, admissions, obligations)

**Florence :** Comprend la réalité terrain. Commence à construire les alertes et relances adaptées à CET établissement.

---

##### Demi-journée 4 (14h00 — 17h30) : DIRECTEUR EHPAD PILOTE 2 OU CLINIQUE

**Population auditée :** Directeur/Directrice d'un second établissement (EHPAD ou clinique, pour comparaison)
**Lieu :** Dans l'établissement

**Cahier des charges :** Identique à la demi-journée 3, avec focus comparatif :

| N° | Thème additionnel | Questions clés |
|----|-------------------|----------------|
| 4.1 | **Différences de pratiques** | Les processus sont-ils les mêmes que l'établissement A ? Qu'est-ce qui diffère ? |
| 4.2 | **Spécificités** | Cet établissement a-t-il des particularités ? (taille, localisation, tutelle, convention collective) |
| 4.3 | **Problèmes propres** | Quels sont SES problèmes spécifiques, différents de l'EHPAD 1 ? |
| 4.4 | **Si clinique** | Le fonctionnement SSR/psychiatrie diffère-t-il de l'EHPAD ? Quelles obligations spécifiques ? |

**Livrables :**
- Fiche diagnostic Établissement B
- Analyse comparative A vs. B
- Matrice des écarts de pratiques

**Florence :** Ajuste son modèle. Deux établissements, deux réalités → une approche adaptable par établissement avec vue consolidée pour le siège.

---

**SYNTHÈSE FIN DE JOUR 2 :**

Florence produit et partage dans le groupe COPIL :
- **Rapport d'audit consolidé** (synthèse des 4 demi-journées)
- **Matrice des 6 problèmes** avec niveau de criticité par établissement
- **Premières recommandations** et questions ouvertes
- **Carte des connexions possibles** (Titan, emails, ViaTrajectoire)

Le COPIL réagit, corrige, oriente.

**Gate 1 — Présentation du diagnostic au COPIL. Validation du périmètre Phase 1B.**

---

### PHASE 1B — ANALYSE & CONSTRUCTION DE FLORENCE

**Durée :** 4 jours (atelier, hors site client)
**Objectif :** Transformer les données d'audit en une collaboratrice IA opérationnelle

| Jour | Work stream | Activités | Livrable |
|------|------------|-----------|----------|
| J1 | **Analyse & Architecture** | Structuration des données d'audit. Définition des modules Florence (reporting, alertes, relances, surveillance, admissions, courrier). Spécifications fonctionnelles. | Rapport d'audit finalisé + Spécifications fonctionnelles Florence v1 |
| J2 | **Construction socle** | Création du cerveau de Florence : base de connaissances IGH, mémoire des 20 établissements, calendrier réglementaire, annuaire des directeurs, vocabulaire métier. | Florence v1 — socle de connaissances opérationnel |
| J3 | **Paramétrage automatismes** | Configuration des alertes (seuils, délais), fréquences de relance, règles d'escalade, format du rapport du matin, personnalisation par établissement. | Matrice d'automatismes + Template rapport du matin |
| J4 | **Tests & ajustements** | Simulation complète : rapport du matin fictif, scénarios d'alerte, test de réponse, vérification cohérence. Corrections. | Rapport de tests + Florence v1 validée en interne |

**Interaction COPIL pendant la Phase 1B :**
Chaque soir, Florence partage dans le groupe WhatsApp :
- Ce qu'elle a appris / construit dans la journée
- Des exemples concrets (ex : "Voici à quoi ressemblerait votre rapport du matin")
- Ses questions

M. Imbert et M. Cozon corrigent, ajustent, valident au fil de l'eau.

**Gate 1B — Démonstration Florence v1 au COPIL sur données réelles. Go/No Go Phase 2.**

---

### PHASE 2 — INTÉGRATION TECHNIQUE

**Durée :** 5 jours (atelier technique)
**Objectif :** Connecter Florence aux systèmes d'information du groupe

| Jour | Work stream | Activités | Livrable | Prérequis |
|------|------------|-----------|----------|-----------|
| J1 | **Connecteur Titan** (1/2) | Contact Malta Informatique, négociation accès API, développement connecteur lecture | Connexion Titan initiée | Contact Malta fourni par DSI |
| J2 | **Connecteur Titan** (2/2) + **Emails** (1/2) | Finalisation connecteur Titan (facturation, occupation, encaissements). Début connexion boîtes emails. | Connecteur Titan opérationnel. Première boîte email connectée. | Identifiants messagerie fournis |
| J3 | **Emails** (2/2) + **ViaTrajectoire** | Connexion des 17 boîtes emails + règles de détection. Configuration monitoring ViaTrajectoire. | Module email opérationnel. Module ViaTrajectoire opérationnel. | Accès ViaTrajectoire fourni |
| J4 | **Rapport du matin** | Développement du rapport consolidé 20 établissements. Agrégation des données Titan + emails + ViaTrajectoire. Format WhatsApp optimisé. Programmation envoi 10h00. | Rapport du matin en production | Tous connecteurs actifs |
| J5 | **Interface web Florence** | Site web privé de pilotage : tableau de bord, historique, indicateurs, accès sécurisé pour M. Imbert et M. Cozon. | Interface web déployée | Données consolidées disponibles |

**Gate 2 — Recette technique. Validation de la connectivité et des flux par le COPIL.**

---

### PHASE 3 — DÉPLOIEMENT PILOTE & CONDUITE DU CHANGEMENT

**Durée :** 2 jours
**Objectif :** Mettre Florence en production sur 2 établissements pilotes et former les directeurs

| Demi-journée | Activité | Participants | Livrable |
|---|---|---|---|
| **J1 matin** | Démo complète au COPIL : Florence avec données réelles, rapport du matin, alertes, interface web | M. Imbert, M. Cozon, Korzec | PV de démonstration |
| **J1 après-midi** | Déploiement EHPAD pilote 1 : Florence en production, premier rapport réel, ajustements | Directeur pilote 1, Korzec | EHPAD 1 opérationnel |
| **J2 matin** | Déploiement EHPAD pilote 2 : mise en production, ajustements spécifiques | Directeur pilote 2, Korzec | EHPAD 2 opérationnel |
| **J2 après-midi** | Formation directeurs : utilisation de Florence via WhatsApp, guide utilisateur, FAQ | Directeurs pilotes | Support de formation + Guide utilisateur |

**Suivi post-pilote (inclus) :** 2 semaines de support à distance via le groupe WhatsApp pour ajustements.

**Gate 3 — Bilan du pilote. Go/No Go déploiement élargi aux 20 établissements.**

---

### PHASE 4 — DÉPLOIEMENT GÉNÉRALISÉ *(sur devis séparé)*

Déploiement progressif sur les 18 établissements restants, par vagues de 5.
Chaque vague inclut : connexion des boîtes emails, formation du directeur, intégration dans le rapport consolidé.

---

## 4. LIVRABLES DE LA MISSION

| Phase | Livrable | Format |
|-------|----------|--------|
| 0 | Charte projet | Document |
| 1 | Note de diagnostic stratégique | Document |
| 1 | Cartographie des Systèmes d'Information | Schéma + Document |
| 1 | Fiches diagnostic Établissement A et B | Document |
| 1 | Analyse comparative + Matrice des écarts | Document |
| 1 | Rapport d'audit consolidé | Document |
| 1B | Spécifications fonctionnelles Florence v1 | Document |
| 1B | Florence v1 — socle de connaissances opérationnel | Système IA |
| 1B | Matrice d'automatismes paramétrée | Document |
| 2 | Connecteur Titan opérationnel | Module technique |
| 2 | Module surveillance emails | Module technique |
| 2 | Module ViaTrajectoire | Module technique |
| 2 | Rapport du matin automatisé | Module technique |
| 2 | Interface web Florence | Application web |
| 3 | Support de formation | Document |
| 3 | Guide utilisateur | Document |
| 3 | PV de démonstration | Document signé |
| 3 | Bilan du pilote | Document |

---

## 5. PLANNING PRÉVISIONNEL

```
Semaine 0   ██████  Phase 0 — Cadrage + Naissance Florence
Semaine 1   ████    Phase 1 — Audit terrain (2 jours / 4 demi-journées)
Semaine 2-3 ████████  Phase 1B — Analyse + Construction (4 jours)
Semaine 3-4 ██████████  Phase 2 — Intégration technique (5 jours)
Semaine 5   ████    Phase 3 — Pilote + Formation (2 jours)
Semaine 5   ▶ Gate 3 — Go/No Go déploiement élargi
```

**Durée totale : 5 semaines**

---

## 6. FACTEURS CLÉS DE SUCCÈS

1. **Implication du COPIL** — Le sponsor et le directeur de mission sont actifs dans le groupe WhatsApp et réactifs aux gates
2. **Accès aux systèmes** — Les identifiants Titan, messagerie et ViaTrajectoire sont fournis avant le Jour 1
3. **Directeurs pilotes coopératifs** — Choisis par M. Cozon parmi ceux qui ont le plus de problèmes (motivation naturelle)
4. **Réalisme des attentes** — Florence sera opérationnelle sur les établissements pilotes en 5 semaines. Le déploiement généralisé (20 établissements) nécessite une phase supplémentaire

---

## 7. GESTION DES RISQUES

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| API Titan non disponible | Moyenne | Fort | Contact Malta Informatique dès Phase 0. Solution de contournement : lecture écran ou export CSV |
| ViaTrajectoire sans accès API | Forte | Moyen | Monitoring par surveillance email (notifications ViaTrajectoire) |
| Résistance des directeurs | Moyenne | Moyen | Formation courte (30 min), outil WhatsApp familier, Florence = alliée pas contrôleuse |
| Données incomplètes | Faible | Moyen | Complétées au fil de l'eau via interactions Florence-directeurs |
| Indisponibilité du COPIL | Faible | Fort | Points async via WhatsApp, gates planifiées à l'avance |

---

## 8. ENGAGEMENTS

- **Confidentialité** : NDA avant toute transmission de données
- **RGPD** : Aucun accès aux données médicales. Hébergement France. Effacement 30 jours (sauf facturation : 3 ans légal)
- **Qualité** : Gates de validation formelles. Aucune phase ne démarre sans accord du Sponsor
- **Transparence** : Florence partage son raisonnement en temps réel. Le COPIL voit tout
- **Réversibilité** : Restitution de toutes les données et configurations au groupe IGH en cas d'arrêt

---

*Coach Digital Paris — Gilles Korzec*
*Plan de mission confidentiel — Mars 2026*
*Référence : CDP-IGH-2026-001*
