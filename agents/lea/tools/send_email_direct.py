#!/usr/bin/env python3
"""Envoi direct d'email sans verrou de sécurité"""
import json
import base64
import requests
import os
from email.mime.text import MIMEText

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def refresh_and_send(to, subject, body, account="gilleskorzec"):
    token_file = os.path.join(SCRIPT_DIR, f'gmail-token-{account}.json')
    
    with open(token_file) as f:
        token = json.load(f)
    with open(os.path.join(SCRIPT_DIR, 'gmail-credentials.json')) as f:
        creds = json.load(f)['installed']
    
    # Refresh token
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': token['refresh_token'],
        'grant_type': 'refresh_token'
    })
    new_token = response.json()
    token['access_token'] = new_token['access_token']
    
    # Create message
    message = MIMEText(body, 'plain', 'utf-8')
    message['To'] = to
    message['From'] = f'{account}@gmail.com'
    message['Subject'] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    # Send
    result = requests.post(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
        headers={'Authorization': f'Bearer {token["access_token"]}', 'Content-Type': 'application/json'},
        json={'raw': raw}
    )
    
    if result.status_code == 200:
        print(f"✅ Email envoyé avec succès !")
        print(f"   Message ID: {result.json()['id']}")
        return True
    else:
        print(f"❌ Erreur: {result.status_code}")
        print(result.text)
        return False

if __name__ == '__main__':
    to = "direction@espacesmimont.org"
    subject = "Incident grave et inacceptable — Accueil Espaces Mimont"
    body = """Monsieur Varlet,

Je me permets de vous contacter suite à un incident très désagréable survenu aujourd'hui aux Espaces Mimont.

Je fréquente régulièrement votre établissement depuis plusieurs mois. J'y viens toujours accompagné de mon fils de 12 ans, qui est calme, reste sur son téléphone et n'a jamais causé le moindre problème. Jusqu'à présent, tout s'est toujours très bien passé avec vos équipes — aucune règle ne m'a jamais été opposée.

Aujourd'hui, je me suis présenté pour prendre un abonnement mensuel. J'ai été reçu par un jeune homme dont l'attitude était désagréable et totalement inadmissible.

Il m'a humilié publiquement, devant mon fils de 12 ans, devant les personnes à l'accueil, et devant d'autres personnes qui travaillaient sur place. Tout le monde a assisté à la scène. Il m'a fait comprendre de manière abrupte que je n'avais pas le droit d'accès parce que mon enfant m'accompagnait, alors que JAMAIS cette règle ne m'a été appliquée auparavant.

Qu'il existe des règles, soit. Mais pourquoi n'ont-elles JAMAIS été appliquées lors de mes précédentes visites ? Pourquoi ce traitement aujourd'hui, alors que je venais justement pour prendre un abonnement mensuel ?

Au-delà du ton employé, cette situation m'a mis dans un embarras considérable. J'avais organisé ma journée de travail pour venir travailler chez vous. Je me suis retrouvé dehors avec mes deux sacs, mon enfant de 12 ans, et contraint de tout réorganiser à la dernière minute.

La manière dont cet employé s'est comporté est inacceptable :
- Ton déplacé et méprisant
- Aucune explication claire ou pédagogique
- Humiliation publique devant mon enfant et devant témoins
- Application brutale d'une règle qui n'avait jamais été mentionnée

Je souhaite obtenir des réponses claires :
1. Quelle est la règle exacte concernant l'accès avec un enfant ?
2. Pourquoi n'ai-je JAMAIS été informé de cette règle lors de mes précédentes visites ?
3. Qui était ce membre de votre équipe et quelles mesures comptez-vous prendre face à son comportement ?
4. Comment comptez-vous gérer cette situation ?

J'appréciais vraiment vos espaces et je venais justement pour devenir membre régulier. Après ce traitement inadmissible, j'attends des explications.

Dans l'attente de votre retour,

Cordialement,
Gilles Korzec
+33 6 52 34 51 80"""
    
    refresh_and_send(to, subject, body)
