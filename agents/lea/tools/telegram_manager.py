#!/usr/bin/env python3
"""
Telegram Account Manager — Coach Digital Paris
Gère le compte Telegram de Gilles via l'API User (Telethon)
"""

import sys
import json
import asyncio
from telethon import TelegramClient, functions, types

API_ID = 32146463
API_HASH = 'edeffff2c2cde22368b2d2183d6f0fe9'
SESSION_FILE = '/home/gilles/.openclaw/workspace/tools/telegram_session'

client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

async def login():
    """Première connexion — demande le code"""
    await client.start()
    me = await client.get_me()
    print(f"✅ Connecté en tant que: {me.first_name} {me.last_name or ''} (@{me.username or 'N/A'})")
    print(f"📱 Téléphone: {me.phone}")

async def list_contacts():
    """Liste tous les contacts"""
    result = await client(functions.contacts.GetContactsRequest(hash=0))
    contacts = result.users
    print(f"\n📇 {len(contacts)} contacts trouvés:\n")
    for i, user in enumerate(contacts, 1):
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        phone = user.phone or "N/A"
        username = f"@{user.username}" if user.username else ""
        print(f"  {i:3}. {name:30} | {phone:15} | {username} | ID: {user.id}")
    return contacts

async def list_dialogs(limit=50):
    """Liste les conversations récentes"""
    dialogs = await client.get_dialogs(limit=limit)
    print(f"\n💬 {len(dialogs)} conversations:\n")
    for i, dialog in enumerate(dialogs, 1):
        dtype = "👤" if dialog.is_user else ("👥" if dialog.is_group else "📢")
        unread = f" ({dialog.unread_count} non lus)" if dialog.unread_count else ""
        print(f"  {i:3}. {dtype} {dialog.name:40} | ID: {dialog.id}{unread}")
    return dialogs

async def list_groups():
    """Liste uniquement les groupes"""
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group]
    print(f"\n👥 {len(groups)} groupes:\n")
    for i, g in enumerate(groups, 1):
        unread = f" ({g.unread_count} non lus)" if g.unread_count else ""
        print(f"  {i:3}. {g.name:40} | ID: {g.id}{unread}")
    return groups

async def set_privacy_contacts_only():
    """Configure la confidentialité : seuls les contacts peuvent contacter"""
    # Messages
    try:
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyStatusTimestamp(),
            rules=[types.InputPrivacyValueAllowContacts()]
        ))
        print("✅ Dernière connexion : visible par contacts uniquement")
    except Exception as e:
        print(f"⚠️ Dernière connexion : {e}")

    # Appels
    try:
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneCall(),
            rules=[types.InputPrivacyValueAllowContacts()]
        ))
        print("✅ Appels : contacts uniquement")
    except Exception as e:
        print(f"⚠️ Appels : {e}")

    # Ajout aux groupes
    try:
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyChatInvite(),
            rules=[types.InputPrivacyValueAllowContacts()]
        ))
        print("✅ Ajout aux groupes : contacts uniquement")
    except Exception as e:
        print(f"⚠️ Ajout aux groupes : {e}")

    # Numéro de téléphone
    try:
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneNumber(),
            rules=[types.InputPrivacyValueAllowContacts()]
        ))
        print("✅ Numéro de téléphone : visible par contacts uniquement")
    except Exception as e:
        print(f"⚠️ Numéro de téléphone : {e}")

    # Photo de profil
    try:
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyProfilePhoto(),
            rules=[types.InputPrivacyValueAllowContacts()]
        ))
        print("✅ Photo de profil : visible par contacts uniquement")
    except Exception as e:
        print(f"⚠️ Photo de profil : {e}")

    # Messages transférés
    try:
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyForwards(),
            rules=[types.InputPrivacyValueAllowContacts()]
        ))
        print("✅ Messages transférés : contacts uniquement")
    except Exception as e:
        print(f"⚠️ Messages transférés : {e}")

    print("\n🔒 Confidentialité configurée — seuls tes contacts peuvent te joindre")

