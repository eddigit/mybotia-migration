# BRIEF V2 — JARVIS : Mode vocal temps réel (Production)

> Brief pour Claude Code. Ne pas modifier manuellement.
> Préparé par Léa — 25 mars 2026, 05h15

---

## Contexte

Le POC V1 est en ligne sur https://voice.mybotia.com (port 3100, Apache reverse proxy SSL).
Il fonctionne en mode push-to-talk : clic → enregistrement → upload audio → STT → LLM → TTS → playback.

**On passe en V2 : mode JARVIS — conversation vocale continue en temps réel.**

---

## Ce qui existe (V1 — NE PAS CASSER)

```
/home/gilles/apps/voice-poc/
├── server.js          # Express, POST /api/voice (Groq Whisper + Groq Llama + edge-tts)
├── start.sh           # Restart loop
├── package.json       # express, cors, multer, @anthropic-ai/sdk, groq-sdk
├── public/
│   ├── index.html     # Frontend (HTML vanilla)
│   ├── app.js         # Frontend JS (push-to-talk)
│   └── style.css      # Design premium dark/violet (13KB — GARDER TEL QUEL)
```

- **DNS** : voice.mybotia.com → 180.149.198.23
- **Apache** : `/etc/apache2/sites-enabled/voice-mybotia-le-ssl.conf` — ProxyPass vers localhost:3100
- **SSL** : Let's Encrypt wildcard *.mybotia.com
- **Process** : `node server.js` (PID actif, auto-restart via start.sh)

---

## Objectif V2 : Mode JARVIS

### UX cible
1. L'utilisateur ouvre voice.mybotia.com
2. Il clique UNE SEULE FOIS sur le bouton micro
3. Le micro reste ouvert en permanence
4. L'IA écoute, détecte quand l'humain a fini de parler, répond vocalement
5. L'humain peut interrompre l'IA à tout moment (barge-in)
6. La conversation continue indéfiniment, sans re-cliquer
7. Un bouton "Raccrocher" met fin à la session

### Ce qui change techniquement

| Aspect | V1 (actuel) | V2 (cible) |
|--------|-------------|------------|
| Transport | HTTP POST (upload blob) | **WebSocket streaming** |
| Mode micro | Push-to-talk (clic/clic) | **Micro ouvert en continu** |
| Détection fin de parole | Manuelle (clic stop) | **VAD automatique (Silero)** |
| STT | Groq Whisper (batch, après upload) | **Groq Whisper streaming** ou **Deepgram Nova-3 WebSocket** |
| LLM | Groq Llama 3.3 70B | **Claude claude-sonnet-4-6 (Anthropic)** |
| TTS | edge-tts (batch, fichier complet) | **edge-tts streaming** (phrase par phrase) |
| Barge-in | Non | **Oui** — coupe la lecture audio dès que l'humain parle |
| Historique conversation | Non (stateless) | **Oui** — contexte conversationnel maintenu en session |
| Latence cible | ~3-5s (upload+process+download) | **< 1.5s** (TTFA — time to first audio) |

---

## Architecture V2

```
┌──────────────────────────────────────────────────────────┐
│                     NAVIGATEUR                            │
│                                                          │
│  WebAudio API → VAD (Silero ONNX en WASM)               │
│       │                                                  │
│       │ Audio PCM chunks (pendant que l'humain parle)    │
│       ▼                                                  │
│  WebSocket ←→ Serveur Node.js (port 3100)               │
│       │                                                  │
│       │ Audio MP3 chunks (pendant que l'IA parle)        │
│       ▼                                                  │
│  AudioContext → Lecture audio en streaming                │
│                                                          │
│  Barge-in : si VAD détecte voix pendant lecture →        │
│             STOP lecture, envoyer nouveau chunk           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                   SERVEUR (Node.js)                       │
│                                                          │
│  WebSocket server (ws ou socket.io)                      │
│       │                                                  │
│  1. Réception chunks audio du navigateur                 │
│  2. VAD serveur (Silero via onnxruntime-node)            │
│     → détecte début/fin de parole                        │
│  3. STT : envoi audio à Groq Whisper API                 │
│     (ou Deepgram Nova-3 WebSocket pour streaming)        │
│  4. LLM : Claude claude-sonnet-4-6 (streaming SSE)              │
│     → system prompt Léa + historique conversation        │
│     → streaming de tokens                                │
│  5. TTS : edge-tts phrase par phrase                     │
│     → dès qu'une phrase est complète, synthèse           │
│     → envoi audio chunk par WebSocket au client          │
│  6. Barge-in : si nouveau audio reçu pendant TTS         │
│     → signal "stop" au client + annule TTS en cours      │
│                                                          │
│  Session : Map<sessionId, { history[], isPlaying }>      │
└──────────────────────────────────────────────────────────┘
```

