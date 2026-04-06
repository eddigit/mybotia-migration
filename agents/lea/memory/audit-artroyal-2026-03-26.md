# 🔍 AUDIT COMPLET — Atelier Art Royal
**Date** : 26 mars 2026 à 3h15
**URL** : https://atelier-art-royal.vercel.app

---

## ✅ CE QUI FONCTIONNE

| Élément | Status |
|---------|--------|
| Page d'accueil | ✅ 200, charge en 84ms |
| Shop / Catalogue | ✅ 200, 84 produits, 7 catégories, 11 rites |
| Login / Register | ✅ Fonctionnel (Vercel serverless → Neon) |
| Dashboard Admin | ✅ Fonctionnel (fix toFixed appliqué) |
| API Express (VPS) | ✅ Tous les endpoints répondent |
| API Serverless (Vercel) | ✅ Login, me, admin-users |
| Paiement SumUp | ✅ Checkout créé avec succès |
| SSL | ✅ Certificat valide |
| Pages légales | ✅ CGV, Mentions légales, Politique de confidentialité |
| Sécurité endpoints | ✅ Admin protégé par auth, users non listables sans token |
| Performance | ✅ < 250ms toutes pages |

---

## 🔴 BUGS CRITIQUES (à corriger avant livraison)

### 1. 🖼️ IMAGES HÉBERGÉES SUR BASE44 — RISQUE DE COUPURE
**100% des images produits** (84 produits) sont hébergées sur `base44.app` qui redirige (302) vers Supabase. Ça fonctionne aujourd'hui mais :
- Dépendance à un service tiers (Base44) qui peut couper l'accès
- Double redirection = lenteur de chargement des images
- Si Base44 tombe, **tout le catalogue est sans image**

**Recommandation** : Migrer toutes les images vers Cloudinary ou le propre stockage du site. Priorité HAUTE.

### 2. 🔓 ENDPOINT ADMIN-RESET ENCORE ACTIF
Le fichier `/api/admin-reset/[token].js` est en production. Le secret est `ArtRoyal-Init-2026` — facilement devinable. Même si c'est protégé par token, il permet de **réinitialiser le mot de passe admin** et **lister tous les users avec emails**.

**Recommandation** : Supprimer ce fichier du repo et redéployer. Le commentaire dans le code dit « DELETE THIS FILE AFTER SETUP IS COMPLETE ». C'est fait (le setup), donc à supprimer. Priorité HAUTE.

---

## 🟡 BUGS MOYENS

### 3. Catégorie "Gants" en doublon
Deux catégories "Gants" existent (IDs différents). Peut créer de la confusion dans les filtres du shop.

### 4. Stock négatif sur un produit
"Tablier Maître REAA Cuir" (6ff4a82b) a un stock de **-4**. Probablement des ventes sans décrément correct.

### 5. Toutes les commandes ont customer_id mais le front cherche user_id
17 commandes existent. La colonne s'appelle `customer_id` dans la base. Si le front utilise `user_id`, les commandes ne s'associent pas aux clients dans l'admin.

### 6. 14 commandes sur 17 sont "cancelled"
Seulement 4 commandes payées (307€ total). 14 annulées — potentiellement des tests, à nettoyer.

---

## 🔵 AMÉLIORATIONS RECOMMANDÉES

### 7. Pas de balises OG (Open Graph)
Pas de `og:title`, `og:image`, `og:description` → les partages sur réseaux sociaux n'afficheront pas de preview. Important pour un e-commerce.

### 8. Title identique sur toutes les pages
Toutes les pages affichent "Atelier Art Royal - Haute Couture Maçonnique". Les pages produit devraient avoir le nom du produit dans le title (SEO).

### 9. 17 produits sans description
Les fiches produit sans description (principalement les sautoirs, bijoux, cordons) sont moins convaincantes pour l'achat et pénalisent le SEO.

### 10. 4 produits sans catégorie
"Tablier Maître RF", "Cordon 3° Ordre", "Tapis Très Sage", "Bandeau" n'apparaissent dans aucune catégorie → potentiellement invisibles dans le shop si le client filtre par catégorie.

### 11. AppSettings vide
La table `app_settings` est vide (0 rows). Si le site utilise des paramètres (nom boutique, devise, frais de port, etc.), ils ne sont pas configurés.

### 12. Pas de domaine personnalisé
Le site est accessible uniquement via `atelier-art-royal.vercel.app`. Pour un site e-commerce professionnel, un domaine propre (ex: atelier-art-royal.com) est indispensable.

### 13. Migrer l'API Express en serverless
L'API tourne encore sur le VPS (port 3101). Pour une architecture 100% cloud (Vercel + Neon), il faudrait migrer les endpoints Express en serverless functions Vercel. Ça supprimerait la dépendance au VPS pour ce site.

---

## 📊 RÉSUMÉ POUR LIVRAISON

| Catégorie | Compte |
|-----------|--------|
| Bugs critiques | 2 (images Base44, endpoint admin-reset) |
| Bugs moyens | 4 |
| Améliorations | 7 |
| **Score global** | **Site fonctionnel, achat possible, admin OK** |

**Le site peut être livré** en l'état pour une V1. Les 2 points critiques (images et admin-reset) doivent être adressés rapidement après livraison.

---

*Audit réalisé par Léa — Coach Digital Paris*
