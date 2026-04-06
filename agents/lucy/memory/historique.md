# Historique Lucy

- **22 mars** : Lucy créée et déployée
- **23 mars** : JID groupe corrigé, bienvenue envoyée, email relance Cozon
- **24 mars** : Briefing métier, cartographie établissements, directives définies
- **25 mars** : RDV terrain Gilles chez IGH Aix (14h) — retours en attente
- **26 mars** : Documents reçus de Cozon (contrat séjour, avenant, règlement)
- **27 mars** : 13 directeurs identifiés, données SIREN 20 entités, famille Imbert 7 membres, FINESS + tarifs CNSA collectés
- **28 mars** : Briefing envoyé, adresses complètes 20 étab., téléphones FINESS, SIREN La Chênaie/Jauberte, Roc Pointu fermé 31/12/2021, veille sectorielle intégrée
- **29 mars** : Briefing envoyé ✅ (9h22). Sites web 20 étab. cartographiés. Deadline CA/ERRD 30 avril identifiée. 5 directeurs toujours non identifiés.
- **30 mars** : WhatsApp Lucy inactif toute la journée (listener down). Briefing 30 mars non envoyé. ×6 tentatives heartbeat échouées.
- **31 mars** : Gateway token mismatch persistant. Briefings 30 et 31 mars non envoyés. Veille sectorielle compilée (voir veille-sectorielle.md). Sources web partiellement inaccessibles (captchas nocturnes).
- **1er avril** : Briefing 1er avril préparé — envoi WhatsApp impossible (gateway token mismatch persistant). Veille silencieuse effectuée (21h Paris) : Mme Lebatteux (Dir. Qualité siège), Agnès Robic (Directrice IGH zone Lyon), note HAS 3,95/4 EHPAD Jardins de la Vire, tarif différencié 35% plafond depuis jan.2025, 1700 lits total groupe confirmé. Veille-sectorielle.md et directeurs-igh.md mis à jour.
- **2 avril** : Gilles contacté à 4h05 (vérification disponibilité ✅). Token mismatch résolu à 10h17 Paris (sync ~/.openclaw-lucy/.openclaw/openclaw.json ↔ ~/.openclaw-lucy/openclaw.json). Briefing matinal envoyé dans groupe IGH ✅ (10h17 Paris). doctor --fix appliqué. Deadline CA/ERRD 30 avril : 28 jours restants.

## Problèmes techniques récurrents
- **WhatsApp Lucy : non liée** — session WhatsApp Web inactive. Commande pour relancer : `openclaw --profile lucy channels login` (scan QR sur le serveur gateway). Briefings non envoyés depuis le 30 mars.
- **Config doctor** : `openclaw --profile lucy doctor --fix` à lancer pour migrer la config (allowlist DM/groupes vide → messages bloqués). GroupPolicy WhatsApp à vérifier pour groupe IGH.
- **Sources web** : DuckDuckGo, Bing, SeniorActu bloquent les requêtes automatiques (surtout la nuit)
- **Sites Rhinoferos** : JS dynamique → scraping impossible pour identifier directeurs manquants
