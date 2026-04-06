# EMRISE — Client Hugo (MàJ 21 mars 2026)

## Infos projet
- **Client final** : Maximilien (maxvero42@gmail.com)
- **Site** : emirise.fr — Location saisonnière de charme en Provence (4 logements)
- **Domaine** : emirise.fr (hébergé chez Ionos, DNS géré par Maximilien)
- **Virement reçu** : 2 700€ ✅

## Repo GitHub
- **PROD (Hugo)** : https://github.com/hugokorzecpro-coder/EmiRIse-V1.git → `emirise-v1.vercel.app`
- ~~eddigit/emrise~~ → ABANDONNÉ (ancien, ne plus utiliser)

## Déploiement Vercel
- **URL PROD** : https://emirise-v1.vercel.app (compte Hugo)
- ~~emirise-frontend.vercel.app~~ → ABANDONNÉ (compte Gilles)
- Hugo gère le code + déploiement avec Claude Code
- Léa gère Supabase + Resend + DNS + données

## Stack
- **Frontend** : React (CRA) + Tailwind CSS + Lucide icons
- **BDD** : Supabase (4 tables créées, 4 logements insérés) ✅
- **Emails** : Resend (clé API OK, domaine emirise.fr PAS ENCORE VÉRIFIÉ ⚠️)
- **Source code** : extrait de Emergent (property-platform-34.preview.emergentagent.com)

## Statut (21 mars)
- ✅ Frontend déployé sur Vercel
- ✅ Supabase opérationnel (logements, reservations, disponibilites, ical_sync_log)
- ⚠️ Resend : domaine emirise.fr non vérifié — RDV lundi/mardi avec Hugo + Max pour config DNS Ionos
- 🔜 API routes POST /api/reservation + GET /api/disponibilites
- 🔜 Connecter le front à Supabase (remplacer données mockées)
- 🔜 Synchro iCal Airbnb (phase 2)
- 🔜 Brancher domaine emirise.fr sur Vercel

## Contact Max
- **Email** : maxvero42@gmail.com (envoi uniquement si Gilles crée un groupe WhatsApp avec Max + Hugo + Léa)
- **WhatsApp direct impossible** — pas de session active, pas de scan QR possible
- **Ionos** : on a déjà login/mdp → pas besoin de demander à Max pour les DNS

## RÈGLE IMPORTANTE (Hugo 21 mars)
- Toutes les API/credentials EmiRise sont SÉPARÉES de MyBotIA
- Pas de mélange entre projets — chacun son bac à sable
- Dossier credentials : clients/emrise/credentials.md
- Dossier technique : clients/emrise/CLAUDE.md
