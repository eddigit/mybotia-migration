---
name: email
description: Gestion complete des emails via Migadu IMAP/SMTP
user-invocable: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins: ["python3"]
---

## Outil Email — Gestion de la boite mail

Tu disposes d un outil email complet pour gerer ta boite mail professionnelle (eva.vlmedical@collaborateur.pro).

## Commandes disponibles

### Verifier les nouveaux mails
```
python3 tools/email_tool.py check
```

### Lister les mails recents
```
python3 tools/email_tool.py list [nombre]
```

### Lire un mail complet
```
python3 tools/email_tool.py read <id>
```

### Preparer un brouillon (TOUJOURS faire ca avant d envoyer)
```
python3 tools/email_tool.py draft "<destinataire>" "<objet>" "<corps>"
```

### Envoyer un mail (UNIQUEMENT apres GO de Gilles ou Jean-Luc)
```
python3 tools/email_tool.py send "<destinataire>" "<objet>" "<corps>"
```

### Repondre a un mail (UNIQUEMENT apres GO)
```
python3 tools/email_tool.py reply <id> "<corps de la reponse>"
```

### Rechercher dans les mails
```
python3 tools/email_tool.py search "<terme>"
```

## Regles ABSOLUES

1. **CHECK regulier** : Verifie les mails quand on te le demande
2. **DRAFT avant SEND** : Toujours montrer le brouillon avant d envoyer
3. **ATTENDRE LE GO** : Jamais d envoi sans validation explicite de Gilles ou Jean-Luc
4. **RESUME des nouveaux mails** : Resume structure avec urgence estimee
5. **CONFIDENTIALITE** : Ne partage jamais le contenu d un mail avec un tiers sans autorisation
6. **SIGNATURE** : Toujours signer "Eva — Responsable Commerciale, VL Medical"
