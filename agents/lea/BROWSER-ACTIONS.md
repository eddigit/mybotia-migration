# Instructions Agent — Actions Navigateur MyBotIA

Ce document décrit le protocole pour qu'un agent IA (Léa, Lucy, etc.) puisse contrôler le navigateur de l'utilisateur via l'extension Chrome MyBotIA.

## Principe

L'agent envoie des blocs d'action dans ses réponses textuelles. L'extension les détecte, les exécute sur la page active du navigateur, et affiche un feedback visuel (glow bleu pulsant + confirmation dans le chat).

## Format des blocs d'action

Insérer un bloc fenced dans la réponse :

````
```mybotia-action
{"action": "...", ...params}
```
````

Format alternatif (tag) :
```
[MYBOTIA_ACTION]{"action": "...", ...params}[/MYBOTIA_ACTION]
```

## Actions disponibles

### 1. Remplir un champ de formulaire

```mybotia-action
{"action": "fill-field", "selector": "#email", "value": "test@example.com"}
```

- `selector` : sélecteur CSS du champ (id, name, class...)
- `value` : valeur à saisir
- Supporte input, textarea, select
- Déclenche les events `input`, `change`, `blur` (compatible React/Vue)

### 2. Cliquer sur un élément

```mybotia-action
{"action": "click-element", "selector": "#submit-btn"}
```

- `selector` : sélecteur CSS de l'élément à cliquer
- Fonctionne sur les boutons, liens, cases à cocher, etc.
- L'élément est mis en surbrillance bleue avant le clic (300ms)

### 3. Naviguer vers une URL

```mybotia-action
{"action": "navigate", "url": "https://example.com/page"}
```

- `url` : URL complète vers laquelle naviguer
- La page actuelle est remplacée (pas un nouvel onglet)

## Sélecteurs CSS — Bonnes pratiques

Utiliser par ordre de préférence :
1. **ID** : `#email`, `#submit-btn` (le plus fiable)
2. **Name** : `[name="email"]`, `[name="password"]`
3. **Label** : `input[aria-label="Email"]`
4. **Type + position** : `form input[type="email"]`
5. **Classe** : `.btn-submit` (moins fiable, peut changer)

Le contexte de page (Phase 2) fournit les sélecteurs exacts pour chaque champ de formulaire détecté. Utiliser ces sélecteurs en priorité.

## Actions multiples

Plusieurs blocs d'action peuvent être dans la même réponse. Ils sont exécutés séquentiellement avec 500ms de délai entre chaque.

Exemple — remplir un formulaire complet :

```
Je vais remplir le formulaire de contact pour vous.

```mybotia-action
{"action": "fill-field", "selector": "#name", "value": "Jean Dupont"}
```

```mybotia-action
{"action": "fill-field", "selector": "#email", "value": "jean@example.com"}
```

```mybotia-action
{"action": "fill-field", "selector": "#message", "value": "Bonjour, je souhaite un rendez-vous."}
```

```mybotia-action
{"action": "click-element", "selector": "#submit"}
```

Formulaire envoyé ! Vérifiez la confirmation à l'écran.
```

## Règles obligatoires pour l'agent

1. **Toujours demander confirmation** avant d'agir sur la page. L'utilisateur doit valider explicitement ("oui", "vas-y", "ok").
2. **Décrire l'action** avant de l'exécuter. Ex : "Je vais remplir le champ email avec votre adresse."
3. **Activer le contexte de page** d'abord. Si l'utilisateur n'a pas partagé le contexte, lui demander d'activer le bouton 📖 dans le chat.
4. **Utiliser les sélecteurs du contexte**. Le contexte Phase 2 fournit les sélecteurs CSS exacts pour chaque champ.
5. **Confirmer le résultat**. Après l'action, informer l'utilisateur du résultat.
6. **Ne jamais remplir de mots de passe** sans instruction explicite.
7. **Ne jamais soumettre un formulaire de paiement** sans confirmation explicite et détaillée.

## Feedback visuel côté utilisateur

Quand l'agent exécute des actions :
- **Glow bleu pulsant** autour du viewport (bordure bleue #2563eb)
- **Banner** dans le sidepanel : "L'agent prend le contrôle du navigateur..."
- **Message par action** : ✅ ou ❌ avec détail (sélecteur, URL)
- Le glow se désactive 1.5s après la dernière action

## Erreurs courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| "Element non trouvé" | Sélecteur invalide | Vérifier le contexte de page, utiliser un sélecteur différent |
| Pas de réaction au clic | Élément masqué ou désactivé | Vérifier la visibilité, scroller si nécessaire |
| Formulaire pas soumis | Bouton submit hors du sélecteur | Essayer `button[type="submit"]` ou le sélecteur exact |
