# TOOLS.md — Outils de Léa

> Les credentials sont stockées dans PostgreSQL (table `credentials` dans `mybotia_crm`).
> Pour récupérer un credential : `python3 tools/get_credential.py <service> [key_name]`
> Pour lister les services : `python3 tools/get_credential.py`

---

## Gmail — coachdigitalparis@gmail.com
Email officiel Coach Digital.
```bash
python3 tools/read_emails.py 5
python3 tools/send_email.py "dest@email.com" "Sujet" "Message"
```
- OK : Lire emails, répondre demandes courantes, relances factures
- Validation Gilles requise : Emails clients importants, engagements financiers

## Gmail — leacoachdigital@gmail.com
Email de Léa (Admin & Juridique).
```bash
python3 tools/read_emails.py 5 "recherche" "leacoachdigital@gmail.com"
python3 tools/send_email.py "dest@email.com" "Sujet" "Message" leacoachdigital@gmail.com
```

## Gmail — gilleskorzec@gmail.com
Email perso Gilles.
```bash
python3 tools/read_emails.py 5 "recherche" "gilleskorzec@gmail.com"
python3 tools/send_email.py "dest@email.com" "Sujet" "Message" gilleskorzec@gmail.com
```
- Validation Gilles requise : Emails importants, sujets sensibles

---

## Banque — Qonto
```bash
python3 tools/qonto.py balance
python3 tools/qonto.py transactions 10
python3 tools/qonto.py org
```
- OK : Consulter solde, lister transactions, préparer éléments comptable
- INTERDIT : Initier virements, partager credentials

---

## PISTE.gouv.fr — APIs Juridiques
Légifrance, Judilibre, BOAMP. Compte coachdigitalparis@gmail.com.
Doc : https://piste.gouv.fr/

---

## GitHub — Org eddigit
Deux tokens dispo : `github-team` (repo+workflow) et `github-admin` (full access, no expiry).

## Vercel — Full Account
Compte gilleskorzec@gmail.com.

## Cloudflare — DNS Management
Permissions : Zone > DNS > Edit (toutes les zones).

## GoDaddy — Domaines Clients
- OK : Consulter domaines, vérifier disponibilité, gérer DNS
- Validation Gilles requise : Achat, transfert, suppression

---

## Notion — API Integration
```bash
python3 tools/get_credential.py notion api_key
```
- OK : Lire, créer, modifier pages et bases de données
- INTERDIT : Supprimer pages sans validation Gilles

---

## MyBotIA Admin — Agent API
```
URL locale : http://127.0.0.1:3001/api/agent/
URL publique : https://admin.mybotia.com/api/agent/
Header : X-API-Key: <api_key>    X-Agent-Id: lea
```
Endpoints : GET /briefing, GET /clients?status=Actif, CRUD clients/pipeline/projets/paiements.

---

## Telegram — Scripts
```bash
python3 tools/telegram_manager.py contacts
python3 tools/telegram_manager.py dialogs
python3 tools/telegram_manager.py groups
```
Bots : @lea_admin_bot, @nina_coachdigital_bot, @julian_expert_bot, @oscar_coachdigital_bot

---

## AWS — Amazon SES
Région eu-north-1. Expéditeur : coachdigitalparis@gmail.com. Domaine vérifié SPF+DKIM+DMARC.

## LWS — Hébergement VPS
Panel : https://panel.lws.fr/ — Client 783705.

---

## Envoi WhatsApp — Texte
```bash
openclaw gateway call send \
  --token $(python3 tools/get_credential.py openclaw-vps gateway_token) \
  --url ws://127.0.0.1:18789 \
  --params '{"channel":"whatsapp","to":"JID","message":"TEXTE","idempotencyKey":"clé-unique"}' \
  --json
```
- DM : `33XXXXXXXXX@s.whatsapp.net`
- Groupe : `120363...@g.us`
- Champ = **"message"** (pas "text" ni "body")

## Envoi WhatsApp — Vocal / Média
```bash
OPENCLAW_GATEWAY_TOKEN=67085f007e934ad258db36616d4797d3d3ec916cafef7d44 \
openclaw message send --channel whatsapp --target "+33XXXXXXXXX" --media "/chemin/fichier.ogg"
```
- ⚠️ `gateway call send` = texte uniquement. Pour fichiers/vocaux → `openclaw message send --media`
- ⚠️ Le fichier DOIT être dans le workspace (`~/.openclaw/workspace/media/`). `/tmp/` interdit (LocalMediaAccessError)
- Script vocal : `scripts/voice-reply-wa.sh "texte" "+33XXXXXXXXX"`

## Envoi Telegram — Vocal
```bash
scripts/voice-reply.sh "texte" "chat_id"
```

## Voix validée — TOUS canaux
- **Voix** : `fr-FR-VivienneMultilingualNeural` rate=-4% pitch=-2Hz
- **Moteur** : edge-tts (gratuit, illimité)
- ⚠️ TOUJOURS Vivienne. Jamais DeniseNeural ou autre.

---

## Extension Chrome MyBotIA — Actions Navigateur (Phase 3)

Quand un utilisateur te parle via l'extension Chrome MyBotIA (sidepanel), tu peux **agir sur sa page** en envoyant des blocs d'action dans ta réponse.

**Instructions complètes** : voir `BROWSER-ACTIONS.md` dans ce workspace.

Actions disponibles :
- `fill-field` : remplir un champ (input, textarea, select)
- `click-element` : cliquer sur un bouton/lien
- `navigate` : naviguer vers une URL

Format :
````
```mybotia-action
{"action": "fill-field", "selector": "#email", "value": "test@example.com"}
```
````

**Règles** : toujours demander confirmation avant d'agir, utiliser les sélecteurs du contexte de page, décrire l'action avant de l'exécuter.

---

> Pour accéder à n'importe quel credential : `python3 tools/get_credential.py`
