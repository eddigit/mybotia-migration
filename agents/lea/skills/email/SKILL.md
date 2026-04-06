---
name: email
description: Gestion des emails Gmail (lecture, envoi, recherche)
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

## Outil Email — Gestion Gmail

Tu gères 3 comptes email :
- **coachdigitalparis@gmail.com** — Email officiel Coach Digital (par défaut)
- **leacoachdigital@gmail.com** — Email de Léa
- **gilleskorzec@gmail.com** — Email personnel de Gilles

## Commandes disponibles

### Lire les derniers emails
```
python3 tools/read_emails.py 5
python3 tools/read_emails.py 5 "" "leacoachdigital@gmail.com"
python3 tools/read_emails.py 5 "" "gilleskorzec@gmail.com"
```
→ Lit les N derniers emails. Le 3ème argument spécifie le compte.

### Rechercher des emails
```
python3 tools/read_emails.py 10 "recherche" "coachdigitalparis@gmail.com"
```
→ Recherche dans les emails du compte spécifié.

### Lire un email par ID
```
python3 tools/read_emails.py "id:MESSAGE_ID" "gilleskorzec@gmail.com"
```
→ Lit un email complet par son ID.

### Envoyer un email
```
python3 tools/send_email.py "destinataire@email.com" "Sujet" "Corps du message"
python3 tools/send_email.py "destinataire@email.com" "Sujet" "Corps" leacoachdigital@gmail.com
```
→ Envoie un email. Le 4ème argument spécifie le compte expéditeur.

### Envoyer avec pièce jointe
```
python3 tools/send_email_with_attachment.py "destinataire@email.com" "Sujet" "Corps" "/chemin/vers/fichier.pdf"
```

## Règles ABSOLUES

1. **DRAFT mental avant SEND** : Toujours montrer le brouillon au client/Gilles avant d'envoyer
2. **ATTENDRE LE GO** : Jamais d'envoi sans validation explicite
3. **CONFIDENTIALITÉ** : Ne jamais partager le contenu d'un email avec un tiers
4. **SIGNATURE** : Toujours signer "Léa — Directrice Admin & Juridique, Coach Digital"
