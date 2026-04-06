#!/usr/bin/env python3
"""
🏛️ RECHERCHE JURIDIQUE UNIFIÉE — Coach Digital Paris
Agrège : Judilibre (Cour de cassation), Légifrance, HUDOC (CEDH), EUR-Lex

Usage:
  python3 legal_search.py judilibre "licenciement abusif"
  python3 legal_search.py legifrance "code travail"
  python3 legal_search.py cedh "France article 6"
  python3 legal_search.py eurlex "protection données personnelles"
  python3 legal_search.py all "droit des contrats"
  python3 legal_search.py status
"""

import sys
import json
import requests
import os
from datetime import datetime

# =============================================
# CONFIGURATION
# =============================================
PISTE_CLIENT_ID     = "f03d31d2-0b86-40e9-825f-13dbaf12d466"
PISTE_CLIENT_SECRET = "6cc0887f-2e23-4965-81ad-7c92cc05cc8a"
PISTE_OAUTH_URL     = "https://sandbox-oauth.piste.gouv.fr/api/oauth/token"
PISTE_API_BASE      = "https://sandbox-api.piste.gouv.fr"

# =============================================
# AUTH PISTE
# =============================================
_piste_token = None

def get_piste_token():
    global _piste_token
    if _piste_token:
        return _piste_token
    r = requests.post(PISTE_OAUTH_URL, data={
        "grant_type": "client_credentials",
        "client_id": PISTE_CLIENT_ID,
        "client_secret": PISTE_CLIENT_SECRET,
        "scope": "openid"
    })
    if r.status_code == 200:
        _piste_token = r.json()["access_token"]
        return _piste_token
    else:
        raise Exception(f"Erreur auth PISTE: {r.status_code} {r.text}")

# =============================================
# 1. JUDILIBRE — Cour de cassation
# =============================================
def search_judilibre(query, max_results=5):
    """Recherche dans la jurisprudence de la Cour de cassation"""
    token = get_piste_token()
    params = {
        "query": query,
        "page_size": max_results,
        "resolve_references": "true"
    }
    r = requests.get(
        f"{PISTE_API_BASE}/cassation/judilibre/v1.0/search",
        headers={"Authorization": f"Bearer {token}"},
        params=params
    )
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}: {r.text[:200]}"}
    
    data = r.json()
    results = []
    for item in data.get("results", []):
        results.append({
            "source": "Cour de cassation (Judilibre)",
            "id": item.get("id"),
            "titre": item.get("title", "Sans titre"),
            "date": item.get("decision_date"),
            "chambre": item.get("chamber"),
            "solution": item.get("solution"),
            "resume": (item.get("summary") or "")[:300],
            "lien": f"https://www.courdecassation.fr/decision/{item.get('id', '')}"
        })
    return {"total": data.get("total", 0), "results": results}

# =============================================
# 2. LÉGIFRANCE — Textes de loi & codes
# =============================================
def search_legifrance(query, max_results=5):
    """Recherche dans les textes de loi via Légifrance (codes + lois/décrets)"""
    token = get_piste_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    all_results = []
    total = 0
    
    # Rechercher dans CODE_ETAT (codes en vigueur) et LODA_ETAT (lois/décrets en vigueur)
    for fond in ["CODE_ETAT", "LODA_ETAT"]:
        payload = {
            "recherche": {
                "query": query,
                "pageNumber": 1,
                "pageSize": max_results,
                "sort": "PERTINENCE",
                "typePagination": "DEFAUT"
            },
            "fond": fond
        }
        r = requests.post(
            f"{PISTE_API_BASE}/dila/legifrance/lf-engine-app/search",
            headers=headers,
            json=payload
        )
        if r.status_code in [200, 206]:
            data = r.json()
            fond_total = data.get("totalResultNumber", 0)
            total += fond_total
            for item in data.get("results", []):
                # Handle nested structure (titles list or direct)
                if "titles" in item:
                    for title_item in item.get("titles", []):
                        all_results.append({
                            "source": f"Légifrance ({fond})",
                            "id": title_item.get("id") or title_item.get("cid"),
                            "titre": title_item.get("title", "Sans titre"),
                            "nature": title_item.get("nature") or title_item.get("legalStatus"),
                            "date": title_item.get("startDate") or title_item.get("lastModificationDate"),
                            "resume": "",
                            "lien": f"https://www.legifrance.gouv.fr/codes/texte_lc/{title_item.get('cid', '')}" if fond == "CODE_ETAT" else f"https://www.legifrance.gouv.fr/loda/id/{title_item.get('id', '')}"
                        })
                else:
                    all_results.append({
                        "source": f"Légifrance ({fond})",
                        "id": item.get("id"),
                        "titre": item.get("title", "Sans titre"),
                        "nature": item.get("nature"),
                        "date": item.get("startDate"),
                        "resume": (item.get("resume") or "")[:300],
                        "lien": f"https://www.legifrance.gouv.fr/loda/id/{item.get('id', '')}"
                    })
    
    return {"total": total, "results": all_results[:max_results]}

