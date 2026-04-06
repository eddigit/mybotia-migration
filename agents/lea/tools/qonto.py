#!/usr/bin/env python3
import sys
import json
import requests

API = "https://thirdparty.qonto.com/v2"
AUTH = "korzec-gilles-2479:20ec4bb2e78dc3a9838128cec53d1b555a23d39e15aac76dd5a32a6f15edce52"
H = {"Authorization": AUTH}

def get_org():
    return requests.get(f"{API}/organization", headers=H).json()

def get_balance():
    accounts = get_org()["organization"]["bank_accounts"]
    return [{"nom": a.get("name", a["slug"]),
             "iban": a["iban"],
             "solde": a["balance"],
             "devise": a["currency"],
             "statut": a.get("status", "")}
            for a in accounts]

def get_transactions(limit=10):
    slug = get_org()["organization"]["bank_accounts"][0]["slug"]
    r = requests.get(f"{API}/transactions", headers=H,
        params={"slug": slug, "per_page": limit,
                "sorted_by": "settled_at:desc"})
    return [{"date": t.get("settled_at", ""),
             "label": t.get("label", ""),
             "montant": t.get("amount"),
             "sens": t.get("side", ""),
             "categorie": t.get("category", "")}
            for t in r.json().get("transactions", [])]

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "balance"
    if cmd == "balance":
        print(json.dumps(get_balance(), indent=2, ensure_ascii=False))
    elif cmd == "transactions":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print(json.dumps(get_transactions(n), indent=2, ensure_ascii=False))
    elif cmd == "org":
        print(json.dumps(get_org(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": f"Commande inconnue: {cmd}"}))
