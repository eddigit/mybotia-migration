#!/usr/bin/env python3
"""TTS via ElevenLabs API, fallback edge-tts Vivienne.
Usage: echo "texte" | python3 tts-elevenlabs.py output.mp3 [rate] [pitch] [voice]
Reads ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID from env or credentials DB.
"""
import asyncio, sys, os, subprocess, json, re

# ── Credentials ──────────────────────────────────────────────────────────
def get_credential(service, key):
    """Get credential from PostgreSQL via docker."""
    try:
        result = subprocess.run(
            ["docker", "exec", "prospection_postgres", "psql", "-U", "prospection",
             "-d", "mybotia_crm", "-t", "-A", "-c",
             f"SELECT key_value FROM credentials WHERE service = '{service}' AND key_name = '{key}';"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return None

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY') or get_credential('elevenlabs', 'api_key')
ELEVENLABS_VOICE_ID = os.environ.get('ELEVENLABS_VOICE_ID') or get_credential('elevenlabs', 'voice_id')

# ── French diction fixes (same as tts-ssml.py) ──────────────────────────
def fix_french_diction(text):
    # ── Contractions françaises ──
    contractions = [
        (r"\bje ai\b", "j'ai"), (r"\bje avais\b", "j'avais"),
        (r"\bje aurais\b", "j'aurais"), (r"\bje étais\b", "j'étais"),
        (r"\bje en\b", "j'en"), (r"\bje y\b", "j'y"),
        (r"\bce est\b", "c'est"), (r"\bde un\b", "d'un"),
        (r"\bde une\b", "d'une"), (r"\bde accord\b", "d'accord"),
        (r"\bque il\b", "qu'il"), (r"\bque elle\b", "qu'elle"),
        (r"\bque on\b", "qu'on"), (r"\bse est\b", "s'est"),
        (r"\bjusque à\b", "jusqu'à"), (r"\blorsque il\b", "lorsqu'il"),
        (r"\bne est\b", "n'est"), (r"\bne a\b", "n'a"),
        (r"\bne ai\b", "n'ai"), (r"\bne ont\b", "n'ont"),
        (r"\bme a\b", "m'a"), (r"\bte a\b", "t'a"),
        (r"\bse en\b", "s'en"), (r"\ble a\b", "l'a"),
        (r"\bpuisque il\b", "puisqu'il"), (r"\bpuisque elle\b", "puisqu'elle"),
        (r"\bquoique il\b", "quoiqu'il"),
    ]
    for pattern, replacement in contractions:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # ── Symboles et unités → mots prononcés ──
    text = re.sub(r'\b(\d+)\s*€', r'\1 euros', text)
    text = re.sub(r'\b(\d+)\s*%', r'\1 pour cent', text)
    text = re.sub(r'\b(\d+)\s*°C?\b', r'\1 degrés', text)
    text = re.sub(r'\b(\d+)\s*km/h\b', r'\1 kilomètres heure', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(\d+)\s*km\b', r'\1 kilomètres', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(\d+)\s*m²\b', r'\1 mètres carrés', text)
    text = re.sub(r'\b(\d+)\s*m\b(?!\w)', r'\1 mètres', text)

    # ── Abréviations courantes ──
    text = re.sub(r'\betc\.\b', 'et cetera', text, flags=re.IGNORECASE)
    text = re.sub(r'\bM\.\s', 'Monsieur ', text)
    text = re.sub(r'\bMme\.?\s', 'Madame ', text)
    text = re.sub(r'\bMe\.?\s', 'Maître ', text)
    text = re.sub(r'\bDr\.?\s', 'Docteur ', text)
    text = re.sub(r'\bn°\s*(\d+)', r'numéro \1', text, flags=re.IGNORECASE)
    text = re.sub(r'\btel\.?\s*:', 'téléphone :', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcàd\b', "c'est-à-dire", text, flags=re.IGNORECASE)
    text = re.sub(r'\brdv\b', 'rendez-vous', text, flags=re.IGNORECASE)
    text = re.sub(r'\basap\b', 'dès que possible', text, flags=re.IGNORECASE)
    text = re.sub(r'\bstp\b', "s'il te plaît", text, flags=re.IGNORECASE)
    text = re.sub(r'\bsvp\b', "s'il vous plaît", text, flags=re.IGNORECASE)

    # ── Sigles tech → épelés ──
    text = re.sub(r'\bIA\b', 'I.A.', text)
    text = re.sub(r'\bCRM\b', 'C.R.M.', text)
    text = re.sub(r'\bSaaS\b', 'sasse', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAPI\b', 'A.P.I.', text)
    text = re.sub(r'\bPDF\b', 'P.D.F.', text)
    text = re.sub(r'\bSMS\b', 'S.M.S.', text)
    text = re.sub(r'\bURL\b', 'U.R.L.', text)
    text = re.sub(r'\bVPS\b', 'V.P.S.', text)
    text = re.sub(r'\bCGV\b', 'C.G.V.', text)
    text = re.sub(r'\bCGU\b', 'C.G.U.', text)
    text = re.sub(r'\bTVA\b', 'T.V.A.', text)
    text = re.sub(r'\bHTTPS?\b', '', text, flags=re.IGNORECASE)

    # ── Nombres grands → lisibles ──
    def format_number(match):
        n = int(match.group(0))
        if n >= 1000000:
            millions = n / 1000000
            return f"{millions:.1f} millions".replace('.0 ', ' ')
        elif n >= 1000:
            return f"{n:,}".replace(',', ' ')
        return str(n)
    text = re.sub(r'\b\d{4,}\b', format_number, text)

    # ── Heures ──
    text = re.sub(r'(\d{1,2})h(\d{2})', r'\1 heures \2', text)
    text = re.sub(r'(\d{1,2})h\b', r'\1 heures', text)

    # ── Ponctuation pour rythme naturel ──
    # Ajouter micro-pauses aux tirets longs et points-virgules
    text = re.sub(r'\s*[—–]\s*', ', ', text)
    text = re.sub(r';', ',', text)

    # ── Nettoyage final ──
    text = re.sub(r'\s{2,}', ' ', text).strip()
    return text


# ── ElevenLabs TTS ───────────────────────────────────────────────────────
def synthesize_elevenlabs(text, output_path):
    """Call ElevenLabs API. Returns True on success."""
    if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
        return False
    try:
        import urllib.request
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        payload = json.dumps({
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.35,
                "similarity_boost": 0.80,
                "style": 0.45,
                "use_speaker_boost": True,
                "speed": 0.95
            }
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                with open(output_path, 'wb') as f:
                    f.write(resp.read())
                return True
        return False
    except Exception as e:
        print(f"[tts-elevenlabs] ElevenLabs error: {e}", file=sys.stderr)
        return False


# ── Fallback edge-tts ────────────────────────────────────────────────────
async def synthesize_edgetts(text, output_path, rate="-5%", pitch="-2Hz", voice="fr-FR-VivienneMultilingualNeural"):
    import edge_tts
    comm = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    await comm.save(output_path)


# ── Main ─────────────────────────────────────────────────────────────────
async def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: echo 'texte' | python3 tts-elevenlabs.py output.mp3 [rate] [pitch] [voice]", file=sys.stderr)
        sys.exit(1)

    output_path = args[0]
    rate = args[1] if len(args) > 1 else "-5%"
    pitch = args[2] if len(args) > 2 else "-2Hz"
    voice = args[3] if len(args) > 3 else "fr-FR-VivienneMultilingualNeural"

    text = sys.stdin.read().strip()
    if not text:
        sys.exit(1)

    # Apply French diction fixes
    text = fix_french_diction(text)

    # Try ElevenLabs first
    if synthesize_elevenlabs(text, output_path):
        print("[tts-elevenlabs] OK (ElevenLabs)", file=sys.stderr)
        return

    # Fallback to edge-tts
    print("[tts-elevenlabs] Fallback to edge-tts", file=sys.stderr)
    await synthesize_edgetts(text, output_path, rate, pitch, voice)

asyncio.run(main())
