#!/usr/bin/env python3
"""
Envoi email avec pièce jointe via Gmail API
Usage: python3 send_email_with_attachment.py "dest" "sujet" "corps" "fichier" [compte]
"""
import json, base64, requests, sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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
        response = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token'
        })
        new_token = response.json()
        if 'access_token' not in new_token:
            print(f"❌ Erreur refresh: {new_token}")
            return None
        token['access_token'] = new_token['access_token']
        with open(token_file, 'w') as f:
            json.dump(token, f, indent=2)
    
    return token['access_token']

def send(to, subject, body, attachment_path, account="coachdigitalparis"):
    access_token = refresh_token(account)
    if not access_token:
        return False
    
    msg = MIMEMultipart()
    msg['To'] = to
    msg['From'] = f'{account}@gmail.com'
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Pièce jointe
    filename = os.path.basename(attachment_path)
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    msg.attach(part)
    
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    
    result = requests.post(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={'raw': raw}
    )
    
    if result.status_code == 200:
        print(f"✅ Email envoyé à {to} avec PJ: {filename}")
        return True
    else:
        print(f"❌ Erreur {result.status_code}: {result.text}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python3 send_email_with_attachment.py dest sujet corps fichier [compte]")
        sys.exit(1)
    
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4]
    account = sys.argv[5] if len(sys.argv) > 5 else "coachdigitalparis"
    
    send(to, subject, body, attachment, account)
