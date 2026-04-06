# DOSSIER IMBERT — EHPAD & Cliniques

## Contact
- **Interlocuteur principal** : Stéphane (bras droit / directeur opérationnel)
- **PDG** : M. Imbert
- **Email** : À récupérer
- **Téléphone** : À récupérer
- **Statut** : Prospect — RDV qualifié le 9 mars 2026

---

## Infos clés (réunion 9 mars 2026 — Gilles + Stéphane)

### Structure du groupe
- **17 EHPAD** (pas 52 comme estimé initialement)
- **3 Cliniques** (facturation différente, à traiter séparément)
- **Total : 20 établissements**
- Taille variable : entre **65 et 95 lits** par EHPAD (moyenne ~80)
- Un EHPAD récemment repris côté **La Rochelle** (gros problèmes admin)

### Logiciel actuel
- **TITAN** (éditeur : Malta Informatique, groupe Equasens/Welcoop)
- Nouvelle version : **TitanLink** (full web)
- URL type : `lupin-ehpad.titanweb.fr`
- **Interopérabilité** : Malta annonce des capacités d'intégration (HL7, échanges avec SI existants)
- **API** : Pas de documentation API publique trouvée — à contacter Malta Informatique directement (+33 5 57 35 19 25 / contact.malta@equasens.com)
- **⚠️ Si Titan a une API** → on peut lire directement les données (lits, factures, encaissements) sans dépendre des directeurs
- **⚠️ Si pas d'API** → collecte via l'IA (WhatsApp/email aux directeurs)

---

## Problématiques identifiées (verbatim Stéphane)

### 1. 🔴 Facturation mensuelle — "Le cauchemar"
- **80 lits = 80 factures par EHPAD chaque fin de mois**
- Le **20 de chaque mois** → émission des factures de séjour pour le mois suivant
- Factures **payables d'avance** → avant le **5 du mois suivant**
- Payeurs : famille du pensionnaire, le pensionnaire, ou son tuteur
- **Problème** : quand on appelle un directeur "Combien vous avez encaissé ?" → "Ah je ne sais pas"
- **Problème** : "Combien de pensionnaires ?" → réponses approximatives ou au hasard
- Stéphane veut **arrêter ça**

### 2. 🔴 Documents administratifs obligatoires — "Documents à la con"
- Obligations réglementaires non respectées par les directeurs
- Exemple concret : **EHPAD La Rochelle** → directeur n'a pas envoyé les documents en temps et en heure
- **Inspection du travail a débarqué "la rage entre les dents"**
- Besoins :
  - Lister TOUTES les tâches administratives obligatoires par établissement
  - L'IA **contrôle** que le directeur l'a fait (pas le faire à sa place)
  - Alerter Stéphane/Imbert si deadline ratée
  - **"J'appuie sur un bouton et ma copine l'IA me dit que tu n'as pas fait ça"**

### 3. 🔴 Gestion du courrier physique — "Courriers maltraités"
- Les établissements reçoivent du **courrier physique** (ARS, inspection du travail, CPAM, préfecture, etc.)
- **Problème** : courriers oubliés, pas ouverts, pas traités en temps et en heure
- **Conséquences** : carences constatées, incidents, **PV et amendes** à payer
- L'administration sanctionne parce qu'un courrier n'a pas été géré
- **Solution IA** :
  1. Le directeur **scanne/photographie** le courrier reçu (depuis son téléphone)
  2. L'IA **lit et analyse** le document (OCR + compréhension)
  3. L'IA **identifie** : expéditeur, objet, deadline de réponse, urgence
  4. **Enregistre** dans le hub central avec date de réception
  5. **Alerte** si une réponse est requise avec deadline
  6. **Relance** le directeur si pas traité dans les délais
  7. **Escalade** à Stéphane/Imbert si deadline critique approche
- Traçabilité complète : on sait quel courrier est arrivé où, quand, et s'il a été traité

### 4. 🔴 Via Trajectoire — Demandes de placement non traitées
- Les EHPAD reçoivent des **demandes de placement** via l'outil **Via Trajectoire** (outil national)
- **Problème** : c'est le plus réactif qui emporte le pensionnaire → certains directeurs ne traitent pas les dossiers à temps et **perdent des admissions**
- **Solution IA** :
  1. Détecter les nouvelles demandes Via Trajectoire reçues
  2. Alerter le directeur : "Tu as reçu X demandes, les as-tu traitées ?"
  3. **Aider à traiter** : proposer des créneaux RDV famille, envoyer une réponse type
  4. Relancer si pas traité dans les 24-48h
  5. Escalade si demande critique non traitée
