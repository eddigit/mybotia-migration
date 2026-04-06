import os
from google_auth_oauthlib.flow import InstalledAppFlow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'gmail-credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'gmail-token-gilleskorzec.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

if not os.path.exists(CREDENTIALS_FILE):
    print(f"ERREUR CRITIQUE: Le fichier {CREDENTIALS_FILE} n'existe pas !")
    exit(1)

print(f"Authentification utilisant : {CREDENTIALS_FILE}")
flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=8090, open_browser=False)

with open(TOKEN_FILE, 'w') as token:
    token.write(creds.to_json())

print(f"✅ Token généré avec succès ici : {TOKEN_FILE}")
