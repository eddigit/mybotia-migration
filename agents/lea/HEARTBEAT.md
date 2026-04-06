# HEARTBEAT.md — Checklist récurrente Léa

## Vérification modèle actif

1. Exécute session_status
2. Vérifie le champ provider/model
3. Si le modèle actif n'est PAS un modèle anthropic → envoie immédiatement un message WhatsApp à +33652345180 :

"🚨 ALERTE : Je ne suis plus sur Anthropic. Modèle actif : [nom du modèle]. Le Max x20 a peut-être sauté. Action requise."

4. Si le modèle est bien anthropic → HEARTBEAT_OK (ne dis rien)

## Canal partagé Jacques

5. Lire `/home/gilles/.openclaw/shared/jacques-to-lea.md`
6. Si messages avec Status: PENDING → les traiter et répondre dans `/home/gilles/.openclaw/shared/lea-to-jacques.md`
7. Si rien de nouveau → ne rien faire
