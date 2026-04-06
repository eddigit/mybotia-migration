# PROCÉDURE — Envoyer un message dans un groupe WhatsApp

## ⚠️ PROBLÈME RÉCURRENT
Léa n'arrive JAMAIS à envoyer dans un groupe WhatsApp depuis une session directe.
Ce problème a frustré Gilles de NOMBREUSES fois. NE PLUS JAMAIS échouer sur ce sujet.

## SOLUTION QUI MARCHE
Utiliser `sessions_send` (outil natif du runtime OpenClaw) avec la clé de session du groupe.

Format de la clé : `agent:main:whatsapp:group:JID_DU_GROUPE`

Exemple : `agent:main:whatsapp:group:120363406115931873@g.us`

## ANNUAIRE DES GROUPES (JID)
Voir : /home/gilles/.openclaw/workspace/memory/whatsapp-groups-directory.md

## SI sessions_send NE MARCHE PAS
1. NE PAS perdre 20 minutes à essayer des trucs
2. Dire IMMÉDIATEMENT à Gilles : "Je n'arrive pas à envoyer, voici le message formaté à copier-coller"
3. Fournir le message prêt à copier

## RÈGLE ABSOLUE
- NE JAMAIS dire "c'est envoyé" sans PREUVE que c'est passé
- NE JAMAIS faire croire que ça a marché si on n'est pas sûr
- Si ça ne marche pas → le dire TOUT DE SUITE, pas après 5 tentatives ratées