- **Bonus** : secrétariat téléphonique IA pour la prise de RDV familles (IA vocale type réception d'appels)

### 5. 🟡 Suivi des impayés et relances
- Pas de visibilité sur payés vs impayés
- Relances manuelles (ou pas de relances du tout)
- L'IA pourrait envoyer des mails de relance automatiques

---

## Ce que Stéphane veut (ses mots)

> "Tous les matins à 10h, un rapport d'où est-ce qu'on en est."
> "La condition, c'est que ce soit simple pour moi."
> "Cadrer les directeurs et les directrices, gentiment."

### Fonctionnalités attendues :
1. **Rapport quotidien 10h** — État de chaque établissement (lits, encaissements, docs)
2. **Simplicité absolue** — Stéphane ne veut rien de compliqué
3. **Contrôle des directeurs** — L'IA vérifie qu'ils ont fait leur boulot
4. **Alertes proactives** — Documents manquants, retards, impayés
5. **Relances automatiques** — Aux familles pour les impayés (avec GO avant envoi)
6. **L'IA en réunion** — Peut participer aux réunions mensuelles, prendre les tâches, suivre

---

## Architecture proposée (à affiner)

### Phase 1 — Lecture Titan (si API dispo)
- Connexion API Titan → lire lits occupés, factures, encaissements
- Dashboard consolidé pour Stéphane/Imbert
- Rapport automatique quotidien 10h
- Zéro effort pour les directeurs

### Phase 2 — Cadrage admin : Formulaires obligatoires type Wizard
**Concept** : Pour chaque obligation administrative, un **formulaire slider plein écran** (type wizard/stepper) :
- Étapes : Suivant → Suivant → Suivant → Valider
- **Champs obligatoires** à chaque étape (impossible de passer sans remplir)
- Design **moderne, propre, mobile-first** (les directeurs remplissent depuis leur téléphone ou PC)
- Une fois validé :
  1. L'IA récupère automatiquement les données
  2. Met à jour le **hub centralisé** (dashboard Stéphane/Imbert)
  3. **Notifie les personnes concernées** : "M. Dupont (EHPAD Tamaris) a complété le formulaire X"
- Si pas rempli à la deadline → relances automatiques + alerte escalade

**Avantages** :
- Zéro ambiguïté : champs obligatoires = données complètes à chaque fois
- Zéro formation : interface intuitive type questionnaire
- Traçabilité totale : qui a rempli quoi, quand
- Vérification automatique : l'IA sait immédiatement si c'est fait ou pas

**Exemples de formulaires wizard** :
- Rapport mensuel lits (occupés, payés, impayés)
- Déclaration documents réglementaires (inspection du travail, ARS, etc.)
- Signalement incident
- Demande de maintenance / travaux

### Phase 2b — Suivi admin + relances (en complément)
- Agent IA contacte chaque directeur (WhatsApp ou email)
- Checklist documents obligatoires par établissement
- Contrôle automatique des deadlines
- Alertes et escalade

### Phase 3 — Relances impayés
- L'IA identifie les impayés via Titan
- Génère les courriers/mails de relance
- Soumis à validation avant envoi

---

## Prochaines étapes (ordre de priorité validé par Gilles)

### 🥇 PRIORITÉ 1 — Les paiements
- Facturation mensuelle, encaissements, impayés, relances
- C'est le nerf de la guerre → on commence par là

### 🥈 PRIORITÉ 2 — Connexion API Titan
- Vérifier si TitanLink a une API → contacter Malta Informatique (+33 5 57 35 19 25)
- Si API dispo → on automatise tout (lecture lits, factures, encaissements)
- Si pas d'API → collecte via formulaires wizard + IA

### Suite
- [ ] Récupérer la liste des 17 EHPAD (noms, tailles, directeurs)
- [ ] Récupérer la liste des documents administratifs obligatoires
- [ ] Identifier 2-3 EHPAD pilotes pour le test
- [ ] Chiffrer la solution (fonction de API Titan oui/non)
- [ ] Préparer une démo / maquette dashboard

---

## Chiffrage (à revoir selon API Titan)

### Si API Titan disponible :
| Poste | Montant |
|-------|---------|
| Setup initial (intégration API + dashboard) | 8 000 - 15 000€ |
| Abonnement mensuel (17 EHPAD) | 300-500€/EHPAD = 5 100 - 8 500€/mois |
| **CA annuel** | **61 200 - 102 000€** |

### Si pas d'API (collecte IA) :
| Poste | Montant |
|-------|---------|
| Setup initial (agents IA + dashboard) | 5 000 - 10 000€ |
| Abonnement mensuel (17 EHPAD) | 200-400€/EHPAD = 3 400 - 6 800€/mois |
| **CA annuel** | **40 800 - 81 600€** |

→ **Dossier à 5-6 chiffres/an.**

---

## 🔒 RGPD — Point critique soulevé en réunion

- **Données médicales** : même le directeur n'a pas le droit d'y accéder → l'IA non plus
- **Stéphane connaît bien le sujet** (était référent RGPD avec Nile il y a 3 ans)
- **Solution évoquée** : hébergement **100% local** (serveur au siège du groupe)
  - Pas de données sur des serveurs étrangers
  - L'API Titan crée un pont, données stockées en local uniquement
  - Effacement automatique après 30 jours (sauf facturation = 3 ans de conservation)
- **Argument de vente** : notre IA peut tourner en local, les données ne sortent pas → conforme RGPD
- Gilles a mentionné que notre système garde tout en local ("Nuclone" / approche locale)
- ⚠️ **Point à creuser** : hébergement HDS (Hébergeur de Données de Santé) potentiellement requis même si local

## Notes réunion
- Gilles a prévenu Stéphane que l'IA enregistre la conversation → Stéphane OK
- Stéphane est pragmatique, veut du concret et du simple
- Le mot clé : **"contrôler que c'est fait"** (pas faire à la place des directeurs)
- Les cliniques sont un sujet séparé (facturation différente)
- Gilles a bien positionné le collaborateur IA vs l'IA généraliste ("c'est plus du tout l'IA qui a des milliards de connaissances")
- **Ce qui a plu à Stéphane** : "Aider les directeurs sur site à gérer les tâches administratives, ne serait-ce qu'en leur rappelant qu'on est le 20 du mois, est-ce que la facturation est bien partie ? Vérifier qu'elle est bien partie, aller dans le logiciel, voir que la facturation a été faite."
- Via Trajectoire : outil clé pour les admissions, réactivité = revenus

---
*Créé le 5 mars 2026 — Mis à jour le 9 mars 2026 après RDV Stéphane*
*Par Léa — Direction Admin & Juridique*
