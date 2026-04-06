#!/usr/bin/env python3
"""
email_tool.py — Outil email pour collaborateurs IA (Migadu IMAP/SMTP)
Usage: python3 email_tool.py <command> [options]

Commands:
  check                    - Vérifie les nouveaux mails non lus
  list [N]                 - Liste les N derniers mails (défaut: 10)
  read <id>                - Lit le contenu complet d'un mail
  send <to> <subject> <body> - Envoie un mail
  reply <id> <body>        - Répond à un mail
  draft <to> <subject> <body> - Prépare un brouillon (affiche sans envoyer)
  search <query>           - Recherche dans les mails

Config: ./config/email.json ou variable EMAIL_CONFIG
"""

import sys
import os
import json
import email
import imaplib
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
from email.utils import formataddr, formatdate, parsedate_to_datetime
from datetime import datetime, timezone
import mimetypes

# --- Configuration ---

def load_config():
    """Charge la config email depuis le fichier JSON ou les variables d'env."""
    config_path = os.environ.get("EMAIL_CONFIG", 
                  os.path.join(os.path.dirname(__file__), "..", "config", "email.json"))
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    
    # Fallback: variables d'environnement
    return {
        "address": os.environ.get("EMAIL_ADDRESS", ""),
        "password": os.environ.get("EMAIL_PASSWORD", ""),
        "name": os.environ.get("EMAIL_NAME", ""),
        "imap_host": os.environ.get("EMAIL_IMAP_HOST", "imap.migadu.com"),
        "imap_port": int(os.environ.get("EMAIL_IMAP_PORT", "993")),
        "smtp_host": os.environ.get("EMAIL_SMTP_HOST", "smtp.migadu.com"),
        "smtp_port": int(os.environ.get("EMAIL_SMTP_PORT", "465")),
    }

# --- Helpers ---

def decode_mime_header(header):
    """Décode un header MIME (subject, from, etc.)."""
    if header is None:
        return ""
    decoded_parts = decode_header(header)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            result.append(part)
    return " ".join(result)

def get_body(msg):
    """Extrait le corps texte d'un message email."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    return part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", errors="replace")
                except:
                    return part.get_payload(decode=True).decode("utf-8", errors="replace")
            elif content_type == "text/html" and not any(
                p.get_content_type() == "text/plain" for p in msg.walk()):
                try:
                    return "[HTML] " + part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", errors="replace")
                except:
                    return "[HTML content]"
    else:
        try:
            return msg.get_payload(decode=True).decode(
                msg.get_content_charset() or "utf-8", errors="replace")
        except:
            return "[Unable to decode]"
    return "[No text content]"

def format_mail_summary(msg, uid):
    """Formate un résumé court d'un mail."""
    from_addr = decode_mime_header(msg.get("From", ""))
    subject = decode_mime_header(msg.get("Subject", "(sans sujet)"))
    date_str = msg.get("Date", "")
    try:
        dt = parsedate_to_datetime(date_str)
        date_fmt = dt.strftime("%d/%m %H:%M")
    except:
        date_fmt = date_str[:16] if date_str else "?"
    
    return f"[{uid}] {date_fmt} | De: {from_addr} | Objet: {subject}"

def connect_imap(config):
    """Connecte au serveur IMAP."""
    ctx = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(config["imap_host"], config["imap_port"], ssl_context=ctx)
    imap.login(config["address"], config["password"])
    return imap

def connect_smtp(config):
    """Connecte au serveur SMTP."""
    ctx = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"], context=ctx)
    smtp.login(config["address"], config["password"])
    return smtp

# --- Commands ---

def cmd_check(config):
    """Vérifie les mails non lus."""
    imap = connect_imap(config)
    imap.select("INBOX")
    _, data = imap.search(None, "UNSEEN")
    uids = data[0].split()
    
    if not uids:
        print("Aucun nouveau mail.")
        imap.logout()
        return
    
    print(f"{len(uids)} mail(s) non lu(s):\n")
    for uid in uids[-10:]:  # Max 10 derniers
        _, msg_data = imap.fetch(uid, "(BODY.PEEK[HEADER])")
        msg = email.message_from_bytes(msg_data[0][1])
        print(format_mail_summary(msg, uid.decode()))
    
    if len(uids) > 10:
        print(f"\n... et {len(uids) - 10} autre(s)")
    
    imap.logout()