---

## Stack technique

### STT — 2 options (choisir la plus simple qui marche)

**Option A : Groq Whisper (batch rapide)**
- On garde Groq Whisper comme en V1
- Le VAD côté serveur accumule l'audio de la phrase complète
- Quand la parole se termine → envoi batch à Groq Whisper
- Latence STT : ~200-400ms (Groq est très rapide)
- ✅ Plus simple, déjà implémenté
- Clé : `GROQ_KEY_REMOVED`

**Option B : Deepgram Nova-3 (streaming WebSocket)**
- WebSocket persistant vers Deepgram
- Transcription partielle en temps réel
- Latence STT : ~100-200ms
- ⚠️ Payant ($0.0043/min) — OK pour prod
- Nécessite une clé API Deepgram (à créer)

**→ Commencer par Option A (Groq batch). Passer à B si la latence est insuffisante.**

### LLM — Claude Anthropic

```javascript
const anthropic = new Anthropic({ apiKey: ANTHROPIC_API_KEY });

// Streaming
const stream = anthropic.messages.stream({
  model: 'claude-sonnet-4-6',
  max_tokens: 300,
  system: SYSTEM_PROMPT,
  messages: conversationHistory
});

// Lire token par token
for await (const event of stream) {
  if (event.type === 'content_block_delta') {
    const text = event.delta.text;
    // Accumuler jusqu'à une phrase complète (. ! ? \n)
    // Dès qu'une phrase est complète → lancer TTS
  }
}
```

- Clé : `ANTHROPIC_KEY_REMOVED`
- Modèle : `claude-sonnet-4-6` (rapide + intelligent)
- Streaming : **obligatoire** pour réduire le TTFA

### TTS — edge-tts (phrase par phrase)

```bash
edge-tts --voice fr-FR-VivienneMultilingualNeural --rate=-4% --pitch=-2Hz \
  --text "Phrase courte." --write-media /tmp/chunk_001.mp3
```

- **Stratégie** : dès qu'une phrase complète sort du LLM, lancer edge-tts dessus
- Pendant que la phrase 1 est lue par le client, préparer la phrase 2
- Pipeline : LLM phrase 1 → TTS phrase 1 → envoi client | LLM phrase 2 → TTS phrase 2 → …
- **VOIX OBLIGATOIRE** : `fr-FR-VivienneMultilingualNeural` rate=-4% pitch=-2Hz

### VAD — Silero (détection voix)

**Côté navigateur (WASM) :**
- `@ricky0123/vad-web` — Silero VAD compilé en WASM
- Détecte début/fin de parole
- Envoie les segments audio uniquement pendant la parole
- npm : `npm install @ricky0123/vad-web`

**Côté serveur (optionnel, backup) :**
- `@ricky0123/vad-node` — Silero via ONNX Runtime
- Double vérification si besoin

---

## System Prompt V2

```
Tu es Léa, directrice administrative et juridique de Coach Digital Paris.

CONTEXTE : Tu es en conversation vocale temps réel. L'utilisateur te parle et t'entend.

RÈGLES VOCALES :
- Réponds en 1 à 3 phrases MAXIMUM par tour de parole
- Sois naturelle et conversationnelle, comme au téléphone
- Pas de listes à puces, pas de markdown, pas de formatage
- Pas de "Bien sûr !", "Absolument !", "Excellente question !" — sois directe
- Si la question est complexe, donne la réponse courte d'abord, puis propose d'approfondir
- Utilise des transitions naturelles : "En fait...", "D'ailleurs...", "Pour ça..."

EXPERTISE :
- Droit des affaires, droit du travail, droit immobilier
- Administratif, facturation, relances
- Recherche de jurisprudence (Judilibre, Légifrance)

IDENTITÉ :
- Tu es Léa, pas une IA générique
- Tu travailles pour Coach Digital Paris, fondé par Gilles Korzec
- Tu ne dis JAMAIS "en tant qu'IA" ou "je suis une intelligence artificielle"
- Tu signes mentalement "Léa - Coach Digital Paris"
```

