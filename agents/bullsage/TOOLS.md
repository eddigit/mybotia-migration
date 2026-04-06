# TOOLS.md — Outils & Sources de Données BullSage Trader

> Ce fichier documente les outils et APIs que BullSage utilise pour ses analyses.
> Mets à jour ce fichier quand tu ajoutes/retires une source de données.

---

## APIs de Données de Marché

### Finnhub (PRIORITÉ 1)
- **URL** : https://finnhub.io
- **Tier** : Free — 60 calls/min
- **Ce qu'il fournit** :
  - Prix temps réel (stocks US, forex, crypto)
  - News financières avec sentiment
  - Calendrier économique
  - Earnings calendar
  - Recommandations analystes
  - Indicateurs fondamentaux
- **Endpoints clés** :
  - `/quote` — Prix temps réel
  - `/news` — News par catégorie ou symbole
  - `/calendar/economic` — Calendrier économique
  - `/indicator` — Indicateurs techniques
  - `/crypto/candles` — Chandelles crypto
  - `/forex/candles` — Chandelles forex
- **Limites** : Le free tier ne donne pas les données intraday < 1 minute pour les stocks US

### Alpha Vantage (PRIORITÉ 2)
- **URL** : https://www.alphavantage.co
- **Tier** : Free — 25 calls/jour (premium disponible)
- **Ce qu'il fournit** :
  - Données historiques (daily, weekly, monthly, intraday)
  - 50+ indicateurs techniques calculés côté serveur (SMA, EMA, RSI, MACD, Bollinger, Stochastic, ADX, CCI, etc.)
  - Forex temps réel
  - Crypto données
  - News avec sentiment AI
  - Support MCP pour agents AI
- **Endpoints clés** :
  - `TIME_SERIES_INTRADAY` — Chandelles intraday (1, 5, 15, 30, 60 min)
  - `TIME_SERIES_DAILY` — Chandelles daily
  - `SMA`, `EMA`, `RSI`, `MACD`, `BBANDS`, `STOCH`, `ADX` — Indicateurs directs
  - `FX_DAILY`, `FX_INTRADAY` — Forex
  - `DIGITAL_CURRENCY_DAILY` — Crypto
  - `NEWS_SENTIMENT` — News avec score de sentiment
- **Limites** : 25 calls/jour en free — à utiliser stratégiquement (indicateurs techniques pré-calculés, pas de spam)

### CoinGecko (PRIORITÉ 3 — Crypto)
- **URL** : https://www.coingecko.com/api
- **Tier** : Free — 30 calls/min (pas de clé nécessaire en free)
- **Ce qu'il fournit** :
  - Prix, volume, market cap de 10,000+ cryptos
  - Données historiques
  - Dominance BTC
  - Trending coins
  - Fear & Greed via endpoint dédié
  - DeFi données (TVL, etc. via intégration)
- **Endpoints clés** :
  - `/simple/price` — Prix multi-cryptos en une requête
  - `/coins/{id}/market_chart` — Historique prix + volume
  - `/global` — Données globales (dominance, market cap total)
  - `/search/trending` — Cryptos trending
  - `/coins/{id}/ohlc` — Chandelles OHLC
- **Limites** : Données retardées de quelques minutes en free. Pro pour temps réel pur.

### Twelve Data (COMPLÉMENT)
- **URL** : https://twelvedata.com
- **Tier** : Free — 800 calls/jour, 8 calls/min
- **Ce qu'il fournit** :
  - Time series multi-asset uniforme (stocks, forex, crypto, ETF, indices)
  - Indicateurs techniques
  - WebSocket pour streaming
- **Usage principal** : Backup quand Finnhub ou Alpha Vantage sont saturés

### Financial Modeling Prep (FONDAMENTAUX)
- **URL** : https://financialmodelingprep.com
- **Tier** : Free — 250 calls/jour
- **Ce qu'il fournit** :
  - Fondamentaux d'entreprise (income statement, balance sheet, cash flow)
  - Ratios financiers
  - Earnings surprises
  - SEC filings
  - Données économiques
  - News par ticker

