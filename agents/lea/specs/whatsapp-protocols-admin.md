# SPEC — Gestion des Protocoles Groupes WhatsApp dans l'Admin

**Date** : 23 mars 2026
**Demandeur** : Gilles
**Rédigé par** : Léa
**Destinataire** : Jules (dev)
**Priorité** : Haute — impact direct sur la qualité des réponses WhatsApp

---

## 1. Contexte & Problème

Aujourd'hui, quand Gilles crée un groupe WhatsApp avec un client ou un prospect, les règles de comportement de l'IA dans ce groupe (est-ce qu'elle répond ? sur quel ton ? est-ce qu'elle parle de tarifs ?) sont notées en vrac dans des fichiers mémoire. Résultat :

- Certains groupes : l'IA ne répond plus alors qu'elle devrait
- Certains groupes : l'IA répond trop ou parle de tarifs alors que c'est interdit
- Aucun endroit centralisé pour voir/modifier les règles par groupe
- Gilles ne retrouve jamais le JID d'un groupe quand il en a besoin

**Objectif** : une page dans l'admin (`admin.mybotia.com`) où Gilles peut configurer le comportement de l'IA pour chaque groupe WhatsApp, et que cette config soit automatiquement écrite dans un fichier que l'IA lit à chaque message.

---

## 2. Flux cible

```
Gilles ouvre l'admin
    → Page "Protocoles WhatsApp"
    → Voit tous les groupes avec leur config
    → Modifie un groupe (profil, ton, directives…)
    → Clique "Sauvegarder"
    → L'API écrit en base PostgreSQL
    → L'API génère automatiquement le fichier WHATSAPP-PROTOCOLS.md
    → L'IA lit ce fichier à chaque message WhatsApp entrant
```

---

## 3. Base de données

### Nouvelle table : `whatsapp_protocols`

| Colonne | Type | Obligatoire | Description |
|---------|------|-------------|-------------|
| `id` | serial PK | oui | ID auto |
| `group_name` | text | oui | Nom lisible du groupe |
| `jid` | text UNIQUE | oui | Identifiant WhatsApp (ex: `120363425376786580@g.us`) |
| `profile` | text | oui | Profil type : `CLIENT`, `DEMO`, `PERSO`, `INTERNE` |
| `reactivity` | text | oui | `TOUJOURS`, `SUR_DEMANDE`, `SILENCIEUX` |
| `tone` | text | non | Ex: "Pro formel", "Pro décontracté", "Amical" |
| `pricing_talk` | text | oui | `INTERDIT`, `SUR_DEMANDE`, `LIBRE` |
| `role` | text | non | Rôle de l'IA dans ce groupe (ex: "Assistante projet") |
| `directives` | text | non | Instructions spécifiques en texte libre |
| `active` | boolean | oui | Groupe actif ou archivé (défaut: true) |
| `client_id` | integer FK → clients(id) | non | Lien vers la table clients existante |
| `projet_id` | integer FK → projets(id) | non | Lien vers le projet associé |
| `gateway_id` | text | non | ID de la gateway concernée (défaut: "mybotia") |
| `created_at` | timestamptz | oui | Date de création (défaut: now()) |
| `updated_at` | timestamptz | oui | Mis à jour automatiquement via trigger |

### Valeurs possibles

**profile** :
| Valeur | Signification |
|--------|---------------|
| `CLIENT` | Client signé, en production. L'IA est active et professionnelle. |
| `DEMO` | Prospect en test. L'IA montre sa valeur, ne livre pas de travail gratuit. |
| `PERSO` | Amis, famille, réseau personnel. |
| `INTERNE` | Équipe Coach Digital. Communication directe et libre. |

**reactivity** :
| Valeur | Signification |
|--------|---------------|
| `TOUJOURS` | L'IA répond à chaque message qui la concerne ou qui pose une question. |
| `SUR_DEMANDE` | L'IA ne répond QUE si on l'interpelle explicitement (mention de son nom, question directe). |
| `SILENCIEUX` | L'IA ne répond JAMAIS sauf sur instruction directe de Gilles dans le webchat. |

**pricing_talk** :
| Valeur | Signification |
|--------|---------------|
| `INTERDIT` | Ne JAMAIS parler de prix, tarifs, budget. Renvoyer vers Gilles. |
| `SUR_DEMANDE` | Peut donner des infos tarifaires SI le client demande explicitement. |
| `LIBRE` | Peut aborder les tarifs librement (groupes internes uniquement). |

