#!/usr/bin/env python3
"""
Serveur OAuth qui capture automatiquement le code de retour Google.
Lance ce script, ouvre le lien affiché, autorise, et c'est fait !
"""
import json
import os
import sys
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'gmail-credentials.json')
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'gmail-token-leacoachdigital.json')

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

# Charger credentials
with open(CREDENTIALS_FILE) as f:
    creds = json.load(f)['installed']

captured_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_code
        
        # Parser l'URL pour extraire le code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        if 'code' in params:
            captured_code = params['code'][0]
            
            # Répondre avec une page de succès
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'''
            <html>
            <head><title>Autorisation reussie!</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: green;">Autorisation reussie!</h1>
                <p>Tu peux fermer cet onglet et retourner au terminal.</p>
                <p>Le token Gmail est en cours de generation...</p>
            </body>
            </html>
            ''')
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Erreur: pas de code</h1></body></html>')
    
    def log_message(self, format, *args):
        pass  # Silence les logs

def main():
    global captured_code
    
    print("\n" + "="*60)
    print("🔐 RENOUVELLEMENT TOKEN GMAIL - leacoachdigital@gmail.com")
    print("="*60)
    
    # Générer l'URL d'autorisation
    auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode({
        'client_id': creds['client_id'],
        'redirect_uri': 'http://localhost:8090',
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'prompt': 'consent'
    })
    
    print("\n📋 OUVRE CE LIEN DANS TON NAVIGATEUR :\n")
    print(auth_url)
    print("\n⏳ En attente de l'autorisation...")
    print("   (Le serveur écoute sur http://localhost:8090)")
    
    # Démarrer le serveur
    server = HTTPServer(('localhost', 8090), OAuthHandler)
    server.timeout = 300  # 5 min timeout
    
    # Attendre une seule requête
    while captured_code is None:
        server.handle_request()
    
    server.server_close()
    
    print("\n✅ Code reçu ! Échange contre un token...")
    
    # Échanger le code contre un token
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'code': captured_code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8090'
    })
    
    if response.status_code != 200:
        print(f"❌ Erreur: {response.text}")
        return 1
    
    token_data = response.json()
    token_data['account'] = 'leacoachdigital@gmail.com'
    
    # Sauvegarder le token
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)
    
    print(f"\n✅ TOKEN RENOUVELÉ AVEC SUCCÈS !")
    print(f"   Fichier: {TOKEN_FILE}")
    print("\n" + "="*60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
