# HEARTBEAT.md -- Routine de Veille

## A chaque heartbeat (toutes les 30 min)
1. Lis jacques-latest-log.md dans ton workspace pour le dernier etat Jacques CLI
2. Lis jacques-MEMORY.md pour les tendances et problemes connus
3. Si Jacques a detecte un probleme WARN ou CRIT, envoie un resume a Gilles sur Telegram
4. Si tout va bien, ne fais rien (pas de spam)

## A chaque message de Gilles demandant l'etat du serveur
1. Lis jacques-latest-log.md (derniere analyse complete)
2. Lis jacques-MEMORY.md (historique et tendances)
3. Fais tes propres checks si necessaire (docker ps, free -m, df -h)
4. Donne un resume clair et actionnable

## Surveillance proactive
- Si swap > 70% dans les rapports Jacques : alerter Gilles
- Si un container est down depuis plus de 15 min : alerter
- Si WhatsApp reste LOGGED_OUT depuis plus de 24h : rappeler a Gilles
- Si Jacques CLI n'a pas mis a jour ses rapports depuis > 30 min : verifier le cron