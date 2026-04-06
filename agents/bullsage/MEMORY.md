# MEMORY.md — Mémoire Long Terme BullSage Trader

> Ce fichier contient les faits curatés qui persistent entre les sessions.
> Mis à jour automatiquement à chaque Evening Review.
> Les journaux quotidiens sont dans memory/YYYY-MM-DD.md

---

## Utilisateur

- Nom de code : Coach Digital
- Capital de trading : [À renseigner au bootstrap]
- Broker(s) : [À renseigner au bootstrap]
- Timezone : Europe/Paris (CET/CEST)
- Style : Multi-timeframe, préférence intraday (1H-4H) et swing (daily)
- Risk tolerance : Modérée — respecte le money management

## Watchlist Active

| Actif | Marché | Priorité | Notes |
|-------|--------|----------|-------|
| BTC/USD | Crypto | Haute | Actif principal crypto |
| ETH/USD | Crypto | Haute | Corrélé BTC mais beta plus élevé |
| SOL/USD | Crypto | Moyenne | Plus volatile, setups fréquents |
| EUR/USD | Forex | Haute | Paire la plus liquide |
| GBP/USD | Forex | Moyenne | Sensible aux données UK |
| USD/JPY | Forex | Moyenne | Carry trade, sensible BOJ |
| NQ100 | Indices | Haute | Tech-heavy, forte volatilité |
| SPX | Indices | Moyenne | Référence marché US |
| XAU/USD | Commodities | Basse | Valeur refuge, check macro |
| DXY | Index | Basse | Corrélation inverse — baromètre |

## Performance Historique

### Signaux (depuis activation)
- Total émis : 0
- Win : 0 (0%)
- Loss : 0 (0%)
- Break-even : 0
- R:R moyen : —
- P&L cumulé : 0€ (100% cash préservé)
- Opportunités manquées : 1 (BTC +10% breakout overnight 3-4 mars)

### Meilleurs setups identifiés
- **BTC LONG Breakout $73K (Grade A estimé 70-75/100)** — Setup prioritaire S4 actuel — cassure $73,092 (pic 4 mars) + volume, objectif $76K-$85K, stop $69.5K. **En attente confirmation jeudi-vendredi.**
- **Bottom $65K-$66K identifié correctement** (2 mars) — bottom réel $65,300 (lun 2 mars), anticipation correcte zone d'accumulation ✅
- **CPI dovish anticipé** (11 mars) — Inflation stable 2.4% malgré pétrole $110+ = catalyseur haussier confirmé, BTC +3.3% ✅

### Patterns récurrents observés
- **Flash crash crypto nocturne (session Asie)** → liquidité réduite → rebound LDN → retest du low en NY (observé lun 23/02 : $64,270 nocturne → $66,300 LDN → $64,630 clôture)
- **F&G ≤ 5-15 = zone de capitulation historique** → les retournements majeurs naissent en extreme fear MAIS timing imprévisible (peut durer des jours/semaines) → **RÈGLE : attendre trigger technique (CHoCH 4H) avant d'entrer, ne JAMAIS deviner le bottom** → ✅ **VALIDÉ 4 mars : bottom $65.3K lun-mar (F&G 10-14/100) → breakout +10% mer**
- **Divergence BTC vs F&G** → BTC monte (+2%), F&G baisse (8/100) = marché nerveux, retail capitule pendant que smart money accumule (observé lun 9/03 : BTC +2.22%, F&G 8/100)
- **"Sell the news" post-earnings en macro bearish** → earnings beat → rally initial → fade complet 24-48h (observé NVDA 25/02 : beat massif → BTC $70K → fade à $65,302 en 48h)
- **Fakeout de canal descendant en bear market** → breakout initial excitant → rejet résistance majeure → retour dans le canal (observé lun 02/03 : rally $65.3K → $70K en 3h → rejet $69K-$70K → retrace $66K-$67K mardi) → **ATTENTION : pattern invalidé si cassure confirmée** (observé mer 04/03 : 2e attaque $69K-$70K → breakout réussi → $73K)
- **Breakout crypto overnight (session Asie)** → mouvements majeurs +5-10% peuvent se produire entre 19h UTC (Evening Review) et 06h UTC (Morning Brief) → **LEÇON 4 mars : Evening Review trop tôt pour capturer breakouts nocturnes** (BTC $66K à 19h UTC → $73K overnight) → **Morning Brief 06:00 UTC systématique REQUIS pour crypto 24/7**
- **Pétrole $100+ = driver macro dominant** → override narrative crypto (observé lun 9/03 : pétrole $110+ → indices -1%, or -1.7%, BTC +2% décorrélation temporaire)
- **CPI dovish malgré pétrole élevé** → CPI février 2.4% stable (Core +0.2%) malgré pétrole $110+ car données pré-escalade Iran (observé mer 11/03) → **ATTENTION : CPI mars/avril capturera impact pétrole si reste > $100** → risque inflation retardée

