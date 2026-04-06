# OPTION A — Agent IA WhatsApp pour les 52 EHPAD Imbert

## Comment ça marche concrètement

### Le principe
Chaque directeur d'EHPAD reçoit un **numéro WhatsApp dédié** (ou est ajouté à un groupe). Un agent IA (clone de Léa) lui pose des questions simples chaque jour et consolide tout pour M. Imbert.

---

## ARCHITECTURE

```
                    ┌─────────────────────────┐
                    │   M. IMBERT (PDG)       │
                    │   Dashboard + Alertes    │
                    │   WhatsApp + Web         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   AGENT IA CENTRAL      │
                    │   "Léa Santé"           │
                    │   (OpenClaw VPS)        │
                    └────────────┬────────────┘
                                 │
            ┌────────┬───────┬───┴───┬────────┬────────┐
            ▼        ▼       ▼       ▼        ▼        ▼
         EHPAD 1  EHPAD 2  EHPAD 3  ...    EHPAD 51  EHPAD 52
         Dir. A   Dir. B   Dir. C          Dir. X    Dir. Y
        (WhatsApp)(WhatsApp)(WhatsApp)     (WhatsApp)(WhatsApp)
```

### 1 agent central, pas 52
On ne crée PAS 52 agents séparés (trop cher, trop complexe). On crée **1 agent IA** qui gère les 52 conversations WhatsApp simultanément. Chaque directeur est identifié par son numéro de téléphone.

---

## CYCLE QUOTIDIEN

### J1 à J24 — Mode collecte normale

**Chaque matin à 9h**, l'agent envoie à chaque directeur :

> Bonjour [Prénom] 👋
> Point rapide de votre établissement :
> 
> 1️⃣ Lits occupés aujourd'hui ? (nombre)
> 2️⃣ Nouvelles entrées depuis hier ?
> 3️⃣ Sorties/décès depuis hier ?
> 4️⃣ Quelque chose à signaler ?
> 
> Vous pouvez répondre en une ligne : "42 lits, 1 entrée, 0 sortie, RAS"

**Si pas de réponse à 12h** → relance douce :
> [Prénom], petit rappel pour le point du jour quand vous avez 2 minutes 🙏

**Si pas de réponse à 17h** → signalement à M. Imbert :
> ⚠️ [EHPAD X] — [Prénom] n'a pas répondu aujourd'hui.

### J25 à J31 — Mode facturation intensif

**Chaque matin à 8h30** :
> Bonjour [Prénom],
> On est en période de facturation 📋
> 
> J'ai besoin de votre bilan précis :
> 
> 1️⃣ Nombre total de lits occupés ce jour ?
> 2️⃣ Nombre de lits PAYÉS (résidents à jour) ?
> 3️⃣ Nombre de lits IMPAYÉS (retards de paiement) ?
> 4️⃣ Montant total des impayés estimé ?
> 5️⃣ Lits réservés non occupés ?
> 
> ⚠️ Merci de répondre AVANT 14h — c'est pour la facturation du groupe.

**Si pas de réponse à 11h** → relance urgente :
> [Prénom], la facturation du groupe dépend de votre retour. Pouvez-vous me donner les chiffres avant 14h ? 🙏

**Si pas de réponse à 14h** → alerte rouge à M. Imbert :
> 🔴 [EHPAD X] — [Prénom] n'a PAS transmis les données de facturation. Appel direct recommandé.

### Fin de mois — Rapport automatique

**Le 28 ou dernier jour ouvré**, l'agent génère automatiquement :

```
═══════════════════════════════════════
RAPPORT MENSUEL — GROUPE IMBERT
Mars 2026
═══════════════════════════════════════

CONSOLIDÉ GROUPE :
• Lits totaux : 2 340
• Lits occupés : 2 187 (93,5%)
• Lits payés : 2 041 (93,3% des occupés)
• Lits impayés : 146 (6,7%)
• Montant impayés estimé : 438 000€

TOP 5 ÉTABLISSEMENTS IMPAYÉS :
1. EHPAD Les Oliviers (Marseille) — 23 lits impayés — 69 000€
2. Clinique Bel Air (Lyon) — 18 lits impayés — 54 000€
3. ...

DIRECTEURS NON RÉPONDANTS CE MOIS :
• EHPAD Soleil (Nice) — 8 jours sans réponse
• ...

TAUX DE RÉPONSE GLOBAL : 89%
═══════════════════════════════════════
```

---

## DASHBOARD M. IMBERT

### Option simple : Notion (inclus)
Une base de données Notion avec :
- 1 ligne par établissement
- Colonnes : Nom, Directeur, Lits total, Occupés, Payés, Impayés, Dernière MàJ, Alerte
- Vue tableau + vue carte + vue calendrier
- Filtres : par région, par taux d'impayés, par retard de réponse
- M. Imbert y accède depuis son téléphone (app Notion)

