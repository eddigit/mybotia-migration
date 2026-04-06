#!/usr/bin/env python3
"""Envoi direct email veille (cron) — bypass verrou interactif, destiné à Gilles uniquement."""
import json, base64, requests, sys, os
from email.mime.text import MIMEText

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def refresh_token(account):
    token_file = os.path.join(SCRIPT_DIR, f'gmail-token-{account}.json')
    with open(token_file) as f:
        token = json.load(f)
    with open(os.path.join(SCRIPT_DIR, 'gmail-credentials.json')) as f:
        creds = json.load(f)['installed']
    test = requests.get('https://gmail.googleapis.com/gmail/v1/users/me/profile',
                        headers={'Authorization': f'Bearer {token["access_token"]}'})
    if test.status_code == 401:
        r = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': creds['client_id'], 'client_secret': creds['client_secret'],
            'refresh_token': token['refresh_token'], 'grant_type': 'refresh_token'
        })
        new = r.json()
        if 'access_token' not in new:
            print(f"❌ Refresh failed: {new}"); return None
        token['access_token'] = new['access_token']
        with open(token_file, 'w') as f:
            json.dump(token, f, indent=2)
    return token['access_token']

def send(to, subject, body, account='leacoachdigital'):
    access = refresh_token(account)
    if not access: return
    from_email = f"{account}@gmail.com"
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['to'] = to; msg['from'] = from_email; msg['subject'] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    r = requests.post(f'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
                      headers={'Authorization': f'Bearer {access}', 'Content-Type': 'application/json'},
                      json={'raw': raw})
    if r.status_code == 200:
        print(f"✅ Email envoyé à {to} depuis {from_email}")
    else:
        print(f"❌ Erreur {r.status_code}: {r.text}")

if __name__ == '__main__':
    to, subject, body = sys.argv[1], sys.argv[2], sys.argv[3]
    account = sys.argv[4] if len(sys.argv) > 4 else 'leacoachdigital'
    send(to, subject, body, account)
