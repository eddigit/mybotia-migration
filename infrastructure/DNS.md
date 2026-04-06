# Inventaire DNS — MyBotIA

**VPS IP :** 180.149.198.23
**SSL :** Wildcard Let's Encrypt (*.mybotia.com) via Cloudflare DNS-01
**Cert path :** /etc/letsencrypt/live/mybotia.com/

## Domaines pointant vers le VPS

### À migrer vers Emergent

| Domaine | Type | Destination actuelle | Notes |
|---------|------|---------------------|-------|
| mybotia.com | A | 180.149.198.23 | Site principal + webchat |
| *.mybotia.com | A/CNAME | 180.149.198.23 | Wildcard — sous-domaines agents |
| app.mybotia.com | A | 180.149.198.23 | Webchat (même que mybotia.com) |
| client.mybotia.com | A | 180.149.198.23 | Admin dashboard Express :3001 |
| admin.mybotia.com | A | 180.149.198.23 | Admin dashboard (alias) |
| lucy.mybotia.com | A | 180.149.198.23 | Webchat Lucy IGH (auth Basic) |
| voice.mybotia.com | A | 180.149.198.23 | Voice POC :3100 |
| collaboratoria.com | Redirect | → mybotia.com | Simple redirection DNS |
| collaborateur.com | Redirect | → mybotia.com | Simple redirection DNS |

### Restent sur le VPS

| Domaine | Type | Destination actuelle | Notes |
|---------|------|---------------------|-------|
| prospection.mybotia.com | A | 180.149.198.23 | Dashboard prospection Docker :3000 |
| listmonk.mybotia.com | A | 180.149.198.23 | Emailing Listmonk Docker :9000 |
| crm.mybotia.com | A | 180.149.198.23 | CRM Twenty Docker :3002 |
| files.mybotia.com | A | 180.149.198.23 | File server (Nginx) |
| api-artroyal.mybotia.com | A | 180.149.198.23 | API ArtRoyal |
| app.bullsagetrader.com | A | 180.149.198.23 | Bullsage Trader |
| clementdelpiano.com | A | 180.149.198.23 | Site client (ISPConfig) |
| support.coachdigitalparis.com | A | 180.149.198.23 | MeshCentral |

### Domaines mail

| Domaine | Usage |
|---------|-------|
| collaborateur.ia.pro | Emails agents (Migadu) — format prenom.entreprise@collaborateur.pro |

## Registrar

**À vérifier par Gilles :**
- mybotia.com → registrar ? (OVH / Gandi / Cloudflare ?)
- collaboratoria.com → registrar ?
- collaborateur.com → registrar ?
- Les DNS sont gérés via Cloudflare (cf. certbot DNS-01)

## Actions post-migration

1. Re-pointer mybotia.com et *.mybotia.com vers l'infrastructure Emergent
2. Configurer les redirections collaboratoria.com et collaborateur.com vers le nouveau domaine
3. Mettre à jour les records MX si nécessaire (Migadu)
4. Les domaines restant sur le VPS ne changent pas