def list_codes():
    """Liste tous les codes disponibles dans Légifrance"""
    token = get_piste_token()
    r = requests.post(
        f"{PISTE_API_BASE}/dila/legifrance/lf-engine-app/list/code",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"pageSize": 50, "pageNumber": 1}
    )
    if r.status_code == 200:
        return r.json().get("results", [])
    return []

# =============================================
# 3. HUDOC — Cour Européenne des Droits de l'Homme
# =============================================
def search_cedh(query, max_results=5):
    """Recherche dans la jurisprudence de la CEDH (Cour Européenne des Droits de l'Homme)"""
    params = {
        "query": query,
        "select": "itemid,docname,kpdate,doctypebranch,respondent,conclusion",
        "sort": "kpdate Descending",
        "start": 0,
        "length": max_results
    }
    r = requests.get(
        "https://hudoc.echr.coe.int/app/query/results",
        params=params,
        headers={"Accept": "application/json"}
    )
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}"}
    
    data = r.json()
    results = []
    for item in data.get("results", []):
        doc = item.get("columns", item)
        results.append({
            "source": "CEDH — Cour Européenne des Droits de l'Homme",
            "id": doc.get("itemid"),
            "titre": doc.get("docname", "Sans titre"),
            "date": doc.get("kpdate"),
            "type": doc.get("doctypebranch"),
            "pays": doc.get("respondent"),
            "conclusion": (doc.get("conclusion") or "")[:300],
            "lien": f"https://hudoc.echr.coe.int/eng#{{{doc.get('itemid', '')}}}"
        })
    return {"total": data.get("resultcount", 0), "results": results}

# =============================================
# 4. EUR-LEX — Droit de l'Union Européenne
# =============================================
def search_eurlex(query, max_results=5):
    """Recherche dans le droit européen via EUR-Lex"""
    params = {
        "qid": "1",
        "text": query,
        "scope": "EURLEX",
        "type": "quick",
        "lang": "fr",
        "page": 1,
        "pageSize": max_results
    }
    # EUR-Lex SPARQL / REST API publique
    r = requests.get(
        "https://eur-lex.europa.eu/search.html",
        params=params,
        headers={"Accept": "application/json, text/html"}
    )
    
    # Fallback via l'API de recherche EUR-Lex
    api_url = f"https://eur-lex.europa.eu/search.html?qid=1&text={requests.utils.quote(query)}&scope=EURLEX&type=quick&lang=fr&andText0=&toDate=&fromDate=&typeDocument=&SUBDOM_INIT=ALL_ALL&DTS_SUBDOM=ALL_ALL"
    
    if r.status_code in [200, 202]:
        return {
            "total": "N/A",
            "results": [{
                "source": "EUR-Lex (Droit UE)",
                "info": f"Recherche disponible sur EUR-Lex",
                "lien": api_url,
                "note": "EUR-Lex ne fournit pas d'API JSON simple — accès via navigateur recommandé"
            }]
        }
    return {"error": f"HTTP {r.status_code}"}

