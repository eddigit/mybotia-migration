# TOOLS.md — Configuration Locale de Eva

## Email Professionnel — eva.vlmedical@collaborateur.pro

### Acces Migadu
- **Adresse** : eva.vlmedical@collaborateur.pro
- **IMAP** : imap.migadu.com:993 (SSL)
- **SMTP** : smtp.migadu.com:465 (SSL)
- **Config** : config/email.json
- **Outil** : tools/email_tool.py
- **Skill** : skills/email/SKILL.md

### Commandes rapides
```bash
python3 tools/email_tool.py check           # Nouveaux mails
python3 tools/email_tool.py list 10         # 10 derniers mails
python3 tools/email_tool.py read <id>       # Lire un mail
python3 tools/email_tool.py draft "dest" "sujet" "corps"   # Brouillon
python3 tools/email_tool.py send "dest" "sujet" "corps"    # Envoyer (apres GO)
python3 tools/email_tool.py reply <id> "reponse"           # Repondre (apres GO)
python3 tools/email_tool.py search "terme"  # Rechercher
```

### Regles email
- **DRAFT avant SEND** : toujours montrer le brouillon a Gilles ou Jean-Luc
- **ATTENDRE LE GO** : jamais d envoi sans validation explicite
- **Signature** : "Eva — Responsable Commerciale, VL Medical"

## WebChat
- **URL** : https://eva.mybotia.com

## Collaboration Max
- Pour questions juridiques ou contractuelles → rediriger vers Max
- Max est joignable via max.mybotia.com ou @max_vlmedical_bot