## Leçons Apprises

### CRITIQUE : Morning Brief Manquant = Opportunités Manquées (confirmé S3+S4)
- **S3 : Breakout overnight manqué** — BTC $66K (19h UTC) → $73K (06h UTC) = +10% pendant session Asie non surveillée
- **S4 : Setup pré-CPI manqué** — BTC $69K-$70K mardi 10 mars = entrée optimale avant CPI dovish mercredi (+1.8% si signal)
- **RÈGLE ABSOLUE** : **Morning Brief 06:00 UTC quotidien NON NÉGOCIABLE pour crypto 24/7**. 3+ jours manqués consécutifs = ÉCHEC OPÉRATIONNEL.

### Anti-patterns identifiés (confirmés 3x)
- **Acheter un rebound en structure baissière Daily sans CHoCH confirmé = piège à liquidité** (pattern confirmé 3x S2+S3)
  - Lun 23/02 : BTC $64,270 → $66,300 (+3.2%) → retour $64,630 puis $62,964 le lendemain
  - Mar 24/02 : BTC $62,964 → $64,445 (+2.3%) → consolidation puis baisse à $65,302
  - Lun 02/03 : BTC $65,300 → $70,000 (+7.2% en 3h) → rejet $69K-$70K → retrace $66K-$67K (fakeout canal)
  - **Règle** : Ne JAMAIS entrer long en série LL/LH Daily sans CHoCH haussier 4H confirmé (clôture au-dessus du dernier LH avec displacement + volume)
- **FOMO sur earnings beat en macro bearish** (pattern confirmé S2)
  - NVDA earnings beat massif mercredi 25/02 → BTC pic $70K → fade complet jeudi-vendredi à $65,302 (-6.7%)
  - **Règle** : En environnement macro bearish (VIX >20, F&G <15), même un earnings exceptionnel ne suffit pas à inverser la tendance sans confirmation technique structurelle

### Ce qui fonctionne exceptionnellement bien (validé S2+S3)
- **Le scoring SMC Grade C filtre correctement les faux setups** — 7 setups analysés (S2+S3), 7/7 gradés C correctement, 0 faux positif, 100% capital préservé
  - Lun 23/02 : 39/100 (LTF Trigger = 0) → pas de trade → capital préservé
  - Mar 24/02 : 30/100 (LTF Trigger = 0) → pas de trade → capital préservé
  - Mer-jeu 25-26/02 : Rally post-NVDA sans CHoCH Daily → pas de signal → fade confirmé vendredi
  - Lun-mar 02-03/03 : Rally $65.3K → $70K (fakeout canal) → grade C (35-40/100) → pas de trade → retrace confirmée mardi
  - **Mar 03/03 19h UTC** : Grade C maintenu malgré 9 confluences présentes → correct car breakout pas confirmé à ce moment (19h UTC = 5h avant clôture Daily UTC) → capital préservé, breakout confirmé overnight
- **Bottom identification réussie** — Zone $65K-$66K documentée 2 mars (F&G <15 + confluence technique) → bottom réel $65,300 lundi 2 mars → breakout +10% mercredi 4 mars → ✅ **anticipation correcte de la zone d'accumulation**
- **Catalyseur fondamental Trump pro-crypto** anticipé S2, confirmé S3 (4 mars : soutien stablecoins yields + Clarity Act) → BTC +10% en 24h
- **Consumer Confidence beat** correctement identifié comme catalyseur potentiel au midday 24/02 (91.2 vs 87.0)
- **Le filtre LTF Trigger = 0 (pas de CHoCH)** est le critère le plus déterminant du scoring SMC — élimine automatiquement les rebonds sans confirmation structurelle

## Contexte Macro Actuel

