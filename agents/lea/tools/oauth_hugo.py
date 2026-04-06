#!/usr/bin/env python3
"""
OAuth Gmail pour Hugo — hugokorzec.pro@gmail.com
Nina accede au Gmail d'Hugo comme assistante.
"""
import json, os, sys, urllib.parse, requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'gmail-credentials.json')
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'gmail-token-hugokorzec.json')
REDIRECT_URI = 'http://localhost'

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

with open(CREDENTIALS_FILE) as f:
    creds = json.load(f)['installed']

auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode({
    'client_id': creds['client_id'],
    'redirect_uri': REDIRECT_URI,
    'response_type': 'code',
    'scope': ' '.join(SCOPES),
    'access_type': 'offline',
    'prompt': 'consent',
    'login_hint': 'hugokorzec.pro@gmail.com'
})

print("\n" + "="*60)
print("HUGO — AUTORISATION GMAIL (pour Nina)")
print("="*60)
print("\n1) Ouvre ce lien dans ton navigateur :\n")
print(auth_url)
print("\n2) Connecte-toi avec hugokorzec.pro@gmail.com")
print("3) Autorise l'acces")
print("4) Tu seras redirige vers une page qui ne charge pas (normal)")
print("5) Copie l'URL COMPLETE de la barre d'adresse\n")

url_or_code = input("Colle l'URL ou le code ici : ").strip()

if 'code=' in url_or_code:
    parsed = urllib.parse.urlparse(url_or_code)
    code = urllib.parse.parse_qs(parsed.query).get('code', [url_or_code])[0]
else:
    code = url_or_code

print("\nEchange du code contre un token...")

response = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': REDIRECT_URI
})

if response.status_code != 200:
    print(f"Erreur: {response.text}")
    sys.exit(1)

token_data = response.json()
token_data['account'] = 'hugokorzec.pro@gmail.com'

with open(TOKEN_FILE, 'w') as f:
    json.dump(token_data, f, indent=2)
os.chmod(TOKEN_FILE, 0o600)

print(f"\nTOKEN HUGO GENERE AVEC SUCCES !")
print(f"Fichier: {TOKEN_FILE}")
print("="*60)
