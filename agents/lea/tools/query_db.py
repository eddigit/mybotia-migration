#!/usr/bin/env python3
"""Requête en lecture seule sur mybotia_crm (PostgreSQL).

Usage:
  python3 tools/query_db.py tables                    # lister les tables
  python3 tools/query_db.py schema <table>            # schéma d'une table
  python3 tools/query_db.py clients                   # tous les clients
  python3 tools/query_db.py clients actif             # clients par statut
  python3 tools/query_db.py projets                   # tous les projets
  python3 tools/query_db.py paiements                 # tous les paiements
  python3 tools/query_db.py sql "SELECT ..."          # requête SQL libre (SELECT only)
"""
import sys, subprocess

DB_CMD = ["docker", "exec", "prospection_postgres", "psql", "-U", "prospection", "-d", "mybotia_crm"]

def query(sql, expanded=False):
    flags = ["-x"] if expanded else []
    result = subprocess.run(DB_CMD + flags + ["-c", sql], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erreur: {result.stderr.strip()}")
        sys.exit(1)
    print(result.stdout.strip())

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "tables":
        query("\\dt")

    elif cmd == "schema" and len(sys.argv) >= 3:
        query(f"\\d+ {sys.argv[2]}")

    elif cmd == "clients":
        if len(sys.argv) >= 3:
            status = sys.argv[2]
            query(f"SELECT id, nom, status, abonnement, email, telephone, jid_whatsapp FROM clients WHERE LOWER(status) LIKE LOWER('%{status}%') ORDER BY nom;")
        else:
            query("SELECT id, nom, status, abonnement, email, telephone FROM clients ORDER BY nom;")

    elif cmd == "projets":
        query("SELECT id, nom, client_id, statut, montant_total, date_debut FROM projets ORDER BY date_debut DESC LIMIT 30;")

    elif cmd == "paiements":
        query("SELECT id, client_id, montant, statut, date_paiement, methode FROM paiements ORDER BY date_paiement DESC LIMIT 20;")

    elif cmd == "sql" and len(sys.argv) >= 3:
        sql = " ".join(sys.argv[2:]).strip().rstrip(";")
        # Sécurité : lecture seule
        forbidden = ["insert", "update", "delete", "drop", "alter", "truncate", "create", "grant", "revoke"]
        sql_lower = sql.lower()
        for word in forbidden:
            if word in sql_lower.split():
                print(f"Erreur: opération '{word}' interdite. Lecture seule uniquement.")
                sys.exit(1)
        query(sql + ";")

    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
