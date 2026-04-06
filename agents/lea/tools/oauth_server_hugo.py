#!/usr/bin/env python3
"""
Serveur OAuth pour Hugo — hugokorzec.pro@gmail.com
Nina accede au Gmail d'Hugo en tant qu'assistante (lecture + envoi).
"""
import json
import os
import sys
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'gmail-credentials.json')
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'gmail-token-hugokorzec.json')

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

with open(CREDENTIALS_FILE) as f:
    creds = json.load(f)['installed']

captured_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if 'code' in params:
            captured_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'''
            <html><head><title>Hugo Gmail OK</title></head>
            <body style="font-family:Arial;text-align:center;padding:50px;">
            <h1 style="color:green;">Hugo Gmail autorise pour Nina !</h1>
            <p>Tu peux fermer cet onglet.</p>
            </body></html>''')
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Erreur: pas de code</h1></body></html>')
    def log_message(self, format, *args):
        pass

def main():
    global captured_code
    print("\n" + "="*60)
    print("HUGO - AUTORISATION GMAIL - hugokorzec.pro@gmail.com")
    print("="*60)

    auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode({
        'client_id': creds['client_id'],
        'redirect_uri': 'http://localhost:8092',
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'prompt': 'consent',
        'login_hint': 'hugokorzec.pro@gmail.com'
    })

    print("\nOUVRE CE LIEN DANS TON NAVIGATEUR :\n")
    print(auth_url)
    print("\nATTENTION : connecte-toi avec hugokorzec.pro@gmail.com !")
    print("En attente sur http://localhost:8092 ...")

    server = HTTPServer(('0.0.0.0', 8092), OAuthHandler)
    server.timeout = 300

    while captured_code is None:
        server.handle_request()
    server.server_close()

    print("\nCode recu ! Echange contre un token...")

    response = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'code': captured_code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8092'
    })

    if response.status_code != 200:
        print(f"Erreur: {response.text}")
        return 1

    token_data = response.json()
    token_data['account'] = 'hugokorzec.pro@gmail.com'

    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print(f"\nTOKEN HUGO GENERE AVEC SUCCES !")
    print(f"Fichier: {TOKEN_FILE}")
    print("="*60)
    return 0

if __name__ == '__main__':
    sys.exit(main())
