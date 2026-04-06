---
name: facturation
description: Génération de factures et devis PDF
user-invocable: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata:
  openclaw:
    emoji: "🧾"
    requires:
      bins: ["python3"]
---

## Outil Facturation — Génération de factures et devis PDF

Tu peux générer des factures et devis au format PDF.

## Commandes disponibles

### Générer une facture
```
python3 tools/generate_invoice.py
```
→ Génère une facture PDF selon les paramètres définis dans le script.

### Générer une facture VL Medical
```
python3 tools/generate_invoice_vlmedical.py
```

### Générer une facture Aubagnac
```
python3 tools/generate_invoice_aubagnac.py
```

## Règles

1. **TOUJOURS vérifier** les montants et les informations avant de générer
2. **MONTRER** le récapitulatif au client avant de générer le PDF
3. **NUMÉROTATION** : suivre la séquence de facturation existante
