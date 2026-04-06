#!/usr/bin/env python3
"""
health_check.py — Diagnostic complet infrastructure MyBotIA
Usage: python3 tools/health_check.py [--quick] [--json]
Oscar — Directeur des Opérations
"""
import subprocess, json, sys, urllib.request, urllib.error, ssl

CHECKS = []
ctx = ssl._create_unverified_context()

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)

def check(name, status, msg):
    CHECKS.append({"name": name, "status": status, "msg": msg})
    icon = {"ok": "✅", "warn": "⚠️", "critical": "❌"}.get(status, "❓")
    if not JSON_MODE:
        print(f"{icon} {name}: {msg}")

def http_check(url, timeout=5):
    try:
        req = urllib.request.Request(url, method="GET")
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except:
        return 0

# --- CHECKS ---

def check_gateway_mybotia():
    code = http_check("http://127.0.0.1:18789/health")
    if code == 200:
        check("Gateway MyBotIA (18789)", "ok", f"HTTP {code}")
    else:
        check("Gateway MyBotIA (18789)", "critical", f"HTTP {code} — DOWN")

def check_gateway_vlmedical():
    code = http_check("http://127.0.0.1:18790/health")
    if code == 200:
        check("Gateway VL Medical (18790)", "ok", f"HTTP {code}")
    else:
        check("Gateway VL Medical (18790)", "critical", f"HTTP {code} — DOWN")

def check_docker():
    rc, out, err = run("docker ps --filter name=mybotia-gateway --format '{{.Status}}'")
    if rc == 0 and out:
        if "healthy" in out.lower():
            check("Docker mybotia-gateway", "ok", out)
        elif "starting" in out.lower():
            check("Docker mybotia-gateway", "warn", f"En démarrage: {out}")
        else:
            check("Docker mybotia-gateway", "warn", out)
    else:
        check("Docker mybotia-gateway", "critical", "Container introuvable ou Docker inaccessible")

def check_systemd():
    rc, out, err = run("systemctl --user is-active openclaw-gateway-vlmedical 2>/dev/null")
    if out.strip() == "active":
        check("Systemd VL Medical", "ok", "Service actif")
    else:
        check("Systemd VL Medical", "critical", f"Service: {out.strip() or 'inconnu'}")

def check_python_tools():
    rc, out, err = run("docker exec mybotia-gateway python3 --version")
    if rc != 0:
        check("Python3 (container)", "critical", "ABSENT — outils Léa HS")
        return
    version = out.strip()
    rc2, out2, err2 = run("docker exec mybotia-gateway python3 -c \"import requests, google.auth, reportlab; print('OK')\"")
    if rc2 != 0:
        check("Python3 (container)", "critical", f"{version} mais modules manquants: {err2}")
    else:
        check("Python3 (container)", "ok", f"{version}, modules OK")

def check_whatsapp():
    rc, out, err = run("openclaw channels status --json 2>/dev/null")
    if rc != 0:
        check("WhatsApp", "warn", "Impossible de vérifier (CLI error)")
        return
    try:
        data = json.loads(out)
        wa = data.get("channels", {}).get("whatsapp", {})
        linked = wa.get("linked", False)
        connected = wa.get("connected", False)
        if linked and connected:
            check("WhatsApp", "ok", "Linked et connecté")
        elif linked:
            check("WhatsApp", "warn", "Linked mais pas connecté")
        else:
            check("WhatsApp", "critical", f"DÉCONNECTÉ (linked={linked})")
    except:
        check("WhatsApp", "warn", "Impossible de parser le statut")

def check_ram():
    rc, out, err = run("free -m | awk '/Mem:/{printf \"%d %d %d\", $2, $3, $7}'")
    if rc == 0 and out:
        parts = out.split()
        if len(parts) >= 3:
            total, used, avail = int(parts[0]), int(parts[1]), int(parts[2])
            pct = (used * 100) // total
            if pct >= 80:
                check("RAM", "critical", f"{pct}% ({avail}Mo dispo sur {total}Mo)")
            elif pct >= 70:
                check("RAM", "warn", f"{pct}% ({avail}Mo dispo sur {total}Mo)")
            else:
                check("RAM", "ok", f"{pct}% ({avail}Mo dispo sur {total}Mo)")
            return
    check("RAM", "warn", "Impossible de vérifier")

def check_disk():
    rc, out, err = run("df / | awk 'NR==2{gsub(/%/,\"\"); print $5}'")
    if rc == 0 and out:
        pct = int(out.strip())
        if pct >= 85:
            check("Disque", "critical", f"{pct}% utilisé")
        elif pct >= 75:
            check("Disque", "warn", f"{pct}% utilisé")
        else:
            check("Disque", "ok", f"{pct}% utilisé")
    else:
        check("Disque", "warn", "Impossible de vérifier")

def check_telegram_bots():
    bots = {
        "lea": "<TELEGRAM_BOT_TOKEN_LEA>",
        "julian": "<TELEGRAM_BOT_TOKEN_JULIAN>",
        "oscar": "<TELEGRAM_BOT_TOKEN_OSCAR>",
        "max": "<TELEGRAM_BOT_TOKEN_VLMEDICAL>",
    }
    issues = []
    for name, token in bots.items():
        try:
            url = f"https://api.telegram.org/bot{token}/getMe"
            resp = urllib.request.urlopen(url, timeout=5, context=ctx)
            data = json.loads(resp.read())
            if not data.get("ok"):
                issues.append(name)
        except:
            issues.append(name)
    if not issues:
        check("Telegram bots", "ok", f"Tous en ligne ({', '.join(bots.keys())})")
    else:
        check("Telegram bots", "critical", f"Problème: {', '.join(issues)}")

# --- MAIN ---

QUICK_MODE = "--quick" in sys.argv
JSON_MODE = "--json" in sys.argv

if not JSON_MODE:
    print("=" * 50)
    print("🎖️  OSCAR — Diagnostic Infrastructure MyBotIA")
    print("=" * 50)
    print()

# Checks critiques (toujours)
check_gateway_mybotia()
check_gateway_vlmedical()
check_docker()
check_whatsapp()
check_python_tools()
check_ram()

if not QUICK_MODE:
    check_disk()
    check_systemd()
    check_telegram_bots()

if JSON_MODE:
    print(json.dumps({"checks": CHECKS, "quick": QUICK_MODE}, indent=2, ensure_ascii=False))
else:
    print()
    criticals = [c for c in CHECKS if c["status"] == "critical"]
    warns = [c for c in CHECKS if c["status"] == "warn"]
    if criticals:
        print(f"🔴 {len(criticals)} CRITIQUE(S) — action requise")
    elif warns:
        print(f"🟡 {len(warns)} WARNING(S) — à surveiller")
    else:
        print("🟢 TOUT OK")

sys.exit(1 if any(c["status"] == "critical" for c in CHECKS) else 0)
