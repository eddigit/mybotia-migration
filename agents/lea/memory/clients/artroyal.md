# Atelier Art Royal — Mémoire Client

## Contact
- **Client** : Tristan Llorca
- **Email** : tristan.llorca@gmail.com
- **Activité** : E-commerce d'articles maçonniques (tabliers, cordons, sautoirs, bijoux, gants)

## Architecture technique

### Site web
- **URL** : https://atelier-art-royal.vercel.app
- **Repo GitHub** : eddigit/atelier-art-royal
- **Vercel Project ID** : prj_W2XKPXuB5nbmFZFAXCQWQPr1Mn5V
- **Vercel Project v2** : prj_iEyUgLDAqrR6Bp3rx0sVbtAmad88 (atelier-art-royal-v2)
- **Framework** : React (Vite) + serverless functions Vercel

### Base de données
- **Provider** : Neon PostgreSQL (Francfort, aws-eu-central-1)
- **Project ID Neon** : divine-breeze-01570614
- **Connection string** : `postgresql://neondb_owner:npg_hFJcq56ngETQ@ep-royal-star-agnaqjie.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require`
- **Tables** : 20 (users, products, orders, categories, etc.)
- **Users** : 37 | **Produits** : 84
- **Migrée depuis** : PostgreSQL local VPS (container Docker) le 26/03/2026

### API Express (VPS)
- **URL** : https://api-artroyal.mybotia.com
- **Chemin VPS** : /home/gilles/artroyal-api/
- **Port** : 3100
- **Config** : /home/gilles/artroyal-api/.env

### Variables d'environnement Vercel
| Variable | Valeur |
|----------|--------|
| DATABASE_URL | (Neon connection string ci-dessus) |
| JWT_SECRET | artroyal-jwt-2026-secret |
| SUMUP_API_KEY | sup_sk_orNeUJe9Gh3hzZ9Md8K7kiOYoeP2ulvDg |
| SUMUP_MERCHANT_CODE | MDELMUGR |
| NEXT_PUBLIC_SITE_URL | https://atelier-art-royal.vercel.app |
| VITE_API_URL | https://api-artroyal.mybotia.com |

### Comptes admin
- gilleskorzec@gmail.com (admin)
- contact@artroyal.fr (admin)

### Cloudinary (images produits)
- **Cloud name** : dezvsjtz5
- **Compte Google** : oscarcoachdigital@gmail.com
- **Migration** : 88 images migrées de Base44 → Cloudinary le 26/03/2026

### Paiement
- SumUp : MDELMUGR

## Problèmes connus (26/03/2026)
- **Dashboard admin page blanche** : le front utilise les anciens IDs MongoDB (old_id) au lieu des UUIDs PostgreSQL → 500 sur /api/entities/Product avec filtre $in → erreur JS A.toFixed
- **Fix en cours** : Claude Code doit adapter le filtre pour chercher par old_id quand format MongoDB

## Historique
- 26/03/2026 : Migration DB vers Neon, config env vars Vercel, login fonctionnel, diagnostic bug admin