async def delete_all_contacts_except(keep_phones):
    """Supprime tous les contacts SAUF ceux dont le numéro est dans keep_phones"""
    result = await client(functions.contacts.GetContactsRequest(hash=0))
    contacts = result.users
    
    to_delete = []
    to_keep = []
    
    for user in contacts:
        phone = (user.phone or "").replace(" ", "").replace("+", "")
        keep = False
        for kp in keep_phones:
            kp_clean = kp.replace(" ", "").replace("+", "")
            if phone.endswith(kp_clean) or kp_clean.endswith(phone):
                keep = True
                break
        if keep:
            to_keep.append(user)
        else:
            to_delete.append(user)
    
    print(f"\n📇 Contacts à GARDER ({len(to_keep)}):")
    for u in to_keep:
        name = f"{u.first_name or ''} {u.last_name or ''}".strip()
        print(f"  ✅ {name} ({u.phone})")
    
    print(f"\n🗑️ Contacts à SUPPRIMER ({len(to_delete)}):")
    for u in to_delete:
        name = f"{u.first_name or ''} {u.last_name or ''}".strip()
        print(f"  ❌ {name} ({u.phone})")
    
    return to_delete, to_keep

async def do_delete_contacts(contacts_to_delete):
    """Exécute la suppression effective des contacts"""
    if not contacts_to_delete:
        print("Aucun contact à supprimer.")
        return
    
    input_users = []
    for user in contacts_to_delete:
        input_users.append(types.InputUser(user_id=user.id, access_hash=user.access_hash))
    
    await client(functions.contacts.DeleteContactsRequest(id=input_users))
    print(f"\n✅ {len(contacts_to_delete)} contacts supprimés!")

async def block_user(user_id):
    """Bloque un utilisateur par son ID"""
    await client(functions.contacts.BlockRequest(
        id=await client.get_input_entity(user_id)
    ))
    print(f"✅ Utilisateur {user_id} bloqué")

async def leave_group(group_id):
    """Quitte un groupe par son ID"""
    await client(functions.channels.LeaveChannelRequest(channel=group_id))
    print(f"✅ Groupe {group_id} quitté")

async def main():
    await client.connect()
    
    if len(sys.argv) < 2:
        print("Usage: python3 telegram_manager.py [commande]")
        print("  login          — Première connexion")
        print("  contacts       — Lister les contacts")
        print("  dialogs        — Lister les conversations")
        print("  groups         — Lister les groupes")
        print("  privacy        — Configurer confidentialité (contacts only)")
        print("  preview-clean  — Prévisualiser le nettoyage contacts")
        print("  clean          — Supprimer tous les contacts sauf équipe")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "login":
        await login()
    elif cmd == "contacts":
        await login()
        await list_contacts()
    elif cmd == "dialogs":
        await login()
        await list_dialogs()
    elif cmd == "groups":
        await login()
        await list_groups()
    elif cmd == "privacy":
        await login()
        await set_privacy_contacts_only()
    elif cmd == "preview-clean":
        await login()
        # Numéros de l'équipe Coach Digital à garder
        keep = [
            "+33652345180",   # Gilles
            "+33756968633",   # Oscar
            "+33780956160",   # Jules
            "+33780942994",   # Léa
            "+33780955161",   # Nina
            "+33648324227",   # Hugo
            "+33689050379",   # Hugo perso
        ]
        await delete_all_contacts_except(keep)
    elif cmd == "clean":
        await login()
        keep = [
            "+33652345180",   # Gilles
            "+33756968633",   # Oscar
            "+33780956160",   # Jules
            "+33780942994",   # Léa
            "+33780955161",   # Nina
            "+33648324227",   # Hugo
            "+33689050379",   # Hugo perso
        ]
        to_delete, to_keep = await delete_all_contacts_except(keep)
        if to_delete:
            confirm = input(f"\n⚠️ Confirmer la suppression de {len(to_delete)} contacts ? (oui/non): ")
            if confirm.lower() == "oui":
                await do_delete_contacts(to_delete)
            else:
                print("Annulé.")
    else:
        print(f"Commande inconnue: {cmd}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
