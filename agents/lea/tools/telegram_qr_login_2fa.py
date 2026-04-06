#!/usr/bin/env python3
"""
Telegram QR Code Login avec support 2FA
Génère un QR code, attend le scan, puis entre le mot de passe 2FA automatiquement
"""

import asyncio
import os
import sys
import qrcode
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

API_ID = 32146463
API_HASH = 'edeffff2c2cde22368b2d2183d6f0fe9'
SESSION_FILE = '/home/gilles/.openclaw/workspace/tools/telegram_session'
PASSWORD_2FA = '$$Reussite888!!'

# Nettoyer ancienne session
if os.path.exists(SESSION_FILE + '.session'):
    os.remove(SESSION_FILE + '.session')
    print("🗑️ Ancienne session supprimée")

async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Déjà connecté : {me.first_name} ({me.phone})")
        await client.disconnect()
        return
    
    print("📱 Connexion par QR Code avec 2FA...")
    print("=" * 50)
    
    qr_login = await client.qr_login()
    
    # Sauvegarder le QR en image
    qr_url = qr_login.url
    qr_img = qrcode.make(qr_url)
    qr_path = '/home/gilles/.openclaw/workspace/tools/telegram_qr.png'
    qr_img.save(qr_path)
    
    # Sauvegarder l'URL pour référence
    with open('/home/gilles/.openclaw/workspace/tools/telegram_qr_url.txt', 'w') as f:
        f.write(qr_url)
    
    print(f"📸 QR Code sauvegardé : {qr_path}")
    print(f"🔗 URL: {qr_url}")
    
    # Afficher en terminal
    qr = qrcode.QRCode(border=1)
    qr.add_data(qr_url)
    qr.make()
    qr.print_ascii()
    
    print("\n📱 SCANNE CE QR CODE MAINTENANT")
    print("Telegram → Paramètres → Appareils → Connecter un appareil")
    print("=" * 50)
    
    # Attendre le scan avec refresh automatique
    scanned = False
    for attempt in range(12):  # 2 minutes total
        try:
            result = await asyncio.wait_for(qr_login.wait(timeout=10), timeout=12)
            scanned = True
            break
        except asyncio.TimeoutError:
            # Refresh le QR
            try:
                await qr_login.recreate()
                qr_img = qrcode.make(qr_login.url)
                qr_img.save(qr_path)
                with open('/home/gilles/.openclaw/workspace/tools/telegram_qr_url.txt', 'w') as f:
                    f.write(qr_login.url)
                print(f"🔄 QR rafraîchi ({attempt + 2}/12) — rescanne si besoin")
            except Exception as e:
                print(f"⚠️ Erreur refresh: {e}")
        except SessionPasswordNeededError:
            print("🔐 2FA détecté — saisie du mot de passe...")
            scanned = True
            break
        except Exception as e:
            if "SessionPasswordNeeded" in str(type(e).__name__) or "SessionPasswordNeeded" in str(e):
                print("🔐 2FA détecté — saisie du mot de passe...")
                scanned = True
                break
            print(f"⚠️ Erreur: {e}")
    
    if not scanned:
        print("❌ Timeout — pas de scan détecté en 2 minutes")
        await client.disconnect()
        return
    
    # Gérer le 2FA
    try:
        me = await client.get_me()
        if me:
            print(f"✅ CONNECTÉ (sans 2FA) : {me.first_name} ({me.phone})")
            await client.disconnect()
            return
    except:
        pass
    
    # Tenter le mot de passe 2FA
    try:
        print(f"🔐 Envoi du mot de passe 2FA...")
        await client.sign_in(password=PASSWORD_2FA)
        me = await client.get_me()
        print(f"\n✅✅✅ CONNECTÉ AVEC 2FA ! {me.first_name} {me.last_name or ''} ({me.phone})")
        print("Session sauvegardée — plus besoin de rescanner.")
    except SessionPasswordNeededError:
        print("🔐 2FA requis, tentative...")
        await client.sign_in(password=PASSWORD_2FA)
        me = await client.get_me()
        print(f"\n✅ CONNECTÉ ! {me.first_name} ({me.phone})")
    except Exception as e:
        print(f"❌ Erreur 2FA: {type(e).__name__}: {e}")
    
    await client.disconnect()

asyncio.run(main())
