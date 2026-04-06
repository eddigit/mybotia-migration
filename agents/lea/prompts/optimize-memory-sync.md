# PROMPT CLAUDE CODE — Optimisation Mémoire & Synchro WhatsApp/Webchat

## Contexte

On utilise OpenClaw (gateway WhatsApp + Webchat) avec un agent principal (Léa) qui gère plusieurs clients via :
- Des **groupes WhatsApp** (chaque client a son groupe)
- Des **DM WhatsApp** (conversations directes)
- Du **Webchat** (interface mybotia.com)

**Problème actuel :**
- Un seul fichier `MEMORY.md` fourre-tout qui grossit, se fait tronquer, et perd du contexte
- Pas de synchro entre les canaux : si on parle d'un client en webchat, le contexte WhatsApp n'est pas chargé
- Les notes quotidiennes (`memory/YYYY-MM-DD.md`) sont des logs bruts sans structure
- Quand un message arrive d'un groupe WhatsApp, l'agent n'a pas automatiquement le contexte complet du client

## Objectif

Créer un **système de mémoire par client/contexte** qui :

1. **Découpe MEMORY.md** en fichiers par client/sujet :
   ```
   memory/clients/igh.md          — Tout sur IGH (Imbert, Cozon, Florence)
   memory/clients/hannah.md       — Tout sur Hannah/Paypers
   memory/clients/byron.md        — Tout sur Byron/Pascal
   memory/clients/herve.md        — Tout sur Hervé Boussaid
   memory/clients/clarisse.md     — Tout sur Clarisse Surin / Bâtonnat
   memory/general.md              — Notes générales (identité légale, règles, etc.)
   ```

2. **Crée un mapping JID → fichier mémoire** :
   ```json
   // memory/channel-mapping.json
   {
     "120363407026699197@g.us": { "client": "igh", "memory": "memory/clients/igh.md", "label": "IGH - EHPAD" },
     "120363405038000558@g.us": { "client": "rachel", "memory": "memory/clients/rachel.md", "label": "Cannes Rachel" },
     "120363408599518725@g.us": { "client": "byron", "memory": "memory/clients/byron.md", "label": "Com BYRON" },
     "120363424295220178@g.us": { "client": "herve", "memory": "memory/clients/herve.md", "label": "Assistante Hervé" },
     "120363425376786580@g.us": { "client": "clarisse", "memory": "memory/clients/clarisse.md", "label": "Bâtonnat 2028" }
   }
   ```

3. **Modifie AGENTS.md** pour que à chaque session :
   - L'agent lise `memory/channel-mapping.json`
   - Identifie le JID/contexte du message entrant
   - Charge le fichier mémoire client correspondant
   - Si webchat : charge le dernier contexte actif ou demande le sujet

4. **Crée un script de migration** qui :
   - Parse le MEMORY.md actuel
   - Extrait les blocs par client (regex sur les ### HEADERS)
   - Les répartit dans les fichiers individuels
   - Conserve `memory/general.md` pour ce qui n'est lié à aucun client
   - Garde une copie backup de l'ancien MEMORY.md

5. **Crée un hook/instruction dans AGENTS.md** (section "Every Session") :
   ```markdown
   ## Chargement contexte
   
   1. Lire memory/channel-mapping.json
   2. Identifier le chat_id du message entrant (metadata inbound)
   3. Si JID trouvé dans le mapping → lire le fichier mémoire correspondant
   4. Sinon → lire memory/general.md + les 2 dernières daily notes
   5. Toujours lire MEMORY-CORE.md (règles transversales, identité légale, procédures)
   ```

6. **MEMORY-CORE.md** — un fichier léger (~2KB max) avec UNIQUEMENT :
   - Identité légale (SIRET, adresse, IBAN)
   - Règles d'or transversales
   - Liste des clients actifs (nom + JID + statut en 1 ligne chacun)
   - Pas de détails — les détails sont dans memory/clients/xxx.md

## Architecture cible

```
workspace/
├── MEMORY-CORE.md                    # Essentiel transversal (2KB max)
├── memory/
│   ├── channel-mapping.json          # JID → client → fichier mémoire
│   ├── general.md                    # Notes non liées à un client
│   ├── clients/
│   │   ├── igh.md                    # Mémoire complète IGH
│   │   ├── hannah.md                 # Mémoire complète Hannah/Paypers
│   │   ├── byron.md                  # Mémoire complète Byron/Pascal
│   │   ├── herve.md                  # Mémoire complète Hervé
│   │   ├── clarisse.md               # Mémoire complète Clarisse/Bâtonnat
│   │   ├── rachel.md                 # Mémoire complète Rachel
│   │   ├── martine.md                # Mémoire complète Martine
│   │   └── emrise.md                 # Mémoire complète Emrise/Hugo
│   └── YYYY-MM-DD.md                 # Daily notes (logs bruts, inchangés)
```

## Contraintes

- **Workspace** : `/home/gilles/.openclaw/workspace/`
- **Ne PAS toucher** : openclaw.json, les configs gateway, les scripts tools/
- **Backup** : copier MEMORY.md → memory/MEMORY-backup-YYYYMMDD.md avant migration
- **Tester** : après migration, vérifier que chaque fichier client contient bien ses données
- **AGENTS.md** : mettre à jour la section "Every Session" avec la nouvelle logique de chargement

## Fichiers à lire pour comprendre le contexte

- `MEMORY.md` — mémoire actuelle à découper
- `AGENTS.md` — règles de fonctionnement actuelles
- `memory/whatsapp-groups-directory.md` — répertoire des groupes WhatsApp (si existe)
- `procedures/onboarding-groupe-whatsapp.md` — procédure groupes (si existe)

## Livrable attendu

1. Script Python `scripts/migrate-memory.py` qui fait la migration automatiquement
2. `memory/channel-mapping.json` peuplé avec tous les groupes connus
3. Fichiers `memory/clients/*.md` créés et remplis
4. `MEMORY-CORE.md` créé (version allégée)
5. `AGENTS.md` mis à jour (section Every Session)
6. Ancien `MEMORY.md` sauvegardé en backup
7. Rapport de migration (ce qui a été déplacé où)