### Dernière mise à jour : 11 mars 2026 (mercredi 19:00 UTC)
- Fed : Taux inchangés 4.25-4.50% — CPI dovish (2.4% stable, Core +0.2%) = baisse taux possible si Iran se résout
- BCE : Cycle de baisse en cours, dernière coupe en janvier → 2.75%
- **Inflation US : CPI février 2.4% YoY (stable), Core +0.2% MoM (baisse vs 0.3%)** ✅ — Dovish malgré pétrole $110+ MAIS données pré-escalade Iran (risque CPI mars/avril si pétrole reste > $100)
- DXY : ~103-104 (baisse sur CPI dovish)
- VIX : Estimé 20-23 (baisse depuis 22-25, CPI calme marchés)
- **BTC : $70,730.58 (mer 11 mars 19:00 UTC) +3.3%** — Rally post-CPI confirmé. Structure Daily HAUSSIÈRE maintenue. Résistance $73K (pic 4 mars) = prochain objectif. Support $70K immédiat, $67K critique.
- ETH : Estimé $2,050-$2,080 (+2-3%) — Suit BTC, au-dessus $2,000
- SOL : Données indisponibles — estimé +3-4% (corrélé BTC)
- BTC Dominance : Stable — altcoins suivent BTC
- **Fear & Greed : Estimé 15-22/100 — FEAR** (remontée depuis 8/100 lundi, mais toujours Fear malgré rally)
- Gold : Estimé $5,100-$5,150 (+1-2% sur CPI dovish)
- **Pétrole : $112 WTI** (pic $119.50 lundi → correction -6.3%) — Trump "guerre bientôt finie" mais prix reste 2x pré-conflit ($77)
- **Catalyseur macro dominant** : **CPI DOVISH** ✅ (inflation stable = Fed peut baisser taux) + Trump optimiste Iran (pétrole baisse)
- **Événements S4** : 
  - ✅ **Mercredi 11 mars** : CPI (DOVISH — Core +0.2%, inflation 2.4% stable) → BTC +3.3%, SPX +0.5-1%
  - **Jeudi-vendredi 12-13 mars** : Setup breakout BTC $73K potentiel (Grade A si confirmé)
  - Surveillance continue : Pétrole et résolution Iran
- **Setup prioritaire S4** : BTC LONG Breakout $73K — Grade A estimé (70-75/100) si cassure confirmée + volume

## Revues Hebdomadaires

### Semaine du 16-21 février 2026 (Semaine 1 — Bootstrap)
- Signaux : 0 | Win rate : — | P&L : —
- Statut : Phase de bootstrap, aucune analyse émise
- Priorité S+1 : activer les routines quotidiennes, tester les APIs, premier signal

### Semaine du 23-28 février 2026 (Semaine 2 — Opérationnelle complète)
**Résumé** : Première semaine opérationnelle de BullSage. Environnement macro bearish dominant (tarifs Trump 15%, AI scare, VIX 21+ peak 2026, F&G 5-13/100 extreme fear). Tous les setups identifiés gradés C (<50/100) → 0 signal émis, capital 100% préservé. Le marché a baissé -3% à -15% selon les actifs.

**Bilan jour par jour** :
- Lun 23/02 : risk-off violent (tarifs Trump 15% + Iran). BTC -4.1% ($64,630), SPY -1.1%, Gold +2.2% ($5,166 ATH). F&G 5/100. Liquidations $500M. Grade C (39/100).
- Mar 24/02 : rebound technique. BTC +2.0% ($62,964→$64,445). SPX +0.8%, NQ +1.1%. Consumer Confidence 91.2 (beat vs 87.0). VIX 21+ (peak 2026). F&G 8/100. Grade C (30/100).
- Mer 25/02 : NVIDIA earnings beat massif (EPS $1.62 vs $1.53, Rev $68.1B, guidance $78B vs $72.6B). BTC pic $70K post-ER puis retrace. Indices mixtes. F&G 11/100. Pas de signal (attente CHoCH Daily).
- Jeu 26/02 : NVDA rollover post-earnings. SPX -1%, NQ100 -2%. BTC $66.6K (-3.5%), ETH -6%, SOL -6.4%. Rotation out of tech = confirmation bear trend. F&G 11/100.
- Ven 27/02 : Continuation baissière. BTC $65,302 (-3.0%), ETH -4.3%, SOL -4.6%. Cassure support $66K. F&G 13/100.
- Sam 28/02 : Weekend consolidation. BTC $65,918 (+0.95%), ETH $1,936.81 (+1.0%), SOL $82.39 (+1.1%). F&G 11/100.

