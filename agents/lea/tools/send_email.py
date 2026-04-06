#!/usr/bin/env python3
"""
Script d'envoi d'email pour Coach Digital via Gmail API
VERROU DE SÉCURITÉ : Exige un code de confirmation manuel avant envoi.
Usage: python3 send_email.py "destinataire@email.com" "Sujet" "Corps du message" [compte]
"""
import json
import base64
import requests
import sys
import os
import random
import string

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def refresh_token_if_needed(account="coachdigitalparis"):
    """Rafraîchit le token si expiré"""
    token_file = os.path.join(SCRIPT_DIR, f'gmail-token-{account.replace("@gmail.com", "")}.json')
    
    with open(token_file) as f:
        token = json.load(f)
    with open(os.path.join(SCRIPT_DIR, 'gmail-credentials.json')) as f:
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
        if 'access_token' not in new_token:
            print(f"❌ Erreur refresh token: {new_token}")
            return None
        token['access_token'] = new_token['access_token']
        with open(token_file, 'w') as f:
            json.dump(token, f, indent=2)
    
    return token['access_token']

def send_email(to, subject, body, account="coachdigitalparis", cc=None, bcc=None):
    """Envoie un email - AVEC CONFIRMATION OBLIGATOIRE"""
    
    # ============================================
    # 🛑 VERROU DE SÉCURITÉ - CONFIRMATION MANUELLE
    # ============================================
    
    print("\n" + "="*60)
    print("🛑 VERROU DE SÉCURITÉ — CONFIRMATION REQUISE")
    print("="*60)
    print("\n📧 BROUILLON EMAIL À ENVOYER :\n")
    print(f"   De: {account}@gmail.com")
    print(f"   À: {to}")
    if cc:
        print(f"   Cc: {cc}")
    print(f"   Objet: {subject}")
    print(f"\n   --- Message ---")
    for line in body.split('\n'):
        print(f"   {line}")
    print(f"   --- Fin ---\n")
    
    # Générer code de confirmation
    code = ''.join(random.choices(string.digits, k=6))
    
    print("="*60)
    print(f"⚠️  Pour envoyer, tape ce code : {code}")
    print("   (ou tape 'ANNULER' pour annuler)")
    print("="*60)
    
    try:
        confirmation = input("\n👉 Code de confirmation : ").strip()
    except EOFError:
        print("\n❌ BLOQUÉ : Aucune confirmation reçue. Email NON envoyé.")
        print("   → L'envoi d'email nécessite une validation MANUELLE de Gilles.")
        return None
    
    if confirmation.upper() == 'ANNULER':
        print("\n❌ Envoi ANNULÉ par l'utilisateur.")
        return None
    
    if confirmation != code:
        print(f"\n❌ BLOQUÉ : Code incorrect. Email NON envoyé.")
        print(f"   Code attendu: {code}")
        print(f"   Code reçu: {confirmation}")
        return None
    
    print("\n✅ Code confirmé. Envoi en cours...")
    
    # ============================================
    # Envoi réel
    # ============================================
    
    access_token = refresh_token_if_needed(account)
    if not access_token:
        print("❌ Erreur d'authentification")
        return None
    
    # Déterminer l'adresse d'envoi
    from_email = f"{account}@gmail.com" if "@" not in account else account
    
    # Build headers
    headers_list = [
        f'From: {from_email}',
        f'To: {to}',
        f'Subject: =?UTF-8?B?{base64.b64encode(subject.encode()).decode()}?=',
        'Content-Type: text/plain; charset="UTF-8"'
    ]
    if cc:
        headers_list.append(f'Cc: {cc}')
    if bcc:
        headers_list.append(f'Bcc: {bcc}')
    
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
        print("Usage: python3 send_email.py 'destinataire@email.com' 'Sujet' 'Corps du message' [compte]")
        print("       compte = coachdigitalparis (défaut) ou gilleskorzec")
        sys.exit(1)
    
    account = sys.argv[4] if len(sys.argv) > 4 else "coachdigitalparis"
    send_email(sys.argv[1], sys.argv[2], sys.argv[3], account)
