# Vision "Oscar & Associés"

*Définie avec Gilles — 04/02/2026 01:37*

---

## Le Concept

**Une équipe d'agents IA au service des cabinets d'avocats.**

Pas juste un logiciel. Un vrai collaborateur digital dédié à chaque cabinet.

---

## Architecture

```
VPS Central (Coach Digital)
│
├── 🧠 Oscar (Agent Principal)
│   └── Bras droit de Gilles
│   └── Supervision des autres agents
│   └── Clients stratégiques
│
├── 💼 Agent Commercial
│   └── Prospection LinkedIn
│   └── Envoi d'emails
│   └── Lead generation
│   └── Qualification prospects
│
├── ⚖️ Agent Cabinet [Client 1]
│   └── Personnalisé (nom, avatar)
│   └── WhatsApp dédié
│   └── Connecté à leur agenda
│   └── Formé sur leur pratique
│
├── ⚖️ Agent Cabinet [Client 2]
│   └── ...
│
└── ⚖️ Agent Cabinet [Client N]
    └── ...
```

---

## Ce que chaque cabinet reçoit

| Élément | Détail |
|---------|--------|
| Agent personnalisé | Nom choisi, avatar choisi, ton adapté |
| Numéro WhatsApp | Dédié au cabinet |
| Connexion agenda | Google Calendar / Outlook |
| Connexion CRM | Notre logiciel Cabinet 2.0 |
| Formation | Sur leur pratique, leurs clients, leur vocabulaire |

---

## Modèle Économique

### Offres

| Formule | Contenu | Prix/mois |
|---------|---------|-----------|
| **Logiciel** | App seule + support email | 400€ |
| **Logiciel + Agent** | App + IA assistant dédié | 800-1200€ |
| **Full Partenaire** | App + Agent + Gilles (DSI externalisé) | 1500€+ |

### Coûts estimés par agent

| Poste | Coût mensuel |
|-------|--------------|
| VPS (mutualisé) | ~2-5€/agent |
| API Claude (Sonnet) | ~20-50€/agent selon usage |
| Numéro WhatsApp | ~10€/agent |
| **Total** | ~30-65€/agent |

**Marge brute : 85-95%** sur l'offre "Logiciel + Agent"

---

## Optimisation des Coûts IA

| Agent | Modèle | Justification |
|-------|--------|---------------|
| Oscar | Opus 4.5 | Tâches complexes, stratégie |
| Commercial | Sonnet 4.5 | Prospection, routine |
| Agents clients | Sonnet 4.5 | Support, RDV, routine |

→ Opus uniquement quand nécessaire, Sonnet pour le volume

---

## Avantages Compétitifs

### Pour les cabinets clients
- **Pas de recrutement** — L'agent est opérationnel immédiatement
- **Pas de formation** — On s'en charge
- **Pas de congés** — Disponible 24/7
- **Coût prévisible** — Forfait mensuel fixe
- **Données locales** — Confidentialité garantie

### Pour nous (Coach Digital)
- **Revenus récurrents** — MRR scalable
- **Différenciation** — Personne ne fait ça
- **Upsell naturel** — Logiciel → Agent → Full
- **Scalable** — Un VPS peut héberger des dizaines d'agents
- **Stickiness** — Client formé = client fidèle

---

## Plan de Déploiement

### Phase 1 : Infrastructure (Semaine du 04/02)
- [ ] Louer VPS Ubuntu (OVH/Scaleway ~10€/mois)
- [ ] Installer OpenClaw + Oscar
- [ ] Chrome headless pour autonomie browser
- [ ] Migrer WhatsApp Oscar
- [ ] Configurer API Google Calendar

### Phase 2 : Agent Commercial (Semaine du 10/02)
- [ ] Créer instance agent commercial
- [ ] Connecter LinkedIn
- [ ] Configurer envoi emails
- [ ] Définir scripts de prospection
- [ ] Former sur le pitch "Logiciel + Agent"

### Phase 3 : Premier Client Pilote (Février/Mars)
- [ ] Identifier un cabinet pilote (Clarisse Surin ?)
- [ ] Déployer agent personnalisé
- [ ] Période test gratuite ou réduite
- [ ] Collecter feedback
- [ ] Ajuster l'offre

### Phase 4 : Commercialisation (Mars/Avril)
- [ ] Offre packagée finalisée
- [ ] Site web dédié (landing page)
- [ ] Agent commercial en mode actif
- [ ] Premiers clients payants

---

## Questions Ouvertes

1. **Nom du service ?** — "Oscar & Associés" ? Autre chose ?
2. **Nom de l'IA pour les clients ?** — Ils choisissent ou on propose ?
3. **WhatsApp Business API ?** — Nécessaire pour scale (numéros multiples)
4. **Hébergement données client ?** — Sur notre VPS ou chez eux ?
5. **Formation agents** — Process standardisé à créer

---

## Inspirations

- **Intercom** — Chat support automatisé
- **Drift** — Chatbots B2B
- **Harvey AI** — IA pour avocats (mais cloud US)

Notre différence : **local, personnalisé, avec un humain (Gilles) dans la boucle**

---

*Document vivant — à enrichir au fil du projet*
