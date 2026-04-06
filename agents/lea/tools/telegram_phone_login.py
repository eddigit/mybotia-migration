#!/usr/bin/env python3
"""
Telegram Login par numéro de téléphone + code + 2FA
Étape 1 : Envoie le code SMS/Telegram
Étape 2 : Attend le code dans un fichier
Étape 3 : Entre le 2FA automatiquement
"""

import asyncio
import os
import sys
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

API_ID = 32146463
API_HASH = 'edeffff2c2cde22368b2d2183d6f0fe9'
SESSION_DIR = '/home/gilles/.openclaw/workspace/tools'
SESSION_FILE = os.path.join(SESSION_DIR, 'telegram_session')
PHONE = '+33652345180'  # Numéro de Gilles
PASSWORD_2FA = '$$Reussite888!!'
CODE_FILE = os.path.join(SESSION_DIR, 'telegram_code.txt')

# Nettoyer
for f in [SESSION_FILE + '.session', CODE_FILE]:
    if os.path.exists(f):
        os.remove(f)
        print(f"🗑️ Supprimé: {f}")

async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Déjà connecté : {me.first_name} ({me.phone})")
        await client.disconnect()
        return
    
    # Étape 1 : Envoyer le code
    print(f"📱 Envoi du code de vérification à {PHONE}...")
    result = await client.send_code_request(PHONE)
    phone_code_hash = result.phone_code_hash
    print(f"✅ Code envoyé ! (hash: {phone_code_hash[:10]}...)")
    print(f"📲 Tu vas recevoir un code sur Telegram ou par SMS")
    print(f"")
    print(f"⏳ J'attends que tu écrives le code dans : {CODE_FILE}")
    print(f"   Ou passe-le en argument : python3 {sys.argv[0]} <CODE>")
    
    # Sauvegarder le hash pour la 2ème étape
    with open(os.path.join(SESSION_DIR, 'telegram_code_hash.txt'), 'w') as f:
        f.write(phone_code_hash)
    
    # Attendre le code (5 minutes max)
    code = None
    for i in range(60):  # 5 minutes
        if os.path.exists(CODE_FILE):
            with open(CODE_FILE, 'r') as f:
                code = f.read().strip()
            if code:
                print(f"📋 Code lu : {code}")
                break
        time.sleep(5)
        if i % 6 == 0 and i > 0:
            print(f"⏳ Toujours en attente du code... ({i*5}s)")
    
    if not code:
        print("❌ Timeout — pas de code reçu en 5 minutes")
        await client.disconnect()
        return
    
    # Étape 2 : Entrer le code
    try:
        print(f"🔑 Saisie du code {code}...")
        await client.sign_in(PHONE, code, phone_code_hash=phone_code_hash)
        me = await client.get_me()
        print(f"✅ CONNECTÉ ! {me.first_name} ({me.phone})")
        await client.disconnect()
        return
    except SessionPasswordNeededError:
        print(f"🔐 2FA requis — saisie du mot de passe...")
        try:
            await client.sign_in(password=PASSWORD_2FA)
            me = await client.get_me()
            print(f"✅✅✅ CONNECTÉ AVEC 2FA ! {me.first_name} {me.last_name or ''} ({me.phone})")
            print("Session sauvegardée !")
        except Exception as e:
            print(f"❌ Erreur 2FA : {e}")
    except Exception as e:
        print(f"❌ Erreur sign_in : {e}")
    
    await client.disconnect()

asyncio.run(main())
