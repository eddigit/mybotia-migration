#!/usr/bin/env python3
"""Ajouter le scope Google Drive au token coachdigitalparis.

Étape 1: Lancer ce script → il affiche une URL
Étape 2: Gilles ouvre l'URL dans son navigateur → autorise → copie le code
Étape 3: Coller le code ici

Usage: python3 tools/google_drive_auth.py
"""
import json, urllib.parse, urllib.request, sys, os

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "gmail-token-coachdigitalparis.json")

with open(TOKEN_FILE) as f:
    t = json.load(f)

CLIENT_ID = t["client_id"]
CLIENT_SECRET = t["client_secret"]

SCOPES = " ".join([
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/drive.file",  # NOUVEAU - upload de fichiers
])

# Étape 1: Générer l'URL d'autorisation
auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": CLIENT_ID,
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "response_type": "code",
    "scope": SCOPES,
    "access_type": "offline",
    "prompt": "consent",
})

print("=" * 60)
print("AUTORISATION GOOGLE DRIVE")
print("=" * 60)
print()
print("1. Ouvre cette URL dans ton navigateur :")
print()
print(auth_url)
print()
print("2. Connecte-toi avec coachdigitalparis@gmail.com")
print("3. Autorise l'accès")
print("4. Copie le code et colle-le ci-dessous")
print()

code = input("Code d'autorisation: ").strip()

if not code:
    print("❌ Pas de code fourni")
    sys.exit(1)

# Étape 2: Échanger le code contre un token
data = urllib.parse.urlencode({
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
with urllib.request.urlopen(req) as resp:
    token_data = json.loads(resp.read())

if "error" in token_data:
    print(f"❌ Erreur: {token_data}")
    sys.exit(1)

# Mettre à jour le fichier token
t["access_token"] = token_data["access_token"]
if "refresh_token" in token_data:
    t["refresh_token"] = token_data["refresh_token"]
t["scope"] = SCOPES

with open(TOKEN_FILE, "w") as f:
    json.dump(t, f, indent=2)

print()
print("✅ Token mis à jour avec le scope Drive !")
print(f"   Fichier: {TOKEN_FILE}")