### Profils par défaut

Quand Gilles sélectionne un profil, les champs se pré-remplissent automatiquement (modifiables ensuite) :

| Profil | Réactivité | Ton | Tarifs | Rôle par défaut |
|--------|-----------|-----|--------|-----------------|
| `CLIENT` | TOUJOURS | Pro formel | INTERDIT | Assistante projet |
| `DEMO` | TOUJOURS | Pro décontracté | INTERDIT | Démonstration IA |
| `PERSO` | SUR_DEMANDE | Amical | INTERDIT | Aide ponctuelle |
| `INTERNE` | TOUJOURS | Direct | LIBRE | Équipe interne |

---

## 4. API — Endpoints

Tous sous `/whatsapp/protocols`, protégés par l'auth admin existante.

### GET `/whatsapp/protocols`
- Retourne tous les protocoles (actifs par défaut, `?all=true` pour inclure archivés)
- Joindre le nom du client depuis la table `clients` si `client_id` est rempli
- Trier par `group_name`

### GET `/whatsapp/protocols/:id`
- Retourne un protocole par son ID

### POST `/whatsapp/protocols`
- Crée un nouveau protocole
- Body : tous les champs sauf `id`, `created_at`, `updated_at`
- **Après insertion** : déclencher la régénération du fichier MD (voir section 6)

### PUT `/whatsapp/protocols/:id`
- Met à jour un protocole existant
- **Après update** : déclencher la régénération du fichier MD

### DELETE `/whatsapp/protocols/:id`
- Supprime (ou archive — mettre `active = false` plutôt que DELETE)
- **Après archivage** : déclencher la régénération du fichier MD

