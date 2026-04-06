---
name: qonto
description: Consultation compte bancaire Qonto (solde, transactions)
user-invocable: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata:
  openclaw:
    emoji: "🏦"
    requires:
      bins: ["python3"]
---

## Outil Banque — Consultation Qonto

Accès en lecture seule au compte bancaire Qonto de Coach Digital.

## Commandes disponibles

### Consulter le solde
```
python3 tools/qonto.py balance
```

### Lister les dernières transactions
```
python3 tools/qonto.py transactions 10
```
→ Affiche les N dernières transactions.

### Informations de l'organisation
```
python3 tools/qonto.py org
```

## Règles ABSOLUES

1. **LECTURE SEULE** : tu ne peux PAS initier de virement ou de paiement
2. **CONFIDENTIALITÉ** : ne jamais partager les informations bancaires
3. **PAS d'IBAN** : ne jamais afficher ou partager l'IBAN complet
