#!/usr/bin/env python3
"""
Telegram QR Code Login — contourne le bug du code non reçu sur VPS
Génère un QR code que Gilles scanne avec son téléphone
"""

import asyncio
import os
import qrcode
import base64
from telethon import TelegramClient

API_ID = 32146463
API_HASH = 'edeffff2c2cde22368b2d2183d6f0fe9'
SESSION_FILE = '/home/gilles/.openclaw/workspace/tools/telegram_session'

# Nettoyer ancienne session
if os.path.exists(SESSION_FILE + '.session'):
    os.remove(SESSION_FILE + '.session')

async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Déjà connecté : {me.first_name} ({me.phone})")
        await client.disconnect()
        return
    
    print("📱 Connexion par QR Code...")
    print("=" * 50)
    
    qr_login = await client.qr_login()
    
    # Générer le QR code en tant qu'image
    qr_url = qr_login.url
    print(f"\nURL QR: {qr_url}\n")
    
    # Sauvegarder en image PNG
    qr_img = qrcode.make(qr_url)
    qr_path = '/home/gilles/.openclaw/workspace/tools/telegram_qr.png'
    qr_img.save(qr_path)
    print(f"📸 QR Code sauvegardé : {qr_path}")
    
    # Aussi afficher en terminal
    qr = qrcode.QRCode(border=1)
    qr.add_data(qr_url)
    qr.make()
    qr.print_ascii()
    
    print("\n" + "=" * 50)
    print("📱 INSTRUCTIONS :")
    print("1. Ouvre Telegram sur ton téléphone")
    print("2. Va dans Paramètres → Appareils → Connecter un appareil")
    print("3. Scanne ce QR code")
    print("=" * 50)
    print("\n⏳ En attente du scan... (timeout 60s)")
    
    try:
        # Attendre que l'utilisateur scanne, avec tentatives de refresh
        for attempt in range(6):
            try:
                result = await asyncio.wait_for(qr_login.wait(timeout=10), timeout=15)
                break
            except asyncio.TimeoutError:
                # Recréer le QR code
                await qr_login.recreate()
                qr_img = qrcode.make(qr_login.url)
                qr_img.save(qr_path)
                print(f"🔄 QR Code rafraîchi (tentative {attempt + 2}/6)")
                qr = qrcode.QRCode(border=1)
                qr.add_data(qr_login.url)
                qr.make()
                qr.print_ascii()
        
        me = await client.get_me()
        print(f"\n✅ CONNECTÉ ! {me.first_name} {me.last_name or ''} ({me.phone})")
        print("La session est sauvegardée — plus besoin de rescanner.")
        
    except Exception as e:
        print(f"\n❌ Erreur: {type(e).__name__}: {e}")
        if "SessionPasswordNeededError" in str(type(e).__name__):
            print("⚠️ Tu as la vérification en 2 étapes activée.")
            print("Il faudra aussi entrer ton mot de passe 2FA.")
    
    await client.disconnect()

asyncio.run(main())
