# CONFIG-LEA-VPS (21 fev 2026)

# VPS SERVEUR

| Composant | Specs |
| --- | --- |
| Hostname | vps116827.serveur-vps.net |
| IP | 180.149.198.23 |
| OS | Debian 13 |
| CPU | Intel Xeon E5-2620 v4 |
| RAM | 8 Go |
| Disque | 79 Go (57 Go libres au 21/02) |
| User | gilles (groupe sudo) |
| Node.js | v22.22.0 |

# OPENCLAW

- Version: **2026.2.19** (stable, MaJ 21 fev 2026, depuis 2026.2.17)
- Port: 18789
- Bind: **loopback** (127.0.0.1 uniquement)
- Modele: **claude-opus-4-6** (via OAuth Claude Max x20)
- Auth LLM: OAuth Claude Max x20 (PAS de cle API standard)
- URL publique: **https://app.mybotia.com** (SSL Let's Encrypt)
- URL interne: ws://127.0.0.1:18789
- Gateway Token: 67085f007e934ad258db36616d4797d3d3ec916cafef7d44
- Config: gateway.remote.url = wss://app.mybotia.com
- Service: systemd (enabled, user gilles)

# ARCHITECTURE RESEAU

```
Internet → https://app.mybotia.com (Apache SSL, port 443)
                    ↓ ProxyPass ws://
           127.0.0.1:18789 (OpenClaw Gateway, loopback only)
                    ↓
           Agents → Anthropic API (OAuth Claude Max x20)
```

# AGENTS

| Agent | ID | Canal | Bot Telegram | Heartbeat |
|-------|----|-------|--------------|-----------|
| Lea | main | WhatsApp + WebChat | @lea_admin_bot | 30min |
| Julian | julian | Telegram | @julian_expert_bot | off |
| Nina | nina | WebChat | - | off |
| Oscar | oscar | Telegram | @oscar_coachdigital_bot | off |

# WHATSAPP

- Numero: +33 7 56 96 86 33
- Status: Connecte (linked=true)
- JID: 33756968633:12@s.whatsapp.net

# DOMAINES

- mybotia.com (principal)
- app.mybotia.com (gateway OpenClaw SSL)
- lea.mybotia.com, julian.mybotia.com, nina.mybotia.com, oscar.mybotia.com (prevus)

# ACCES SSH

| Host ID | User | IP | Note |
|---------|------|----|------|
| vps-coachdigital | gilles | 180.149.198.23:22 | sudo avec mdp |
| gillescoach@wsl-local | gillescoach | localhost:22 | WSL local |

Note: root SSH desactive (PermitRootLogin=no). Utiliser gilles + sudo.

# SAUVEGARDES

- ~/.openclaw/openclaw.json.bak-20260221
- ~/.openclaw/workspace.bak-20260221/
- /etc/apache2/sites-available/app-mybotia-le-ssl.conf.bak-20260221
