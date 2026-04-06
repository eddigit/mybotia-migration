# PROMPT JACQUES — Retour Docker sécurisé (29 mars 2026 - 21h)

> Colle ce prompt à Jacques dans une session Claude Code sur le VPS

---

Jacques, mission critique ce soir. On remet les gateways dans Docker. Le mode nohup c'est un mode dégradé temporaire depuis le 16 mars, on ne reste pas dessus.

## CONTEXTE

- Upgrade 2026.3.28 fait aujourd'hui ✅ — tout fonctionne bien, on ne touche PAS au code ni à la config OpenClaw
- 3 gateways tournent en nohup sur le host (aucune isolation, aucun restart auto)
- Les docker-compose et Dockerfiles sont déjà prêts et à jour
- Objectif : remettre les gateways dans Docker SANS CASSER ce qui a été fait aujourd'hui

## ÉTAT ACTUEL DES PROCESS (à vérifier avant de commencer)

| Gateway | PID | Port | Config |
|---------|-----|------|--------|
| mybotia (Léa+Nina) | 3844986 | 18789 | ~/.openclaw/ |
| vlmedical (Max) | 3844929 | 18790 | ~/.openclaw-vlmedical/ |
| lucy (Lucy) | 3877331 | 18795 | ~/.openclaw-lucy/ |

## DOCKER-COMPOSE EXISTANTS

- **mybotia** : `~/.openclaw/docker/docker-compose.yml` (mem_limit: 4g, port 18789)
- **vlmedical** : `~/.openclaw-vlmedical/docker/docker-compose.yml` (mem_limit: 1536m, port 18790)
- **lucy** : PAS de docker-compose → à créer sur le modèle vlmedical (mem_limit: 1536m, port 18795)

## PROCÉDURE — UNE GATEWAY À LA FOIS

### Ordre : vlmedical → lucy → mybotia (la moins critique d'abord)

Pour CHAQUE gateway :

1. **Vérifier** que le docker-compose est à jour et compatible avec OpenClaw 2026.3.28
2. **Rebuild l'image Docker** (la version node/openclaw a changé depuis le 16 mars)
   ```bash
   cd ~/.openclaw-vlmedical/docker/  # ou le bon répertoire
   docker compose build --no-cache
   ```
3. **Stopper le process nohup** : `kill <PID>`
4. **Attendre 5 secondes** que le port soit libéré
5. **Lancer le container** : `docker compose up -d`
6. **Vérifier** :
   - `docker ps` → container UP + healthy
   - `curl -f http://localhost:<PORT>/health?t=<TOKEN>` → OK
   - WhatsApp connecté (vérifier les logs : `docker logs <container> --tail 20`)
7. **Attendre 2 minutes** de stabilité avant de passer à la suivante

### Pour Lucy (pas de docker-compose existant)

Créer `~/.openclaw-lucy/docker/docker-compose.yml` sur le modèle vlmedical :
- container_name: lucy-gateway
- OPENCLAW_CONFIG_PATH=/home/gilles/.openclaw-lucy/openclaw.json
- OPENCLAW_STATE_DIR=/home/gilles/.openclaw-lucy
- Volume : /home/gilles/.openclaw-lucy:/home/gilles/.openclaw-lucy:rw
- mem_limit: 1536m
- memswap_limit: 3g
- Port 18795
- Healthcheck avec le token Lucy (vérifier dans son openclaw.json)

## ⚠️ POINTS CRITIQUES

1. **NE PAS modifier** les fichiers openclaw.json, les credentials WhatsApp, ni aucune config applicative
2. **NE PAS** `docker compose down` sur les anciens containers arrêtés (ils sont déjà stoppés, on s'en fiche)
3. **Vérifier que OpenClaw 2026.3.28 est bien installé dans l'image** après le build (`docker exec <container> openclaw --version`)
4. **Si un container ne démarre pas** : NE PAS boucler. Arrêter, relancer en nohup comme avant, et m'alerter
5. **Le Dockerfile utilise node:22-alpine** — vérifier que les binaires OpenClaw 2026.3.28 sont compatibles Alpine (npm global)

## ROLLBACK

Si ça merde :
```bash
docker compose down
# Relancer en nohup comme avant :
nohup openclaw gateway &
```

## VALIDATION FINALE

Quand les 3 containers tournent :
```bash
docker ps  # 3 containers UP + healthy
curl -f http://localhost:18789/health?t=67085f007e934ad258db36616d4797d3d3ec916cafef7d44
curl -f http://localhost:18790/health?t=fbbb3632c613522dba34c9065f757a8fa57ab3073d326a49
# + healthcheck Lucy
```

Envoyer un message test à Léa sur WhatsApp pour confirmer que tout passe.

## APRÈS LA MIGRATION

- Stopper les services systemd morts : `sudo systemctl disable openclaw-mybotia.service openclaw-vlmedical.service`
- Mettre à jour le watchdog `gateway-watchdog.sh` pour surveiller les containers Docker (docker ps/health) au lieu des process nohup
- Log dans ta mémoire : "29 mars 21h — Retour Docker sécurisé, 3 gateways containerisées"

---

**C'est une opération propre. Tu ne changes RIEN à ce que tu as fait aujourd'hui. Tu remets juste les gateways dans leurs containers Docker pour l'isolation mémoire et le restart automatique. GO.**
