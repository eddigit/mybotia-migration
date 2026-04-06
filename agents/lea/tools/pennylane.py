#!/usr/bin/env python3
"""API Pennylane — Gestion devis, factures et clients.

Usage:
  python3 tools/pennylane.py customers                  # Lister les clients
  python3 tools/pennylane.py customers create "Nom" "email"  # Créer un client
  python3 tools/pennylane.py invoices                   # Lister les factures
  python3 tools/pennylane.py quotes                     # Lister les devis
  python3 tools/pennylane.py products                   # Lister les produits
  python3 tools/pennylane.py products create "Nom" 980  # Créer un produit
  python3 tools/pennylane.py invoice create <customer_id> <product_id> <qty>  # Créer une facture
  python3 tools/pennylane.py quote create <customer_id> <product_id> <qty>    # Créer un devis
"""
import sys, os, json, subprocess, urllib.request, urllib.error

BASE_URL = "https://app.pennylane.com/api/external/v2"

def get_token():
    result = subprocess.run(
        ["python3", "tools/get_credential.py", "pennylane", "api_token"],
        capture_output=True, text=True,
        cwd=os.path.expanduser("~/.openclaw/workspace")
    )
    token = result.stdout.strip()
    if not token or "non trouvé" in token:
        print("❌ Token Pennylane non trouvé")
        sys.exit(1)
    return token

def api(method, endpoint, data=None):
    token = get_token()
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ Erreur API ({e.code}): {body}")
        return None

def list_items(endpoint, label):
    result = api("GET", endpoint)
    if not result:
        return
    items = result.get("items", [])
    if not items:
        print(f"Aucun {label} trouvé.")
        return
    print(f"\n📋 {len(items)} {label}(s) :\n")
    for item in items:
        if "name" in item:
            print(f"  [{item.get('id', '?')}] {item['name']} — {item.get('email', item.get('unit_price', ''))}")
        elif "invoice_number" in item:
            print(f"  [{item.get('id', '?')}] {item['invoice_number']} — {item.get('total', '?')}€ — {item.get('status', '?')}")
        elif "quote_number" in item:
            print(f"  [{item.get('id', '?')}] {item['quote_number']} — {item.get('total', '?')}€ — {item.get('status', '?')}")
        else:
            print(f"  [{item.get('id', '?')}] {json.dumps(item, ensure_ascii=False)[:120]}")
    return items

def create_customer(name, email=None, phone=None):
    data = {
        "customer": {
            "customer_type": "company",
            "name": name,
        }
    }
    if email:
        data["customer"]["emails"] = [email]
    if phone:
        data["customer"]["phone"] = phone
    result = api("POST", "customers", data)
    if result:
        print(f"✅ Client créé : [{result.get('id')}] {result.get('name')}")
    return result

def create_product(label, price_ht, vat_rate="FR_200"):
    data = {
        "label": label,
        "unit": "piece",
        "price_before_tax": str(price_ht),
        "vat_rate": vat_rate,
        "currency": "EUR",
    }
    result = api("POST", "products", data)
    if result:
        print(f"✅ Produit créé : [{result.get('id')}] {result.get('label')} — {result.get('price_before_tax')}€ HT")
    return result

def create_invoice(customer_id, product_id, quantity=1, label=None):
    data = {
        "invoice": {
            "customer_id": int(customer_id),
            "date": None,  # today
            "currency": "EUR",
            "line_items": [{
                "product_id": int(product_id),
                "quantity": int(quantity),
            }]
        }
    }
    if label:
        data["invoice"]["line_items"][0]["label"] = label
    result = api("POST", "customer_invoices", data)
    if result:
        num = result.get("invoice_number", "?")
        total = result.get("total", "?")
        print(f"✅ Facture créée : {num} — {total}€")
    return result

def create_quote(customer_id, product_id, quantity=1, label=None):
    data = {
        "quote": {
            "customer_id": int(customer_id),
            "date": None,
            "currency": "EUR",
            "line_items": [{
                "product_id": int(product_id),
                "quantity": int(quantity),
            }]
        }
    }
    if label:
        data["quote"]["line_items"][0]["label"] = label
    result = api("POST", "quotes", data)
    if result:
        num = result.get("quote_number", "?")
        total = result.get("total", "?")
        print(f"✅ Devis créé : {num} — {total}€")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "list"
    
    if cmd == "customers":
        if action == "create" and len(sys.argv) >= 4:
            create_customer(sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
        else:
            list_items("customers", "client")
    
    elif cmd == "invoices":
        if action == "create" and len(sys.argv) >= 5:
            create_invoice(sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else 1)
        else:
            list_items("customer_invoices", "facture")
    
    elif cmd == "quotes":
        if action == "create" and len(sys.argv) >= 5:
            create_quote(sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else 1)
        else:
            list_items("quotes", "devis")
    
    elif cmd == "products":
        if action == "create" and len(sys.argv) >= 5:
            create_product(sys.argv[3], sys.argv[4])
        else:
            list_items("products", "produit")
    
    else:
        print(f"❌ Commande inconnue: {cmd}")
        print(__doc__)