def cmd_list(config, count=10):
    """Liste les N derniers mails."""
    imap = connect_imap(config)
    imap.select("INBOX")
    _, data = imap.search(None, "ALL")
    uids = data[0].split()
    
    if not uids:
        print("Boite mail vide.")
        imap.logout()
        return
    
    recent = uids[-count:]
    recent.reverse()
    
    print(f"Derniers {min(count, len(uids))} mails:\n")
    for uid in recent:
        _, msg_data = imap.fetch(uid, "(BODY.PEEK[HEADER] FLAGS)")
        msg = email.message_from_bytes(msg_data[0][1])
        flags = msg_data[0][0].decode() if msg_data[0][0] else ""
        unread = "NEW " if "\\Seen" not in flags else "    "
        print(f"{unread}{format_mail_summary(msg, uid.decode())}")
    
    imap.logout()

def cmd_read(config, mail_id):
    """Lit le contenu complet d'un mail."""
    imap = connect_imap(config)
    imap.select("INBOX")
    _, msg_data = imap.fetch(str(mail_id).encode(), "(RFC822)")
    
    if not msg_data or msg_data[0] is None:
        print(f"Mail {mail_id} non trouve.")
        imap.logout()
        return
    
    msg = email.message_from_bytes(msg_data[0][1])
    
    print(f"De: {decode_mime_header(msg.get('From', ''))}")
    print(f"A: {decode_mime_header(msg.get('To', ''))}")
    if msg.get("Cc"):
        print(f"Cc: {decode_mime_header(msg.get('Cc'))}")
    print(f"Date: {msg.get('Date', '?')}")
    print(f"Objet: {decode_mime_header(msg.get('Subject', '(sans sujet)'))}")
    print(f"Message-ID: {msg.get('Message-ID', '?')}")
    
    # Pièces jointes
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            filename = part.get_filename()
            if filename:
                attachments.append(decode_mime_header(filename))
    if attachments:
        print(f"Pieces jointes: {', '.join(attachments)}")
    
    print(f"\n{'='*60}\n")
    print(get_body(msg))
    
    imap.logout()

def cmd_send(config, to, subject, body, reply_to_id=None, reply_msg=None, attachments=None, cc=None):
    """Envoie un mail, avec pièces jointes et CC optionnels."""
    msg = MIMEMultipart()
    msg["From"] = formataddr((config.get("name", ""), config["address"]))
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    
    if cc:
        msg["Cc"] = cc
    
    if reply_to_id and reply_msg:
        msg["In-Reply-To"] = reply_msg.get("Message-ID", "")
        msg["References"] = reply_msg.get("Message-ID", "")
    
    # Signature
    signature = config.get("signature", f"\n--\n{config.get('name', '')}\n{config['address']}")
    full_body = body + signature
    
    msg.attach(MIMEText(full_body, "plain", "utf-8"))
    
    # Pièces jointes
    if attachments:
        for filepath in attachments:
            if not os.path.exists(filepath):
                print(f"ATTENTION: fichier introuvable: {filepath}")
                continue
            filename = os.path.basename(filepath)
            mime_type, _ = mimetypes.guess_type(filepath)
            if mime_type is None:
                mime_type = "application/octet-stream"
            maintype, subtype = mime_type.split("/", 1)
            
            with open(filepath, "rb") as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(part)
            print(f"  Piece jointe: {filename} ({os.path.getsize(filepath)} octets)")
    
    # Destinataires = To + Cc
    recipients = [to]
    if cc:
        recipients.extend([addr.strip() for addr in cc.split(",")])
    
    smtp = connect_smtp(config)
    smtp.send_message(msg, to_addrs=recipients)
    smtp.quit()
    
    # Copier dans le dossier Sent via IMAP
    try:
        imap = connect_imap(config)
        imap.select("Sent")
        imap.append("Sent", "\\Seen", None, msg.as_bytes())
        imap.logout()
    except Exception as e:
        print(f"  (Copie Sent echouee: {e})")
    
    print(f"Mail envoye avec succes.")
    print(f"  De: {config['address']}")
    print(f"  A: {to}")
    if cc:
        print(f"  Cc: {cc}")
    print(f"  Objet: {subject}")

def cmd_draft(config, to, subject, body, attachments=None, cc=None):
    """Affiche un brouillon sans envoyer."""
    signature = config.get("signature", f"\n--\n{config.get('name', '')}\n{config['address']}")
    
    print("=" * 60)
    print("BROUILLON (non envoye)")
    print("=" * 60)
    print(f"De: {config.get('name', '')} <{config['address']}>")
    print(f"A: {to}")
    if cc:
        print(f"Cc: {cc}")
    print(f"Objet: {subject}")
    if attachments:
        print(f"Pieces jointes ({len(attachments)}):")
        for fp in attachments:
            name = os.path.basename(fp)
            size = os.path.getsize(fp) if os.path.exists(fp) else 0
            status = "OK" if os.path.exists(fp) else "INTROUVABLE"
            print(f"  - {name} ({size} octets) [{status}]")
    print("-" * 60)
    print(body + signature)
    print("=" * 60)
    print("\nPour envoyer, confirmez avec 'GO'.")

