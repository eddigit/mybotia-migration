# HEARTBEAT.md — Tâches Récurrentes

> Les tâches marquées 🔄 sont automatiques (cron).
> Les tâches marquées 👤 nécessitent un échange avec Hugo.

---

## Quotidien (Chaque Session)

### Matin (Première session du jour)

- [ ] 📖 Lire SOUL.md, AGENTS.md, USER.md, MEMORY.md, memory/ (aujourd'hui + hier)
- [ ] 🔄 Vérifier la version OpenClaw : `npm view openclaw version`
- [ ] 📬 Vérifier les réponses LinkedIn reçues depuis la dernière session
- [ ] 📬 Vérifier les réponses email reçues depuis le dernier envoi
- [ ] 📊 Mettre à jour la pipeline dans memory/ (nouveau jour = nouveau fichier)
- [ ] 👤 Briefing à Hugo : actions en attente, réponses reçues, validations en cours

### En continu

- [ ] 💼 Préparer les messages de prospection du jour (LinkedIn + email)
- [ ] 👤 Soumettre les messages à Hugo (format standardisé) pour transmission au CEO
- [ ] ⏳ Attendre validation du CEO via Hugo
- [ ] 🔄 Envoyer les messages validés (via browser/email)
- [ ] 📝 Logger chaque envoi dans memory/ : prospect, message, date, statut

### Fin de journée

- [ ] 📊 Résumé du jour dans memory/YYYY-MM-DD.md
- [ ] 🔍 Identifier les prospects à relancer demain (J+5 à J+7)
- [ ] 👤 Report de fin de journée à Hugo

---

## Hebdomadaire (Chaque Lundi)

- [ ] 📊 Rapport hebdomadaire à Hugo (pour transmission au CEO) :
  - Volume d'activité (messages, emails, invitations)
  - Taux de réponse par canal et par segment
  - Nombre de RDV obtenus
  - Prospects chauds en cours
  - Suggestions d'ajustement de la stratégie
- [ ] 🎯 Planifier les segments de la semaine
- [ ] 🔄 Vérifier la mise à jour OpenClaw
- [ ] 🧹 Nettoyer les prospects en impasse

---

## Mensuel (Premier lundi du mois)

- [ ] 📊 Rapport mensuel complet à Hugo :
  - Funnel : contacts → réponses → RDV → conversions
  - Taux par segment
  - Top 5 messages les plus performants
  - Anti-patterns identifiés
- [ ] 🎯 Révision de stratégie (propositions à remonter)
- [ ] 🧹 Maintenance base de contacts (bounces, désinscriptions, mises à jour profils)

---

## Format du Journal Quotidien (memory/YYYY-MM-DD.md)

```markdown
# Nina — Journal du [DATE]

## Résumé
- Messages LinkedIn envoyés : X
- Emails envoyés : X
- Réponses reçues : X
- RDV obtenus : X

## Actions réalisées
1. [Action] — [Résultat]

## Réponses reçues
- Me [Nom] ([Spécialité]) — Réponse : [positive/négative/question] — Suite : [action prévue]

## Prospects en attente de relance
- Me [Nom] — Premier contact le [date] — Relance prévue le [date]

## Validations en attente du CEO
- [Message X pour Me Y] — Soumis à Hugo le [date]

## Notes / Observations
- [Insights, patterns, suggestions]

## Prochaines actions
1. [Priorité 1]
2. [Priorité 2]
```

---

## Cron Jobs

```json
[
  {
    "id": "nina-morning-check",
    "schedule": "0 8 * * 1-5",
    "agentId": "nina",
    "message": "C'est le matin. Vérifie les réponses LinkedIn et email, mets à jour la pipeline, et prépare le briefing pour Hugo."
  },
  {
    "id": "nina-weekly-report",
    "schedule": "0 9 * * 1",
    "agentId": "nina",
    "message": "C'est lundi. Prépare le rapport hebdomadaire pour Hugo."
  },
  {
    "id": "nina-relance-check",
    "schedule": "0 14 * * 1-5",
    "agentId": "nina",
    "message": "Identifie les prospects à relancer (J+5/J+7) et prépare les messages à soumettre à Hugo."
  }
]
```
