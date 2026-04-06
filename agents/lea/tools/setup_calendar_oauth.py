#!/usr/bin/env python3
"""
Setup OAuth pour Google Calendar + Gmail - gilleskorzec@gmail.com
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Scopes complets : Gmail + Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

CREDENTIALS_FILE = 'credentials-gilleskorzec@gmail.com.json'
TOKEN_FILE = 'tools/gmail-token-gilleskorzec.json'

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Fichier {CREDENTIALS_FILE} introuvable")
        return
    
    print("🔐 OAuth pour gilleskorzec@gmail.com")
    print("📋 Scopes: gmail.readonly, gmail.send, calendar, calendar.events")
    
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    
    # Génère l'URL d'autorisation
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print(f"\n🌐 Ouvre cette URL :\n")
    print(auth_url)
    print(f"\n📋 Colle le code d'autorisation ici : ", end='')
    code = input().strip()
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    # Sauvegarde le token
    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': list(creds.scopes)
    }
    
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)
    
    print(f"\n✅ Token sauvegardé : {TOKEN_FILE}")

if __name__ == '__main__':
    main()
