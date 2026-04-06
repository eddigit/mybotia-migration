
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

def setup_oauth_gilleskorzec():
    token_file = 'tools/gmail-token-gilleskorzec.json'
    credentials_file = 'credentials-gilleskorzec@gmail.com.json'

    creds = None
    # The token file is now a JSON file to store the token in a human-readable format
    if os.path.exists(token_file):
        with open(token_file, 'r') as token:
            # Use google.oauth2.credentials.Credentials to load the token
            token_data = json.load(token)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                print(f"Error: {credentials_file} not found.")
                return

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            # Generate the authorization URL and prompt the user to open it
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"Please go to this URL and authorize access: {auth_url}")
            code = input("Enter the authorization code: ")
            flow.fetch_token(code=code)
            creds = flow.credentials
        
        # Save the credentials to the token file in JSON format
        with open(token_file, 'w') as token:
            json.dump(creds.to_json(), token)
    return creds

if __name__ == '__main__':
    import json
    print("Starting OAuth flow for gilleskorzec@gmail.com...")
    setup_oauth_gilleskorzec()
    print("OAuth flow completed. Token saved to tools/gmail-token-gilleskorzec.json")