---

## Frontend V2 — Modifications

### Ce qui est GARDÉ tel quel :
- `style.css` — design complet (13KB), ne pas toucher
- Palette violet/indigo, fond sombre, animations
- Structure HTML globale (header, card, footer)
- Badge agent

### Logo — REMPLACER
- Remplacer le logo texte "M / MyBotIA" par le vrai logo SVG :
- URL : `https://res.cloudinary.com/dniurvpzd/image/upload/v1772032713/Logo_Collaborateur_IA_coujhr.svg`
- Afficher en `<img>` dans le header, hauteur ~34-40px, pas de déformation
- Garder le texte "MyBot**IA**" à côté si ça rend bien, sinon le logo seul suffit

### Ce qui CHANGE :

1. **Bouton micro** → bascule entre "Démarrer" et "Raccrocher"
   - Clic 1 : ouvre le WebSocket + active le micro en continu
   - Clic 2 : ferme le WebSocket + coupe le micro
   - Plus de clic par message

2. **États visuels** (réutiliser les classes CSS existantes) :
   - `idle` → "Cliquez pour démarrer la conversation"
   - `listening` → "En écoute..." (avatar-ring.recording — pulsation violette)
   - `processing` → "Réflexion..." (avatar-ring.processing — spinner)
   - `speaking` → "Léa répond..." (avatar-ring.speaking — glow vert)
   - Transitions automatiques, pas de clic

3. **Transcript** → historique scrollable
   - Garder le design des blocs transcript existants
   - Ajouter au fil de la conversation (pas remplacer)
   - Scroll auto vers le bas

4. **Indicateur de connexion** → petit point vert/rouge à côté du badge agent

5. **Barre de volume** (optionnel, nice-to-have) → visualisation du niveau micro

---

## Backend V2 — Modifications

### Garder :
- Express pour servir les fichiers statiques
- Le endpoint `/api/health`
- Le port 3100

### Ajouter :

1. **WebSocket server** (`ws` ou `socket.io`)
   - Même port 3100 (upgrade HTTP → WS)
   - Protocole de messages :

```
CLIENT → SERVER :
  { type: "audio", data: <ArrayBuffer PCM 16kHz mono> }
  { type: "speech_start" }        // VAD détecte début parole
  { type: "speech_end" }          // VAD détecte fin parole
  { type: "stop" }                // L'utilisateur raccroche

SERVER → CLIENT :
  { type: "listening" }           // Serveur prêt à écouter
  { type: "processing" }          // STT reçu, LLM en cours
  { type: "transcript", text: "..." }          // Ce que l'humain a dit
  { type: "response_text", text: "..." }       // Ce que Léa dit (pour affichage)
  { type: "audio_chunk", data: <ArrayBuffer MP3> }  // Audio à jouer
  { type: "audio_end" }           // Fin de la réponse audio
  { type: "barge_in" }            // Stop lecture, l'humain reprend la parole
  { type: "error", message: "..." }
```

2. **Session manager** :
   - `Map<wsConnection, Session>`
   - Session = `{ id, history: Message[], isGenerating: boolean, ttsProcess: ChildProcess|null }`
   - Historique limité aux 20 derniers messages (pour ne pas exploser le contexte)

3. **Pipeline streaming** :
```
speech_end reçu
  → concaténer les chunks audio de la phrase
  → convertir en format compatible Groq (webm/ogg si besoin via ffmpeg)
  → envoyer à Groq Whisper
  → recevoir transcription
  → envoyer { type: "transcript" } au client
  → envoyer { type: "processing" } au client
  → streamer Claude (claude-sonnet-4-6)
  → accumuler tokens jusqu'à fin de phrase (. ! ? \n)
  → dès qu'une phrase est complète :
      → lancer edge-tts en parallèle
      → envoyer { type: "response_text" } au client
      → envoyer { type: "audio_chunk" } dès que le MP3 est prêt
  → à la fin du streaming Claude :
      → envoyer { type: "audio_end" }
      → repasser en mode écoute
```

