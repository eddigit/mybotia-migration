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

Tu disposes d'un outil email complet pour gérer ta boîte mail professionnelle (max.vlmedical@collaborateur.pro).

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
→ Affiche le contenu complet d'un mail par son ID (obtenu via list ou check).

### Préparer un brouillon (TOUJOURS faire ça avant d'envoyer)
```
python3 tools/email_tool.py draft "<destinataire>" "<objet>" "<corps>"
```
→ Affiche le mail tel qu'il serait envoyé, SANS l'envoyer. Montre-le au client et attends son "GO".

### Envoyer un mail (UNIQUEMENT après GO du client)
```
python3 tools/email_tool.py send "<destinataire>" "<objet>" "<corps>"
```
→ Envoie le mail. ⚠️ JAMAIS sans validation explicite du client.

### Répondre à un mail (UNIQUEMENT après GO du client)
```
python3 tools/email_tool.py reply <id> "<corps de la réponse>"
```
→ Répond au mail avec citation de l'original. ⚠️ JAMAIS sans validation explicite du client.

### Rechercher dans les mails
```
python3 tools/email_tool.py search "<terme>"
```
→ Recherche dans les objets et corps des mails.

## Règles ABSOLUES

1. **CHECK régulier** : Vérifie les mails quand le client te le demande ou en début de conversation
2. **DRAFT avant SEND** : Toujours montrer le brouillon avant d'envoyer
3. **ATTENDRE LE GO** : Jamais d'envoi sans validation explicite ("GO", "envoie", "vas-y", "ok envoie")
4. **RÉSUMÉ des nouveaux mails** : Quand tu trouves de nouveaux mails, présente un résumé structuré avec urgence estimée
5. **CONFIDENTIALITÉ** : Ne partage jamais le contenu d'un mail avec un tiers sans autorisation