### POST `/whatsapp/protocols/sync-md`
- Force la régénération du fichier MD manuellement (bouton "Forcer la sync" dans l'admin)

---

## 5. Interface Admin — Page "Protocoles WhatsApp"

### Accès
- Nouvelle entrée dans le menu latéral : **"📋 Protocoles WhatsApp"**
- Accessible uniquement aux admins (pas aux operators type Hugo/Nina)

### Vue tableau principal
Un tableau avec colonnes :

| Groupe | JID | Profil | Réactivité | Ton | Tarifs | Client lié | Projet | Statut |
|--------|-----|--------|-----------|-----|--------|------------|--------|

- Le **JID** doit avoir un bouton "copier" (icône clipboard) → copie dans le presse-papier en 1 clic
- **Profil** affiché en badge coloré (CLIENT = bleu, DEMO = orange, PERSO = gris, INTERNE = vert)
- **Réactivité** en badge (TOUJOURS = vert, SUR_DEMANDE = jaune, SILENCIEUX = rouge)
- **Statut** : toggle actif/archivé

### Formulaire d'édition (modale ou page)
Quand on clique sur un groupe ou "Ajouter" :

1. **Nom du groupe** — champ texte
2. **JID** — champ texte (format validé : doit finir par `@g.us`)
3. **Profil** — dropdown (CLIENT / DEMO / PERSO / INTERNE) → pré-remplit les champs suivants
4. **Réactivité** — dropdown (TOUJOURS / SUR_DEMANDE / SILENCIEUX)
5. **Ton** — champ texte libre (pré-rempli selon profil)
6. **Tarifs** — dropdown (INTERDIT / SUR_DEMANDE / LIBRE)
7. **Rôle de l'IA** — champ texte libre
8. **Directives spécifiques** — textarea (instructions particulières pour ce groupe)
9. **Client lié** — dropdown recherchable parmi les clients existants en base (optionnel)
10. **Projet lié** — dropdown filtré automatiquement sur les projets du client sélectionné. Si aucun client sélectionné → dropdown vide/désactivé. Si client sélectionné mais aucun projet → afficher "(aucun projet)" 
11. **Gateway** — dropdown des gateways disponibles (défaut: mybotia)

### Bouton "Sauvegarder"
- Écrit en base PostgreSQL
- Régénère le fichier MD
- Affiche un toast de confirmation : "✅ Protocole mis à jour — fichier IA synchronisé"

### Import initial
- Un bouton "Importer les groupes existants" qui lit les groupes déjà en base (table `clients` avec `jid_whatsapp` rempli) et crée les protocoles correspondants avec le profil par défaut `DEMO`
- Cela permet de pré-remplir la page au premier lancement sans tout ressaisir

---

## 6. Génération du fichier WHATSAPP-PROTOCOLS.md

### Chemin de destination
```
/home/gilles/.openclaw/workspace/WHATSAPP-PROTOCOLS.md
```

### Déclenchement
Automatique à chaque CREATE / UPDATE / DELETE sur la table `whatsapp_protocols`.

### Format du fichier généré

Le fichier doit suivre **exactement** ce format (c'est ce que l'IA parse) :

```markdown
# WHATSAPP-PROTOCOLS — Règles de comportement par groupe
# Généré automatiquement par l'admin MyBotIA — Ne pas modifier manuellement
# Dernière mise à jour : [DATE ISO]

---

## Profils de référence

| Profil | Réactivité par défaut | Ton | Tarifs | Description |
|--------|----------------------|-----|--------|-------------|
| CLIENT | TOUJOURS | Pro formel | INTERDIT | Client signé, en production |
| DEMO | TOUJOURS | Pro décontracté | INTERDIT | Prospect en test, montrer la valeur |
| PERSO | SUR_DEMANDE | Amical | INTERDIT | Amis, famille, réseau |
| INTERNE | TOUJOURS | Direct | LIBRE | Équipe Coach Digital |

### Légende réactivité
- **TOUJOURS** : Répondre à chaque message pertinent
- **SUR_DEMANDE** : Répondre uniquement si interpellée (nom cité, question directe)
- **SILENCIEUX** : Ne jamais répondre sauf instruction de Gilles via webchat

### Légende tarifs
- **INTERDIT** : Ne JAMAIS parler de prix/tarifs → renvoyer vers Gilles
- **SUR_DEMANDE** : Donner des infos tarifaires uniquement si demandé explicitement
- **LIBRE** : Peut aborder les tarifs librement

---

## Groupes actifs

### [NOM DU GROUPE]
- **JID** : [JID]
- **Profil** : [PROFIL]
- **Réactivité** : [REACTIVITE]
- **Ton** : [TON]
- **Tarifs** : [PRICING]
- **Rôle** : [ROLE]
- **Directives** : [DIRECTIVES ou "Aucune directive spécifique"]

---

(répéter pour chaque groupe actif)

---

## Groupes archivés

### [NOM]
- **JID** : [JID]
- **Statut** : ARCHIVÉ — ne plus répondre

---

## Règle par défaut (groupe non répertorié)

Si un message arrive d'un groupe qui n'est PAS dans cette liste :
- **Profil** : DEMO
- **Réactivité** : SUR_DEMANDE
- **Ton** : Pro décontracté
- **Tarifs** : INTERDIT
- **Rôle** : Assistante en mode découverte
- **Action** : Signaler à Gilles qu'un nouveau groupe non configuré a été détecté
```

---

## 7. Synchronisation et fiabilité

### Le problème à éviter
Gilles a constaté que les mises à jour OpenClaw dans l'admin ne reflétaient pas l'état réel du serveur. Il ne faut PAS reproduire ce problème.

### Garanties à implémenter

1. **Source de vérité = PostgreSQL** — le fichier MD est un export, pas la source
2. **Écriture atomique du fichier** — écrire dans un `.tmp` puis renommer (éviter les fichiers corrompus si crash)
3. **Vérification après écriture** — après avoir écrit le MD, relire et comparer le nombre de groupes avec ce qui est en base. Si ça ne correspond pas → logger une erreur
4. **Timestamp dans le fichier** — la première ligne contient la date de dernière génération. L'IA peut vérifier que le fichier est récent
5. **Bouton "Forcer la sync"** dans l'admin — pour régénérer manuellement si besoin
6. **Indicateur de santé** — dans la page admin, afficher :
   - "✅ Fichier synchronisé — dernière génération : [date]"
   - "⚠️ Fichier désynchronisé — [N] groupes en base vs [M] dans le fichier"

---

## 8. Notification à l'IA après mise à jour

### Le problème
Le fichier MD est généré, mais l'IA ne sait pas qu'il a changé. Elle peut continuer à travailler avec une version en cache ou un ancien contexte pendant toute la session.

### Solution : endpoint de notification + bouton admin

**Côté API** : ajouter un endpoint `POST /whatsapp/protocols/notify-agent`

Cet endpoint doit :
1. Envoyer un message dans la session webchat de l'IA via la gateway OpenClaw (même mécanisme que `openclaw gateway call send` mais sur le canal webchat/interne)
2. Le message envoyé sera :
```
🔄 MISE À JOUR PROTOCOLES WHATSAPP — [DATE]
Les protocoles ont été modifiés dans l'admin. Groupes modifiés : [LISTE DES NOMS].
Relis WHATSAPP-PROTOCOLS.md maintenant.
```

**Côté admin** : 
- Le bouton "Sauvegarder" dans la page protocoles fait **3 choses** dans l'ordre :
  1. Écriture en base PostgreSQL
  2. Régénération du fichier MD
  3. Notification à l'IA (appel à `/whatsapp/protocols/notify-agent`)
- Afficher un toast : "✅ Sauvegardé + IA notifiée"

**Côté bouton dédié** :
- Un bouton visible "🔄 Notifier l'IA" dans la barre d'actions de la page
- Permet de forcer la notification sans modifier de données (si Gilles veut juste s'assurer que l'IA a bien la dernière version)

### Mécanisme technique de notification

Option la plus simple et fiable : écrire un petit fichier flag que l'IA vérifie.

```
/home/gilles/.openclaw/workspace/.protocols-updated
```

Contenu du fichier :
```json
{
  "updated_at": "2026-03-23T15:01:00Z",
  "groups_changed": ["Bâtonnat 2028", "Hannah"],
  "action": "update"
}
```

Ce fichier est écrit à chaque sauvegarde. L'IA, quand elle reçoit un message WhatsApp, vérifie ce flag ET relit le fichier MD.

Mais **en plus**, le message webchat est envoyé pour que l'IA soit informée immédiatement même si aucun message WhatsApp n'arrive.

---

## 9. Migration des données existantes

À l'installation, importer les groupes déjà connus depuis :

1. **Table `clients`** — tous les enregistrements avec `jid_whatsapp` non null
2. **Fichier `whatsapp-groups-directory.md`** — les groupes qui ne sont pas en base clients

Pour chaque groupe importé :
- Profil par défaut = `DEMO`
- Réactivité = `SUR_DEMANDE`
- Tarifs = `INTERDIT`
- Directives = vide

Gilles passera ensuite dans l'admin pour configurer chaque groupe correctement.

---

## 9. Données initiales à insérer

Voici les groupes connus à ce jour avec le JID. Gilles configurera les protocoles après via l'admin.

| Groupe | JID | Client lié en base |
|--------|-----|--------------------|
| IGH — Livraisons | `120363407026699197@g.us` | Me Clarisse Surin (Livraisons) #37 |
| Hannah — Paypers | `120363425162106700@g.us` | Hannah (Personnel) #34 |
| Com BYRON | `120363408599518725@g.us` | BYRON - Pascal #43 |
| Assistante Hervé | `120363424295220178@g.us` | — (à créer) |
| Bâtonnat 2028 | `120363425376786580@g.us` | — (à créer) |
| Clarisse Surin | `120363426451963719@g.us` | Me Clarisse Surin #35 |
| Cannes Rachel | `120363405038000558@g.us` | — (à créer) |
| ETF — Martine | `120363426071294259@g.us` | ETF (Association) #39 |
| Assistante Jean-Luc | `120363406232810102@g.us` | Assistante Jean-Luc (VL Medical) #40 |
| Ness ma femme | `120363424470242785@g.us` | Ness (Personnel) #38 |
| Académie Levinet | `120363425931772536@g.us` | Académie LEVINET #36 |
| Clément Delpiano | `120363424693375693@g.us` | Clément Delpiano #33 |
| Soutien Xavier | `120363406115931873@g.us` | — |
| Soutien Clemsen | `120363406481118458@g.us` | — |
| Maggia Coiffure | `120363424038612397@g.us` | — |
| Me Gilles Tobiana | `120363407336999165@g.us` | Maître Gilles Tobiana #42 |
| Le Latin — Aymen | `120363407466857521@g.us` | Le Latin - Aymen Jelassi #45 |

---

## 10. Résumé des livrables

1. ☐ Migration SQL — table `whatsapp_protocols` + trigger `updated_at`
2. ☐ Endpoints API — CRUD + sync-md
3. ☐ Service de génération du fichier MD — appelé après chaque écriture
4. ☐ Page admin — tableau + formulaire d'édition + bouton copier JID
5. ☐ Import initial — script qui pré-remplit depuis les données existantes
6. ☐ Indicateur de santé — vérification sync base ↔ fichier
7. ☐ Tests — vérifier que le fichier MD est bien généré et lisible

---

*Spec rédigée par Léa — 23 mars 2026*
*À valider par Gilles avant dev*
