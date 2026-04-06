#!/usr/bin/env python3
"""Récupérer un credential depuis PostgreSQL.
Usage: python3 tools/get_credential.py <service> [key_name]
  - Sans key_name : liste toutes les clés du service
  - Avec key_name : affiche la valeur
"""
import sys, subprocess, json

DB_CMD = ["docker", "exec", "prospection_postgres", "psql", "-U", "prospection", "-d", "mybotia_crm", "-t", "-A"]

def query(sql):
    result = subprocess.run(DB_CMD + ["-c", sql], capture_output=True, text=True)
    return result.stdout.strip()

if len(sys.argv) < 2:
    # Liste tous les services
    rows = query("SELECT DISTINCT service FROM credentials ORDER BY service;")
    print("Services disponibles:")
    for r in rows.split('\n'):
        if r: print(f"  {r}")
elif len(sys.argv) == 2:
    service = sys.argv[1]
    rows = query(f"SELECT key_name, key_value, notes FROM credentials WHERE service = '{service}' ORDER BY key_name;")
    if not rows:
        print(f"Service '{service}' non trouvé")
        sys.exit(1)
    for line in rows.split('\n'):
        if '|' in line:
            parts = line.split('|')
            name, value, notes = parts[0], parts[1], parts[2] if len(parts) > 2 else ''
            print(f"  {name}: {value}" + (f"  ({notes})" if notes else ""))
else:
    service, key_name = sys.argv[1], sys.argv[2]
    value = query(f"SELECT key_value FROM credentials WHERE service = '{service}' AND key_name = '{key_name}';")
    if not value:
        print(f"Credential '{service}/{key_name}' non trouvée")
        sys.exit(1)
    print(value)
