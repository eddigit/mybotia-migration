#!/usr/bin/env python3
"""TTS SSML — voix naturelle française via edge-tts.
Usage: python3 tts-ssml.py output.mp3 --rate=-5% --pitch=-3% < text
       python3 tts-ssml.py output.mp3 --text "Bonjour Gilles"
"""
import asyncio, sys, re, argparse
import edge_tts

VOICE = "fr-FR-VivienneMultilingualNeural"
STYLE = "friendly"
STYLE_DEGREE = "1.2"

# ── Post-traitement français — diction naturelle ────────────────────────────
def fix_french_diction(text):
    """Corrige les problèmes courants de diction TTS en français."""

    # Contractions obligatoires en français parlé
    # "je ai" → "j'ai", "te aider" → "t'aider", etc.
    contractions = [
        (r"\bje ai\b", "j'ai"),
        (r"\bje avais\b", "j'avais"),
        (r"\bje aurais\b", "j'aurais"),
        (r"\bje aurai\b", "j'aurai"),
        (r"\bje étais\b", "j'étais"),
        (r"\bje en\b", "j'en"),
        (r"\bje y\b", "j'y"),
        (r"\bte aider\b", "t'aider"),
        (r"\bte envoyer\b", "t'envoyer"),
        (r"\bte expliquer\b", "t'expliquer"),
        (r"\bte informer\b", "t'informer"),
        (r"\bte accompagner\b", "t'accompagner"),
        (r"\bte assurer\b", "t'assurer"),
        (r"\bme a\b", "m'a"),
        (r"\bme en\b", "m'en"),
        (r"\bme y\b", "m'y"),
        (r"\bse est\b", "s'est"),
        (r"\bse en\b", "s'en"),
        (r"\bce est\b", "c'est"),
        (r"\bde un\b", "d'un"),
        (r"\bde une\b", "d'une"),
        (r"\bde abord\b", "d'abord"),
        (r"\bde accord\b", "d'accord"),
        (r"\bde ailleurs\b", "d'ailleurs"),
        (r"\ble on\b", "l'on"),
        (r"\bla entreprise\b", "l'entreprise"),
        (r"\bla application\b", "l'application"),
        (r"\bla équipe\b", "l'équipe"),
        (r"\bla idée\b", "l'idée"),
        (r"\bque il\b", "qu'il"),
        (r"\bque elle\b", "qu'elle"),
        (r"\bque on\b", "qu'on"),
        (r"\bque un\b", "qu'un"),
        (r"\bque une\b", "qu'une"),
        (r"\bjusque à\b", "jusqu'à"),
        (r"\bjusque au\b", "jusqu'au"),
        (r"\bjusque ici\b", "jusqu'ici"),
        (r"\blorsque il\b", "lorsqu'il"),
        (r"\blorsque on\b", "lorsqu'on"),
        (r"\bpuisque il\b", "puisqu'il"),
        (r"\bpuisque on\b", "puisqu'on"),
    ]
    for pattern, replacement in contractions:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Nombres et abréviations courantes — prononciation
    text = re.sub(r'\b(\d+)\s*€', r'\1 euros', text)
    text = re.sub(r'\b(\d+)\s*%', r'\1 pour cent', text)
    text = re.sub(r'\betc\.\b', 'et cetera', text, flags=re.IGNORECASE)
    text = re.sub(r'\bM\.\s', 'Monsieur ', text)
    text = re.sub(r'\bMme\.?\s', 'Madame ', text)
    text = re.sub(r'\bn°\s*(\d+)', r'numéro \1', text, flags=re.IGNORECASE)

    # Sigles courants — épeler
    text = re.sub(r'\bIA\b', 'I.A.', text)
    text = re.sub(r'\bCRM\b', 'C.R.M.', text)
    text = re.sub(r'\bPOC\b', 'P.O.C.', text)
    text = re.sub(r'\bAPI\b', 'A.P.I.', text)
    text = re.sub(r'\bUI\b', 'U.I.', text)
    text = re.sub(r'\bUX\b', 'U.X.', text)
    text = re.sub(r'\bSMS\b', 'S.M.S.', text)
    text = re.sub(r'\bPDF\b', 'P.D.F.', text)
    text = re.sub(r'\bHT\b', 'H.T.', text)
    text = re.sub(r'\bTTC\b', 'T.T.C.', text)
    text = re.sub(r'\bRH\b', 'R.H.', text)
    text = re.sub(r'\bIT\b', 'I.T.', text)
    text = re.sub(r'\bCA\b', 'C.A.', text)
    text = re.sub(r'\bCDI\b', 'C.D.I.', text)
    text = re.sub(r'\bSaaS\b', 'sasse', text, flags=re.IGNORECASE)

    # Email / web — prononciation naturelle
    # arobase @ → "arobase"
    text = re.sub(r'@', ' arobase ', text)
    # .com .fr .org .net .io .pro → prononcé
    text = re.sub(r'\.com\b', ' point com', text, flags=re.IGNORECASE)
    text = re.sub(r'\.fr\b', ' point fr', text, flags=re.IGNORECASE)
    text = re.sub(r'\.org\b', ' point org', text, flags=re.IGNORECASE)
    text = re.sub(r'\.net\b', ' point net', text, flags=re.IGNORECASE)
    text = re.sub(r'\.io\b', ' point i o', text, flags=re.IGNORECASE)
    text = re.sub(r'\.pro\b', ' point pro', text, flags=re.IGNORECASE)
    text = re.sub(r'\.ai\b', ' point a i', text, flags=re.IGNORECASE)
    # https:// http:// www. → supprimer (déjà mentionné le domaine)
    text = re.sub(r'https?://', '', text)
    text = re.sub(r'\bwww\.', '', text)
    # Sous-domaines courants
    text = re.sub(r'\.mybotia\.', ' point mybotia point ', text)

    # Ponctuation technique
    text = re.sub(r'/', ' slash ', text)
    text = re.sub(r'#(\d+)', r'numéro \1', text)

    # Heures — 14h30 → "14 heures 30"
    text = re.sub(r'(\d{1,2})h(\d{2})', r'\1 heures \2', text)
    text = re.sub(r'(\d{1,2})h\b', r'\1 heures', text)

    # Cleanup espaces multiples
    text = re.sub(r'\s{2,}', ' ', text).strip()

    return text


