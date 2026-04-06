import os
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

flow = InstalledAppFlow.from_client_secrets_file('credentials-gilleskorzec@gmail.com.json', SCOPES)
creds = flow.run_local_server(port=8090, open_browser=False)

with open('tools/gmail-token-gilleskorzec.json', 'w') as f:
    f.write(creds.to_json())

print('Token sauvegardé dans tools/gmail-token-gilleskorzec.json')