### Option avancée : Dashboard web custom (+supplément)
- Interface web dédiée avec graphiques
- Carte de France avec les 52 établissements
- Graphiques d'évolution mensuelle
- Export PDF/Excel pour la compta
- Login sécurisé

**Recommandation** : Démarrer avec Notion (gratuit, rapide), upgrader en web custom si besoin.

---

## MISE EN PLACE — ÉTAPES

### Phase 1 — Pilote (Semaine 1-2) → 3-5 EHPAD

**Jour 1-2 : Préparation**
- Récupérer la liste des 52 établissements (nom, directeur, téléphone, nb lits)
- Choisir 3-5 EHPAD pilotes (les plus problématiques = meilleure démo)
- Créer la base Notion avec les 52 établissements
- Configurer l'agent IA sur notre VPS OpenClaw

**Jour 3 : Onboarding directeurs pilotes**
- M. Imbert envoie un message aux directeurs pilotes :
  "Bonjour, on met en place un assistant pour simplifier les remontées mensuelles.
   Vous allez recevoir un message WhatsApp de Léa, notre assistante.
   Répondez-lui comme vous répondriez à une collègue. C'est simple et rapide."
- L'agent envoie son premier message de présentation

**Jour 4-14 : Test**
- Collecte quotidienne sur les 3-5 pilotes
- Ajustement des questions selon les retours
- Premier mini-rapport envoyé à M. Imbert

**Fin semaine 2 : Bilan pilote avec M. Imbert**
- Ça marche ? Les directeurs répondent ?
- Les données sont utiles ?
- GO pour déploiement sur les 52 ?

### Phase 2 — Déploiement (Semaine 3-4) → 52 EHPAD

- Onboarding par vagues de 10-15 établissements
- Chaque vague = 2-3 jours
- Support continu pour les directeurs qui galèrent
- Dashboard Notion complet opérationnel

### Phase 3 — Optimisation (Mois 2+)

- Ajout de questions spécifiques selon les besoins
- Intégration avec le logiciel de facturation (si API disponible)
- Rapports PDF automatiques
- Upgrade vers dashboard web si nécessaire

---

## TECHNIQUE — CE QU'ON UTILISE

| Composant | Outil | Coût |
|-----------|-------|------|
| Agent IA | OpenClaw sur notre VPS | Déjà en place |
| Modèle IA | Claude Sonnet (pas besoin d'Opus pour ça) | ~50-100€/mois |
| WhatsApp | Numéro dédié "Léa Santé" | ~10€/mois |
| Base de données | Notion (ou Supabase) | Gratuit → 20€/mois |
| Hébergement | Notre VPS existant | Déjà payé |
| Cron jobs | OpenClaw cron (envoi auto 9h, relances) | Inclus |

**Coût de fonctionnement pour nous : ~100-150€/mois max**

---

## TARIFICATION CLIENT

### Par EHPAD/Clinique :
| Poste | Montant |
|-------|---------|
| Setup initial (onboarding + config) | 150€ une fois |
| Abonnement mensuel | 200€/mois |

### Pour le groupe (52 établissements) :
| Poste | Montant |
|-------|---------|
| Setup global (base, dashboard, agent) | 5 000€ une fois |
| Abonnement mensuel (52 × 200€) | **10 400€/mois** |
| **CA annuel** | **124 800€/an** |

### Marge :
- Coût réel : ~150€/mois
- Revenu : 10 400€/mois
- **Marge : ~98%**

### Alternative — Forfait groupe :
- Forfait tout compris : **7 500€/mois** (remise volume)
- = 144€/EHPAD/mois (au lieu de 200€)
- CA annuel : 90 000€
- Marge : ~98%

---

## ARGUMENTS DE VENTE

1. **Zéro formation** — Les directeurs savent utiliser WhatsApp
2. **Déploiement en 2 semaines** — Pas 6 mois de projet IT
3. **ROI immédiat** — Récupérer ne serait-ce que 5% des impayés non détectés = des centaines de milliers d'euros
4. **Pas de logiciel à installer** — Tout passe par WhatsApp + un dashboard web
5. **Escalade automatique** — Plus besoin de courir après les directeurs
6. **Rapport de facturation prêt le 28** — Plus de retard, plus de stress

### Le pitch :
> "M. Imbert, imaginez : le 28 de chaque mois, vous recevez automatiquement un rapport complet avec le nombre exact de lits payés et impayés dans vos 52 établissements. Sans avoir à appeler un seul directeur. L'IA s'en charge tous les jours."

---

## RISQUES ET SOLUTIONS

| Risque | Solution |
|--------|----------|
| Directeurs ne répondent pas | Escalade automatique + M. Imbert prévenu en temps réel |
| Données erronées | Croisement avec données historiques + alertes si incohérence |
| Confidentialité des données | Hébergement France, pas de partage, accès restreint |
| Directeurs technophobes | WhatsApp = le plus simple possible, réponse en 1 ligne |
| Changement de directeur | Onboarding automatique du nouveau en 5 min |

---
*Option A — Version détaillée — Créé le 5 mars 2026 par Léa*