def cmd_reply(config, mail_id, body):
    """Répond à un mail."""
    imap = connect_imap(config)
    imap.select("INBOX")
    _, msg_data = imap.fetch(str(mail_id).encode(), "(RFC822)")
    
    if not msg_data or msg_data[0] is None:
        print(f"Mail {mail_id} non trouve.")
        imap.logout()
        return
    
    original = email.message_from_bytes(msg_data[0][1])
    imap.logout()
    
    reply_to = original.get("Reply-To", original.get("From", ""))
    subject = decode_mime_header(original.get("Subject", ""))
    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"
    
    # Citation du message original
    orig_body = get_body(original)
    orig_from = decode_mime_header(original.get("From", ""))
    orig_date = original.get("Date", "")
    
    quoted = "\n".join(f"> {line}" for line in orig_body.split("\n")[:20])
    full_body = f"{body}\n\nLe {orig_date}, {orig_from} a ecrit:\n{quoted}"
    
    cmd_send(config, reply_to, subject, full_body, 
             reply_to_id=mail_id, reply_msg=original)

def cmd_search(config, query):
    """Recherche dans les mails."""
    imap = connect_imap(config)
    imap.select("INBOX")
    
    # Recherche dans sujet et corps
    _, data = imap.search(None, f'(OR SUBJECT "{query}" BODY "{query}")')
    uids = data[0].split()
    
    if not uids:
        print(f"Aucun resultat pour: {query}")
        imap.logout()
        return
    
    print(f"{len(uids)} resultat(s) pour '{query}':\n")
    for uid in uids[-15:]:
        _, msg_data = imap.fetch(uid, "(BODY.PEEK[HEADER])")
        msg = email.message_from_bytes(msg_data[0][1])
        print(format_mail_summary(msg, uid.decode()))
    
    imap.logout()

# --- Main ---

def parse_extra_args(args):
    """Extrait les pièces jointes (--attach) et CC (--cc) de la liste d'arguments.
    Retourne (args_clean, attachments, cc)."""
    attachments = []
    cc = None
    clean = []
    i = 0
    while i < len(args):
        if args[i] in ("--attach", "--attachment"):
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                attachments.append(args[i])
                i += 1
        elif args[i] == "--cc":
            i += 1
            if i < len(args):
                cc = args[i]
                i += 1
        else:
            clean.append(args[i])
            i += 1
    return clean, attachments, cc

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    config = load_config()
    
    if not config.get("address") or not config.get("password"):
        print("ERREUR: Configuration email manquante.")
        print("Creez config/email.json ou definissez EMAIL_ADDRESS et EMAIL_PASSWORD")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    remaining, attachments, cc = parse_extra_args(sys.argv[2:])
    
    try:
        if cmd == "check":
            cmd_check(config)
        elif cmd == "list":
            count = int(remaining[0]) if remaining else 10
            cmd_list(config, count)
        elif cmd == "read":
            if not remaining:
                print("Usage: email_tool.py read <id>")
                sys.exit(1)
            cmd_read(config, remaining[0])
        elif cmd == "send":
            if len(remaining) < 3:
                print("Usage: email_tool.py send <to> <subject> <body> [--attach file1 file2 ...]")
                sys.exit(1)
            cmd_send(config, remaining[0], remaining[1], remaining[2], attachments=attachments or None, cc=cc)
        elif cmd == "draft":
            if len(remaining) < 3:
                print("Usage: email_tool.py draft <to> <subject> <body> [--attach file1 file2 ...]")
                sys.exit(1)
            cmd_draft(config, remaining[0], remaining[1], remaining[2], attachments=attachments or None, cc=cc)
        elif cmd == "reply":
            if len(remaining) < 2:
                print("Usage: email_tool.py reply <id> <body>")
                sys.exit(1)
            cmd_reply(config, remaining[0], remaining[1])
        elif cmd == "search":
            if not remaining:
                print("Usage: email_tool.py search <query>")
                sys.exit(1)
            cmd_search(config, " ".join(remaining))
        else:
            print(f"Commande inconnue: {cmd}")
            print(__doc__)
            sys.exit(1)
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