4. **Barge-in** :
   - Si `speech_start` reçu pendant que le serveur génère/envoie de l'audio :
     - Envoyer `{ type: "barge_in" }` au client
     - Kill le process edge-tts en cours
     - Annuler le streaming Claude en cours
     - Repasser en mode écoute
     - L'historique garde quand même la réponse partielle de Léa

---

## Apache — Modification nécessaire

Le WebSocket doit passer par Apache. Modifier `/etc/apache2/sites-enabled/voice-mybotia-le-ssl.conf` :

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName voice.mybotia.com

    ProxyPreserveHost On
    ProxyRequests Off

    # WebSocket upgrade
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) ws://localhost:3100/$1 [P,L]

    # HTTP normal
    ProxyPass / http://localhost:3100/
    ProxyPassReverse / http://localhost:3100/

    Header always set X-Content-Type-Options "nosniff"

    SSLCertificateFile /etc/letsencrypt/live/mybotia.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/mybotia.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```

Modules Apache requis : `proxy_wstunnel` (probablement déjà activé).

---

## Dépendances à ajouter

```bash
cd /home/gilles/apps/voice-poc
npm install ws         # WebSocket server
# @anthropic-ai/sdk déjà dans package.json
# groq-sdk déjà dans package.json
```

Côté frontend (via CDN ou bundle) :
- `@ricky0123/vad-web` pour le VAD Silero en WASM
- Ou alternative : simple détection de volume (RMS threshold) si le VAD WASM est trop lourd

---

## Contraintes

1. **NE PAS casser la V1** — garder `/api/voice` POST fonctionnel en parallèle
2. **Port 3100** — ne pas changer (Apache configuré dessus)
3. **Voix** : `fr-FR-VivienneMultilingualNeural` rate=-4% pitch=-2Hz — NON NÉGOCIABLE
4. **Pas de framework frontend** — JS vanilla uniquement
5. **Pas de LiveKit pour cette V2** — on fait du WebSocket pur, LiveKit = V3
6. **Fichiers temporaires** dans `/tmp/` — cleanup systématique
7. **ffmpeg** est installé sur le serveur (pour conversion audio si nécessaire)
8. **edge-tts** est installé globalement (`pip install edge-tts`)
9. **Timeout** : 60s max par échange (vs 30s en V1)
10. **Design** : garder style.css EXACTEMENT tel quel, ajouter du CSS si besoin mais ne rien supprimer/modifier

---

## Tests de validation

1. ✅ Ouvrir voice.mybotia.com, cliquer "Démarrer"
2. ✅ Parler → l'IA détecte la fin de parole automatiquement
3. ✅ La réponse audio commence en < 2 secondes
4. ✅ Pendant que l'IA parle, parler → l'IA se tait immédiatement (barge-in)
5. ✅ Continuer la conversation sans re-cliquer
6. ✅ La transcription s'affiche en temps réel des deux côtés
7. ✅ Cliquer "Raccrocher" → micro coupé, WebSocket fermé
8. ✅ L'historique conversationnel est cohérent (Claude se souvient du début)
9. ✅ `/api/health` toujours fonctionnel
10. ✅ L'ancienne route POST `/api/voice` fonctionne toujours

---

## Fichiers à modifier

| Fichier | Action |
|---------|--------|
| `server.js` | Ajouter WebSocket server + pipeline streaming + sessions |
| `public/app.js` | Réécrire pour WebSocket + VAD + audio streaming |
| `public/index.html` | Modifier le bouton (Démarrer/Raccrocher) + transcript scrollable |
| `public/style.css` | **NE PAS MODIFIER** — ajouter un `style-v2.css` si besoin |
| `package.json` | Ajouter `ws` |

---

## Priorité

**Faire marcher le flux de base d'abord :**
1. WebSocket connecté ✓
2. Audio envoyé du navigateur au serveur ✓
3. VAD détecte fin de parole ✓
4. Groq Whisper transcrit ✓
5. Claude répond en streaming ✓
6. edge-tts génère l'audio phrase par phrase ✓
7. Audio renvoyé et joué ✓

**Ensuite seulement :**
8. Barge-in
9. Historique conversationnel
10. Polish UX

---

*Brief prêt. Gilles lance Claude Code dessus.*
