#!/usr/bin/env python3
"""
Test envoi email via Brevo API
"""

import requests
import json

# Clé API Brevo
with open('/home/gilles/.openclaw/workspace-nina/config/brevo_api_key.txt', 'r') as f:
    API_KEY = f.read().strip()

url = "https://api.brevo.com/v3/smtp/email"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": API_KEY
}

payload = {
    "sender": {
        "name": "Hugo Korzec",
        "email": "hugokorzec.pro@gmail.com"
    },
    "to": [
        {
            "email": "hugokorzec.pro@gmail.com",
            "name": "Hugo TEST"
        }
    ],
    "subject": "Test Brevo - Campagne Avocats Paris",
    "htmlContent": """
    <html>
        <body>
            <h1>Test d'envoi Brevo</h1>
            <p>Ceci est un test d'envoi via l'API Brevo.</p>
            <p>Si vous recevez cet email, la configuration fonctionne.</p>
            <p><strong>Prochaine étape :</strong> Envoi des 200 emails demain matin.</p>
            <p>Cordialement,<br>Nina</p>
        </body>
    </html>
    """
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        print("\n✅ Email envoyé avec succès !")
        print(f"Message ID: {response.json().get('messageId')}")
    else:
        print(f"\n❌ Erreur: {response.json()}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
