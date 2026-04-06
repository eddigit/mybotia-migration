#!/usr/bin/env python3
"""
Script de gestion Google Calendar pour Coach Digital
Usage:
  python3 calendar.py list [jours]              # Liste les événements (défaut: 7 jours)
  python3 calendar.py add "titre" "date" "heure" [durée_min] [description]
  python3 calendar.py task "titre" "date"       # Ajoute une tâche (événement journée)
  python3 calendar.py today                     # Événements aujourd'hui
  python3 calendar.py week                      # Événements cette semaine
"""
import json
import requests
import sys
import os
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'gmail-token-coachdigital.json')
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, '..', 'credentials-coachdigitalparis@gmail.com.json')

def get_token():
    with open(TOKEN_FILE) as f:
        token = json.load(f)
    with open(CREDENTIALS_FILE) as f:
        creds = json.load(f)
        client = creds.get('installed') or creds.get('web')
    
    # Refresh if needed
    headers = {'Authorization': f'Bearer {token["access_token"]}'}
    test = requests.get('https://www.googleapis.com/calendar/v3/calendars/primary', headers=headers)
    
    if test.status_code == 401:
        response = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': client['client_id'],
            'client_secret': client['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token'
        })
        new_token = response.json()
        if 'access_token' in new_token:
            token['access_token'] = new_token['access_token']
            with open(TOKEN_FILE, 'w') as f:
                json.dump(token, f, indent=2)
    
    return token['access_token']

def list_events(days=7):
    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    now = datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + timedelta(days=days)).isoformat() + 'Z'
    
    resp = requests.get(
        f'https://www.googleapis.com/calendar/v3/calendars/primary/events',
        headers=headers,
        params={
            'timeMin': time_min,
            'timeMax': time_max,
            'singleEvents': True,
            'orderBy': 'startTime',
            'maxResults': 50
        }
    )
    
    events = resp.json().get('items', [])
    
    if not events:
        print(f"📅 Aucun événement dans les {days} prochains jours")
        return
    
    print(f"📅 {len(events)} événement(s) dans les {days} prochains jours:\n")
    
    current_date = None
    for event in events:
        start = event.get('start', {})
        date_str = start.get('dateTime', start.get('date', ''))
        
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            event_date = dt.strftime('%A %d/%m')
            event_time = dt.strftime('%H:%M')
        else:
            event_date = date_str
            event_time = "Journée"
        
        if event_date != current_date:
            current_date = event_date
            print(f"\n📆 {current_date}")
            print("-" * 40)
        
        summary = event.get('summary', 'Sans titre')
        print(f"  {event_time} - {summary}")

def add_event(title, date, time, duration=60, description=''):
    token = get_token()
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Parser la date et l'heure
    try:
        if '/' in date:
            day, month, year = date.split('/')
            if len(year) == 2:
                year = '20' + year
            date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        start_dt = datetime.fromisoformat(f"{date}T{time}:00")
        end_dt = start_dt + timedelta(minutes=int(duration))
    except Exception as e:
        print(f"❌ Erreur de date/heure: {e}")
        print("   Format attendu: date=JJ/MM/AAAA ou AAAA-MM-JJ, heure=HH:MM")
        return
    
    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Europe/Paris'
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Europe/Paris'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ]
        }
    }
    
    resp = requests.post(
        'https://www.googleapis.com/calendar/v3/calendars/primary/events',
        headers=headers,
        json=event
    )
    
    if resp.status_code == 200:
        created = resp.json()
        print(f"✅ Événement créé : {title}")
        print(f"   📅 {start_dt.strftime('%d/%m/%Y %H:%M')} - {end_dt.strftime('%H:%M')}")
        print(f"   🔗 {created.get('htmlLink', '')}")
    else:
        print(f"❌ Erreur: {resp.status_code} - {resp.text[:200]}")

def add_task(title, date):
    """Ajoute un événement sur toute la journée (tâche)"""
    token = get_token()
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    try:
        if '/' in date:
            day, month, year = date.split('/')
            if len(year) == 2:
                year = '20' + year
            date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except:
        pass
    
    event = {
        'summary': f"📋 {title}",
        'start': {'date': date},
        'end': {'date': date},
        'transparency': 'transparent'  # Ne bloque pas le calendrier
    }
    
    resp = requests.post(
        'https://www.googleapis.com/calendar/v3/calendars/primary/events',
        headers=headers,
        json=event
    )
    
    if resp.status_code == 200:
        print(f"✅ Tâche créée : {title}")
        print(f"   📅 {date}")
    else:
        print(f"❌ Erreur: {resp.status_code}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'list':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        list_events(days)
    elif cmd == 'today':
        list_events(1)
    elif cmd == 'week':
        list_events(7)
    elif cmd == 'add':
        if len(sys.argv) < 5:
            print("Usage: calendar.py add \"titre\" \"date\" \"heure\" [durée_min] [description]")
        else:
            title = sys.argv[2]
            date = sys.argv[3]
            time = sys.argv[4]
            duration = int(sys.argv[5]) if len(sys.argv) > 5 else 60
            desc = sys.argv[6] if len(sys.argv) > 6 else ''
            add_event(title, date, time, duration, desc)
    elif cmd == 'task':
        if len(sys.argv) < 4:
            print("Usage: calendar.py task \"titre\" \"date\"")
        else:
            add_task(sys.argv[2], sys.argv[3])
    else:
        print(f"Commande inconnue: {cmd}")
        print(__doc__)
