#!/usr/bin/env python3
"""
Envoi automatique d'email (sans confirmation interactive).
Usage: python3 send_email_auto.py "dest@email.com" "Sujet" "Corps HTML" [compte]
UNIQUEMENT pour les envois internes / à Gilles. PAS pour les clients.
"""
import json, base64, requests, sys, os

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
        print("❌ Erreur d'authentification")
        return None
    from_email = f"{account}@gmail.com" if "@" not in account else account
    headers_list = [
        f'From: {from_email}',
        f'To: {to}',
        f'Subject: =?UTF-8?B?{base64.b64encode(subject.encode()).decode()}?=',
        'MIME-Version: 1.0',
        'Content-Type: text/html; charset="UTF-8"'
    ]
    email_raw = '\n'.join(headers_list) + '\n\n' + body
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
        result = response.json()
        print(f"✅ Email envoyé ! ID: {result['id']}")
        return result
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 send_email_auto.py 'dest' 'sujet' 'corps' [compte]")
        sys.exit(1)
    account = sys.argv[4] if len(sys.argv) > 4 else "coachdigitalparis"
    send_email(sys.argv[1], sys.argv[2], sys.argv[3], account)
