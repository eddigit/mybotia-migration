#!/usr/bin/env python3
"""
Script d'envoi d'email avec pièce jointe via Gmail API
Usage: python3 send_email_attachment.py "dest@email.com" "Sujet" "Corps" "chemin/fichier.pdf" [compte]
Compte: coachdigital (défaut) ou gilleskorzec
"""
import json
import base64
import requests
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_token_and_email(account='coachdigital'):
    """Récupère le token et l'email selon le compte"""
    if account == 'gilleskorzec':
        token_file = 'gmail-token-gilleskorzec.json'
        creds_file = os.path.join(SCRIPT_DIR, '..', 'credentials-gilleskorzec@gmail.com.json')
        from_email = 'gilleskorzec@gmail.com'
    else:
        token_file = 'gmail-token-coachdigital.json'
        creds_file = os.path.join(SCRIPT_DIR, 'gmail-credentials.json')
        from_email = 'coachdigitalparis@gmail.com'
    
    return token_file, creds_file, from_email

def refresh_token_if_needed(account='coachdigital'):
    """Rafraîchit le token si expiré"""
    token_file, creds_file, _ = get_token_and_email(account)
    
    with open(os.path.join(SCRIPT_DIR, token_file)) as f:
        token = json.load(f)
    with open(creds_file) as f:
        creds = json.load(f)['installed']
    
    # Test token validity
    test = requests.get(
        'https://gmail.googleapis.com/gmail/v1/users/me/profile',
        headers={'Authorization': f'Bearer {token["access_token"]}'}
    )
    
    if test.status_code == 401:
        # Refresh token
        response = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token'
        })
        new_token = response.json()
        token['access_token'] = new_token['access_token']
        with open(os.path.join(SCRIPT_DIR, token_file), 'w') as f:
            json.dump(token, f, indent=2)
    
    return token['access_token']

def send_email_with_attachment(to, subject, body, attachment_path=None, account='coachdigital'):
    """Envoie un email avec pièce jointe optionnelle"""
    access_token = refresh_token_if_needed(account)
    _, _, from_email = get_token_and_email(account)
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    
    # Body
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Attachment
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)
        print(f"📎 Pièce jointe: {filename}")
    
    # Encode and send
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    
    response = requests.post(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={'raw': raw}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Email envoyé depuis {from_email} ! ID: {result['id']}")
        return result
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 send_email_attachment.py 'dest@email.com' 'Sujet' 'Corps' ['fichier.pdf'] [compte]")
        print("Compte: coachdigital (défaut) ou gilleskorzec")
        sys.exit(1)
    
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    account = sys.argv[5] if len(sys.argv) > 5 else 'coachdigital'
    
    send_email_with_attachment(to, subject, body, attachment, account)
