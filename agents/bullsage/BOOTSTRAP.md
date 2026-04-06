# BOOTSTRAP.md — Rituel Première Session BullSage Trader

> Ce fichier guide la première interaction avec BullSage après installation.
> Exécuter une seule fois, puis passer au fonctionnement normal via HEARTBEAT.md.

---

## Étape 1 — Vérification Technique

```bash
# Vérifier la version OpenClaw
openclaw --version
npm view openclaw version

# Vérifier que les fichiers workspace sont chargés
openclaw doctor

# Vérifier la santé du gateway
openclaw health
```

**Si openclaw doctor signale des problèmes** → les résoudre AVANT de continuer.

---

## Étape 2 — Vérification des APIs

Tester chaque API configurée dans .env :

### Finnhub
```bash
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=${FINNHUB_API_KEY}"
```
→ Doit retourner un JSON avec `c` (current price), `h` (high), `l` (low), etc.

### Alpha Vantage
```bash
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey=${ALPHA_VANTAGE_API_KEY}"
```
→ Doit retourner un JSON avec `Global Quote`.

### CoinGecko
```bash
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
```
→ Doit retourner les prix BTC et ETH avec variation 24h.

### Fear & Greed Index
```bash
curl "https://api.alternative.me/fng/?limit=1"
```
→ Doit retourner le score actuel (0-100).

**Signaler** toute API qui ne répond pas. L'analyse sera limitée aux sources fonctionnelles.

---

## Étape 3 — Configuration Personnelle

Demander à l'utilisateur :

1. **Capital de trading** (pour calculer les tailles de position)
   - "Quel est ton capital de trading total ? (utilisé uniquement pour le calcul de position sizing, jamais stocké en clair)"

2. **Broker(s) utilisé(s)**
   - "Quel(s) broker(s) utilises-tu ? (pour adapter les tickers et les spreads)"
   - Exemples : Binance (crypto), eToro, IBKR, XTB, MT4/MT5

3. **Watchlist initiale**
   - "Quels actifs veux-tu surveiller en priorité ?"
   - Défaut : BTC, ETH, SOL, EUR/USD, GBP/USD, USD/JPY, NQ100, SPX

4. **Préférence d'alertes**
   - "À quelle fréquence veux-tu les alertes ? [Signaux A+ uniquement / A+ et A / Tout]"

5. **Timezone confirmation**
   - "Confirmes-tu que tes horaires de trading sont en CET (Europe/Paris) ?"

---

## Étape 4 — Premier Morning Brief

Exécuter un Morning Brief complet pour vérifier que tout fonctionne :

1. Récupérer les données de tous les actifs de la watchlist
2. Générer le brief au format standard (voir HEARTBEAT.md)
3. Vérifier que l'envoi via le canal configuré (Telegram, etc.) fonctionne
4. Demander feedback à l'utilisateur : "Le format te convient ?"

---

## Étape 5 — Activation des Cron Jobs

```bash
# Vérifier que les cron jobs sont configurés
openclaw cron list

# Si les jobs du fichier openclaw.json ne sont pas actifs :
openclaw gateway restart
openclaw cron list
```

Jobs attendus :
- `morning-brief` : 06:00 UTC lun-ven
- `morning-brief-weekend` : 08:00 UTC sam-dim
- `midday-scan` : 13:00 UTC lun-ven
- `evening-review` : 20:00 UTC lun-ven
- `weekly-review` : 20:00 UTC sam

---

## Étape 6 — Message de Confirmation

```
📈🐂 BullSage Trader est opérationnel.

✅ OpenClaw : v[VERSION]
✅ APIs : [X/Y] connectées
✅ Watchlist : [liste des actifs]
✅ Alertes : [fréquence choisie]
✅ Canal : [Telegram/WhatsApp/etc.]
✅ Cron jobs : [X] tâches planifiées

Je suis prêt à analyser. Demande-moi un signal sur n'importe quel actif, 
ou attends le prochain Morning Brief programmé à [heure].

⚠️ Rappel : Je suis un outil d'analyse, pas un conseiller financier agréé. 
Toute décision de trading reste la tienne.
```

---

## Post-Bootstrap

Après la première session :
- Supprimer ou ignorer ce fichier — il ne sert qu'une fois
- Le fonctionnement quotidien est géré par HEARTBEAT.md
- Les mises à jour de configuration passent par AGENTS.md et TOOLS.md
