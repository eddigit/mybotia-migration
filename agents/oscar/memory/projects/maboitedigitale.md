# MaBoiteDigitale.com - Documentation Projet

**Date:** 2026-02-03
**Status:** En production

## Architecture

### Frontend
- **URL:** https://www.maboitedigitale.com
- **Hébergement:** Vercel
- **Projet Vercel:** maboitedigitale2026 (prj_whus4DYtWQWdHj0o7dxuj61yV189)
- **Framework:** Create React App
- **Repo GitHub:** eddigit/maboitedigitale

### Backend
- **URL API:** https://maboitedigitale-api.onrender.com
- **Hébergement:** Render
- **Framework:** FastAPI (Python)
- **Documentation API:** https://maboitedigitale-api.onrender.com/docs

### Base de données
- **Type:** MongoDB Atlas (probable)
- **À vérifier:** cluster, région, credentials

## Diagnostic 2026-02-03 23h15

### Ce qui fonctionne ✅
- Backend répond rapidement (~150ms) aux routes simples
- /docs accessible (FastAPI)
- Route /api/auth/login existe et valide les champs

### Problèmes identifiés ⚠️
- Certaines routes timeout (register, openapi.json)
- Gilles a du mal à se connecter → lenteur backend ?
- Pas de cron-job keep-alive configuré ?

### Actions à faire
1. Vérifier les logs Render
2. Créer compte Oscar (oscarcoachdigital@gmail.com / Test123456!)
3. Tester toute la plateforme
4. Configurer cron-job keep-alive si nécessaire
5. Diagnostiquer les routes lentes

## Intégration En Toute Franchise

MaBoiteDigitale est partenaire d'En Toute Franchise avec :
- Tarif adhérent : 17€/mois au lieu de 39€
- Code promo à configurer
- Lien vers https://maboitedigitale.com sur le site ETF

## Contacts & Accès

- **Compte Oscar à créer:** oscarcoachdigital@gmail.com
- **Dashboard Render:** https://dashboard.render.com
- **Dashboard Vercel:** https://vercel.com (gilleskorzec@gmail.com)
