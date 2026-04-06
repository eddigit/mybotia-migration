---
name: legal_search
description: Recherche juridique française via APIs PISTE (Légifrance, Judilibre, BOAMP)
user-invocable: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata:
  openclaw:
    emoji: "⚖️"
    requires:
      bins: ["python3"]
---

## Outil Recherche Juridique — APIs PISTE (Légifrance, Judilibre, BOAMP)

Tu disposes d'un outil de recherche juridique connecté aux bases officielles françaises.

## Commandes disponibles

### Recherche dans Légifrance (textes de loi)
```
python3 tools/legal_search.py legifrance "<termes de recherche>"
```
→ Recherche dans les codes, lois, décrets. Renvoie les textes pertinents avec références.

### Recherche dans Judilibre (jurisprudence Cour de cassation)
```
python3 tools/legal_search.py judilibre "<termes de recherche>"
```
→ Recherche dans les décisions de la Cour de cassation. Renvoie les arrêts pertinents.

### Recherche dans le BOAMP (marchés publics)
```
python3 tools/legal_search.py boamp "<termes de recherche>"
```
→ Recherche dans les avis de marchés publics.

## Capacités

- **Légifrance** : Code civil, Code de commerce, Code du travail, Code pénal, tous les codes et textes législatifs
- **Judilibre** : Arrêts de la Cour de cassation, toutes chambres
- **BOAMP** : Marchés publics, appels d'offres

## Règles

1. **TOUJOURS citer les références** : numéro d'article, date de l'arrêt, numéro de pourvoi
2. **VÉRIFIER la date** : signaler si un texte a été modifié récemment
3. **CONTEXTUALISER** : expliquer en langage clair ce que le texte signifie
4. **PRUDENCE** : dire clairement quand une analyse nécessite un avocat
