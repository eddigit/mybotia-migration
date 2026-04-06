#!/usr/bin/env python3
"""
read_logs.py — Lecture des logs infrastructure MyBotIA
Usage: python3 tools/read_logs.py <source> [lines] [--errors]
Sources: docker, systemd, monitoring, autofix
Oscar — Directeur des Operations
"""
import subprocess, sys

def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() or r.stderr.strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERREUR: {e}]"

if len(sys.argv) < 2:
    print("Usage: python3 tools/read_logs.py <source> [lines] [--errors]")
    print("Sources: docker, systemd, monitoring, autofix, apache")
    sys.exit(1)

source = sys.argv[1]
lines = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 30
errors_only = "--errors" in sys.argv

if source == "docker":
    cmd = f"docker logs mybotia-gateway --tail {lines} 2>&1"
    if errors_only:
        cmd += " | grep -iE 'error|exception|fatal|fail|crash|panic'"
    print(f"📋 Logs Docker mybotia-gateway (dernières {lines} lignes):")
    print(run(cmd))

elif source == "systemd":
    cmd = f"journalctl --user -u openclaw-gateway-vlmedical --no-pager -n {lines} 2>&1"
    if errors_only:
        cmd += " | grep -iE 'error|exception|fatal|fail|crash'"
    print(f"📋 Logs systemd VL Medical (dernières {lines} lignes):")
    print(run(cmd))

elif source == "monitoring":
    cmd = f"tail -n {lines} /home/gilles/scripts/monitoring/logs/monitoring.log 2>/dev/null"
    if errors_only:
        cmd = f"grep -iE 'alerte|erreur|critical|echec' /home/gilles/scripts/monitoring/logs/monitoring.log | tail -n {lines}"
    print(f"📋 Logs monitoring (dernières {lines} lignes):")
    print(run(cmd))

elif source == "autofix":
    cmd = f"tail -n {lines} /home/gilles/scripts/monitoring/logs/autofix.log 2>/dev/null"
    print(f"📋 Logs auto-fix (dernières {lines} lignes):")
    result = run(cmd)
    print(result if result else "(aucun incident auto-fixe pour le moment)")

elif source == "apache":
    cmd = f"sudo tail -n {lines} /var/log/apache2/error.log 2>/dev/null"
    if errors_only:
        cmd = f"sudo grep -iE 'error|fatal|crit' /var/log/apache2/error.log | tail -n {lines}"
    print(f"📋 Logs Apache (dernières {lines} lignes):")
    print(run(cmd))

else:
    print(f"❌ Source inconnue: {source}")
    print("Sources valides: docker, systemd, monitoring, autofix, apache")
    sys.exit(1)
