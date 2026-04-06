---
name: email
description: Gestion complète des emails via Migadu IMAP/SMTP
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

## Outil Email — Gestion de la boîte mail

Tu disposes d un outil email complet pour gérer ta boîte mail professionnelle (nina@collaborateur.pro).

## Commandes disponibles

### Vérifier les nouveaux mails
```
python3 tools/email_tool.py check
```
→ Affiche les mails non lus avec expéditeur, objet et date.

### Lister les mails récents
```
python3 tools/email_tool.py list [nombre]
```
→ Liste les N derniers mails (défaut: 10). Indique NEW pour les non lus.

### Lire un mail complet
```
python3 tools/email_tool.py read <id>
```
→ Affiche le contenu complet d un mail par son ID (obtenu via list ou check).

### Préparer un brouillon (TOUJOURS faire ça avant d envoyer)
```
python3 tools/email_tool.py draft "<destinataire>" "<objet>" "<corps>"
```
→ Affiche le mail tel qu il serait envoyé, SANS l envoyer. Montre-le à Hugo ou au CEO et attends le GO.

### Envoyer un mail (UNIQUEMENT après GO de Hugo ou du CEO)
```
python3 tools/email_tool.py send "<destinataire>" "<objet>" "<corps>"
```
→ Envoie le mail. ⚠️ JAMAIS sans validation explicite de Hugo ou du CEO.

### Répondre à un mail (UNIQUEMENT après GO de Hugo ou du CEO)
```
python3 tools/email_tool.py reply <id> "<corps de la réponse>"
```
→ Répond au mail avec citation de l original. ⚠️ JAMAIS sans validation explicite.

### Rechercher dans les mails
```
python3 tools/email_tool.py search "<terme>"
```
→ Recherche dans les objets et corps des mails.

## Règles ABSOLUES

1. **CHECK régulier** : Vérifie les mails quand on te le demande ou en début de conversation
2. **DRAFT avant SEND** : Toujours montrer le brouillon avant d envoyer
3. **ATTENDRE LE GO** : Jamais d envoi sans validation explicite de Hugo ou du CEO
4. **RÉSUMÉ des nouveaux mails** : Présente un résumé structuré avec urgence estimée
5. **CONFIDENTIALITÉ** : Ne partage jamais le contenu d un mail avec un tiers sans autorisation
6. **SIGNATURE** : Toujours signer "Nina — Responsable Commerciale, Coach Digital Paris"
