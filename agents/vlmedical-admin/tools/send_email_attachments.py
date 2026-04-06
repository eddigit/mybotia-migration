#!/usr/bin/env python3
"""
Envoie un email avec plusieurs pièces jointes via SMTP Migadu.
Usage: python3 send_email_attachments.py <to> <subject> <body> <file1> [file2] [file3...]
"""

import sys
import json
import os
import smtplib
import imaplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr, formatdate

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "email.json")
    with open(config_path, "r") as f:
        return json.load(f)

def send_with_attachments(to, subject, body, files):
    config = load_config()
    
    msg = MIMEMultipart()
    msg["From"] = formataddr((config["name"], config["address"]))
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    
    full_body = body + config.get("signature", "")
    msg.attach(MIMEText(full_body, "plain", "utf-8"))
    
    for filepath in files:
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()
        subtype = "pdf" if ext == ".pdf" else "vnd.openxmlformats-officedocument.spreadsheetml.sheet" if ext == ".xlsx" else "octet-stream"
        
        with open(filepath, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype=subtype)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(attachment)
        print(f"   PJ ajoutée : {filename}")
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"], context=context) as server:
        server.login(config["address"], config["password"])
        server.sendmail(config["address"], to, msg.as_string())
    
    # Copier dans le dossier Sent via IMAP
    try:
        imap = imaplib.IMAP4_SSL(config["imap_host"], config["imap_port"], ssl_context=context)
        imap.login(config["address"], config["password"])
        imap.select("Sent")
        imap.append("Sent", "\\Seen", None, msg.as_bytes())
        imap.logout()
    except Exception as e:
        print(f"   (Copie Sent échouée: {e})")
    
    print(f"\n✅ Email envoyé à {to}")
    print(f"   Objet : {subject}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 send_email_attachments.py <to> <subject> <body> <file1> [file2...]")
        sys.exit(1)
    
    send_with_attachments(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
