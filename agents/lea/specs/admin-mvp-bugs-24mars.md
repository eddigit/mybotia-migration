# BRIEF CLAUDE CODE — Bugs Admin MVP (24 mars 2026)

**Projet** : `/home/gilles/apps/admin/`
**Stack** : Node.js Express + PostgreSQL + Vanilla JS frontend
**Priorité** : Haute — Gilles utilise l'admin au quotidien, ces bugs le bloquent

---

## BUG 1 — Suppression clients inactifs impossible 🔴

**Fichier** : `public/js/crm.js` ligne 561 + `routes/crm.js` ou `routes/agent-api.js`

**Symptôme** : Quand on clique "Archiver" sur un client inactif, rien ne se passe (ou erreur silencieuse). Il y a 19 clients inactifs impossibles à supprimer.

**Code actuel** (crm.js:561) :
```js
async function deleteCrmClient(clientId) {
  if (!confirm('Archiver ce client dans Notion ?')) return;
  const res = await api('/api/crm/clients/' + clientId, { method: 'DELETE' });
```

**À corriger** :
1. Vérifier que l'endpoint `DELETE /api/crm/clients/:id` fonctionne réellement (tester en curl)
2. Si le problème est côté Notion sync (le client est dans Notion et la suppression échoue), permettre la suppression locale PostgreSQL même si Notion échoue
3. Ajouter un vrai feedback d'erreur visible si la suppression échoue (pas d'erreur silencieuse)
4. Renommer "Archiver" en "Supprimer" avec une vraie suppression (pas juste un changement de statut), OU ajouter un bouton "Supprimer définitivement" en plus de "Archiver"

---

## BUG 2 — Pipeline : calculs mélangent one-shot et récurrent 🔴

**Fichier** : `public/js/pipeline.js` (renderPipelineContent) + `services/notion-crm.js` (getPipelineStats)

**Symptôme** : Le KPI "CA gagné" affiche 135 582€ en mélangeant :
- Les montants one-shot (ex: 13 942€ IGH mise en place)
- Les montants récurrents ANNUALISÉS (ex: 980€/mois × 12 = 11 760€)

C'est **trompeur** : on ne peut pas additionner un one-shot déjà encaissable avec une projection annuelle de récurrent.

**Calcul actuel** (pipeline.js) :
```js
const total = (a.montantOneshot || 0) + (a.montantRecurrent || 0) * 12;
```

**À corriger** :
1. **Séparer les KPIs du pipeline en 3 lignes claires** :
   - `CA One-shot signé` = somme des `montantOneshot` des affaires Gagnées
   - `MRR signé` = somme des `montantRecurrent` des affaires Gagnées (mensuel)
   - `ARR` = MRR × 12 (affiché séparément, clairement étiqueté "projection annuelle")
2. La "Valeur totale" peut rester comme total global mais doit indiquer clairement que c'est une projection
3. Même logique pour "Valeur pondérée" — séparer one-shot pondéré et récurrent pondéré
4. Dans les cartes affaires, afficher les deux montants séparément :
   - One-shot : X€
   - Récurrent : X€/mois

**Côté backend** (`services/notion-crm.js` → `getPipelineStats`) :
Ajouter dans les stats retournées :
```js
stats.caOneshotGagne = affaires.filter(a => a.phase === 'Gagné').reduce((s, a) => s + (a.montantOneshot || 0), 0);
stats.mrrGagne = affaires.filter(a => a.phase === 'Gagné').reduce((s, a) => s + (a.montantRecurrent || 0), 0);
stats.arrGagne = stats.mrrGagne * 12;
```

---

## BUG 3 — Pipeline : pas de filtre par phase 🟡

**Fichier** : `public/js/pipeline.js` (renderPipelineContent)

**Symptôme** : On ne peut pas filtrer pour ne voir QUE les affaires en cours (Lead → Négociation) en excluant les Gagnées. Quand on a 18 affaires dont 7 gagnées, c'est illisible.

**À ajouter** :
1. Toolbar avec boutons filtres par phase : `Tous | En cours | Gagnés | Perdus`
   - "En cours" = Lead + Qualifié + Proposition + Négociation + Production
   - "Gagnés" = Gagné uniquement
   - "Perdus" = Perdu uniquement
2. Garder le filtre en state (`STATE.pipeline.filter`)
3. Les KPIs doivent toujours montrer les totaux globaux (pas filtrés)

---

## BUG 4 — Sync protocoles WhatsApp ne ramène pas les nouveaux groupes 🔴

**Fichiers** : `routes/whatsapp-protocols.js` + `services/whatsapp-protocols.js`

**Symptôme** : 2 groupes WhatsApp créés hier n'apparaissent pas dans la page Protocoles WA, même après "Forcer la synchronisation".

**À investiguer** :
1. Vérifier que `listProtocols()` lit bien la table `whatsapp_protocols` en PostgreSQL
2. Vérifier que le bouton "Sync" appelle bien un endpoint qui scanne les groupes actifs du gateway et les ajoute s'ils sont nouveaux (pas juste une relecture de la DB)
3. Si la sync ne fait que relire la DB → ajouter une vraie détection : appeler le gateway pour lister les groupes WhatsApp actifs, comparer avec la DB, créer les entrées manquantes
4. Alternative simple : permettre l'ajout manuel d'un protocole avec un champ JID libre

**Endpoint gateway pour lister les groupes** (si disponible) :
```bash
# Vérifier si un endpoint existe pour lister les groupes WhatsApp
grep -r "groups\|chats\|conversations" /home/gilles/apps/admin/services/whatsapp-protocols.js
```

---

## AMÉLIORATION 5 — Bouton "Supprimer définitivement" pour les clients 🟡

**Contexte** : Il y a 19 clients inactifs qui polluent la base. Gilles veut pouvoir les supprimer.

**À ajouter** :
- Dans la fiche client (vue détail), si le statut est "Inactif" :
  - Bouton rouge "Supprimer définitivement" avec double confirmation
  - Supprime de PostgreSQL ET de Notion (si notionId existe)
  - Si Notion échoue → supprimer quand même en local avec un warning

---

## Fichiers à modifier (résumé)

| Fichier | Bugs |
|---------|------|
| `public/js/pipeline.js` | #2 (KPIs séparés), #3 (filtres phase) |
| `public/js/crm.js` | #1 (suppression), #5 (bouton supprimer) |
| `services/notion-crm.js` | #2 (stats backend séparées one-shot/récurrent) |
| `routes/crm.js` | #1 (endpoint DELETE) |
| `services/whatsapp-protocols.js` | #4 (sync groupes) |
| `routes/whatsapp-protocols.js` | #4 (endpoint sync) |

---

## Test après corrections

1. **Suppression client** : filtrer Inactifs → supprimer un client → vérifier qu'il disparaît
2. **Pipeline KPIs** : vérifier que CA one-shot, MRR et ARR sont affichés séparément
3. **Pipeline filtres** : cliquer "En cours" → seules les affaires Lead/Qualifié/Proposition/Négo/Production s'affichent
4. **Sync WA** : cliquer Sync → les nouveaux groupes apparaissent
5. Vérifier que rien n'est cassé sur les autres pages (dashboard, tâches, etc.)