# =============================================
# 5. STATUS — Vérification de toutes les connexions
# =============================================
def check_status():
    print("\n🏛️  STATUT DES CONNEXIONS JURIDIQUES")
    print("=" * 50)
    
    # PISTE Auth
    try:
        token = get_piste_token()
        print(f"✅ PISTE.gouv.fr — Auth OK (token: {token[:20]}...)")
    except Exception as e:
        print(f"❌ PISTE.gouv.fr — Auth ERREUR: {e}")
        token = None
    
    # Judilibre
    if token:
        r = requests.get(
            f"{PISTE_API_BASE}/cassation/judilibre/v1.0/healthcheck",
            headers={"Authorization": f"Bearer {token}"}
        )
        if r.status_code == 200:
            print(f"✅ Judilibre (Cour de cassation) — {r.json().get('status', 'OK')}")
        else:
            print(f"⚠️  Judilibre — HTTP {r.status_code}")
    
    # Légifrance
    if token:
        r = requests.post(
            f"{PISTE_API_BASE}/dila/legifrance/lf-engine-app/list/code",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"pageSize": 1, "pageNumber": 1}
        )
        if r.status_code == 200 and r.json().get("results"):
            print(f"✅ Légifrance (Textes de loi) — OK ({len(r.json()['results'])} code testé)")
        else:
            print(f"⚠️  Légifrance — HTTP {r.status_code}")
    
    # HUDOC (CEDH)
    r = requests.get(
        "https://hudoc.echr.coe.int/app/query/results",
        params={"query": "test", "select": "itemid,docname", "sort": "kpdate Descending", "start": 0, "length": 1},
        headers={"Accept": "application/json"}
    )
    if r.status_code == 200:
        count = r.json().get("resultcount", 0)
        print(f"✅ HUDOC — CEDH (Cour Européenne des Droits de l'Homme) — {count} arrêts disponibles")
    else:
        print(f"❌ HUDOC CEDH — HTTP {r.status_code}")
    
    # EUR-Lex
    r = requests.get("https://eur-lex.europa.eu/search.html?qid=1&text=test&scope=EURLEX&type=quick&lang=fr")
    if r.status_code in [200, 202]:
        print(f"✅ EUR-Lex (Droit de l'Union Européenne) — Accessible")
    else:
        print(f"❌ EUR-Lex — HTTP {r.status_code}")
    
    print("\n📋 SOURCES NON DISPONIBLES (pas d'API publique) :")
    print("   ⚠️  Barreau de Paris / CNB — pas d'API disponible")
    print("   ⚠️  Cours d'appel — décisions non publiées en API")
    print("   ⚠️  PISTE Production — nécessite activation par la DILA")
    print("\n💡 Pour activer PISTE en production : contacter api@dila.gouv.fr")
    print("=" * 50)

# =============================================
# MAIN
# =============================================
def print_results(data, source_name):
    if "error" in data:
        print(f"❌ Erreur {source_name}: {data['error']}")
        return
    total = data.get("total", "?")
    results = data.get("results", [])
    print(f"\n📚 {source_name} — {total} résultat(s) total, {len(results)} affichés")
    print("-" * 50)
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r.get('titre', r.get('info', 'Sans titre'))}")
        for key in ["date", "chambre", "solution", "pays", "type", "nature", "note"]:
            if r.get(key):
                print(f"    {key.capitalize()}: {r[key]}")
        if r.get("resume") or r.get("conclusion"):
            text = r.get("resume") or r.get("conclusion")
            print(f"    Résumé: {text[:200]}...")
        if r.get("lien"):
            print(f"    🔗 {r['lien']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    query = sys.argv[2] if len(sys.argv) > 2 else ""
    max_r = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    if command == "status":
        check_status()
    
    elif command == "judilibre":
        print(f"🔍 Recherche Judilibre (Cour de cassation) : '{query}'")
        print_results(search_judilibre(query, max_r), "Judilibre")
    
    elif command == "legifrance":
        print(f"🔍 Recherche Légifrance : '{query}'")
        print_results(search_legifrance(query, max_r), "Légifrance")
    
    elif command == "codes":
        print("📋 Codes disponibles dans Légifrance :")
        codes = list_codes()
        for c in codes:
            print(f"  • {c.get('title')} [{c.get('id')}]")
    
    elif command == "cedh":
        print(f"🔍 Recherche CEDH (HUDOC) : '{query}'")
        print_results(search_cedh(query, max_r), "CEDH — HUDOC")
    
    elif command == "eurlex":
        print(f"🔍 Recherche EUR-Lex : '{query}'")
        print_results(search_eurlex(query, max_r), "EUR-Lex")
    
    elif command == "all":
        print(f"🔍 Recherche multi-sources : '{query}'")
        print_results(search_judilibre(query, 3), "Judilibre (Cour de cassation)")
        print_results(search_legifrance(query, 3), "Légifrance")
        print_results(search_cedh(query, 3), "CEDH — HUDOC")
        print_results(search_eurlex(query, 2), "EUR-Lex")
    
    else:
        print(f"Commande inconnue : {command}")
        print(__doc__)
