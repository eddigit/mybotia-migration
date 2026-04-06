# TOOLS.md — Configuration Locale de Nina

## Email Professionnel — nina@collaborateur.pro

### Accès Migadu
- **Adresse** : nina@collaborateur.pro
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
python3 tools/email_tool.py send "dest" "sujet" "corps"    # Envoyer (après GO)
python3 tools/email_tool.py send "dest" "sujet" "corps" --cc "copie@example.com"  # Avec CC
python3 tools/email_tool.py reply <id> "réponse"           # Répondre (après GO)
python3 tools/email_tool.py search "terme"  # Rechercher
```

### Règles email
- **DRAFT avant SEND** : toujours montrer le brouillon à Hugo ou au CEO
- **ATTENDRE LE GO** : jamais d envoi sans validation explicite
- **Signature** : "Nina — Responsable Commerciale, Coach Digital Paris"
- **Horaires** : mardi-jeudi, 9h-11h ou 14h-16h (sauf instruction contraire)
- **Max 50 emails/jour**

## Telegram
- **Bot** : @nina_coachdigital_bot
- **Groupe** : TEAM GILLES KORZEC (requireMention: true)

## WebChat
- **URL** : https://nina.mybotia.com
