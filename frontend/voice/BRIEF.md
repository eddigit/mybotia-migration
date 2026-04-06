# POC Voice Mode — Collaborateur IA Vocal

## Objectif
Page web sur voice.mybotia.com permettant une conversation vocale avec un collaborateur IA.
L'utilisateur clique sur un bouton micro, parle, et reçoit une réponse vocale.

## Flux technique
1. L'utilisateur clique sur le bouton micro
2. Le navigateur enregistre l'audio (Web Audio API / MediaRecorder)
3. L'audio est envoyé au serveur (Node.js/Express sur le VPS)
4. Le serveur transcrit via Groq Whisper API (clé: GROQ_KEY_REMOVED)
5. Le texte transcrit est envoyé à Claude (Anthropic API, clé: ANTHROPIC_KEY_REMOVED)
6. La réponse de Claude est convertie en audio via edge-tts (voix: fr-FR-VivienneMultilingualNeural, rate=-4%, pitch=-2Hz)
7. L'audio est renvoyé au navigateur et joué automatiquement

## Stack
- **Frontend** : HTML/CSS/JS vanilla, design minimaliste et premium
- **Backend** : Node.js + Express
- **STT** : Groq Whisper API
- **LLM** : Anthropic Claude (claude-sonnet-4-6)
- **TTS** : edge-tts (installé sur le serveur, commande: edge-tts)
- **Port** : 3100 (backend)

## Design
- Fond sombre, élégant
- Gros bouton micro au centre (pulsation quand écoute active)
- Indicateur visuel : "En écoute...", "Réflexion...", "Parle..."
- Logo MyBotIA en haut
- Responsive mobile

## Système prompt du collaborateur
"Tu es Léa, collaboratrice IA de Coach Digital Paris. Tu réponds de manière concise et professionnelle en français. Tu es spécialisée en juridique, administratif et commercial. Réponds en 2-3 phrases maximum pour que la réponse vocale reste fluide."

## Contraintes
- Pas de framework frontend lourd (pas de React/Vue)
- Pas de LiveKit pour l'instant (on fait simple)
- Le fichier audio temporaire est nettoyé après envoi
- CORS configuré pour mybotia.com
- Timeout de 30 secondes max pour l'ensemble du flux
