# RECHERCHE API TITAN / TITANLINK

## Éditeur
- **Malta Informatique** (groupe Equasens/Welcoop, division AXIGATE LINK)
- Siège : Bordeaux
- Contact : +33 5 57 35 19 25 / contact.malta@equasens.com
- Site : https://www.malta-informatique.fr

## Ce qu'on sait

### Interopérabilité documentée (source : fiche produit Malta)
- **IHE HL7** : dossier résident, séjours, mouvements (création, intégration, flux)
- **HPRIM** : examens biologiques (HPRIM Santé 2.1 + HPRIM 1 et 2)
- **ORMC / SEPA** : prélèvements bancaires
- **ROLMRE / HELIOS** : titres de recette (secteur public)
- **PN13** : circuit du médicament (PUI/pharmacie)
- **Exports comptables** : +100 logiciels déjà référencés, module d'export paramétrable
- **Appels contextuels URL** : possibilité d'appeler des services intranet avec IPP du résident

### Ce qui MANQUE dans la doc publique
- **Aucune mention d'API REST/JSON** moderne
- Pas de documentation développeur publique
- Pas de portail API
- L'interopérabilité est basée sur des standards santé anciens (HL7, HPRIM), pas sur du REST

### Hypothèse
TitanLink étant "full web" (nouvelle version), il est PROBABLE qu'il y ait une API interne. Mais elle n'est peut-être pas exposée aux clients.

## Actions

| Date | Action | Résultat |
|------|--------|---------|
| 9 mars 2026 | Recherche web approfondie | Pas d'API REST trouvée |
| 9 mars 2026 | Email envoyé à contact.malta@equasens.com | En attente de réponse |
| 14 mars 2026 | Relance si pas de réponse | À faire |
| | Appel téléphonique +33 5 57 35 19 25 | Si email sans réponse |

## Impact sur le projet Imbert

**Si API disponible :**
→ On lit directement les données Titan (lits, factures, encaissements)
→ Rapport quotidien automatique sans intervention des directeurs
→ C'est le scénario idéal

**Si pas d'API :**
→ Collecte via formulaires wizard (directeurs remplissent sur leur téléphone)
→ Ou via WhatsApp (l'agent pose les questions, les directeurs répondent)
→ Fonctionne aussi, mais dépend de la réactivité des directeurs

---
*9 mars 2026 — Léa*
