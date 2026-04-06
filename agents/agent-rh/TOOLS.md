# TOOLS.md — Agent RH

## Outils disponibles

Cet agent est un agent de conversation pure. Il n'a PAS accès à :
- Le système de fichiers
- Les emails
- Les API externes
- Les bases de données

Son seul outil est la conversation. Il collecte des informations et les structure en JSON.

## Notes

- Le JSON final (entre les marqueurs ===ONBOARDING_DATA_START=== et ===ONBOARDING_DATA_END===) est parsé par le frontend
- Le frontend se charge de dispatcher les données (Notion, email, webhook)
- L'agent ne doit JAMAIS essayer d'exécuter des commandes ou d'accéder à des fichiers
