#!/usr/bin/env python3
"""
auto_fix.py — Auto-remediation des pannes connues MyBotIA
Usage: python3 tools/auto_fix.py --check | --fix [--dry]
Oscar — Directeur des Operations
"""
import subprocess, json, sys, time, urllib.request

DRY_RUN = "--dry" in sys.argv
FIX_MODE = "--fix" in sys.argv
CHECK_MODE = "--check" in sys.argv or not FIX_MODE

def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)

def http_check(url, timeout=5):
    try:
        resp = urllib.request.urlopen(url, timeout=timeout)
        return resp.status
    except:
        return 0

def execute_fix(name, cmd):
    if DRY_RUN:
        print(f"  [DRY RUN] Commande: {cmd}")
        return True
    print(f"  🔧 Execution: {cmd}")
    rc, out, err = run(cmd, timeout=120)
    if rc == 0:
        print(f"  ✅ Fix applique")
        return True
    else:
        print(f"  ❌ Echec: {err or out}")
        return False

def log_incident(title, diagnostic, action, result):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
[{timestamp}] INCIDENT AUTO-FIX
Titre: {title}
Diagnostic: {diagnostic}
Action: {action}
Resultat: {result}
"""
    try:
        with open("/home/gilles/scripts/monitoring/logs/autofix.log", "a") as f:
            f.write(entry)
    except:
        pass

issues_found = 0
fixes_applied = 0

print("=" * 50)
print("🎖️  OSCAR — Auto-remediation MyBotIA")
print(f"Mode: {'CHECK' if CHECK_MODE and not FIX_MODE else 'FIX'}{' (DRY RUN)' if DRY_RUN else ''}")
print("=" * 50)
print()

# --- CHECK 1: Gateway MyBotIA ---
code = http_check("http://127.0.0.1:18789/health")
if code != 200:
    issues_found += 1
    print(f"❌ Gateway MyBotIA DOWN (HTTP {code})")
    if FIX_MODE:
        print("  Tentative: restart container Docker...")
        if execute_fix("gw-restart", "docker restart mybotia-gateway"):
            time.sleep(15)
            code2 = http_check("http://127.0.0.1:18789/health")
            if code2 == 200:
                fixes_applied += 1
                log_incident("Gateway MyBotIA DOWN", f"HTTP {code}", "docker restart mybotia-gateway", "OK apres restart")
                print(f"  ✅ Gateway repartie (HTTP {code2})")
            else:
                log_incident("Gateway MyBotIA DOWN", f"HTTP {code}", "docker restart mybotia-gateway", f"ECHEC — toujours HTTP {code2}")
                print(f"  ❌ Toujours down apres restart (HTTP {code2}) — ESCALADE")
else:
    print(f"✅ Gateway MyBotIA OK (HTTP {code})")

# --- CHECK 2: Gateway VL Medical ---
code = http_check("http://127.0.0.1:18790/health")
if code != 200:
    issues_found += 1
    print(f"❌ Gateway VL Medical DOWN (HTTP {code})")
    if FIX_MODE:
        print("  Tentative: restart service systemd...")
        if execute_fix("vlmed-restart", "systemctl --user restart openclaw-gateway-vlmedical"):
            time.sleep(15)
            code2 = http_check("http://127.0.0.1:18790/health")
            if code2 == 200:
                fixes_applied += 1
                log_incident("Gateway VL Medical DOWN", f"HTTP {code}", "systemctl restart", "OK")
                print(f"  ✅ Gateway VL Medical repartie (HTTP {code2})")
            else:
                log_incident("Gateway VL Medical DOWN", f"HTTP {code}", "systemctl restart", f"ECHEC — HTTP {code2}")
                print(f"  ❌ Toujours down — ESCALADE")
else:
    print(f"✅ Gateway VL Medical OK (HTTP {code})")

# --- CHECK 3: Python3 dans le container ---
rc, out, err = run("docker exec mybotia-gateway python3 --version")
if rc != 0:
    issues_found += 1
    print(f"❌ Python3 ABSENT du container — outils Lea HS")
    if FIX_MODE:
        print("  Tentative: rebuild image Docker (peut prendre 2 min)...")
        if execute_fix("py-rebuild", "cd /home/gilles/.openclaw/docker && docker compose build && docker compose up -d"):
            time.sleep(20)
            rc2, out2, _ = run("docker exec mybotia-gateway python3 --version")
            if rc2 == 0:
                fixes_applied += 1
                log_incident("Python3 absent container", "python3 not found", "rebuild Docker image", f"OK — {out2}")
                print(f"  ✅ Python3 restaure: {out2}")
            else:
                log_incident("Python3 absent container", "python3 not found", "rebuild Docker image", "ECHEC")
                print(f"  ❌ Rebuild echoue — ESCALADE")
else:
    # Verifier les modules
    rc2, _, err2 = run("docker exec mybotia-gateway python3 -c 'import requests, google.auth, reportlab'")
    if rc2 != 0:
        issues_found += 1
        print(f"⚠️ Python3 OK ({out}) mais modules manquants")
        if FIX_MODE:
            print("  Tentative: rebuild image Docker...")
            execute_fix("py-modules", "cd /home/gilles/.openclaw/docker && docker compose build && docker compose up -d")
    else:
        print(f"✅ Python3 OK ({out}), modules OK")

# --- CHECK 4: RAM ---
rc, out, _ = run("free -m | awk '/Mem:/{printf \"%d %d\", $2, $3}'")
if rc == 0 and out:
    parts = out.split()
    if len(parts) >= 2:
        total, used = int(parts[0]), int(parts[1])
        pct = (used * 100) // total
        if pct >= 90:
            issues_found += 1
            print(f"❌ RAM critique: {pct}%")
            if FIX_MODE:
                print("  Recherche processus orphelins OpenClaw...")
                rc3, procs, _ = run("ps aux | grep 'openclaw' | grep -v grep | grep -v 'mybotia-gateway' | awk '{print $2, $11}'")
                if procs:
                    print(f"  Processus suspects: {procs}")
                    print("  ⚠️ Kill automatique desactive — verification manuelle requise")
        elif pct >= 80:
            print(f"⚠️ RAM elevee: {pct}%")
        else:
            print(f"✅ RAM OK: {pct}%")

# --- RÉSUMÉ ---
print()
print("=" * 50)
if issues_found == 0:
    print("🟢 Aucun probleme detecte")
elif FIX_MODE:
    print(f"📊 {issues_found} probleme(s), {fixes_applied} corrige(s), {issues_found - fixes_applied} restant(s)")
else:
    print(f"📊 {issues_found} probleme(s) detecte(s) — lancer avec --fix pour corriger")

sys.exit(1 if issues_found > fixes_applied else 0)
