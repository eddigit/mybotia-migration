# Instructions : Fix Gmail OAuth Définitif

## CONTEXTE
Le token OAuth pour coachdigitalparis@gmail.com est expiré. Il faut :
1. Renouveler le token maintenant
2. Publier l'app Google Cloud pour éviter l'expiration à 7 jours

---

## PARTIE 1 : Renouveler le token (5 min)

### Étape 1.1 - Lancer le script
```bash
cd ~/.openclaw/workspace && python3 tools/renew_token_coachdigital.py
```

### Étape 1.2 - Suivre les instructions du script
1. Le script affiche un **lien d'autorisation** → Copie-le
2. Ouvre ce lien dans le navigateur
3. Connecte-toi avec **coachdigitalparis@gmail.com**
4. Autorise l'accès Gmail (lecture + envoi)
5. Tu seras redirigé vers une URL comme : `http://localhost/?code=XXXXXX&scope=...`
6. Copie le paramètre **code** de l'URL (tout ce qui est entre `code=` et `&`)
7. Colle ce code dans le terminal quand le script le demande

### Étape 1.3 - Vérifier
```bash
cd ~/.openclaw/workspace && python3 tools/read_emails.py 2 "" "coachdigitalparis"
```
Si ça affiche des emails, c'est bon ✅

---

## PARTIE 2 : Publier l'app Google Cloud (10 min)

### Pourquoi ?
Les apps en mode "Testing" ont des tokens qui expirent après 7 jours.
Publier l'app = tokens permanents.

### Étape 2.1 - Accéder à Google Cloud Console
1. Va sur https://console.cloud.google.com/
2. Connecte-toi avec **coachdigitalparis@gmail.com**
3. Sélectionne le projet **gmail-api-oauth2-486416**

### Étape 2.2 - OAuth Consent Screen
1. Menu hamburger → **APIs & Services** → **OAuth consent screen**
2. Tu devrais voir "Publishing status: Testing"
3. Clique sur **PUBLISH APP**
4. Confirme dans la popup

### Étape 2.3 - Vérification (optionnel pour usage interne)
- Si l'app est uniquement pour toi (usage interne), pas besoin de vérification Google
- Clique "Confirm" si Google demande une vérification
- Pour un usage personnel/interne, sélectionne "Internal" si disponible, sinon "External" sans vérification fonctionne aussi

### Étape 2.4 - Vérifier le statut
- Le statut doit maintenant afficher "Published" ou "In production"
- Les tokens ne expireront plus après 7 jours

---

## VALIDATION FINALE

Teste que tout fonctionne :
```bash
cd ~/.openclaw/workspace && python3 tools/read_emails.py 5 "" "coachdigitalparis"
```

Si des emails s'affichent → **C'est réglé définitivement** ✅

---

## RÉSUMÉ DES CREDENTIALS

- **Compte** : coachdigitalparis@gmail.com
- **Projet Google Cloud** : gmail-api-oauth2-486416
- **Token file** : ~/.openclaw/workspace/tools/gmail-token-coachdigital.json
- **Credentials file** : ~/.openclaw/workspace/tools/gmail-credentials.json

---

*Instructions générées par Iris le 14 février 2026*
