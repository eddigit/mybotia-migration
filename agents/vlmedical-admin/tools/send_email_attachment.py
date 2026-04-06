#!/usr/bin/env python3
"""
Envoie un email avec pièce jointe PDF via SMTP Migadu.
Usage: python3 send_email_attachment.py <to> <subject> <body> <attachment_path>
"""

import sys
import json
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr, formatdate

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "email.json")
    with open(config_path, "r") as f:
        return json.load(f)

def send_with_attachment(to, subject, body, attachment_path):
    config = load_config()
    
    msg = MIMEMultipart()
    msg["From"] = formataddr((config["name"], config["address"]))
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    
    # Corps du message avec signature
    full_body = body + config.get("signature", "")
    msg.attach(MIMEText(full_body, "plain", "utf-8"))
    
    # Pièce jointe
    filename = os.path.basename(attachment_path)
    with open(attachment_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(attachment)
    
    # Envoi
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"], context=context) as server:
        server.login(config["address"], config["password"])
        server.sendmail(config["address"], to, msg.as_string())
    
    print(f"✅ Email envoyé à {to}")
    print(f"   Objet : {subject}")
    print(f"   Pièce jointe : {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 send_email_attachment.py <to> <subject> <body> <attachment_path>")
        sys.exit(1)
    
    send_with_attachment(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
