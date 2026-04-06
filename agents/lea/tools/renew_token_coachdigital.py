#!/usr/bin/env python3
"""
Renouvellement du token Gmail pour coachdigitalparis@gmail.com
Usage: python3 renew_token_coachdigital.py
"""
import json
import os
import sys
import urllib.parse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'gmail-credentials.json')
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'gmail-token-coachdigital.json')

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def main():
    # Charger les credentials
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Fichier credentials introuvable: {CREDENTIALS_FILE}")
        return

    with open(CREDENTIALS_FILE) as f:
        creds = json.load(f)['installed']

    # Générer l'URL d'autorisation
    auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode({
        'client_id': creds['client_id'],
        'redirect_uri': 'http://localhost',
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'prompt': 'consent'  # Force nouveau refresh_token
    })

    print("\n" + "="*60)
    print("🔐 RENOUVELLEMENT TOKEN - coachdigitalparis@gmail.com")
    print("="*60)
    print("\n1. Ouvre ce lien dans ton navigateur :\n")
    print(auth_url)
    print("\n2. Connecte-toi avec coachdigitalparis@gmail.com")
    print("3. Autorise l'accès")
    print("4. Tu seras redirigé vers une URL comme :")
    print("   http://localhost/?code=XXXXXX&scope=...")
    print("\n5. Copie le 'code' de l'URL et colle-le ci-dessous :\n")

    code = input("Code d'autorisation: ").strip()

    if not code:
        print("❌ Code vide, abandon.")
        return

    # Échanger le code contre un token
    import requests
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost'
    })

    if response.status_code != 200:
        print(f"❌ Erreur: {response.text}")
        return

    token_data = response.json()
    token_data['account'] = 'coachdigitalparis@gmail.com'

    # Sauvegarder le token
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print(f"\n✅ Token renouvelé avec succès !")
    print(f"   Fichier: {TOKEN_FILE}")

if __name__ == '__main__':
    main()
