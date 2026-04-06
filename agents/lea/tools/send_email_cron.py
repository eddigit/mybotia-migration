#!/usr/bin/env python3
"""
Script d'envoi d'email pour tâches CRON automatiques (sans verrou interactif).
Usage: python3 send_email_cron.py "destinataire@email.com" "Sujet" "Corps du message" [compte]
"""
import json
import base64
import requests
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def refresh_token_if_needed(account="coachdigitalparis"):
    token_file = os.path.join(SCRIPT_DIR, f'gmail-token-{account.replace("@gmail.com", "")}.json')
    with open(token_file) as f:
        token = json.load(f)
    with open(os.path.join(SCRIPT_DIR, 'gmail-credentials.json')) as f:
        creds = json.load(f)['installed']
    test = requests.get(
        'https://gmail.googleapis.com/gmail/v1/users/me/profile',
        headers={'Authorization': f'Bearer {token["access_token"]}'}
    )
    if test.status_code == 401:
        response = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token'
        })
        new_token = response.json()
        if 'access_token' not in new_token:
            print(f"❌ Erreur refresh token: {new_token}")
            return None
        token['access_token'] = new_token['access_token']
        with open(token_file, 'w') as f:
            json.dump(token, f, indent=2)
    return token['access_token']

def send_email(to, subject, body, account="coachdigitalparis"):
    access_token = refresh_token_if_needed(account)
    if not access_token:
        return None
    sender = f"{account}@gmail.com" if "@" not in account else account
    account_key = account.replace("@gmail.com", "")
    email_raw = '\r\n'.join([
        f'From: {sender}',
        f'To: {to}',
        f'Subject: =?UTF-8?B?{base64.b64encode(subject.encode()).decode()}?=',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
        '',
        base64.b64encode(body.encode()).decode()
    ])
    message = base64.urlsafe_b64encode(email_raw.encode()).decode()
    response = requests.post(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={'raw': message}
    )
    if response.status_code == 200:
        msg_id = response.json().get('id', 'N/A')
        print(f"✅ Email envoyé à {to} (ID: {msg_id})")
        return msg_id
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 send_email_cron.py 'dest' 'sujet' 'corps' [compte]")
        sys.exit(1)
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    account = sys.argv[4] if len(sys.argv) > 4 else "coachdigitalparis"
    send_email(to, subject, body, account)