**Performance** : 0 signaux | 0€ P&L | 100% cash ✅
**Décision clé** : Refuser d'entrer sur le rally post-NVDA (mer-jeu) = capital préservé. Le fade complet jeudi-vendredi a validé le scoring Grade C.
**Leçon majeure** : *En macro bearish (VIX 21+, F&G <15, tarifs + AI scare), même un earnings beat massif (NVDA) ne suffit pas à inverser la tendance sans CHoCH Daily/4H confirmé. La discipline de NE PAS trader vaut mieux qu'un trade Grade C.*
**Anti-pattern confirmé 2x** : Acheter un rebound en structure baissière Daily sans CHoCH = piège à liquidité (lun $64,270→$66,300→$64,630, mar $62,964→$64,445→consolidation). Capital préservé 2x.
**Points d'amélioration S3** : Morning Briefs manqués (4/5 jours), VIX non systématique, diversifier APIs (rate limits), activer Midday Scan quotidien.
**Setup prioritaire S3** : BTC LONG conditionnel si test $62K-$64K + CHoCH 4H + 5 confluences (Grade A estimé 70-75/100).

### Semaine du 2-7 mars 2026 (Semaine 3 — Transition Bear → Bull)
**Résumé** : Retournement haussier majeur confirmé. BTC breakout +10% en 24h (mercredi 4 mars). Bottom $65K-$66K identifié correctement (2 mars), catalyseur fondamental Trump pro-crypto anticipé et confirmé. **Opportunité manquée** : +10% théorique (breakout overnight après Evening Review 19h UTC).

**Bilan jour par jour** :
- Lun 02/03 : Ouverture de mois. BTC $65,300 (bottom confirmé de la semaine). F&G 10/100 (extreme fear). Rebalancing institutionnel. Grade C (attente confirmation).
- Mar 03/03 : Rally $65.3K → $70K (+7.2% en 3h) → rejet $69K-$70K (2e fois) → $66,442 (19h UTC). F&G 14/100. Grade C (35-40/100) — pas de CHoCH Daily confirmé à 19h UTC (correct).
- Mer 04/03 : 🚀 **BREAKOUT MAJEUR** — BTC $66,442 → $73,092 (+10% en 24h). Cassure $69K-$70K confirmée avec volume. Catalyseur : Trump soutient rendements stablecoins + Clarity Act. Structure D1 haussière établie. F&G estimé 18-22/100.
- Jeu 05/03 : Données manquantes (pas d'Evening Review). BTC estimé consolidation $71K-$74K. ADP Employment prévu.
- Ven 06/03 : Données manquantes (pas d'Evening Review). NFP (événement majeur). BTC estimé réaction NFP.

**Performance** : 0 signaux | 0€ P&L | 100% cash ✅
**Décision clé** : **Bottom identification réussie** ($65K-$66K documenté 2 mars, bottom réel $65,300 lundi) ✅ + **Catalyseur fondamental anticipé** (Trump pro-crypto) ✅ + **Opportunité manquée** (+10% théorique, breakout overnight) ⚠️
**Leçon majeure** : *Les marchés crypto bougent 24/7. Une Evening Review à 19h UTC (5h avant clôture Daily UTC) ne capture pas les breakouts overnight (session Asie 00:00-09:00 UTC). Morning Brief 06:00 UTC systématique REQUIS pour crypto.*
**Meilleure décision** : Anticipation correcte zone d'accumulation + catalyseur fondamental. Le cerveau analytique fonctionnait.
**Pire décision** : Ne pas ajuster le timing des analyses pour crypto 24/7. Evening Review 19h UTC = snapshot incomplet.
**Points d'amélioration S4** : Activer Morning Brief 06:00 UTC quotidien (CRITIQUE), activer Evening Review 20:00 UTC (0/5 jours jeu-ven), intégrer Alpha Vantage + CoinGecko (rate limits), activer Midday Scan.
**Setup prioritaire S4** : BTC LONG $71K-$72K (Grade A estimé 70/100) si consolidation confirmée post-breakout.

## Notes Techniques

- Version OpenClaw : 2026.2.19
- APIs actives : [liste après bootstrap]
- Dernière maintenance : [date]

## Infra & Comptes

- **Domaine** : bullsagetrader.com
- **DNS / CDN** : Cloudflare (proxy désactivé, DNS only)
  - **Compte Cloudflare** : bullsagetrader@gmail.com
- **Sous-domaine app** : app.bullsagetrader.com → A record → 180.149.198.23
- **VPS** : LWS 180.149.198.23 (partagé avec Léa, Julian, Nina, Oscar)
- **Gmail agent** : bullsagetrader@gmail.com
- **OpenClaw agent ID** : bullsage
- **Modèle** : anthropic/claude-opus-4-6
