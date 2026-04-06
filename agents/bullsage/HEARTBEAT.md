# HEARTBEAT.md — Routines Quotidiennes BullSage Trader

> Tâches récurrentes exécutées automatiquement. Chaque tâche a un déclencheur et un format de sortie.

---

## 🌅 Morning Brief — 07:00 CET (06:00 UTC)

**Déclencheur** : Chaque jour ouvré (lundi-vendredi). Samedi/dimanche : version réduite crypto-only.

**Ce que tu fais** :
1. Récupérer les prix actuels : BTC, ETH, SOL, EUR/USD, GBP/USD, USD/JPY, NQ100, SPX
2. Calculer les variations 24h et la tendance de fond (daily)
3. Consulter le calendrier économique du jour (événements à impact élevé/moyen)
4. Vérifier le Fear & Greed Index (crypto) et le VIX (indices)
5. Scanner les news majeures des dernières 12 heures
6. Identifier les niveaux clés du jour (S/R, pivots, zones de liquidité)

**Format de sortie** :
```
📋 MORNING BRIEF — [Date]
Session active : [Asie → Londres]

📊 MARCHÉS
BTC : $XX,XXX (▲/▼ X.X%) — Tendance : [haussière/baissière/neutre]
ETH : $X,XXX (▲/▼ X.X%) — Tendance : [...]
EUR/USD : X.XXXX (▲/▼ X pips) — Tendance : [...]
NQ100 : XX,XXX (▲/▼ X.X%) — Tendance : [...]

🌡️ SENTIMENT
Fear & Greed : XX/100 ([Extreme Fear/Fear/Neutral/Greed/Extreme Greed])
VIX : XX.XX ([bas/normal/élevé/alerte])

📅 CALENDRIER DU JOUR
[HH:MM] 🔴/🟡 [Événement] — Impact attendu : [description courte]

🎯 NIVEAUX CLÉS
[Actif 1] : Support XX,XXX | Résistance XX,XXX
[Actif 2] : Support X.XXXX | Résistance X.XXXX

💡 PLAN DU JOUR
[1-3 phrases sur la stratégie du jour : quoi surveiller, quoi éviter, setups potentiels]

⚠️ RISQUES
[Événements susceptibles de créer de la volatilité]
```

---

## 🔔 Midday Scan — 14:00 CET (13:00 UTC)

**Déclencheur** : Chaque jour ouvré, chevauchement Londres/New York.

**Ce que tu fais** :
1. Update des prix et volumes depuis le morning brief
2. Vérifier si les niveaux clés ont été atteints/cassés
3. Scanner les nouveaux setups formés pendant la session Londres
4. Évaluer l'impact de l'ouverture US (pre-market, gap, volume)
5. Mettre à jour les signaux actifs (ajustement stop/TP si nécessaire)

**Format de sortie** :
```
🔔 MIDDAY SCAN — [Date] 14:00 CET

📊 UPDATE MARCHÉS
[Variations depuis le morning brief — actifs principaux uniquement]

🎯 SIGNAUX ACTIFS
[Liste des signaux en cours avec status : en position / en attente / invalidé]

📊 NOUVEAUX SETUPS
[Si un setup A+ ou A s'est formé, signal complet. Sinon : "Aucun nouveau setup qualifié."]

⚡ ÉVÉNEMENTS RESTANTS
[Événements macro restants dans la journée]
```

---

## 🌙 Evening Review — 21:00 CET (20:00 UTC)

**Déclencheur** : Chaque jour ouvré. Samedi soir : weekly review.

**Ce que tu fais** :
1. Bilan complet de la journée : mouvements majeurs, volumes
2. Status de tous les signaux émis aujourd'hui (résultat)
3. P&L estimé des trades suivis
4. Identifier les setups qui se forment pour demain
5. Mettre à jour les niveaux clés pour la session Asie/Londres suivante
6. Leçons du jour : qu'est-ce qui a fonctionné, qu'est-ce qui a raté

**Format de sortie** :
```
🌙 EVENING REVIEW — [Date]

📊 BILAN DU JOUR
[Actifs principaux : variation du jour, volume, événements marquants]

📈 RÉSULTATS DES SIGNAUX
Signal 1 : [Actif] [Direction] → ✅ TP1 touché / ❌ SL touché / ⏳ En cours
Signal 2 : [...]
P&L estimé du jour : [+/- X%]

🔮 PRÉPARATION DEMAIN
[Niveaux à surveiller, événements prévus, setups en formation]

📝 LEÇONS
[Ce qui a bien fonctionné / ce qui doit être ajusté]
```

---

## 📊 Weekly Review — Samedi 21:00 CET

**Déclencheur** : Chaque samedi soir.

**Ce que tu fais** :
1. Bilan de la semaine : tendances dominantes par marché
2. Taux de réussite des signaux de la semaine (win rate, R:R moyen)
3. Analyse des erreurs et des succès
4. Perspective hebdomadaire pour la semaine suivante
5. Niveaux clés weekly à surveiller

**Format de sortie** :
```
📊 WEEKLY REVIEW — Semaine du [Date] au [Date]

📈 PERFORMANCE
Signaux émis : X
Win : X (XX%) | Loss : X (XX%) | BE : X
R:R moyen : X.X
P&L estimé : +/- X%

🏆 MEILLEUR TRADE : [Actif] [Direction] — [Raison du succès]
💀 PIRE TRADE : [Actif] [Direction] — [Raison de l'échec, leçon]

📅 PERSPECTIVE SEMAINE PROCHAINE
[Événements macro clés]
[Tendances dominantes]
[Setups en formation sur timeframes ≥ daily]
[Niveaux weekly clés par actif]
```

---

## ⚡ Alertes En Continu

**Déclencheur** : Surveillance permanente sur les actifs de la watchlist.

### Alerte Signal A+/A
```
🚨 SIGNAL A+ — [ACTIF]
[Signal formaté complet — voir SOUL.md pour le format]
```

### Alerte Niveau Clé Touché
```
⚡ NIVEAU CLÉ — [ACTIF]
[Niveau] [cassé/testé] à [prix]
Implication : [continuation/retournement/fausse cassure à confirmer]
Action : [entrer / attendre confirmation / ajuster stop]
```

### Alerte Macro Urgente
```
🔴 ALERTE MACRO
[Événement] — [Impact attendu]
Actifs impactés : [liste]
Action recommandée : [couper les positions / serrer les stops / attendre]
```

### Alerte Stop Approché
```
🛑 STOP APPROCHÉ — [ACTIF]
Position : [LONG/SHORT] depuis [prix]
Stop-Loss : [prix] — Distance restante : [X pips / $X / X%]
Action : [maintenir / ajuster / sortir avant le stop]
```

---

## 🔧 Maintenance Technique

### Vérification OpenClaw (chaque session)
```bash
npm view openclaw version          # Dernière version publiée
openclaw --version                 # Version installée
openclaw doctor                    # Diagnostic complet
openclaw health                    # État du gateway
```

### Vérification APIs (quotidienne)
- Tester la connectivité de chaque API de données
- Vérifier les limites de rate (surtout free tiers)
- Signaler immédiatement si une source de données est down

### Mise à jour Memory (fin de chaque session)
- Sauvegarder les signaux émis et leurs résultats
- Documenter les leçons apprises
- Mettre à jour la watchlist si nécessaire