def add_ssml_pauses(text):
    """Insert SSML break tags at natural pause points."""
    # Pause after sentence-ending punctuation
    text = re.sub(r'([.!?…])\s+', r'\1 <break time="300ms"/> ', text)
    # Shorter pause after commas and semicolons
    text = re.sub(r'([,;])\s+', r'\1 <break time="150ms"/> ', text)
    # Pause after colons
    text = re.sub(r':\s+', r': <break time="200ms"/> ', text)
    # Micro-pause before transition words (natural breathing)
    text = re.sub(
        r'\b(mais|donc|alors|en fait|d\'ailleurs|par contre|cependant|toutefois|du coup|en revanche)\b',
        r'<break time="120ms"/> \1',
        text, flags=re.IGNORECASE
    )
    return text


def build_ssml(text, rate="-5%", pitch="-3%"):
    """Build SSML with express-as style for natural delivery."""
    text = fix_french_diction(text)
    text = add_ssml_pauses(text)
    return f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="fr-FR">
  <voice name="{VOICE}">
    <lang xml:lang="fr-FR">
      <mstts:express-as style="{STYLE}" styledegree="{STYLE_DEGREE}">
        <prosody rate="{rate}" pitch="{pitch}">
          {text}
        </prosody>
      </mstts:express-as>
    </lang>
  </voice>
</speak>'''


async def main():
    # Simple arg parsing to avoid argparse issues with negative values like -5%
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 tts-ssml.py output.mp3 [rate] [pitch]", file=sys.stderr)
        print("Text via stdin", file=sys.stderr)
        sys.exit(1)

    output_path = args[0]
    rate = args[1] if len(args) > 1 else "-5%"
    pitch = args[2] if len(args) > 2 else "-2Hz"
    voice = args[3] if len(args) > 3 else VOICE

    text = sys.stdin.read().strip()
    if not text:
        sys.exit(1)

    # Apply French diction fixes (contractions, abbreviations, etc.)
    text = fix_french_diction(text)

    # Use Communicate with explicit parameters — NOT SSML.
    # edge_tts.Communicate escapes XML tags, so passing SSML as text
    # destroys <lang xml:lang="fr-FR"> and Vivienne falls back to German.
    comm = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    await comm.save(output_path)

asyncio.run(main())
