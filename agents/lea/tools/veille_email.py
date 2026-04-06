#!/usr/bin/env python3
"""
Envoi automatique d'email de veille (cron uniquement, pas d'interactivité).
Usage: python3 veille_email.py "destinataire" "sujet" "corps_html"
"""
import json, base64, requests, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def refresh_token(account="coachdigitalparis"):
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
        resp = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token'
        })
        new_token = resp.json()
        token['access_token'] = new_token['access_token']
        with open(token_file, 'w') as f:
            json.dump(token, f)
    return token['access_token']

def send(to, subject, body_html, account="coachdigitalparis"):
    access_token = refresh_token(account)
    from_email = f"{account}@gmail.com" if "@" not in account else account
    
    email_raw = '\r\n'.join([
        f'From: {from_email}',
        f'To: {to}',
        f'Subject: =?UTF-8?B?{base64.b64encode(subject.encode()).decode()}?=',
        'MIME-Version: 1.0',
        'Content-Type: text/html; charset=UTF-8',
        '',
        body_html
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
        print(f"✅ Email envoyé à {to}")
        return True
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 veille_email.py dest sujet corps_html")
        sys.exit(1)
    send(sys.argv[1], sys.argv[2], sys.argv[3])
