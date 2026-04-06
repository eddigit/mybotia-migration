from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Scopes nécessaires (lecture + envoi)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

# Chemins des fichiers
CREDENTIALS = 'tools/credentials-gilleskorzec@gmail.com.json'
TOKEN = 'tools/gmail-token-gilleskorzec.json'

def main():
    if not os.path.exists(CREDENTIALS):
        print(f"ERREUR: Le fichier {CREDENTIALS} est introuvable !")
        return

    print("Lancement de l'authentification...")
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
    
    # On lance le serveur local pour récupérer le token
    creds = flow.run_local_server(port=8090, open_browser=False)
    
    # On sauvegarde le nouveau token
    with open(TOKEN, 'w') as token_file:
        token_file.write(creds.to_json())
    
    print(f"\n✅ SUCCÈS ! Nouveau token sauvegardé dans {TOKEN}")

if __name__ == '__main__':
    main()