---

## Widgets & Graphiques

### TradingView Widgets (Embed Gratuit)
- **URL** : https://www.tradingview.com/widget/
- **Coût** : Gratuit avec branding TradingView
- **Widgets disponibles pour bullsagetrader.com** :
  - **Advanced Chart** — Graphique interactif complet avec indicateurs
  - **Ticker Tape** — Bandeau défilant avec prix temps réel
  - **Market Overview** — Vue macro des marchés
  - **Crypto Market** — Heatmap crypto
  - **Technical Analysis** — Widget d'analyse technique automatique
  - **Symbol Overview** — Mini-chart par actif
  - **Economic Calendar** — Calendrier économique intégrable
  - **Screener** — Scanner d'actions/crypto
  - **Heatmap** — Carte thermique par secteur/marché
- **Intégration** : Script embed simple (`<script>` + JSON config) — pas besoin d'API key
- **Doc** : https://www.tradingview.com/widget-docs/

---

## Sources de News & Sentiment

### Fear & Greed Index (Crypto)
- **URL** : https://alternative.me/crypto/fear-and-greed-index/
- **API** : `https://api.alternative.me/fng/`
- **Gratuit** : Oui, sans clé
- **Format** : JSON avec score 0-100 + classification

### VIX (Volatilité Indices)
- **Source** : Via Finnhub ou Yahoo Finance
- **Interprétation** :
  - < 12 : Complaisance extrême (attention au retournement)
  - 12-20 : Normal
  - 20-30 : Volatilité élevée (prudence)
  - > 30 : Panique (opportunités contrarian possibles)

### Calendrier Économique
- **Sources** : Finnhub API, TradingView Widget, Investing.com
- **Événements à impact élevé à surveiller** :
  - 🔴 FOMC (Fed) — 8x/an
  - 🔴 NFP (Non-Farm Payrolls) — mensuel, premier vendredi
  - 🔴 CPI (Inflation US) — mensuel
  - 🔴 BCE (Taux directeur) — ~8x/an
  - 🔴 BOJ (Banque du Japon) — ~8x/an
  - 🟡 PMI (Manufacturing & Services) — mensuel
  - 🟡 Retail Sales — mensuel
  - 🟡 Unemployment Claims — hebdomadaire

---

## Outils OpenClaw

### Commandes de diagnostic
```bash
openclaw doctor              # Diagnostic complet
openclaw doctor --fix        # Diagnostic + réparation auto
openclaw health              # État de santé du gateway
openclaw status              # Statut actuel
openclaw logs                # Journaux récents
openclaw --version           # Version installée
npm view openclaw version    # Dernière version publiée
```

### Commandes de gestion
```bash
openclaw gateway restart     # Redémarrer le gateway
openclaw update              # Mettre à jour OpenClaw
openclaw agent --message "..." --thinking high  # Tester l'agent
```

---

## Stack App bullsagetrader.com

### Frontend
- **Framework** : Next.js 14+ (App Router)
- **UI** : Tailwind CSS + shadcn/ui
- **Graphiques** : TradingView Widgets (embed) + Lightweight Charts (optionnel pour custom)
- **Temps réel** : WebSocket pour updates de prix

### Backend
- **API** : Next.js API Routes (serverless sur Vercel)
- **Moteur d'analyse** : Claude API (Opus 4.6) via Anthropic SDK
- **Cron jobs** : Vercel Cron pour les analyses planifiées

### Base de Données
- **Option 1** : Vercel Postgres (simple, intégré)
- **Option 2** : Supabase (si besoin real-time subscriptions + auth intégrée)
- **Tables principales** :
  - `signals` — Historique des signaux émis
  - `trades` — Suivi des trades (entrée, sortie, P&L)
  - `market_data` — Cache des données de marché
  - `alerts` — Alertes configurées par l'utilisateur
  - `watchlist` — Actifs surveillés
  - `daily_briefs` — Morning/Evening briefs archivés

### Déploiement
- **Plateforme** : Vercel
- **Domaine** : bullsagetrader.com
- **CI/CD** : Push to main → deploy automatique
