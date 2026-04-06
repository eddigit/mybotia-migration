#!/usr/bin/env python3
"""
Quota Manager — Budget journalier par groupe WhatsApp
Usage:
  python3 tools/quota_manager.py check <session_key>    → vérifie si le quota est OK
  python3 tools/quota_manager.py status                  → affiche tous les quotas du jour
  python3 tools/quota_manager.py topup <session_key>     → ajoute un forfait de 3€ (GO Gilles requis)
  python3 tools/quota_manager.py reset                   → reset quotas (nouveau jour)
  python3 tools/quota_manager.py set-limit <amount>      → change la limite par défaut
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path

QUOTA_FILE = Path(__file__).parent.parent / "memory" / "quotas.json"
DEFAULT_LIMIT_EUR = 3.00
# Sessions exemptées (Gilles = illimité)
EXEMPT_SESSIONS = [
    "agent:main:main",  # Telegram Gilles
    "agent:main:chat-",  # Webchat (Gilles direct)
]
# Préfixes de sessions WhatsApp groupe à surveiller
TRACKED_PREFIX = "agent:main:whatsapp:group:"


def load_quotas():
    if QUOTA_FILE.exists():
        with open(QUOTA_FILE) as f:
            data = json.load(f)
        # Reset si c'est un nouveau jour
        if data.get("date") != str(date.today()):
            data = {"date": str(date.today()), "limit_eur": data.get("limit_eur", DEFAULT_LIMIT_EUR), "groups": {}}
            save_quotas(data)
        return data
    return {"date": str(date.today()), "limit_eur": DEFAULT_LIMIT_EUR, "groups": {}}


def save_quotas(data):
    QUOTA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUOTA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_exempt(session_key):
    for prefix in EXEMPT_SESSIONS:
        if session_key.startswith(prefix):
            return True
    return False


def is_tracked(session_key):
    return session_key.startswith(TRACKED_PREFIX)


def get_group_id(session_key):
    # Extract JID from session key like "agent:main:whatsapp:group:120363...@g.us"
    parts = session_key.split(":")
    if len(parts) >= 5:
        return parts[4]
    return session_key


def check_quota(session_key):
    """Check if a session is within budget. Returns (allowed, message)"""
    if is_exempt(session_key):
        return True, "exempt"

    if not is_tracked(session_key):
        return True, "not_tracked"

    data = load_quotas()
    group_id = get_group_id(session_key)
    group_data = data.get("groups", {}).get(group_id, {"spent": 0, "topups": 0, "blocked_at": None})

    limit = data.get("limit_eur", DEFAULT_LIMIT_EUR)
    total_budget = limit + (group_data.get("topups", 0) * limit)
    spent = group_data.get("spent", 0)

    if spent >= total_budget:
        return False, "BLOCKED"

    remaining = total_budget - spent
    return True, f"ok (reste {remaining:.2f}€)"


def update_spent(session_key, cost_usd):
    """Update spent amount for a group (cost in USD, stored in EUR ~= USD for simplicity)"""
    if not is_tracked(session_key):
        return

    data = load_quotas()
    group_id = get_group_id(session_key)

    if "groups" not in data:
        data["groups"] = {}
    if group_id not in data["groups"]:
        data["groups"][group_id] = {"spent": 0, "topups": 0, "blocked_at": None}

    data["groups"][group_id]["spent"] = round(data["groups"][group_id]["spent"] + cost_usd, 4)

    # Check if just exceeded
    limit = data.get("limit_eur", DEFAULT_LIMIT_EUR)
    total_budget = limit + (data["groups"][group_id].get("topups", 0) * limit)
    if data["groups"][group_id]["spent"] >= total_budget and not data["groups"][group_id].get("blocked_at"):
        data["groups"][group_id]["blocked_at"] = datetime.now().isoformat()

    save_quotas(data)


def topup(session_key):
    """Add one more quota block of 3€"""
    data = load_quotas()
    group_id = get_group_id(session_key) if is_tracked(session_key) else session_key

    if "groups" not in data:
        data["groups"] = {}
    if group_id not in data["groups"]:
        data["groups"][group_id] = {"spent": 0, "topups": 0, "blocked_at": None}

    data["groups"][group_id]["topups"] = data["groups"][group_id].get("topups", 0) + 1
    data["groups"][group_id]["blocked_at"] = None
    save_quotas(data)

    limit = data.get("limit_eur", DEFAULT_LIMIT_EUR)
    total = limit + (data["groups"][group_id]["topups"] * limit)
    print(f"✅ Forfait ajouté pour {group_id}. Nouveau budget: {total:.2f}€")


def show_status():
    """Show all quotas for today"""
    data = load_quotas()
    limit = data.get("limit_eur", DEFAULT_LIMIT_EUR)
    print(f"📊 Quotas du {data.get('date', 'N/A')} — Limite par défaut: {limit:.2f}€\n")

    groups = data.get("groups", {})
    if not groups:
        print("Aucun groupe n'a consommé de tokens aujourd'hui.")
        return

    for gid, gdata in sorted(groups.items(), key=lambda x: x[1].get("spent", 0), reverse=True):
        spent = gdata.get("spent", 0)
        topups = gdata.get("topups", 0)
        total_budget = limit + (topups * limit)
        blocked = gdata.get("blocked_at")
        status = "🔴 BLOQUÉ" if blocked else ("🟡 >80%" if spent / total_budget > 0.8 else "🟢 OK")
        print(f"  {gid}: {spent:.2f}€ / {total_budget:.2f}€ {status}")


def sync_from_sessions():
    """Sync costs from OpenClaw session data (run periodically)"""
    import subprocess
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "call", "sessions.list",
             "--token", "67085f007e934ad258db36616d4797d3d3ec916cafef7d44",
             "--url", "ws://127.0.0.1:18789", "--json"],
            capture_output=True, text=True, timeout=15
        )
        sessions_data = json.loads(result.stdout)
        sessions = sessions_data.get("result", {}).get("sessions", [])

        data = load_quotas()
        today = str(date.today())

        for s in sessions:
            key = s.get("key", "")
            if not is_tracked(key):
                continue

            cost = s.get("estimatedCostUsd", 0)
            group_id = get_group_id(key)

            # Only count today's costs (approximate: we reset daily)
            if "groups" not in data:
                data["groups"] = {}
            if group_id not in data["groups"]:
                data["groups"][group_id] = {"spent": 0, "topups": 0, "blocked_at": None}

            # Store the session cost (overwrite, not accumulate - sessions track total)
            data["groups"][group_id]["session_cost"] = round(cost, 4)

        save_quotas(data)
        print("✅ Sync OK")
    except Exception as e:
        print(f"❌ Sync error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "check":
        if len(sys.argv) < 3:
            print("Usage: quota_manager.py check <session_key>")
            sys.exit(1)
        allowed, msg = check_quota(sys.argv[2])
        print(f"{'✅ ALLOWED' if allowed else '🔴 BLOCKED'}: {msg}")
        sys.exit(0 if allowed else 1)

    elif cmd == "status":
        show_status()

    elif cmd == "topup":
        if len(sys.argv) < 3:
            print("Usage: quota_manager.py topup <session_key_or_group_jid>")
            sys.exit(1)
        topup(sys.argv[2])

    elif cmd == "reset":
        save_quotas({"date": str(date.today()), "limit_eur": DEFAULT_LIMIT_EUR, "groups": {}})
        print("✅ Quotas réinitialisés")

    elif cmd == "set-limit":
        if len(sys.argv) < 3:
            print("Usage: quota_manager.py set-limit <amount_eur>")
            sys.exit(1)
        data = load_quotas()
        data["limit_eur"] = float(sys.argv[2])
        save_quotas(data)
        print(f"✅ Limite fixée à {data['limit_eur']:.2f}€")

    elif cmd == "sync":
        sync_from_sessions()

    else:
        print(__doc__)
