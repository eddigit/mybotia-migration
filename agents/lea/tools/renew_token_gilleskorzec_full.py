#!/usr/bin/env python3
"""
Renouvelle le token Gmail gilleskorzec avec TOUS les scopes
Version avec serveur HTTP pour capturer le code OAuth
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.settings.basic'
]

CREDENTIALS_FILE = os.path.expanduser('~/.openclaw/workspace/tools/gmail-credentials.json')
TOKEN_FILE = os.path.expanduser('~/.openclaw/workspace/tools/gmail-token-gilleskorzec.json')
REDIRECT_URI = 'http://localhost:8091'

authorization_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code
        query = parse_qs(urlparse(self.path).query)
        
        if 'code' in query:
            authorization_code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <html><body style="font-family:Arial;text-align:center;padding:50px;">
                <h1>Autorisation reussie!</h1>
                <p>Tu peux fermer cette fenetre.</p>
                </body></html>
            ''')
            print(f"\n✅ Code reçu!")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Erreur: pas de code')
    
    def log_message(self, format, *args):
        pass

def main():
    print("🔐 Renouvellement token Gmail gilleskorzec@gmail.com (scopes complets)")
    print()
    
    with open(CREDENTIALS_FILE, 'r') as f:
        creds_data = json.load(f)
    
    client_id = creds_data['installed']['client_id']
    client_secret = creds_data['installed']['client_secret']
    
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    
    print("📋 Ouvre cette URL dans ton navigateur:")
    print()
    print(auth_url)
    print()
    print("⏳ En attente sur http://localhost:8091 ...")
    
    server = HTTPServer(('localhost', 8091), OAuthHandler)
    server.timeout = 300
    
    while authorization_code is None:
        server.handle_request()
    
    server.server_close()
    
    # Échanger le code contre un token
    flow.fetch_token(code=authorization_code)
    creds = flow.credentials
    
    token_data = {
        'access_token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': list(creds.scopes) if creds.scopes else SCOPES
    }
    
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)
    
    print(f"✅ Token sauvegardé: {TOKEN_FILE}")
    print("🎉 Scopes complets activés!")

if __name__ == '__main__':
    main()
