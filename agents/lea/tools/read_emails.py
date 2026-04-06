#!/usr/bin/env python3
"""
read_emails.py v2.0 - Optimise pour OpenClaw (anti-timeout)
Listing = metadata only + parallele. Lecture complete = par ID uniquement.

Usage:
  python3 read_emails.py [max] [query] [account]
  python3 read_emails.py id:MSG_ID [account]
"""
import json, base64, requests, sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MAX = 20
ABSOLUTE_MAX = 50
WORKERS = 5

def refresh_token_if_needed(account_name):
    clean = account_name.replace("@gmail.com", "")
    token_file = os.path.join(SCRIPT_DIR, f'gmail-token-{clean}.json')
    creds_file = None
    for c in [
        os.path.join(SCRIPT_DIR, '..', f'credentials-{account_name}.json'),
        os.path.join(SCRIPT_DIR, '..', f'credentials-{clean}.json'),
        os.path.join(SCRIPT_DIR, 'gmail-credentials.json'),
    ]:
        if os.path.exists(c):
            creds_file = c
            break
    if not os.path.exists(token_file):
        print(f"Error: Token file {token_file} not found.")
        return None
    if not creds_file:
        print(f"Error: Credentials not found for {account_name}.")
        return None
    with open(token_file) as f:
        token = json.load(f)
    with open(creds_file) as f:
        cd = json.load(f)
        creds = cd.get('installed') or cd.get('web')
    if not creds:
        print("Error: Invalid credentials format.")
        return None
    test = requests.get(
        'https://gmail.googleapis.com/gmail/v1/users/me/profile',
        headers={'Authorization': f'Bearer {token["access_token"]}'},
        timeout=10)
    if test.status_code == 401:
        resp = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token'
        }, timeout=10)
        new = resp.json()
        if 'access_token' not in new:
            err = new.get('error', '?')
            desc = new.get('error_description', '')
            print(f"Token refresh failed: {err} - {desc}")
            if err == 'invalid_grant':
                print("Refresh token mort. Projet Google Cloud en mode Testing?")
                print("Fix: passer en Production dans Google Cloud Console")
            return None
        token['access_token'] = new['access_token']
        if 'refresh_token' in new:
            token['refresh_token'] = new['refresh_token']
        with open(token_file, 'w') as f:
            json.dump(token, f, indent=2)
    return token['access_token']

def get_header(headers, name):
    for h in headers:
        if h['name'].lower() == name.lower():
            return h['value']
    return None

def fetch_metadata(msg_id, access_token):
    try:
        r = requests.get(
            f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}',
            headers={'Authorization': f'Bearer {access_token}'},
            params={'format': 'metadata', 'metadataHeaders': ['From','To','Subject','Date']},
            timeout=15)
        if r.status_code == 200:
            d = r.json()
            h = d.get('payload', {}).get('headers', [])
            return {
                'id': msg_id,
                'from': get_header(h, 'From'),
                'to': get_header(h, 'To'),
                'subject': get_header(h, 'Subject'),
                'date': get_header(h, 'Date'),
                'snippet': d.get('snippet', ''),
            }
    except:
        pass
    return None

def list_emails(max_results=DEFAULT_MAX, query=None, account_name="coachdigitalparis"):
    access_token = refresh_token_if_needed(account_name)
    if not access_token:
        return []
    if max_results > ABSOLUTE_MAX:
        print(f"Limite reduite de {max_results} a {ABSOLUTE_MAX}.")
        max_results = ABSOLUTE_MAX
    params = {'maxResults': max_results}
    if query:
        params['q'] = query
    r = requests.get(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages',
        headers={'Authorization': f'Bearer {access_token}'},
        params=params, timeout=15)
    if r.status_code != 200:
        print(f"Erreur {r.status_code}: {r.text}")
        return []
    messages = r.json().get('messages', [])
    if not messages:
        print("Aucun email trouve.")
        return []
    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(fetch_metadata, m['id'], access_token): m['id'] for m in messages}
        for f in as_completed(futs):
            res = f.result()
            if res:
                results.append(res)
    order = [m['id'] for m in messages]
    results.sort(key=lambda x: order.index(x['id']))
    return results

def extract_body(payload):
    if 'body' in payload and payload['body'].get('data'):
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
    if 'parts' in payload:
        for p in payload['parts']:
            if p['mimeType'] == 'text/plain' and p['body'].get('data'):
                return base64.urlsafe_b64decode(p['body']['data']).decode('utf-8', errors='ignore')
            if 'parts' in p:
                r = extract_body(p)
                if r:
                    return r
    return ""

def get_email_content_by_id(message_id, account_name="coachdigitalparis"):
    access_token = refresh_token_if_needed(account_name)
    if not access_token:
        return None
    r = requests.get(
        f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}',
        headers={'Authorization': f'Bearer {access_token}'},
        params={'format': 'full'}, timeout=30)
    if r.status_code != 200:
        print(f"Erreur {r.status_code}: {r.text}")
        return None
    d = r.json()
    h = d['payload'].get('headers', [])
    return {
        'id': message_id,
        'from': get_header(h, 'From'),
        'to': get_header(h, 'To'),
        'subject': get_header(h, 'Subject'),
        'date': get_header(h, 'Date'),
        'snippet': d.get('snippet', ''),
        'body': extract_body(d['payload'])
    }

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].startswith("id:"):
        mid = sys.argv[1].split(":", 1)[1]
        acct = sys.argv[2] if len(sys.argv) > 2 else "coachdigitalparis"
        email = get_email_content_by_id(mid, acct)
        if email:
            print(json.dumps(email, indent=2, ensure_ascii=False))
        else:
            print(f"Email {mid} not found or error.")
    else:
        mx = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MAX
        q = sys.argv[2] if len(sys.argv) > 2 else None
        acct = sys.argv[3] if len(sys.argv) > 3 else "coachdigitalparis"
        emails = list_emails(mx, q, acct)
        print(f"\n{len(emails)} email(s) trouves dans {acct}:\n")
        for i, e in enumerate(emails, 1):
            print(f"--- Email {i} [ID: {e['id']}] ---")
            print(f"De: {e['from']}")
            print(f"A: {e['to']}")
            print(f"Sujet: {e['subject']}")
            print(f"Date: {e['date']}")
            print(f"Apercu: {e['snippet']}")
            print()
        if emails:
            print(f"Pour lire un email complet: python3 tools/read_emails.py id:MESSAGE_ID {acct}")